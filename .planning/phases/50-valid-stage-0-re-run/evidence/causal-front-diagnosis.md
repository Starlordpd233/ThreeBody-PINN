# Phase 50 Plan 50-06 — Bounded causal-front diagnosis

**Status:** source-grounding record only. Not a recipe change, not a later-generation authorization, and not a reopening of GAP-50-03.

```yaml
grounded_causal_front_repair: none-in-current-sources
later_generation_likelihood_claim: prohibited
telemetry_overwrite_proven: true
validation_conversion_defect: repaired
causal_front_behavioral_remedy: none
```

## Classification

Three findings are classified separately. They are not one defect and do not share a remedy.

| Class | Disposition | What 50-06 did |
|---|---|---|
| Validation conversion defect | Proven conformance defect (D-19). Production used a one-step MPS-to-CPU/`float64` cast that torch 2.12.1 rejects. The locked metric adapter already requires detach → CPU → then `float64`. | Repaired only the prediction conversion in `compute_validation_gate`. Metric, frame, population, thresholds, cadence, and fail-closed exception semantics are unchanged. |
| Telemetry overwrite | Proven by `tests/phase50/test_causal_telemetry.py` before any production edit. Validation compose overwrote `_last_widened_details` between StepGuards and `_log_step` on both the Adam and L-BFGS validation-step boundaries. | Took an immutable training snapshot of `w_n_stats` and residuals immediately after the training compose and passed those explicit values to `_log_step`. Guard ordering and the causal formula are unchanged. This is D-24 provenance, not a causal-dynamics remedy. |
| Causal-front behavioral remedy | Current sources ground none. The invariant-B HALT, the locked formula, the locked `N=500` window, and `front_idx=0` on the retained seed-41 log are internally consistent. They do not identify a wrong literal, a guard defect, or an authorized recipe change. | Recorded `grounded_causal_front_repair: none-in-current-sources`. Did not infer, implement, or automatically repair causal dynamics from `front_idx=0`. |

## Locked causal formula

`RunController._non_data_terms` computes mean-squared residual energy per causal bin as `Rbar = sum(residual**2, body/component) / 3`, then calls `causal_physics_loss(..., return_details=True)`.

`causal_physics_loss` (`pinn/loss_catalog.py`) implements the locked prefix-exponential weights:

- `w_1 = 1` by construction (`CAUSAL_W1`; exclusive prefix of the first bin is 0).
- `w_n = exp(-eta_c * sum_{m<n} stopgrad(Rbar_m))`, with the exponent clamped at the active dtype/device log-tiny floor.
- Default `eta_c = CAUSAL_ETA_C = 1.0`.
- Loss is `(1/N_t) sum_n w_n Rbar_n`.

`front_idx` is then:

```text
front_idx = max({ n | w_n > 0.5 }, default=-1)
```

This is a controller-side reduction of the already-computed `w_n` vector. It is not a second causal law.

With `eta_c = 1`, `front_idx = 0` means `w_1` is the last (and first) weight above 0.5, equivalently that the first-bin mean squared residual was not below `ln(2)` at the evaluated step. That is an algebraic consequence of the implemented formula, not a diagnosis of why the residual stayed there.

## Locked invariant-B guard behavior

`StepGuards` (`pinn/training/guards.py`) evaluates invariant B only on a valid physics-evaluated sample:

- Maintain a monotone high-water mark of `front_idx`. Transient regressions never reset age.
- If the front is not saturated (`high_water < n_colloc - 1`) and `step - last_advance_step > N`, HALT with `guard=invariant_b`, `metric=steps_since_front_advance`, `threshold_provisional=false`.
- `N` is the run-local `front_advance_window_n`. The shipped Stage-0 / seed-41 value is `500`. The guard does not invent, raise, or soften `N`.

This is the owner-ratified GATE-03 / D-20 window. A HALT at step 501 after `front_idx` stayed 0 is the defined gate, not a crash.

## Retained seed-41 facts (generation 3, attempt 2)

Cited from the already-committed terminal record. These numbers justify no recipe edit (D-19 / SCOPE-29 / D-20).

