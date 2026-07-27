"""CONF-01 / RG-01 target-frame probe — train-free residual on stored targets.

This module is the CONF-01 measurement core (Phase 46, plan 46-02). It answers
RG-02's question — are the exact stored positions consumed as training targets
the raw ``r`` or the locked ``r' = r/D``? — by MEASURING the resident
``StageIndex`` surface under two symmetric hypotheses with two control arms
(D-01, D-03), never by asserting a code-inspection suspicion.

Motivating observation (NOT the verdict): the residency path stores
``parsed_brutus.positions`` (``pinn/data/adapter.py:863,925-926,938``). Code
inspection alone does not set the verdict (D-01/D-04); the verdict derives only
from measured residual and identity evidence produced here. Evidence rendering
and the real-corpus CLI are plan 46-04; the one real evidence run and the
D-08/D-09 branch routing are plan 46-06.

Frame symmetry (D-03)
---------------------
Four structurally parallel arms — scaled-hypothesis, raw-hypothesis, positive
control (canonical preprocessing output), provenance control (parsed raw) — each
carry an explicit ``CoordinateConvention``. No arm is privileged in code: both
hypothesis arms are built by the same helper with different conventions. Under
the implemented normalized relative residual
``norm(a_fd - a_newton) / clamp_min(norm(a_fd), tiny)`` the theory-predicted arm
separations (REPORTED diagnostics only, never classification constants) are: a
raw series read as scaled gives ``a_fd = T^2 a`` vs ``a_newton = a``, i.e.
``(T^2 - 1)/T^2 ~= 0.99``; a scaled series read as raw gives
``a_fd = (1/D) a'`` vs ``a_newton = D^2 a'``, i.e. ``D^3 - 1 = 99`` — with
``D^3 == T^2 == 100`` (``pinn/constants.py:24,31``). Both dwarf any numerical
tolerance.

Tolerance basis — GAP-46-03 (RESOLVED-WITH-INSTRUCTION, 2026-07-26)
-------------------------------------------------------------------
The per-trajectory comparison tolerance is implemented EXACTLY per the recorded
resolution, which ratifies Option A. Verbatim resolution note:

    "Option A — ratify the measured two-term numerical comparison tolerance, with
    these binding guardrails:
    1. Per trajectory and under the same qualifying-snapshot mask, the
       finite-difference floor is ``max(positive_control_median_residual,
       provenance_control_median_residual)``.
    2. The fp32 term is the measured, nonnegative residual increase caused by
       fp32-cast-then-float64-restored copies of the same control inputs. The
       tolerance is ``finite_difference_floor + fp32_roundtrip_increment``.
    3. Persist the floor, round-trip increment, and sum separately. No safety
       multiplier, population-fitted percentile, imported physics threshold,
       Phase 38 threshold, or theory-predicted ``~21x`` / ``~99x`` separation may
       enter the tolerance; those separations remain diagnostics only.
    4. This tolerance answers only whether two measurements agree within the
       numerical resolution of the finite-difference operator. It is not a
       physics-acceptance, target-quality, Hamiltonian, or training threshold.
    5. Non-finite controls, a non-positive/non-finite tolerance, simultaneous
       consistency of both hypotheses, or failure of the opposing arm to lie
       strictly above the tolerance remains fail-closed as ``VERDICT_AMBIGUOUS``."

A dtype-only basis was rejected because it omits the discretization error of the
measurement operator and would test the coherent controls against a bound below
that operator's own resolution.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
import torch

from pinn.constants import D_CHARACTERISTIC_LENGTH, T_CHARACTERISTIC_TIME
from pinn.physics_residual import EPS_SOFT, softened_acceleration

__all__ = [
    "PROBE_SCHEMA_VERSION",
    "ARM_SCALED",
    "ARM_RAW",
    "ARM_POSITIVE_CONTROL",
    "ARM_PROVENANCE_CONTROL",
    "VERDICT_TARGETS_ARE_SCALED",
    "VERDICT_TARGETS_ARE_RAW",
    "VERDICT_AMBIGUOUS",
    "VERDICT_NON_FRAME_DIVERGENCE",
    "CoordinateConvention",
    "ArmResidual",
    "TrajectoryFrameMeasures",
    "ConfoundMeasures",
    "PopulationArmSummary",
    "FrameProbeOutcome",
    "FrameProbeUnavailable",
    "minimum_pairwise_separation",
    "second_difference_acceleration",
    "newtonian_acceleration_series",
    "arm_residual",
    "numerical_tolerance_for",
    "measure_trajectory",
    "measure_confounds",
    "probe_population",
    "decide_verdict",
]

PROBE_SCHEMA_VERSION = "phase46-target-frame/v1"

ARM_SCALED = "scaled_hypothesis"
ARM_RAW = "raw_hypothesis"
ARM_POSITIVE_CONTROL = "positive_control"
ARM_PROVENANCE_CONTROL = "provenance_control"

VERDICT_TARGETS_ARE_SCALED = "TARGETS_ARE_SCALED"
VERDICT_TARGETS_ARE_RAW = "TARGETS_ARE_RAW"
VERDICT_AMBIGUOUS = "VERDICT_AMBIGUOUS"
VERDICT_NON_FRAME_DIVERGENCE = "VERDICT_NON_FRAME_DIVERGENCE"

# Relative close-encounter guard: a snapshot qualifies only if its minimum
# pairwise separation exceeds this FRACTION of the trajectory's own median
# separation. It is a relative guard (no absolute physics constant) and is
# applied identically to every arm of one trajectory.
_SEPARATION_GUARD_FRACTION = 0.1
_TINY = 1e-12


@dataclass(frozen=True)
class CoordinateConvention:
    """Explicit per-arm coordinate tuple (D-03/D-05); serialized by plan 46-04."""

    position: str
    time: str
    velocity: str
    masses: str


ARM_CONVENTIONS = {
    ARM_SCALED: CoordinateConvention(
        position="r_prime_as_resident",
        time="u_eq_t_over_T",
        velocity="d2r_prime_du2_via_second_difference",
        masses="ordered_raw_as_stored",
    ),
    ARM_RAW: CoordinateConvention(
        position="resident_over_D",
        time="u_eq_t_over_T",
        velocity="d2r_prime_du2_via_second_difference",
        masses="ordered_raw_as_stored",
    ),
    ARM_POSITIVE_CONTROL: CoordinateConvention(
        position="preprocess_r_gauge",
        time="u_eq_t_parsed_over_T",
        velocity="d2r_prime_du2_via_second_difference",
        masses="preprocess_masses_ordered",
    ),
    ARM_PROVENANCE_CONTROL: CoordinateConvention(
        position="parsed_over_D",
        time="u_eq_t_parsed_over_T",
        velocity="d2r_prime_du2_via_second_difference",
        masses="parsed_file_order",
    ),
}


class FrameProbeUnavailable(Exception):
    """Raised when no verdict can be produced (e.g. empty population).

    Callers convert this to an operational failure, never a verdict.
    """


@dataclass(frozen=True)
class ArmResidual:
    """One arm's per-qualifying-snapshot relative residual summary.

    ``relative_residual`` holds ``norm(a_fd - a_newton) / clamp_min(norm(a_fd),
    tiny)`` per qualifying snapshot. ``softening`` records the force softening
    used (the verified ``pinn.physics_residual`` default, never a frame-decision
    constant).
    """

    arm: str
    median: float
    maximum: float
    relative_residual: np.ndarray
    exclusions: tuple
    finite: bool
    softening: float = float(EPS_SOFT)


@dataclass(frozen=True)
class TrajectoryFrameMeasures:
    """Per-trajectory four-arm measures + the numerics-derived tolerance.

    ``numerical_tolerance`` is a FINITE-DIFFERENCE / dtype NUMERICAL comparison
    tolerance (GAP-46-03), reported separately from any physics acceptance
    threshold; ``tolerance_floor`` and ``tolerance_fp32_increment`` persist its
    two terms separately (guardrail 3).
    """

    key: object
    arms: dict
    tolerance_floor: float
    tolerance_fp32_increment: float
    numerical_tolerance: float
    consistency: dict
    separation: dict
    exclusions: tuple
    separation_guard: float
    finite: bool


@dataclass(frozen=True)
class ConfoundMeasures:
    """Confound discriminators (D-04), cheapest boolean first."""

    key: object
    permutation_identity: bool
    permutation: tuple
    mass_diff_vs_ordered: float
    mass_diff_vs_file_order: float
    mass_convention: str
    identity_raw: bool
    identity_scaled: bool
    identity_neither: bool
    identity_max_abs_diff: dict
    com_offset_stored: np.ndarray
    com_drift_stored: np.ndarray
    com_offset_file_order: np.ndarray
    stepwise_attribution: dict
    first_diverging_step: object
    raw_residual_uncorrected: float
    raw_residual_corrected: float
    restoring_permutation: tuple


@dataclass(frozen=True)
class PopulationArmSummary:
    """Descriptive per-arm population summary (never a classification input)."""

    arm: str
    count_consistent: int
    count_separated: int
    residual_medians: tuple
    residual_maxima: tuple


@dataclass(frozen=True)
class FrameProbeOutcome:
    verdict: str
    arm_summaries: dict
    confound_register: tuple
    disagreement_keys: tuple
    rationale: dict


# ---------------------------------------------------------------------------
# Geometry and residual primitives (float64 CPU)
# ---------------------------------------------------------------------------


def _as_f64_numpy(value):
    return np.asarray(value, dtype=np.float64)


def minimum_pairwise_separation(positions):
    """Per-snapshot minimum off-diagonal pair distance (trivial geometry).

    Implemented locally (the Phase 38 probe's helper is private to a probe-local
    module); this is geometry, not the verified-clean gate math.
    """
    pos = _as_f64_numpy(positions)
    difference = pos[:, None, :, :] - pos[:, None, :, :].transpose(0, 2, 1, 3)
    # difference[t, i, j, :] = pos[t, j] - pos[t, i]
    separation = np.linalg.norm(difference, axis=-1)  # (T, 3, 3)
    n = separation.shape[-1]
    eye = np.eye(n, dtype=bool)
    separation = np.where(eye[None, :, :], np.inf, separation)
    return separation.reshape(separation.shape[0], -1).min(axis=-1)


def second_difference_acceleration(positions, times):
    """Non-uniform-grid central second difference of positions over ``times``.

    Returns ``(acceleration, interior_mask)``: ``acceleration`` is ``(Nt, 3, 3)``
    with endpoints left at zero (NOT estimated); ``interior_mask`` is ``(Nt,)``
    bool, True only at interior indices. Unit-agnostic — works identically for
    ``(r, t)`` and ``(r_prime, u)``. Requires at least 3 snapshots; fewer raises
    a typed ValueError the caller converts into a recorded exclusion.
    """
    pos = _as_f64_numpy(positions)
    t = _as_f64_numpy(times)
    n = int(t.shape[0])
    if n < 3:
        raise ValueError(
            f"second_difference_acceleration requires >= 3 snapshots; got {n}"
        )
    acceleration = np.zeros_like(pos)
    interior = np.zeros(n, dtype=bool)
    for i in range(1, n - 1):
        half_span = (t[i + 1] - t[i - 1]) / 2.0
        forward = (pos[i + 1] - pos[i]) / (t[i + 1] - t[i])
        backward = (pos[i] - pos[i - 1]) / (t[i] - t[i - 1])
        acceleration[i] = (forward - backward) / half_span
        interior[i] = True
    return acceleration, interior


def newtonian_acceleration_series(positions, masses):
    """Verified softened Newtonian force (``pinn.physics_residual``).

    A thin composition wrapper calling ``softened_acceleration`` with its locked
    default softening (``EPS_SOFT``); the force is NOT re-derived here. Callers
    MUST pass only the qualifying snapshot subset — ``softened_acceleration``
    raises on any non-finite input, so non-finite snapshots are masked out before
    this call.
    """
    pos = torch.as_tensor(_as_f64_numpy(positions), dtype=torch.float64,
                          device=torch.device("cpu"))
    m = torch.as_tensor(_as_f64_numpy(masses), dtype=torch.float64,
                        device=torch.device("cpu"))
    accel = softened_acceleration(pos, m, dtype=torch.float64,
                                  device=torch.device("cpu"))
    return accel.detach().cpu().numpy()


def _compute_qualifying(positions, times):
    """Compute the shared qualifying-snapshot mask + exclusion ledger.

    The mask combines interior-only, minimum-separation-above-guard (a fixed
    fraction of the trajectory's own median separation), and finite values. The
    SAME mask indices apply to every arm of one trajectory (D-03 symmetry).
    Returns ``(qualifying_mask, exclusions, guard_value)``.
    """
    pos = _as_f64_numpy(positions)
    t = _as_f64_numpy(times)
    n = int(t.shape[0])
    if n < 3:
        exclusions = tuple((i, "too_few_snapshots") for i in range(n))
        return np.zeros(n, dtype=bool), exclusions, 0.0
    _, interior = second_difference_acceleration(pos, t)
    finite = np.all(np.isfinite(pos), axis=(1, 2))
    sep = minimum_pairwise_separation(pos)
    interior_sep = sep[interior]
    median_sep = float(np.median(interior_sep)) if interior_sep.size else float("nan")
    guard = _SEPARATION_GUARD_FRACTION * median_sep if np.isfinite(median_sep) else 0.0
    close = sep > guard
    qualifying = interior & finite & close
    exclusions = []
    for i in range(n):
        if not bool(finite[i]):
            exclusions.append((i, "non_finite"))
        elif not bool(interior[i]):
            exclusions.append((i, "endpoint"))
        elif not bool(close[i]):
            exclusions.append((i, "close_encounter"))
    return qualifying, tuple(exclusions), float(guard)


def arm_residual(positions, times, masses, *, qualifying_mask, arm_name,
                 exclusions=()):
    """One arm's relative residual over the shared qualifying snapshots.

    ``relative_residual = norm(a_fd - a_newton) / clamp_min(norm(a_fd), tiny)``
    per qualifying snapshot; ``median`` / ``maximum`` over qualifying snapshots.
    The qualifying mask is supplied by the caller (computed once per trajectory).
    """
    pos = _as_f64_numpy(positions)
    t = _as_f64_numpy(times)
    qual_idx = np.where(np.asarray(qualifying_mask, dtype=bool))[0]
    # ``exclusions`` is the shared per-trajectory qualifying-snapshot ledger
    # (computed once in ``_compute_qualifying``); the SAME indices exclude the
    # same snapshots in every arm of one trajectory (D-03 symmetry), so each
    # ArmResidual carries an identical, non-empty-when-endpoints-exist ledger.
    if qual_idx.size == 0 or pos.shape[0] < 3:
        return ArmResidual(
            arm=arm_name, median=float("nan"), maximum=float("nan"),
            relative_residual=np.empty(0, dtype=np.float64),
            exclusions=exclusions, finite=False,
        )
    accel_fd, _ = second_difference_acceleration(pos, t)
    a_newton = newtonian_acceleration_series(pos[qual_idx], masses)
    fd_qual = accel_fd[qual_idx]
    diff = fd_qual - a_newton
    numerator = np.linalg.norm(diff.reshape(diff.shape[0], -1), axis=-1)
    denominator = np.clip(
        np.linalg.norm(fd_qual.reshape(fd_qual.shape[0], -1), axis=-1), _TINY, None
    )
    relative = numerator / denominator
    finite = bool(np.all(np.isfinite(relative)))
    return ArmResidual(
        arm=arm_name,
        median=float(np.median(relative)),
        maximum=float(np.max(relative)),
        relative_residual=relative,
        exclusions=exclusions,
        finite=finite,
    )


def numerical_tolerance_for(control_arms, fp32_roundtrip_probe):
    """The D-06 tolerance, EXACTLY per GAP-46-03 Option A (see module docstring).

    Returns ``(finite_difference_floor, fp32_roundtrip_increment,
    numerical_tolerance)`` — the three terms persisted SEPARATELY (guardrail 3).
    ``fp32_roundtrip_probe`` is a callable returning the measured, nonnegative
    fp32 round-trip residual increment. No multiplicative safety constant, no
    imported threshold, no physics quantity enters. A non-positive / non-finite
    tolerance fails closed (guardrail 5) by returning ``nan`` as the tolerance.
    """
    medians = [float(arm.median) for arm in control_arms]
    if not medians or any(not np.isfinite(m) for m in medians):
        return (float("nan"), float("nan"), float("nan"))
    floor = max(medians)
    increment = float(fp32_roundtrip_probe())
    if not np.isfinite(increment):
        return (floor, float("nan"), float("nan"))
    increment = max(0.0, increment)
    tolerance = floor + increment
    if not np.isfinite(tolerance) or not (tolerance > 0.0):
        return (floor, increment, float("nan"))
    return (floor, increment, float(tolerance))


def _consistent(median, tolerance):
    """Boundary direction pinned: residual == tolerance is consistent (<=)."""
    if not np.isfinite(median) or not np.isfinite(tolerance):
        return False
    return bool(median <= tolerance)


def _separated(median, tolerance):
    """Separation requires the opposing arm STRICTLY above tolerance (>)."""
    if not np.isfinite(median) or not np.isfinite(tolerance):
        return False
    return bool(median > tolerance)


def measure_trajectory(key, resident, controls):
    """Measure one trajectory symmetrically under both hypotheses + both controls.

    ``resident`` is ``(times_res, positions_res, velocities_res, masses_record)``
    read ONLY through the StageIndex accessor surface; ``times_res`` is the raw
    native snapshot time (the model-facing seam), so each arm differences over
    ``u = times_res / T``. ``controls`` is ``(times_parsed, positions_parsed,
    velocities_parsed, masses_parsed_file_order, pre)`` or ``None`` (in which case
    the control arms and tolerance are unavailable and the trajectory fails
    closed).
    """
    times_res = _as_f64_numpy(resident[0])
    positions_res = _as_f64_numpy(resident[1])
    masses_record = _as_f64_numpy(resident[3])
    D = float(D_CHARACTERISTIC_LENGTH)
    T = float(T_CHARACTERISTIC_TIME)

    qualifying, exclusions, guard = _compute_qualifying(positions_res, times_res)
    u_res = times_res / T

    arms = {
        ARM_SCALED: arm_residual(positions_res, u_res, masses_record,
                                 qualifying_mask=qualifying, arm_name=ARM_SCALED,
                                 exclusions=exclusions),
        ARM_RAW: arm_residual(positions_res / D, u_res, masses_record,
                              qualifying_mask=qualifying, arm_name=ARM_RAW,
                              exclusions=exclusions),
    }

    floor = float("nan")
    increment = float("nan")
    tolerance = float("nan")
    if controls is not None:
        times_parsed = _as_f64_numpy(controls[0])
        positions_parsed = _as_f64_numpy(controls[1])
        masses_parsed = _as_f64_numpy(controls[3])
        pre = controls[4]
        u_parsed = times_parsed / T
        positive = arm_residual(_as_f64_numpy(pre.r_gauge), u_parsed,
                                _as_f64_numpy(pre.masses_ordered),
                                qualifying_mask=qualifying,
                                arm_name=ARM_POSITIVE_CONTROL,
                                exclusions=exclusions)
        provenance = arm_residual(positions_parsed / D, u_parsed, masses_parsed,
                                  qualifying_mask=qualifying,
                                  arm_name=ARM_PROVENANCE_CONTROL,
                                  exclusions=exclusions)
        arms[ARM_POSITIVE_CONTROL] = positive
        arms[ARM_PROVENANCE_CONTROL] = provenance

        def _fp32_roundtrip_increment():
            pos_f32 = positions_parsed.astype(np.float32).astype(np.float64) / D
            fp32_prov = arm_residual(pos_f32, u_parsed, masses_parsed,
                                     qualifying_mask=qualifying,
                                     arm_name=ARM_PROVENANCE_CONTROL)
            if not fp32_prov.finite or not provenance.finite:
                return float("nan")
            return fp32_prov.median - provenance.median

        floor, increment, tolerance = numerical_tolerance_for(
            [positive, provenance], _fp32_roundtrip_increment
        )

    consistency = {name: _consistent(arm.median, tolerance)
                   for name, arm in arms.items()}
    scaled_median = arms[ARM_SCALED].median
    raw_median = arms[ARM_RAW].median
    # separation[X] = "arm X's OWN residual is strictly above tolerance". This is
    # what decide_verdict Rule 4 (all_scaled_separated) and PopulationArmSummary
    # (count_separated per arm) both consume; keying it on the opposing arm made
    # TARGETS_ARE_RAW unreachable for a genuine raw population.
    separation = {
        ARM_SCALED: _separated(scaled_median, tolerance),
        ARM_RAW: _separated(raw_median, tolerance),
    }
    finite = bool(
        np.isfinite(tolerance)
        and all(arm.finite for arm in arms.values())
    )
    return TrajectoryFrameMeasures(
        key=key,
        arms=arms,
        tolerance_floor=floor,
        tolerance_fp32_increment=increment,
        numerical_tolerance=tolerance,
        consistency=consistency,
        separation=separation,
        exclusions=exclusions,
        separation_guard=guard,
        finite=finite,
    )


# ---------------------------------------------------------------------------
# Confound discriminators (D-04)
# ---------------------------------------------------------------------------


def _fp32_roundtrip(array):
    return np.asarray(array, dtype=np.float64).astype(np.float32).astype(np.float64)


def _fp32_compare(resident, candidate):
    """Max-abs difference of resident against an fp32-cast candidate."""
    resident = _as_f64_numpy(resident)
    candidate_f32 = _fp32_roundtrip(candidate)
    return float(np.max(np.abs(resident - candidate_f32))) if resident.size else 0.0


def _fp32_threshold(candidate):
    magnitude = float(np.max(np.abs(_as_f64_numpy(candidate)))) if np.size(candidate) else 1.0
    return np.finfo(np.float32).eps * max(magnitude, 1.0)


def _com_series(positions, masses):
    masses = _as_f64_numpy(masses)
    positions = _as_f64_numpy(positions)
    total = float(masses.sum())
    return (masses.reshape(1, 3, 1) * positions).sum(axis=1) / total


def _linear_drift(com, times):
    com = _as_f64_numpy(com)
    t = _as_f64_numpy(times)
    if t.shape[0] < 2:
        return np.zeros(3, dtype=np.float64)
    span = t[-1] - t[0]
    if span == 0:
        return np.zeros(3, dtype=np.float64)
    return (com[-1] - com[0]) / span


def measure_confounds(key, resident, controls):
    """Confound discriminators, cheapest boolean first (per the 46-GAPS routing).

    Distinguishes a pure D-scale mismatch from body-permutation, COM/boost,
    rotation-gauge, and metadata-pairing mismatches, including a
    permutation-corrected re-evaluation of the raw arm so mass-pairing damage is
    attributable (D-04).
    """
    times_res = _as_f64_numpy(resident[0])
    positions_res = _as_f64_numpy(resident[1])
    velocities_res = _as_f64_numpy(resident[2])
    masses_record = _as_f64_numpy(resident[3])

    times_parsed = _as_f64_numpy(controls[0])
    positions_parsed = _as_f64_numpy(controls[1])
    velocities_parsed = _as_f64_numpy(controls[2])
    masses_parsed = _as_f64_numpy(controls[3])
    pre = controls[4]
    D = float(pre.D)
    T = float(pre.T)

    # 1. Permutation (cheapest boolean).
    permutation = tuple(int(i) for i in np.asarray(pre.permutation))
    permutation_identity = bool((np.asarray(pre.permutation) == np.arange(3)).all())

    # 2. Mass pairing.
    mass_diff_vs_ordered = float(np.max(np.abs(masses_record - _as_f64_numpy(pre.masses_ordered))))
    mass_diff_vs_file_order = float(np.max(np.abs(masses_record - masses_parsed)))
    if mass_diff_vs_ordered <= mass_diff_vs_file_order:
        mass_convention = "ordered"
    else:
        mass_convention = "file_order"

    # 3. Identity checks (fp32-round-trip tolerance).
    pos_diff_raw = _fp32_compare(positions_res, positions_parsed)
    vel_diff_raw = _fp32_compare(velocities_res, velocities_parsed)
    pos_diff_scaled = _fp32_compare(positions_res, pre.r_gauge)
    vel_diff_scaled = _fp32_compare(velocities_res, pre.v_gauge)
    pos_tol_raw = _fp32_threshold(positions_parsed)
    vel_tol_raw = _fp32_threshold(velocities_parsed)
    pos_tol_scaled = _fp32_threshold(pre.r_gauge)
    vel_tol_scaled = _fp32_threshold(pre.v_gauge)
    identity_raw = bool(pos_diff_raw <= pos_tol_raw and vel_diff_raw <= vel_tol_raw)
    identity_scaled = bool(pos_diff_scaled <= pos_tol_scaled and vel_diff_scaled <= vel_tol_scaled)
    identity_neither = bool(not identity_raw and not identity_scaled)
    identity_max_abs_diff = {
        "positions_vs_parsed": pos_diff_raw,
        "velocities_vs_parsed": vel_diff_raw,
        "positions_vs_r_gauge": pos_diff_scaled,
        "velocities_vs_v_gauge": vel_diff_scaled,
    }

    # 4. COM measures under stored and file-order pairings.
    com_stored = _com_series(positions_res, masses_record)
    com_offset_stored = com_stored[0]
    com_drift_stored = _linear_drift(com_stored, times_res)
    com_file_order = _com_series(positions_res, masses_parsed)
    com_offset_file_order = com_file_order[0]

    # 5. Stepwise transform attribution (rebuild locked-pipeline intermediates).
    R_COM0 = _as_f64_numpy(pre.R_COM0)
    V_COM = _as_f64_numpy(pre.V_COM)
    r_bar = positions_parsed - R_COM0[None, None, :] - V_COM[None, None, :] * times_parsed[:, None, None]
    r_bar_perm = r_bar[:, list(permutation), :]
    r_rot = np.einsum("ij,tbj->tbi", _as_f64_numpy(pre.R0), r_bar_perm)
    r_scaled = r_rot / D
    stepwise_attribution = {
        "com_recenter_boost": _fp32_compare(positions_res, r_bar),
        "plus_permutation": _fp32_compare(positions_res, r_bar_perm),
        "plus_rotation": _fp32_compare(positions_res, r_rot),
        "plus_scale": _fp32_compare(positions_res, r_scaled),
    }
    # A resident that already matches the conformant scaled output (``r_scaled``)
    # has NO diverging transform — it differs from every earlier intermediate
    # only because the full pipeline was applied. Attribute only when the
    # resident does not match the final locked output; otherwise a fully
    # conformant scaled resident would falsely register a divergence and block
    # the TARGETS_ARE_SCALED route (Rule 3 needs an empty confound register).
    first_diverging_step = None
    if _fp32_compare(positions_res, r_scaled) > _fp32_threshold(r_scaled):
        for step_name in ("com_recenter_boost", "plus_permutation", "plus_rotation", "plus_scale"):
            candidate = {"com_recenter_boost": r_bar, "plus_permutation": r_bar_perm,
                         "plus_rotation": r_rot, "plus_scale": r_scaled}[step_name]
            if stepwise_attribution[step_name] > _fp32_threshold(candidate):
                first_diverging_step = step_name
                break

    # 6. Corrected re-evaluation of the raw arm (permutation-corrected masses).
    u_res = times_res / T
    qualifying, _, _ = _compute_qualifying(positions_res, times_res)
    raw_uncorrected = arm_residual(positions_res / D, u_res, masses_record,
                                   qualifying_mask=qualifying, arm_name=ARM_RAW)
    inverse_permutation = np.argsort(np.asarray(pre.permutation))
    masses_corrected = masses_record[inverse_permutation]
    raw_corrected = arm_residual(positions_res / D, u_res, masses_corrected,
                                 qualifying_mask=qualifying, arm_name=ARM_RAW)
    restoring_permutation = tuple(int(i) for i in inverse_permutation)

    return ConfoundMeasures(
        key=key,
        permutation_identity=permutation_identity,
        permutation=permutation,
        mass_diff_vs_ordered=mass_diff_vs_ordered,
        mass_diff_vs_file_order=mass_diff_vs_file_order,
        mass_convention=mass_convention,
        identity_raw=identity_raw,
        identity_scaled=identity_scaled,
        identity_neither=identity_neither,
        identity_max_abs_diff=identity_max_abs_diff,
        com_offset_stored=com_offset_stored,
        com_drift_stored=com_drift_stored,
        com_offset_file_order=com_offset_file_order,
        stepwise_attribution=stepwise_attribution,
        first_diverging_step=first_diverging_step,
        raw_residual_uncorrected=raw_uncorrected.median,
        raw_residual_corrected=raw_corrected.median,
        restoring_permutation=restoring_permutation,
    )


# ---------------------------------------------------------------------------
# Population traversal + fail-closed verdict
# ---------------------------------------------------------------------------


def probe_population(population, resident_reader, control_reader):
    """Sort by RecordKey, measure every trajectory, and account for the population.

    ``population`` is a sequence of ``(key, membership)`` pairs, where
    ``membership`` maps a manifest label to a split name. Readers are injected
    callables so tests stay dataset-free (D-24) and the CLI (46-04) supplies real
    ones; ``resident_reader(key)`` dereferences ONLY the StageIndex accessor
    surface. Returns ``(results, accounting)``.
    """
    sorted_population = sorted(population, key=lambda item: item[0])
    results = []
    exclusion_counts = {}
    key_membership = {}
    for key, membership in sorted_population:
        key_membership[key] = dict(membership)
        resident = resident_reader(key)
        controls = control_reader(key)
        measures = measure_trajectory(key, resident, controls)
        confounds = measure_confounds(key, resident, controls)
        results.append((measures, confounds))
        for _, reason in measures.exclusions:
            exclusion_counts[reason] = exclusion_counts.get(reason, 0) + 1

    counts_per_split_per_manifest = {}
    for key, membership in sorted_population:
        for manifest_label, split_name in membership.items():
            per_split = counts_per_split_per_manifest.setdefault(manifest_label, {})
            per_split[split_name] = per_split.get(split_name, 0) + 1

    accounting = {
        "sorted_keys": [key for key, _ in sorted_population],
        "counts_per_split_per_manifest": counts_per_split_per_manifest,
        "exclusion_counts": exclusion_counts,
        "key_membership": key_membership,
    }
    return results, accounting


def _winning_arm(measures):
    scaled = measures.consistency.get(ARM_SCALED, False)
    raw = measures.consistency.get(ARM_RAW, False)
    if scaled and raw:
        return "conflicted"
    if scaled:
        return "scaled"
    if raw:
        return "raw"
    return "neither"


def decide_verdict(measures, accounting):
    """Classify into exactly one of four fail-closed verdicts (D-06).

    Rules, in order: (1) empty population raises FrameProbeUnavailable; (2) any
    non-finite measure, any empty split subgroup, or train/validation disagreement
    -> VERDICT_AMBIGUOUS; (3) VERDICT_TARGETS_ARE_SCALED requires every trajectory
    scaled-consistent AND raw-separated AND identity_scaled AND empty confound
    register (the ONLY route to D-08); (4) VERDICT_TARGETS_ARE_RAW requires every
    trajectory identity_raw AND raw-consistent under corrected pairing AND
    scaled-separated; (5) VERDICT_NON_FRAME_DIVERGENCE when identity is unanimous
    for neither control but attribution names the diverging transform; (6) else
    VERDICT_AMBIGUOUS. Outcomes 4, 5, 6 all route to the D-09 owner branch.
    """
    if not measures:
        raise FrameProbeUnavailable("empty population: no verdict from nothing")

    key_membership = accounting.get("key_membership", {})
    counts_per_split = accounting.get("counts_per_split_per_manifest", {})

    # Per-arm population summaries (descriptive only).
    arm_summaries = {}
    for arm_name in (ARM_SCALED, ARM_RAW, ARM_POSITIVE_CONTROL, ARM_PROVENANCE_CONTROL):
        consistent = separated = 0
        medians = []
        maxima = []
        for traj, _ in measures:
            arm = traj.arms.get(arm_name)
            if arm is None:
                continue
            if traj.consistency.get(arm_name, False):
                consistent += 1
            if traj.separation.get(arm_name, False):
                separated += 1
            medians.append(arm.median)
            maxima.append(arm.maximum)
        arm_summaries[arm_name] = PopulationArmSummary(
            arm=arm_name, count_consistent=consistent, count_separated=separated,
            residual_medians=tuple(medians), residual_maxima=tuple(maxima),
        )

    # Confound register: every non-identity permutation / mass mismatch / gauge
    # attribution.
    confound_register = []
    for traj, conf in measures:
        if not conf.permutation_identity:
            confound_register.append(("permutation", conf.key, conf.permutation))
        if conf.mass_convention != "ordered":
            confound_register.append(("mass_pairing", conf.key, conf.mass_convention))
        if conf.first_diverging_step is not None:
            confound_register.append(("gauge_attribution", conf.key, conf.first_diverging_step))

    # Rule 2: non-finite, empty split subgroup, or train/validation disagreement.
    offending = []
    for traj, _ in measures:
        if not traj.finite:
            offending.append(traj.key)
    for manifest_label, per_split in counts_per_split.items():
        for split_name in ("train", "validation"):
            if per_split.get(split_name, 0) == 0:
                offending.append(("empty_split", manifest_label, split_name))

    winners_by_split = {}
    for traj, _ in measures:
        membership = key_membership.get(traj.key, {})
        winner = _winning_arm(traj)
        for manifest_label, split_name in membership.items():
            winners_by_split.setdefault(split_name, set()).add(winner)
    train_winners = winners_by_split.get("train", set())
    validation_winners = winners_by_split.get("validation", set())
    disagreement = bool(
        train_winners and validation_winners and train_winners != validation_winners
    )
    if disagreement:
        for traj, _ in measures:
            offending.append(traj.key)

    if offending or disagreement:
        return FrameProbeOutcome(
            verdict=VERDICT_AMBIGUOUS, arm_summaries=arm_summaries,
            confound_register=tuple(confound_register),
            disagreement_keys=tuple(offending),
            rationale={"rule": 2, "offending": [str(k) for k in offending],
                       "disagreement": disagreement},
        )

    all_winners = {_winning_arm(traj) for traj, _ in measures}
    all_identity_scaled = all(conf.identity_scaled for _, conf in measures)
    all_identity_raw = all(conf.identity_raw for _, conf in measures)
    all_identity_neither = all(conf.identity_neither for _, conf in measures)
    all_scaled_separated = all(traj.separation.get(ARM_SCALED, False) for traj, _ in measures)
    all_raw_corrected_consistent = all(
        np.isfinite(conf.raw_residual_corrected)
        and conf.raw_residual_corrected <= traj.numerical_tolerance
        for traj, conf in measures
    )

    # Rule 3: TARGETS_ARE_SCALED — the only D-08 route.
    if (all_winners == {"scaled"} and all_identity_scaled
            and not confound_register):
        return FrameProbeOutcome(
            verdict=VERDICT_TARGETS_ARE_SCALED, arm_summaries=arm_summaries,
            confound_register=(), disagreement_keys=(),
            rationale={"rule": 3, "route": "D-08"},
        )

    # Rule 4: TARGETS_ARE_RAW.
    if (all_identity_raw and all_raw_corrected_consistent and all_scaled_separated):
        return FrameProbeOutcome(
            verdict=VERDICT_TARGETS_ARE_RAW, arm_summaries=arm_summaries,
            confound_register=tuple(confound_register), disagreement_keys=(),
            rationale={"rule": 4, "route": "D-09"},
        )

    # Rule 5: VERDICT_NON_FRAME_DIVERGENCE.
    if all_identity_neither and any(conf.first_diverging_step is not None
                                    for _, conf in measures):
        return FrameProbeOutcome(
            verdict=VERDICT_NON_FRAME_DIVERGENCE, arm_summaries=arm_summaries,
            confound_register=tuple(confound_register), disagreement_keys=(),
            rationale={"rule": 5, "route": "D-09"},
        )

    # Rule 6: fail closed.
    return FrameProbeOutcome(
        verdict=VERDICT_AMBIGUOUS, arm_summaries=arm_summaries,
        confound_register=tuple(confound_register), disagreement_keys=(),
        rationale={"rule": 6, "route": "D-09"},
    )
