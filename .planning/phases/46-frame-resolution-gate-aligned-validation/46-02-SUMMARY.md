# 46-02 SUMMARY — CONF-01 target-frame probe core

Plan 46-02 (Wave 2, Strand A computation layer). Builds the train-free residual
instrument that answers RG-02 (are the stored training-target positions raw `r`
or the locked `r' = r/D`?) by MEASURING the resident surface under two symmetric
hypotheses with two control arms (D-01, D-03), never by asserting the
code-inspection suspicion.

## Execution interpreter

Reused from 46-01: `<home>/Desktop/3_body_problem/.venv/bin/python`
(portably `PY="$(dirname "$(git rev-parse --git-common-dir)")/.venv/bin/python"`),
torch 2.12.0, numpy 2.2.0, pytest 9.1.1.

## Exported symbols (`pinn/verification/target_frame_probe.py`)

- Constants: `PROBE_SCHEMA_VERSION`, `ARM_SCALED`, `ARM_RAW`,
  `ARM_POSITIVE_CONTROL`, `ARM_PROVENANCE_CONTROL`, `VERDICT_TARGETS_ARE_SCALED`,
  `VERDICT_TARGETS_ARE_RAW`, `VERDICT_AMBIGUOUS`, `VERDICT_NON_FRAME_DIVERGENCE`.
- Types: `CoordinateConvention`, `ArmResidual`, `TrajectoryFrameMeasures`,
  `ConfoundMeasures`, `PopulationArmSummary`, `FrameProbeOutcome`,
  `FrameProbeUnavailable`.
- Functions: `minimum_pairwise_separation`, `second_difference_acceleration`,
  `newtonian_acceleration_series`, `arm_residual`, `numerical_tolerance_for`,
  `measure_trajectory`, `measure_confounds`, `probe_population`, `decide_verdict`.
- Single source of D/T: `from pinn.constants import D_CHARACTERISTIC_LENGTH,
  T_CHARACTERISTIC_TIME`. Single verified force: `from pinn.physics_residual
  import EPS_SOFT, softened_acceleration`. No hardcoded D/T literal and no
  Phase-38 threshold constant is imported or redeclared (both greps return 0).

## Per-trajectory tolerance — GAP-46-03 (RESOLVED-WITH-INSTRUCTION, 2026-07-26)

Implemented EXACTLY per the recorded resolution (Option A), quoted verbatim in
the module docstring. Verbatim resolution note:

> Option A — ratify the measured two-term numerical comparison tolerance, with
> these binding guardrails:
> 1. Per trajectory and under the same qualifying-snapshot mask, the
>    finite-difference floor is `max(positive_control_median_residual,
>    provenance_control_median_residual)`.
> 2. The fp32 term is the measured, nonnegative residual increase caused by
>    fp32-cast-then-float64-restored copies of the same control inputs. The
>    tolerance is `finite_difference_floor + fp32_roundtrip_increment`.
> 3. Persist the floor, round-trip increment, and sum separately. No safety
>    multiplier, population-fitted percentile, imported physics threshold,
>    Phase 38 threshold, or theory-predicted `~21x` / `~99x` separation may
>    enter the tolerance; those separations remain diagnostics only.
> 4. This tolerance answers only whether two measurements agree within the
>    numerical resolution of the finite-difference operator. It is not a
>    physics-acceptance, target-quality, Hamiltonian, or training threshold.
> 5. Non-finite controls, a non-positive/non-finite tolerance, simultaneous
>    consistency of both hypotheses, or failure of the opposing arm to lie
>    strictly above the tolerance remains fail-closed as `VERDICT_AMBIGUOUS`.

As-implemented formula: `numerical_tolerance_for(control_arms,
fp32_roundtrip_probe)` returns the three terms persisted separately
(`TrajectoryFrameMeasures.tolerance_floor`, `.tolerance_fp32_increment`,
`.numerical_tolerance`):

```
floor      = max(positive_control.median, provenance_control.median)      # guardrail 1
increment  = max(0.0, fp32_roundtrip_probe())                             # guardrail 2 (nonnegative)
tolerance  = floor + increment                                            # guardrail 3 (no multiplier)
# fail closed (tolerance := nan) when any control median is non-finite,
# the increment is non-finite, or the sum is not strictly positive.        # guardrail 5
```

