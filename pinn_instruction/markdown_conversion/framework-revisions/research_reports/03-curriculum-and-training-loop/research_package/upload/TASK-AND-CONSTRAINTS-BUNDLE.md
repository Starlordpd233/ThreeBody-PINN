# Task And Constraints Bundle

Build date: 2026-06-18. This is a mechanical transport bundle for the
doc-03 research package. Content between BEGIN/END delimiters is
byte-identical to the source package parts, verified at build time by
round-trip extraction and SHA-256 comparison. The wrapper text is not a
source edit and does not summarize the enclosed files.

## Contents

| File | Bytes | SHA-256 |
|------|-------|---------|
| `scope-12-hard-constraints.md` | 6,931 | `736475ea84d017df966d7dfada3061870fdf9144257e6fb5f34978e68368f157` |
| `framed-research-questions.md` | 29,957 | `ea9c23a4ea9ead32426d3a32087fe1e9013590b8c1b6051f721c4db8983e78d7` |
| `resolution-doc-skeleton.md` | 6,118 | `bef2163e14a21c3d51ae6d799e217c2a94bd22f461eb0ec1e4605be82a41d0a9` |

===== BEGIN FILE scope-12-hard-constraints.md (6931 bytes, sha256 736475ea84d017df966d7dfada3061870fdf9144257e6fb5f34978e68368f157) =====
# Hard Constraints — Locked v1.4 + v1.5 Outcomes (the SCOPE-12 set)

> **Treatment class:** AUTHORED upload companion. Reference any other companion or
> snapshot by **bare filename** only. This preamble is a hard-constraints contract for
> the external research: the items below are **already decided and locked**. They are
> NOT open questions, NOT part of this adjudication, and may NOT be re-opened by the
> research. The contested/open questions live in `framed-research-questions.md`; the
> figure-grounding table lives in `claims-register.md`; the verified dataset anchors
> live in `verified-facts-reference.md`.

The doc-03 (curriculum + training loop) adjudication runs **on top of** two prior locked
milestones: doc-01 (architecture + physics foundations) and doc-02 (data pipeline +
validation). Their outcomes are settled framework conventions. The research must treat
every item in this file as a fixed boundary condition and reconcile its answers **to**
these constraints — never against them.

---

## 1. Locked v1.4 + v1.5 outcomes (verbatim — hard constraints)

These are stated verbatim as the locked grounding set. Respect them; do not re-derive,
re-open, or contradict any of them.

1. **14D network input `[τ, IC₁₃]`.** The network input is exactly 14 dimensions:
   the normalized time `τ = 2u − 1` (autograd leaf `u = t/T`) concatenated with the
   13-component initial-condition vector `IC₁₃`.

2. **Jacobi-state `IC₁₃`.** `IC₁₃` is the fixed-gauge Jacobi-state initial-condition
   encoding (raw ordered masses + Jacobi position/velocity scalars + energy), produced
   by the locked preprocessing pipeline (COM removal, zero-momentum boost, canonical
   ordering, canonical rotation gauge). It is redundant-but-reconstructive and is not
   justified by constraint counting (locked Phase 19, PHYS-06).

3. **Mass-weighted COM projection head.** A hard mass-weighted center-of-mass
   projection head is applied to the 9D position output **before** any loss or metric is
   evaluated; linear momentum is enforced structurally by this head, so no separate
   linear-momentum loss term exists.

4. **PHYS-03 training-time softening `eps_soft = 1e-5`.** The training-time Plummer
   softening parameter is `ε_train = 1e-5`, applied identically in the physics-residual
   force term and the energy regularizer (matched-Plummer form
   `r_safe = sqrt(‖Δr′‖² + ε_train²)`). Additive `(‖r‖ + ε)` softening on the distance
   norm is the PHYS-03 anti-pattern and is prohibited.

5. **Post-v1.3 SCS gate `ε_H > 10⁻⁵` / `SCS > −5`.** The self-consistency / energy-gate
   thresholds adopted post-v1.3 are locked: the energy-denominator floor regime
   `ε_H > 10⁻⁵` and the screening gate `SCS > −5`.

6. **PHYS-01 raw-mass `D ≈ 4.6416`.** The characteristic length scale is
   `D = (G·T²)^(1/3) ≈ 4.6416` (with `G = 1`), derived from **raw-mass**
   non-dimensionalization (raw masses `mᵢ`, not mass fractions). The alternative
   total-mass form `D = (G·M_tot·T²)^(1/3) ≈ 6.694` (with `M_tot = 3`) was **rejected**
   by v1.5 Phase 25 (EVID-10) and is documented as a future-only framework-wide rewrite,
   never adopted. **`D ≈ 4.6416` is locked; `D = 6.694` is not selectable.**

7. **v1.5 data-side contracts PIPE-01..10 / VAL-01..04.** The v1.5 DataLoader,
   stage-query, and validation-metric contracts are locked: the stage-query interface
   (`sample_replay(n, max_stage)`, `sample_lookahead(n, stage)`, `has_stage(k)`), the
   trajectory-admission gate, the blacklist-exclusion and quality-metric (SASD / IPR /
   PSC) contracts, and the validation-metric definitions. The research consumes these as
   fixed inputs.

---

## 2. Live-code citations are OVERRIDDEN (the source-of-truth override)

issue-03 carries "Canonical" citations of two live implementation files —
`data-processing-pipeline-full.py` and `basic_architecture.py`. **These citations are
overridden and carry no authority for this adjudication.** The live implementation code
is **not** a grounding source. Where issue-03 cites those two files as canonical
(for IC-vector assembly, stage assignment, `get_batch()`, the SIREN implementation, or
any other contract), the **framework specs are the source of truth** — specifically the
two spec-edit targets `ctl_instruction.md` and `pinn_architecture.md`, plus the locked
conventions in items 1–7 above. Any divergence between the live code and the specs is
resolved in favor of the specs; the code is reconciled later, outside this adjudication.

