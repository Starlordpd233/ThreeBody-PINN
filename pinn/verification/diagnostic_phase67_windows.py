"""Phase 67 (EXP-05, D-06): sampled signed-lap window prefixes.

D-06's window intervention selects, for each requested lap count, the FIRST
EXISTING gold sample whose cumulative SIGNED inner-pair turns about the census
initial orbit normal reach that count. The selection reuses the census's own
ordered inner-pair separation (``r_second - r_first``), its initial normal
(:func:`pinn.verification.stage0_census.orbit_normal`) and its principal
signed-angle steps (``atan2(normal . cross(r[j-1], r[j]), r[j-1] . r[j])``
divided by ``2*pi``), accumulated from exactly zero on the first sample.

Contract highlights (D-06/D-11, EXP-05):

- The endpoint is the exact float64 gold timestamp of the crossing sample —
  never an interpolated sample, never an average-period duration.
- The retained grid is the loader's exact inclusive mask
  :func:`pinn.verification.diagnostic_data.physical_window`
  (``0 <= t <= endpoint``), not the census helper's ``t_max`` tolerance.
- ``tau`` keeps the locked global ``T_CHARACTERISTIC_TIME`` normalization and
  is never rescaled to stretch a prefix to ``[-1, 1]``.
- A reversal is a signed step: absolute turning never substitutes for the
  signed count, and a grid whose steps reach the census unwrap limit cannot
  be unwrapped and refuses.
- A grid that cannot distinguish two requested counts (their first crossings
  share one sample) refuses instead of silently merging arms.
- ``L*10/N_in`` appears only as a labelled rough planning duration, never as
  the endpoint rule.

This module reads no corpus: callers hand it an already-loaded reference
object with ``times``, ``positions``, ``velocities`` and ``inner_pair``.
"""

from __future__ import annotations

import hashlib
import math

import numpy as np

from pinn.constants import T_CHARACTERISTIC_TIME
from pinn.verification.diagnostic_data import (
    DiagnosticDataRefused,
    physical_window,
    validate_window,
)
from pinn.verification.feasibility_scorecard import load_scorecard
from pinn.verification.stage0_census import (
    CensusHalt,
    _angle_steps,
    _pair_slots,
    _separation,
    orbit_normal,
)

__all__ = ["WindowPrefixRefused", "first_lap_prefixes"]

_TWO_PI = 2.0 * np.pi
#: The D-06 ladder: prefixes at 1, 2, 5 and 10 signed inner laps.
DEFAULT_LAP_COUNTS = (1, 2, 5, 10)

#: GAP-59-08 stays explicit on every window artifact: the frozen scorer's
#: energy diagnostic is an associated limitation, and nothing here imposes or
#: adjudicates an energy pass bar (D-11/D-13; Phase 68 owns that ruling).
GAP_59_08_NOTE = (
    "GAP-59-08: the energy diagnostic limitation stays open; this window "
    "evidence imposes no energy threshold and makes no energy-bar ruling"
)


class WindowPrefixRefused(RuntimeError):
    """A signed-lap prefix request violates the D-06 window contract."""


def _plain_lap_counts(lap_counts):
    """Validate the requested lap counts: a non-empty tuple of distinct
    finite numbers, each at least one full signed lap, booleans excluded."""
    if not isinstance(lap_counts, tuple) or len(lap_counts) == 0:
        raise WindowPrefixRefused(
            f"lap counts must be a non-empty tuple of real numbers; got {lap_counts!r}"
        )
    counts = []
    for lap in lap_counts:
        if isinstance(lap, bool) or not isinstance(lap, (int, float)):
            raise WindowPrefixRefused(
                f"each lap count must be a real number, booleans excluded; got {lap!r}"
            )
        value = float(lap)
        if not math.isfinite(value):
            raise WindowPrefixRefused(f"each lap count must be finite; got {lap!r}")
        if value < 1.0:
            raise WindowPrefixRefused(
                f"each lap count is at least one full signed lap; got {lap!r}"
            )
        counts.append(value)
    if len(set(counts)) != len(counts):
        raise WindowPrefixRefused(
            f"lap counts must be distinct; got {lap_counts!r}"
        )
    return counts


