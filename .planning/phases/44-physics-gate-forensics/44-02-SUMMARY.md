---
phase: 44-physics-gate-forensics
plan: 02
wave: 1
requirements: [DIAG-02]
status: complete
---

# 44-02 Summary — DIAG-02 five-term loss decomposition

## Objective
Decompose the five loss terms per step across `stage0-smoke` and pilot seeds
41/42/43, reporting raw AND λ-weighted contributions, attributing each run's
warmup spike independently, and characterizing the PHYS-05 scheduled-weight
interaction.

## What was built
- `evidence/diag02/loss_decomposition.py` — deterministic, fail-closed analyzer
  across four runs. Per-step raw + λ-weighted values keyed by the JSONL's 1-indexed
  step; spike attribution (max `total`, earliest step on tie); PHYS-05 interaction.
- `evidence/diag02/loss_decomposition.json` — the decomposition (620,174 B).

## Key results (verified fact, cited to the JSON)
- **Each run's warmup spike is its own event** (not one shared ~3.7e9 figure):
  smoke step 194 (total 4.61e9), seed41 step 123 (6.08e9), seed42 step 100
  (3.73e9), seed43 step 169 (3.83e9). `loss_phys` dominates every spike
  (share ≈ 0.99998–0.99999) with grad_norm ~5–7e13; all spikes finite.
- **PHYS-05 interaction:** `lambda_phys` first reaches 1.0 at **step 31** in all
  four runs; `lambda_l == 0.0` at all 300 steps in all four runs (asserted) — the
  angular-momentum term never contributed gradient signal.
- **Dominance does not flip** between raw and weighted cumulative views
  (`loss_phys` dominates both in every run).
- `stage0-smoke` reported as a separate fourth trace; never pooled (D-10). No
  TensorBoard parsing (all required fields are in `train.log.jsonl`).

## Verification
- Byte-identical on re-run.
- Fail-closed: all 26 required keys present in every step record; step set
  exactly {1..300} per run; no loss term imputed as zero.

## Deviations
- Mechanical (recorded, not a physics decision): the artifact carries **27** keys
  per step record, not the plan's "26 expected" — the extra is the `event`
  discriminator. The script asserts the 26 required keys are PRESENT and records
  the actual 27-key set; no term is imputed. Nothing in the analysis depends on
  this off-by-one.