---

## 3. Locked hard constraints vs. revisable baseline (read this carefully)

Two different categories of spec content travel in this package, and the research must
NOT conflate them:

- **Locked hard constraints (items 1–7 above).** Fixed. Not in scope. Not re-openable.
  These are the SCOPE-12-locked v1.4 + v1.5 outcomes.

- **Revisable current doc-03 design state (the baseline).** The **current positions** in
  `ctl_instruction.md` and `pinn_architecture.md` on the doc-03 training-loop contracts —
  curriculum staging, batch construction (replay/lookahead, data-fidelity vs.
  collocation), stage-transition criteria, loss scaling and the loss-weight schedule,
  the `τ_L` / `L_max` formulas, and gradient clipping — are the **baseline / current
  design state**. They are the genuinely-open spec-edit targets of this adjudication and
  **may be revised** by the resolution the research informs. Treat them as the current
  baseline to critique against, not as locked law.

The research's job is to reconcile the revisable baseline **under** the locked hard
constraints. A proposed change to a revisable contract is in scope; a proposed change to
a locked hard constraint is out of scope and must be surfaced as a conflict, not adopted.

**Worked example of the distinction (the `D` case).** The *value* `D ≈ 4.6416` is a
locked hard constraint (item 6) — not open. What *is* open is how issue-03's `τ_L` /
`L_max` derivation re-derives **given** that locked `D`. So "which `D` is correct" is
settled (it is `4.6416`); "how the `τ_L` formula reconciles under `D ≈ 4.6416`" is the
open reconciliation question (see `framed-research-questions.md`). The same locked-vs-open
split applies to the softening parameter: the loss-side `eps_soft = 1e-5` (item 4) is
locked, while whether a distinct static-context softening coexists with it is open.

---

## 4. Findings out of scope for this adjudication (declined at the consolidation gate)

**None.** No candidate finding was declined at the consolidation gate; in particular the
ALM `μ_p`-clamp finding is **included** as its own framed question, so it retains a
resolution path. (This slot exists so that any finding declined in a future revision is
recorded here as "out of scope for this adjudication," with the downstream consequence
noted. At present there are no such declined findings.)

===== END FILE scope-12-hard-constraints.md =====

===== BEGIN FILE framed-research-questions.md (29957 bytes, sha256 ea9c23a4ea9ead32426d3a32087fe1e9013590b8c1b6051f721c4db8983e78d7) =====
# Framed Research Questions — doc-03 Curriculum and Training Loop

> **Treatment class:** AUTHORED upload companion. Reference every other companion or
> snapshot by **bare filename** only — no repository paths. The hard-constraints
> contract is in `scope-12-hard-constraints.md`; the figure-grounding table (every
> `CLM-NN` below resolves to a row there) is in `claims-register.md`; the verified
> dataset anchors are in `verified-facts-reference.md`. The non-binding output skeleton
> is in `resolution-doc-skeleton.md`.

## How to read these questions

Each question states **two positions** and asks you to adjudicate between them without
presupposing an answer:

- **Issue-doc position** — what `03-curriculum-and-training-loop.md` (the adjudication
  subject) says. **This document is NON-authoritative.** It is a consolidated audit; it
  and its own "Recommended Resolutions" may contain errors. Do not treat its recommended
  resolution as the verdict.
- **Framework-spec position** — what the current framework specs (`ctl_instruction.md`,
  `pinn_architecture.md`) say, cited by **bare filename + section anchor** so the
  paraphrase is grounded, not asserted. These are the **revisable baseline** for the
  doc-03 contracts (see `scope-12-hard-constraints.md` §3), except where a value is a
  locked hard constraint (called out per question).

**The worked seed-conflict.** The `D = 6.694` vs `D ≈ 4.6416` case (its own section
below) is the canonical example of why the issue doc is non-authoritative: the issue doc
states `D = 6.694` as a "corrected" value, but it conflicts with the locked raw-mass
`D ≈ 4.6416` and was rejected by v1.5 Phase 25 (EVID-10). Read every issue-doc figure
through that lens.

**Where the attached materials are silent or ambiguous, record the gap** (in your
output, against the relevant `claims-register.md` row) — **do not invent** a value, a
threshold, or a derivation. Unverified figures are unverified inputs, not facts; v1.6 has
no in-milestone phase that verifies them (see `claims-register.md`).

**Three decisions are explicitly left unsettled here and require framework-owner
approval** — referred to throughout by descriptive name: **the causal-training-mode
decision**, **the s_min-frame decision**, and **the epsilon-strategy decision**. Pose
options; do not pick one.

---

## Section 2 — Decisions Requiring Human Approval

### The causal-training-mode decision (unsettled — framework-owner approval required)

**What is being decided.** How the training loop handles temporal causality across the
collocation time domain `[0, T]`. This is the single most consequential training-loop
decision and is **posed unsettled**.

**Options on the table (state all three; recommend none):**
- **Option A — per-time-step causal weighting.** Exponential weights
  `w_i ∝ exp(−λ Σ_{j<i} L_j)` enforce a strict arrow of time. Issue-doc risk: a
  "Causal Firewall" — an early stiffness spike drives all subsequent weights to zero.
- **Option B — global sampling + ALM.** Sample time points globally from `[0, T]`, no
  causal weighting; ALM sees the full constraint-violation field. Issue-doc risk:
  temporal-causality violation — late-time gradients propagate through unresolved
  early-time dynamics.
- **Option C — time-windowed causal-ALM hybrid.** Partition `[0, T]` into overlapping
  causal windows with localized ALM, hard convergence gating, and state propagation
  between windows. Most complex; the issue doc presents it as resolving both failure
  modes but notes it is an end-to-end rewrite of the Adam phase.