def _rough_planning_duration(lap, census_n_in):
    """The labelled approximate duration ``L*T/N_in`` — a cost estimate only.

    D-06: this value never selects an endpoint and never becomes a fitted
    window; the endpoint is always the earliest existing crossing sample.
    """
    if (
        isinstance(census_n_in, bool)
        or not isinstance(census_n_in, (int, float))
        or not math.isfinite(float(census_n_in))
        or float(census_n_in) <= 0.0
    ):
        raise WindowPrefixRefused(
            f"census_n_in must be a finite positive number, booleans excluded; "
            f"got {census_n_in!r}"
        )
    return {
        "value": float(lap) * float(T_CHARACTERISTIC_TIME) / float(census_n_in),
        "note": (
            "approximate planning duration L*T/N_in from the census mean inner "
            "motion; a labelled cost estimate only — never the endpoint and "
            "never a fitted window"
        ),
    }


def _reference_arrays(reference):
    """Validate and return the reference's finite, strictly increasing grid.

    The physical window starts at exactly zero (D-06/D-11); the arrays must
    be finite before any angular search runs.
    """
    times = getattr(reference, "times", None)
    positions = getattr(reference, "positions", None)
    velocities = getattr(reference, "velocities", None)
    inner_pair = getattr(reference, "inner_pair", None)
    if times is None or positions is None or velocities is None or inner_pair is None:
        raise WindowPrefixRefused(
            "the reference needs times, positions, velocities and inner_pair; "
            "a field is missing"
        )
    t = np.asarray(times, dtype=np.float64).reshape(-1)
    pos = np.asarray(positions, dtype=np.float64)
    vel = np.asarray(velocities, dtype=np.float64)
    if t.size == 0 or not bool(np.all(np.isfinite(t))):
        raise WindowPrefixRefused("record times are empty or non-finite")
    if pos.shape != (t.size, 3, 3) or vel.shape != (t.size, 3, 3):
        raise WindowPrefixRefused(
            f"positions and velocities must be ({t.size}, 3, 3) arrays; got "
            f"{pos.shape} and {vel.shape}"
        )
    if not bool(np.all(np.isfinite(pos))) or not bool(np.all(np.isfinite(vel))):
        raise WindowPrefixRefused(
            "positions and velocities must be finite before any search"
        )
    if t.size < 2:
        raise WindowPrefixRefused(
            f"at least two samples are needed for a prefix; got {t.size}"
        )
    if not bool(np.all(np.diff(t) > 0.0)):
        raise WindowPrefixRefused(
            "record times must be distinct and strictly increasing"
        )
    if float(t[0]) != 0.0:
        raise WindowPrefixRefused(
            "the physical window starts at exactly zero; the record starts at "
            f"{float(t[0])!r}"
        )
    return t, pos, vel


def _signed_turns(reference, times, positions, velocities):
    """Cumulative signed inner-pair turns and the guarded maximum step.

    The cumulative count begins at exactly zero on the first sample, so the
    first sample never contributes a turn. The step guard is the census's own
    admission limit (``census_rules.unwrap_max_step_rad`` from the frozen
    scorecard), applied over the whole searched record: one aliased step
    anywhere corrupts every later crossing decision.

    The guarded step is the larger of two measures against that one limit:
    the census's observed principal step, and the increment predicted by the
    local angular rate about the same normal (trapezoid over the recorded
    separation and its derivative). The principal step alone cannot exceed
    pi — a true increment beyond pi wraps silently — so the predicted
    increment is what actually exposes an aliased grid at the census limit.
    """
    try:
        first, second, _outer = _pair_slots(reference)
        vector, derivative = _separation(positions, velocities, first, second)
        normal = orbit_normal(vector[0], derivative[0])
        steps = _angle_steps(vector, normal)
    except CensusHalt as exc:
        raise WindowPrefixRefused(str(exc)) from exc
    if not bool(np.all(np.isfinite(steps))):
        raise WindowPrefixRefused("a signed inner-pair angle step is not finite")
    radius_sq = np.sum(vector * vector, axis=1)
    if not bool(np.all(np.isfinite(radius_sq))) or bool(np.any(radius_sq <= 0.0)):
        raise WindowPrefixRefused(
            "the inner-pair separation vanishes; its angle is undefined"
        )
    omega = (np.cross(vector, derivative) @ normal) / radius_sq
    if not bool(np.all(np.isfinite(omega))):
        raise WindowPrefixRefused("an inner-pair angular rate is not finite")
    predicted = 0.5 * (omega[:-1] + omega[1:]) * np.diff(times)
    if not bool(np.all(np.isfinite(predicted))):
        raise WindowPrefixRefused("a predicted inner-pair angle step is not finite")
    turns = np.concatenate(([0.0], np.cumsum(steps) / _TWO_PI))
    max_step = float(max(np.max(np.abs(steps)), np.max(np.abs(predicted))))
    return turns, max_step


