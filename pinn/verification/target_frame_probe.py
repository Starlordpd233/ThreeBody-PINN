"""CONF-01 / RG-01 target-frame probe — train-free residual on stored targets.

This module is the CONF-01 measurement core (Phase 46, plan 46-02). It answers
RG-02's question — are the exact stored positions consumed as training targets
the raw ``r`` or the locked ``r' = r/D``? — by MEASURING the resident
``StageIndex`` surface under two symmetric hypotheses with two control arms
(D-01, D-03), never by asserting a code-inspection suspicion.

Motivating observation (NOT the verdict): the residency path stores
``parsed_brutus.positions`` (``pinn/data/adapter.py:863,925-926,938``). Code
inspection alone does not set the verdict (D-01/D-04); the verdict derives only
from measured residual and identity evidence produced here. Plan 46-04 added
manifest-parametric population resolution (``resolve_probe_population``), the
deterministic D-05 evidence layer (``render_evidence_payload`` /
``write_frame_probe_evidence``), and the ``python -m
pinn.verification.target_frame_probe`` CLI; the one real evidence run and the
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

import argparse
import collections
import datetime as dt
import hashlib
import json
import math
import subprocess
import sys
import warnings
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np
import torch

from pinn.constants import D_CHARACTERISTIC_LENGTH, T_CHARACTERISTIC_TIME
from pinn.data.adapter import (
    BRUTUS_FOLDER_TABLE,
    BRUTUS_SUBDIR,
    DEFAULT_BLACKLIST_NAME,
    AdmittedSetAdapter,
    EvidenceRedactionError,
    parse_brutus_file,
    record_key_from_brutus,
)
from pinn.data.preprocessing import preprocess_trajectory
from pinn.data.splits import SplitManifest, StageIndex
from pinn.data.types import StageLabel
from pinn.physics_residual import EPS_SOFT, softened_acceleration
from pinn.training.atomic_io import atomic_write_text

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
    "ProbePopulation",
    "ManifestIdentity",
    "EvidenceProvenance",
    "FrameProbeRun",
    "POPULATION_RULE",
    "TOLERANCE_DERIVATION",
    "minimum_pairwise_separation",
    "second_difference_acceleration",
    "newtonian_acceleration_series",
    "arm_residual",
    "numerical_tolerance_for",
    "measure_trajectory",
    "measure_confounds",
    "probe_population",
    "decide_verdict",
    "resolve_probe_population",
    "render_evidence_payload",
    "render_summary_markdown",
    "write_frame_probe_evidence",
    "main",
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


# ---------------------------------------------------------------------------
# Population resolution from explicit split manifests (46-04; D-02, D-16)
# ---------------------------------------------------------------------------

_REPO_ROOT = Path(__file__).resolve().parents[2]
_DEFAULT_EVIDENCE_ROOT = (
    _REPO_ROOT / ".planning" / "phases"
    / "46-frame-resolution-gate-aligned-validation" / "evidence" / "target-frame"
)

# JSON-safe string sentinels — the phase-wide convention shared with
# ``pinn.evaluate._json_safe_float`` and ``validation_gate.json_safe_float``.
_NAN_SENTINEL = "NaN"
_POS_INF_SENTINEL = "Infinity"
_NEG_INF_SENTINEL = "-Infinity"

# The exact D-02 population rule, recorded in the evidence payload so the
# committed artifact is self-describing (quoted verbatim by plan 46-06).
POPULATION_RULE = (
    "A Stage-0 record is eligible iff its RecordKey appears in the "
    "train-or-validation view of EVERY supplied manifest; a record whose "
    "physical key is in ANY supplied manifest's test partition is excluded, "
    "with the exclusion counted and attributed as test_under_<label>."
)

# The tolerance derivation formula (46-02 SUMMARY; GAP-46-03 Option A), stated
# in the evidence SEPARATELY from any physics acceptance threshold (D-06).
TOLERANCE_DERIVATION = (
    "numerical_tolerance = tolerance_floor + tolerance_fp32_increment, where "
    "tolerance_floor = max(positive_control_median_residual, "
    "provenance_control_median_residual) under the shared qualifying-snapshot "
    "mask and tolerance_fp32_increment = max(0.0, measured fp32-cast-then-"
    "float64-restored provenance-control median residual increase). No safety "
    "multiplier, population-fitted percentile, imported physics threshold, "
    "Phase 38 threshold, or theory-predicted ~21x / ~99x separation enters "
    "(GAP-46-03 Option A guardrails 1-3)."
)


@dataclass(frozen=True)
class ProbePopulation:
    """Resolved eligible population (D-02) — train/validation memberships only.

    Carries NO withheld-split view: the test partition enters only as a
    physical-key set read from each manifest's payload
    (``SplitManifest.physical_keys("test")``), used for the exclusion ledger,
    and is never materialized as a ``StageIndex`` (D-16).

    ``exclusion_ledger`` maps each reason (``test_under_<label>``) to the sorted
    tuple of excluded :class:`PhysicalKey` values. ``first_manifest_label``
    records the routing label the resident reader uses; memberships may differ
    across manifests, but every view reads the same underlying residency, so
    the choice affects index routing only.
    """

    eligible: tuple
    membership: dict
    counts_per_split_per_manifest: dict
    exclusion_ledger: dict
    first_manifest_label: object


@dataclass(frozen=True)
class ManifestIdentity:
    """One supplied manifest's evidence identity (repo-relative path + hash)."""

    label: str
    path: str
    sha256: str