**Issue-doc position.** `03-curriculum-and-training-loop.md` calls Option B the "current
SOT" and keeps the decision open, while flagging that the Causal-Training-Mismatch
blueprint recommends Option C; it asks the framework owner to choose and to record
Option B (if chosen) as an intentional departure from the blueprint.

**Framework-spec position.** Note a divergence the research must surface rather than
silently resolve: `ctl_instruction.md` § "Loss Function Formulation" / "Phase 2: Total
Training Loss" already adopts **causal weighting** as the PHYS-05 default
(`w_n = exp(−η_c · Σ_{m<n} stopgrad(R̄_m))`, `η_c = 1`) and **explicitly rejects** the
previous pseudo-ALM formulation `L_data + λ_p·L_phys + (μ_p/2)·L_phys² + λ_E·L_energy` as
not representing a standard augmented Lagrangian; optional ALM survives only as a P2
ablation on **scalar** conservation constraints (`pinn_architecture.md §4.2`), and
`pinn_architecture.md §3.2 / §4.1` carries the same causal-weighting default. The issue
doc's "global + ALM is current SOT" framing therefore does **not** match the current
spec's causal-weighting-plus-no-dense-ALM baseline.

**Open question (neutral).** Given that the spec baseline is causal weighting with ALM
confined to scalar constraints, and the issue doc frames the choice as A vs B vs C: which
causal-training mode should the framework adopt, and how is it reconciled with the
existing PHYS-05 causal-weighting default and the rejection of dense-residual ALM? State
both positions; do not presuppose a verdict. Figures referenced: none beyond the
design-constant context (the dense-residual is the heart of the physics loss; no dataset
figure gates this).

### The s_min-frame decision (unsettled — framework-owner approval required)

**What is being decided.** Whether the collision-criterion separation `s_min` is used in
**unsoftened** geometric form for the curriculum stage gate while a **softened** form is
used inside the training-loss collision criterion — or softened everywhere.

**Options on the table:**
- **Option A (matches the spec baseline):** unsoftened `s_min` for the curriculum stage
  gate (a true geometric close-encounter detector); `max(s_min, eps_soft = 1e-5)` inside
  the training-loss collision criterion; always log the unsoftened value for diagnostics.
- **Option B:** use softened `max(s_min, eps)` everywhere.

**Issue-doc position.** `03-curriculum-and-training-loop.md` states the SOT is already
internally consistent (unsoftened `s_min` for the gate, softened in the loss) and frames
this as documentation cleanup; it recommends Option A but leaves the frame open for
explicit approval, and preserves the unsoftened-everywhere alternative under "Considered
Alternatives."

**Framework-spec position.** `ctl_instruction.md` § "Step 3" item 1 defines `s_min` from
"true pairwise separations (no softening)" — explicitly an unsoftened geometric quantity
— while the static-invariant potential uses the Plummer form with `ε_inv = 1e-10`, and
the training-time residual/energy use `ε_train = 1e-5` (`pinn_architecture.md §3.2`,
`§3.4`). The spec already separates the unsoftened geometric `s_min` from the softened
loss potentials.

**Open question (neutral).** Confirm or revise the s_min frame: unsoftened gate +
softened loss (Option A) vs. softened everywhere (Option B), stated as both positions
with no presupposed verdict. (Note: the s_min-frame decision is distinct from the D5
stage-transition finding below — both legitimately appear in this set.)

### The epsilon-strategy decision (unsettled — framework-owner approval required)

> **LOCKED vs OPEN delineation — read first.**
>
> - **LOCKED (not re-openable; SCOPE-12 hard constraint, `claims-register.md` CLM-19,
>   PHYS-03).** The **training-loss-side** softening is `eps_soft = 1e-5`, applied
>   identically in the physics residual and the energy regularizer. This value is fixed
>   and is **not** part of this decision. Do **not** frame any question as "which loss-side
>   epsilon is correct."
> - **OPEN (the genuine reconciliation question).** Whether a **distinct
>   static/invariant-computation softening** (`ε_inv = 1e-10`, used offline for invariant
>   computation — `E`, `Q`, stage assignment) legitimately **coexists** with the locked
>   loss-side `eps_soft = 1e-5` (the "dual-context" arrangement), versus collapsing both
>   contexts to a single value.

**What is being decided.** Only the OPEN part above: the relationship between the
static/invariant-computation softening and the locked training-loss softening — not the
training-loss value itself.

**Options on the table (scoped to the OPEN part):**
- **Option A:** `1e-5` everywhere (including static invariant computation), citing the
  argument that `1e-10` is numerically indistinguishable from zero in double precision.
  Trade-off: changes the invariant computation (`E`, `Q`, stage assignment) to softened
  physics.
- **Option B (dual-context):** `ε_inv = 1e-10` for static invariants (offline, float64)
  and the locked `eps_soft = 1e-5` for the dynamic training loss (GPU). Trade-off: the
  curriculum gate and the loss operate on slightly different physics.
- **Option C:** tighten everything to `1e-10` — the issue doc records a substantive
  scientific argument *against* this.

**Issue-doc position.** `03-curriculum-and-training-loop.md` flags an internal SOT
contradiction: one source mandates `1e-5` for **all** calculations (with the
double-precision argument against `1e-10`), while the invariant-computation step uses
`1e-10` and its justification text is truncated/incomplete. It asks the owner to resolve
the five-order-of-magnitude split.

