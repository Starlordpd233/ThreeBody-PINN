---
status: diagnosed
phase: 39-data-ingestion-stage-0-population-scan
source:
  - 39-01-SUMMARY.md
  - 39-02-SUMMARY.md
  - 39-03-SUMMARY.md
  - 39-04-SUMMARY.md
  - 39-05-SUMMARY.md
  - 39-06-SUMMARY.md
  - 39-07-SUMMARY.md
started: 2026-07-15T06:36:39-07:00
updated: 2026-07-15T07:00:57-07:00
---

## Current Test

[testing complete]

## Tests

### 1. Phase 39 Suite Discovery
expected: The dataset-free Phase 39 suite discovers without import errors or broad deferred skips.
result: pass
source: automated
coverage_id: 39-01-D1

### 2. TinyCorpus and Mechanical Boundary Audit
expected: The read-only fixture and sole-reader/classifier/prohibition audits are deterministic and contained.
result: pass
source: automated
coverage_id: 39-01-D2

### 3. Sole Float64 Parser
expected: Folder mapping, footer provenance, measured cadence, pairing, and hash-state behavior use the sole parser seam.
result: pass
source: automated
coverage_id: 39-02-D1

### 4. Preprocessing and Invariants
expected: COM/momentum normalization, canonical gauge, IC13 construction, and normalization preserve the locked numeric contract.
result: pass
source: automated
coverage_id: 39-02-D2

### 5. Sole Stage Classifier
expected: Only original hierarchical base records receive Stage 0/1 labels; gold and excluded records remain UNASSIGNED.
result: pass
source: automated
coverage_id: 39-02-D3

### 6. Seven-Clause Admission Gate
expected: The full Step-1A gate enforces quarantine/rejection boundaries without denominator floors or external metric substitution.
result: pass
source: automated
coverage_id: 39-02-D4

### 7. Routed Spec Defect Banners
expected: The phase-local spec preserves and routes the known DATA-01/DATA-06 contradictions without modifying authoritative framework specs.
result: pass
source: automated
coverage_id: 39-02-D5

### 8. Immutable Stage Index
expected: StageIndex consumes persisted labels and restricts access to the requested split through the production adapter seam.
result: pass
source: automated
coverage_id: 39-04-D1

### 9. Grouped Hamilton Partition
expected: Physical groups never leak across splits and complete signatures receive deterministic Hamilton allocations.
result: pass
source: automated
coverage_id: 39-04-D2

### 10. Canonical Split Persistence
expected: splits.json is atomic, byte-stable, contained, tamper-checked, and round-trips through typed parsing.
result: pass
source: automated
coverage_id: 39-04-D3

### 11. Replay and Lookahead Selection
expected: Replay, lookahead, padding, local RNG, and identity fail-closed behavior match DATA-05.
result: pass
source: automated
coverage_id: 39-05-D1

### 12. Data-Fidelity Point Set
expected: The mixed snapshot sampler produces aligned global-time model inputs, targets, masses, and provenance.
result: pass
source: automated
coverage_id: 39-05-D2

### 13. Balanced Collocation Point Set
expected: The fixed collocation set uses deterministic near-even quotas over selected trajectories and stays train-restricted.
result: pass
source: automated
coverage_id: 39-05-D3

### 14. Population Report Contract
expected: Persisted labels, gold fail-closed behavior, byte accounting, s_min evidence, and classifier sensitivity are reported deterministically.
result: pass
source: automated
coverage_id: 39-06-D1

### 15. Stage-0 Fatal Boundary
expected: Full admitted Stage-0 counts 0..239 are fatal and 240+ is nonfatal regardless of diagnostic train count.
result: pass
source: automated
coverage_id: 39-06-D2

### 16. Atomic Scan CLI Artifacts
expected: The scan CLI writes canonical contained report/manifest/log artifacts and returns the locked 0/2 status.
result: pass
source: automated
coverage_id: 39-06-D3

### 17. Frozen DATA-01..06 Contract Intent
expected: The deferred Wave-0 contracts accurately encode the locked DATA-01..06 behavior and intended downstream seam.
result: issue
reported: The contracts test selection padding and collocation quotas separately but do not encode their required interaction; the integrated undersized-lookahead case violates GAP-39-12 while all existing tests pass.
severity: major
rationale: human_judgment in 39-01 coverage metadata
coverage_id: 39-01-D3

### 18. Production Adapter Integration
expected: A production-shaped corpus initializes through the sole adapter into an admitted-only CPU-fp32, memory-only set with exact accessors, disposition logs, and version state.
result: pass
source: automated-independent
verification: Current Phase 39 suite passed 219 tests with zero skips; the retained real-corpus adapter scan admitted 15,028 records and passed reader/classifier/accessor/memory audits.
rationale: 39-03-SUMMARY.md is legacy and has no structured coverage block

### 19. Current Dataset-Free and Repository Regression
expected: The current Phase 39 suite and full repository suite both pass with no Phase 39 skips.
result: pass
source: automated-independent
verification: Phase 39 ran 219 tests in 1.968s; full repository ran 402 tests in 188.998s; both exited 0 with zero skips.
rationale: validation_failed because 39-07-P1 uses unsupported coverage kind regression
coverage_id: 39-07-P1