def first_lap_prefixes(
    reference,
    lap_counts=DEFAULT_LAP_COUNTS,
    *,
    census_n_in=None,
    scorecard=None,
):
    """The D-06 signed-lap prefixes of one loaded reference record.

    For each requested lap count, the earliest existing gold sample whose
    cumulative signed inner-pair turns about the census initial normal reach
    that count becomes the prefix endpoint (its exact float64 timestamp).
    Each returned evidence mapping carries the immediate preceding/current
    bracket (indices, timestamps and turns), the endpoint, the retained
    sample count, the actual lap coverage at the crossing, the census
    maximum angular step, and the sha256 of the retained physical grid and of
    its locked-global ``tau``. Refuses (never interpolates or rescales) on
    non-finite data, non-increasing times, a nonzero physical start, an
    undefined orbit normal, census angular aliasing, unreached counts, a
    grid that cannot distinguish two requested counts, or an endpoint
    outside the loader's ``(0, T_CHARACTERISTIC_TIME]`` window domain.
    """
    counts = _plain_lap_counts(lap_counts)
    t, positions, velocities = _reference_arrays(reference)
    turns, max_step_rad = _signed_turns(reference, t, positions, velocities)
    if scorecard is None:
        scorecard = load_scorecard()
    limit = float(scorecard.section("census_rules")["unwrap_max_step_rad"])
    if max_step_rad >= limit:
        raise WindowPrefixRefused(
            f"the inner-pair angular step reached the census unwrap limit "
            f"{limit!r} (max step {max_step_rad!r}); the grid cannot be unwrapped"
        )
    crossings = {}
    for lap in counts:
        found = np.flatnonzero(turns >= lap)
        if found.size == 0:
            raise WindowPrefixRefused(
                f"the requested {lap!r} laps are unreached: the record covers "
                f"at most {float(turns[-1])!r} signed inner turns"
            )
        crossings[lap] = int(found[0])
    if len(set(crossings.values())) != len(crossings):
        raise WindowPrefixRefused(
            "the grid cannot distinguish the requested laps: at least two "
            "requested counts first cross at the same gold sample; use "
            "separate counts or a finer grid"
        )
    prefixes = []
    for lap in counts:
        index = crossings[lap]
        endpoint = float(t[index])
        try:
            window = validate_window(endpoint)
            mask = physical_window(t, window)
        except DiagnosticDataRefused as exc:
            raise WindowPrefixRefused(str(exc)) from exc
        retained = np.asarray(t[mask], dtype=np.float64)
        tau = 2.0 * (retained / T_CHARACTERISTIC_TIME) - 1.0
        prefix = {
            "requested_laps": lap,
            "preceding_index": index - 1,
            "preceding_time": float(t[index - 1]),
            "preceding_turns": float(turns[index - 1]),
            "crossing_index": index,
            "requested_endpoint": endpoint,
            "last_retained_timestamp": float(retained[-1]),
            "sample_count": int(retained.shape[0]),
            "actual_laps": float(turns[index]),
            "max_step_rad": max_step_rad,
            "physical_times_sha256": hashlib.sha256(
                np.ascontiguousarray(retained, dtype=np.float64).tobytes()
            ).hexdigest(),
            "normalized_tau_sha256": hashlib.sha256(
                np.ascontiguousarray(tau, dtype=np.float64).tobytes()
            ).hexdigest(),
        }
        if census_n_in is not None:
            prefix["rough_planning_duration"] = _rough_planning_duration(lap, census_n_in)
        prefixes.append(prefix)
    return prefixes