**Framework-spec position.** `ctl_instruction.md` § "Step 3" item 1 states the
static-invariant softening `ε_inv = 1e-10` is "context-specific for offline invariant
computation and is distinct from the training-time softening `ε_train = 1e-5`";
`pinn_architecture.md §3.2 / §3.4` fixes `ε_train = 1e-5` in the residual and energy
contracts, and `pinn_architecture.md §3.4` adds a dual-epsilon visibility note separating
the data-side validation `ε_inv = 1e-10` from the training-time `ε_train = 1e-5`. The
spec baseline is therefore already a dual-context arrangement with the **loss side locked
at `1e-5`**.

**Open question (neutral).** Given the locked loss-side `eps_soft = 1e-5`, should the
static/invariant softening remain a distinct `1e-10` (dual-context, Option B), collapse
into `1e-5` (Option A), or be unified at `1e-10` (Option C — argued against)? Frame this
as the **static-context reconciliation under the locked loss-side value**, never as
"which epsilon is correct." Figure referenced: the locked loss-side value is `CLM-19`'s
companion constraint (PHYS-03); state it as fixed.

---

## Section 3 — Confirmed Findings (BLOCKING and MAJOR)

### B-07 — Replay/lookahead batch construction not implemented

**Issue-doc position.** `03-curriculum-and-training-loop.md` finding B-07 (BLOCKING):
the current `get_batch()` uses a flat random draw of trajectories; the CTL design requires
a two-phase sampler — 240 replay trajectories from stages `≤ k` plus 16 lookahead
trajectories from stage `k+1`, with 32 points/trajectory split 50/50
uniform/acceleration-weighted (audit §6). Replay/lookahead counts `CLM-12`.

**Framework-spec position.** `ctl_instruction.md` § "Mini-Batch Construction with
Lookahead Sampling" specifies the replay/lookahead split (replay `B_≤k = 240`, lookahead
`B_{k+1} = 16` for batch size 256) and `n_pts(traj) = min(n_pts_cap, n_snapshots)` with
`n_pts_cap` default 32 and the 50/50 weighted/uniform composition; `pinn_architecture.md
§3.1` shows the legacy `get_batch(batch_size, points_per_trajectory=32)` that B-07 flags
as not yet implementing replay/lookahead (`N_data = 256 × 32 = 8192`, `CLM-12`).

**Open question (neutral).** Confirm the replay/lookahead batch-construction contract
(counts, per-trajectory point count, 50/50 composition) against the spec baseline, and
identify any reconciliation needed between the audit §6 pseudocode and the
`ctl_instruction.md` mini-batch contract. Counts are claimed design constants (`CLM-12`),
not verified.

### B-08 — Data-fidelity and collocation points conflated

**Issue-doc position.** B-08 (BLOCKING): the CTL design does not separate data-fidelity
points (must match Brutus snapshots, L1) from collocation points (anywhere in `[0, T]`,
physics + energy). Fix: two independent point sets — 8192 data-fidelity points (L1) and
4096 collocation points (physics+energy), both 50/50 sampled (`CLM-12`).

**Framework-spec position.** `pinn_architecture.md §3.1` defines the data-fidelity term
(Huber on scaled projected positions, `N_data = 256 × 32 = 8192`) and `§3.2` defines the
physics residual on collocation points; `ctl_instruction.md` § "Loss Function
Formulation" composes them. The spec does carry distinct data and collocation roles, but
B-08 flags that the **separate-point-set** discipline (independent 8192 / 4096 sets) is
not reconciled into the batch constructor (`CLM-12`).

**Open question (neutral).** Confirm whether the two-independent-point-set contract
(8192 data-fidelity L1; 4096 collocation physics+energy) should be made explicit in the
batch constructor, and how it reconciles with the current `pinn_architecture.md §3.1`
data term and `§3.2` collocation residual. State both positions.

### M6 — `L_norm` lacks clamping before IC-vector mapping

**Issue-doc position.** M6 (MAJOR): `L_norm` can numerically exceed 1, producing a
normalized IC component > 1 after the `2x − 1` mapping; fix is `np.clip(L_norm, 0, 1)`
before mapping.

**Framework-spec position.** `ctl_instruction.md` § "Step 3" item 2 defines
`L_norm = L / L_max` with the `compute_L_norm` reference returning `L / (L_max + eps)`;
`ctl_instruction.md` § "Step 4" retains `L_norm` as a **metadata** descriptor (staging,
diagnostics, loss scaling) and states the invariant-heavy quantities are **no longer
final network IC slots** under the Phase 17 input contract.

**Open question (neutral).** Given that `L_norm` is now metadata (not an IC slot under
the locked 14D `[τ, IC₁₃]` contract), confirm where the clamping discipline applies —
whether M6's clamp is still required for the staging/diagnostic use of `L_norm`, and
whether any normalized-range guard remains relevant. State both positions; do not assume
the IC-vector-mapping framing still holds.

### M7 — `τ_L` computed but excluded from the IC vector

**Issue-doc position.** M7 (MAJOR): Lyapunov time `τ_L` is computed but dropped from the
IC vector with no documented decision; the issue doc recommends **excluding `τ_L` from
the IC vector by design** (a derived dynamical property, not an IC invariant), using it
only for stage gating and evaluation.

**Framework-spec position.** `ctl_instruction.md` § "Step 3" returns `τ_L` in the
invariant tuple and uses `(E, Q, s_min, L_norm, τ_L)` for **default stage gating**;
§ "Step 4" excludes the invariant-heavy descriptors (including `τ_L`) from the final
`IC₁₃` network slots, consistent with the locked 14D Jacobi-state input contract.

**Open question (neutral).** Confirm M7: that `τ_L` is excluded from `IC₁₃` by design and
retained only for staging/evaluation, reconciled with the locked Jacobi-state input
contract. State both positions.

### M14 — Gradient-clipping spec divergence (PINN median-based vs CTL C-schedule)

