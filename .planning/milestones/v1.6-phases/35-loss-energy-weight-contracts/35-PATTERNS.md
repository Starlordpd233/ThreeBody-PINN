# Phase 35: Loss & Energy-Weight Contracts - Pattern Map

**Mapped:** 2026-06-27
**Files analyzed:** 12
**Analogs found:** 12 / 12

## File Classification

| New/Modified File | Role | Data Flow | Closest Analog | Match Quality |
|-------------------|------|-----------|----------------|---------------|
| `.planning/phases/35-loss-energy-weight-contracts/evidence/m15-energy-weight-schedule.md` | model | transform | `.planning/phases/34-training-loop-batch-construction-contracts/evidence/b-08-data-vs-collocation-points.md` + Phase 32 `_TEMPLATE.md` | exact |
| `.planning/phases/35-loss-energy-weight-contracts/evidence/ns-12-componentwise-ad.md` | model | transform | `.planning/phases/34-training-loop-batch-construction-contracts/evidence/b-08-data-vs-collocation-points.md` + Phase 32 `_TEMPLATE.md` | exact |
| `.planning/phases/35-loss-energy-weight-contracts/evidence/ns-13-energy-huber-delta.md` | model | transform | `.planning/phases/34-training-loop-batch-construction-contracts/evidence/alm-mu-p-clamp.md` + Phase 32 `_TEMPLATE.md` | exact |
| `.planning/phases/35-loss-energy-weight-contracts/evidence/ns-18-loss-scaling-units.md` | model | transform | `.planning/phases/34-training-loop-batch-construction-contracts/evidence/b-08-data-vs-collocation-points.md` + Phase 32 `_TEMPLATE.md` | exact |
| `pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md` | config | transform | current `pinn_architecture.md` loss sections + Phase 34 LOOP callouts | exact |
| `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md` | config | transform | current `ctl_instruction.md` total-loss/data-flow section + Phase 34 LOOP callouts | exact |
| `.planning/phases/32-evidence-framework-issue-ledger-conflict-adjudication/32-ISSUE-LEDGER.md` | store | CRUD | same ledger rows for Phase 34 transitions | exact |
| `.planning/phases/32-evidence-framework-issue-ledger-conflict-adjudication/32-GAPS.md` | store | event-driven | `GAP-32-01` resolved owner-decision record | exact |
| `.planning/milestones/v1.6-GAPS.md` | store | event-driven | existing v1.6 gap index entries | exact |
| `.planning/phases/35-loss-energy-weight-contracts/35-VALIDATION.md` | test | batch | `.planning/phases/34-training-loop-batch-construction-contracts/34-VALIDATION.md` | exact |
| `.planning/phases/35-loss-energy-weight-contracts/35-VERIFICATION.md` | test | batch | `.planning/phases/34-training-loop-batch-construction-contracts/34-VERIFICATION.md` | exact |
| `.planning/phases/35-loss-energy-weight-contracts/35-GAPS.md` (conditional) | store | event-driven | `.planning/phases/34-training-loop-batch-construction-contracts/34-GAPS.md` | exact |

**Note:** `35-VALIDATION.md` already exists as an untracked worktree file at mapping time. Treat it as user-owned input; read it before any future modification.

## Pattern Assignments

### Phase 35 Evidence Packets (model, transform)

**Applies to:**
- `.planning/phases/35-loss-energy-weight-contracts/evidence/m15-energy-weight-schedule.md`
- `.planning/phases/35-loss-energy-weight-contracts/evidence/ns-12-componentwise-ad.md`
- `.planning/phases/35-loss-energy-weight-contracts/evidence/ns-13-energy-huber-delta.md`
- `.planning/phases/35-loss-energy-weight-contracts/evidence/ns-18-loss-scaling-units.md`

**Analog:** `.planning/phases/32-evidence-framework-issue-ledger-conflict-adjudication/evidence/_TEMPLATE.md`

**Header/schema pattern** (lines 5-20):
```markdown
## Header

| Field | Value |
|---|---|
| ID | `<ID>` |
| Title | `<Title>` |
| Severity | `BLOCKING` / `MAJOR` / `MINOR` / `INFO` / `owner-decision` |
| Current Status | `PENDING` / `IN_PROGRESS` / `FIX_APPLIED` / `VERIFIED` / `DEFERRED` |
| Current Verdict | `accept-resolution` / `accept-issue-doc` / `accept-third-position` / `reject-both-as-unsupported` / `defer-with-blocker` / `-` |
| Phase | `Phase NN` |
| Owner Phase | `Phase 32` / `Phase 33` / `Phase 34` / `Phase 35` / `Phase 36` / `FUT` |
| Consumer Phase | `Phase NN` or `None` |
| Acceptance Check ID | `AC-<REQ-ID>` |
| Spec Sections Touched | Exact framework spec section names or `None` |
| Code Paths Touched | `Not code-applicable` or FUT hand-off paths only |
```

