"""Phase 67 (EXP-05, D-06): sampled signed-lap window prefixes and baselines.

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

:symbol:`same_window_expectations` then verifies, on exactly the selected
samples, that the harness's matched-window constant and two-Kepler
comparisons agree with an independent recomputation through the same frozen
``score_trajectory``/``two_kepler_prediction`` functions — a
serialization/consistency check (relative tolerance 1e-8, absolute 1e-10),
never a new science bar. A formula refusal stays an explicit nonapplicability
with its reason and never becomes a manufactured finite score, different
windows cannot borrow each other's (or the full-window EXP-01) constants
because the retained grid is hash-checked against the selected prefix, and
GAP-59-08's energy limitation stays explicit with no energy-threshold ruling
(D-11/D-13).

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
from pinn.verification.diagnostic_fit import _comparison_rows
from pinn.verification.feasibility_scorecard import load_scorecard
from pinn.verification.feasibility_scorer import score_trajectory
from pinn.verification.stage0_census import (
    CensusHalt,
    _angle_steps,
    _pair_slots,
    _separation,
    orbit_normal,
)
from pinn.verification.two_kepler import NotApplicable, two_kepler_prediction

__all__ = [
    "WindowPrefixRefused",
    "WindowExpectationRefused",
    "first_lap_prefixes",
    "same_window_expectations",
]

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


class WindowExpectationRefused(RuntimeError):
    """A same-window baseline expectation violates the D-06/D-13 contract."""


#: The declared consistency tolerance for the independent baseline
#: recomputation — a serialization/consistency check, not a new science bar.
_BASELINE_REL_TOL = 1e-8
_BASELINE_ABS_TOL = 1e-10


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


def _close(left, right, maxima):
    """One numeric closeness update: returns False outside the tolerance."""
    a = float(left)
    b = float(right)
    if math.isnan(a) or math.isnan(b):
        if math.isnan(a) and math.isnan(b):
            return True
        return False
    delta = abs(a - b)
    maxima[0] = max(maxima[0], delta)
    if b != 0.0:
        maxima[1] = max(maxima[1], delta / abs(b))
    return math.isclose(a, b, rel_tol=_BASELINE_REL_TOL, abs_tol=_BASELINE_ABS_TOL)


def _score_agreement(left, right):
    """(agree, max_abs_delta, max_rel_delta) between two frozen score dicts.

    Labels and integer fields must match exactly; numeric fields use the
    declared consistency tolerance. Both sides come from the same frozen
    functions on the same arrays, so agreement is expected bitwise; the
    tolerance only guards serialization-level drift.
    """
    maxima = [0.0, 0.0]
    if sorted(left) != sorted(right):
        return False, math.inf, math.inf
    for key in ("velocity_source", "grid", "frame", "tier", "n_times"):
        if left.get(key) != right.get(key):
            return False, math.inf, math.inf
    for key in ("E", "e_sys_max", "e_in_max", "eps_h", "R_sys"):
        if not _close(left[key], right[key], maxima):
            return False, maxima[0], maxima[1]
    horizon_left = list(left.get("h") or [])
    horizon_right = list(right.get("h") or [])
    if len(horizon_left) != len(horizon_right):
        return False, maxima[0], maxima[1]
    for pair_left, pair_right in zip(horizon_left, horizon_right):
        if float(pair_left[0]) != float(pair_right[0]):
            return False, maxima[0], maxima[1]
        if not _close(pair_left[1], pair_right[1], maxima):
            return False, maxima[0], maxima[1]
    return True, maxima[0], maxima[1]


def _independent_constant_row(positions, times, masses, inner_pair, *, scorecard, grid):
    """The same-window mean-position constant with zero velocities, scored
    through the frozen ``score_trajectory`` independently of the harness row."""
    constant = np.broadcast_to(
        positions.mean(axis=0, keepdims=True), positions.shape
    ).copy()
    score = score_trajectory(
        constant,
        np.zeros_like(constant),
        positions,
        masses,
        inner_pair,
        times,
        velocity_source="analytic",
        scorecard=scorecard,
        grid=grid,
    )
    return {
        "comparison": "window_mean_constant",
        "predictor": {
            "kind": "window_mean_constant",
            "velocities": "zero",
            "definition": "each body held at its time-mean position over the window",
            "construction": "independent same-window recomputation",
        },
        "score": score.to_json_dict(),
    }


def _independent_kepler_row(
    positions, times, masses, inner_pair, r0, v0, *, scorecard, grid
):
    """The frozen two-Kepler formula called directly on the selected window.

    A ``NotApplicable`` result stays an explicit refusal with its reason; a
    Newton-solver failure stays the frozen message. Neither becomes a score.
    """
    elapsed = (times - times[0]) / T_CHARACTERISTIC_TIME
    try:
        predicted, predicted_v = two_kepler_prediction(r0, v0, masses, inner_pair, elapsed)
    except NotApplicable as exc:
        return {
            "comparison": "two_kepler",
            "applicable": False,
            "failure": "not_applicable",
            "reason": exc.reason,
            "construction": "independent same-window recomputation",
        }
    except RuntimeError as exc:
        return {
            "comparison": "two_kepler",
            "applicable": False,
            "failure": "solver_did_not_converge",
            "reason": str(exc),
            "construction": "independent same-window recomputation",
        }
    score = score_trajectory(
        predicted,
        predicted_v,
        positions,
        masses,
        inner_pair,
        times,
        velocity_source="analytic",
        scorecard=scorecard,
        grid=grid,
    )
    return {
        "comparison": "two_kepler",
        "applicable": True,
        "initial_state": "the train record's first in-window snapshot (true_r0, true_v0)",
        "construction": "independent same-window recomputation",
        "score": score.to_json_dict(),
    }


def _require_prefix_grid(prefix, times, physical_sha, tau_sha):
    """The retained grid must be exactly the selected prefix's grid.

    A window loaded elsewhere (another lap's prefix, a tampered interior
    timestamp, or the full-window EXP-01 grid) refuses before any scoring,
    so no window can borrow another window's baselines or constants.
    """
    if not isinstance(prefix, dict):
        raise WindowExpectationRefused(
            f"the prefix evidence must be a mapping; got {prefix!r}"
        )
    expected_physical = prefix.get("physical_times_sha256")
    expected_tau = prefix.get("normalized_tau_sha256")
    endpoint = prefix.get("requested_endpoint")
    sample_count = prefix.get("sample_count")
    if (
        not isinstance(expected_physical, str)
        or not isinstance(expected_tau, str)
        or endpoint is None
        or sample_count is None
    ):
        raise WindowExpectationRefused(
            "the prefix evidence lacks its grid hashes, endpoint or sample count"
        )
    if expected_physical != physical_sha or expected_tau != tau_sha:
        raise WindowExpectationRefused(
            "the retained grid does not match the prefix evidence: grid hashes "
            f"{physical_sha} / {tau_sha} vs prefix {expected_physical} / "
            f"{expected_tau}"
        )
    if float(times[-1]) != float(endpoint) or int(times.size) != int(sample_count):
        raise WindowExpectationRefused(
            "the loaded window does not match the prefix evidence: last "
            f"retained timestamp {float(times[-1])!r} / {int(times.size)} "
            f"samples vs endpoint {float(endpoint)!r} / {int(sample_count)} "
            "samples"
        )


def same_window_expectations(data, *, scorecard, prefix=None):
    """Independently checked constant and two-Kepler baselines on one window.

    ``data`` is the loader's loaded arm (``score`` view, ordered masses and
    the first in-window snapshot). The harness's own matched-window
    comparison rows (``_comparison_rows`` through the frozen
    ``score_trajectory``) are compared against an independent same-window
    recomputation — the mean-position constant with zero velocities and a
    direct ``two_kepler_prediction`` call — under the declared consistency
    tolerance. When ``prefix`` (evidence from :func:`first_lap_prefixes`) is
    given, the retained grid's hashes, endpoint and sample count must match
    it exactly, so different windows cannot borrow each other's baselines.
    Returns the evidence mapping (window, grid, ordered masses/inner pair,
    both paths' rows, applicability/reason, agreement, GAP-59-08 note);
    refuses on any disagreement or tampered window/grid.
    """
    view = getattr(data, "score", None)
    masses = getattr(data, "masses", None)
    true_r0 = getattr(data, "true_r0", None)
    true_v0 = getattr(data, "true_v0", None)
    if view is None or masses is None or true_r0 is None or true_v0 is None:
        raise WindowExpectationRefused(
            "the loaded data needs score, masses, true_r0 and true_v0; "
            "a field is missing"
        )
    times = np.asarray(view.times, dtype=np.float64).reshape(-1)
    positions = np.asarray(view.positions, dtype=np.float64)
    mass = np.asarray(masses, dtype=np.float64).reshape(3)
    if times.size < 2 or positions.shape != (times.size, 3, 3):
        raise WindowExpectationRefused(
            f"the score view needs at least two samples of (N, 3, 3) "
            f"positions; got {times.size} times and {positions.shape}"
        )
    if (
        not bool(np.all(np.isfinite(times)))
        or not bool(np.all(np.isfinite(positions)))
        or not bool(np.all(np.isfinite(mass)))
    ):
        raise WindowExpectationRefused("the score view must be finite")
    if not bool(np.all(np.diff(times) > 0.0)):
        raise WindowExpectationRefused(
            "score-view times must be distinct and strictly increasing"
        )
    inner_pair = tuple(int(slot) for slot in view.inner_pair)
    grid = str(view.grid)
    physical_sha = hashlib.sha256(
        np.ascontiguousarray(times, dtype=np.float64).tobytes()
    ).hexdigest()
    tau = 2.0 * (times / T_CHARACTERISTIC_TIME) - 1.0
    tau_sha = hashlib.sha256(
        np.ascontiguousarray(tau, dtype=np.float64).tobytes()
    ).hexdigest()
    if prefix is not None:
        _require_prefix_grid(prefix, times, physical_sha, tau_sha)
    harness_rows = {row["comparison"]: row for row in _comparison_rows(data, scorecard=scorecard)}
    r0 = true_r0.detach().cpu().numpy().astype(np.float64).reshape(3, 3)
    v0 = true_v0.detach().cpu().numpy().astype(np.float64).reshape(3, 3)
    constant_harness = harness_rows.get("window_mean_constant")
    kepler_harness = harness_rows.get("two_kepler")
    if constant_harness is None or kepler_harness is None:
        raise WindowExpectationRefused(
            "the harness comparison rows are missing a baseline; "
            f"got {sorted(harness_rows)}"
        )
    constant_independent = _independent_constant_row(
        positions, times, mass, inner_pair, scorecard=scorecard, grid=grid
    )
    constant_agree, constant_abs, constant_rel = _score_agreement(
        constant_harness["score"], constant_independent["score"]
    )
    if not constant_agree:
        raise WindowExpectationRefused(
            "the window-mean constant baselines disagree beyond the "
            f"consistency tolerance (rtol {_BASELINE_REL_TOL!r}, atol "
            f"{_BASELINE_ABS_TOL!r}): max abs delta {constant_abs!r}, "
            f"max rel delta {constant_rel!r}"
        )
    kepler_independent = _independent_kepler_row(
        positions, times, mass, inner_pair, r0, v0, scorecard=scorecard, grid=grid
    )
    applicable = bool(kepler_harness.get("applicable", False))
    if (
        applicable != bool(kepler_independent.get("applicable", False))
        or kepler_harness.get("failure") != kepler_independent.get("failure")
        or kepler_harness.get("reason") != kepler_independent.get("reason")
    ):
        raise WindowExpectationRefused(
            "the two-Kepler formula applicability disagrees between the "
            f"harness row ({kepler_harness.get('applicable')!r}, "
            f"{kepler_harness.get('failure')!r}, {kepler_harness.get('reason')!r}) "
            f"and the independent row ({kepler_independent.get('applicable')!r}, "
            f"{kepler_independent.get('failure')!r}, "
            f"{kepler_independent.get('reason')!r})"
        )
    kepler_block = {
        "applicable": applicable,
        "reason": kepler_harness.get("reason"),
        "harness": kepler_harness,
        "independent": kepler_independent,
    }
    if applicable:
        kepler_agree, kepler_abs, kepler_rel = _score_agreement(
            kepler_harness["score"], kepler_independent["score"]
        )
        if not kepler_agree:
            raise WindowExpectationRefused(
                "the two-Kepler baselines disagree beyond the consistency "
                f"tolerance (rtol {_BASELINE_REL_TOL!r}, atol "
                f"{_BASELINE_ABS_TOL!r}): max abs delta {kepler_abs!r}, "
                f"max rel delta {kepler_rel!r}"
            )
        kepler_block["agree"] = kepler_agree
        kepler_block["max_abs_delta"] = kepler_abs
        kepler_block["max_rel_delta"] = kepler_rel
    else:
        # Both paths carry the same explicit refusal, which is itself the
        # agreement on a nonapplicable formula.
        kepler_block["agree"] = True
    return {
        "grid": grid,
        "window": {
            "first_time": float(times[0]),
            "last_time": float(times[-1]),
            "sample_count": int(times.size),
        },
        "physical_times_sha256": physical_sha,
        "normalized_tau_sha256": tau_sha,
        "masses": [float(value) for value in mass],
        "inner_pair": [int(slot) for slot in inner_pair],
        "constant": {
            "harness": constant_harness,
            "independent": constant_independent,
            "agree": constant_agree,
            "max_abs_delta": constant_abs,
            "max_rel_delta": constant_rel,
        },
        "two_kepler": kepler_block,
        "gap_59_08": GAP_59_08_NOTE,
    }