**Issue-doc position.** M14 (MAJOR): two gradient-clipping strategies are documented
independently — PINN median-based adaptive clipping vs. a CTL curriculum-aware `C`
schedule. Fix: merge as `clip_value = C_stage · median(grad_norm_history)`, with
`C_stage` from the CTL schedule (`C_table` claimed `8.5 / 5.0 / 3.0`, `CLM-10`) and the
median over the PINN rolling window.

**Framework-spec position.** `pinn_architecture.md §4.4` specifies median-based clipping
at **`5.0 × median`** of the last 100 gradient norms; `ctl_instruction.md` § "Adaptive
Median-Based Gradient Clipping" specifies the curriculum-aware `C` schedule
(stages 0–1: `7–10`; 2–3: `5`; 4–6: `3`). The two specs carry the two halves M14 wants
merged; the `C`-schedule values are the baseline behind the issue-doc `C_table` (`CLM-10`).

**Open question (neutral).** Confirm the merged clipping contract `C_stage · median(·)`,
reconciling the fixed `5.0` factor in `pinn_architecture.md §4.4` with the per-stage `C`
schedule in `ctl_instruction.md`, and the claimed `C_table` values (`CLM-10`). State both
positions.

### M15 — Energy-loss weight may overwhelm; capped-hybrid schedule

**Issue-doc position.** M15 (MAJOR): `λ_E` (up to 1000 at Stage 6) risks overwhelming
physics/data terms; fix is a capped-hybrid schedule `λ_E(k) = min(10^(k−3), cap[k])` with
`cap_table = {0:1, 1:5, 2:20, 3:50, 4:100, 5:200, 6:500}` (`CLM-11`), plus a safeguard to
reduce `λ_E` when the energy term dominates.

**Framework-spec position.** `pinn_architecture.md §4.1` (PHYS-05) gives the current
loss-weight baseline: `λ_E^max(k) = λ_L^max(k) = {0 for k∈{0,1}; 10^{k−4} for k∈{2,3,4};
1 for k∈{5,6}}`, with linear warmup over `I_warm = min(2000, 0.1·N_Adam,k)`. The current
spec schedule **differs** from the issue-doc capped-hybrid `cap_table` (`CLM-11`).

**Open question (neutral).** Reconcile the energy-loss weight schedule: the issue-doc
capped-hybrid `cap_table` (`CLM-11`) vs. the current PHYS-05 `λ_E^max(k)` warmup schedule
in `pinn_architecture.md §4.1`, including whether the dominance safeguard is adopted.
State both positions; the `cap_table` figures are claimed design constants (`CLM-11`).

### M16 — `dt_out`-aware collocation scaling

**Issue-doc position.** M16 (MAJOR): `dt_out` varies ~17× across variants but collocation
density is uniform; fix (audit-verbatim direction) is to scale collocation as
`n_col ∝ dt_base / dt_out`. The issue doc explicitly preserves the `dt_base/dt_out`
direction and flags that the inverse `dt_out/dt_base` form would be a separate methodology
change.

**Framework-spec position.** `ctl_instruction.md` § "Mini-Batch Construction with
Lookahead Sampling" exposes `n_snapshots(traj)` and `dt_out(traj)` as loader metadata and
explicitly labels the M16 collocation-density question as a **deferred, forward-interface**
item ("not used here") — i.e. the spec carries the hook but defers the scaling rule to
doc-03. Per-variant `dt_out` values are **verified** (`CLM-17`: std 0.17 / hier 0.08 /
gold 0.01 — see `verified-facts-reference.md`); the stage-table `dt_out` figures depend on
those.

**Open question (neutral).** Confirm the `dt_out`-aware collocation-scaling rule
(`n_col ∝ dt_base/dt_out`, audit-verbatim direction) and where it lands in the spec, using
the verified per-variant `dt_out` (`CLM-17`). State both positions; flag that the inverse
direction is a distinct methodology change.

### D5 — Stage-transition criteria unattainable; dual-path fallback

**Issue-doc position.** D5 (MAJOR): the strict transition criteria (monotonic validation
loss) are theoretically unattainable with limited data; fix is a dual-path advance
(strict: plateau + validation-stable + physics-residual + energy-drift; fallback:
max-epochs `{0:500…6:1200}` (`CLM-09`), stagnation, NaN rollback) plus a Stage-0 pilot to
calibrate. Per-stage `epsilon_phys/epsilon_energy` thresholds (`5e-3 … 1e-4`, `CLM-08`)
are explicitly "not fixed."

**Framework-spec position.** `ctl_instruction.md` § "Stage Transition Criteria" lists
**four** strict criteria (training-loss plateau `ε_plateau = 1e-5`, patience 200;
validation-loss stability; physics-residual `ε_phys = 1e-4`; energy-drift `ε_energy = 1e-4`
using the locked `ε_H = 1e-4·S_H` floor) and carries an author note questioning their
attainability with limited data — but does **not** yet encode the fallback path or the
per-stage threshold table that D5 proposes.

**Open question (neutral).** Confirm the dual-path stage-transition contract (strict +
fallback) and the per-stage threshold table (`CLM-08`, `CLM-09`), reconciling with the
current four strict criteria in `ctl_instruction.md`. State both positions; the threshold
and max-epochs figures are claimed-unverified design hypotheses (`CLM-08`, `CLM-09`).

### NS-12 — Componentwise AD for velocities/accelerations

**Issue-doc position.** NS-12 (MAJOR): the sources say velocities/accelerations are
derived via AD but give no concrete three-body PyTorch implementation; fix is the
component-wise AD requirement (do not differentiate the summed 9D output as a proxy for
per-coordinate acceleration).