- `evidence/attempts/stage0-rerun-seed41-attempt-02/failure/trip.json`: `guard=invariant_b`, `disposition=HALT`, `step=501`, `threshold=500.0`, `threshold_provisional=false`, `metric=steps_since_front_advance`, `value=501.0`, reason `"causal front high-water mark did not advance within N=500 steps"`.
- `50-05-SUMMARY.md` / `50-VERIFICATION.md`: `front_idx=0` on all 502 logged steps; seeds 42 and 43 were not launched; `final_band_generation` is null.
- `configs/stage0-rerun-seed41.yaml`: `front_advance_window_n: 500`, `max_epochs: 1000`, `n_adam: 1000`, `validation_every: 100`, `lambda_e_max: 0.0`, `replay_count` unset (DATA-05 default 240). No 50-06 edit touched this file.
- Five validation events exist with `gate_status=failed:TypeError` and no sidecar. That is the validation-conversion class above. It did not cause the HALT: the guard runs before validation.

GAP-50-03 Option A (2026-08-15) remains historical context: accept that generation-3 HALT record; do not launch 42/43 at that head; do not change `N`; do not start another generation until separately authorized. This diagnosis does not edit, reinterpret, or resolve GAP-50-03.

## Task-2 telemetry result

`telemetry_overwrite_proven: true`.

The bounded regression `tests/phase50/test_causal_telemetry.py` ran against the pre-repair implementation first. It installed distinguishable training sentinels (`w_min=0.11`, `front_idx=2`, residuals `[0.01, 0.02, 0.03]`) and validation sentinels (`w_min=9.11`, `front_idx=0`, residuals `[9.01, 9.02, 9.03]`) in one validation-step execution.

Observed before the repair:

- StepGuards / `_guard_causal_inputs` received the training snapshot.
- The later `_log_step` emission carried the validation snapshot (`w_min=9.11`) on both the Adam (`phase=2a`) and L-BFGS (`phase=2b`) validation-step boundaries.

That overwrite cannot have caused the seed-41 HALT: the guard consumes training-step causal stats before validation. It would have tainted D-24 front-trajectory provenance at validation steps.

Repair: immutable local copy of training `w_n_stats` and residuals immediately after the training compose, passed as explicit `_log_step` kwargs. Guard ordering, `front_idx` computation, `N=500`, causal `eta`/`w1`, losses, optimizer state, and recipe values were not changed. The passing-after test is the same module.

This provenance repair is not a causal-front remedy and is not represented as one.

## Consulted sources

Each source was opened. None independently grounds a causal-front behavioral repair.

| Source | Why it does not authorize a causal-front remedy |
|---|---|
| `50-VERIFICATION.md` gaps 1 and 3 | Gap 1 records that invariant B did not hold for a full graded run. Gap 3 records the missing validation-ε_H / TypeError. Neither names a wrong causal literal or a legal dynamics change. |
| `50-RESEARCH.md` Seed-41 halt + Open Question 1 | Dispositioned: no independently grounded causal-front defect or remedy exists in current sources. Automatic causal-front repair is prohibited. |
| `50-GAPS.md` GAP-50-03 | RESOLVED-WITH-INSTRUCTION Option A. Historical generation-3 terminal ruling only. Does not authorize generation 4 or a dynamics repair. Read-only in this plan. |
| `pinn/training/controllers.py` causal formula | Matches the locked `w_n` / `front_idx` contract. No mismatch found. |
| `pinn/training/guards.py` invariant-B window | Matches the locked high-water / `N` HALT contract. The seed-41 trip is that contract firing. |
| `pinn/loss_catalog.py` `causal_physics_loss` | Locked prefix-exponential weights; `eta_c=1`, `w_1=1`. No source-silent alternative selected. |
| `configs/stage0-rerun-seed41.yaml` | Frozen recipe. `front_advance_window_n: 500` is the owner-ratified value. Observing a HALT does not authorize editing it. |
| `50-CONTEXT.md` D-19 / D-20 / SCOPE-29 | A change justified by the observed `front_idx` trajectory is tuning and is prohibited. An invariant-B HALT is an owner checkpoint, not a number to adjust. |
| `AGENTS.md` STOP protocol | Source-silent semantic decisions must be surfaced, not invented. |

## What 50-06 may not claim

- `later_generation_likelihood_claim: prohibited`. This plan does not forecast that a later unchanged run will pass invariant B, fail it, or finish.
- Repairing the TypeError does not establish RUN-01 or RUN-02.
- Repairing telemetry ownership does not establish that the causal front will advance.
- `front_idx=0` is compatible with the specified weighting and a large first-bin residual. Compatibility is not a license to change the recipe or the window.
- Plan 50-08 exclusively owns the owner decision when no causal remedy exists: whether a later unchanged generation may be preregistered. This diagnosis does not make that decision.

## Later-generation ownership

Plan 50-08 is the owner-checkpoint plan. 50-06 lands only the grounded conformance work and this record. No smoke, graded seed, preregistration amendment, or generation-4 ledger row is authorized here.