**Source/citation pattern** (lines 21-31):
```markdown
## Source Positions

Add side-by-side line-range citations from the two issue-03 adjudication sources before selecting a verdict. Neither source is authoritative.

| Source | Required Line-Range Citation | Standing | Position Summary |
|---|---|---|---|
| `pinn_instruction/issues/03-curriculum-and-training-loop.md` | `path:START-END` | Non-authoritative issue source | Summarize the issue-document claim. |
| `pinn_instruction/markdown_conversion/framework-revisions/research_reports/03-curriculum-and-training-loop/research_result/03-final-resolution.md` | `path:START-END` plus section anchor | candidate verdict source, not authority | Summarize the resolution-document claim. |
| `.planning/phases/31-resolution-doc-readiness-verification/31-RESOLUTION-MAP.md` | `path:START-END` | Navigation / line-map aid | Record section mapping and freshness notes. |
```

**Guard pattern: no live-code grounding** (Phase 32 README lines 42-45):
```markdown
## No Live `pinn/` Grounding

Live `pinn/` code is NOT grounding evidence for v1.6 adjudication. References to `pinn/basic_architecture.py` or `pinn/data-processing-pipeline-full.py` may appear only as FUT-01/FUT-04 hand-off notes, and the same paragraph must state that the reference is NOT grounding.
```

**Verdict/status enum pattern** (Phase 32 README lines 46-72):
```markdown
## Verdict Enum

Use exactly one of these values once a packet is adjudicated:

| Verdict | Meaning |
|---|---|
| `accept-resolution` | Accept the candidate resolution document's position after independent verification. |
| `accept-issue-doc` | Accept the issue document's position after independent verification. |
| `accept-third-position` | Reject both source positions in favor of an independently justified convention. |
| `reject-both-as-unsupported` | Reject both source positions because neither survives evidence review. |
| `defer-with-blocker` | Defer because evidence is unavailable, explicit user instruction is required, or a blocker prevents adjudication. |

Pending ledger rows use `-` until the packet records one of the five verdicts.
```

**Filled accept-resolution packet pattern** (Phase 34 `b-08` lines 58-69):
```markdown
## Verdict

Verdict: `accept-resolution`

Explicit user instruction: None

Reasoning:

- The resolution doc §1.5 `modified` verdict is independently grounded by the need to keep data-fidelity points tied to BRUTUS snapshots and collocation points free in `[0,T]`, a distinction already implicit in the current spec's PHYS-05 loss catalog.
- The two-point-set contract, single-forward-pass allowance, and provisional `8192/4096` example budgets are preserved with a source citation; the actual data count follows the per-trajectory cap rule from B-07.
- The mandatory collocation 50/50 mix is deferred per GAP-06; Phase 34 will record this deferral rather than invent a continuous sampler.
- The B-08 contract is consistent with the SI-PINN-003 canonical-home decision: `ctl_instruction.md` owns batch construction; `pinn_architecture.md` keeps loss-term definitions and points to `ctl_instruction.md` for batch construction.
```

**Filled defer-with-blocker packet pattern** (Phase 34 `alm-mu-p-clamp` lines 59-70):
```markdown
## Verdict

Verdict: `defer-with-blocker`

Explicit user instruction: None

Reasoning:

- The resolution doc §1.18 `defer` verdict is independently grounded by the current specs, which already reject dense-residual ALM and document ALM only as an optional scalar-conservation P2 ablation.
- Claim ALM-03 defers the clamp as missing-specification; GAP-19 records the unspecified ablation mechanics.
- The default training-step contract will NOT include a dense-residual ALM update or a `mu_p` clamp.
- The `[1e-4, 100]` bounds and RMSprop-style update are carried as deferred/not adopted; they may apply only to a future optional scalar-conservation ALM ablation after its update law is defined.
```

