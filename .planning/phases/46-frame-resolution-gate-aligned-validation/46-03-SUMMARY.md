# 46-03 SUMMARY — INST-01 validation gate composition + atomic sidecar

Plan 46-03 (Wave 2, Strand B frame-independent core). Builds the full-pool,
frame-explicit conservation observation that composes the verified
`pinn.verification.gate_metrics` functions, the versioned atomic sidecar writer,
and the compact `validation.jsonl` field producer. The production frame constant
(`RATIFIED_VALIDATION_FRAME`) and the `train.py`/`summary.py` wiring land in
46-07; this plan adds no scheduling logic, trigger condition, or config option
(D-10).

## Execution interpreter

Reused from 46-01: `<home>/Desktop/3_body_problem/.venv/bin/python`,
torch 2.12.0, numpy 2.2.0, pytest 9.1.1.

## Exported symbols (`pinn/training/validation_gate.py`)

- Constants: `GATE_SIDECAR_SCHEMA_VERSION` (`"phase46-validation-gate/v1"`),
  `POSITION_FRAME_SCALED`, `POSITION_FRAME_RAW`, `TIME_COORD_NORMALIZED`,
  `TIME_COORD_RAW`, `MASS_CONVENTION_ORDERED_RAW`, `COHERENT_FRAME_PAIRS`.
- Types: `FrameConvention` (frozen; `__post_init__` raises `IncoherentFrameError`
  on an incoherent position/time pair), `TrajectoryGateRow`,
  `ValidationGateObservation`; exceptions `IncoherentFrameError`,
  `ValidationGateUnavailable`.
- Functions: `json_safe_float`, `gate_time_coordinate`, `build_gate_inputs`,
  `compute_validation_gate`, `sidecar_relative_path`, `publish_gate_sidecar`,
  `validate_sidecar_payload`, `compact_validation_fields`.
- Composition, not reimplementation: `from pinn.verification import gate_metrics`
  is the sole source of velocity / Hamiltonian / eps_H / SCS / aggregation /
  verdict (grep for redefined gate-metric funcs returns 0); the atomic write is
  `pinn.training.atomic_io.atomic_write_text` only (no hand-rolled
  `os.replace`/`.tmp.` — grep returns 0). No import of `pinn.evaluate` (D-16).

## Frame coherence (D-12; GAP-46-01 structural guard)

`COHERENT_FRAME_PAIRS = {(r_prime, u_t_over_T), (r_raw, t_native)}`. The locked
scaled contract's pair is `(r_prime, u = t/T)`; the raw pair exists ONLY to
express an owner-ratified D-09 outcome. `gate_time_coordinate` is the SINGLE
place the gate's time coordinate is constructed (`times / T` under normalized,
`times` unchanged under raw), so the GAP-46-01 pairing (physics-frame positions
handed to gate_metrics with raw native times) cannot arise by omission.

## `compute_validation_gate` contract

1. `keys = sorted(validation_source.records_at_or_below(int(stage)))`; empty →
   `ValidationGateUnavailable` (D-20, instrumentation failure → ineligible).
2. `prior_training = bool(model.training)`; `model.eval()`; the whole pass runs
   in a handler-less `try/finally` that restores the PRIOR mode (strictly
   stronger than the evaluator's unconditional `train()` restore; D-12), inside
   `torch.no_grad()`.
3. Per key: `build_gate_inputs` (the locked `tau = 2*(t/T) - 1` map of
   `batches.py:271-273`) → `model(inputs, masses_batch)` → predicted positions
   `(N,3,3)` → `gate_metrics.compute_trajectory_gate_metrics(predicted,
   gate_time_coordinate(times, frame), masses)` → `TrajectoryGateRow(eps_h,
   scs=gate_metrics.scs_from_eps_h(eps_h))` (per-row SCS is a labeled
   diagnostic, D-14).
4. Aggregate ONCE via `gate_metrics.aggregate_gate_verdict([row.eps_h ...])` —
   worst-case max, SCS from that single value, strict-boundary verdict (the
   boundary `eps_H == 1e-5` PASSES; `> 1e-5` FAILs).
5. `ValidationGateObservation` with `split="validation"`, `gate_status="ok"` and
   both reject thresholds recorded in-band (failure statuses are the 46-07
   caller's responsibility).

Observation-only (D-15): no loss/weight/optimizer/scheduler/stage-exit/replay/
checkpoint-rank/early-stop state is touched.

## Sidecar schema keys (D-18 — what 46-07's summary projection and 46-05 assert)

```
schema_version, run_dir, sidecar_path, global_step, stage, split,
frame{position_frame, time_coord, mass_convention, conf01_evidence_ref},
n_trajectories,
rows[]{record_key{variant, fidelity, id}, eps_h, scs},
n_nonfinite,
eps_h_reject_threshold, scs_reject_threshold,
aggregate_eps_h, aggregate_scs, verdict, gate_status
```

- `publish_gate_sidecar`: builds the payload (run identity is the run-dir NAME
  + the sidecar's own relative path — never absolute), serializes with
  `sort_keys` + trailing newline + `allow_nan=False`, asserts containment, and
  writes via `atomic_io.atomic_write_text` BEFORE any pointer is produced (D-17).
  Two publishes of one observation into same-basename run dirs are byte-identical.
- `validate_sidecar_payload`: exact `schema_version`, all required keys, rows
  count == `n_trajectories`, rows sorted by the `(variant, fidelity, id)` triple,
  every metric finite-or-sentinel, verdict in `{PASS, FAIL}`. Raises `ValueError`
  on any violation; returns the payload on success.
- `compact_validation_fields`: re-reads and schema-validates the published
  sidecar under `run_dir`, then (and only then) returns the pointer fields; a
  missing/truncated/schema-invalid sidecar raises `ValidationGateUnavailable`
  (D-17: a JSONL record can never advertise a sidecar that was not durably
  published).

## Compact `validation.jsonl` gate_* field list (the 46-07 wiring emits these)

```
gate_schema_version, gate_eps_h, gate_scs, gate_verdict, gate_status,
gate_n_trajectories, gate_n_nonfinite, gate_sidecar
```

All metric values are `json_safe_float`-sanitized so `_append_validation_record`'s
`allow_nan=False` cannot raise; a genuinely non-finite `eps_H` is preserved as a
quoted string sentinel with a FAIL verdict (D-20) — never null-collapsed or
dropped (the null-collapsing summary helper is the named anti-analog and is not
used here).

## Verification

- `pytest tests/phase46/test_gate_composition.py -x -q -rs` → **19 passed, 0 skipped**.
- Card verify (fixtures self-check + frame probe + gate composition) → **52 passed, 0 skipped**.
- `pytest tests/phase46/ -q` → 52 passed.
- Acceptance greps: `gate_metrics` import present; 0 redefined gate-metric
  functions; no `pinn.evaluate` import; `validation_every` count 0;
  `atomic_write_text` in use; 0 hand-rolled `os.replace`/`.tmp.`;
  `_null_if_nonfinite` count 0.

## Provenance

Completed by the position-1 understudy (Claude Code, glm-5.2) after the primary
position-1 session became non-responsive mid-Wave-2 (owner-authorized manual
takeover). This module and its suite are new (the primary had not started 46-03).
No change to `pinn/train.py`, `pinn/training/summary.py`,
`pinn/training/controllers.py`, `pinn/evaluate.py`, or `pinn/verification/`
(wiring is 46-07; the evaluator is out of bounds; gate_metrics is composed, not
reopened).
