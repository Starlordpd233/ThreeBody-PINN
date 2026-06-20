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
