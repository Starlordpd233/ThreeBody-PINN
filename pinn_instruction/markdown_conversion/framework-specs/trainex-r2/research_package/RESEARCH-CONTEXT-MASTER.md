---
title: Trainex R2 Research Context Master — Stage-0 Physics-Gate Training-Recipe Questions
package_for: trainex-r2 (single sub-package)
role: the external research agent's single entry point — orientation, manifest, source tiering, five neutrally framed questions, claims register, provenance, and the neutral output contract
status: active
created: 2026-07-24
source_baseline: 9b1f0e7a4735df1c54867530cfd1f13b390e1514
self_contained: true
---

# Trainex R2 Research Context Master

This is **upload attachment 1 of 4**. It is your single entry point: read it
first, then the three other attached files it names. **You are working from the
attached files only.** Any file referenced inside an attachment but not itself
attached is unavailable to you — do not guess at its content; if its absence
matters to an answer, record that as a gap (see the Output Contract, §7).

## 1. Orientation

**What happened.** A curriculum-trained Physics-Informed Neural Network (a
"CTL-PINN") for the three-body problem was trained on a Stage-0 (easiest,
highly-stable) slice of an admitted dataset under a fixed curriculum recipe.
After training, its sole held-out physics-conservation gate rendered **FAIL**:
on **all 1,500** held-out trajectories, the worst-case relative Hamiltonian
drift `eps_H` exceeded the reject threshold `1e-5` (the best trajectory still
missed by about five orders of magnitude). The project owner signed an
"adjust" verdict — keep the demonstrated Stage-0 mechanical slice, but block
full-platform expansion and route a separately governed investigation of the
failed gate. A forensic diagnosis was produced and is attached
(`44-DIAGNOSIS.md`); it characterizes the failure and ranks candidate causes by
the strength of the retained evidence.

**What this package asks.** Five training-recipe research questions (§4):
training budget/steps, warmup + learning-rate schedule, loss weighting /
balancing (with a normalization / data-scale sub-facet), Stage-0 curriculum
pacing, and the evaluation-policy question.

**What you are NOT asked to do.** You are **not** asked to choose or recommend
the remedy. Remedy adjudication is the project owner's decision, made in a
separately governed step from the research you and other agents return. Your
job is to answer the five questions with reasoning and cited evidence, frame
the trade-offs between plausible positions, and record where the attached
materials are silent — not to pick a fix. You are also not asked to run any
evaluation or training; the questions are about recipe design and governance
given the evidence already in hand.

## 2. Manifest (the four attached files)

| # | Bare filename | Role | Treatment |
|---|---------------|------|-----------|
| 1 | `RESEARCH-CONTEXT-MASTER.md` | This document — your entry point. | Read first. |
| 2 | `44-DIAGNOSIS.md` | The forensics centerpiece: a verbatim snapshot of the hypothesis-ranked, `[FACT]`/`[HYP]`-tagged diagnosis. | `[FACT]`-tagged content is established; `[HYP]`-tagged content is agent analysis to challenge. Internal references it makes to files you do not have are unavailable (per §1). |
| 3 | `framework-specs-bundle.md` | Excerpts of the locked framework specs: the two-sided gate definition, Stage-0 curriculum recipe, the five-term loss catalog, the PHYS-05 warmup schedule, and the input/output + COM-projection contract. | **Authoritative locked spec — hard constraint.** Not open to challenge; treat as ground truth. |
| 4 | `run-evidence-bundle.md` | The retained run evidence: the held-out gate receipt/headline metrics, the three-seed calibration, the owner-signed verdict (with the exhausted-evaluator-budget record), and the training-time loss-composition excerpts. | Authoritative record of what the retained v2.0 artifacts show. |

## 3. Source tiering (how to treat each kind of content)

- **Hard constraint (rely on as ground truth):** the locked spec excerpts
  (`framework-specs-bundle.md`); every `[FACT]` / `F-` row in the claims
  register (§5); the owner decisions, including the gate-statistic instruction
  (F-15); and the no-remedy posture stated in §1.
