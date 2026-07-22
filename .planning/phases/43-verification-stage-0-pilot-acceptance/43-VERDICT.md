---
schema_version: phase43-verdict/v1
status: awaiting-owner-decision
gate: FAIL
verdict: pending-owner
recommendation: adjust
owner_decision: null
receipt_citation: runs/stage0-pilot-seed42/evaluation/evaluation-receipt.json
seed_citation: .planning/phases/43-verification-stage-0-pilot-acceptance/43-CALIBRATION.md
timing_citation: .planning/phases/43-verification-stage-0-pilot-acceptance/evidence/smoke/README.md
seams_citation: pinn/STATUS.md
---

# Phase 43 ACC-06 Verdict Evidence Draft

This is the evidence package for the owner's `go` / `adjust` / `rethink`
decision. The owner decision is deliberately **not recorded yet**. The agent's
grounded recommendation is **adjust**: the Stage-0 mechanical slice is real and
repeatable, but the sole held-out gate is an unequivocal `FAIL`, and the pilot
does not establish convergence.

## Decision boundary

- **Owner decision:** `pending-owner`
- **Agent recommendation:** `adjust`
- **Why `go` cannot be unqualified:** the receipt reports `gate: FAIL` with
  `eps_H = 237.2086056078468`, versus rejection above `1e-5`. A `go` decision,
  if the owner chooses it, must explicitly acknowledge and override that failed
  gate; this draft cannot encode an unqualified `verdict: go`.
- **Confirm-only gate rule:** the authoritative SPEC and corrected CTX-75 reject
  only when `eps_H > 1e-5` (equivalently `SCS > -5`). Equality passes. No
  correction action is pending.

## Evidence matrix

| Evidence | Observed result | Grounding |
| --- | --- | --- |
| Sole held-out receipt | `FAIL`; `eps_H = 237.2086056078468`; `SCS = 2.3751304405952904`; 1,500 test trajectories; timestamp `2026-07-22T12:23:13.553360+00:00` | `runs/stage0-pilot-seed42/evaluation/evaluation-receipt.json`; `runs/stage0-pilot-seed42/evaluation/metrics.json`; `runs/stage0-pilot-seed42/evaluation/metrics.md` |
| Receipt provenance | checkpoint `6c6f4ae0ebbf6dd56a792503fb32428038bb8dc0f9dc235507a11eff7f9edeaa`; config `ac15f434681d2244fda9a0bcdc8b33416ed1c8737b682f695782501862fb86ad`; splits `5846ae5b55104e55a85d644875c3da187200c3d521f52a9298876d656c6d8903` | `runs/stage0-pilot-seed42/evaluation/evaluation-receipt.json` |
| Preserved artifact identities | receipt `73ea15473a7677f7af75eb424bbdbadb89067e4df10649ad77d6e263eaad033b`; metrics JSON `fe19df3f7c4d56f2d3e4df182c6d320ccd1ba1405dbc888f433b5f14ecb4bdd6`; metrics Markdown `169b7dd6c2bc57f9982341b725ab8b3e92e54bed93b5f360e57af49f6094eed7` | SHA-256 over the three files in `runs/stage0-pilot-seed42/evaluation/` after the sole successful invocation |
| Production summary refresh | completed summary now renders the held-out preview: the same `eps_H`, `SCS`, `FAIL`, and `n_test_trajectories = 1500`; refreshed summary JSON digest `5a11d6ee4f88fbd01979bf587bfa8c95b1fe8f556b51c49099cc3bcb01adcab4`, Markdown digest `f3e9f7b0814221f627c14beecf6d4ff38ca92bc75491aaaff9be5f926f7c9053` | `runs/stage0-pilot-seed42/summary.json`; `runs/stage0-pilot-seed42/summary.md` |
| Pilot seed band | seeds 41/42/43 all finished 300/300 finite steps. Final loss span `499723360.0` (relative `0.8819003775663107`); final validation span `1773057232.0` (relative `3.8224247683129153`); two of three validation trends worsened | `.planning/phases/43-verification-stage-0-pilot-acceptance/43-CALIBRATION.md` |
| Pilot confidence | `HIGH` for the requested three-seed operational calibration; explicitly not a convergence claim | `.planning/phases/43-verification-stage-0-pilot-acceptance/43-CALIBRATION.md#confidence` |
| Timing | accepted smoke `s_per_step = 0.11570179534756522`, 300-step forecast `34.710538604269566 s`; pilot final EMA band `0.09618073375458501`–`0.09881577425706371`; pilot wall-clock band `195.713358`–`201.914951 s`; production estimate recorded as roughly `270`–`305 s/run` | `.planning/phases/43-verification-stage-0-pilot-acceptance/evidence/smoke/README.md`; `.planning/phases/43-verification-stage-0-pilot-acceptance/43-CALIBRATION.md` |
| Owner-ratified seams | B-5 registry unchanged; D4-a checkpoint ceiling `120 s`; R-1 loss ceiling `100000000000.0`, disk floor `0.05`, memory watermark `0.7`; R-2 `recover_retries = 0` | smoke evidence; `43-CALIBRATION.md`; `configs/stage0-example.yaml`; `pinn/STATUS.md` |
| Phase-38 real-trajectory gap | GAP-38-01 is `RESOLVED-WITH-INSTRUCTION`: owner chose real evidence; residual and overfit rungs passed on admitted trajectory `standard_quasi_random_gold_standard/0000` | `.planning/phases/38-pinn-model-rebuild-from-specs-fut-01/38-GAPS.md` |

