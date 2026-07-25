# 44-DIAGNOSIS — Physics-Gate Forensics (Stage-0 CTL-PINN)

**Phase 44** · Milestone **v2.1** (Physics-Gate Investigation & trainex-r2 Research Package)
**Diagnosed run family:** `runs/stage0-{smoke,pilot-seed41,pilot-seed42,pilot-seed43}` — the
Stage-0 pilot produced under the v2.0 `adjust` verdict.
**Pinned evidence tree:** `git_head = 8631576…` (see `evidence/manifest.json`).
**Status:** Read-only forensics over **retained v2.0 artifacts only**. The evaluator was **not**
invoked (SCOPE-22); no training was run (SCOPE-23); no spec was edited (SCOPE-24); no Stage-1 /
PLAT work (SCOPE-25); **no remedy is selected** (SCOPE-26).

> **Remedy abstinence (read first).** This report *characterizes* how the Stage-0 model fails the
> physics-conservation gate and *ranks candidate causes by the strength of the retained evidence*.
> It does **not** choose, recommend, or pre-judge a remedy. Ranking hypotheses is in scope; deciding
> among them is owner-routed through the trainex-r2 resolution doc in a later milestone (SCOPE-26,
> D-15). Any source-silent physics-adjudication call is surfaced as a STOP-protocol gap, never
> decided inline (see [GAP-44-01](#gap-44-01--the-eps_h-headline-statistic-max-vs-aggregate)).

This report is written for **two audiences at once**: the owner (adjudicating the remedy) and the
external trainex-r2 researchers (who will not have this repo's context). Every claim carries a
citation a stranger can follow.

---

## How to read this report — verified fact vs agent hypothesis

Following the v1.4/v1.5/v1.6 house style (and to make Phase 45's claims register, PKG-11, a direct
lift), every claim is marked inline:

- **[FACT]** — a number or structural observation re-derived from a retained artifact by a
  pinned, re-runnable script, or quoted verbatim from a cited file. These are established.
- **[HYP]** — an interpretive judgement by this report (a candidate-cause attribution, a ranking).
  These are agent analysis, **not** established fact.

The diagnosis' *evidence* is [FACT]; its *ranking* is [HYP].

---

## 1. The failure, in one paragraph

[FACT] The sole held-out physics-conservation gate rendered **FAIL** for `stage0-pilot-seed42`:
`eps_H = 237.2086056078468` against a reject threshold of `1e-5`, and `SCS = 2.3751304405952904`
against a reject threshold of `-5.0` (`runs/stage0-pilot-seed42/evaluation/metrics.json`;
`43-VERDICT.md:27-49`). [FACT] This is **uniform, population-wide failure**: all **1500 / 1500**
held-out trajectories exceed the `1e-5` threshold individually — the *best* trajectory
(`min = 0.9741251227996501`) already misses by roughly five orders of magnitude — and the
distribution carries a heavy right tail (`max/median ≈ 106×`, `p99/median ≈ 24.7×`)
(`evidence/diag01/eps_h_distribution.json`, `overall`, `verdict`, `tail_structure`). [FACT] The
network is not structurally broken: the Phase 38 single-trajectory overfit rung achieved a
`L0/Lf = 1097.6107…` data-loss reduction (≥ 1e3) on a real admitted trajectory
(`evidence/diag03/seed_band.json`, `phase38_overfit_rung_citation`; `38-VERIFICATION.md` Rung 4).
[HYP] The gate failure therefore emerges at **population scale under the Stage-0 budget and recipe**,
not from a machine that cannot fit a trajectory.

## 2. Both gate criteria are addressed

The gate is two-sided (`ctl_instruction.md:567-572`).

| Criterion | Reject rule | Preserved value | Verdict | Source |
|-----------|-------------|-----------------|---------|--------|
| **ε_H** (energy drift) | `eps_H > 1e-5` | per-trajectory; **max = 237.2086…** (the gate headline — GAP-44-01 resolved), mean = 5.6222, median = 2.2327; **1500/1500 exceed** | FAIL | `evidence/diag01/eps_h_distribution.json` |
| **SCS** (= `log10(eps_H)`) | `SCS > -5` | aggregate-only `SCS = 2.3751304405952904` | FAIL | `metrics.json` top-level `scs` |

[FACT] The preserved artifact carries a per-trajectory `eps_H` array but **no per-trajectory SCS**;
this report does not speculate why (D-15). The aggregate `SCS` is exactly `log10(max per-trajectory
eps_H) = log10(237.2086…) = 2.3751…`, consistent with the headline `eps_H` being the worst-case
maximum (confirmed as the gate statistic by the GAP-44-01 resolution, owner option A 2026-07-23).

### 2.1 The ε_H distribution (DIAG-01)

[FACT] Full distribution over 1,500 held-out trajectories
(`evidence/diag01/eps_h_distribution.json`, `overall`):

| min | p25 | p50 (median) | p75 | p90 | p99 | max | mean |
|-----|-----|--------------|-----|-----|-----|-----|------|
| 0.9741 | 1.2153 | 2.2327 | 5.2177 | 11.0890 | 55.0688 | 237.2086 | 5.6222 |

[FACT] Pre-registered verdict (D-05, stated in the script before any number is read as a verdict):
failure is **uniform** iff `min > 1e-5` (strict). `min = 0.9741 > 1e-5` → **uniform failure**;
`n_exceeding_threshold = 1500 / 1500`, `frac_exceeding_threshold = 1.0`.

[FACT] Neither recorded trajectory attribute separates the population (no ≥10× median gap):
`variant` — hierarchical 970 (median 1.847, max 135.19) vs standard 530 (median 2.854, max
237.21); `fidelity` — base 759 (median 1.374, max 237.21) vs gold 741 (median 4.572, max 144.32).
Worst trajectory: `id 1414`, `standard`, `base`, `eps_H = 237.2086…`.

## 3. The training-time loss composition (DIAG-02)

[FACT] Across `stage0-smoke` and pilot seeds 41/42/43, every run shows a finite warmup **spike**
dominated by `loss_phys`, and each spike is its own event (not one shared figure)
(`evidence/diag02/loss_decomposition.json`, per-run `warmup_spike`):

| run | spike step | total | dominant term | term share | grad_norm | lr |
|-----|-----------|-------|---------------|-----------|-----------|----|
| smoke | 194 | 4.61e9 | loss_phys | 0.99999 | 5.63e13 | 2.78e-4 |
| seed41 | 123 | 6.08e9 | loss_phys | 0.99999 | 6.65e13 | 6.39e-4 |
| seed42 | 100 | 3.73e9 | loss_phys | 0.99998 | 7.06e13 | 7.50e-4 |
| seed43 | 169 | 3.83e9 | loss_phys | 0.99999 | 6.24e13 | 4.01e-4 |

[FACT] PHYS-05 interaction: `lambda_phys` first reaches 1.0 at **step 31** in all four runs, and
`lambda_l == 0.0` at **all 300 steps** in all four runs (asserted) — the angular-momentum term never
contributed gradient signal. [FACT] `loss_phys` dominates the cumulative view under **both** raw and
λ-weighted aggregation in every run (dominance does not flip). [FACT] All four runs finished
**300/300 finite** steps (0 non-finite steps). `stage0-smoke` is reported as a separate fourth trace
and is never pooled (D-10).

## 4. The seed band (DIAG-03)

[FACT] Per-seed validation trend, **first-vs-last** (D-11; step-100 → step-300 `final_val_loss`):
seed41 **improving** (2.27e9 → 4.64e8), seed42 **improving** (8.38e8 → 7.85e7), seed43
**worsening** (8.97e8 → 1.85e9) → **1 of 3 worsened**. (`stage0-smoke` worsening, separate trace.)
[FACT] This **DISAGREES** with 43-CALIBRATION's "2/3 seeds worsened", explicitly because the
direction definitions differ: 43-CAL uses the validation.jsonl last-window `trend` field
(step-200 → 300), under which seed41 also worsens (→ 2/3); this report uses first-vs-last. Neither
definition is adjudicated (`evidence/diag03/seed_band.json`, `calibration_agreement`).

[FACT] Final-loss spreads reproduce 43-CALIBRATION's formulas exactly: relative span
**3.8224247683129153** (matches the recorded value; `cross_check.matches_within_1e-9_rel: true`).
[FACT] **Held-out splits diverge across seeds**: `stage0-smoke` and `stage0-pilot-seed42` share an
identical split (byte-identical SHA-256), while seed41 and seed43 each differ. Cross-seed
validation-*magnitude* comparisons therefore span **different held-out populations**; only
within-seed trend direction is a clean longitudinal signal. [FACT] Phase 38 machinery-integrity
control (cited, never re-run, SCOPE-23): single-trajectory overfit `ratio = 1097.6107…` ≥ 1e3, PASS,
176 steps, on the `zeros(13)` Phase-38 placeholder IC13.

---

## 5. Pre-registered ranking rubric (stated BEFORE the table)

[HYP] The rubric below is fixed in this report before any candidate is ranked, so the ordering is
not post-hoc (same discipline as DIAG-01's D-05 criterion).

- **Dimension — *evidence support*:** the degree to which the DIAG-01..03 [FACT] outputs directly
  support a candidate as a *contributor* to the gate failure. (This is **not** a "most likely remedy"
  ranking — remedy selection is out of scope, SCOPE-26.)
- **Levels:**
  - **Strong** — direct supporting evidence in DIAG-01..03, with no directly-contradicting evidence.
  - **Moderate** — real supporting evidence, but partially contradicted or indirect.
  - **Weak** — little direct support, or notably contradicted by the evidence.
- **Tie-handling:** tied rows are **declared explicitly** in the table and ordered alphabetically by
  candidate name; no silent ordering.

## 6. Ranked candidate causes

| # | Candidate cause | Support | Supporting evidence (DIAG-01..03 [FACT]) | Contradicting evidence (or explicit none) | Discriminating test (**proposed only**, never executed — SCOPE-23) |
|---|-----------------|---------|------------------------------------------|-------------------------------------------|--------------------------------------------------------------------|
| 1 | Population-scale generalization shortfall (capacity vs 1,500 diverse trajectories) | **Strong** | Uniform failure: 1500/1500 exceed `1e-5`, `min = 0.9741` (DIAG-01); yet the network fits one trajectory, Phase 38 `ratio = 1097.6` (DIAG-03 citation) | No contradicting evidence identified in DIAG-01..03 outputs | Train/evaluate a higher-capacity variant on the same population (proposed for owner authorization) |
| 2 (tie) | Loss-term imbalance (`loss_phys` dominates; `lambda_l = 0`) | **Moderate** | `loss_phys` carries ≈99.998–99.999% of every warmup spike and dominates cumulative raw + weighted; angular-momentum weight is 0.0 at all 300 steps (DIAG-02) | Dominance alone does not establish the weighting is *wrong* — a dominant physics residual may be intended; the loss catalog is spec-locked (SCOPE-24) | A λ-weighting / loss-balancing ablation on the population (proposed for owner authorization) |
| 3 (tie) | Optimization / warmup pathology | **Moderate** | Finite warmup spikes of 3.7e9–6.1e9 in `loss_phys` with `grad_norm ≈ 5–7e13`; seed42 spikes at peak `lr = 7.5e-4` (DIAG-02) | All runs finished 300/300 finite steps (0 non-finite); the network reaches a data-loss floor on one trajectory (Phase 38) — pathology is not catastrophic | A warmup / LR-schedule ablation recording per-step `grad_norm`/`finite` (proposed for owner authorization) |
| 4 (tie) | Normalization / data-scale mismatch in the physics residual | **Moderate** | `loss_phys ≈ 1e9` vs `loss_data ≈ 0.1` — roughly ten orders of magnitude separating the physics-residual scale from the data term (DIAG-02 per-step raw terms) | The architecture carries LayerNorm (ARCH-02) and the IC/vector are dataset-normalized; a scale gap is not by itself a correctness failure | A physics-residual normalization-scale ablation (proposed for owner authorization) |
| 5 | Insufficient Stage-0 training budget (300 steps) | **Weak** | Only 300 steps per run; validation trends are still moving (DIAG-03) | Phase 38 reached a single-trajectory floor in **176** steps; budget and population-scale are confounded and cannot be separated by DIAG-01..03 alone | A longer-budget population run (proposed for owner authorization) |

[HYP] Candidates 2–4 are declared a tie at **Moderate**: each has real supporting evidence that is
genuinely (not trivially) contradicted, and DIAG-01..03 do not by themselves separate them. They are
ordered alphabetically (`loss-term imbalance`, `optimization/warmup`, `normalization/data-scale`)
per the pre-registered tie rule. [HYP] Candidate 1 ranks above the tie because its supporting
evidence (uniform failure + proven single-trajectory competence) is direct and uncontradicted.
[HYP] Candidate 5 ranks lowest because the Phase 38 step-count evidence and the budget/population
confound materially weaken a pure "need more steps" reading.

> Every discriminating test above is a **proposal for owner authorization only**. None is executed
> in this phase (SCOPE-23). They are recorded so the trainex-r2 package can pose them as research
> questions (D-14).

---

## GAP-44-01 — the ε_H headline statistic (max vs aggregate)

[FACT] The preserved `metrics.json` reports top-level `eps_h = 237.2086056078468`, which is
**exactly** `max(per_trajectory.eps_h)` (verified by exact float equality in DIAG-01); the mean is
`5.6221870977458295` and the median `2.232675867436938`. [FACT] The locked spec defines
**per-trajectory** `eps_H = max_t |(H(t)-H(0))/H(0)|` and the per-trajectory reject rule
`eps_H > 1e-5` (`ctl_instruction.md:567-572`), and 43-VERDICT cites `eps_H = 237.21` as the gate
number — but no consulted source explicitly defines the **aggregate held-out headline statistic**
(max vs mean vs median vs fraction-failing) over the 1,500 trajectories.

This was recorded as **GAP-44-01** (`.planning/phases/44-physics-gate-forensics/44-GAPS.md`;
index `.planning/milestones/v2.1-GAPS.md`) and is now **RESOLVED-WITH-INSTRUCTION** (owner
instruction 2026-07-23, option A): **the worst-case max IS the gate statistic.** The held-out gate
fails if ANY trajectory's `eps_H` exceeds `1e-5`, and the headline is
`max = 237.2086056078468` — confirming the evaluator's rendering, consistent with the
per-trajectory reject rule applied set-wide and with the preserved aggregate `SCS = log10(max)`.
The mean (5.62) and median (2.23) remain quoted as distribution facts, not gate numbers. [FACT]
The choice is **verdict-neutral**: because 1500/1500 trajectories exceed `1e-5` individually, the
population is FAIL under any aggregate — the resolution fixes the reported headline magnitude and
the research framing, not pass/fail.

---

## 7. What this diagnosis does NOT do

- **Selects no remedy** (SCOPE-26, D-15). It ranks hypotheses; the remedy is owner-adjudicated from
  the trainex-r2 resolution doc in a later milestone.
- **Runs no evaluator** (SCOPE-22 — the budget is exhausted; `43-VERDICT.md` records the audited
  attempts).
- **Runs no training** and **proposes no executed diagnostic run** (SCOPE-23; discriminating tests
  are proposals for owner authorization only).
- **Edits no framework spec** (SCOPE-24). A diagnosis implicating a spec parameter becomes an ERW
  research question, never an edit.
- **Decides no source-silent adjudication call.** The max-vs-mean gate statistic was surfaced as
  GAP-44-01 and resolved by owner instruction (2026-07-23: worst-case max), not decided inline;
  the trend-direction disagreement with 43-CALIBRATION is reported, not adjudicated.

## 8. Provenance and reproduction

Every number above traces to a retained script output or a cited file. The evidence is pinned by
`evidence/manifest.json` (`git_head = 8631576…`, `git_head_available: true`, 15 inputs by SHA-256,
`cross_check.all_match: true`), assembled from each diag output's embedded provenance.

**Pre-shipping re-run (D-02):** immediately before this report was committed, the three analysis
scripts were re-run; all three diag outputs were **byte-unchanged** versus the committed versions,
and all **15/15** manifest input hashes still matched the live tree. The diag outputs are
deterministic functions of their pinned inputs (no timestamps; `sort_keys`; full-repr floats).

**Reproduce** (pinned interpreter — never bare `python3`; the repo `.venv`/system Pythons lack
`torch`/`numpy`):
```sh
cd <repo>/.planning/phases/44-physics-gate-forensics/evidence
~/miniforge3/envs/pinn-train/bin/python3 diag01/eps_h_distribution.py
~/miniforge3/envs/pinn-train/bin/python3 diag02/loss_decomposition.py
~/miniforge3/envs/pinn-train/bin/python3 diag03/seed_band.py
~/miniforge3/envs/pinn-train/bin/python3 build_manifest.py
```
Inputs are read-only from `runs/`, `.planning/milestones/v2.0-*`, and the framework specs; nothing
under those paths is written. See `evidence/README.md` for the full reproduction boundary and the
self-check assertions that gate each output.

---

*Phase 44 — Physics-Gate Forensics. Read-only diagnosis; remedy deliberately left open. This report
is Phase 45's trainex-r2 centerpiece (its structure should survive being snapshotted and
commit-pinned into the trainex-r2 package, PKG-09).*