@dataclass(frozen=True)
class EvidenceProvenance:
    """D-05 provenance block.

    ``data_root_source`` is the adapter's resolution-source LABEL
    (``"explicit"`` / ``"env:GSD_DATA_ROOT"`` / ``"git_common_dir_default"``) —
    NEVER the resolved absolute path (T-46-04-02). ``probe_invocation`` is the
    argv with any absolute paths reduced to repo-relative or basename form.
    """

    repo_commit: str
    manifests: tuple
    blacklist_sha256: str
    data_root_source: str
    dtype: str
    device: str
    math: str
    torch_version: str
    probe_invocation: tuple


@dataclass(frozen=True)
class FrameProbeRun:
    """The classified outcome plus the per-trajectory evidence it summarizes."""

    outcome: FrameProbeOutcome
    results: tuple
    accounting: dict
    population: ProbePopulation


def resolve_probe_population(stage0_keys_by_manifest, test_physical_keys_by_manifest):
    """Resolve the eligible Stage-0 population from explicit split manifests.

    Pure function over already-loaded data (tests stay dataset-free, D-24):
    ``stage0_keys_by_manifest`` maps each manifest label to its
    ``{"train": ..., "validation": ...}`` sorted Stage-0 RecordKey views, and
    ``test_physical_keys_by_manifest`` maps each label to the manifest's
    test-partition PHYSICAL-key set — read from the manifest payload
    (``SplitManifest.physical_keys``), NEVER from a StageIndex (the fence bans
    constructing or reading a withheld-split index, and key-set arithmetic on
    the manifest payload carries no trajectory data).

    Rule (D-02 under multiple frozen manifests): a RecordKey is ELIGIBLE iff it
    appears in the train-or-validation view of EVERY supplied manifest and its
    physical key is in NO supplied manifest's test partition; every physical
    key in ANY supplied manifest's test partition is EXCLUDED with the reason
    ``test_under_<label>`` attributed to that manifest. With a single manifest
    this degenerates to that manifest's train+validation Stage-0 population —
    the machinery is invariant to how many manifests 46-06 supplies, so the
    population-instantiation decision stays a recorded 46-06 input, not a code
    assumption. Empty eligibility raises :class:`FrameProbeUnavailable`.
    """
    labels = list(stage0_keys_by_manifest.keys())
    if not labels:
        raise FrameProbeUnavailable(
            "resolve_probe_population: no manifests supplied")
    test_sets = {
        label: frozenset(test_physical_keys_by_manifest.get(label, ()))
        for label in labels
    }
    test_union = frozenset().union(*test_sets.values()) if test_sets else frozenset()
    membership = {}
    for label in labels:
        views = stage0_keys_by_manifest[label]
        for split_name in ("train", "validation"):
            for key in views.get(split_name, ()):
                membership.setdefault(key, {})[label] = split_name
    eligible = tuple(sorted(
        key for key, key_membership in membership.items()
        if len(key_membership) == len(labels)
        and key.physical_key not in test_union
    ))
    if not eligible:
        raise FrameProbeUnavailable(
            f"resolve_probe_population: empty eligible population across "
            f"{len(labels)} manifest(s)")
    exclusion_ledger = {
        f"test_under_{label}": tuple(sorted(physical_keys))
        for label, physical_keys in sorted(test_sets.items())
        if physical_keys
    }
    counts = {}
    for label in labels:
        per_split = {"train": 0, "validation": 0}
        for key in eligible:
            per_split[membership[key][label]] += 1
        counts[label] = per_split
    return ProbePopulation(
        eligible=eligible,
        membership={key: dict(membership[key]) for key in eligible},
        counts_per_split_per_manifest=counts,
        exclusion_ledger=exclusion_ledger,
        first_manifest_label=labels[0],
    )