- **Agent analysis — challengeable:** the DIAG-04 candidate-cause rankings and
  interpretive prose — every `[HYP]` / `H-` row in the claims register (§5).
  Treat these as **hypotheses to test against the evidence**, not as settled
  findings. A ranking of "Strong / Moderate / Weak" is one prior analysis; it is
  not a conclusion you must defend or assume.

This round has **no** brainstorm-baseline tier; the inputs are locked facts and
one diagnosis. Do not over-weight the headline failure magnitude: the
gate-statistic choice (F-15) is verdict-neutral, because the population fails
under any aggregate statistic.

## 4. The five research questions

Each question is posed **neutrally** — no recommended answer, no preferred
value, schedule, direction, or candidate. Each block gives: the facts that bear
on it (cited to `F-` rows and attached files) → the relevant spec position →
the matching DIAG-04 candidate as `[HYP]` context only → a **proposed**
research direction (requiring separate project-owner authorization; never
performed here) → what a complete answer specifies (the **structure** of an
adequate answer, never a value) → the question itself.

### Q1 — Training budget / steps

- **Facts:** all four runs finished **300/300 finite** steps (F-10); per-seed
  validation trends were **still moving** at step 300 — 1 of 3 seeds worsening
  first-vs-last (F-11); yet the Phase 38 single-trajectory overfit control
  reached its data-loss floor in **176 steps** (F-06).
- **Spec position:** the Stage-0 budget is a recipe parameter, not a locked
  invariant (see `framework-specs-bundle.md`, Excerpts 2–3).
- **`[HYP]` context (agent analysis — not established fact):** DIAG-04
  candidate 5 — "insufficient Stage-0 training budget" — ranked **Weak** (H-07),
  and **explicitly confounded** with candidate 1 (population-scale
  generalization shortfall, H-03): budget and population-scale cannot be
  separated by the retained evidence alone.
- **Proposed research direction (owner-authorization-gated; not performed
  here):** a longer-budget population run, designed to **deconfound** budget
  from population scale.
- **What a complete answer specifies:** a reasoned budget rule that addresses
  the budget/population-scale confound — i.e., the evidence and the
  deconfounding design that would establish whether 300 steps is simply too few
  for this population, distinct from a capacity shortfall. (Structure only; do
  not state a step count.)
- **The question:** *Given that validation was still moving at 300 steps yet a
  single trajectory reached a floor in 176, what is the principled way to
  decide whether and how much more budget the Stage-0 population run should
  receive — and what evidence would separate a pure budget shortfall from the
  population-scale generalization shortfall?*

### Q2 — Warmup + learning-rate schedule

- **Facts:** every run showed a finite warmup **spike** of 3.7e9–6.1e9
  dominated by `loss_phys`, with `grad_norm ≈ 5–7e13`; seed42 spiked at peak
  `lr = 7.5e-4` (F-07); all runs finished finite (F-10).
- **Spec position:** the PHYS-05 warmup schedule and the causal weighting
  (`eta_c = 1`) — see `framework-specs-bundle.md`, Excerpt 5 and §3.2.
- **`[HYP]` context:** DIAG-04 candidate 3 — "optimization / warmup pathology" —
  ranked **Moderate** (H-05); partially contradicted because all runs finished
  finite and the network reaches a data-loss floor on one trajectory (F-06), so
  any pathology is not catastrophic.
- **Proposed research direction (owner-authorization-gated; not performed
  here):** a warmup / LR-schedule ablation recording per-step `grad_norm` and
  finiteness.
- **What a complete answer specifies:** a warmup/LR-schedule design with stated
  rationale and the per-step diagnostics that would confirm or refute an
  optimization-pathology contribution to the gate failure. (Structure only; do
  not state a schedule.)
- **The question:** *How should warmup and the learning-rate schedule be
  designed for this Stage-0 population, and what per-step evidence would
  distinguish a benign finite warmup transient from a pathology that contributes
  to the physics-gate failure?*

### Q3 — Loss weighting / balancing (includes the normalization / data-scale sub-facet)