The held-out failure is not marginal: `eps_H / 1e-5` is approximately
`23,720,860.56`. Healthy validation for seed 42 and a mechanically successful
smoke therefore do not support a claim that the model passes the physics gate.

## Evaluator invocation audit

The held-out evaluator budget is exhausted. No evaluator or held-out command
may be run again under the current owner policy.

1. **Attempt 1 — failed before held-out split access (2026-07-22).**
   `pinn.evaluate` omitted `config.data.blacklist_path`, so adapter construction
   refused before held-out split access. No receipt or metrics were written.
   The narrow wiring repair landed in `a136cd36` (`pinn/evaluate.py`,
   `tests/phase43/test_evaluate_gate.py`) with 23/23 focused tests passing.
2. **Attempt 2 — failed during gate-metric conversion (2026-07-22).**
   Exact error: `Cannot convert a MPS Tensor to float64 dtype as the MPS
   framework doesn't support float64`. No receipt or metrics were written.
   Held-out split records and predictions were likely processed before this
   conversion failure; this attempt is not represented as pre-access.
3. **Attempt 3 — final authorized invocation, completed (2026-07-22).**
   The MPS conversion repair first transferred detached tensors to CPU in their
   supported dtype and only then cast to float64 (`9ffbd561`). The unchanged
   three input digests were verified immediately before invocation. The command
   completed once, wrote the receipt/metrics, refreshed the production summary,
   and reported `OVERALL: FAIL`. This was the final invocation regardless of
   outcome; it must not be retried.

## Validation context

- The narrow conversion regression failed before the repair on real MPS with
  the exact unsupported-float64 error, then passed after the repair.
- Focused metric/evaluator suite: 50/50 passed.
- Phase 43 suite: 173/173 passed after the repair and before the final
  invocation.
- The known full-suite baseline is **not green**: the supplied 1,010-test run
  recorded **24 failures and 10 errors**. Durable evidence in
  `.planning/phases/43-verification-stage-0-pilot-acceptance/deferred-items.md`
  accounts for 17 Phase-41 failures and 5 Phase-42 failures plus 10 Phase-42
  errors caused by older subprocess fixtures lacking the new fail-closed timing
  calibration. `.planning/STATE.md` separately records the older Phase-39
  `test_only_allowed_modules_parse_the_corpus` detector false positive. This
  Task 1 did not rerun or claim to resolve that baseline.

## Recommendation and owner choices

### `adjust` — agent recommendation

Keep the demonstrated Stage-0 mechanical slice, but do not authorize the full
multi-stage platform yet. Investigate and plan corrections for the failed
physics-conservation gate and non-convergent/noisy pilot behavior. Because the
held-out budget is exhausted, any later evaluation requires a new, explicitly
changed owner policy and a separately governed evidence boundary.

### `rethink`

Revisit the viability premise, training objective, metric construction, or
Stage-0 recipe before further platform work. This is the conservative choice
if the magnitude of the held-out failure indicates the current slice is not a
suitable base for incremental tuning.

### `go`

Proceed only as an explicit owner override. The sign-off must state that it is
qualified despite `gate: FAIL`, cite the receipt, and define what the failed
gate permits and forbids. An unqualified `go` is rejected by the grounding
test and must not be recorded.

## Awaiting owner sign-off

Choose `go`, `adjust`, or `rethink`. The decision, date, rationale, and any
qualification belong here only after the owner responds at the blocking-human
checkpoint.

