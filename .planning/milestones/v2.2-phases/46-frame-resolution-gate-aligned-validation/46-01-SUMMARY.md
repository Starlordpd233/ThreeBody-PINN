# Plan 46-01 SUMMARY — Phase 46 Test Scaffolding & Dual-Frame Fixtures

Wave 1 / plan 46-01 of Phase 46 (Frame Resolution & Gate-Aligned Validation),
milestone v2.2. Executed inline (trainex inline-execution convention) in
`.worktrees/trainex` on branch `milestone/v2.1`.

Status: **complete and green.** Files added under `tests/phase46/` only; no
existing file modified.

## execution interpreter

Resolved portably as `PY="$(dirname "$(git rev-parse --git-common-dir)")/.venv/bin/python"`,
which from this worktree resolves to the MAIN checkout virtualenv:

- **Absolute path:** `<home>/Desktop/3_body_problem/.venv/bin/python`
- **torch:** 2.12.0
- **numpy:** 2.2.0
- **pytest:** 9.1.1

**Lockfile-drift observation (record only; a lockfile change is out of Phase 46
scope):** `requirements-lock.txt:19` pins `torch==2.12.1` while 2.12.0 is
installed, and `requirements-lock.txt:11` pins `numpy==2.4.6` while 2.2.0 is
installed. No `pytest==` pin was surfaced. Every later Phase 46 plan reuses the
same resolution expression above.

## exported fixture symbols

`tests/phase46/__init__.py`:
- `_SKIP_PHRASE = "skipped Phase46 production symbol"` (the SOLE definition;
  `__all__ = ["_SKIP_PHRASE"]`; assigned exactly once).

`tests/phase46/_fixtures.py` (`__all__`):
- `StubStageSource` — duck-typed `StageIndex` over an explicit ordered
  `RecordKey -> record` mapping; preserves caller INSERTION order (never sorted)
  on `record_keys()` / `records_at(...)` / `records_at_or_below(...)`; the latter
  accepts a plain int stage. Exposes the full surface: `record_keys`, `get`,
  `n_snapshots`, `snapshot_times`, `snapshot_positions`, `snapshot_velocities`,
  `acceleration_magnitudes`, `dt_out`, `stage_label`, `has_stage`, `records_at`,
  `records_at_or_below`, `is_blacklisted`, `blacklisted_physical_keys`,
  `gold_numeric_stage_count`.
- `make_stub_split_sources` — disjoint, both-non-empty `(train_source,
  validation_source)` 2-tuple; the validation source is inserted in DESCENDING id
  order so `records_at_or_below(0)` is genuinely non-sorted. No constructor for
  any third/withheld split view exists (D-16); the banned identifiers
  `test_source` / `make_test` / `test_index` / `held*out` appear nowhere.
- `StubModel` — callable `model(tau_ic13, masses) -> (N, 9)` float64 tensor with
  `.eval()` / `.train()` / `.training`, a `.calls` shape log, and an injectable
  per-call `fail_hook`.
- `DualFrameTrajectory` — frozen dataclass: `masses`, `times_raw`,
  `positions_raw`, `velocities_raw`, `times_scaled`, `positions_scaled`,
  `velocities_scaled`, `D`, `T`, `finite_difference_tolerance`.
- `make_dual_frame_trajectory` — closed-form Lagrange equilateral generator.
- `make_degenerate_trajectory` — `"non_finite"` / `"coincident"` /
  `"single_snapshot"`.
- `make_empty_source` — zero-record `StubStageSource`.
- `make_pairing_confound_trajectory` — `(trajectory, permutation)` with the mass
  vector cyclically rolled relative to the positions.
- `make_com_offset_trajectory` — `(trajectory, offset, drift)` with a constant
  COM offset + uniform drift added in the raw encoding.

`tests/phase46/test_fixtures_selfcheck.py`: the self-check suite (fixtures only;
imports no not-yet-landed production symbol; never uses `_SKIP_PHRASE`).

## derived finite_difference_tolerance (reuse this; do not re-derive a different number)

`make_dual_frame_trajectory` computes the tolerance from the sampling, `omega`,
and the shared `D`/`T` (NEVER a bare constant; NEVER a physics acceptance
threshold — it is a finite-difference / dtype NUMERICAL tolerance per D-06). The
exact expression (`_scaled_frame_tolerance`):

