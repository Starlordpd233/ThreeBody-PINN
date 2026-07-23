---
status: consumed
purpose: execution-plan
created: 2026-07-19
milestone: v2.0
phase: 42-operator-runbook-surface-monitoring
retirement_trigger: Phase 42 plan 01 execution is complete and committed; the widened
  `_log_step` spine is the substrate consumed by 42-04 (JSONL/human sinks) and
  42-05 (TensorBoard residual panel).
execution_status: executed
executed_at: 2026-07-19T02:50 PDT
review_status: passed
---

# Plan 42-01 Execution Summary

**Phase:** 42-operator-runbook-surface-monitoring (Wave 1)
**Position:** 1 (head / launcher)
**Watchdog chain:** `phase-42-execution-c358a84ab0e7c4ba`

## What was done

Landed the shared emission spine that every downstream Phase 42 sink (JSONL
handler 42-04, human mirror 42-04, TensorBoard residual panel 42-05) fans out
from. Three tasks, all verified against the Phase 40/41 regression suite.

### Task 1 — `causal_physics_loss(return_details=True)` (pinn/loss_catalog.py)

- Added keyword-only `return_details: bool = False` parameter to
  `causal_physics_loss`.
- Default path is byte-for-byte unchanged: returns the bare scalar `loss`
  exactly as before.
- When `return_details=True`, returns `(loss, {"w_n": weights.detach(),
  "rbar": rbar.detach()})` — both tensors detached (CTX-70) so the autograd
  graph is not retained across steps.
- **Verification:** inline check prints `OK`; 111 Phase 40/41 tests pass.

### Task 2 — Widen `RunController._log_step` (pinn/training/controllers.py)

- Added 7 new keyword-only params to `_log_step`: `stage`, `grad_norm`,
  `w_n_stats`, `residuals_per_bin`, `s_per_step`, `eta_seconds`, `epoch`,
  plus `step_completed` and `weights`.
- Widened the `extra={}` dict IN PLACE with the canonical JSONL vocabulary:
  `event`, `step`, `phase`, `total`, `lr`, `loss_data/ic/phys/energy/angmom`,
  `stage`, `lambda_data/ic/phys/e/l` (matching `LossWeights` fields exactly),
  `grad_norm`, `w_min/w_mean/w_max/front_idx`, `s_per_step`, `eta_seconds`,
  `epoch`, `step_completed`, plus TB-only `residuals_bin_{n:02d}`.
- `front_idx = max([n for n, w in enumerate(w_n.tolist()) if w > 0.5],
  default=-1)` — the `default=-1` fallback is required for a collapsed
  causal-weight vector (cycle-2 agy HIGH).
- `_non_data_terms` now calls `causal_physics_loss(..., return_details=True)`,
  computes w_n stats + per-bin residuals, converts EVERY scalar to native
  Python via `.item()`/`.tolist()` (cycle-2 agy HIGH — no `torch.Tensor`
  reaches `json.dumps`), and stashes on `self._last_widened_details`.
- `self._last_widened_details` initialized `None` in `__init__`; `_log_step`
  is None-tolerant so tests that monkeypatch `_compose_loss_terms` still log.
- Per-step-delta clock (`self._last_step_wall`, `self._s_per_step_ema`) for
  `s_per_step` (EMA) and `eta_seconds` (stage-remaining ETA, null until warm).
- `run.log_every` unchanged — no `log_freq` field (Anti-Pattern #2).
- **Verification:** inline signature check prints `OK widened`; 111 tests pass.

### Task 3 — Emit before every guard early-return (Adam + L-BFGS)

- **Adam** (`_run_adam_phase`): `_log_step` fires BEFORE all 5 guard-disposition
  returns (guard hook tripped, non-finite loss ×2, clip non_finite ×2), each
  with `step_completed=False`, `step=self._global_step + 1` (the index the
  completed step would have carried). Normal completion path logs once at the
  original site, now widened with `stage=k`, `grad_norm`, `epoch`, `weights`.
- **L-BFGS** (`_run_lbfgs_phase`, controllers.py:748 — cycle-2 claude LOW
  method-attribution fix):
  - `_make_lbfgs_closure` now stashes `closure_state['data_detached']`
    (detached `weighted_data`) on each closure invocation.
  - New `_lbfgs_full_loss_terms(closure_state)` builds a full `LossTerms`
    from `closure_state['data_detached']` + `self._last_widened_details`
    (review finding #7), replacing the total-only `_scalar_loss_terms` at the
    L-BFGS log site. A one-line caveat comment notes the breakdown reflects
    the last closure evaluation, not necessarily the accepted step.
  - Guard-trip returns (3) and the normal completion log all emit the widened
    record with `step_completed=False`/`True` respectively.
  - Guard-bridge `_scalar_loss_terms(total_for_guard)` at :805 left UNCHANGED.
- **Verification:** 111 Phase 40/41 controller tests pass (control flow
  unchanged; only emission moved/duplicated).

## Acceptance criteria (all met)

- [x] `grep -nE 'return_details' pinn/loss_catalog.py` — keyword-only
  default-False param + tuple-return branch present.
- [x] Phase 38/40/41 loss + controller tests pass unchanged (default path
  byte-for-byte preserved).
- [x] Inline check prints `OK` (default == details-path loss; keys exactly
  `{w_n, rbar}`; both tensors `requires_grad == False`).
- [x] `RunController._log_step` signature contains all 7 new keyword params
  (inline check prints `OK widened`).
- [x] `grep -nE 'return_details=True' pinn/training/controllers.py` —
  `_non_data_terms` uses the details path.
- [x] `grep -c 'log_freq' pinn/training/controllers.py` returns 0.
- [x] `grep -nE 'front_idx' pinn/training/controllers.py` shows the
  `w_n > 0.5` propagation-front computation WITH `default=-1` fallback.
- [x] `grep -nE 'lambda_data|lambda_ic|lambda_phys|lambda_e|lambda_l'`
  shows canonical `LossWeights` field names; `grep -c 'lambda_energy|lambda_angmom'`
  returns 0.
- [x] `_non_data_terms` stash converts detached tensors to native Python
  (`.item()`/`.tolist()`) — no `torch.Tensor` reaches `json.dumps`.
- [x] `_log_step(` call appears before every guard-disposition `return` in
  both `_run_adam_phase` and `_run_lbfgs_phase`.
- [x] `grep -nE 'step_completed'` shows the boolean on both normal and
  guard-trip paths.
- [x] L-BFGS emission builds full widened record from
  `closure_state['data_detached']` + `self._last_widened_details`;
  guard-bridge `_scalar_loss_terms(...)` at :805 unchanged.
- [x] 111 Phase 40/41 controller tests pass.

## Files modified

- `pinn/loss_catalog.py` — `causal_physics_loss(..., return_details=False)`
  additive detached-details path.
- `pinn/training/controllers.py` — widened `_log_step`, `_non_data_terms`,
  `_lbfgs_full_loss_terms`, guard-trip emissions in both optimizer phases.

## Watchdog chain

- Chain token: `phase-42-execution-c358a84ab0e7c4ba`
- Position 1 done marker published:
  `wd-publish-done --key phase-42-execution-1 --stage phase-42-execution-c358a84ab0e7c4ba --scope 'pinn/loss_catalog.py pinn/training/controllers.py'`
- Join cards for positions 2–9 emitted by `wd-chain-start` (see launcher
  transcript); hand off to separate top-level sessions.