- **Facts:** `loss_phys` carries ≈99.998–99.999% of every warmup spike and
  dominates the cumulative view under **both** raw and λ-weighted aggregation
  (F-07, F-09); `lambda_l == 0.0` at all 300 steps in all four runs (F-08);
  under the locked PHYS-05 schedule, Stage 0 (`k ∈ {0,1}`) sets both
  conservation weights `lambda_E^max = lambda_L^max = 0` (Excerpt 5), so the
  angular-momentum and energy terms contribute no gradient signal during
  Stage 0 by design.
- **Normalization / data-scale sub-facet (candidate 4, kept inside this
  question):** there is roughly a **ten-order** separation between
  `loss_phys ≈ 1e9` and `loss_data ≈ 0.1` (F-07; H-06), to be read against the
  `tanh` input normalization, the hard mass-weighted COM projection head, and
  the absence of a separate linear-momentum term (Excerpt 6).
- **Spec position:** the five-term loss catalog and total assembly
  (`framework-specs-bundle.md`, Excerpt 4) and the PHYS-05 schedule (Excerpt 5).
- **`[HYP]` context:** DIAG-04 candidate 2 — "loss-term imbalance" — ranked
  **Moderate** (H-04); and candidate 4 — "normalization / data-scale mismatch"
  — ranked **Moderate** (H-06). Both are challengeable: a dominant physics
  residual may be intended, the loss catalog is spec-locked, and a scale gap is
  not by itself a correctness failure.
- **Proposed research direction (owner-authorization-gated; not performed
  here):** a λ-weighting / loss-balancing ablation, and separately a
  physics-residual normalization-scale ablation, on the population.
- **What a complete answer specifies:** a loss-weighting / balancing approach
  (and a stance on the normalization / data-scale sub-facet) with the rationale
  and the weighted-loss / gradient evidence that would justify it — including
  how it engages the locked PHYS-05 Stage-0 zeroing of the conservation
  weights. (Structure only; do not state weights or a schedule.)
- **The question:** *How should the loss terms be weighted/balanced for the
  Stage-0 population — including how to treat the ≈10-order scale separation
  between the physics and data terms and the Stage-0 zeroing of the
  conservation weights — and what evidence distinguishes intended dominance
  from a weighting that contributes to the gate failure?*

### Q4 — Stage-0 curriculum pacing

- **Facts:** `lambda_phys` reaches 1.0 at **step 31** in all four runs (F-08);
  the recipe is Stage-0-only under a cumulative-replay curriculum
  (`framework-specs-bundle.md`, Excerpts 2–3).
- **Spec position:** the Stage-0 definition and Stage 0/1 criteria, cumulative
  replay, and the PHYS-05 stage-boundary re-warmup rule (Excerpts 2, 3, 5).
- **`[HYP]` context:** no single DIAG-04 candidate is mapped to this question;
  it cross-cuts candidates 2–5 (the recipe context in which they all sit).
- **Proposed research direction (owner-authorization-gated; not performed
  here):** a curriculum-pacing / stage-progression study within a fixed budget.
- **What a complete answer specifies:** how stage / `front_idx` progression and
  the PHYS-05 scheduled-weight ramps should interact **within the 300-step
  budget**, and the diagnostics that would show whether the pacing helps or
  hurts gate compliance. (Structure only; do not state a pacing scheme.)
- **The question:** *Within the Stage-0 budget, how should curriculum stage
  progression and the PHYS-05 weight ramps be paced relative to each other, and
  what evidence bears on whether the current pacing is appropriate for gate
  compliance?*

### Q5 — Evaluation policy (governance / evidence-design ONLY)

- **Facts:** the held-out evaluator budget is **exhausted** — two failed
  attempts plus one completed FAIL, all audited, and the final invocation must
  not be retried under current owner policy (see `run-evidence-bundle.md`,
  Group 3, the evaluator-invocation audit; F-01).
- **`[HYP]` context:** none mapped; this is a governance question.
- **This is NOT a request to run any evaluation now.** It asks what a
  **future** evaluation would require.
- **What a complete answer specifies:** the evidence, the held-out-data
  governance (a new, explicitly changed owner policy and a separately governed
  evidence boundary), and the acceptance structure a future held-out evaluation
  would need — given the budget is exhausted and the population fails under any
  aggregate statistic (F-02, F-15). (Structure only; do not propose running an
  evaluation, and do not set numeric acceptance bands beyond what the locked
  spec already states.)