**Framework-spec position.** `pinn_architecture.md §5.3.1` (PHYS-02) is the canonical
componentwise normalized-time AD contract: it requires all nine `dr'_{i,α}/du`,
**forbids** the `torch.autograd.grad(r.sum(), u, …)` anti-pattern, lists acceptable
patterns (`jacrev` + `vmap`, explicit per-component loop, full-Jacobian), and gives a
worked synthetic-trajectory derivative test. The spec already encodes NS-12's requirement.

**Open question (neutral).** Confirm that the PHYS-02 componentwise AD contract in
`pinn_architecture.md §5.3.1` fully satisfies NS-12 (no summed-output proxy), and whether
any concrete three-body collocation-batch detail remains open. State both positions.

### NS-13 — Huber energy δ = 1.0 too large; tune from `|ΔH|` quantiles

**Issue-doc position.** NS-13 (MAJOR): the spec'd Huber `δ = 1.0` for the energy loss is
uncalibrated for normalized Hamiltonian residuals and may behave like L2 over the whole
expected range; fix is to tune `δ` from observed normalized `|ΔH|` quantiles (start
`≈ 0.01–0.1`, per stage).

**Framework-spec position.** `pinn_architecture.md §3.4` fixes the energy regularizer
Huber transition at `δ = 1.0` (PHYS-04), with the relative drift `ΔH_n` normalized by
`|H_ε(r_0)| + ε_H` and the locked floor `ε_H = 1e-4·S_H`. The current spec uses the
`δ = 1.0` that NS-13 questions.

**Open question (neutral).** Reconcile the energy-loss Huber `δ`: the spec baseline
`δ = 1.0` (`pinn_architecture.md §3.4`) vs. the NS-13 quantile-tuned `δ ≈ 0.01–0.1`,
including whether `δ` becomes stage-dependent. State both positions.

### NS-18 — Loss-component scaling contract across L_data / L_physics / L_energy

**Issue-doc position.** NS-18 (MAJOR): the loss components need an explicit scaling
contract so all terms operate in the same dimensionless coordinate system — `L_data` on
scaled positions `r' = r/D` (`CLM-19` locked `D`) with L1/MAE; `L_physics` on collocation
points with componentwise AD accelerations and `eps_soft = 1e-5`; `L_energy` on the same
collocation set with `dr'/du` and the same `eps_soft = 1e-5`.

**Framework-spec position.** `pinn_architecture.md §3.1` (data term, Huber on scaled
positions), `§3.2` (physics residual, `ε_train = 1e-5`, causal weighting), `§3.4` (energy
regularizer, same `ε_train = 1e-5`), and `§4.1` (PHYS-05 total-loss composition) together
define the scaling/units contract; the data term in the current spec is a **Huber**
contract (replacing the earlier MAE/L1 prose), which differs from the issue-doc's L1/MAE
framing.

**Open question (neutral).** Confirm the loss-component scaling/units contract across
`L_data` / `L_physics` / `L_energy`, reconciling the issue-doc L1/MAE data-loss framing
with the current `pinn_architecture.md §3.1` Huber data contract, under the locked `D`
(`CLM-19`) and locked `eps_soft = 1e-5`. State both positions.

---

## Section 6 / `stage_strat_revision.md` — Data-Driven Adaptive Stage Assignment

### Adaptive stage-assignment methodology

**Issue-doc position.** `03-curriculum-and-training-loop.md` § "Data-Driven Adaptive
Stage Assignment" proposes replacing fixed theoretical thresholds with data-adaptive
criteria: EDA over all trajectories' invariants, correlation/PCA, K-means (`k = 6–7`)
clustering, quantile thresholds, a `>10%`-per-stage population safeguard, and a small
PINN pilot; it augments (not replaces) `assign_curriculum_stage()`. The deep-dive
methodology lives in the baseline report `stage_strat_revision.md`.

**Framework-spec position.** `ctl_instruction.md` § "Step 5: Curriculum Stage Assignment"
and § "Multi-Stage Data Stratification by Difficulty" define the current threshold-based
stage assignment keyed by `record_key` over the admitted set; the per-stage population
counts are claimed-unverified (`CLM-02..CLM-07`). The adaptive methodology is the
revisable baseline to critique against (`stage_strat_revision.md` carries a
baseline-critique mandate).

**Open question (neutral).** Adjudicate the data-driven adaptive stage-assignment
methodology against the current threshold-based `ctl_instruction.md` Step 5: which stage
boundaries, clustering/quantile criteria, and population safeguards land in the spec, and
how they reconcile with the locked stage-query contracts (PIPE-01..10). The per-stage
trajectory counts are claimed-unverified inputs (`CLM-02..CLM-07`); do not treat them as
fact.

---

## Section 7 — `τ_L` and `L_max` Formula Resolution + the `D` conflict

### `D = 6.694` vs `D ≈ 4.6416` (the worked seed-conflict)

> **LOCKED vs OPEN delineation — read first.**
>
> - **LOCKED (not re-openable; SCOPE-12 hard constraint, `claims-register.md` CLM-19,
>   PHYS-01).** The characteristic length scale is `D ≈ 4.6416`
>   (`D = (G·T²)^(1/3)`, raw-mass convention). The total-mass form `D = 6.694`
>   (`D = cbrt(G·M_tot·T²)`, `M_tot = 3`) was **rejected by v1.5 Phase 25 (EVID-10)** and
>   is documented as a future-only rewrite. Do **not** frame any question as "which `D`
>   is correct" — that is settled.
> - **OPEN (the genuine reconciliation question).** How issue-03's `τ_L` / `L_max`
>   derivation **re-derives under the locked `D ≈ 4.6416`** — i.e., the propagation of the
>   locked value through the formulas, not the value itself.

