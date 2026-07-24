---
title: Trainex R2 Claims Register — verified facts vs agent hypotheses
role: durable claims record for the trainex-r2 round; mirrored verbatim as a section of the research-context master (D-03); not uploaded
status: active
created: 2026-07-24
source_baseline: 9b1f0e7a4735df1c54867530cfd1f13b390e1514
---

# Claims Register (trainex-r2)

This register separates **v2.0-verified facts** (`F-` rows, established, may be
relied on) from **unverified agent hypotheses** (`H-` rows — the DIAG-04
candidate-cause rankings and interpretive prose, labeled "agent analysis — not
established fact"). It is a **direct lift** of the inline `[FACT]` / `[HYP]`
tags in `44-DIAGNOSIS.md` (D-09): every row's status traces to a tag or table
row in that snapshot — no claim was re-judged, re-derived, or newly adjudicated
to build this register (RESEARCH anti-pattern avoided).

**How to read.** `F-` rows are established evidence (re-derived from a retained
artifact by a pinned script, or quoted verbatim from a cited file). `H-` rows
are one prior analysis to **challenge** — a candidate-cause attribution or
ranking, not a settled finding. Citations are bare filenames + diagnosis
section numbers (the external agent has no repository access).

## Reconciliation (tag-occurrence → row mapping)

The diagnosis snapshot carries **23 `[FACT]` inline tag occurrences and 7
`[HYP]` inline tag occurrences**. These map to the register as follows.

- **23 `[FACT]` → 16 `F-` rows (F-01..F-16).** Tag occurrences referencing the
  same retained number were merged: the gate-FAIL numbers appear in §1, §2, and
  the GAP-44-01 section and merge into F-01, F-05, and F-15; the distribution
  statistics appear in §1 and §2.1 and merge into F-02 and F-03; the Phase-38
  single-trajectory overfit control appears in §1 and §4 and merges into F-06;
  the provenance statements in §8 merge into F-16.
- **7 `[HYP]` → 8 `H-` rows (H-01..H-08).** The §1 closing-paragraph emergence
  hypothesis → H-01; the §5 rubric statement → H-02; the §6 ranking-interpretation
  tags and the §6 candidate table (5 ranked rows) consolidate into the five
  per-candidate rows H-03..H-07 plus the consolidated tie-rationale H-08.

Every row below traces to a tag or table row in `44-DIAGNOSIS.md`; no new
judgment was introduced.

## FACT table (F- — v2.0-verified, established)

| ID | Claim (numbers verbatim) | Source | Status |
|----|--------------------------|--------|--------|
| F-01 | Sole held-out physics-conservation gate rendered **FAIL**: `eps_H = 237.2086056078468` (> reject threshold `1e-5`); `SCS = 2.3751304405952904` (> reject threshold `-5.0`); 1,500 test trajectories; timestamp `2026-07-22T12:23:13.553360+00:00`. | 44-DIAGNOSIS.md §1, §2; metrics.json; evaluation-receipt.json; 43-VERDICT.md | v2.0-verified |
| F-02 | **Uniform, population-wide failure**: all **1500 / 1500** held-out trajectories exceed `1e-5` individually; best trajectory `min = 0.9741251227996501` (misses by ~5 orders); `n_exceeding_threshold = 1500/1500`, `frac_exceeding_threshold = 1.0` (pre-registered: uniform iff `min > 1e-5`). | 44-DIAGNOSIS.md §1, §2.1; eps_h_distribution.json | v2.0-verified |
| F-03 | ε_H distribution over 1,500 trajectories — min 0.9741, p25 1.2153, p50 (median) 2.2327, p75 5.2177, p90 11.0890, p99 55.0688, max 237.2086, mean 5.6222; heavy right tail (`max/median ≈ 106×`, `p99/median ≈ 24.7×`). | 44-DIAGNOSIS.md §2.1; eps_h_distribution.json | v2.0-verified |
| F-04 | No recorded trajectory attribute separates the population (no ≥10× median gap): variant — hierarchical 970 (median 1.847, max 135.19) vs standard 530 (median 2.854, max 237.21); fidelity — base 759 (median 1.374, max 237.21) vs gold 741 (median 4.572, max 144.32). Worst trajectory: id 1414, standard, base, `eps_H = 237.2086…`. | 44-DIAGNOSIS.md §2.1; eps_h_distribution.json | v2.0-verified |
| F-05 | Preserved artifact carries a per-trajectory `eps_H` array but **no per-trajectory SCS**; the aggregate `SCS` is exactly `log10(max per-trajectory eps_H) = log10(237.2086…) = 2.3751…`, consistent with the headline being the worst-case maximum. | 44-DIAGNOSIS.md §2; metrics.json | v2.0-verified |
| F-06 | The network is not structurally broken: the Phase 38 single-trajectory overfit rung achieved `L0/Lf = 1097.6107…` data-loss reduction (≥ 1e3) on a real admitted trajectory, in **176 steps** (cited, never re-run — SCOPE-23). | 44-DIAGNOSIS.md §1, §4; (Phase 38 verification) | v2.0-verified |
| F-07 | Every run shows a finite warmup **spike** dominated by `loss_phys`, each its own event: smoke (step 194, total 4.61e9, share 0.99999, grad_norm 5.63e13, lr 2.78e-4); seed41 (123, 6.08e9, 0.99999, 6.65e13, 6.39e-4); seed42 (100, 3.73e9, 0.99998, 7.06e13, 7.50e-4); seed43 (169, 3.83e9, 0.99999, 6.24e13, 4.01e-4). | 44-DIAGNOSIS.md §3; loss_decomposition.json | v2.0-verified |
| F-08 | `lambda_phys` first reaches 1.0 at **step 31** in all four runs; `lambda_l == 0.0` at **all 300 steps** in all four runs (the angular-momentum term never contributed gradient signal). | 44-DIAGNOSIS.md §3; loss_decomposition.json; train.log.jsonl | v2.0-verified |
| F-09 | `loss_phys` dominates the cumulative view under **both** raw and λ-weighted aggregation in every run (dominance does not flip). | 44-DIAGNOSIS.md §3; loss_decomposition.json | v2.0-verified |
| F-10 | All four runs finished **300/300 finite** steps (0 non-finite steps); `stage0-smoke` is a separate fourth trace, never pooled. | 44-DIAGNOSIS.md §3; train.log.jsonl | v2.0-verified |
| F-11 | Per-seed validation trend, **first-vs-last** (step-100 → step-300): seed41 improving (2.27e9 → 4.64e8); seed42 improving (8.38e8 → 7.85e7); seed43 worsening (8.97e8 → 1.85e9) → **1 of 3 worsened**. | 44-DIAGNOSIS.md §4; (validation.jsonl) | v2.0-verified |
| F-12 | This **DISAGREES** with 43-CALIBRATION's "2/3 seeds worsened" because the direction definitions differ (43-CAL uses the validation last-window `trend` field step-200 → 300, under which seed41 also worsens → 2/3; this report uses first-vs-last). **Neither definition is adjudicated.** | 44-DIAGNOSIS.md §4; 43-CALIBRATION.md | v2.0-verified |
| F-13 | Final-loss spreads reproduce 43-CALIBRATION's formulas exactly: relative span **3.8224247683129153** (matches the recorded value; `cross_check.matches_within_1e-9_rel: true`). | 44-DIAGNOSIS.md §4; 43-CALIBRATION.md | v2.0-verified |
| F-14 | Held-out splits diverge across seeds: `stage0-smoke` and `stage0-pilot-seed42` share an identical split (byte-identical SHA-256), while seed41 and seed43 each differ; cross-seed validation-*magnitude* comparisons span different held-out populations (only within-seed trend direction is a clean longitudinal signal). | 44-DIAGNOSIS.md §4; (split SHA-256 evidence) | v2.0-verified |
| F-15 | **GAP-44-01 resolution** — the worst-case max IS the gate statistic (owner instruction, option A, 2026-07-23): headline = `max = 237.2086056078468`; the held-out gate fails if ANY trajectory's `eps_H` exceeds `1e-5`. The choice is **verdict-neutral**: because 1500/1500 trajectories exceed `1e-5` individually, the population is FAIL under any aggregate — the resolution fixes the reported headline magnitude and framing, not pass/fail. | 44-DIAGNOSIS.md GAP-44-01; owner instruction 2026-07-23 | owner-instructed (verdict-neutral) |
| F-16 | Provenance: evidence pinned by the manifest (`git_head = 8631576…`, 15 inputs by SHA-256, `cross_check.all_match: true`); pre-shipping re-run: the three analysis scripts re-run, all three diag outputs byte-unchanged vs committed, all 15/15 manifest input hashes still matched (deterministic; `sort_keys`; full-repr floats). | 44-DIAGNOSIS.md §8; (manifest.json) | v2.0-verified |

## HYP table (H- — agent analysis, not established fact)

Every row in this table is **agent analysis — not established fact**. These are
the DIAG-04 candidate-cause rankings and interpretive judgements from
`44-DIAGNOSIS.md`; they are one prior analysis to challenge against evidence,
not settled findings (D-09, D-12).

| ID | Claim | Source | Label |
|----|-------|--------|-------|
| H-01 | The gate failure emerges at **population scale under the Stage-0 budget and recipe**, not from a machine that cannot fit a trajectory. | 44-DIAGNOSIS.md §1 | agent analysis — not established fact |
| H-02 | The evidence-support ranking rubric (Strong / Moderate / Weak) is fixed in the report **before** any candidate is ranked, so the ordering is not post-hoc. | 44-DIAGNOSIS.md §5 | agent analysis — not established fact |
| H-03 | Candidate 1 — **population-scale generalization shortfall** (capacity vs 1,500 diverse trajectories). Support: **Strong** (uniform failure + proven single-trajectory competence; no contradicting evidence). | 44-DIAGNOSIS.md §6 | agent analysis — not established fact |
| H-04 | Candidate 2 — **loss-term imbalance** (`loss_phys` dominates; `lambda_l = 0`). Support: **Moderate** (tied). | 44-DIAGNOSIS.md §6 | agent analysis — not established fact |
| H-05 | Candidate 3 — **optimization / warmup pathology** (finite warmup spikes; `grad_norm ≈ 5–7e13`). Support: **Moderate** (tied). | 44-DIAGNOSIS.md §6 | agent analysis — not established fact |
| H-06 | Candidate 4 — **normalization / data-scale mismatch** in the physics residual (`loss_phys ≈ 1e9` vs `loss_data ≈ 0.1`). Support: **Moderate** (tied). | 44-DIAGNOSIS.md §6 | agent analysis — not established fact |
| H-07 | Candidate 5 — **insufficient Stage-0 training budget** (300 steps). Support: **Weak** (Phase-38 step-count evidence + budget/population confound). | 44-DIAGNOSIS.md §6 | agent analysis — not established fact |
| H-08 | Tie rationale: candidates 2–4 are tied at Moderate (each genuinely — not trivially — contradicted, and DIAG-01..03 do not separate them; ordered alphabetically per the pre-registered tie rule); candidate 1 ranks above the tie (direct, uncontradicted); candidate 5 ranks lowest (the Phase-38 step-count evidence and the budget/population confound materially weaken a pure "need more steps" reading). | 44-DIAGNOSIS.md §6 | agent analysis — not established fact |

## What this register does NOT contain

- **No remedy selection or recommendation** (SCOPE-26). The candidates are
  ranked by evidence support only; deciding among them is owner-adjudicated from
  the returned research in a separately governed step.
- **No new fact/hypothesis judgments.** Every `F-`/`H-` row traces to an inline
  tag or table row in `44-DIAGNOSIS.md`; status was not re-derived.
- **No adjudication of the trend-direction disagreement** (F-12) or the
  max-vs-aggregate statistic beyond the owner's GAP-44-01 instruction (F-15).
