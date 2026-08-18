---
status: complete
phase: 46-frame-resolution-gate-aligned-validation
source:
  - 46-01-SUMMARY.md
  - 46-02-SUMMARY.md
  - 46-03-SUMMARY.md
  - 46-04-SUMMARY.md
  - 46-05-SUMMARY.md
  - 46-06-SUMMARY.md
  - 46-07-SUMMARY.md
  - 46-08-SUMMARY.md
  - 46-09-SUMMARY.md
started: 2026-07-29T10:38:13Z
updated: 2026-07-29T12:22:08Z
---

## Current Test

[testing complete]

## Tests

### 1. Pre-repair verdict traceability
expected: Opening 46-VERDICT.md shows the committed pre-repair evidence result as VERDICT_AMBIGUOUS, cites the evidence run, and routes the result through D-09 for an owner decision. It does not upgrade the evidence to a clean raw- or scaled-target verdict.
result: pass
source: automated

### 2. Post-repair verdict and operational frame
expected: 46-VERDICT-POSTREPAIR.md and GAP-46-06 preserve the unchanged probe's VERDICT_NON_FRAME_DIVERGENCE result, record exact pairing repair over all 1,651 trajectories with unchanged controls, and trace the operational frame ("r_raw", "t_native", "ordered_raw") to the owner's option-B instruction rather than to a clean machine verdict.
result: pass
source: automated

### 3. Validation conservation artifacts
expected: A Phase 46 validation run publishes one schema-valid validation_gate sidecar per validation event with per-trajectory {record_key, eps_h, scs} rows and the ratified frame; the same event's validation.jsonl record carries the eight gate_* fields, and summary.json/summary.md project them with eval01_precondition_iii. An instrumentation-success/metric-failure observation remains gate_status "ok" with gate_verdict "FAIL".
result: pass
source: automated

### 4. Manifest-parametric population resolution and fail-closed empty eligibility
expected: Manifest-parametric population resolution attributes test exclusions and fails closed when no eligible records remain.
result: pass
source: automated
coverage_id: D1
coverage_source: 46-04-SUMMARY.md

### 5. Resident and control reader routing
expected: Resident and control readers use the model-facing adapter seams, preserve containment, and filter eligibility correctly.
result: pass
source: automated
coverage_id: D2
coverage_source: 46-04-SUMMARY.md

### 6. Deterministic contained evidence payload
expected: The D-05 evidence payload is complete, deterministic, path-redacted, containment-guarded, non-overwriting, and sentinel-safe.
result: pass
source: automated
coverage_id: D3
coverage_source: 46-04-SUMMARY.md

### 7. Sanctioned target-frame CLI surface
expected: The target-frame probe CLI exposes exactly the five sanctioned flags, returns help successfully, and reserves nonzero exit status for operational failure.
result: pass
source: automated
coverage_id: D4
coverage_source: 46-04-SUMMARY.md

### 8. Held-out evaluator isolation
expected: The validation gate neither imports nor transitively loads the held-out evaluator.
result: pass
source: automated
coverage_id: D1
coverage_source: 46-05-SUMMARY.md

### 9. Prior model-mode restoration
expected: The validation gate restores either prior model mode after healthy execution and injected mid-population failure.
result: pass
source: automated
coverage_id: D2
coverage_source: 46-05-SUMMARY.md

### 10. Observation-only non-interference
expected: Validation observations leave model parameters and gradients untouched and produce deterministic consecutive results through the pinned interface.
result: pass
source: automated
coverage_id: D3
coverage_source: 46-05-SUMMARY.md

### 11. Validation-only population
expected: Gate rows are exactly the sorted validation keys, never train or withheld-split keys.
result: pass
source: automated
coverage_id: D4
coverage_source: 46-05-SUMMARY.md

### 12. Atomic sidecar publication
expected: Sidecar publication leaves a valid final file without temporary residue, is byte-identical on repeat, and rejects hostile steps before writing.
result: pass
source: automated
coverage_id: D5
coverage_source: 46-05-SUMMARY.md

### 13. Sidecar schema fail-closed behavior
expected: The full sidecar schema rejects missing or malformed required fields, invalid ordering, count mismatches, and illegal metric encodings.
result: pass
source: automated
coverage_id: D6
coverage_source: 46-05-SUMMARY.md

### 14. Non-finite metric retention
expected: Non-finite metrics survive as quoted JSON sentinels with a retained FAIL verdict instead of being dropped or rendered null.
result: pass
source: automated
coverage_id: D7
coverage_source: 46-05-SUMMARY.md

### 15. Durable-pointer discipline
expected: Missing or corrupt sidecars refuse compact fields; a valid sidecar returns exactly the eight gate_* fields, including a valid metric FAIL with instrumentation status ok.
result: pass
source: automated
coverage_id: D8
coverage_source: 46-05-SUMMARY.md

### 16. Ratified probe population hard gate
expected: The real-corpus probe population uses the exact owner-ratified seed-41/42/43 manifest hashes before any measurement step.
result: pass
source: automated
coverage_id: D1
coverage_source: 46-06-SUMMARY.md

### 17. Single committed real-corpus probe
expected: The sanctioned CONF-01 evidence run executes exactly once and persists the verified schema, verdict, provenance, and redacted paths.
result: pass
source: automated
coverage_id: D2
coverage_source: 46-06-SUMMARY.md

### 18. Ordered COM/boost preprocessing seam
expected: Ordered COM/boost arrays are independently re-derived from raw fixture equations under a nonidentity permutation.
result: pass
source: automated
coverage_id: D1
coverage_source: 46-08-SUMMARY.md

### 19. Resident body pairing
expected: Resident positions, velocities, and masses address the same bodies without changing membership or accounting.
result: pass
source: automated
coverage_id: D2
coverage_source: 46-08-SUMMARY.md

### 20. Minimum repair transform boundary
expected: The pairing repair stops before rotation and global scaling and leaves all twelve pre-existing preprocessing outputs byte-identical.
result: pass
source: automated
coverage_id: D3
coverage_source: 46-08-SUMMARY.md

## Summary

total: 20
passed: 20
issues: 0
pending: 0
skipped: 0
blocked: 0

## Gaps

[none yet]
