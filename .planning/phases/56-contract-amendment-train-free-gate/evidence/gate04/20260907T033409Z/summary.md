# GATE-04 — the completed gate's authoritative run

This is the phase's own end-to-end evidence run: the finished GATE-04 module
(`pinn/verification/gate04_train_free.py`), with every plan of Phase 56
landed (56-01 through 56-05), invoked once for the record via its operator
CLI over the six default audited cases.

## Command as executed

```
.venv/bin/python -m pinn.verification.gate04_train_free
```

- Working directory: `<home>/Desktop/3_body_problem/.worktrees/trainex`
- Started: `2026-09-07T03:30:27Z`
- Completed: `2026-09-07T03:34:10Z`
- Elapsed: `223` seconds
- Exit code: `0`

## Tree state

- git_sha: `be823429215c6576ee05b86a44e0e9503743cbf0` (available=True) — the
  commit landing plan 56-06 Task 1 (`56-OPEN-ITEMS.md`), the last commit on
  this branch before this run
- git_worktree_dirty: `True` (available=True) — pre-existing, unrelated
  working-tree changes outside this phase's scope were present at run time
  (`.planning/config.json`, a v2.2 design doc); this run's own files
  (`r_ref_stage0.json`, this evidence directory) are what this task commits
- precision/device: `float64` / `cpu`
- torch_version: `2.12.0`
- numpy_version: `2.2.0`

## Verdict

```
verdict=PASS INCOMPLETE (unratified: ii; GAP-56-01 OPEN, see 56-GAPS.md)
```

- `verdict`: `PASS`
- `blocking_reasons`: (none)
- `unratified_conditions`: `("ii",)` — condition (ii) remains unratified;
  GAP-56-01 is still OPEN. This PASS is an INCOMPLETE result by the module's
  own contract, not a full GATE-04 clearance.
- `causal_clip_min_weight`: `2.2250738585072626e-308` (float64/cpu dtype
  clamp floor, read from the runtime at call time)

## Per-case table

| Case | seed | `front_idx` | min weight | condition (i) satisfied |
|---|---|---|---|---|
| 41 | 41 | 0 | 1.313271e-06 | True |
| 42 | 42 | 0 | 2.100040e-11 | True |
| 43 | 43 | 0 | 2.405949e-07 | True |
| 0 | 0 | 0 | 5.101871e-08 | True |
| 7 | 7 | 0 | 1.922777e-07 | True |
| 41-variable-mass | 41 | 0 | 7.192018e-08 | True |

Every one of the six cases satisfies condition (i): every reported minimum
weight sits many orders of magnitude above the dtype clamp floor. `front_idx
= 0` for all six at initialization is the expected, healthy result (see
`56-OPEN-ITEMS.md` Section 2, Finding 1) — not a failure signal. Condition
(ii) is measured (`condition_ii_diagnostics`, `condition_iii_diagnostics`,
both present on every case entry) but not adjudicated; GAP-56-01 remains
OPEN.

## Reference value

- Statistic: `median` (numpy.median convention — the arithmetic mean of the
  two central order statistics of the 96 sorted values, explicitly not
  `torch.median`'s lower-of-two)
- Reference value (`R_ref`): `19749775821.24417`
- Constituent data: 6 cases x 16 bins = 96 raw bin means, all recorded in
  the committed `pinn/verification/artifacts/r_ref_stage0.json`

## Provenance succession — this run supersedes the tracer's value

The regenerated `pinn/verification/artifacts/r_ref_stage0.json` committed by
this task carries this run's provenance (`git_sha` above), not plan 56-01's
tracer-commit provenance. The numeric `R_ref` value itself is unchanged from
every prior run in this phase (56-01, 56-02, 56-03, 56-05 all independently
reproduced `19749775821.24417`) because the computation is fully
deterministic — the same recorded seeds, the same network construction, the
same 4096-point stratified draw. What changes is which code path produced
it: plan 56-01's tracer slice wired only condition (i); this run is the
finished gate, with conditions (i) and (iii) fully wired and both diagnostic
records populated on every case. The artifact that will gate Phase 57's
RUN-04 should carry the finished path's provenance, not the tracer's — that
is the entire reason this task re-runs the gate rather than treating the
already-committed tracer artifact as final.

## Re-derivability

This run wrote its own evidence directory (`raw.json` beside this file,
non-overwriting, timestamped) via the operator CLI's own evidence writer,
and refreshed the governed `R_ref` artifact at its default path because the
invocation used no `--cases-config` (the canonical six-case run). Re-running
the identical command against the identical commit will reproduce this
record bit-for-bit, per the module's fully deterministic construction.
