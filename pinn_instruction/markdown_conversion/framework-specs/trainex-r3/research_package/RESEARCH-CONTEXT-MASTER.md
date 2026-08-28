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

**Status: commissioned.** The owner selected `commission trainex-r3` at checkpoint ① on 2026-08-21; the ruling record is `.planning/phases/54-recalibration-decision-grounding/54-RULING.md`. Checkpoint ② — the recalibration ratification itself — remains open and is what this round informs.

**The three uploaded attachments** (ERW Rule 15 caps a sub-package at five; this round ships three):

| # | Attachment | Treatment |
|---|---|---|
| 1 | `RESEARCH-CONTEXT-MASTER.md` — this file | The entry point. Read first. Its §3 fixes how to treat every other source, §5 carries the questions, §9 the output contract. |
| 2 | `framework-specs-bundle.md` | Verbatim locked framework-spec excerpts: SIREN initialization and §2.2's fixed-at-30 sentence, the SQR-SkipResNet formulation, the architectural hyperparameters, §3.2's physics residual and causal weighting in full, the collocation-sampling contract, the clip guard, the warmup, the optimizer split, and the Stage-0 curriculum and total-loss assembly. **Hard constraint** — authoritative as a statement of what the contract currently says. |
| 3 | `v2.2-closure-evidence-bundle.md` | Verbatim, in full: the 2026-08-17 residual-frame conformance audit, `52-VER-20-ROUTING-HANDOFF.md` (the routing authority; item (e) is this round's subject), and `52-DIAG-05-REDERIVATION.md` (the operative diagnosis). **Hard constraint** for the evidence; the *reasoning* is testable under ERW Rule 17. |

Files that exist at the round root but are **not** uploaded: `DELIVERY-NOTE.md` (user-only routing), `RESEARCH-AGENT-PROMPT.md` (pasted, not attached), and `research_results/` (created at delivery).

**Route B means the attachments are not the boundary.** They frame the questions and fix the baseline. The repository is an additional evidence source, and published literature is a required one (§3). Nothing here says "attached files only" — under ERW Rule 17 that instruction would contradict the mandate.

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
- **External published literature (the round's own evidence tier, added at ERW-02):** the causal-weighting formula in `pinn_architecture.md` §3.2 is not original to this project, and the framework spec's `## References` section does not cite a source for it (`F-13`). Published literature is therefore an expected and required evidence source for this round, on the same footing as the repository: cited by author, title, venue, and year, with the claim it supports stated in the source's own terms. A literature claim is a checkable assertion like any other — it carries its citation precisely so the project can re-derive it. Where the literature and this project's formulation differ, the difference is itself a finding.
- **Repo-derived evidence (the Route-B tier):** under `access_mode: open-book` the repository is an additional evidence source and not a replacement for this package. A claim derived from the live tree arrives as a checkable assertion carrying a `file:line`, not as an established fact, and ERW Rule 19 requires every such claim to be independently verified in-repo, with the verification recorded, before it informs a decision, a roadmap, or a spec edit. `pinn/` is not a grounding source for spec decisions — it is cited in §4 only as the current divergence being disposed of.

**Anchor-resolution rule (Route-B hazard, added at ERW-02 — read before resolving any citation).** Five files named `pinn_architecture.md` exist in this repository, and they carry **different line numbering**:

| Path | Lines | Standing |
|---|---|---|
| `pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md` | 1098 | **The live locked spec. The only authoritative one. Every citation in this packet means this file.** |
| `pinn_instruction/markdown_conversion/framework-specs/integrity-r1/specs/pinn_architecture.md` | 1010 | frozen snapshot of an earlier round — not authoritative |
| `pinn_instruction/markdown_conversion/framework-specs/trainex-r1/specs/pinn_architecture.md` | 1013 | frozen snapshot of an earlier round — not authoritative |
| `pinn_instruction/markdown_conversion/framework-specs/integrity-r2/specs/pinn_architecture.md` | 1064 | frozen snapshot of an earlier round — not authoritative |
| `pinn_instruction/markdown_conversion/framework-revisions/research_reports/02-data-pipeline-and-validation/research_package/specs/pinn_architecture.md` | 1010 | frozen snapshot of an earlier round — not authoritative |

The divergence is not cosmetic: `:181` is the locked `first_omega_0` sentence in the live spec and is unrelated prose in the `integrity-r1` snapshot. The same applies to `ctl_instruction.md`. Resolve every anchor against the **live** file at the path above, and **resolve by content match, not by line number** — `pinn_architecture.md` was edited by this milestone's Phase 53, so line anchors quoted in planning documents written before those commits are stale by construction. `54-RULING.md`'s "Anchor-drift warning" records four such already-confirmed stale anchors in `.planning/REQUIREMENTS.md` and `.planning/ROADMAP.md`; treat any anchor found outside this packet as suspect until content-matched.

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

**M2 — the chain, and the two factors the audit attributes it to.** The physics residual is a second-derivative operator, and the audit attributes the magnitude of that second derivative to **two compounding factors**, not one. Quoted verbatim:

> The physics residual is a **second-derivative operator**. A SIREN carries broadband high-frequency content by design (`first_omega_0 = 30`, ARCH-01, §2.2: "a high initial frequency injects a high-frequency Fourier basis"), and the 12-layer SQR-SkipResNet stack compounds it — the `LayerNorm(x)^p` skip branch with `p = 2` has Jacobian `2·LN(x)/std(x)` ≈ 3 per odd layer, six of them. The measured ratio `‖a′‖/‖v′‖ ≈ 650–900` is the network's effective angular frequency in `u`; differentiating twice multiplies amplitude by `ω² ≈ 10⁵–10⁶`.

(`docs/work/reviews/milestone_v2.2/50-valid-stage-0-re-run/2026-08-17-residual-frame-conformance-audit.md:165`.)

The measured effective angular frequency `650–900` therefore stands against `first_omega_0 = 30`: those are not the same number, and the audit's own account places the difference in the SQR-SkipResNet stack. The `‖a′‖` column values run `1.94×10⁵`–`2.79×10⁵` in network units; the `R̄` medians run `1.25×10¹⁰`–`2.60×10¹⁰` (`docs/work/reviews/milestone_v2.2/50-valid-stage-0-re-run/2026-08-17-residual-frame-conformance-audit.md:142-151` for the numbers; corroborated independently at `.planning/milestones/v2.2-phases/52-diagnosis-re-derivation-handoff/52-VER-20-ROUTING-HANDOFF.md:37`).

**Correction recorded (ERW-02, 2026-08-21; see §11).** This entry previously read "`first_omega_0 = 30` sets the second-derivative magnitude," attributing the scale to `first_omega_0` alone — narrower than the audit it cites. Only the `first_omega_0` sentence carries an owner-ratified contract marker and appears among the decision surfaces in §4.3; the SQR-SkipResNet stack's contribution to the same quantity is recorded here as evidence, and its absence from the surface list is named in §7.

**M3 — the float32 underflow bound, at both precisions.** The causal weight `exp(−η_c R̄)` underflows float32 at `R̄ > 87.34` — 8.46 decades below the median (`2026-08-17-residual-frame-conformance-audit.md:127`). The rounded form `87.3` appears in the routing handoff and carries its own citation (`52-VER-20-ROUTING-HANDOFF.md:40`). The audit carries the precise value; the handoff carries the rounded one; both are transcribed here at their own precision.

**M4 — the floored collocation weights.** 15 of 16 collocation weights sit on the numerical floor: `w_min` is pinned at the float32 tiny clamp on 502/502 steps and `w_mean = 0.0625 = 1/16` exactly on 502/502 steps, so `w₂…w₁₆` all sit at the clamp floor and `L_phys = R̄₁/16` (`2026-08-17-residual-frame-conformance-audit.md:121`). `w₁ = 1` by construction (`pinn/loss_catalog.py:340`).

**M5 — the step-501 halt.** `front_idx = 0` at step 501: invariant B (front-advance-within-N, `N = 500`, Phase 49 GATE-03) HALTed, and `front_idx = 0` held on all 502 logged steps (`.planning/milestones/v2.2-phases/52-diagnosis-re-derivation-handoff/52-DIAG-05-REDERIVATION.md:58`; `.planning/milestones/v2.2-phases/50-valid-stage-0-re-run/50-03-SUMMARY.md:84`). The 2026-08-17 audit is not a source for this fact: it carries no training-step number, and its `front_idx` entries describe the initialization-only probe and the whole retained log.

**M6 — the comparison scale the audit states.** The audit gives the scale the locked formula presumes, and the measured scale a converged network reaches, in one sentence:

> The causal weight `exp(−η_c R̄)` with `η_c = 1` and an **unnormalized** `R̄` presumes `R̄ = O(1)`, which is what a *converged* network gives (Gate B: residual = 0.65 % of `‖a′‖` on a true trajectory). At initialization the same quantity is ~10¹⁰.

(`docs/work/reviews/milestone_v2.2/50-valid-stage-0-re-run/2026-08-17-residual-frame-conformance-audit.md:167`.) The `0.65 %` figure is the audit's own, measured on a true trajectory. It is transcribed because it is the only converged-regime residual scale any source in this package states; this packet takes no position on whether it is a reference scale for anything.

**M7 — internal consistency of the six-row probe (ERW-02 check, 2026-08-21).** The probe's own columns are mutually consistent with the locked `R̄` definition. `pinn_architecture.md` defines `R̄_n = (1/3) Σ_{i=1}^{3} ‖f_i(u_n)‖²`, and `‖F_grav‖` is four to five decades below `‖a′‖` in every row, so `R̄ ≈ ‖a′‖² / 3`. Evaluating that against the six rows of M1: `1.37`, `2.47`, `1.61`, `2.59`, `1.25`, `1.73` (`×10¹⁰`) against the printed medians `1.37`, `2.46`, `1.62`, `2.60`, `1.25`, `1.74` (`×10¹⁰`) — agreement to three significant figures in all six rows. This is arithmetic on the packet's own transcribed numbers and adds no new source.

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

#### The remedy families the routing authority authorizes

The five surfaces above are the surfaces named by `.planning/REQUIREMENTS.md` ERW-01. Item (e)'s own statement of what it is asking for is wider than a list of surfaces, and it is transcribed here verbatim so this packet does not narrow its own routing authority:

> **This is not a request to reword a spec table.** It is a request to
> recalibrate one or more of: `η_c` / the causal-exponent form, an explicit
> normalization of `R̄` (e.g. by a converged-scale reference), or the SIREN
> initialization scale — or to redesign the curriculum mechanism so it does not
> require the two to already agree at initialization.

(`.planning/milestones/v2.2-phases/52-diagnosis-re-derivation-handoff/52-VER-20-ROUTING-HANDOFF.md:45-49`.)

Three things in that sentence are not captured by S1–S5 as stated above, and are recorded rather than left implicit:

1. **"the causal-exponent form."** Item (e) pairs `η_c` with the *form* of the exponent, not only its coefficient. S1 as stated is the coefficient.
2. **"(e.g. by a converged-scale reference)."** Item (e) names an example of a reference scale. S2 as stated records that no reference scale is pinned anywhere in the spec; that remains true, and item (e)'s example is transcribed for completeness rather than as a pin.
3. **"or to redesign the curriculum mechanism so it does not require the two to already agree at initialization."** A fourth remedy family, at the level of the mechanism rather than its parameters. No surface among S1–S5 corresponds to it.

SCOPE-33 authorizes exactly the VER-20 items plus the coupled `N_t` disposition, so all four families sit inside this milestone's spec-edit authorization and inside this round's scope.

**Correction recorded (ERW-02, 2026-08-21; see §11).** The five surfaces were assembled from the requirement text and did not transcribe item (e)'s remedy enumeration. Leaving the fourth family unstated narrowed the decision space relative to the packet's own cited routing authority. Nothing in S1–S5 is withdrawn; the enumeration is added alongside it.

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

### 5.7 Requirements every answer carries (cross-cutting, added at ERW-02)

These constrain the *form* of an adequate answer. They name no value, no direction, and no candidate.

**(a) Quantified capacity, per surface.** For each surface an answer dispositions, state the scaling law relating a change on that surface to the resulting change in the causal exponent at initialization; **derive it rather than assert it**; and state the magnitude of change that surface is capable of producing. State that magnitude against the two thresholds the evidence already fixes — the float32 underflow point (`F-03`) and the front-advance condition implied by the `front_idx` definition (`F-05`, and the definition itself as it stands in the repository). A disposition whose stated capacity does not reach the threshold it addresses is incomplete.

**(b) Behaviour across the residual range, not only at initialization.** Every source in this package characterizes initialization; §7 records that as a gap. For each disposition, state what the causal weight vector does as `R̄` varies across the range a training run must traverse, and state what that range is with the evidence fixing it. An answer that establishes a disposition works at step 0 and is silent about later training has answered half the question.

**(c) The source method, identified and cited.** Identify the published method the §3.2 causal-weighting formula derives from; cite it; and state **that method's own calibration procedure** for the exponent coefficient in the source's own terms — including whatever criterion the source uses to decide the coefficient is set correctly, and including how the source treats the number of terms entering the prefix sum. State every point at which this project's formulation departs from the source. `F-13` records what the spec's reference list does and does not cover.

**(d) The mechanism-redesign family.** §4.3 records that item (e) authorizes a fourth remedy family, at the level of the mechanism rather than its parameters. It is in scope. State whether the assembled evidence and the literature bear on it, and if an answer dispositions it, disposition it under the same output contract as the rest.

**(e) Independent derivation before comparison.** Where this packet transcribes an analysis — every `H-` row in §6 — derive the result independently first, then state agreement or disagreement with what is transcribed, with reasons. ERW Rule 17 makes this a duty rather than a courtesy.

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
| F-11 | The 2026-08-17 audit attributes the initialization second-derivative magnitude to **two** compounding factors: `first_omega_0 = 30`, and the 12-layer SQR-SkipResNet stack (the `LayerNorm(x)^p` skip branch with `p = 2`, Jacobian `2·LN(x)/std(x)` ≈ 3 per odd layer, six of them). The measured effective angular frequency `‖a′‖/‖v′‖ ≈ 650–900` stands against `first_omega_0 = 30` | `docs/work/reviews/milestone_v2.2/50-valid-stage-0-re-run/2026-08-17-residual-frame-conformance-audit.md:165` | established (ERW-02) |
| F-12 | The audit states the converged-regime comparison scale: `η_c = 1` on unnormalized `R̄` presumes `R̄ = O(1)`, "which is what a *converged* network gives (Gate B: residual = 0.65 % of `‖a′‖` on a true trajectory)" | `docs/work/reviews/milestone_v2.2/50-valid-stage-0-re-run/2026-08-17-residual-frame-conformance-audit.md:167` | established (ERW-02) |
| F-13 | `pinn_architecture.md`'s `## References` section carries 17 numbered entries — covering the Power-Enhanced ResNet, PIG, SIREN, DeepXDE, and PINN-implementation repositories. **No entry cites a source for the causal-weighting scheme** of §3.2 | `pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md:1017-1035` | established (ERW-02) |
| F-14 | The live `R̄` construction matches the locked spec factor: `rbar = (residual ** 2).sum(dim=(-2, -1)) / 3.0` against the spec's `R̄_n = (1/3) Σ_i ‖f_i(u_n)‖²`. (The trainex-r2 round recorded a `1/9`-vs-`1/3` divergence as `RG-04` [r2-QUAL]; it is not present in the post-repair tree) | `pinn/training/controllers.py:656`; `pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md:429` | established (ERW-02) |
| F-15 | A causal-exponent clip **is** implemented in the post-repair tree: `weights = torch.exp(torch.clamp_min(exponent, floor))`, with the floor resolved per dtype and device rather than hardcoded. (The trainex-r2 round recorded `[FACT-W] No causal-exponent clip is implemented` [r2-QUAL]; that observation describes the pre-repair tree) | `pinn/loss_catalog.py:339` (floor at `:334`, `:337`; resolver at `:77`) | established (ERW-02) |

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

**S3-adjacent — the SQR-SkipResNet contribution to the same quantity (added at ERW-02).** `F-11` records that the audit attributes the initialization second-derivative magnitude to `first_omega_0` **and** the 12-layer SQR-SkipResNet stack. Only `first_omega_0` carries an owner-ratified contract marker and appears among the decision surfaces. The evidence does not establish how the two factors divide the measured `‖a′‖/‖v′‖ ≈ 650–900`, and no source dispositions the stack's contribution. Whether the stack constitutes a surface of its own is not settled by anything in this package. The silence: `pinn_architecture.md` §2.3 and §2.4 fix the skip cadence and the power term `p = 2` and say nothing about their derivative-scale consequence, and the audit measures the compound effect without decomposing it.

**Cross-cutting — the source method's own calibration (added at ERW-02).** `F-13` records that the framework spec cites no source for the causal-weighting scheme of §3.2. Nothing in this package states that method's calibration procedure for the exponent coefficient, its criterion for deciding the coefficient is set correctly, or how it treats the number of terms entering the prefix sum. §5.7(c) asks for exactly that. The silence recorded here is this package's, not the literature's.

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

**The literature requirement (§3's external tier, §5.7(c)).** Identify and cite the published method the §3.2 causal-weighting formula derives from, state that method's own calibration procedure for the exponent coefficient in the source's own terms, and state where this project's formulation departs from it. Cite by author, title, venue, and year. The framework spec's reference list does not cover this ground (`F-13`), so a report that answers only from the repository and the attachments has left the round's central evidence tier untouched.

**The Rule 9 gap discipline.** Where the attached materials and the repository are silent or ambiguous, record it in the gaps section — never invent. A gap is a legitimate, valued output.

**The Rule 19 notice.** Every repo-derived claim arrives as a checkable assertion carrying a `file:line`, and the project verifies each one in-repo — with the verification recorded — before it informs any decision, roadmap, or spec edit.

The consolidated decision sheet is presented to the owner for ratification at checkpoint ②. It is a candidate, not the ratification.

## 10. Neutrality self-audit

This section defines the neutrality checks and records their results. It sits outside the neutrality-ban region because it defines the check; a check definition that names its own tokens is not the packet's voice. All results below were produced by the commands stated and recorded at phase close (2026-08-20).

| Check | Scope | Method | Result |
|---|---|---|---|
| Bar A — D-04 Layer-1 scoped lexical ban | the `NEUTRALITY-BAN` region (§0's own voice through §8) | region-scoped case-insensitive grep for: `recommend`, `suggest`, `prefer`, `best`, `most likely`, `primary candidate`, `default to`, `should use`, `ranked`, `leading option` | **PASS — empty.** The region-scoped grep over the delimited region returned no lines (exit 1). |
| Bar A2 — D-04 Layer-2 Rule-7 carve-out presence | §9 Output contract | case-insensitive count of `suggested default` / `one-way` / `two-way` / `decision sheet` in §9; expected at least 4 | **PASS — 4** matching lines (the Rule-7 contract paragraph, the door-classification line, the opening line, the ratification line). |
| Bar B — D-06 tag discipline | all lines outside §0 | case-sensitive literal `trainex-r2` line match minus lines carrying `[r2-QUAL]` | **PASS — empty** (no untagged mention outside §0). |
| Bar C — D-02 branch-neutrality file absence | the trainex-r3 round root | absence of `research_package/RESEARCH-AGENT-PROMPT.md`, `specs/`, and `research_results/` | **PASS — `NEUTRAL`** at checkpoint ① (all three absent). **Superseded at ERW-02:** the owner commissioned the round on 2026-08-21, so the prompt and `specs/` now exist by instruction. The bar certified the pre-commission state and has discharged its purpose. |
| Bar D — read-only boundary | framework specs, `pinn/`, `simulation_data/`, `tests/` | `git diff --stat` over the cited paths | **PASS — empty.** |
| Bar E — planning-source read-only bar | `.planning/REQUIREMENTS.md`, `.planning/ROADMAP.md` | `git diff --stat` over the two files | **PASS — empty** (the stale anchors are warned about, never corrected). |
| Bar F — no cost or preference framing | `54-RULING.md` | case-insensitive grep for cost and effort vocabulary | **PASS — 0.** |
| Tree completeness (45-AUDIT Check 1) | the trainex-r3 round root | `find … -type f | sort` | **PASS — exactly two paths** at checkpoint ①: the master and the delivery note. **Superseded at ERW-02** — see the ERW-02 table below for the commissioned tree. |
| Pin consistency | master frontmatter, §8, delivery note | the `source_baseline` 40-character hash must be byte-identical in all three | **PASS —** `6a4f9b9902ab62e1d1f57bba0e521f38120c416d` in all three places. |
| Boundary attestation (45-AUDIT Check 9) | all cited source trees | `git status --short` over the cited trees plus one attestation sentence per scope item | **PASS — clean.** See the attestation sentences below. |
| Manual 1 — structural neutrality read | §4.3's five surfaces | per-surface confirmation of the five-element D-05 form and the absence of option menus | **PASS —** per-surface verdicts for S1–S5 recorded in `54-02-SUMMARY.md`; re-read at close: no sentence enumerates comparable alternatives. |
| Manual 2 — citation-fidelity read | every `file:line` the packet cites | line-existence check plus content match against the attributed figure | **PASS — 30 distinct citations checked, 30 resolved, 0 failures.** Key figures content-verified with `sed -n` at audit `:121`, `:127`, `:142`, `52-DIAG-05-REDERIVATION.md:58`, and `52-VER-20-ROUTING-HANDOFF.md:37,:40`. |
| Manual 3 — stale-anchor sweep | `pinn_architecture.md:<3-digit>` citations under `.planning/` | read-only resolution against the live file; nothing corrected | **RUN — 348 sites, 6 new findings recorded** in the sweep record below. |

The two-layer neutrality criterion these checks enforce:

- **Layer 1** is the scoped lexical ban binding the packet's own voice in §0 through §8 — the region delimited by the two region markers defined in the section map.
- **Layer 2** is the explicit ERW Rule-7 carve-out for §9: §9 must carry the vocabulary of marked defaults, door classification, and decision sheets, because roadmap Success Criterion 4 requires this packet to specify the trainex-r3 output contract. A §9 that is lexically clean under Layer 1's vocabulary means the Rule-7 contract was gutted rather than satisfied — which is what Bar A2 exists to catch.

**Excluded 45-AUDIT checks, with reasons.** Check 3 (self-containment / zero repo-path markers) is Route-A-only and does not apply to a Route-B master, whose Rules 1–2 inversion makes repository paths expected. Check 4 (snapshot fidelity) and Check 6 (pin consistency across snapshot files) presuppose the `specs/` bundle D-02 deliberately withholds. These checks were deferred to the ERW-02 audit, not waived — **and they are now run**: see Check 4 and Check 6 in the ERW-02 table below.

**Boundary attestation (one sentence per scope item).** SCOPE-33: the framework-spec edits this milestone authorizes are the VER-20 items and the coupled `N_t` disposition — this packet cites the specs and edits none (Bar D). SCOPE-34: the recalibration decision is owner-ratified, never agent-decided — this packet marks no default, ranks no option, and picks nothing (Bar A, Manual 1, §1.3). SCOPE-35: exactly one held-out evaluation exists and this packet neither spends it nor plans its spending. SCOPE-36: Stage-0 only — this packet proposes no platform work. SCOPE-37: iteration after the spec edit is conformance-only — this packet names no tuning loop. SCOPE-38: amending a locked contract requires re-ratification — the three re-ratification blocks live in `54-RULING.md`, not here, and no spec value is changed.

**Requirement and success-criterion traceability (45-AUDIT Check 10).**

| Requirement or success criterion | Certified by |
|---|---|
| ERW-01 — the packet marks no default | Bar A (empty), Manual 1 (per-surface structural read), §1.3 |
| ERW-01 — it ranks no option and picks nothing | Bar A (empty), Manual 1 (no option menus), the no-precedence order statements in §4.3 and `54-RULING.md` |
| ERW-01 — it names its own gaps | §7 (all five surfaces plus cross-cutting entries), `GAP-54-01` (OPEN, pointing here) |
| ERW-01 — it doubles as the trainex-r3 `RESEARCH-CONTEXT-MASTER.md` | D-01/D-02: the packet is that file, at the round root, with the withheld artifacts named by path (Bar C, tree completeness) |
| Roadmap SC-1 — verifiable by inspection | §10 (the criterion travels with the artifact), Bars A, A2, B |
| Roadmap SC-2 — every trainex-r2 citation travels with its premise qualification | §0 qualification block, `[r2-QUAL]` inline tag, Bar B (empty) |
| Roadmap SC-3 (gate half) — the packet is presented at a blocking gate; the agent selects no branch | the checkpoint presentation, `54-RULING.md` (its `Branch` field unfilled), Bar F (0) |
| Roadmap SC-4 | **Not yet applicable** — ERW-02's, discharged after checkpoint ① (D-11) |
| Roadmap SC-5 | **Not yet applicable** — the `N_t` completeness rule is pre-declared in `54-RULING.md` and discharges with the ruling |

**Stale-anchor sweep (Manual 3, read-only; nothing corrected — Bar E proves it).** Command: `grep -rnoE 'pinn_architecture\.md:[0-9]{3}' .planning/ | grep -v '/phases/54-recalibration' | sort -u` → **348 distinct (file, anchor) sites**. Of these, **302** sit in closed-milestone archives (v1.4–v2.1) — pre-existing historical drift, counted and not individually re-attributed; the citing phases are closed, and any Phase 56 edit must re-derive every anchor by content match regardless. The remaining **46 active-scope sites** were resolved one by one. The four already-known stale anchors (recorded in `54-RULING.md`'s anchor-drift section) are confirmed stale again: `:424` (18 sites, incl. `REQUIREMENTS.md:90`, `ROADMAP.md:45,:130`, `.planning/reports/MILESTONE_SUMMARY-v1.6.md:161`) → replacement `:445`; `:167` → `:181`; `:433` → `:454`; `:440` → `:461`. **New Phase-56 findings beyond those four**, each with citing file and resolution:

1. `.planning/phases/53-narrow-spec-codification/53-CONTEXT.md:68,:233` cite `pinn_architecture.md:253` for §2.4's "Recommended Value" header — live `:253` is §2.2 prose; the header is now at `:267` (Phase 53's own context record pre-dates its `spec(53)` commits).
2. `.planning/reports/MILESTONE_SUMMARY-v1.6.md:172` cites `:537` for the Huber-δ calibration row — live `:537` is the softening-parameter prose; the cited row has moved.
3. `.planning/milestones/v2.2-phases/49-conformance-gate/49-RESEARCH.md:1334` cites `:633` — live `:633` is a blank line.
4. `.planning/codebase/CONCERNS.md:60` cites `:263` — live `:263` no longer carries the referenced content.
5. `.planning/forensics/report-20260608-145000.md:84` cites `:987` — live `:987` no longer matches the cited context.
6. `.planning/phases/53-narrow-spec-codification/53-RESEARCH.md:165` cites `:976` for the sections-6–9 numbering anomaly — live `:976` is inside a code block.

Still resolving in the live tree (no action): v2.2 Phase 47's Hamiltonian/Plummer/energy-regularizer anchors (`:505`, `:531`, `:533`, `:539`, `:542`, `:544`), `53-UAT.md:144` (`:518` = the §3.4 heading), and `53-PATTERNS.md` / `53-RESEARCH.md` anchors `:292`, `:310`, `:655`, `:667`. Sweep-method note: the 3-digit pattern truncates four-digit anchors, so `53-PATTERNS.md:144`, `53-PATTERNS.md:225`, and `53-RESEARCH.md:138` render `pinn_architecture.md:1014` / `:1047` as `:101` / `:104` — pattern artifacts, not citations of lines 101/104.

## 11. ERW-02 amendment record (2026-08-21)

The owner commissioned the round at checkpoint ① on 2026-08-21 with the instruction *"make sure that the information inlcuded in that package is accurate and faithful."* This section records every change made to this master after the gate, with its reason, so the pre-gate and post-gate states are distinguishable. Nothing recorded at checkpoint ① is withdrawn; every change is an addition, a correction of a transcription against its own cited source, or a status update.

| # | Change | Class | Reason |
|---|---|---|---|
| A-1 | §4.1 `M2` rewritten to quote the audit's two-factor attribution verbatim; `F-11` added | **correction** | The entry read "`first_omega_0 = 30` sets the second-derivative magnitude." The audit it cites attributes the magnitude to `first_omega_0` **and** the 12-layer SQR-SkipResNet stack (`:165`). The packet was narrower than its source, in a direction that overstates one decision surface. |
| A-2 | §4.3 gains a verbatim transcription of item (e)'s remedy enumeration, and names the three elements S1–S5 do not capture — including the **fourth remedy family** (mechanism redesign) | **correction** | The five surfaces were assembled from the requirement text. Item (e), the packet's own cited routing authority, authorizes a wider remedy space; omitting it narrowed the decision relative to its source. |
| A-3 | §4.1 gains `M6` (the audit's converged-regime comparison scale, `R̄ = O(1)`, residual 0.65 % of `‖a′‖` on a true trajectory) | addition | The only converged-regime residual scale any source in this package states. Transcribed because §5.2 asks about reference scales and the datum existed unused. |
| A-4 | §4.1 gains `M7` (internal consistency of the six-row probe against the locked `R̄` definition) | verification | `R̄ ≈ ‖a′‖²/3` reproduces all six printed medians to three significant figures — an independent check that the probe's columns are mutually consistent. Arithmetic on already-transcribed numbers; no new source. |
| A-5 | §3 gains the **external published literature** evidence tier; §5.7(c) and §9 require the source method be identified, cited, and its own calibration procedure stated | addition | `F-13`: the spec's 17-entry reference list cites no source for the §3.2 causal-weighting scheme. Without this tier the round could return a repository-only answer and leave its central evidence base untouched. |
| A-6 | §3 gains the **anchor-resolution rule** | **correction** | Four files named `pinn_architecture.md` exist with different line numbering (1098 / 1010 / 1013 / 1064); `:181` is the locked `first_omega_0` sentence in the live spec and unrelated prose in the `integrity-r1` snapshot. A Route-B agent resolving a bare filename could silently read the wrong file. |
| A-7 | §5 gains §5.7 — cross-cutting requirements on the *form* of an answer (quantified per-surface capacity with a derived scaling law; behaviour across the residual range, not only at initialization; the source method and its calibration; the mechanism-redesign family; independent derivation before comparison) | addition | The §5.1–§5.6 questions ask what the evidence supports. §7 records that the evidence characterizes initialization only. Without §5.7 the round could answer within that limit and reproduce it. §5.7(e) exists so the round derives independently rather than ratifying what this packet transcribes. |
| A-8 | §6 gains `F-11`…`F-15`; §7 gains two entries (the SQR-SkipResNet contribution; the source method's own calibration) | addition | New verified facts and the gaps they expose. `F-14` and `F-15` retire two trainex-r2 observations [r2-QUAL] that describe the pre-repair tree and no longer hold. |
| A-9 | §2 manifest rewritten from the withheld-artifact statement to the commissioned three-attachment list | status | The round is commissioned; the checkpoint-① manifest is no longer true. |
| A-10 | §10 Bar C and Tree completeness marked superseded; Checks 4 and 6 run | status / verification | Both bars certified the pre-commission state. The two deferred checks are now discharged. |
| A-11 | §3 anchor-resolution rule: fifth `pinn_architecture.md` path added; "Four files" corrected to "Five files" | **correction** | `find . -name 'pinn_architecture.md' -not -path './.git/*' -exec wc -l {} \;` returns five paths. A-6 recorded four (1098 / 1010 / 1013 / 1064). The unlisted copy is `pinn_instruction/markdown_conversion/framework-revisions/research_reports/02-data-pipeline-and-validation/research_package/specs/pinn_architecture.md` (1010 lines). An open-book agent resolving a bare filename against that unlisted copy is the failure the rule exists to prevent. Authorized by `.planning/phases/54-recalibration-decision-grounding/54-RECONCILIATION.md`. A-6's row text is left unchanged. |
| A-12 | §11 Bar A2 result restated as 4 matching lines and 11 occurrences | **correction** | The ERW-02 table described itself as a line-anchored count and recorded 11. The canonical `54-01-PLAN.md` command `grep -cEi` returns 4 matching lines; `grep -oEi \| wc -l` returns 11 occurrences. The stated method did not reproduce the stated number. Both commands now travel with both numbers. Authorized by `54-RECONCILIATION.md`. |
| A-13 | §11 Check 6 restated over five round-root files, not four | **correction** | The ERW-02 table said "all four round files" and omitted `research_package/RESEARCH-AGENT-PROMPT.md`. Re-derivation over the authorized five-path manifest finds the same 40-character pin in all five and no other 40-hex string. Authorized by `54-RECONCILIATION.md`. |
| A-14 | §11 citation-resolution count restated as 52 with its extraction command | **correction** | The ERW-02 table recorded 49 distinct `file:line` citations with no command. `grep -oE '[A-Za-z0-9_./-]+\.(md\|py):[0-9]+' MASTER \| sort -u` returns 52; all 52 resolve in the live tree. Authorized by `54-RECONCILIATION.md`. |
| A-15 | Delivery-note attachment table: specs-bundle block count 13 → 10 | **correction** | `specs/framework-specs-bundle.md` contains 10 `BEGIN VERBATIM` blocks. 13 is the sum across both bundles (10 + 3), which the attachment-2 cell had attributed to the specs file alone. The obligations table already recorded 10 and 3 separately and is unchanged. Authorized by `54-RECONCILIATION.md`. |
| A-16 | Packet `A-10` supersession of the two-path tree-completeness guard is itself superseded by the ledger record | status / verification | The retirement now lives in `.planning/phases/54-recalibration-decision-grounding/54-RECONCILIATION.md` with Checks R1 and R2 as the replacement. The packet's A-10 text is not withdrawn. Authorized by `54-RECONCILIATION.md`. |

### ERW-02 audit results

| Check | Method | Result |
|---|---|---|
| Bar A — Layer-1 scoped lexical ban | region-scoped case-insensitive scan of the `NEUTRALITY-BAN` region for the ten banned tokens | **PASS — 0 hits** across the region. |
| Bar A2 — Layer-2 Rule-7 carve-out | canonical line count (`grep -cEi`) and occurrence count (`grep -oEi \| wc -l`) of `suggested default` / `one-way` / `two-way` / `decision sheet` in §9 | **PASS — 4 matching lines, 11 occurrences** (≥ 4 required). |
| Bar B — `[r2-QUAL]` tag discipline | literal `trainex-r2` line match outside §0, minus tagged lines | **PASS — 0 untagged.** |
| **Check 4 — snapshot fidelity** (deferred from checkpoint ①) | every `BEGIN/END VERBATIM` block in both bundles re-extracted from the pinned commit and compared byte-for-byte | **PASS — 13 excerpts (10 in `specs/framework-specs-bundle.md` + 3 in `research_package/v2.2-closure-evidence-bundle.md`), 0 mismatches.** |
| **Check 6 — pin consistency across snapshot files** (deferred from checkpoint ①) | the 40-character `source_baseline` must be the only 40-hex string, and identical, in all five round-root files | **PASS —** `6a4f9b9902ab62e1d1f57bba0e521f38120c416d` in `DELIVERY-NOTE.md`, `research_package/RESEARCH-AGENT-PROMPT.md`, `research_package/RESEARCH-CONTEXT-MASTER.md`, `research_package/v2.2-closure-evidence-bundle.md`, and `specs/framework-specs-bundle.md`; no other hash present. |
| Baseline still current | `git diff --stat 6a4f9b99..HEAD` over every cited source path | **PASS — empty.** No cited file changed between the pin and the commissioning commit, so every anchor in this packet remains re-derivable at the pin. |
| Citation resolution | distinct `file:line` citations extracted by `grep -oE '[A-Za-z0-9_./-]+\.(md\|py):[0-9]+' MASTER \| sort -u` and resolved against the live tree | **PASS — 52/52 resolve, 0 out of range.** Eleven cite `pinn_architecture.md` by bare filename, which is why the §3 anchor-resolution rule was added. |
| Attachment cap (Rule 15) | count of uploaded attachments for this sub-package | **PASS — 3 of at most 5.** |
