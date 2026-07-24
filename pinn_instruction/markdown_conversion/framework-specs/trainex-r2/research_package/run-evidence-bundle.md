---
title: Trainex R2 Run-Evidence Bundle — held-out gate, calibration, verdict, loss composition
role: excerpted run evidence — the authoritative record of what the retained v2.0 evaluation and training artifacts show (read-only facts; no re-analysis)
status: active
created: 2026-07-24
source_baseline: 9b1f0e7a4735df1c54867530cfd1f13b390e1514
self_contained: true
---

# Run-Evidence Bundle (trainex-r2)

This bundle is **upload attachment 4 of at most 5** for the trainex-r2 research
round. It carries the retained v2.0 run evidence the five research questions
stand on: the sole held-out gate rendering, the three-seed calibration, the
owner-signed verdict (with the audited exhausted-evaluator budget), and the
training-time loss-composition excerpts.

**These are verified facts ([FACT] in the house style), read-only.** Nothing
here is re-evaluated, re-ranked, or re-interpreted (SCOPE-22/23/26): the
evaluator is never invoked, no training is run, no remedy is chosen.

**Self-containment / path-abbreviation convention.** The retained artifacts
record internal run directory paths and absolute machine paths. Those are
abbreviated to a **bare name in square brackets** (e.g. the run directory
appears as `[stage0-pilot-seed42]`) so this bundle carries no repository path.
Numbers, SHA-256 identities, timestamps, verdicts, and normative conclusions
are reproduced **unmodified**.

---

## Group 1 — The held-out evaluation rendering (sole gate result)

### Evaluation receipt

Source: evaluation-receipt.json (near-full; paths abbreviated)

```json
{
  "checkpoint_path": "[stage0-pilot-seed42 checkpoints best.pt]",
  "checkpoint_sha256": "6c6f4ae0ebbf6dd56a792503fb32428038bb8dc0f9dc235507a11eff7f9edeaa",
  "config_sha256": "ac15f434681d2244fda9a0bcdc8b33416ed1c8737b682f695782501862fb86ad",
  "eps_h": 237.2086056078468,
  "run_dir": "[stage0-pilot-seed42]",
  "schema_version": "phase43-evaluation-receipt/v1",
  "scs": 2.3751304405952904,
  "splits_sha256": "5846ae5b55104e55a85d644875c3da187200c3d521f52a9298876d656c6d8903",
  "timestamp": "2026-07-22T12:23:13.553360+00:00",
  "verdict": "FAIL"
}
```

### Human-readable metrics summary

Source: metrics.md (near-full; header path abbreviated)

> # Phase 43 Evaluation Metrics
> Run: `[stage0-pilot-seed42]`
> Checkpoint: `[best.pt]`
> Held-out test trajectories: 1500
> Generated: 2026-07-22T12:23:13.553360+00:00
>
> ## Gate Check
> - ε_H: 2.372086e+02 (reject if > 1e-5) → ❌
> - SCS: 2.375130e+00 (reject if > -5) → ❌
> **OVERALL: FAIL**
>
> ε_H (epsilon_H) is the worst-case relative Hamiltonian drift across the
> held-out test trajectories: `max_t |(H(t) - H(0)) / H(0)|`, computed on
> detached CPU float64 tensors with the Plummer softening `eps_inv = 1e-10`
> (distinct from the training-time softening). A smaller value means the
> model's predicted trajectory conserves energy more closely to that
> trajectory's own initial energy.
>
> SCS (Scaled Conservation Score) is `log10(ε_H)`; a smaller (more negative)
> SCS is better. The gate REJECTS if `ε_H > 1e-5` (equivalently `SCS > -5`);
> the boundary itself PASSES (strict-inequality reject).

### Headline metrics (large file — headline fields only)

Source: metrics.json (the per-trajectory array of 1,500 entries is NOT excerpted; only the top-level headline fields)

- `eps_h`: **237.2086056078468**
- `eps_h_reject_threshold`: **1e-05**
- `scs`: **2.3751304405952904**
- `scs_reject_threshold`: **-5.0**
- `n_test_trajectories`: **1500**
- `verdict`: **FAIL**
- `schema_version`: `phase43-evaluate-metrics/v1`

The full per-trajectory ε_H distribution statistics (min 0.9741, median 2.2327,
mean 5.6222, max 237.2086, p99 55.07; 1500/1500 exceed 1e-5; `max/median ≈
106×`, `p99/median ≈ 24.7×`) are carried by the attached diagnosis §2.1
(`44-DIAGNOSIS.md`).

---

## Group 2 — Three-seed Stage-0 calibration

Source: 43-CALIBRATION.md (near-full; run paths abbreviated, R-1/R-2 candidate
option tables trimmed as administrative boilerplate — the ratified values are
retained in the ratification record)