**Issue-doc position.** `03-curriculum-and-training-loop.md` § "τ_L and L_max Formula
Resolution" uses `D = np.cbrt(G · M_tot_ref · T_scale²) = 6.694` (`M_tot_ref = 3.0`,
`T_scale = 10`) in the `compute_tau_L` shadow-trajectory routine, and states `D = 6.694`
as a "corrected B-02 formula" (`CLM-01`, claimed-unverified). **This is the canonical
example of the issue doc being non-authoritative:** the value conflicts with the locked
convention.

**Framework-spec position.** `ctl_instruction.md §2.5` ("Global scaling") locks
`D = (G·T²)^(1/3) ≈ 4.6416` (with `G = 1`), raw-mass nondimensionalization, PHYS-01 /
PIPE-09; it documents the `D = 6.694` mass-fraction alternative as **rejected as a
pipeline instruction** ("no configuration parameter may select the mass-fraction form")
and cites the EVID-10 adjudication. `D ≈ 4.6416` is `CLM-19` (`verified` / locked).

**Open question (neutral, scoped to the OPEN part).** Given the **locked** `D ≈ 4.6416`,
how does issue-03's `τ_L` / `L_max` derivation reconcile — i.e., re-derive the
`compute_tau_L` / `L_max` formulas under `D ≈ 4.6416` (not `6.694`), and identify any
downstream stage-threshold consequences. Both values (`6.694` claimed `CLM-01`; `4.6416`
locked `CLM-19`) appear so the conflict is fully registered; only the reconciliation
**under the locked value** is open.

### `τ_L` and `L_max` computation formulas

**Issue-doc position.** § "τ_L and L_max Formula Resolution" resolves `L_max = M_total ·
r_char · v_char` (with `v_char = sqrt(2|E|/M_total)`) and `τ_L = 1/λ_max` via
shadow-trajectory divergence (perturb by `epsilon_pert = 1e-8`, integrate nominal +
perturbed, track exponential separation; potential softening `epsilon_soft = 1e-10`),
plus a faster PCA+Rosenstein batch approximation for ~15K trajectories.

**Framework-spec position.** `ctl_instruction.md` § "Step 3" item 2 gives the canonical
`L_max = M_tot · r_char · v_char` with `v_char = sqrt(2|E|/M_tot)` and
`L_norm = L/L_max` (the `compute_L_norm` reference); the spec does not yet inline the
shadow-trajectory `τ_L` routine with the split `epsilon_pert = 1e-8` / `epsilon_soft =
1e-10`. Note the split softening here (`epsilon_pert = 1e-8` perturbation magnitude;
`epsilon_soft = 1e-10` static potential softening) is **distinct** from the locked
training-loss `eps_soft = 1e-5` — these are different contexts (see the epsilon-strategy
decision and `scope-12-hard-constraints.md`).

**Open question (neutral).** Confirm the `τ_L` / `L_max` computation contracts — the
`L_max` formula, the shadow-trajectory `τ_L` method with split `epsilon_pert = 1e-8` /
`epsilon_soft = 1e-10`, and the PCA+Rosenstein batch approximation — landing in the spec
under the locked `D ≈ 4.6416` (`CLM-19`). State both positions; do not collapse the split
static softening into the locked loss-side `1e-5`.

---

## Section 15 / ALM Parameter Update — the `μ_p`-clamp finding

### ALM `μ_p` clamp

**Issue-doc position.** `03-curriculum-and-training-loop.md` § "ALM Parameter Update
Specification" (MINOR/INFO) notes `μ_p` can diverge without bounds; fix is
`μ_p = np.clip(μ_p, 1e-4, 100.0)` in the ALM update (lower bound prevents physics
enforcement from decaying to zero; upper bound prevents overwhelming the data term).

**Framework-spec position.** The current spec **rejects** the dense-residual pseudo-ALM
formulation (`ctl_instruction.md` § "Loss Function Formulation") and confines ALM to a
**P2 ablation on scalar conservation constraints only** (`pinn_architecture.md §4.2`),
with dual updates only between Adam epochs / refinement passes and never inside L-BFGS.
The `μ_p`-clamp finding therefore attaches to the optional ALM ablation, not the baseline
loss.

**Open question (neutral).** Confirm whether the `μ_p`-clamp (`[1e-4, 100.0]`) applies to
the surviving P2 scalar-constraint ALM ablation (`pinn_architecture.md §4.2`), given that
dense-residual ALM is rejected — i.e., where (if anywhere) the clamp lands now. State both
positions.

---

*All inline figures reference a `CLM-NN` ID resolving to a row in `claims-register.md`.
Where the attached materials are silent or ambiguous, record the gap against the relevant
claims-register row — do not invent. The three decisions named by description above and
the `D` conflict are posed unsettled; nothing here presupposes a verdict.*

===== END FILE framed-research-questions.md =====

===== BEGIN FILE resolution-doc-skeleton.md (6118 bytes, sha256 bef2163e14a21c3d51ae6d799e217c2a94bd22f461eb0ec1e4605be82a41d0a9) =====
# Resolution-Doc Skeleton (NON-BINDING) — doc-03 Curriculum and Training Loop

> **NON-BINDING.** The resolution doc remains the framework owner's product. This skeleton
> is a **suggestion only** — it exists to ease coverage-checking (so every framed question
> has a visible verdict slot) and to carry the downstream finding → adjudication-phase
> mapping. **No schema is mandated.** You may structure the resolution doc however you
> prefer; the v1.4 and v1.5 resolution docs are offered only as **format precedents**, not
> as a required template.
>
> **Treatment class:** AUTHORED upload companion. Reference companions by **bare filename**
> only. The questions this skeleton mirrors live in `framed-research-questions.md`; the hard
> constraints in `scope-12-hard-constraints.md`; the figure register in `claims-register.md`.

## Format precedents (suggestion only — no schema required)

- **v1.4 resolution doc:** `ctl_pinn_resolution.md` — the doc-01 (architecture + physics
  foundations) resolution doc. A workable per-finding verdict format.
