---
status: complete
phase: 43-verification-stage-0-pilot-acceptance
source: [43-01-SUMMARY.md, 43-02-SUMMARY.md, 43-03-SUMMARY.md, 43-04-SUMMARY.md, 43-05-SUMMARY.md, 43-06-SUMMARY.md, 43-07-SUMMARY.md, 43-08-SUMMARY.md, 43-09-SUMMARY.md, 43-10-SUMMARY.md, 43-11-SUMMARY.md, 43-12-SUMMARY.md]
started: 2026-07-23T06:01:43Z
updated: 2026-07-23T06:01:43Z
verification_method: agent-direct
---

## Current Test

[testing complete]

<!--
This is a verification/acceptance phase: its deliverables are objective code
contracts (verify ladder, duration gate, once-only held-out gate, marker schema,
receipt-grounded verdict) and real run evidence, not click-through UI. Per the
direct-verification protocol for verification-type phases, the agent verified the
semantic contracts by running the phase-43 regression suite rather than asking the
user to hand-confirm each. The two genuine human-judgment items (non-convergence,
go/adjust/rethink verdict) were already rendered by the owner as `adjust`
(2026-07-22, 43-VERDICT.md). The held-out evaluator was NOT re-run (budget
exhausted per the owner verdict).

Coverage classification (gsd query uat.classify-coverage) auto-passed 27 of 33
plan deliverables from passing tests; the remainder were verified directly below.
-->

## Tests

### 1. ACC-01 — Verify ladder + measured-duration gate safely authorize only verified long runs
expected: A five-rung `verify` pre-flight ladder (device sanity → §10.3 AD probe → fp64-CPU gradcheck → residual-on-ground-truth + §10 probes → single-trajectory overfit) plus a smoke-derived duration gate authorize any run > 30 min, and refuse forged/incomplete authorization.
result: pass
source: agent-direct
evidence: |
  Auto-covered: 43-01 D1–D6; 43-04 D1–D4; 43-09 D1–D2 (all `all_auto_covered`).
  CR-03 (duration gate bound to the *requested* not *effective* strict-CPU runtime) — CLOSED: `test_verify_gate.py#DurationGateFunctionTests` green; `_effective_runtime_labels` returns float64/cpu under a float32/mps config.
  CR-04 (forged five-record marker accepted) — CLOSED: `test_verify_ladder.py#MarkerFreshnessTests` green; marker authorization now requires MARKER_SCHEMA_VERSION, exact ordered LADDER, strict booleans, and all six fingerprint keys.
  GAP-43-01 (device-sanity rung vs Phase 38 availability-probe prohibition) — RESOLVED-WITH-INSTRUCTION (owner Option A: MPS materialization proof); prohibition scan 58/58 OK.

### 2. ACC-02 — Real ~5-minute smoke exercises the mechanical surface (interrupt/resume) and records measured s/step
expected: A ~32-trajectory / ~300-step smoke over the real admitted corpus runs Ctrl-C → `--resume latest` to completion, writes checkpoints, and records a measured s/step that forecasts the D4-a ceiling.
result: pass
source: agent-direct
evidence: |
  Real run present: `runs/stage0-smoke` — 300/300 gap-free steps, checkpoints 100/158/200/300, one SIGTERM interrupt + resume to finished, `s_per_step=0.11570179534756522`, 300-step forecast 34.71 s (43-06).
  Auto-covered: 43-06 D1–D2. The 43-03 smoke-composition deliverables (config-seam, admitted CPU/fp32 composition, replay-32 selection, timing calibration, data-reachability preflight) are exercised by the real smoke run and `test_real_data_smoke_config.py` / `test_timing_calibration.py` (green in the 198/198 suite).
  Note (non-blocking): 43-03-SUMMARY.md's `coverage:` block uses `kind:` values outside the allowed enum, so `uat.classify-coverage` flagged those 5 entries `validation_failed` (a summary-authoring nit, not a code gap). Verified directly instead.
  ACC-02 = Complete in REQUIREMENTS.md; repository suite green (43-12: 1,036 → 1,039 with materialization tests).

### 3. ACC-03 — Held-out set evaluated once; binary physics gate rendered honestly
expected: A separate `evaluate` script runs the held-out test set exactly once and renders the binary post-v1.3 gate (`ε_H > 1e-5` reject; `SCS > −5`) with plain-English `metrics.md`; replay/crash/concurrent attempts cannot reopen the budget.
result: pass
source: agent-direct
evidence: |
  Real final receipt present at the canonical path `runs/stage0-pilot-seed42/evaluation/evaluation-receipt.json`: `FAIL`, `eps_H=237.2086056078468`, `SCS=2.3751304405952904`, 1,500 trajectories. Metrics/receipt/summary digests match 43-VERDICT.md.
  Auto-covered: 43-02 (all 3).
  CR-01 (alternate output-dir replay bypass) + CR-02 (non-atomic pre-access claim) — CLOSED: `test_evaluate_gate.py#ClosedEvaluationFlowTests` green; output bound to `<run_dir>/evaluation`, `evaluation-attempt.json` claimed via O_CREAT|O_EXCL before corpus access; failed/abandoned/concurrent/completed attempts all consume the once-only budget.
  Held-out evaluator NOT re-run (budget exhausted). Regressions use synthetic TinyCorpus only.