The fp32 round-trip probe re-evaluates the provenance-control arm on
`fp32_cast_then_float64_restore(positions_parsed) / D` and takes the increase
of its median residual over the float64 provenance median — a measured dtype
term, never a constant.

## Qualifying-snapshot mask (D-03 symmetry)

Computed once per trajectory in `_compute_qualifying` from the raw-frame
geometry and index-mapped to every arm: `interior` (central-second-difference
interior points only — endpoints are NOT estimated) AND `finite` AND
`minimum_pairwise_separation > guard`, where the guard is a fixed fraction
(`_SEPARATION_GUARD_FRACTION = 0.1`) of the trajectory's OWN median interior
pair separation — a relative guard, no absolute physics constant. Every
exclusion is ledgered with a reason (`endpoint`, `close_encounter`,
`non_finite`, `too_few_snapshots`); the same ledger is attached to each
`ArmResidual`, so exclusion indices are identical across all four arms.

## Verdict routing — exact rule order (`decide_verdict`, D-06)

1. Empty population → raise `FrameProbeUnavailable` (callers convert to an
   operational failure, never a verdict).
2. Any trajectory non-finite, any empty train/validation subgroup, or
   train-vs-validation disagreement on the winning arm → `VERDICT_AMBIGUOUS`.
3. `VERDICT_TARGETS_ARE_SCALED` (the ONLY D-08 route): every trajectory
   scaled-consistent AND raw-separated (winner `scaled`), every `identity_scaled`
   true, confound register empty.
4. `VERDICT_TARGETS_ARE_RAW` (D-09 route): every `identity_raw` true AND
   raw-arm consistent under the permutation-corrected pairing AND scaled-arm
   separated; confound findings attached, not suppressed.
5. `VERDICT_NON_FRAME_DIVERGENCE` (D-09 route): `identity_neither` unanimous
   AND a stepwise transform divergence is attributable.
6. Anything else → `VERDICT_AMBIGUOUS` (D-09 route); the classifier never
   breaks a tie.

Boundary direction pinned: consistent is `median <= tolerance`; separated is
`median > tolerance` (so a residual exactly at tolerance is consistent and
never separated).

## Implementation notes (defects fixed during integration)

The recovered partial module was nearly complete and faithful to the plan; the
dataset-free suite (which had not yet been written) surfaced three defects, all
fixed and covered by tests:

1. `separation[X]` was keyed on the OPPOSING arm's residual, which inverted
   `decide_verdict` Rule 4 and made `TARGETS_ARE_RAW` unreachable for a genuine
   raw population. Re-keyed to "arm X's OWN residual strictly above tolerance"
   (`test_2`, `test_11b`).
2. `arm_residual.exclusions` was always empty (no-op comprehension), failing
   acceptance criterion 7. The shared per-trajectory ledger is now passed in
   and attached to every arm (`test_5`).
3. `first_diverging_step` flagged a divergence for a fully-conformant scaled
   resident (it equals `r_scaled`, so it differs from every earlier
   intermediate), polluting the confound register and blocking Rule 3.
   Attribution now fires only when the resident does not match the final locked
   output `r_scaled` (`test_11a`).

## Verification

- `pytest tests/phase46/test_frame_probe.py -q -rs` → **19 passed, 0 skipped**.
- `pytest tests/phase46/ -q` → 33 passed (fixtures self-check + frame probe).
- Acceptance greps: both required imports present; 0 hardcoded D/T literals; 0
  Phase-38 threshold constants; explicit `sorted(...)` in `probe_population`;
  0 `simulation_data` references in the test module.

## Provenance

Completed by the position-1 understudy (Claude Code, glm-5.2) after the primary
position-1 session became non-responsive mid-Wave-2 (usage-limit park; owner
instruction authorized the manual takeover — Phase 46 ran under the legacy
announce protocol, so no Stage-4 coverage/approval existed). The primary's
partial `target_frame_probe.py` was preserved and completed; the test module is
new. No code under `pinn/data/`, `pinn/training/`, or `pinn/evaluate.py` was
modified (D-16/D-25).