### 20. Retained Real-Corpus Thrust-A Evidence
expected: The retained read-only real-corpus scan proves Stage 0 is train-ready, gold numeric count is zero, memory is below the watermark, and retained artifacts are byte-identical.
result: pass
source: automated-independent
verification: All retained-evidence gates exited 0; full Stage-0 count is 2,265, train count 1,812, gold numeric count 0, memory fraction 0.024292, and the logged splits SHA-256 matches the retained bytes.
rationale: validation_failed because 39-07-P2 uses unsupported coverage kind dataset-backed
coverage_id: 39-07-P2

### 21. Phase-Close Integrity Audit
expected: Reader/classifier/source-integrity and readiness audits agree with the retained report and split bytes without mutating framework specs or simulation_data.
result: pass
source: automated-independent
verification: The exact 39-07-03 gate exited 0; reader, classifier, report, manifest, spec-hash, corpus-fingerprint, evidence-identity, and Phase 38 preflight markers all pass.
rationale: validation_failed because 39-07-P3 uses unsupported coverage kind audit
coverage_id: 39-07-P3

### 22. Replacement-Padded Lookahead Collocation Weight
expected: When a Stage-1 pool is padded with replacement to 16 slots, GAP-39-12 allocates the 4,096 collocation points over all 256 selected replay/lookahead slots, preserving 16 points per slot.
result: issue
reported: With one Stage-1 identity padded to 16 slots, the implementation collapses duplicates to 241 unique keys and assigns only 17 collocation points to lookahead instead of 256.
severity: major

### 23. Memory Safety Configuration
expected: The adapter rejects non-finite/out-of-range memory settings and non-CPU residency so the explicit DATA-01 watermark cannot be bypassed or misreported.
result: issue
reported: memory_watermark=NaN with capacity_bytes=1 constructs successfully at 14,044 resident bytes, and device=meta constructs non-CPU records with a misleading 1,504-byte memory line.
severity: major

### 24. Canonical Phase Verification State
expected: Phase 39 has a fresh passing VERIFICATION.md and completed validation ledger before ROADMAP marks the phase complete.
result: issue
reported: init.verify-work reports verification_status=missing and every 39-VALIDATION task row is still pending while ROADMAP already marks Phase 39 complete.
severity: major

## Summary

total: 24
passed: 20
issues: 4
pending: 0
skipped: 0

## Gaps

- truth: Replacement-padded lookahead retains its locked collocation weight.
  status: failed
  reason: sample_collocation_points deduplicates selected record keys before applying GAP-39-12 quotas.
  severity: major
  test: 22
  root_cause: pinn/data/batches.py:302 constructs identities with tuple(sorted(set(record_keys))), changing M from 256 selected slots to 241 unique keys in the one-lookahead case and assigning only 17 aggregate lookahead points.
  artifacts:
    - path: pinn/data/batches.py
      issue: Duplicate lookahead slots are collapsed before quota allocation.
    - path: tests/phase39/test_batches.py
      issue: Selection and quota tests are separate; no integrated undersized-lookahead quota test exists.
  missing:
    - Extend the frozen Wave-0 contract to cover quota allocation after replacement padding.
    - Preserve selected-slot multiplicity through collocation allocation or encode slot provenance explicitly.
    - Add integration coverage for lookahead pools of size 1 and 15.
  debug_session: .planning/debug/phase39-collocation-slot-multiplicity.md

- truth: DATA-01 residency and memory safety inputs fail closed.
  status: failed
  reason: Adapter constructor parameters are coerced but not validated for finiteness, range, positive capacity, or CPU-only residency.
  severity: major
  test: 23
  root_cause: AdmittedSetAdapter validates only precision; capacity, watermark, interim_s0, and device are forwarded after coercion without domain checks, so NaN/Inf/negative values bypass comparison and non-CPU storage breaks the CPU-oriented byte accounting.
  artifacts:
    - path: pinn/data/adapter.py
      issue: Missing constructor validation for capacity_bytes, memory_watermark, interim_s0, and device.
    - path: tests/phase39/test_adapter.py
      issue: Tests assert the valid CPU path but not invalid configuration rejection.
  missing:
    - Validate finite positive capacity, finite watermark in the allowed range, finite positive interim_s0, and CPU-only residency.
    - Add negative configuration tests, including CLI NaN handling.
  debug_session: .planning/debug/phase39-memory-guard-validation.md

- truth: Phase completion is backed by canonical verification state.
  status: failed
  reason: Implementation and evidence are green, but the GSD completion predicate has no passing VERIFICATION.md and the validation ledger remains pending.
  severity: major
  test: 24
  root_cause: Commit 61adc800 conflated successful Plan 39-07 execution evidence with phase completion, updating ROADMAP and STATE without execute-phase's verify_phase_goal step; unsupported coverage kinds and the untouched validation ledger are independent metadata debts.
  artifacts:
    - path: .planning/phases/39-data-ingestion-stage-0-population-scan/39-VALIDATION.md
      issue: All task rows remain pending.
    - path: .planning/phases/39-data-ingestion-stage-0-population-scan/39-07-SUMMARY.md
      issue: Coverage kinds are unsupported, so phase-close claims classify as validation_failed.
    - path: .planning/ROADMAP.md
      issue: Phase is marked complete despite missing canonical verification.
  missing:
    - Restore Phase 39 to incomplete until implementation gaps are fixed and canonical verification passes.
    - Correct coverage kinds so phase-close evidence is machine-classifiable.
    - Rerun each validation command before marking its ledger row green.
    - Generate a fresh Phase 39 VERIFICATION.md and rerun the shared completion predicate.
  debug_session: .planning/debug/phase39-canonical-verification-state.md
