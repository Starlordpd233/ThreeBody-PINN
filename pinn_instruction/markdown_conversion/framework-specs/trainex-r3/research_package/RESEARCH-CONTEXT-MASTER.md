---
title: Trainex R3 Research Context Master — Causal-Weight / SIREN-Scale Recalibration Decision Packet
package_for: trainex-r3 (single sub-package)
role: the owner's single entry point at checkpoint ① and, unchanged, the external research agent's single entry point if the round is commissioned
status: active
created: 2026-08-20
source_baseline: 6a4f9b9902ab62e1d1f57bba0e521f38120c416d
self_contained: true
access_mode: open-book
---

# Trainex R3 Research Context Master — Causal-Weight / SIREN-Scale Recalibration Decision Packet

## 0. Premise qualification — the standing of trainex-r2 in this round

The trainex-r2 round's output contract is quoted here first, verbatim, because it is the standing block every other mention of that round in this packet routes back to. The quotation is an attributed quotation of an externally authored document; it sits above the neutrality-ban markers below because it is that document's voice, not this packet's.

```
3. **Do not recommend a remedy.** Remedy adjudication is owner-governed
   downstream. Your answers inform that decision; they do not make it.
```

`[VERIFIED verbatim: pinn_instruction/markdown_conversion/framework-specs/trainex-r2/research_package/RESEARCH-CONTEXT-MASTER.md:319-320]`

<!-- NEUTRALITY-BAN-BEGIN -->

The consequence of that contract, stated as the absence list it produced: the trainex-r2 round carries no decision sheet, no options menu, no marked defaults, and no one-way/two-way door classification.

The vintage of that round: packaged 2026-07-24 and delivered 2026-07-25, predating the v2.2 conformance repairs, so its observations describe the pre-repair tree.

The standing of its Q3: Q3 framed the diagnosis and independently derived the `first_omega_0 = 30` second-derivative mechanism **as a hypothesis** — since confirmed by the 2026-08-17 residual-frame conformance audit — and it does not contain the answer.

The citation convention this section establishes: every mention of the trainex-r2 round anywhere outside §0 carries the ASCII tag `[r2-QUAL]` appended on the same line, routing the reader back to this section. A mention without the tag is a defect. §0 itself is the qualification block and is exempt.

## 1. Orientation

### 1.1 What happened

v2.2's conformant Stage-0 re-run (generation 3, seed 41) halted on invariant B at step 501, with `front_idx` at 0 on all 502 logged steps — the full `N = 500` front-advance window passed without a single advance (`.planning/milestones/v2.2-phases/52-diagnosis-re-derivation-handoff/52-DIAG-05-REDERIVATION.md:58`; `.planning/milestones/v2.2-phases/50-valid-stage-0-re-run/50-03-SUMMARY.md:84`).

A same-day bounded residual-frame conformance audit (2026-08-17) established that the halt is a property of the locked architecture at initialization, not of the training dynamics (`docs/work/reviews/milestone_v2.2/50-valid-stage-0-re-run/2026-08-17-residual-frame-conformance-audit.md` §6). The owner then selected `stop-incomplete`, closing v2.2 with the single held-out evaluation preserved unspent (`.planning/milestones/v2.2-GAPS.md` "Milestone close (2026-08-17)").

VER-20 item (e) is the resulting handoff (`.planning/milestones/v2.2-phases/52-diagnosis-re-derivation-handoff/52-VER-20-ROUTING-HANDOFF.md`), and it frames the work in its own words: *"the correct calibration is a research question, not an engineering default."* The mechanism facts are transcribed in §4.

### 1.2 What this packet asks

This packet frames one decision: the recalibration of the causal-weight formula against the SIREN initialization scale, across the five coupled decision surfaces §4 enumerates. The framed questions themselves are in §5. This document is a question, framed — not an analysis that arrives at an answer.

### 1.3 What this packet does not do

The recalibration decision is owner-ratified, never agent-decided (SCOPE-34, `.planning/REQUIREMENTS.md:119`). This packet marks no default, ranks no option, and picks nothing; the criterion by which a reader verifies that by inspection is stated in §10. If the round is commissioned, the external agent's deliverable is a different document governed by the output contract in §9 — the bar above binds this packet's own voice, never §9's specification of that deliverable. `self_contained: true` means, for this round, that the packet states its mechanism inline so it stands alone for the owner's read at the gate, while under Route B the repository is an additional evidence source and not a replacement for the package.