**Phase 35 source-line assignment for packets:**
- M15: final resolution `03-final-resolution.md:56-59`, claim rows `M15-01..04` at lines 139-142, `DGR-09..10` at lines 198-199, `GAP-09` at line 227.
- NS-12: final resolution `03-final-resolution.md:68-71`, claim rows `NS12-01..03` at lines 152-154, `GAP-13` at line 231.
- NS-13: final resolution `03-final-resolution.md:72-75`, claim rows `NS13-01..03` at lines 155-157, `DGR-14` at line 203, `GAP-14` at line 232.
- NS-18: final resolution `03-final-resolution.md:76-79`, claim rows `NS18-01..04` at lines 158-161.

---

### `pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md` (config, transform)

**Analog:** current `pinn_architecture.md` loss sections and Phase 34 callout style.

**Component-math canonical home pattern: data Huber** (lines 292-308):
```markdown
## 3.1 Data Fidelity Term ($\mathcal{L}_{\text{data}}$): Anchoring to Ground Truth

The data fidelity loss uses a Huber contract on scaled projected
positions:

$$L_{data} = \frac{1}{N_t} \sum_n \sum_i \operatorname{Huber}_{\delta_r}(r_{\theta,i}'(u_n) - r_i'(u_n))$$

where $\delta_r = 1$ is the default Huber transition. The previous
MAE/L1 data-loss prose is replaced by this Huber contract.
```

**Pointer-only anti-duplication pattern** (lines 351-353):
```markdown
> **Phase 34 contract: batch-construction reconciliation (SI-PINN-003; ctl canonical; AC-LOOP-02; grounded by the resolution doc §1.5 claim matrix B07-04 and `ctl_instruction.md` Mini-Batch Construction).**
>
> *Note (PIPE-04): `points_per_trajectory=32` and `N_data = batch_size * points_per_trajectory` are code defaults/illustrations only, not the spec contract. The operative data-loss sampling rule is `n_pts(traj) = min(n_pts_cap, n_snapshots(traj))` without replacement, defined canonically in `ctl_instruction.md` Mini-Batch Construction.
```

**Causal weighting pattern for LOSS-04** (lines 408-417):
```markdown
For sorted collocation times $u_1 < \cdots < u_{N_t}$, the default
causal weights are:

$$w_1 = 1,\qquad
w_n = \exp\left(-\eta_c \sum_{m=1}^{n-1} \operatorname{stopgrad}(\bar R_m)\right),
\quad n>1.$$

The default physics loss consumed by $L_{total}$ is therefore:

$$L_{phys}^{causal} = \frac{1}{N_t} \sum_{n=1}^{N_t} w_n \bar R_n.$$
```

**Energy Huber baseline pattern for LOSS-03** (lines 519-531):
```markdown
$$L_{E} = \frac{1}{N} \sum_n \operatorname{Huber}(\Delta H_n, \delta=1.0)$$

where

$$\Delta H_n = \frac{H_\epsilon(r_\theta'(u_n), v_\theta'(u_n)) - H_\epsilon(r_0', v_0')}{|H_\epsilon(r_0', v_0')| + \epsilon_H}$$

The relative drift symbol is $\Delta H_n$.

$$epsilon_H = 1e-4 * S_H$$

$$S_H = median_train(K0 + Uabs0)$$

and $\delta = 1.0$ is the Huber transition.
```

**Warmup/no-linear-momentum pattern for LOSS-01/02** (lines 625-656):
```markdown
## 4.1 Loss Balancing via Warmup Schedule (PHYS-05)

$$L_{total} = L_{data} + \lambda_{IC} \cdot L_{IC} + \lambda_{phys} \cdot L_{phys}^{causal} + \lambda_E \cdot L_E + \lambda_L \cdot L_L$$

where:

- $L_{data}$: Huber loss on position predictions, $\delta_r = 1$ default
  (resolution §8.2).
- $L_{phys}^{causal}$: Physics residual with causal weighting
  $w_n = exp(-\eta_c \sum_{m<n} stopgrad(\bar R_m))$, $w_1 = 1$,
  $\eta_c = 1$ default. Use `stopgrad` in weights by default. Clip the
  causal exponent to avoid underflow, but do not choose a numeric
  clipping bound in Phase 19; surface a gap if one is needed.
- $L_{E}$: Soft energy conservation regularizer,
  see §3.4.
- $L_{L}$: Angular momentum conservation loss, see §3.5.
- No dedicated L_P term: linear momentum is enforced structurally by
  the Phase 17 COM projection head / zero-momentum output contract, so a
  separate linear-momentum loss would be redundant.

The warmup schedule is:

- $\lambda_E^{max}(k) = \lambda_L^{max}(k) = \{0 \text{ for } k \in \{0,1\}; 10^{k-4} \text{ for } k \in \{2,3,4\}; 1 \text{ for } k \in \{5,6\}\}$
```