```
h_raw   = times_raw[1] - times_raw[0]          # raw snapshot spacing
omega_u = omega * T                            # angular velocity in u = t/T
h_u     = h_raw / T                            # spacing in u
amp_u   = amplitude / D                        # amplitude = max body-to-COM distance
wh      = omega_u * h_u
exact_factor = omega_u**2 * |1 - 2*(1 - cos(wh)) / wh**2|   # == omega_u**2 * wh**2 / 12 to leading order
finite_difference_tolerance = 3.0 * amp_u * exact_factor + 1e-12 * omega_u**2 * amp_u
                              ^-- sqrt(9) vector-norm factor      ^-- fp64 round-off floor
```

The closed-form `exact_factor` bounds the central-second-difference truncation
error of the SCALED frame, which is the larger error because `d2/du2` amplifies
the raw truncation by `T**2 / D == D**2` under the locked identity `D**3 == T**2`.
It is a rigorous upper bound on any matched-frame residual. For `h_raw <= 0`
(fewer than two snapshots) the tolerance is `0.0` (no finite-difference
resolution; reads as fail-closed downstream).

**Observed value for the default parameters** `masses=(1.0, 0.8, 0.6)`,
`side=1.0`, `n_snapshots=64`, `n_periods=0.5`:

| Quantity | Value |
|---|---|
| D | 4.641588833612778 |
| T | 10.0 |
| omega = sqrt((m1+m2+m3)/side^3) | 1.5491933384829668 |
| amplitude (max body-to-COM distance) | 0.6508541396588879 |
| h_raw | 0.032188719650584216 |
| **finite_difference_tolerance** | **0.020919480923081466** |

The Lagrange equilateral solution is exact for ARBITRARY masses: the net
gravitational acceleration on body i reduces to `omega**2 * (r_COM - r_i)`,
exactly the centripetal acceleration of rigid rotation about the COM, so the raw
encoding satisfies `d2r/dt2 == a_newton(r, m)` to finite-difference accuracy and
the scaled encoding satisfies `d2r'/du2 == a_newton(r', m)` because `D**3 == T**2`.
Treating the raw arrays as `r'` leaves a residual of `(T**2 - 1) * a_newton ≈ 99x`
the acceleration — the two frames are overwhelmingly separable.

## verification

- Task 1 inline contract check: PASS (`_SKIP_PHRASE` value, non-empty disjoint
  split sources, non-sorted `records_at_or_below(0)`, `StubModel` `(N,14)/(N,3)
  -> (N,9)`).
- Task 2 self-check: `pytest tests/phase46/test_fixtures_selfcheck.py -x -q -rs`
  → **14 passed, 0 skipped**, exit 0, no warnings.
- `pytest tests/phase46/ -x -q` → 14 passed.
- Full-suite collection: `pytest tests/ --collect-only -q` → 1189 tests collected
  cleanly (no import breakage from the added package).
- Acceptance criteria AC1–AC6 all verified (single `_SKIP_PHRASE` assignment;
  `from pinn.constants import` present; no hardcoded D/T literal; banned
  identifiers absent; 2-tuple disjoint non-empty split sources; `StubModel`
  surface incl. fail-hook mode restoration; matched-Plummer `eps_inv`/`1e-10`
  present and `EPS_SOFT` count 0).

**Pre-existing failures (NOT caused by this plan):** `tests/phase43`
`DurationGateLaunchTests` (and the related verify-launch tests) fail in this
worktree with *"no valid persisted Stage-0 timing calibration is available for a
non-smoke launch … Run the ACC-02 smoke (configs/smoke.yaml) to persist a
calibration first."* This is an environmental artifact (the ACC-02 timing
calibration is a run artifact present in the main checkout, not the worktree) and
is unrelated to plan 46-01: `git status --short` shows additions only under
`tests/phase46/`, and `tests/phase43` has no reference to phase46. Spot-checked
green under the confirmed interpreter: phase37 (55 passed), phase38 (128 passed +
84 subtests), phase39 (264 passed), phase40 (163 passed), phase41 (193 passed).

## governance

No new source-silent semantic gap was encountered; GAP-46-01/02/03 are
RESOLVED-WITH-INSTRUCTION and were consumed verbatim (none binds 46-01 directly —
GAP-46-03's two-term tolerance basis is a 46-02 concern). The fixture's
`finite_difference_tolerance` is a numerical resolution bound, deliberately
distinct from any physics threshold (D-06), and is NOT the probe tolerance.
