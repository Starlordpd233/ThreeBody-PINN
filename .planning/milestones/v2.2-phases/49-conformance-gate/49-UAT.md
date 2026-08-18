---
status: complete
phase: 49-conformance-gate
source:
  - 49-01-SUMMARY.md
  - 49-02-SUMMARY.md
  - 49-03-SUMMARY.md
  - 49-04-SUMMARY.md
  - 49-05-SUMMARY.md
  - 49-06-SUMMARY.md
  - 49-07-SUMMARY.md
  - 49-08-SUMMARY.md
started: 2026-08-07T08:29:48Z
updated: 2026-08-07T08:34:48Z
verification_mode: agent-automated
verification_note: >
  Owner explicitly delegated the five pending operator checkpoints to the agent
  on 2026-08-07. Each was discharged with fresh executable evidence rather than
  by accepting the phase summaries at face value.
verify_pre_gates:
  - capId: ai-integration
    check: api-coverage.verify-pre
    block: false
    message: "api-coverage: no external-API integration detected; coverage matrix not required"
---

## Current Test

[testing complete]

## Tests

### 1. Exact PHYS-05 stage-table assertion
expected: Exact PHYS-05 table assertion reads ScheduledWeights.state_dict and enforces locked/advisory tiers.
result: pass
source: automated
coverage_id: 49-01-D1

### 2. Run-start refusal evidence ordering
expected: Run-start preflight persists passed and failed assertion evidence, including refusal-before-exit ordering.
result: pass
source: automated
coverage_id: 49-01-D2

### 3. Stage-boundary conformance enforcement
expected: CurriculumController re-asserts entered stages and refuses an un-rebound Stage-2 scheduler.
result: pass
source: automated
coverage_id: 49-01-D3

### 4. Invariant configuration contract
expected: Optional InvariantsConfig validates the owner slot and fail-closed YAML mapping.
result: pass
source: automated
coverage_id: 49-02-D1

### 5. Runtime invariant HALTs
expected: Invariant A/B and causal_stats_missing trip HALT with saturation, high-water, and record-only coverage.
result: pass
source: automated
coverage_id: 49-02-D2

### 6. Guard-hook causal-statistics wiring
expected: guard_hook forwards existing causal statistics and collocation length while retaining failure bundles.
result: pass
source: automated
coverage_id: 49-02-D3

### 7. Schema-v2 invariant-B checkpoint payload
expected: Schema-v2 checkpoint payloads persist invariant-B state and dynamic schema versioning.
result: pass
source: automated
coverage_id: 49-03-D1

### 8. Resume-continuous stall window
expected: Invariant-B state restores across a checkpoint and trips at the continued-window boundary.
result: pass
source: automated
coverage_id: 49-03-D2

### 9. Fail-closed resume payload handling
expected: Schema-v1, missing-key, malformed-state, and explicit-None resume outcomes are covered.
result: pass
source: automated
coverage_id: 49-03-D3

### 10. Placeholder census completeness
expected: Explicit placeholder census covers the D-08 population, blocks unwaived placeholders, records provisional disagreements, and checks instrumentation fields.
result: pass
source: automated
coverage_id: 49-04-D1

### 11. Divergence-register proof integrity
expected: Divergence register validates fail-closed, preserves mandatory entries, and executes every closed proof-test node.
result: pass
source: automated
coverage_id: 49-04-D2

### 12. Composed preflight evidence
expected: Run-start preflight composes table, census, open-register, and findings evidence with refusal-first and byte-idempotent writes.
result: pass
source: automated
coverage_id: 49-04-D3

### 13. Conformance projection in summary.json
expected: summary.json carries the validated preflight payload verbatim and reports the kind-filtered eval01_precondition_i flag.
result: pass
source: automated
coverage_id: 49-05-D1

### 14. Conformance rendering across run dispositions
expected: summary.md renders a Conformance section for valid, malformed, absent, finished, and failed/refused run states.
result: pass
source: automated
coverage_id: 49-05-D2

### 15. Owner-ratified invariant-B enforcement
expected: |
  The shipped Stage-0 configuration enforces the owner-selected front-advance
  window N = 500. The INV-B-N-UNSET divergence is closed with an executable
  proof test, and a conformant synthetic run reports eval01_precondition_i as
  true rather than silently remaining in record-only mode.