# ---------------------------------------------------------------------------
# CLI-side reader builders (46-04; exercised over the real corpus by 46-06)
# ---------------------------------------------------------------------------


def _build_resident_reader(train_index, validation_index, membership):
    """Resident-reader for the CLI — the exact model-facing surface (D-01).

    ``membership`` maps each eligible RecordKey to its split name under the
    FIRST supplied manifest label (both views read the same underlying
    residency, so the routing choice affects index routing only — it is
    recorded in the evidence via ``ProbePopulation.first_manifest_label``).
    Returns a callable mapping key to ``(times, positions, velocities, masses,
    ic13)``: the snapshot accessors of the correct split's StageIndex plus the
    record's stored mass vector and ic13 via ``.get(key)``.
    """

    def read(key):
        split_name = membership[key]
        index = train_index if split_name == "train" else validation_index
        record = index.get(key)
        return (
            index.snapshot_times(key),
            index.snapshot_positions(key),
            index.snapshot_velocities(key),
            record.masses,
            record.ic13,
        )

    return read


def _build_control_reader(data_root, eligible_physical_keys, *, chunk_size=64):
    """Control-reader for the CLI — the D-03 provenance/positive-control supply
    line explicitly authorized by D-01 ("parsed corpus arrays and the output of
    preprocess_trajectory are provenance and positive-control arms"). It is NOT
    a second training-data path: nothing downstream of the probe may consume it.

    Corpus files are located through the adapter module's own public seams —
    ``sorted(BRUTUS_FOLDER_TABLE.items())`` iteration with the
    ``data_root / BRUTUS_SUBDIR / folder`` ``*.txt`` glob exactly as the
    adapter's scan does, ``record_key_from_brutus`` for identity, and
    ``parse_brutus_file(path, root=data_root)`` for parsing (containment
    enforced by the adapter's own ``resolve_within_root``) — no second
    path-mapping convention is invented. Each eligible key's parsed float64
    arrays are transformed once by ``preprocess_trajectory``.

    Streams per key: at most ``chunk_size`` parsed controls are held at once
    (FIFO eviction); the whole corpus is never cached.
    """
    if isinstance(chunk_size, bool) or not isinstance(chunk_size, int) or chunk_size <= 0:
        raise ValueError(f"chunk_size must be a positive int; got {chunk_size!r}")
    root = Path(data_root)
    eligible = frozenset(eligible_physical_keys)
    paths = {}
    for folder, (_variant, _fidelity) in sorted(BRUTUS_FOLDER_TABLE.items()):
        folder_dir = root / BRUTUS_SUBDIR / folder
        files = sorted(folder_dir.glob("*.txt")) if folder_dir.is_dir() else []
        for path in files:
            key = record_key_from_brutus(folder, path.name)
            if key.physical_key in eligible:
                paths[key] = path
    cache = collections.OrderedDict()

    def read(key):
        cached = cache.get(key)
        if cached is not None:
            return cached
        parsed = parse_brutus_file(paths[key], root=root)
        pre = preprocess_trajectory(parsed.times, parsed.positions,
                                    parsed.velocities, parsed.masses)
        controls = (parsed.times, parsed.positions, parsed.velocities,
                    parsed.masses, pre)
        cache[key] = controls
        while len(cache) > chunk_size:
            cache.popitem(last=False)
        return controls

    return read


# ---------------------------------------------------------------------------
# D-05 evidence payload rendering (46-04; deterministic, non-finite-safe)
# ---------------------------------------------------------------------------