> **Status:** OWNER-RATIFIED. Pilot date: 2026-07-22.
>
> ## Pilot contract
> Three ordinary real-data runs used the Phase 41 smoke configuration with only
> the seed and unique run name changed. Each run used the admitted dataset,
> MPS/float32, 300 Adam steps, the owner-ratified D4-a wall-clock checkpoint
> ceiling of `120.0` seconds, and the values present before this calibration:
> - `run.guards.loss_explosion_ceiling = 100000000000.0`
> - `run.guards.disk_floor_fraction = 0.05`
> - `run.guards.memory_watermark_fraction = 0.7`
> - `run.recover_retries = 0`
>
> ## Raw observations
> | Seed | Run | Terminal disposition | Steps finite | Final total loss | Peak total loss | Final validation | Trend | Wall clock | Final s/step EMA |
> | ---: | --- | --- | --- | ---: | ---: | ---: | --- | ---: | ---: |
> | 41 | `[stage0-pilot-seed41]` | `finished` | 300 / 300 | 566643776.0 | 6081173504.0 | 463856672.0 | worsening | 201.914951 s | 0.09881577425706371 |
> | 42 | `[stage0-pilot-seed42]` | `finished` | 300 / 300 | 650443456.0 | 3734660096.0 | 78489008.0 | improving | 197.683446 s | 0.09758273411582492 |
> | 43 | `[stage0-pilot-seed43]` | `finished` | 300 / 300 | 150720096.0 | 3832843264.0 | 1851546240.0 | worsening | 195.713358 s | 0.09618073375458501 |
>
> All three runs emitted `stage-0-init.pt`, steps 100/200/300 checkpoints,
> `best.pt`, `latest.pt`, and the wall-clock checkpoint. No seed emitted a
> failure bundle or a non-finite step.
>
> ## Defined spread calculation
> For every reported metric, the absolute span is `max(seed values) - min(seed
> values)`. The relative span is `(max - min) / median(seed values)`. No values
> are rounded before the calculation.
> | Metric | Minimum | Median | Maximum | Absolute span | Relative span |
> | --- | ---: | ---: | ---: | ---: | ---: |
> | Final total loss | 150720096.0 | 566643776.0 | 650443456.0 | 499723360.0 | 0.8819003775663107 |
> | Final validation loss | 78489008.0 | 463856672.0 | 1851546240.0 | 1773057232.0 | **3.8224247683129153** |
> | Peak total loss | 3734660096.0 | 3832843264.0 | 6081173504.0 | 2346513408.0 | 0.612212200284744 |
> | Wall clock seconds | 195.713358 | 197.683446 | 201.914951 | 6.201593000000003 | 0.03137133192224908 |
>
> ## Confidence
> **Overall confidence: HIGH.** Three distinct seeds completed the same
> admitted-data configuration with 300/300 finite steps. This is sufficient for
> the requested seed-band calibration. **It is not a convergence claim:** final
> validation relative span is `3.8224247683129153`, and two final validation
> trends were worsening.
>
> ## Ratification record
> **Owner sign-off:** approved on 2026-07-22.
> **Exact R-1 values:** `loss_explosion_ceiling = 100000000000.0`;
> `disk_floor_fraction = 0.05`; `memory_watermark_fraction = 0.7`.
> **Exact R-2 value:** `recover_retries = 0`.
> The four exact owner-provided values are active in `[stage0-example.yaml]`;
> no value was rounded, reinterpreted, or substituted.

---

## Group 3 — Owner-signed verdict and the exhausted evaluator budget

Source: 43-VERDICT.md (near-full; paths abbreviated)

> schema_version: phase43-verdict/v1 · status: owner-signed · gate: FAIL ·
> verdict: adjust · owner_decision: adjust · owner_decision_date: 2026-07-22
>
> # Phase 43 ACC-06 Owner Verdict
> The owner rendered the exact verdict **adjust** on 2026-07-22. This matches
> the agent's grounded recommendation: the Stage-0 mechanical slice is real and
> repeatable, but the sole held-out gate is an unequivocal `FAIL`, and the
> pilot does not establish convergence.
>
> ## Decision boundary
> - **Owner decision:** `adjust` (owner-authored, signed 2026-07-22)
> - **Why `go` cannot be unqualified:** the receipt reports `gate: FAIL` with
>   `eps_H = 237.2086056078468`, versus rejection above `1e-5`. A `go` decision
>   must explicitly acknowledge and override that failed gate.
> - **Confirm-only gate rule:** the authoritative SPEC rejects only when
>   `eps_H > 1e-5` (equivalently `SCS > -5`). Equality passes.
>
> The held-out failure is not marginal: `eps_H / 1e-5` is approximately
> `23,720,860.56`. Healthy validation for seed 42 and a mechanically successful
> smoke therefore do not support a claim that the model passes the physics gate.