## 2. Manifest — what this round contains, and what it deliberately does not

What this round contains today: one authored file, this master, at `pinn_instruction/markdown_conversion/framework-specs/trainex-r3/research_package/RESEARCH-CONTEXT-MASTER.md` — plus the user-only `DELIVERY-NOTE.md` at the round root, which is never uploaded.

What this round deliberately does not contain, by exact path: `research_package/RESEARCH-AGENT-PROMPT.md`, `specs/`, and `research_results/`. The runbook's own reason: a package without its prompt is incomplete, and the two always ship together — so a round root carrying a master and no prompt is, by that definition, a round that has not been commissioned. These three artifacts are authored only if the owner commissions the round at checkpoint ①, and their absence is therefore the structural proof that no branch was assumed.

The r2-to-r3 role mapping (headings of the trainex-r2 round's master [r2-QUAL], quoted verbatim with their line numbers; the renumbering is deliberate so the r2 roles keep their original relative order):

| trainex-r2 section [r2-QUAL] | this master's section | role |
|---|---|---|
| `## 1. Orientation` (r2:19) | `## 1. Orientation` | orientation |
| `## 2. Manifest (the four attached files)` (r2:48) | `## 2. Manifest — what this round contains, and what it deliberately does not` | manifest |
| `## 3. Source tiering (how to treat each kind of content)` (r2:57) | `## 3. Source tiering — how to treat each kind of content` | tiering |
| `## 4. The six research questions` (r2:74) | `## 5. The framed questions` | questions |
| `## 5. Claims register (folded in verbatim from CLAIMS-REGISTER.md)` (r2:254) | `## 6. Claims register` | claims |
| `## 6. Provenance` (r2:297) | `## 8. Provenance` | provenance |
| `## 7. Output contract` (r2:308) | `## 9. Output contract` | output contract |

The three additional sections — §0, §4, and §7 — are the v2.3-specific additions D-03 mandates.

## 3. Source tiering — how to treat each kind of content

- **Hard constraint (relied on as ground truth):** the locked framework specs (`pinn_architecture.md`, `ctl_instruction.md`) as they stand, with their owner-ratified contract markers; the v2.2 closure record — the 2026-08-17 residual-frame conformance audit, `52-DIAG-05-REDERIVATION.md` §3 as the operative diagnosis (superseding `44-DIAGNOSIS.md` and `44-ERRATUM.md`), `52-VER-20-ROUTING-HANDOFF.md`, and `.planning/milestones/v2.2-GAPS.md`'s milestone-close section; every `F-` row in §6; and the SCOPE boundaries stated in §1.3. The operative diagnosis is treated as settled and is not re-litigated.
- **Challengeable (to be tested rather than assumed):** every `H-` row in §6, including the trainex-r2 round's interpretive content [r2-QUAL].
- **Repo-derived evidence (the Route-B tier):** under `access_mode: open-book` the repository is an additional evidence source and not a replacement for this package. A claim derived from the live tree arrives as a checkable assertion carrying a `file:line`, not as an established fact, and ERW Rule 19 requires every such claim to be independently verified in-repo, with the verification recorded, before it informs a decision, a roadmap, or a spec edit. `pinn/` is not a grounding source for spec decisions — it is cited in §4 only as the current divergence being disposed of.

## 4. The confirmed mechanism and the coupled decision surfaces

### 4.1 The confirmed mechanism

Everything in this section is transcription from already-published, already-cited sources. Nothing in this section is agent inference.

**M1 — the six-row seed/IC initialization probe** (all six rows are the probe's printed output; medians over the 16 collocation points):

| seed / IC | ‖r′‖ | ‖v′‖ | ‖a′‖ = ‖d²r′/du²‖ | ‖F_grav‖ | min pairwise sep | `R̄` median | `front_idx` |
|---|---|---|---|---|---|---|---|
| 41, m=(1,1,1), IC13=0 | 1.28 | 310 | 2.03×10⁵ | 2.17 | 0.91 | 1.37×10¹⁰ | 0 |
| 42 | 1.13 | 331 | 2.72×10⁵ | 3.29 | 0.67 | 2.46×10¹⁰ | 0 |
| 43 | 0.97 | 251 | 2.20×10⁵ | 3.24 | 0.72 | 1.62×10¹⁰ | 0 |
| 0 | 0.91 | 281 | 2.79×10⁵ | 5.94 | 0.50 | 2.60×10¹⁰ | 0 |
| 7 | 0.85 | 290 | 1.94×10⁵ | 5.89 | 0.51 | 1.25×10¹⁰ | 0 |
| 41, m=(1,0.8,0.6), random tanh IC13 | 0.95 | 231 | 2.28×10⁵ | 2.85 | 0.72 | 1.74×10¹⁰ | 0 |

(`docs/work/reviews/milestone_v2.2/50-valid-stage-0-re-run/2026-08-17-residual-frame-conformance-audit.md:142` — header; `:144-149` — rows; `:151` — the parenthetical note.)

**M2 — the chain.** `first_omega_0 = 30` sets the second-derivative magnitude, which sets `R̄`, which drives the causal exponent. The `‖a′‖` column values run `1.94×10⁵`–`2.79×10⁵` in network units; the `R̄` medians run `1.25×10¹⁰`–`2.60×10¹⁰` (`2026-08-17-residual-frame-conformance-audit.md:142-151` for the numbers, `:163-169` for the mechanism prose; corroborated independently at `.planning/milestones/v2.2-phases/52-diagnosis-re-derivation-handoff/52-VER-20-ROUTING-HANDOFF.md:37`).

**M3 — the float32 underflow bound, at both precisions.** The causal weight `exp(−η_c R̄)` underflows float32 at `R̄ > 87.34` — 8.46 decades below the median (`2026-08-17-residual-frame-conformance-audit.md:127`). The rounded form `87.3` appears in the routing handoff and carries its own citation (`52-VER-20-ROUTING-HANDOFF.md:40`). The audit carries the precise value; the handoff carries the rounded one; both are transcribed here at their own precision.

**M4 — the floored collocation weights.** 15 of 16 collocation weights sit on the numerical floor: `w_min` is pinned at the float32 tiny clamp on 502/502 steps and `w_mean = 0.0625 = 1/16` exactly on 502/502 steps, so `w₂…w₁₆` all sit at the clamp floor and `L_phys = R̄₁/16` (`2026-08-17-residual-frame-conformance-audit.md:121`). `w₁ = 1` by construction (`pinn/loss_catalog.py:340`).

**M5 — the step-501 halt.** `front_idx = 0` at step 501: invariant B (front-advance-within-N, `N = 500`, Phase 49 GATE-03) HALTed, and `front_idx = 0` held on all 502 logged steps (`.planning/milestones/v2.2-phases/52-diagnosis-re-derivation-handoff/52-DIAG-05-REDERIVATION.md:58`; `.planning/milestones/v2.2-phases/50-valid-stage-0-re-run/50-03-SUMMARY.md:84`). The 2026-08-17 audit is not a source for this fact: it carries no training-step number, and its `front_idx` entries describe the initialization-only probe and the whole retained log.

### 4.2 The mechanical coupling

`w_n` is an **exclusive** prefix sum over collocation points: `cumsum_excl[0] = 0`, `cumsum_excl[n] = Σ_{m<n} R̄_m.detach()`, implemented by right-shifting a `torch.cumsum` and prepending a zero (`pinn/loss_catalog.py:326-342`, the shift at `:330-333`, `w₁ = 1` pinned at `:340`). The exponent at point *n* therefore grows with the count of preceding points. `pinn/train.py:1033` runs `collocation_count = 16`; `pinn_architecture.md:454` specifies `n_col = 4096` in `sample_collocation_points`, and `:461` states the spec's range of 2048–4096. `4096 / 16 = 256` exactly, so calibrating at one count and honoring the other moves the exponent by roughly **256×**. This is verifiable arithmetic on two already-fixed numbers; stating it is mechanism.

SPEC-06 makes this coupling a joint-ratification requirement: roadmap Success Criterion 5 therefore treats a ruling that does not dispose of `N_t` / `n_col` as incomplete. The `pinn/` citations here record the current numeric divergence being disposed of — never authority for what either number is to become.

### 4.3 The five decision surfaces

The five surfaces appear in the order `52-VER-20-ROUTING-HANDOFF.md` item (e) and `.planning/REQUIREMENTS.md` ERW-01 name them. That order is transcription order: it carries no precedence, no priority, and no sequencing implication.

#### S1 — `η_c`, the causal-weight exponent coefficient

- **What it is:** the coefficient in the causal-weight exponent, `w_n = exp(−η_c Σ_{m=1}^{n−1} stopgrad(R̄_m))`.
- **Where specified:** `pinn_architecture.md:435` (the `w_n` formula in §3.2). The current implementation value is at `pinn/constants.py:71` (`CAUSAL_ETA_C = 1.0`).
- **Contract marker:** `pinn_architecture.md:445` — the Phase 35 contract block (LOSS-04; D-04 RESOLVED-WITH-INSTRUCTION / owner-ratified Option A; AC-LOSS-04), quoted: *"This file keeps the per-time causal weighting component as the default: `w_1 = 1`, `w_n = exp(-eta_c * sum_{m<n} stopgrad(Rbar_m))`, and `eta_c = 1`."* A change to `η_c` makes this block the ruling SPEC-01 must name as superseded.
- **Coupled to:** S4 (`N_t` / `n_col`) through the exclusive prefix sum (§4.2); SPEC-06 makes the two dispositions joint.
- **What the evidence pins, and does not:** the failure signature at `η_c = 1` on unnormalized `R̄` — saturation at step 0 (§4.1). It does not pin any value, form, or normalization under which the mechanism would not saturate at initialization — see §7.

#### S2 — the `R̄` normalization and its reference scale

- **What it is:** whether and how `R̄` is normalized before it enters the causal exponent, and against what reference scale.
- **Where specified:** nowhere. The `pinn_architecture.md:435` formula consumes `R̄` unnormalized, and no normalization is specified anywhere in the spec. The absence is itself the fact this surface states.
- **Contract marker:** none.
- **Coupled to:** S1 directly (the exponent consumes `R̄`); S3 indirectly (the initialization scale sets the magnitude `R̄` starts at).
- **What the evidence pins, and does not:** the magnitude `R̄ ≈ 10¹⁰` at initialization and its consequences (§4.1). It does not pin whether a normalization is to be introduced, or any reference scale — see §7.

#### S3 — `ω₀` / `first_omega_0`, the SIREN initialization scale

- **What it is:** the first-layer SIREN frequency parameter — the initialization scale that sets the network's second-derivative magnitude.
- **Where specified:** `pinn_architecture.md:181` (§2.2: *"`first_omega_0` is fixed at `30` and is not scheduled during training."*). §2.4's hyperparameter table carries the same value at `pinn_architecture.md:274` under the header at `pinn_architecture.md:267`; that table header is already routed to Phase 56 by Phase 53's unswept inventory and is not this packet's concern.
- **Contract marker:** the fixed-at-30 sentence at `:181` is the contract marker.
- **Coupled to:** S2's magnitude, and therefore S1's exponent, through the chain in §4.1.
- **What the evidence pins, and does not:** the second-derivative magnitudes `1.94×10⁵`–`2.79×10⁵` and the resulting `R̄` medians at initialization (§4.1). It does not pin anything about any scale other than the locked one — see §7.

#### S4 — `N_t` / `n_col`, the collocation-point count

- **What it is:** the number of collocation points the physics loss averages over.
- **Where specified:** `pinn_architecture.md:454` (`n_col=4096` in `sample_collocation_points`) and `pinn_architecture.md:461` (the spec's stated range 2048–4096). The current training run uses `pinn/train.py:1033` (`collocation_count=16`).
- **Contract marker:** none of its own; bound to S1 by SPEC-06's joint-ratification requirement.
- **Coupled to:** S1, through the exclusive prefix sum — the exponent grows with the count of preceding points, and the two fixed numbers differ by the exact factor 256 (§4.2).
- **What the evidence pins, and does not:** both fixed numbers and the 256× arithmetic (§4.2). It does not pin any count a recalibrated recipe would use — see §7.

#### S5 — the causal-exponent clip's declared semantics

- **What it is:** the purpose and bound (if any) of the clip applied to the causal exponent.
- **Where specified:** `pinn_architecture.md:668-671` — *"Clip the causal exponent to avoid underflow, but do not choose a numeric clipping bound in Phase 19; surface a gap if one is needed. The causal exponent clip is required only to avoid underflow."* (the first sentence spans `:668-670`; `:671` is the self-contained second sentence). The current implementation derives the floor per dtype/device rather than hardcoding it (`pinn/loss_catalog.py:73`, `:77`; consumed at `:334-339`).
- **Contract marker:** the underflow-only purpose at `:668-671`, plus the Phase 35 guard block at `pinn_architecture.md:692`, which defers the numeric bound to FUT.
- **Coupled to:** S1 and S2 — the clip is the mechanism's defense against the exponent magnitude those surfaces produce.
- **What the evidence pins, and does not:** the underflow-only purpose. It does not pin any numeric bound — see §7.

## 5. The framed questions

Each question states what a complete answer specifies — the structure of an adequate answer, never a value. No question names a candidate, a range, a form, or a direction of change. The ordering follows §4.3's transcription order and carries no precedence; no question is marked central.

### 5.1 `η_c`, the causal-weight exponent coefficient (S1)

What a complete answer specifies: a disposition of the exponent coefficient against the residual magnitude it consumes, stating the evidence (cited to `F-` rows and source documents) that locates the working range of the mechanism, and stating explicitly how the disposition engages the `N_t` / `n_col` question, given that SPEC-06 makes the two joint. The question: what disposition of the causal-weight exponent coefficient does the assembled evidence support, against what residual magnitude, and what evidence would establish that the mechanism is not saturated at initialization?

### 5.2 The `R̄` normalization and its reference scale (S2)

What a complete answer specifies: whether a normalization is to be introduced, and if so its form and its reference scale, with the evidence that fixes the scale, plus a statement of how the normalized quantity feeds the causal exponent and the clip. The question: does the assembled evidence support introducing a normalization of `R̄` before the causal exponent, and against what reference scale would any such normalization be defined?

### 5.3 `ω₀` / `first_omega_0`, the SIREN initialization scale (S3)

What a complete answer specifies: whether the locked initialization scale stands, and if not, what the changed scale implies for the second-derivative magnitude the causal mechanism is calibrated against — with the cited evidence for that magnitude at the candidate scale. The question: does the assembled evidence support changing the SIREN initialization scale, and what would a changed scale imply for the residual magnitude the causal weighting mechanism consumes?

### 5.4 `N_t` / `n_col`, the collocation-point count (S4)

What a complete answer specifies: a disposition of the collocation-point count that is stated jointly with the `η_c` disposition, because the exclusive prefix sum makes the exponent magnitude depend on the count of preceding points — the exact factor between the two fixed numbers is 256 (§4.2). The question: what collocation-point count does the assembled evidence support, stated jointly with the exponent-coefficient disposition, and what evidence fixes that count?

### 5.5 The causal-exponent clip's declared semantics (S5)

What a complete answer specifies: whether the underflow-only purpose stands, and if a numeric bound is to be chosen, what its form and value are and which of the other dispositions it depends on. The question: does the assembled evidence support a numeric causal-exponent clip bound, and on which of the other four dispositions would any such bound depend?

### 5.6 The couplings across the surfaces (SPEC-06)

What a complete answer specifies: a joint disposition of the surfaces that interact through the mechanism — the exponent coefficient and the collocation-point count through the prefix sum, the residual magnitude and the initialization scale through the second-derivative chain, and the clip through whichever of those changes — with the evidence for the joint choice, so that no surface's disposition is left under-determined by the others. The question: what joint disposition of the coupled surfaces does the assembled evidence support, and what evidence would establish that the chosen combination is coherent at initialization and through training?

## 6. Claims register

Two tables, per the standing convention. `F-` rows are established evidence a reader may rely on. `H-` rows are prior analysis to challenge, and every `H-` row carries the label "agent analysis — not established fact".

### F- rows (established evidence)

| ID | Claim (numbers verbatim) | Source (file:line) | Status |
|---|---|---|---|
| F-01 | The six-row seed/IC initialization probe: seeds 41, 42, 43, 0, 7, and an alt-mass/random-IC 41 variant; columns `‖r′‖`, `‖v′‖`, `‖a′‖ = ‖d²r′/du²‖`, `‖F_grav‖`, min pairwise sep, `R̄` median, `front_idx`; all six rows are the probe's printed output, medians over the 16 collocation points | `docs/work/reviews/milestone_v2.2/50-valid-stage-0-re-run/2026-08-17-residual-frame-conformance-audit.md:142` (`:144-149`, `:151`) | established |
| F-02 | `first_omega_0 = 30` sets the second-derivative magnitude: `‖a′‖` column values `1.94×10⁵`–`2.79×10⁵`, `R̄` medians `1.25×10¹⁰`–`2.60×10¹⁰` | `docs/work/reviews/milestone_v2.2/50-valid-stage-0-re-run/2026-08-17-residual-frame-conformance-audit.md:142-151` (numbers), `:163-169` (prose); `.planning/milestones/v2.2-phases/52-diagnosis-re-derivation-handoff/52-VER-20-ROUTING-HANDOFF.md:37` | established |
| F-03 | `exp(−η_c R̄)` underflows float32 at `R̄ > 87.34`; the routing handoff's rounded form is `87.3` | `docs/work/reviews/milestone_v2.2/50-valid-stage-0-re-run/2026-08-17-residual-frame-conformance-audit.md:127`; `.planning/milestones/v2.2-phases/52-diagnosis-re-derivation-handoff/52-VER-20-ROUTING-HANDOFF.md:40` | established |
| F-04 | 15 of 16 collocation weights on the numerical floor: `w_min` pinned at the float32 tiny clamp on 502/502 steps, `w_mean = 0.0625 = 1/16` exactly on 502/502 steps, so `w₂…w₁₆` all sit at the clamp floor and `L_phys = R̄₁/16`; `w₁ = 1` by construction | `docs/work/reviews/milestone_v2.2/50-valid-stage-0-re-run/2026-08-17-residual-frame-conformance-audit.md:121`; `pinn/loss_catalog.py:340` | established |
| F-05 | `front_idx = 0` at step 501: invariant B (front-advance-within-N, `N = 500`, Phase 49 GATE-03) HALTed; `front_idx = 0` on all 502 logged steps | `.planning/milestones/v2.2-phases/52-diagnosis-re-derivation-handoff/52-DIAG-05-REDERIVATION.md:58`; `.planning/milestones/v2.2-phases/50-valid-stage-0-re-run/50-03-SUMMARY.md:84` | established |
| F-06 | `w_n` is an exclusive prefix sum: `cumsum_excl[0] = 0`, `cumsum_excl[n] = Σ_{m<n} R̄_m.detach()`, implemented by right-shifting a `torch.cumsum` and prepending a zero | `pinn/loss_catalog.py:326-342` (shift `:330-333`) | established |
| F-07 | `collocation_count = 16` at `pinn/train.py:1033` versus `n_col = 4096` at `pinn_architecture.md:454` (range 2048–4096 at `:461`); `4096 / 16 = 256` exactly | `pinn/train.py:1033`; `pinn_architecture.md:454,:461` | established |
| F-08 | The Phase 35 causal-training contract fixes `eta_c = 1` (LOSS-04; D-04 RESOLVED-WITH-INSTRUCTION / owner-ratified Option A; AC-LOSS-04) | `pinn_architecture.md:445` | established |
| F-09 | `first_omega_0` is fixed at `30` and is not scheduled during training | `pinn_architecture.md:181` | established |
| F-10 | The causal exponent clip is required only to avoid underflow; no numeric bound is chosen in the spec | `pinn_architecture.md:668-671` (guard block `pinn_architecture.md:692`) | established |

One claim moved from `H-` in the trainex-r2 round to `F-` here, and the move is recorded rather than silent [r2-QUAL]: the `ω₀ = 30` second-derivative mechanism was derived by that round's Q3 as a **hypothesis**, and it was subsequently confirmed by the 2026-08-17 conformance audit — so it appears here as `F-02` with the audit as its source, and the r2 round is its prior, not its evidence [r2-QUAL].

### H- rows (prior analysis — challenge)

| ID | Claim | Source | Label |
|---|---|---|---|
| H-01 | The trainex-r2 round's Q3 interpretive content: the SIREN-scale mechanism as derived by that round, and its framing of what the diagnosis implied [r2-QUAL] | `trainex-r2-research-report.md` Q3 (qualified in §0) | agent analysis — not established fact |

The register records claims. It does not order them by standing and carries no support rubric. A claim whose standing is unclear from the sources goes in the `H-` table with its uncertainty stated.

## 7. What the assembled evidence cannot answer

This section names the gaps the assembled evidence leaves open, one entry per decision surface plus the cross-cutting entries. It records gaps; it does not resolve them. An entry ends at the statement of absence.

**S1 — `η_c`.** The evidence pins the failure signature at the locked value on unnormalized `R̄` — saturation at step 0, 15 of 16 weights floored (F-03, F-04, §4.1). It does not pin any value, form, or normalization under which the mechanism would not saturate at initialization. The silence is the sources' own: `pinn_architecture.md:445` fixes the current value and nothing else, and `52-VER-20-ROUTING-HANDOFF.md:51` declares the correct calibration a research question rather than an engineering default.

**S2 — the `R̄` normalization.** The evidence pins the magnitude `R̄ ≈ 10¹⁰` at initialization and its consequence (§4.1). It does not pin whether a normalization is to be introduced, its form, or its reference scale. The silence: `pinn_architecture.md:435` consumes `R̄` unnormalized, and no normalization is specified anywhere in the spec — the absence is the fact.

**S3 — `ω₀` / `first_omega_0`.** The evidence pins the second-derivative magnitudes the locked scale produces (F-02, §4.1). It does not pin anything about any other scale. The silence: `pinn_architecture.md:181` fixes the value at 30 and is silent on alternatives.

**S4 — `N_t` / `n_col`.** The evidence pins the two fixed numbers and the exact 256 factor between them (F-07, §4.2). It does not pin any count a recalibrated recipe would use. The silence: `pinn_architecture.md:454` and `pinn_architecture.md:461` fix the spec's value and stated range, and no source states a disposition of the count.

**S5 — the clip.** The evidence pins the underflow-only purpose (F-10). It does not pin any numeric bound. The silence: `pinn_architecture.md:668-671` states the purpose and chooses no bound, and `pinn_architecture.md:692` defers the bound to FUT.

**Cross-cutting — interactions beyond the arithmetic.** §4.2 states the arithmetic coupling between the exponent and the collocation-point count. The evidence does not establish how the surfaces interact beyond that arithmetic — no source tests combined dispositions.

**Cross-cutting — behavior after initialization.** Both the 2026-08-17 audit and the eventual Phase 55 INST-04 probe characterize the architecture at initialization. The evidence does not establish post-initialization behavior under any recalibrated recipe, because no such run exists.

**Cross-cutting — the trainex-r2 construction limit.** That round's output contract clause 3 barred it from naming a remedy [r2-QUAL], so by construction it could not answer what the recalibrated values are; its Q3 content stands in §6's `H-` table as prior analysis.

This enumeration is the surfaced content of `GAP-54-01` in `.planning/phases/54-recalibration-decision-grounding/54-GAPS.md` and `.planning/milestones/v2.3-GAPS.md`; the register points here rather than duplicating it.

## 8. Provenance

- **Package baseline (`source_baseline`):** `6a4f9b9902ab62e1d1f57bba0e521f38120c416d` — the repository commit at package assembly, and the ERW Rule-5 pin every `file:line` citation in §4, §6, and §7 is re-derivable against.
- **Complementary evidence pins:** the 2026-08-17 residual-frame conformance audit is committed at `ae14a99e` (as named in the roadmap's grounding list, `.planning/ROADMAP.md:47`). The operative diagnosis (`52-DIAG-05-REDERIVATION.md`) carries no separate pin of its own; it is committed in the same tree as the audit. The pins are complementary rather than superseding: the package baseline pins the state this packet was assembled against, and the audit pin fixes the evidence document itself.
- **The ERW Rule 20 live-tree pin is not recorded here.** It belongs to the delivery note and is filled at ERW-02, because it records the tree an external agent actually saw during an engagement — and no engagement exists yet.

<!-- NEUTRALITY-BAN-END -->

## 9. Output contract

This section specifies the deliverable a commissioned external research agent produces — and it is the one section of this packet that uses the vocabulary of marked defaults, door classification, and decision sheets, because ERW Rule 7 requires that deliverable to carry them. That vocabulary describes the external agent's document, never this packet's own position: this packet still marks no default and ranks no option (§1.3, §10).

Produce one research report, structured as per-question sections plus a dedicated up-front findings section and a dedicated gaps section.

**The Rule 7 build-design contract.** For each decision, an options menu of two to four options with their mechanical-surface trade-offs and their cross-decision interactions; a **suggested default clearly marked** on each menu; a **one-way versus two-way door classification** on every suggested default and every deviation from it; a fill-in **decision sheet** with columns for the decision, its options, the suggested default, the door type, and the owner's pick; a **composed first-run recipe** presented as a cross-menu coherence check; a "what the runbook inherits" section; and a claims-and-uncertainty register. Rule 7's own prompt requirement: suggest defaults; never decide.

The door classification marks whether each suggested default is a one-way or a two-way door.

**The Rule 17 premise-challenge mandate, as a duty.** Test this packet's own stated premises against the repository, and report contradictions as first-class findings up front, ahead of the per-question answers. An agent that finds a false premise and buries it has failed the round. The trainex-r2 report's "source-verification findings that bear on multiple questions" section, placed ahead of the per-question answers, is the shape to produce [r2-QUAL].

**The Rule 18 read-only bars, in the imperative.**
No file edited.
No training run.
No evaluation invoked.
No command with side effects, no commit.
This project's standing bars apply to external agents exactly as they apply to in-repo agents: no held-out evaluation, no new training runs, no framework-spec edits, and no remedy selection. Discriminating experiments are proposed as owner-gated options, never performed.

**The Rule 9 gap discipline.** Where the attached materials and the repository are silent or ambiguous, record it in the gaps section — never invent. A gap is a legitimate, valued output.

**The Rule 19 notice.** Every repo-derived claim arrives as a checkable assertion carrying a `file:line`, and the project verifies each one in-repo — with the verification recorded — before it informs any decision, roadmap, or spec edit.

The consolidated decision sheet is presented to the owner for ratification at checkpoint ②. It is a candidate, not the ratification.

## 10. Neutrality self-audit

This section defines the neutrality checks and records their results. It sits outside the neutrality-ban region because it defines the check; a check definition that names its own tokens is not the packet's voice.

| Check | Scope | Method | Result |
|---|---|---|---|
| Bar A — D-04 Layer-1 scoped lexical ban | the `NEUTRALITY-BAN` region (§0's own voice through §8) | region-scoped case-insensitive grep for: `recommend`, `suggest`, `prefer`, `best`, `most likely`, `primary candidate`, `default to`, `should use`, `ranked`, `leading option`; expected empty | PENDING — run at phase close (plan 54-05) |
| Bar A2 — D-04 Layer-2 Rule-7 carve-out presence | §9 Output contract | case-insensitive count of `suggested default` / `one-way` / `two-way` / `decision sheet` in §9; expected at least 4 once §9 is written | PENDING — run at phase close (plan 54-05) |
| Bar B — D-06 tag discipline | all lines outside §0 | case-sensitive literal `trainex-r2` line match minus lines carrying `[r2-QUAL]`; expected empty | PENDING — run at phase close (plan 54-05) |
| Bar C — D-02 branch-neutrality file absence | the trainex-r3 round root | absence of `research_package/RESEARCH-AGENT-PROMPT.md`, `specs/`, and `research_results/`; expected to print `NEUTRAL` | PENDING — run at phase close (plan 54-05) |
| Bar D — read-only boundary | framework specs, `pinn/`, `simulation_data/`, `tests/` | `git diff --stat` over the cited paths; expected empty | PENDING — run at phase close (plan 54-05) |
| Tree completeness (45-AUDIT Check 1) | the trainex-r3 round root | `find … -type f` prints exactly the two authored paths | PENDING — run at phase close (plan 54-05) |

The two-layer neutrality criterion these checks enforce:

- **Layer 1** is the scoped lexical ban binding the packet's own voice in §0 through §8 — the region delimited by the two region markers defined in the section map.
- **Layer 2** is the explicit ERW Rule-7 carve-out for §9: §9 must carry the vocabulary of marked defaults, door classification, and decision sheets, because roadmap Success Criterion 4 requires this packet to specify the trainex-r3 output contract. A §9 that is lexically clean under Layer 1's vocabulary means the Rule-7 contract was gutted rather than satisfied — which is what Bar A2 exists to catch.

**Excluded 45-AUDIT checks, with reasons.** Check 3 (self-containment / zero repo-path markers) is Route-A-only and does not apply to a Route-B master, whose Rules 1–2 inversion makes repository paths expected. Check 4 (snapshot fidelity) and Check 6 (pin consistency across snapshot files) presuppose the `specs/` bundle D-02 deliberately withholds. These checks are deferred to the ERW-02 audit if the round is commissioned, not waived.
