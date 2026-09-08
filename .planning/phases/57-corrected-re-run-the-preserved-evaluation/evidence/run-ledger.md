# Phase 57 Run Ledger

The ledger is append-only during the smoke and graded run window.  This
scaffold is committed before any run and intentionally contains no launch
records.  The final generation is set only after the complete band or the
authorized scientific terminal branch is recorded.

<!-- phase57-run-ledger-schema: phase57-run-ledger/v1 -->
```json
{
  "schema": "phase57-run-ledger/v1",
  "phase": 57,
  "milestone": "v2.3",
  "pre_registration": {
    "source": ".planning/phases/57-corrected-re-run-the-preserved-evaluation/57-RULING.md",
    "seed": 42,
    "fallback_order": [42, 41, 43],
    "fallback_basis": "structural_ineligibility_only",
    "front_advance_window_n": 500,
    "evaluation": "preserved-unspent-until-three-preconditions-pass"
  },
  "final_band_generation": null,
  "band_generations": [],
  "records": []
}
```