**Phase callout and normative-pseudocode label pattern** (lines 714-748):
````markdown
> **Phase 34 contract: adaptive median-based gradient clipping (LOOP-04; M14 modified/accept-resolution; AC-LOOP-04; grounded by the resolution doc §1.8 and `evidence/m14-gradient-clipping.md`).**

The merged clipping mechanism is **locked**: during Adam epochs only,
the clip value is the product of the curriculum-aware stage multiplier
$C_{\text{stage}}$ and the median of recent global gradient norms,
computed over a rolling window of recent global gradient norms.

``` {.python language="Python" caption="Listing 6: Adaptive Gradient Clipping Logic (normative spec contract — not executable; FUT-01/FUT-04 implements)"}
# Maintain a queue/list of the last 100 gradient norms
grad_history = []

# Clip norm to C_stage times the median of recent norms
clip_value = C_stage * torch.median(torch.stack(grad_history))
torch.nn.utils.clip_grad_norm_(model.parameters(), clip_value)
```
````

**AD/tau chain-factor pattern for LOSS-01** (lines 783-787 and 878-893):
```markdown
If velocities or accelerations are needed for analysis, derive them by differentiating with respect to
the canonical autograd leaf $u$. The $2\times$ and $4\times$ chain-rule
factors apply only to an implementation path that differentiates
directly with respect to $\tau$.

**Canonical autograd leaf:** `u=t/T`. When the code path differentiates
with respect to `u`:

- $v' = dr'/du$ (velocity in scaled time, no chain-rule factor)
- $a' = d^2r'/du^2$ (acceleration in scaled time, no chain-rule factor)

**Conditional chain-rule factors for τ/tau:** If a code path
differentiates directly with respect to $\tau = 2u - 1$ (rather than
`u`), then:

- $v' = 2 \cdot dr'/d\tau$
- $a' = 4 \cdot d^2r'/d\tau^2$

These factors apply ONLY to the $\tau$-leaf code path.
```

---

### `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md` (config, transform)

**Analog:** current `ctl_instruction.md` total-loss assembly and Phase 34 LOOP callout sections.

**Input/canonical leaf pattern** (lines 1519-1528):
```markdown
#### Network input contract

The network input is exactly

$$
x_{\mathrm{net}} = [\tau, IC_{13}], \qquad \tau = 2u - 1,\qquad u=t/T.
$$

For the normalized-time derivative contract (autograd leaf, chain-rule factors,
componentwise derivatives, and synthetic-trajectory test), see pinn_architecture.md PHYS-02 contract.
```

**Training data-flow/assembly pattern** (lines 1689-1758):
```markdown
### Data Flow During Training

1. **Input**: The model receives the 14-dimensional network input `[\tau, IC_{13}]`, where `u=t/T` is the autograd leaf and `\tau=2u-1`.

2. **Network Prediction**: The network emits a raw 9D position head for the three bodies. The architecture applies the hard mass-weighted COM projection defined in `pinn_architecture.md` before any loss, residual, diagnostic, or evaluation metric consumes the output.

## Loss Function Formulation

### Phase 2: Total Training Loss

The default training loss is:

$$
\mathcal{L}_{\mathrm{total}} = \mathcal{L}_{\mathrm{data}} + \lambda_{\mathrm{IC}} \, \mathcal{L}_{\mathrm{IC}} + \lambda_{\mathrm{phys}} \, \mathcal{L}_{\mathrm{phys}}^{\mathrm{causal}} + \lambda_E \, \mathcal{L}_E + \lambda_L \, \mathcal{L}_L
$$

where each term is defined by name in the PHYS-05 loss-term catalog in
`pinn_architecture.md` ($\mathcal{L}_{\mathrm{data}}$, $\mathcal{L}_{\mathrm{IC}}$, $\mathcal{L}_{\mathrm{phys}}^{\mathrm{causal}}$, $\mathcal{L}_E$, and $\mathcal{L}_L$).
The loss-balancing contract, warmup schedule, and optimizer-phase semantics
are defined in the PHYS-05 training-loss contract in `pinn_architecture.md`.

**Per-step ordering skeleton (Adam epoch).** The default training step follows this order, treating each loss term as an opaque input whose component definition, weight schedule (`λ_E`, `λ_L`, etc.), and Huber-δ calibration are owned by Phase 35.
```