### Evaluator invocation audit — THE exhausted budget (grounds the evaluation-policy question)

> The held-out evaluator budget is exhausted. No evaluator or held-out command
> may be run again under the current owner policy.
>
> 1. **Attempt 1 — failed before held-out split access (2026-07-22).**
>    `pinn.evaluate` omitted `config.data.blacklist_path`, so adapter
>    construction refused before held-out split access. No receipt or metrics
>    were written. The narrow wiring repair landed in commit `a136cd36`
>    (`[evaluate.py]`, `[test_evaluate_gate.py]`) with 23/23 focused tests
>    passing.
> 2. **Attempt 2 — failed during gate-metric conversion (2026-07-22).**
>    Exact error: `Cannot convert a MPS Tensor to float64 dtype as the MPS
>    framework doesn't support float64`. No receipt or metrics were written.
>    Held-out split records and predictions were likely processed before this
>    conversion failure.
> 3. **Attempt 3 — final authorized invocation, completed (2026-07-22).**
>    The MPS conversion repair first transferred detached tensors to CPU in
>    their supported dtype and only then cast to float64 (`9ffbd561`). The
>    unchanged three input digests were verified immediately before invocation.
>    The command completed once, wrote the receipt/metrics, refreshed the
>    production summary, and reported `OVERALL: FAIL`. **This was the final
>    invocation regardless of outcome; it must not be retried.**

### Recommendation and owner sign-off

> **`adjust` — agent recommendation (owner-adopted):** Keep the demonstrated
> Stage-0 mechanical slice, but do not authorize the full multi-stage platform
> yet. Investigate and plan corrections for the failed physics-conservation
> gate and non-convergent/noisy pilot behavior. Because the held-out budget is
> exhausted, any later evaluation requires a new, explicitly changed owner
> policy and a separately governed evidence boundary.
>
> **Owner sign-off:** Decision `adjust` (2026-07-22) — retain the demonstrated
> mechanical Stage-0 slice, block full-platform expansion, and route a
> separately governed investigation of the failed physics-conservation gate and
> non-convergent/noisy pilot behavior. This decision does not claim that the
> remedy is known. It does not authorize another held-out evaluation, Stage 1,
> or any PLAT-01..07 implementation.

---

## Group 4 — Training-time loss composition (DIAG-02 excerpts)

Source: 44-DIAGNOSIS.md §3 (quoted faithfully); per-run decomposition output
Source: loss_decomposition.json

> Across `stage0-smoke` and pilot seeds 41/42/43, every run shows a finite
> warmup **spike** dominated by `loss_phys`, and each spike is its own event
> (not one shared figure):
>
> | run | spike step | total | dominant term | term share | grad_norm | lr |
> |-----|-----------|-------|---------------|-----------|-----------|----|
> | smoke | 194 | 4.61e9 | loss_phys | 0.99999 | 5.63e13 | 2.78e-4 |
> | seed41 | 123 | 6.08e9 | loss_phys | 0.99999 | 6.65e13 | 6.39e-4 |
> | seed42 | 100 | 3.73e9 | loss_phys | 0.99998 | 7.06e13 | 7.50e-4 |
> | seed43 | 169 | 3.83e9 | loss_phys | 0.99999 | 6.24e13 | 4.01e-4 |
>
> PHYS-05 interaction: `lambda_phys` first reaches 1.0 at **step 31** in all
> four runs, and `lambda_l == 0.0` at **all 300 steps** in all four runs
> (asserted) — the angular-momentum term never contributed gradient signal.
> `loss_phys` dominates the cumulative view under **both** raw and λ-weighted
> aggregation in every run (dominance does not flip). All four runs finished
> **300/300 finite** steps (0 non-finite steps). `stage0-smoke` is reported as
> a separate fourth trace and is never pooled.

**Read alongside Excerpt 4–5 of the framework-specs bundle:** under the locked
PHYS-05 schedule, Stage 0 (`k ∈ {0,1}`) sets `lambda_E^max = lambda_L^max = 0`,
so both conservation weights are zero throughout Stage 0 — consistent with the
observed `lambda_l == 0.0`. The `loss_phys ≈ 1e9` vs `loss_data ≈ 0.1` scale
gap (roughly ten orders) is the normalization/data-scale sub-facet of the
loss-weighting question.

---

*End of run-evidence bundle. All numbers, SHA-256 identities, timestamps,
verdicts, and the exhausted-evaluator-budget record are reproduced unmodified
from the retained v2.0 artifacts; run-directory and machine paths were
abbreviated to bare names for self-containment. No evaluator was invoked and no
training was run to produce this bundle (SCOPE-22/23).*
