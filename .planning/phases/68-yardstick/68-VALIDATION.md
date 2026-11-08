---
phase: "68"
slug: yardstick
status: draft
nyquist_compliant: false
wave_0_complete: false
created: "2026-11-08"
---

# Phase 68 validation strategy

## Test infrastructure

| Property | Value |
|---|---|
| Runner | `<home>/miniforge3/envs/pinn-train/bin/python -B -m unittest` |
| Configuration | Repository root, CPU fixtures, fresh process for open attestation |
| Quick check after the tracer | `<home>/miniforge3/envs/pinn-train/bin/python -B -m unittest tests.phase68.test_yardstick_audit` |
| Scoped regression check | `<home>/miniforge3/envs/pinn-train/bin/python -B -m unittest tests.phase68.test_yardstick_audit tests.phase59.test_scorecard tests.phase59.test_scorer_known_errors tests.phase59.test_split_allowlist tests.phase43.test_gate_boundary` |
| Baseline | 80 focused existing tests in 1.823 seconds. Measure the new checks during execution. |

## Sampling rate

- Run the fixture check after the tracer and the scoped regression check
  after completing the fixed-panel path.
- Replay the exact audit JSON through the guarded entry point before its
  commit. Verify the committed report against the JSON and the frozen
  scorer, gate and caller sources before checkpoint 2.
- At each owner checkpoint verify the committed input documents and
  compare the written ruling to the actual reply. Check the scorecard
  freeze after a GAP-59-08 update.
- Keep each synthetic check under 30 seconds. Record the measured runtime
  of the six-record audit and replay separately.

## Per-task verification map

| Task | Wave | Requirement | Threat ref | Evidence and check | State |
|---|---:|---|---|---|---|
| 68-01-01 | 1 | YARD-01 | T-68-01-I | Temporary nested base/gold pair through reader, scoring and gate. Rejected keys hit no corpus open. Quick check above. | Planned |
| 68-01-02 | 1 | YARD-01 | T-68-01-T | Scoped regression check. Exact matrix, tier/gate/horizon edges, explicit nonfinite and refusal states, successful and altered replay fixture. | Planned |
| 68-01-03 | 1 | YARD-01 | T-68-01-I/T | `python -B -m pinn.verification.yardstick_audit --check .planning/phases/68-yardstick/evidence/yardstick-audit.json` with the above interpreter. Audit replay, committed outputs, and cross-check all tables and reported exceptions. | Planned |
| 68-02-01 | 2 | YARD-02, YARD-03 | T-68-02-T | `git cat-file -e HEAD:.planning/phases/68-yardstick/68-CHECKPOINT-2.md`. Inspect the packet against committed audit values and source comparisons. | Planned |
| 68-02-02 | 2 | YARD-02, YARD-03 | T-68-02-E | `git cat-file -e HEAD:.planning/phases/68-yardstick/68-CHECKPOINT-2-RULING.md` after an explicit reply. Verify authority, chronology, gap state, the scorecard freeze, and the follow-up packet. | Owner input |
| 68-02-03 | 2 | YARD-03 | T-68-02-E | Check the committed ruling, each answer or open row, C-5 dependency, and scoped v2.6 handoff. `git diff HEAD^ HEAD --check` checks the ruling commit's patch whitespace. | Owner input |

## Spec acceptance coverage

The numbers refer to the checkboxes in `68-SPEC.md` in order.

| Checkboxes | Task | Evidence |
|---|---|---|
| 1–3 | 68-01-03 | Inventory and complete known-answer rows with exact zero checks, every constant pass and each discrepancy. |
| 4–5 | 68-01-02, 68-01-03 | Native gold and recorded-velocity pairs, separately labelled coarse evidence, and replay with source and input pins. |
| 6–8 | 68-01-02 | Existing boundary and aggregation checks, keyed failure evidence and exact ordered rows with stable metric identities. |
| 9–10 | 68-01-01 through 68-01-03 | Frame, cadence and permutation evidence, pre-open refusal, actual opens and the absence of production execution paths. |
| 11–12 | 68-02-01, 68-02-02 | Audit and packet chronology, three C-7 alternatives, explicit reply before a reciprocal gap update, and open-state behavior. |
| 13–15 | 68-02-02, 68-02-03 | Follow-up packet, separate C-6 and C-7 authority, dispositions and v2.6 amendment routing. |
| 16 | 68-01-03 | Compare all reported constant passes and Brutus failures with the complete result and the metric definitions. |
| 17 | 68-01-03, 68-02-01, 68-02-02 | Review the task, scope and limits of every claim carried into the packet. |
| 18 | 68-02-02, 68-02-03 | Compare the actual owner reply with the ruling, gap and amendment table. |

## Wave 0 requirements

Existing infrastructure covers the phase. The tracer adds the new audit
test module with its implementation before the rest of the audit uses it.

## Manual verifications

| Requirement | Check |
|---|---|
| YARD-01 | Compare every table row and constant pass with the committed JSON. Confirm that the report identifies correct-answer failures and preserves historical versus measured values, routes and sample scopes. |
| YARD-02 | Compare the C-7 recommendation with both grids, then compare the reply and disposition verbatim. A missing, deferred or ambiguous choice leaves GAP-59-08 OPEN and YARD-02 pending. |
| YARD-03 | Check each recommendation against C-1, the baselines, Phase 66/67, the audit and the primary papers. Check the C-6 reply rule and trace each proposed v2.6 amendment to a recorded owner instruction or the standing C-11 route. |

## Validation sign-off

- [ ] Tracer, scoped regression checks and full audit replay pass.
- [ ] Data access evidence shows only the six admitted TRAIN records per capture.
- [ ] Verify table coverage and the scientific judgment checks.
- [ ] Verify owner records and the freeze before phase close.