**Verdict-status callout and canonical-home pattern** (lines 1787-1819):
```markdown
> **Phase 34 contract: replay/lookahead batch construction (LOOP-01; provisional; AC-LOOP-01; grounded by the resolution doc §1.4 and `evidence/b-07-replay-lookahead-batching.md`).** This `ctl_instruction.md` section is the **canonical** batch-construction contract (SI-PINN-003); `pinn_architecture.md` points here rather than duplicating the rule.

> **Phase 34 contract: data versus collocation points (LOOP-02; provisional; AC-LOOP-02; grounded by the resolution doc §1.5 and `evidence/b-08-data-vs-collocation-points.md`).**

The training batch consists of two logically independent point sets:

1. **Data-fidelity points**: sampled from the discrete BRUTUS trajectory snapshots (the replay/lookahead trajectories above), used for the Huber data loss $\mathcal{L}_{\text{data}}$.
2. **Collocation points**: continuous samples from $[0,T]$ for the physics residual $\mathcal{L}_{\text{phys}}^{\text{causal}}$ and the energy residual $\mathcal{L}_E$ (energy reuses the physics collocation set).

> **Phase 34 contract: mixed time sampling (LOOP-03; data retained / collocation deferred; grounded by the resolution doc §§1.4–1.5 and the B-07/B-08 evidence packets).**

- **Collocation points — 50/50 deferred:** A mandatory 50/50 mixed continuous collocation sampler is **deferred** (B-08 / GAP-06); Phase 34 does not mandate it.
```

**Phase 35 callout to copy/adapt:**
```markdown
> **Phase 35 contract: <contract name> (LOSS-NN; <finding-id> <verdict/status>; AC-LOSS-NN; grounded by the resolution doc §<section> and `evidence/<packet>.md`).** <One-sentence canonical-home note: this file owns assembly/methodology or points to `pinn_architecture.md` for component math.>
```

---

### `32-ISSUE-LEDGER.md` (store, CRUD)

**Analog:** `.planning/phases/32-evidence-framework-issue-ledger-conflict-adjudication/32-ISSUE-LEDGER.md`

**Ledger invariant pattern** (lines 1-5):
```markdown
# Phase 32 Issue Ledger

Stable issue-03 ledger for Phase 32 through Phase 36. The ledger is seeded from `31-RESOLUTION-MAP.md` and `32-RESEARCH.md`; it records process state only and does not assign semantic verdicts before evidence packets exist.

`FIX_APPLIED is not terminal`. Closure requires `VERIFIED` after the named acceptance check passes, or `DEFERRED` with a written blocker and `defer-with-blocker` verdict.
```

**Phase 35 row pattern before execution** (lines 23 and 26-28):
```markdown
| M15 | Energy-loss weights | Phase 35 | PENDING | - | Owner must author packet before spec edits | AC-LOSS-02 | `ctl_instruction.md` energy-loss weight schedule | Phase 35 LOSS-02; Phase 36 | Seeded; packet-before-edit forward reference |
| NS-12 | Componentwise automatic differentiation | Phase 35 | PENDING | - | Owner must author packet before spec edits | AC-LOSS-01-AD | `ctl_instruction.md` loss scaling and AD cross-link | Phase 35 LOSS-01; Phase 36 | Seeded; packet-before-edit forward reference |
| NS-13 | Energy Huber delta | Phase 35 | PENDING | - | Owner must author packet before spec edits | AC-LOSS-03 | `ctl_instruction.md` Huber delta calibration contract | Phase 35 LOSS-03; Phase 36 | Seeded; packet-before-edit forward reference |
| NS-18 | Loss scaling and units | Phase 35 | PENDING | - | Owner must author packet before spec edits | AC-LOSS-01 | `ctl_instruction.md` dimensionless loss scaling | Phase 35 LOSS-01; Phase 36 | Seeded; packet-before-edit forward reference |
```

**Packet-before-edit mandate** (lines 34-36):
```markdown
## Non-Headline Packet Mandate

Every non-headline row above has exactly one primary owner phase from Phase 33, Phase 34, or Phase 35. That owner must author the evidence packet and update this ledger before editing any spec section for the row. Phase 36 must reject any spec edit whose row lacks packet/verdict linkage.
```

**Transition-log pattern** (lines 89-115):
```markdown
### M15

- 2026-06-21 pending-commit PENDING seeded by Phase 32 Plan 32-01 Task 3; Phase 35 must author the packet before spec edits.

### NS-12

- 2026-06-21 pending-commit PENDING seeded by Phase 32 Plan 32-01 Task 3; Phase 35 must author the packet before spec edits.

### NS-13

- 2026-06-21 pending-commit PENDING seeded by Phase 32 Plan 32-01 Task 3; Phase 35 must author the packet before spec edits.

### NS-18

- 2026-06-21 pending-commit PENDING seeded by Phase 32 Plan 32-01 Task 3; Phase 35 must author the packet before spec edits.
```

