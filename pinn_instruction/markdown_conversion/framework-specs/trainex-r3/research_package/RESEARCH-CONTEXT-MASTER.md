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

_Written by plan 54-04._

## 3. Source tiering — how to treat each kind of content

_Written by plan 54-04._

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

_Written by plan 54-04._

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

_Written by plan 54-04._

## 8. Provenance

_Written by plan 54-04._

<!-- NEUTRALITY-BAN-END -->

## 9. Output contract

_Written by plan 54-04._

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