- **The question:** *If a future held-out evaluation were ever authorized, what
  evidence, governance, and acceptance structure would it require given that
  the current evaluator budget is exhausted and the population fails the gate
  under any aggregate statistic?*

## 5. Claims register (folded in verbatim from CLAIMS-REGISTER.md)

`F-` rows are established evidence you may rely on. `H-` rows are one prior
analysis to **challenge**. Every `H-` row is **agent analysis — not established
fact**. (This is the same content as the standalone register; row counts match
exactly: 16 `F-` rows, 8 `H-` rows.)

### FACT table (F- — v2.0-verified, established)

| ID | Claim (numbers verbatim) | Source | Status |
|----|--------------------------|--------|--------|
| F-01 | Sole held-out physics-conservation gate rendered **FAIL**: `eps_H = 237.2086056078468` (> `1e-5`); `SCS = 2.3751304405952904` (>`-5.0`); 1,500 test trajectories. | 44-DIAGNOSIS.md §1, §2; metrics.json; 43-VERDICT.md | v2.0-verified |
| F-02 | **Uniform failure**: all **1500 / 1500** trajectories exceed `1e-5`; `min = 0.9741251227996501`; `frac_exceeding = 1.0`. | 44-DIAGNOSIS.md §1, §2.1; eps_h_distribution.json | v2.0-verified |
| F-03 | ε_H distribution — min 0.9741, p50 2.2327, p99 55.0688, max 237.2086, mean 5.6222; `max/median ≈ 106×`, `p99/median ≈ 24.7×`. | 44-DIAGNOSIS.md §2.1; eps_h_distribution.json | v2.0-verified |
| F-04 | No trajectory attribute separates the population (no ≥10× median gap); variant/fidelity subpopulation stats as recorded. | 44-DIAGNOSIS.md §2.1; eps_h_distribution.json | v2.0-verified |
| F-05 | No per-trajectory SCS recorded; aggregate `SCS = log10(max eps_H) = 2.3751…`. | 44-DIAGNOSIS.md §2; metrics.json | v2.0-verified |
| F-06 | Network not structurally broken: Phase 38 single-trajectory overfit `L0/Lf = 1097.6107…` (≥1e3) in 176 steps (cited, never re-run). | 44-DIAGNOSIS.md §1, §4 | v2.0-verified |
| F-07 | Per-run warmup spike dominated by `loss_phys` (3.7e9–6.1e9; `grad_norm ≈ 5–7e13`; seed42 at `lr = 7.5e-4`). | 44-DIAGNOSIS.md §3; loss_decomposition.json | v2.0-verified |
| F-08 | `lambda_phys = 1.0` from step 31; `lambda_l = 0.0` at all 300 steps, all four runs. | 44-DIAGNOSIS.md §3; loss_decomposition.json; train.log.jsonl | v2.0-verified |
| F-09 | `loss_phys` dominates cumulative raw **and** λ-weighted aggregation in every run (no flip). | 44-DIAGNOSIS.md §3; loss_decomposition.json | v2.0-verified |
| F-10 | All four runs finished 300/300 finite steps; `stage0-smoke` separate, never pooled. | 44-DIAGNOSIS.md §3; train.log.jsonl | v2.0-verified |
| F-11 | Per-seed validation trend first-vs-last: seed41 improving, seed42 improving, seed43 worsening → 1 of 3 worsened. | 44-DIAGNOSIS.md §4 | v2.0-verified |
| F-12 | DISAGREES with 43-CALIBRATION's "2/3 worsened" (different direction definition); neither adjudicated. | 44-DIAGNOSIS.md §4; 43-CALIBRATION.md | v2.0-verified |
| F-13 | Final-loss spreads reproduce 43-CALIBRATION exactly: relative span `3.8224247683129153` (within 1e-9). | 44-DIAGNOSIS.md §4; 43-CALIBRATION.md | v2.0-verified |
| F-14 | Held-out splits diverge across seeds (seed42 shares smoke's split by SHA-256; seed41/43 differ). | 44-DIAGNOSIS.md §4 | v2.0-verified |
| F-15 | **GAP-44-01 resolution** — worst-case max IS the gate statistic (owner, option A, 2026-07-23); **verdict-neutral** (1500/1500 fail under any aggregate). | 44-DIAGNOSIS.md GAP-44-01 | owner-instructed (verdict-neutral) |
| F-16 | Provenance: evidence pinned (`git_head = 8631576…`, 15 SHA-256 inputs, `all_match: true`); pre-shipping re-run byte-unchanged. | 44-DIAGNOSIS.md §8 | v2.0-verified |

### HYP table (H- — agent analysis, not established fact)

Every row below is **agent analysis — not established fact**.

| ID | Claim | Source | Label |
|----|-------|--------|-------|
| H-01 | Failure emerges at population scale under the Stage-0 budget/recipe, not from a machine that cannot fit a trajectory. | 44-DIAGNOSIS.md §1 | agent analysis — not established fact |
| H-02 | The evidence-support rubric is fixed before ranking (not post-hoc). | 44-DIAGNOSIS.md §5 | agent analysis — not established fact |
| H-03 | Candidate 1 — population-scale generalization shortfall. Support: **Strong**. | 44-DIAGNOSIS.md §6 | agent analysis — not established fact |
| H-04 | Candidate 2 — loss-term imbalance. Support: **Moderate** (tied). | 44-DIAGNOSIS.md §6 | agent analysis — not established fact |
| H-05 | Candidate 3 — optimization/warmup pathology. Support: **Moderate** (tied). | 44-DIAGNOSIS.md §6 | agent analysis — not established fact |
| H-06 | Candidate 4 — normalization/data-scale mismatch. Support: **Moderate** (tied). | 44-DIAGNOSIS.md §6 | agent analysis — not established fact |
| H-07 | Candidate 5 — insufficient Stage-0 budget. Support: **Weak**. | 44-DIAGNOSIS.md §6 | agent analysis — not established fact |
| H-08 | Tie rationale: candidates 2–4 tied at Moderate; candidate 1 above; candidate 5 lowest. | 44-DIAGNOSIS.md §6 | agent analysis — not established fact |

## 6. Provenance

- **Package baseline (`source_baseline`):** `9b1f0e7a4735df1c54867530cfd1f13b390e1514`
  — the repository commit at package assembly. Every snapshot source (the
  diagnosis, the run evidence, the locked specs) is committed at this baseline.
- **Complementary diagnosis evidence pin:** the attached `44-DIAGNOSIS.md`
  carries its own deeper evidence pin in its §8 — its 15 analysis inputs are
  pinned by SHA-256 at commit `8631576dc5d8f76d1d0b301895ec5014161941cc`
  (`cross_check.all_match: true`). The two pins are complementary (package
  baseline vs diagnosis evidence tree); neither supersedes the other.

## 7. Output contract

Produce one research report, structured as **per-question sections (Q1–Q5) plus
a dedicated gaps section**. The project will later consolidate individual agents'
reports into one resolution document; write yours to stand alone.

1. **Answer each of the five questions** with reasoning, citing evidence to the
   attached files by **bare filename and section** (e.g., "44-DIAGNOSIS.md §3",
   "framework-specs-bundle.md Excerpt 5", "F-07").
2. **Frame the trade-offs** between plausible positions; do not assume a house
   preference.
3. **Do not recommend a remedy.** Remedy adjudication is owner-governed
   downstream. Your answers inform that decision; they do not make it.
4. **Where the attached materials are silent or ambiguous, record it in the
   gaps section — never invent.** (A gap is a legitimate, valued output.)
5. **List which `F-` / `H-` claims** each answer relied on, and flag any place
   you treat an `H-` row as if it were established (you should not, but say so
   if you do).
6. Keep every DIAG-04 candidate mention labeled as agent analysis, and every
   discriminating-test mention as a proposal requiring separate owner
   authorization — not as work performed or promised.

*This master carries no repository paths. Companion files are referenced by bare
filename only; you have no codebase access.*