---

### `32-GAPS.md`, `v1.6-GAPS.md`, and Conditional `35-GAPS.md` (store, event-driven)

**Analog:** `.planning/phases/32-evidence-framework-issue-ledger-conflict-adjudication/32-GAPS.md` and `.planning/phases/34-training-loop-batch-construction-contracts/34-GAPS.md`

**Resolved owner-decision pattern for D-04 / LOSS-04** (`32-GAPS.md` lines 50-57):
```markdown
- **Status:** **RESOLVED-WITH-INSTRUCTION** (2026-06-26)
- **Resolution note:** Per the user's Phase 35 spec-gate instruction, Option A is
  ratified: retain the current per-time causal weighting baseline with
  `w_n = exp(-eta_c * sum_{m<n} stopgrad(Rbar_m))`, `w_1 = 1`, and
  `eta_c = 1`; preserve the dense-residual pseudo-ALM rejection; keep optional
  scalar-conservation ALM as deferred P2 only; and defer the numeric
  causal-exponent clip bound to FUT. Phase 35 `LOSS-04` owns transcription of
  this owner-ratified verdict and status.
```

**Milestone index pattern** (`v1.6-GAPS.md` lines 16-22):
```markdown
## Phase 32: Evidence Framework, Issue Ledger & Conflict Adjudication

**Register:** `.planning/phases/32-evidence-framework-issue-ledger-conflict-adjudication/32-GAPS.md`

| Gap | Decision | Resolution |
|-----|----------|------------|
| GAP-32-01 | D-04 causal-training mode owner decision | **RESOLVED-WITH-INSTRUCTION** (2026-06-26) - Owner ratified **Option A** at the Phase 35 SPEC gate: retain the current per-time causal weighting baseline (`w_n = exp(-eta_c * sum_{m<n} stopgrad(Rbar_m))`, `w_1 = 1`, `eta_c = 1`); preserve the dense-residual pseudo-ALM rejection; keep optional scalar-conservation ALM as deferred P2 only; and defer the numeric causal-exponent clip bound to FUT. Phase 35 `LOSS-04` transcribes this owner-ratified verdict and status. |
```

**New STOP gap schema pattern** (`34-GAPS.md` lines 8-23):
```markdown
## GAP-34-01 - Batch edge-case policy for replay/lookahead batch construction

- **Decision point:** What deterministic policy should govern the batch edge cases...
- **Where in artifact:** `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md`, section **Mini-Batch Construction with Lookahead Sampling**...
- **Task context:** Plan 34-03 Task 1, transcribing the LOOP-01 replay/lookahead batch-construction contract.
- **Classification:** **semantic** — the selected edge policy changes the effective batch distribution...
- **Source silence:** ...
- **Mathematical / engineering grounding:** ...
- **Agent was tempted to:** ...
- **What the user needs to decide:**
  - **A.** ...
  - **B.** ...
  - **C.** ...
- **Confidence of impact:** **HIGH** — ...
- **Status:** **RESOLVED-WITH-INSTRUCTION**
- **Resolution note:** ...
```

Apply this only if Phase 35 packet/edit work surfaces a new source-silent semantic/process/cross-phase decision. Otherwise do not create `35-GAPS.md`.

---

### `35-VALIDATION.md` (test, batch)

**Analog:** `.planning/phases/34-training-loop-batch-construction-contracts/34-VALIDATION.md`

**Frontmatter and scope pattern** (lines 1-24):
```markdown
---
phase: 34
slug: training-loop-batch-construction-contracts
status: active
nyquist_compliant: true
wave_0_complete: true
created: 2026-06-24
---

# Phase 34 - Validation Strategy

| Property | Value |
|----------|-------|
| **Framework** | shell + Python source-token / negative-token / no-duplication checks + git protected-path guards + disposable formula-sanity probes (D-34-17). NOT runtime training tests (SCOPE-14). |
| **Quick run command** | `rg -n "LOOP-0[1-8]\|SI-PINN-003" .planning/phases/34-training-loop-batch-construction-contracts/34-*-PLAN.md` |
| **Full suite command** | plan coverage check, framework-spec token checks, the LOOP-04 (a)–(e) cross-file consistency suite, the locked-convention regression guard, forbidden-path git-diff guard, and STOP-gap completeness checks if new gaps are opened |
```

