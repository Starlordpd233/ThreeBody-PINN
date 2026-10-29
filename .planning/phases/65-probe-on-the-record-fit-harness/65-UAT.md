---
status: testing
phase: 65-probe-on-the-record-fit-harness
source: [65-VERIFICATION.md]
started: 2026-10-29T22:40:00Z
updated: 2026-10-29T22:40:00Z
---

## Current Test

number: 1
name: Review the 65-05 judgment-tier reporting prohibition (association, not discovery/cause)
expected: |
  The prose keeps the reproduction framed as a reproduction of already-seen results,
  association only, with D-02/D-07 labels preserved. Non-authoritative LLM-judge text
  review: COMPLIANT (both 65-PROBE-RESULT.md and 65-FINDINGS.md Section 1 state the
  association-only framing explicitly and route themselves for review in 65-FINDINGS.md
  Section 5). Human confirmation is the deciding verdict.
awaiting: user response

## Tests

### 1. Review the 65-05 judgment-tier prohibition: "The historical cosine association must not be presented as independent prospective discovery or causal proof" (65-05-PLAN.md must_haves.prohibitions, status unresolved) against 65-PROBE-RESULT.md and 65-FINDINGS.md Section 1.
expected: The prose keeps the reproduction framed as a reproduction of already-seen results, association only, with D-02/D-07 labels preserved. Non-authoritative LLM-judge text review: COMPLIANT. Human confirmation is the deciding verdict.
result: [pending]

### 2. Review the 65-06 judgment-tier prohibition: "The short 1632 smoke must not be presented as learnability, cause confirmation or measured cost for an unmeasured variant" (65-06-PLAN.md must_haves.prohibitions, status unresolved) against 65-SMOKE-PREDICTION.md and 65-FINDINGS.md Sections 3-4.
expected: The prose keeps mechanics and cost separate from inference; the 0.014265 s/step basis is bounded to the exact configuration with the not-steady-state caveat. Non-authoritative LLM-judge text review: COMPLIANT. Human confirmation is the deciding verdict.
result: [pending]

### 3. Owner decision: amend/re-commit the 65-05 probe registration's two drifted dependency digests (pinn/verification/diagnostic_fit.py 2e2c06eb->b00e45b4, pinn/verification/diagnostic_guard.py d164bc4d->8dd577a2), or leave the probe registration historical.
expected: A recorded owner decision. The probe itself needs no further runs; its committed result remains verifiable (probe verify-result -> VERIFY-RESULT-OK, exit 0, historical-dependency mode). Until decided, probe check-registration refuses against the live tree (exit 2) and one content test fails (RegistrationContentTests.test_the_recorded_dependency_and_source_digests_match_disk).
result: [pending]

### 4. Owner decision: route the two documented 65-04 runner defects (diagnostic_probe.py _render_stdout KeyError on preserved_only verdicts; empty reading_rule.new_measurements field), the missing standalone logger-parity subcommand, and the stdout-rendering suite gap.
expected: A recorded routing decision (remediation plan or accepted-as-historical). Any diagnostic_probe.py edit changes the probe registration's pinned dependency digests, so the decision is coupled to the digest decision above.
result: [pending]

## Summary

total: 4
passed: 0
issues: 0
pending: 4
skipped: 0
blocked: 0

## Gaps