### 4. ACC-04 — Enriched, honest end-of-run summary
expected: `summary.md` reports final losses, validation summary, curriculum progression, held-out preview, run-to-run comparison hint, and the honesty layer (healthy val ≠ working model; clean loss ≠ correct physics).
result: pass
source: automated
evidence: |
  Auto-covered: 43-05 D1–D3. `runs/stage0-pilot-seed42/summary.md` carries real final losses, validation, curriculum, the 1,500-trajectory FAIL preview, comparison guidance, and all three honesty statements (43-12 acceptance evidence). ACC-04 = Complete in REQUIREMENTS.md.

### 5. ACC-05 — Stage-0 pilot across 2–3 seeds; owner thresholds calibrated from observed variance
expected: The short run repeats across seeds; the seed-band spread is recorded; the ⚖ guard / RECOVER thresholds are calibrated from observed variance for owner ratification.
result: pass
source: automated
evidence: |
  Auto-covered: 43-07 D1–D3. Seeds 41/42/43 all finished 300/300 finite steps; `43-CALIBRATION.md` records raw spread, confidence (HIGH, explicitly not a convergence claim), and dated owner-ratified values (loss ceiling 1e11, disk floor 0.05, memory watermark 0.7, recover_retries 0), loaded from `configs/stage0-example.yaml`.

### 6. ACC-06 — Milestone closes with a go/adjust/rethink verdict + FUT-01/FUT-04 handoff
expected: The owner renders go/adjust/rethink on whether the Stage-0 slice justifies the full platform, and the handoff separates shipped / seam-placeholder / deferred work.
result: pass
source: owner-signed + agent-direct
evidence: |
  Owner rendered `adjust` (43-VERDICT.md, signed 2026-07-22): retain the mechanical Stage-0 slice, block full-platform expansion, investigate the failed physics gate / non-convergence. This is the genuine human-judgment item (43-08 D2) — already made by the owner.
  Handoff (43-08 D3): `pinn/STATUS.md` present — shipped slice / explicit seams / deferred PLAT-01..07.
  CR-05 (verdict backstop validated citation text, not the receipt) — CLOSED: `test_verdict_grounding.py#VerdictGroundingTests` green against the real receipt; typed YAML + ISO-date parsing; gate/eps_H/SCS/checkpoint+config+splits digests compared; a PASS/go citing a FAIL receipt is rejected.

### 7. Gap-closure hardening (CR-01..CR-05) verified against current code
expected: The five authorization-bypass BLOCKERs found by the 2026-07-22 verification are each closed with a TDD regression that was RED before the fix and is now GREEN.
result: pass
source: agent-direct
evidence: |
  Independent run (this session): `~/miniforge3/envs/pinn-train/bin/python -m unittest discover -s tests/phase43 -p 'test_*.py'` → **198 tests, OK** (8.955 s). Suite includes all five CR regressions + the real-receipt-grounded verdict test (real receipt present, not skipped). The `error:`/`OVERALL: FAIL` console lines are the synthetic fail-closed negative controls, not failures.
  Repository-wide green recorded by 43-12 (`discover -s tests` exit 0, 1,036 tests) + GAP-43-01 (+3 materialization tests → 1,039 exit 0). NOT re-run this session (expensive; already recorded; phase42 subprocess suite ~270 s).

### 8. 43-06 D3 — Non-convergent Stage-0 loss reported honestly (human-judgment)
expected: The smoke/pilot loss is bounded but non-descending within the 300-step Adam budget, and this is reported as a watch-item — never framed as convergence.
result: pass
source: owner-adjudicated
evidence: |
  The non-convergence is accurately reported (43-06 records it as an ACC-05 watch-item; 43-CALIBRATION.md confidence is explicitly "not a convergence claim"). The owner's `adjust` verdict is *about* this finding ("investigate the failed physics gate / non-convergence"). It is the phase's honest deliverable, not a defect to fix here.

## Summary

total: 8
passed: 8
issues: 0
pending: 0
skipped: 0
blocked: 0

## Gaps

[none — no code issues found; all ACC-01..06 verified, all 5 CR blockers closed]

## Phase Completion Note

UAT passes with zero issues, but **the phase cannot auto-transition**: the canonical
`43-VERIFICATION.md` still reads `status: gaps_found`. That report was written
2026-07-22T13:01Z and **predates** the gap-closure work (plans 43-09..43-12 and the
GAP-43-01 device-sanity fix) that closed all five of the blockers it cites. It is
**stale**, not evidence of open gaps:

- CR-01/CR-02 → closed by 43-10 (canonical output + O_EXCL atomic claim)
- CR-03/CR-04 → closed by 43-09 (effective-runtime gate + fail-closed marker schema)
- CR-05 → closed by 43-11 (typed, receipt-grounded verdict validation)
- ACC-02/ACC-04 Pending + repository-red → closed by 43-12 + GAP-43-01; ACC-01..06 all Complete in REQUIREMENTS.md

The completion predicate (`phase uat-passed --require-verification`) blocks on the
stale `gaps_found`. `.planning/STATE.md` is also stale (`executing`, `stopped_at:
Completed 43-06-PLAN.md`) and carries uncommitted edits. Legitimate closure requires
refreshing the canonical verification to reflect the now-green state. The held-out
evaluator budget is exhausted — any re-verification must cite the existing receipt and
must NOT re-run the evaluator.