**Token/negative/protected-path check pattern** (lines 86-167):
````markdown
### Framework-Spec Contract Tokens (per-requirement)

```bash
python3 - <<'PY'
from pathlib import Path
ctl = Path("pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md").read_text()
pinn = Path("pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md").read_text()
checks = {
    "LOOP-01 replay/lookahead (ctl)": (ctl, ["B_replay", "B_lookahead", "has_stage", "provisional"]),
    "LOOP-05 ALM optional (pinn)":    (pinn, ["ALM", "optional", "deferred"]),
}
missing = {name: [t for t in toks if t not in src] for name, (src, toks) in checks.items()}
missing = {name: toks for name, toks in missing.items() if toks}
assert not missing, missing
PY
```

### Forbidden-Path Status Guard (SCOPE-08/09/13 + no-live-code)

```bash
git diff --name-only -- \
  pinn_instruction/markdown_conversion/framework-specs/sampling_method.md \
  pinn_instruction/markdown_conversion/framework-revisions/data_quality_assessment.md \
  pinn_instruction/markdown_conversion/framework-revisions/review-of-framework/review_of_framework.md \
  pinn_instruction/markdown_conversion/framework-revisions/stage-strat-revision/stage_strat_revision.md \
  pinn_instruction/markdown_conversion/framework-revisions/research_reports/03-curriculum-and-training-loop/research_result/03-final-resolution.md \
  pinn/
```
````

**Phase 35 validation checks should adapt these to:** `AC-LOSS-01..04`, `LOSS-01..04`, `M15`, `NS-12`, `NS-13`, `NS-18`, `D-04`, `modified`, `rejected`, `defer`, `RESOLVED-WITH-INSTRUCTION`, `delta_E = 1.0`, `lambda_E`, `lambda_E = 1000` absence, cap-table absence, no numeric causal clip, no default dense-residual ALM, no duplicated normative body text.

---

### `35-VERIFICATION.md` (test, batch)

**Analog:** `.planning/phases/34-training-loop-batch-construction-contracts/34-VERIFICATION.md`

**Frontmatter/artifact summary pattern** (lines 1-64):
```markdown
---
phase: 34
slug: training-loop-batch-construction-contracts
verified: 2026-06-25T07:30:00Z
status: passed
score: 9/9 requirements verified; 5/5 LOOP ledger rows VERIFIED; GAP-34-01 resolved (Plan 34-06)
gaps_remaining: []
behavior_unverified: 0
overrides_applied: 0
roadmap_truths:
  - "LOOP-01 replay/lookahead batch construction transcribed as provisional..."
artifacts:
  - path: "pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md"
    provides: "Transcribed LOOP-01/02/03/06/07/08 contracts and LOOP-04 C-schedule (single canonical home)"
  - path: "pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md"
    provides: "Transcribed LOOP-04 mechanism (single canonical home), LOOP-05 optional/deferred ALM, SI-PINN-003 reconciliation"
prohibitions:
  - statement: "MUST NOT close any ledger row to VERIFIED before 34-VERIFICATION.md records passing checks"
    status: resolved
    verification: "ledger closure in Task 2 occurred only after Task 1 verification PASS recorded"
---
```

**Goal-backward truth table pattern** (lines 80-91):
```markdown
| # | Truth (ROADMAP SC / LOOP ID) | Status | Evidence |
|---|---|---|---|
| 1 | LOOP-01 replay/lookahead batch construction is defined ... | ✓ VERIFIED | `ctl_instruction.md:1787-1799` Phase 34 contract callout; ... |
| 2 | LOOP-02 two-independent-point-set contract defined ... | ✓ VERIFIED | `ctl_instruction.md:1801-1818` LOOP-02/03 callouts; ... |
```

**Command/result recording pattern** (lines 149-170):
````markdown
## 2. Framework-Spec Contract Tokens — PASS

Command run (matches `34-VALIDATION.md`):

```python
from pathlib import Path
ctl = Path("pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md").read_text()
pinn = Path("pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md").read_text()
checks = {
    "LOOP-01 replay/lookahead (ctl)": (ctl, ["B_replay", "B_lookahead", "has_stage", "provisional"]),
}
```

Result: `CONTRACT-TOKENS: PASS`.
````