def _json_safe(value):
    """Recursively encode for deterministic, non-finite-safe JSON (D-05/D-18).

    Non-finite floats map to string sentinels (``"NaN"`` / ``"Infinity"`` /
    ``"-Infinity"``) — preserved, never dropped or nulled (CONF-01 precision
    edge). numpy arrays/scalars and tuples convert to JSON-native shapes.
    """
    if isinstance(value, float):
        if math.isnan(value):
            return _NAN_SENTINEL
        if math.isinf(value):
            return _POS_INF_SENTINEL if value > 0 else _NEG_INF_SENTINEL
        return value
    if isinstance(value, bool) or value is None or isinstance(value, (int, str)):
        return value
    if isinstance(value, np.floating):
        return _json_safe(float(value))
    if isinstance(value, np.integer):
        return int(value)
    if isinstance(value, np.ndarray):
        return _json_safe(value.tolist())
    if isinstance(value, dict):
        return {str(key): _json_safe(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_json_safe(item) for item in value]
    return str(value)


def _key_triple(key):
    return {"variant": key.variant, "fidelity": key.fidelity, "id": int(key.id)}


def _physical_key_pair(physical_key):
    return {"variant": physical_key.variant, "id": int(physical_key.id)}


def _distribution(values):
    """Descriptive distribution fields (never a classification input, D-06/D-14)."""
    values = np.asarray(values, dtype=np.float64)
    if values.size == 0:
        return {"count": 0, "median": float("nan"), "q25": float("nan"),
                "q75": float("nan"), "max": float("nan")}
    # NaN propagates honestly into the sentinels; the warning filter only keeps
    # numpy's reduce-over-NaN notices out of the operator's stderr.
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", RuntimeWarning)
        return {
            "count": int(values.size),
            "median": float(np.median(values)),
            "q25": float(np.quantile(values, 0.25)),
            "q75": float(np.quantile(values, 0.75)),
            "max": float(np.max(values)),
        }


def _trajectory_row(measures, confounds, membership):
    row = {
        "key": _key_triple(measures.key),
        "membership": dict(membership),
        "arms": {
            arm_name: {"median": arm.median, "maximum": arm.maximum,
                       "softening": arm.softening}
            for arm_name, arm in sorted(measures.arms.items())
        },
        "tolerance_floor": measures.tolerance_floor,
        "tolerance_fp32_increment": measures.tolerance_fp32_increment,
        "numerical_tolerance": measures.numerical_tolerance,
        "consistency": dict(measures.consistency),
        "separation": dict(measures.separation),
        "exclusions": [[int(index), str(reason)]
                       for index, reason in measures.exclusions],
        "separation_guard": measures.separation_guard,
        "finite": bool(measures.finite),
        "confounds": {
            "permutation_identity": bool(confounds.permutation_identity),
            "permutation": list(confounds.permutation),
            "mass_diff_vs_ordered": confounds.mass_diff_vs_ordered,
            "mass_diff_vs_file_order": confounds.mass_diff_vs_file_order,
            "mass_convention": confounds.mass_convention,
            "identity_raw": bool(confounds.identity_raw),
            "identity_scaled": bool(confounds.identity_scaled),
            "identity_neither": bool(confounds.identity_neither),
            "identity_max_abs_diff": dict(confounds.identity_max_abs_diff),
            "com_offset_stored": confounds.com_offset_stored,
            "com_drift_stored": confounds.com_drift_stored,
            "com_offset_file_order": confounds.com_offset_file_order,
            "stepwise_attribution": dict(confounds.stepwise_attribution),
            "first_diverging_step": confounds.first_diverging_step,
            "raw_residual_uncorrected": confounds.raw_residual_uncorrected,
            "raw_residual_corrected": confounds.raw_residual_corrected,
            "restoring_permutation": list(confounds.restoring_permutation),
        },
    }
    return _json_safe(row)


def render_evidence_payload(run, provenance):
    """Render the D-05 machine-readable evidence dict (deterministic).

    Every float passes the module's JSON-safe sentinel encoding; serialization
    is ``json.dumps(payload, sort_keys=True, indent=2)`` plus a trailing
    newline, so two renders of one outcome are byte-identical (CONF-01 ordering
    edge). Aggregate distributions are clearly labeled descriptive diagnostics,
    never the classification criterion (D-06/D-14).
    """
    key_membership = run.accounting.get("key_membership", {})
    rows = sorted(
        (
            _trajectory_row(measures, confounds,
                            key_membership.get(measures.key, {}))
            for measures, confounds in run.results
        ),
        key=lambda row: (row["key"]["variant"], row["key"]["fidelity"],
                         row["key"]["id"]),
    )
    aggregates = {
        arm_name: {
            "role": "descriptive_diagnostic",
            "count_consistent": int(summary.count_consistent),
            "count_separated": int(summary.count_separated),
            "residual_medians": _distribution(summary.residual_medians),
            "residual_maxima": _distribution(summary.residual_maxima),
        }
        for arm_name, summary in sorted(run.outcome.arm_summaries.items())
    }
    payload = {
        "schema_version": PROBE_SCHEMA_VERSION,
        "repo_commit": provenance.repo_commit,
        "probe_invocation": list(provenance.probe_invocation),
        "manifests": [
            {"label": manifest.label, "path": manifest.path,
             "sha256": manifest.sha256}
            for manifest in provenance.manifests
        ],
        "blacklist_sha256": provenance.blacklist_sha256,
        "data_root_source": provenance.data_root_source,
        "dtype": provenance.dtype,
        "device": provenance.device,
        "math": provenance.math,
        "torch_version": provenance.torch_version,
        "D_characteristic_length": float(D_CHARACTERISTIC_LENGTH),
        "T_characteristic_time": float(T_CHARACTERISTIC_TIME),
        "arms": {
            arm_name: {
                "convention": {
                    "position": convention.position,
                    "time": convention.time,
                    "velocity": convention.velocity,
                    "masses": convention.masses,
                },
                "softening": float(EPS_SOFT),
            }
            for arm_name, convention in sorted(ARM_CONVENTIONS.items())
        },
        "population": {
            "rule": POPULATION_RULE,
            "eligible_count": len(run.population.eligible),
            "counts_per_split_per_manifest":
                run.population.counts_per_split_per_manifest,
            "exclusion_ledger": {
                reason: [_physical_key_pair(physical_key) for physical_key in keys]
                for reason, keys in sorted(run.population.exclusion_ledger.items())
            },
            "exclusion_counts": {
                reason: len(keys)
                for reason, keys in sorted(run.population.exclusion_ledger.items())
            },
        },
        "exclusion_counts": dict(sorted(
            run.accounting.get("exclusion_counts", {}).items())),
        "trajectories": rows,
        "aggregates": aggregates,
        "tolerance_derivation": TOLERANCE_DERIVATION,
        "confound_register": [
            [kind,
             _key_triple(key) if hasattr(key, "fidelity") else str(key),
             _json_safe(detail)]
            for kind, key, detail in run.outcome.confound_register
        ],
        "verdict": run.outcome.verdict,
        "rationale": run.outcome.rationale,
    }
    return _json_safe(payload)


def _fmt(value):
    if isinstance(value, str):
        return value
    if isinstance(value, float):
        return f"{value:.6g}"
    return str(value)


def render_summary_markdown(payload):
    """Markdown rendering that LEADS with what was measured and the resulting
    branch (46-CONTEXT § Specific Ideas): the verdict + population-size
    headline, the visually symmetric two-hypothesis table with the control arms
    beside them, every arm's coordinate tuple, population/exclusion accounting,
    the confound register, and the numerical tolerance derivation stated
    SEPARATELY from the no-physics-threshold sentence (D-06).
    """
    arms = payload["arms"]
    aggregates = payload["aggregates"]
    population = payload["population"]
    order = (ARM_SCALED, ARM_RAW, ARM_POSITIVE_CONTROL, ARM_PROVENANCE_CONTROL)
    titles = {
        ARM_SCALED: "scaled hypothesis",
        ARM_RAW: "raw hypothesis",
        ARM_POSITIVE_CONTROL: "positive control",
        ARM_PROVENANCE_CONTROL: "provenance control",
    }
    lines = [
        "# CONF-01 Target-Frame Probe Evidence",
        "",
        f"**Verdict: `{payload['verdict']}`** — measured over "
        f"**{population['eligible_count']}** eligible Stage-0 trajectories.",
        "",
        "## What was measured",
        "",
        "The exact resident `StageIndex` trajectory surface consumed as "
        "training targets (D-01), measured train-free under two symmetric frame "
        "hypotheses with two control arms (D-03). The verdict routes the branch: "
        "`TARGETS_ARE_SCALED` -> D-08 (conformant); every other verdict -> D-09 "
        "(owner branch).",
        "",
        "## Symmetric hypotheses and control arms",
        "",
        "| measure | " + " | ".join(titles[arm] for arm in order) + " |",
        "|" + "---|" * (len(order) + 1),
    ]
    for attribute in ("position", "time", "velocity", "masses"):
        lines.append(
            f"| convention {attribute} | " + " | ".join(
                f"`{arms[arm]['convention'][attribute]}`" for arm in order) + " |"
        )
    lines.append("| force softening | " + " | ".join(
        _fmt(arms[arm]["softening"]) for arm in order) + " |")
    lines.append("| median of per-trajectory median residuals | " + " | ".join(
        _fmt(aggregates[arm]["residual_medians"]["median"]) for arm in order) + " |")
    lines.append("| max of per-trajectory max residuals | " + " | ".join(
        _fmt(aggregates[arm]["residual_maxima"]["max"]) for arm in order) + " |")
    lines.append("| trajectories consistent | " + " | ".join(
        str(aggregates[arm]["count_consistent"]) for arm in order) + " |")
    lines.append("| trajectories separated (own residual > tolerance) | "
                 + " | ".join(str(aggregates[arm]["count_separated"])
                             for arm in order) + " |")
    lines += [
        "",
        "## Population accounting",
        "",
        f"- Rule: {population['rule']}",
        f"- Eligible trajectories: {population['eligible_count']}",
        "- Per-manifest per-split eligible counts:",
    ]
    for label, per_split in sorted(population["counts_per_split_per_manifest"].items()):
        lines.append(f"  - `{label}`: train {per_split.get('train', 0)}, "
                     f"validation {per_split.get('validation', 0)}")
    lines.append("- Population-level exclusions:")
    if population["exclusion_counts"]:
        for reason, count in sorted(population["exclusion_counts"].items()):
            lines.append(f"  - `{reason}`: {count}")
    else:
        lines.append("  - none")
    lines.append("- Snapshot-level exclusions (shared qualifying mask):")
    if payload["exclusion_counts"]:
        for reason, count in sorted(payload["exclusion_counts"].items()):
            lines.append(f"  - `{reason}`: {count}")
    else:
        lines.append("  - none")
    lines += ["", "## Confound register", ""]
    if payload["confound_register"]:
        for kind, key, detail in payload["confound_register"]:
            if isinstance(key, dict):
                key_text = f"{key['variant']}/{key['fidelity']}/{key['id']}"
            else:
                key_text = str(key)
            lines.append(f"- {kind}: {key_text} -> {detail}")
    else:
        lines.append("- none (empty register)")
    lines += [
        "",
        "## Provenance",
        "",
        f"- Repository commit: `{payload['repo_commit']}`",
    ]
    for manifest in payload["manifests"]:
        lines.append(f"- Manifest `{manifest['label']}`: `{manifest['path']}` "
                     f"sha256 `{manifest['sha256']}`")
    lines.append(f"- Blacklist sha256: `{payload['blacklist_sha256']}`")
    lines.append(f"- Data-root resolution source: `{payload['data_root_source']}`")
    lines.append(f"- D = {_fmt(payload['D_characteristic_length'])}, "
                 f"T = {_fmt(payload['T_characteristic_time'])}")
    lines.append(f"- dtype/device: `{payload['dtype']}` / `{payload['device']}` "
                 f"(probe math `{payload['math']}`), "
                 f"torch `{payload['torch_version']}`")
    lines += [
        "",
        "## Numerical tolerance derivation",
        "",
        payload["tolerance_derivation"],
        "",
        "No physics acceptance threshold was applied: the tolerance above "
        "answers only whether two measurements agree within the numerical "
        "resolution of the finite-difference operator and the represented "
        "dtype; it is not a physics-acceptance, target-quality, Hamiltonian, "
        "or training threshold (D-06, GAP-46-03 guardrail 4).",
        "",
    ]
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Evidence writer (46-04; containment-guarded, atomic, non-overwriting)
# ---------------------------------------------------------------------------


def _reject_evidence_root(evidence_root, *, data_root=None):
    """Containment guard (T-46-04-03): refuse an evidence root inside
    ``simulation_data/`` (the residual_probe guard) or inside the supplied
    corpus data root."""
    resolved = Path(evidence_root).resolve()
    dataset_root = (_REPO_ROOT / "simulation_data").resolve()
    try:
        resolved.relative_to(dataset_root)
    except ValueError:
        pass
    else:
        raise ValueError("evidence root must not be inside simulation_data")
    if data_root is not None:
        corpus_root = Path(data_root).resolve()
        try:
            resolved.relative_to(corpus_root)
        except ValueError:
            pass
        else:
            raise ValueError(
                "evidence root must not be inside the corpus data root")


def _new_run_dir(evidence_root):
    """Allocate a non-overwriting UTC run directory (the residual_probe pattern)."""
    run_id = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    for suffix in range(1000):
        name = run_id if suffix == 0 else f"{run_id}-{suffix:03d}"
        candidate = evidence_root / name
        try:
            candidate.mkdir(parents=True, exist_ok=False)
        except FileExistsError:
            continue
        return candidate
    raise FileExistsError(
        f"could not allocate exclusive evidence directory under {evidence_root}")


def _guard_serialized_bytes(raw, *, data_root=None):
    """Fail-closed redaction guard (the adapter ``evidence_lines`` precedent):
    committed evidence bytes never contain the host home prefix or the resolved
    corpus root (T-46-04-02)."""
    home = str(Path.home())
    if home and home in raw:
        raise EvidenceRedactionError(
            "serialized frame-probe evidence contains the host home prefix")
    if data_root is not None:
        root_str = str(Path(data_root).resolve())
        if root_str in raw:
            raise EvidenceRedactionError(
                "serialized frame-probe evidence contains the resolved data root")


def write_frame_probe_evidence(payload, evidence_root, *, data_root=None):
    """Write ``raw.json`` + ``summary.md`` under a fresh UTC run dir.

    Guard order: containment refusal first (``simulation_data/`` and the
    supplied corpus root), then the serialized bytes pass the fail-closed
    redaction guard, then a non-overwriting UTC run directory is allocated and
    both artifacts are written via
    ``pinn.training.atomic_io.atomic_write_text``. Returns the run directory.
    """
    root = Path(evidence_root)
    _reject_evidence_root(root, data_root=data_root)
    raw = json.dumps(payload, sort_keys=True, indent=2) + "\n"
    summary = render_summary_markdown(payload)
    _guard_serialized_bytes(raw + summary, data_root=data_root)
    run_dir = _new_run_dir(root)
    atomic_write_text(run_dir / "raw.json", raw)
    atomic_write_text(run_dir / "summary.md", summary)
    return run_dir


# ---------------------------------------------------------------------------
# CLI — the single sanctioned entry point (46-04; invoked once by 46-06)
# ---------------------------------------------------------------------------


def _sha256_file(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def _reduce_path(value, repo_root):
    """Reduce a path for committed evidence: repo-relative when inside the
    repo, else basename — never a host-absolute path (T-46-04-02)."""
    path = Path(value)
    try:
        resolved = path.resolve()
    except OSError:
        return path.name
    try:
        return resolved.relative_to(Path(repo_root).resolve()).as_posix()
    except ValueError:
        return resolved.name


def _reduced_invocation(argv, repo_root):
    """The probe invocation with any path-like token path-reduced."""
    reduced = ["python", "-m", "pinn.verification.target_frame_probe"]
    for token in argv:
        token_str = str(token)
        candidate = Path(token_str)
        if candidate.is_absolute() or candidate.exists():
            reduced.append(_reduce_path(candidate, repo_root))
        else:
            reduced.append(token_str)
    return tuple(reduced)


def _unique_labels(paths):
    """Deterministic manifest labels from path stems (``~2`` on collisions)."""
    seen = {}
    labels = []
    for path in paths:
        stem = Path(path).stem
        count = seen.get(stem, 0) + 1
        seen[stem] = count
        labels.append(stem if count == 1 else f"{stem}~{count}")
    return labels


def _stage0_view(index):
    """Sorted Stage-0 RecordKey view of one train/validation StageIndex."""
    return tuple(sorted(
        key for key in index.record_keys()
        if index.stage_label(key) is StageLabel.STAGE_0
    ))


def _run_probe(args, argv):
    repo_root = _REPO_ROOT
    repo_commit = subprocess.check_output(
        ["git", "rev-parse", "HEAD"], text=True, cwd=repo_root).strip()
    adapter = AdmittedSetAdapter(
        root=args.data_root, blacklist_path=args.blacklist_path)
    labels = _unique_labels(args.manifest)
    stage0_views = {}
    test_keys = {}
    first_views = None
    for position, (label, manifest_path) in enumerate(zip(labels, args.manifest)):
        manifest = SplitManifest.from_path(manifest_path)
        # StageIndex.from_split validates the manifest physical-key population
        # against the adapter and raises on mismatch — a drifted population is
        # an operational failure, never a probed one (D-02, T-46-04-05).
        train_index = StageIndex.from_split(adapter, manifest, "train")
        validation_index = StageIndex.from_split(adapter, manifest, "validation")
        if position == 0:
            first_views = (train_index, validation_index)
        stage0_views[label] = {
            "train": _stage0_view(train_index),
            "validation": _stage0_view(validation_index),
        }
        # The test partition is read as a PHYSICAL-key set from the manifest
        # payload, never materialized as a StageIndex (D-16, T-46-04-04).
        test_keys[label] = manifest.physical_keys("test")
    population = resolve_probe_population(stage0_views, test_keys)
    routing = {
        key: population.membership[key][population.first_manifest_label]
        for key in population.eligible
    }
    resident_reader = _build_resident_reader(first_views[0], first_views[1], routing)
    control_reader = _build_control_reader(
        adapter.data_root,
        frozenset(key.physical_key for key in population.eligible),
        chunk_size=args.chunk_size,
    )
    results, accounting = probe_population(
        [(key, population.membership[key]) for key in population.eligible],
        resident_reader, control_reader)
    outcome = decide_verdict(results, accounting)
    blacklist_path = (
        args.blacklist_path
        if args.blacklist_path is not None
        else adapter.data_root / DEFAULT_BLACKLIST_NAME
    )
    provenance = EvidenceProvenance(
        repo_commit=repo_commit,
        manifests=tuple(
            ManifestIdentity(label=label,
                             path=_reduce_path(manifest_path, repo_root),
                             sha256=_sha256_file(manifest_path))
            for label, manifest_path in zip(labels, args.manifest)
        ),
        blacklist_sha256=_sha256_file(blacklist_path),
        data_root_source=adapter.data_root_source,
        # float32/CPU is the adapter's only supported residency, so no
        # precision/device flags exist; the probe's measurement math is float64.
        dtype="float32",
        device="cpu",
        math="float64",
        torch_version=torch.__version__,
        probe_invocation=_reduced_invocation(argv, repo_root),
    )
    run = FrameProbeRun(outcome=outcome, results=tuple(results),
                        accounting=accounting, population=population)
    payload = render_evidence_payload(run, provenance)
    run_dir = write_frame_probe_evidence(payload, args.evidence_root,
                                         data_root=adapter.data_root)
    return run_dir, outcome, len(population.eligible)


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="python -m pinn.verification.target_frame_probe",
        description=(
            "Measure the resident Stage-0 target surface under symmetric "
            "raw/scaled frame hypotheses with two control arms and write the "
            "D-05 CONF-01 evidence artifact. Exit 0 means evidence was measured "
            "and durably written (whatever the verdict — branch routing is plan "
            "46-06's job); exit 2 means the probe could not run or could not "
            "write."
        ),
    )
    parser.add_argument(
        "--manifest", action="append", required=True, type=Path, metavar="PATH",
        help="path to a frozen splits manifest; repeat for each retained "
             "manifest (at least one required)")
    parser.add_argument(
        "--evidence-root", type=Path, default=_DEFAULT_EVIDENCE_ROOT,
        help="evidence tree root (default: the Phase 46 target-frame tree)")
    parser.add_argument(
        "--data-root", type=Path, default=None,
        help="corpus Data/ root (default: the adapter's standard resolution)")
    parser.add_argument(
        "--blacklist-path", type=Path, default=None,
        help="blacklist JSON (default: the adapter's standard resolution)")
    parser.add_argument(
        "--chunk-size", type=int, default=64,
        help="maximum parsed controls held in memory at once (default: 64)")
    args = parser.parse_args(argv)
    if args.chunk_size <= 0:
        parser.error("--chunk-size must be a positive integer")
    raw_argv = list(sys.argv[1:] if argv is None else argv)
    try:
        run_dir, outcome, eligible_count = _run_probe(args, raw_argv)
    except Exception as exc:  # noqa: BLE001 - operational failure, never a verdict
        print(f"target-frame probe operational failure: "
              f"{type(exc).__name__}: {exc}", file=sys.stderr)
        return 2
    print(f"CONF-01 target-frame probe: verdict={outcome.verdict} "
          f"eligible={eligible_count} evidence={run_dir}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