- **v1.5 resolution doc:** `02-resolution-doc.md` — the doc-02 (data pipeline + validation)
  resolution doc. The most recent precedent; same package family.

Either is a fine model. Adopt, adapt, or ignore the structure below as you see fit.

## Downstream adjudication-phase map (where each verdict lands)

Each resolved finding feeds a later v1.6 adjudication phase. The mapping below is a guide so
the verdict is written with its destination spec contract in mind. Spec-edit targets are
`ctl_instruction.md` and `pinn_architecture.md` only.

| Finding cluster | Adjudication phase | Primary spec-edit target |
|-----------------|--------------------|--------------------------|
| Cross-milestone / cross-source conflicts (root-cause adjudication) — the `D` conflict; the three named decisions | **Phase 32** (root-cause adjudication / evidence) | both targets, as adjudicated |
| Curriculum / staging / `τ_L` / `L_max` / stage transitions (CURR cluster) | **Phase 33** | `ctl_instruction.md` |
| Training-loop mechanics: batch construction, loss composition, causal mode (LOOP cluster) | **Phase 34** | `ctl_instruction.md` + `pinn_architecture.md` |
| Loss scaling / weights / gradient clipping / softening (LOSS cluster) | **Phase 35** | `pinn_architecture.md` |
| Source-issue / cross-reference reconciliation | **Phase 36** (FUT hand-off) | both targets / FUT |

---

## Per-finding verdict slots (one per framed question)

> Fill each slot with the adjudicated verdict, the evidence, and the resulting spec edit.
> Leave the locked sub-parts marked LOCKED (do not re-open). Slots are ordered as in
> `framed-research-questions.md` (issue-03 section order).

### The causal-training-mode decision  → Phase 32 / Phase 34
- **Verdict:** _(per-time-step A / global+ALM B / time-windowed hybrid C — owner's choice)_
- **Reconciliation note:** how the choice relates to the existing PHYS-05 causal-weighting
  default and the rejection of dense-residual ALM.

### The s_min-frame decision  → Phase 32 / Phase 33
- **Verdict:** _(unsoftened gate + softened loss / softened everywhere)_
- **Note:** distinct from the D5 stage-transition finding.

### The epsilon-strategy decision  → Phase 32 / Phase 35
- **LOCKED:** loss-side `eps_soft = 1e-5` (not re-openable; `claims-register.md` CLM-19 /
  PHYS-03).
- **Verdict (OPEN part only):** static/invariant-softening reconciliation under the locked
  loss-side value — dual-context `1e-10` / collapse to `1e-5` / unify at `1e-10`.

### B-07 — replay/lookahead batch construction  → Phase 34
- **Verdict / spec edit:** _(replay/lookahead counts, per-trajectory points, 50/50)_

### B-08 — data-fidelity vs collocation point separation  → Phase 34
- **Verdict / spec edit:** _(two independent point sets contract)_

### M6 — `L_norm` clamping  → Phase 33
- **Verdict / spec edit:** _(clamp discipline given `L_norm` is now metadata)_

### M7 — `τ_L` excluded from IC vector  → Phase 33
- **Verdict / spec edit:** _(confirm exclusion by design under the locked 14D contract)_

### M14 — merged gradient clipping  → Phase 35
- **Verdict / spec edit:** _(`C_stage · median(·)`; reconcile `5.0` factor vs `C` schedule)_

### M15 — energy-loss weight schedule  → Phase 35
- **Verdict / spec edit:** _(capped-hybrid `cap_table` vs PHYS-05 warmup `λ_E^max(k)`)_

### M16 — `dt_out`-aware collocation scaling  → Phase 33 / Phase 35
- **Verdict / spec edit:** _(`n_col ∝ dt_base/dt_out`; verified `dt_out` from CLM-17)_

### D5 — stage-transition dual-path  → Phase 33
- **Verdict / spec edit:** _(strict + fallback; per-stage thresholds CLM-08 / max-epochs CLM-09)_

### NS-12 — componentwise AD  → Phase 34
- **Verdict / spec edit:** _(confirm PHYS-02 componentwise AD satisfies NS-12)_

### NS-13 — Huber energy δ  → Phase 35
- **Verdict / spec edit:** _(δ = 1.0 baseline vs quantile-tuned 0.01–0.1)_

### NS-18 — loss-component scaling contract  → Phase 35
- **Verdict / spec edit:** _(units contract across L_data / L_physics / L_energy)_

### Data-driven adaptive stage assignment  → Phase 33
- **Verdict / spec edit:** _(adaptive methodology vs threshold-based Step 5; population safeguards)_

### `D = 6.694` vs `D ≈ 4.6416` (the worked conflict)  → Phase 32
- **LOCKED:** `D ≈ 4.6416` (not re-openable; CLM-19 / PHYS-01; `6.694` rejected by EVID-10).
- **Verdict (OPEN part only):** `τ_L` / `L_max` re-derivation under the locked `D`.

### `τ_L` / `L_max` computation formulas  → Phase 33
- **Verdict / spec edit:** _(L_max formula; shadow-trajectory τ_L with split
  `epsilon_pert = 1e-8` / `epsilon_soft = 1e-10`; PCA+Rosenstein approximation)_

### ALM `μ_p` clamp  → Phase 34 / Phase 35
- **Verdict / spec edit:** _(clamp `[1e-4, 100.0]` placement given dense-residual ALM is
  rejected; applies to the P2 scalar-constraint ablation if anywhere)_

---

*This skeleton is non-binding and prescribes no schema; the v1.4 `ctl_pinn_resolution.md`
and v1.5 `02-resolution-doc.md` are format precedents only. Adapt freely.*

===== END FILE resolution-doc-skeleton.md =====