result: pass
source: agent-automated
evidence: |
  The real config loader returned front_advance_window_n == 500. The real
  register loader returned INV-B-N-UNSET with status closed, waiver null, and
  proof_test test_invariant_b_trips_after_window_and_marks_threshold_nonprovisional.
  That proof node plus the real synthetic main composition seam both passed:
  2 passed in 2.82s. The seam asserts summary.json eval01_precondition_i is true.

### 16. Maintained launch fixtures preserve the PHYS-05 gate
expected: |
  Maintained launch suites use the locked Stage-0 PHYS-05 row and launch
  successfully, while an explicit non-conformant-cap test is still refused.
  The production launch gate itself was not weakened to make fixtures pass.
result: pass
source: agent-automated
evidence: |
  Phys05LaunchGateTests exercised both the conformant launch and explicit
  non-conformant-cap refusal: 2 passed in 3.97s. The exact 49-07 range
  d2f4de5e..b0dd0774 is byte-unchanged for pinn/train.py. A broader comparison
  to current HEAD differs only because the later 7d4ffd8d CR-08 producer wiring
  moved the still-present preflight call after RunController construction; the
  current file retains run_start_preflight and the controlled refusal branch.
coverage_id: 49-07-CR-10

### 17. Null invariant sections load consistently
expected: |
  Omitting run.invariants, using an empty mapping, a comment-only section, or
  explicit null all resolve to the same default InvariantsConfig shape; both
  shipped configurations load while unknown keys still fail closed.
result: pass
source: agent-automated
evidence: |
  tests/phase49/test_config_null_sections.py and tests/phase40/test_config.py
  passed together: 32 passed in 0.62s. The selection covers omitted, empty,
  comment-only, explicit-null, scalar-refusal, unknown-key, and both shipped
  configuration paths.
coverage_id: 49-07-CR-01

### 18. Strict causal-front index validation
expected: Invariant B accepts only a finite, non-boolean, integral front_idx equal to -1 or within [0, n_colloc); malformed values and impossible restored high-water marks are refused.
result: pass
source: automated
coverage_id: 49-07-CR-02

### 19. Non-finite preflight artifact refusal
expected: Preflight artifacts carrying NaN or Infinity are rejected at load and cannot be written, while terminal summary finalization still succeeds.
result: pass
source: automated
coverage_id: 49-07-CR-11

### 20. Self-contradicting preflight refusal
expected: A passed artifact contradicting its own failed event or failed locked check is refused, and a forged artifact cannot report EVAL-01 eligibility.
result: pass
source: automated
coverage_id: 49-07-CR-05

### 21. Closed divergence proof resolution
expected: A closed entry whose proof_test does not resolve to a real module and node fails the register load closed; every valid closed proof node executes successfully.
result: pass
source: automated
coverage_id: 49-07-CR-07

### 22. Controlled setup and scheduler refusals
expected: |
  Malformed metadata, census producer failures, and corrupt scheduler scalars
  produce a controlled non-zero launch result only after a failed run_start
  event is persisted. Booleans, strings, infinities, and negative budgets do
  not bypass the gate or leak raw TypeError/OverflowError failures.
result: pass
source: agent-automated
evidence: |
  Seventeen focused cases passed in 1.02s: cap and budget/warmup type-domain
  matrices, the real entrypoint's infinite-budget refusal, the real entrypoint's
  census RuntimeError refusal, malformed metadata, RuntimeError census, and
  non-mapping census-result persistence/normalization paths.

### 23. Append-only resumed evidence and concrete census producers
expected: |
  Reusing a run directory validates and retains every existing preflight event
  in order before appending the new attempt; malformed prior history is never
  replaced. The concrete census producer suite still resolves resident,
  batch, model, collocation, anchor, and non-data-term quantities.
result: pass
source: agent-automated
evidence: |
  The two resume-history tests and all thirteen concrete census producer tests
  passed together: 15 passed in 1.43s. This includes canonical-byte retention,
  malformed-history non-replacement, shape/finiteness/body-order corruption,
  missing producer fields, and producer exceptions.

## Summary

total: 23
passed: 23
issues: 0
pending: 0
skipped: 0
blocked: 0

## Coverage Classifier Warnings

- `49-07-SUMMARY.md` CR-10 uses unsupported verification kind `invariant`.
- `49-07-SUMMARY.md` CR-01 uses unsupported verification kind `regression`.
- Both deliverables remain present as manual checkpoints; neither was dropped
  or auto-passed from the malformed metadata.

## Gaps

[none yet]
