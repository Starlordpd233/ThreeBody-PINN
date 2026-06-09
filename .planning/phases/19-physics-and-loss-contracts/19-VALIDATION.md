---
phase: 19
slug: physics-and-loss-contracts
status: passed
nyquist_compliant: true
wave_0_complete: true
created: 2026-06-09
---

# Phase 19 - Validation Strategy

## Test Infrastructure

| Property | Value |
|---|---|
| Framework | shell and `rg` structural contract checks |
| Config file | none |
| Quick run command | `rg -n "PASS: AC-PHYS-0[1-6]" .planning/phases/19-physics-and-loss-contracts/19-VERIFICATION.md` |
| Full suite command | Current-spec checks for PHYS-01 through PHYS-06 plus evidence-packet and stale-wording guards |
| Estimated runtime | under 10 seconds |

## Sampling Rate

- After each spec-edit task: run the task's targeted positive and negative `rg` guards.
- After each plan wave: run every AC-PHYS structural check affected by the wave.
- Before closeout: run the six-contract full suite and confirm no live `pinn/` diff.

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Test Type | Automated Command | File Exists | Status |
|---|---|---|---|---|---|---|---|
| 19-01-* | 01 | 1 | PHYS-01, PHYS-03, PHYS-06, VER-05 | doc-structure | Check raw-mass scaling, matched Plummer static invariant, IC13 validity, B-02/B-09/M4 evidence, and stale-text absence | yes | green |
| 19-02-* | 02 | 2 | PHYS-02, PHYS-03, PHYS-04, PHYS-05, VER-05 | doc-structure | Check normalized-time derivative, componentwise AD, matched Plummer force/energy, soft regularizer, causal loss, and optional P2 ALM markers | yes | green |
| 19-03-* | 03 | 3 | PHYS-04, PHYS-05, VER-05 | negative doc-structure | Check HNN and pseudo-ALM default framing is absent and FUT-01 divergence remains handoff-only | yes | green |
| 19-04-* | 04 | 4 | PHYS-01..06, VER-05 | full-suite | Re-run all six AC-PHYS guards and require `PASS: AC-PHYS-01` through `PASS: AC-PHYS-06` | yes | green |

## Wave 0 Requirements

- [x] Phase 16 evidence packets B-02, B-07, B-08, B-09, and M4 exist.
- [x] Phase 16 issue-ledger lifecycle schema exists.
- [x] `19-VERIFICATION.md` records the six structural acceptance checks.
- [x] No additional test framework is required.

## Manual-Only Verifications

None. `19-VERIFICATION.md` records that all Phase 19 must-haves are checkable through repository text, evidence packets, ledger status, and structural guards.

## Validation Sign-Off

- [x] All Phase 19 task groups have automated structural verification.
- [x] Sampling continuity is preserved across all four plans.
- [x] Wave 0 dependencies exist.
- [x] No watch-mode flags.
- [x] Feedback latency < 10s.
- [x] `nyquist_compliant: true` set in frontmatter.

**Approval:** approved 2026-06-09 after the six-contract structural suite passed.

## Validation Audit 2026-06-09

| Metric | Count |
|---|---|
| Gaps found | 1 missing `VALIDATION.md` |
| Resolved | 1 |
| Escalated | 0 |
