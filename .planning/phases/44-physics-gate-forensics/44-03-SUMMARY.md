---
phase: 44-physics-gate-forensics
plan: 03
wave: 1
requirements: [DIAG-03]
status: complete
---

# 44-03 Summary — DIAG-03 three-seed band characterization

## Objective
Characterize the three pilot seeds' validation trends, compute final-loss spreads
using 43-CALIBRATION.md's formulas verbatim, state AGREE/DISAGREE with the
"2/3 seeds worsened" claim, record the held-out-split divergence, and cite the
Phase 38 single-trajectory overfit rung as the machinery-integrity control.

## What was built
- `evidence/diag03/seed_band.py` — deterministic, fail-closed analyzer.
  Three-way direction (first-vs-last, exact-equality=flat); 43-CAL spread
  formulas verbatim; splits.json SHA-256 divergence; Phase 38 citation block.
- `evidence/diag03/seed_band.json` — the band output (9,623 B).

## Key results (verified fact, cited to the JSON)
- **Trend (first-vs-last, D-11):** seed41 improving (2.27e9→4.64e8), seed42
  improving (8.38e8→7.85e7), seed43 worsening (8.97e8→1.85e9) → **1/3 worsened**.
  (`stage0-smoke` worsening, reported as the separate fourth trace.)
- **DISAGREE with 43-CALIBRATION's "2/3 worsened"** — explicitly attributed to the
  direction definition: 43-CAL uses the validation.jsonl last-window `trend`
  field (step200→300, under which seed41 also worsens → 2/3); this script uses
  first-vs-last (step100→300). Neither definition adjudicated.
- **Spreads reproduce 43-CALIBRATION exactly:** final relative span
  `3.8224247683129153` (matches the recorded value; cross-check `True`).
- **Held-out splits diverge:** `stage0-smoke` == `stage0-pilot-seed42`
  (byte-identical SHA-256); seed41 and seed43 each differ → cross-seed magnitude
  comparisons span DIFFERENT held-out populations; only within-seed trend is a
  clean longitudinal signal.
- **Phase 38 machinery-integrity control (cited, never re-run, SCOPE-23):**
  single-trajectory overfit ratio `1097.6107…` ≥ 1e3 PASS in 176 steps; IC13 was
  the `zeros(13)` Phase-38 placeholder. The network CAN fit one trajectory, so
  the gate failure emerges at population scale / under the Stage-0 budget.

## Verification
- Byte-identical on re-run.
- `median != 0` asserted before the relative-span division; no rounding before
  calculation (D-11). Phase 38 block flagged `CITATION-NOT-COMPUTATION`.

## Deviations
None. The plan executed as specified.