**Ledger closure pattern** (lines 340-366):
```markdown
## 9. Phase-32 Ledger Closure — PASS

After verification, the five LOOP-related rows are closed `VERIFIED` with preserved verdicts:

| Finding row | AC ID | Consuming plan | Transition | Preserved verdict |
|---|---|---|---|---|
| B-07 | AC-LOOP-01 | 34-03 (ctl LOOP-01) | `IN_PROGRESS → FIX_APPLIED → VERIFIED` | `accept-resolution` |

No new status enum or AC-ID scheme was minted. D-04, the Phase-33-owned rows, and the Phase-35-owned rows (M15/NS-12/13/18) remain unchanged.
```

For Phase 35, replace LOOP rows with M15, NS-12, NS-13, NS-18, and D-04; close them only after `35-VERIFICATION.md` records PASS.

## Shared Patterns

### Source Precedence
**Source:** `35-CONTEXT.md` lines 52-56 and `35-RESEARCH.md` lines 258-289
**Apply to:** all Phase 35 packets, spec edits, validation, and verification

Use `35-SPEC.md`, `35-CONTEXT.md`, Phase 31 map, Phase 32 ledger/packets/gaps, the current framework specs, and the issue-03 final resolution. Do not copy stale `.planning/REQUIREMENTS.md` or `ROADMAP.md` Phase 35 preview text when it conflicts with the SPEC.

### Packet Before Edit
**Source:** `35-CONTEXT.md` lines 166-176; Phase 32 README lines 90-94
**Apply to:** M15, NS-12, NS-13, NS-18

Every Phase 35-owned row must have its packet authored and `32-ISSUE-LEDGER.md` updated before any framework-spec edit for that row. D-04 consumes the existing Phase 32 packet plus the resolved gap; do not create a new D-04 packet unless the plan explicitly needs a handoff note.

### Verdict-Status Callout
**Source:** `35-CONTEXT.md` lines 89-104; `ctl_instruction.md` lines 1787-1831; `pinn_architecture.md` lines 714-728
**Apply to:** both framework specs

Copy the callout shape:
```markdown
> **Phase 35 contract: <name> (LOSS-NN; <finding-id> <verdict/status>; AC-LOSS-NN; grounded by <source> and `evidence/<packet>.md`).**
```

Use `modified`, `rejected`, `defer`/`deferred`, `locked`, and `RESOLVED-WITH-INSTRUCTION` exactly where the SPEC assigns those statuses.

### Single Canonical Home
**Source:** `35-CONTEXT.md` lines 106-124; Phase 34 `b-08` lines 94-104; `pinn_architecture.md` lines 351-353
**Apply to:** `ctl_instruction.md` and `pinn_architecture.md`

Keep component math in `pinn_architecture.md`; keep training-methodology/assembly in `ctl_instruction.md`. The non-owning file points by stable section heading and AC ID. Do not duplicate formula bodies.

### STOP Gap Handling
**Source:** `AGENTS.md` lines 63-89; Phase 32 README lines 76-88; `34-GAPS.md` lines 8-23
**Apply to:** all packets and spec edits

If a packet or edit surfaces a source-silent semantic, process-schema, or cross-phase choice, stop affected work and create `35-GAPS.md` plus a `.planning/milestones/v1.6-GAPS.md` row using the full gap schema. Do not fill missing numeric schedules, Huber tables, causal clip bounds, or causal-mode mechanics.

### Validation Modality
**Source:** `34-VALIDATION.md` lines 17-34 and 86-167; `34-VERIFICATION.md` lines 370-374
**Apply to:** `35-VALIDATION.md` and `35-VERIFICATION.md`

Phase 35 is specwork-only. Use `rg`, `python3 -c` / short Python snippets, `git diff --name-only`, token/negative checks, no-duplication checks, and ledger/gap status checks. Do not run training, EDA, Stage-0 pilot, DataLoader implementation, or live `pinn/` tests for Phase 35.

## No Analog Found

None. All Phase 35 files have close Phase 32/34 analogs.

## Metadata

**Analog search scope:** `.planning/phases/32-*`, `.planning/phases/33-*`, `.planning/phases/34-*`, `.planning/phases/35-*`, `.planning/milestones/v1.6-GAPS.md`, `pinn_instruction/markdown_conversion/framework-specs/`, `.claude/rules/`, Phase 31 resolution map.

**Files scanned:** 20+ files via `rg --files`, targeted `rg`, and line-numbered reads.

**Pattern extraction date:** 2026-06-27

**Worktree state at mapping:** branch `milestone/v1.6`; existing user-owned changes at start were `M AGENTS.md`, untracked `35-RESEARCH.md`, and untracked `35-VALIDATION.md`.
