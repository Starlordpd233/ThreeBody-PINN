"""Phase 43 / 43-02 Task 1 — the position-only Hamiltonian gate metric (ACC-03).

Covers ``pinn.verification.gate_metrics``: the no-grad finite-difference
velocity, the matched-Plummer float64/eps_inv=1e-10 Hamiltonian, worst-
trajectory aggregation, both gate-boundary equalities (SPEC edge R3 /
prohibition 1: strict-inequality reject, boundary PASSES), above/below
threshold behavior, and NaN/Inf FAIL.

Skip discipline: not-yet-landed production symbols route through ``_require``
and SKIP (never ERROR) — the Phase-43 convention (``tests/phase43/__init__``).
"""

from __future__ import annotations

import importlib
import math
import unittest

import torch

from tests.phase43 import _SKIP_PHRASE

MODULE = "pinn.verification.gate_metrics"


def _require(symbol, module=MODULE):
    try:
        mod = importlib.import_module(module)
    except ImportError:
        raise unittest.SkipTest(f"{_SKIP_PHRASE} {module}.{symbol}")
    if not hasattr(mod, symbol):
        raise unittest.SkipTest(f"{_SKIP_PHRASE} {module}.{symbol}")
    return getattr(mod, symbol)


# ---------------------------------------------------------------------------
# No-grad finite-difference velocity.
# ---------------------------------------------------------------------------
class FiniteDifferenceVelocityTests(unittest.TestCase):
    def test_recovers_exact_constant_velocity_for_linear_motion(self):
        finite_difference_velocity = _require("finite_difference_velocity")
        times = torch.tensor([0.0, 1.0, 2.5, 4.0], dtype=torch.float32)
        # Constant velocity (2, -1, 0.5) per body 0; other bodies static.
        velocity_true = torch.tensor([2.0, -1.0, 0.5])
        positions = torch.zeros(4, 3, 3, dtype=torch.float32)
        for t_idx, t in enumerate(times.tolist()):
            positions[t_idx, 0, :] = velocity_true * t

        velocity = finite_difference_velocity(positions, times)

        self.assertEqual(velocity.dtype, torch.float64)
        self.assertEqual(velocity.device.type, "cpu")
        self.assertFalse(velocity.requires_grad)
        torch.testing.assert_close(
            velocity[:, 0, :], velocity_true.double().expand(4, 3), atol=1e-9, rtol=0
        )
        # Static bodies (1, 2) recover exactly zero velocity everywhere.
        torch.testing.assert_close(
            velocity[:, 1:, :], torch.zeros(4, 2, 3, dtype=torch.float64)
        )

    def test_requires_at_least_two_time_samples(self):
        finite_difference_velocity = _require("finite_difference_velocity")
        positions = torch.zeros(1, 3, 3)
        times = torch.tensor([0.0])
        with self.assertRaises(ValueError):
            finite_difference_velocity(positions, times)

    def test_requires_strictly_increasing_times(self):
        finite_difference_velocity = _require("finite_difference_velocity")
        positions = torch.zeros(3, 3, 3)
        non_monotone = torch.tensor([0.0, 1.0, 1.0])
        decreasing = torch.tensor([2.0, 1.0, 0.0])
        with self.assertRaises(ValueError):
            finite_difference_velocity(positions, non_monotone)
        with self.assertRaises(ValueError):
            finite_difference_velocity(positions, decreasing)

    def test_rejects_shape_mismatch(self):
        finite_difference_velocity = _require("finite_difference_velocity")
        positions = torch.zeros(4, 3, 3)
        times = torch.tensor([0.0, 1.0, 2.0])  # only 3 times for 4 positions
        with self.assertRaises(ValueError):
            finite_difference_velocity(positions, times)


# ---------------------------------------------------------------------------
# Matched-Plummer Hamiltonian: float64 CPU, eps_inv=1e-10 usage.
# ---------------------------------------------------------------------------
class MatchedPlummerHamiltonianTests(unittest.TestCase):
    def test_matches_hand_computed_two_snapshot_value(self):
        matched_plummer_hamiltonian_series = _require(
            "matched_plummer_hamiltonian_series"
        )
        masses = torch.tensor([1.0, 2.0, 3.0])
        # Two snapshots; bodies on the x-axis so pairwise separations are trivial.
        positions = torch.tensor(
            [
                [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [3.0, 0.0, 0.0]],
                [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [3.0, 0.0, 0.0]],
            ]
        )
        velocities = torch.tensor(
            [
                [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]],
                [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]],
            ]
        )
        eps_inv = 1e-10
        # T = 0.5*(1*1 + 2*1 + 3*1) = 3.0
        kinetic_expected = 3.0
        # V = -(m0 m1 / r01 + m0 m2 / r02 + m1 m2 / r12), r_safe = sqrt(r^2 + eps^2)
        r01 = math.sqrt(1.0 ** 2 + eps_inv ** 2)
        r02 = math.sqrt(3.0 ** 2 + eps_inv ** 2)
        r12 = math.sqrt(2.0 ** 2 + eps_inv ** 2)
        potential_expected = -(1.0 * 2.0 / r01 + 1.0 * 3.0 / r02 + 2.0 * 3.0 / r12)
        h_expected = kinetic_expected + potential_expected

        h_series = matched_plummer_hamiltonian_series(
            positions, velocities, masses, eps_inv=eps_inv
        )

        self.assertEqual(h_series.dtype, torch.float64)
        self.assertEqual(h_series.device.type, "cpu")
        self.assertEqual(tuple(h_series.shape), (2,))
        for value in h_series.tolist():
            self.assertAlmostEqual(value, h_expected, places=10)

    def test_eps_inv_actually_participates_in_the_potential(self):
        """A colliding pair (zero separation) is only finite because of the
        softening — proves eps_inv=1e-10 (not some other/absent value) is used."""
        matched_plummer_hamiltonian_series = _require(
            "matched_plummer_hamiltonian_series"
        )
        masses = torch.tensor([1.0, 1.0, 1.0])
        positions = torch.zeros(1, 3, 3)  # all three bodies coincide
        velocities = torch.zeros(1, 3, 3)
        h_series = matched_plummer_hamiltonian_series(
            positions, velocities, masses, eps_inv=1e-10
        )
        self.assertTrue(torch.isfinite(h_series).all())
        # V = -3 pairs * (1*1 / 1e-10) = -3e10
        self.assertAlmostEqual(float(h_series[0]), -3.0e10, delta=1.0)

    def test_default_eps_inv_constant_is_1e_minus_10(self):
        eps_inv = _require("EPS_INV")
        self.assertEqual(eps_inv, 1e-10)


# ---------------------------------------------------------------------------
# Per-trajectory eps_H + worst-trajectory aggregation.
# ---------------------------------------------------------------------------
class TrajectoryEpsHTests(unittest.TestCase):
    def test_zero_drift_gives_zero_eps_h(self):
        trajectory_eps_h = _require("trajectory_eps_h")
        h_series = torch.tensor([1.5, 1.5, 1.5], dtype=torch.float64)
        self.assertEqual(trajectory_eps_h(h_series), 0.0)

    def test_worst_time_drift_is_reported(self):
        trajectory_eps_h = _require("trajectory_eps_h")
        h0 = 2.0
        h_series = torch.tensor([h0, h0 * 1.00001, h0 * 1.1], dtype=torch.float64)
        eps_h = trajectory_eps_h(h_series)
        self.assertAlmostEqual(eps_h, 0.1, places=6)

    def test_zero_h0_yields_nonfinite(self):
        trajectory_eps_h = _require("trajectory_eps_h")
        h_series = torch.tensor([0.0, 1.0], dtype=torch.float64)
        self.assertFalse(math.isfinite(trajectory_eps_h(h_series)))

    def test_nonfinite_series_entry_yields_nonfinite(self):
        trajectory_eps_h = _require("trajectory_eps_h")
        h_series = torch.tensor([1.0, float("nan")], dtype=torch.float64)
        self.assertFalse(math.isfinite(trajectory_eps_h(h_series)))
        h_series_inf = torch.tensor([1.0, float("inf")], dtype=torch.float64)
        self.assertFalse(math.isfinite(trajectory_eps_h(h_series_inf)))


class ComputeTrajectoryGateMetricsTests(unittest.TestCase):
    def test_composes_velocity_and_hamiltonian_with_finite_kinetic_energy(self):
        compute_trajectory_gate_metrics = _require("compute_trajectory_gate_metrics")
        times = torch.tensor([0.0, 1.0, 2.0], dtype=torch.float32)
        masses = torch.tensor([1.0, 1.0, 1.0])
        positions = torch.zeros(3, 3, 3, dtype=torch.float32)
        for t_idx, t in enumerate(times.tolist()):
            positions[t_idx, 0, 0] = t  # body 0 moves at unit velocity along x
            positions[t_idx, 1, 1] = 5.0  # body 1 fixed, offset from origin
            positions[t_idx, 2, 2] = -5.0  # body 2 fixed, offset from origin

        result = compute_trajectory_gate_metrics(positions, times, masses)

        self.assertTrue(torch.isfinite(result.hamiltonian_series).all())
        self.assertTrue(math.isfinite(result.eps_h))
        # A conserved analytic trajectory (constant velocities, fixed
        # separations) has an EXACTLY constant Hamiltonian -> eps_H == 0.
        self.assertAlmostEqual(result.eps_h, 0.0, places=8)


class AggregateTestEpsHTests(unittest.TestCase):
    def test_takes_the_maximum_not_mean_or_min(self):
        aggregate_test_eps_h = _require("aggregate_test_eps_h")
        self.assertEqual(aggregate_test_eps_h([1e-7, 1e-6, 1e-4, 1e-8]), 1e-4)

    def test_any_nonfinite_trajectory_makes_the_aggregate_nonfinite(self):
        aggregate_test_eps_h = _require("aggregate_test_eps_h")
        self.assertFalse(
            math.isfinite(aggregate_test_eps_h([1e-7, float("nan"), 1e-6]))
        )
        self.assertFalse(
            math.isfinite(aggregate_test_eps_h([1e-7, float("inf"), 1e-6]))
        )

    def test_requires_at_least_one_trajectory(self):
        aggregate_test_eps_h = _require("aggregate_test_eps_h")
        with self.assertRaises(ValueError):
            aggregate_test_eps_h([])


# ---------------------------------------------------------------------------
# Gate boundary — SPEC edge R3 / prohibition 1 (strict-inequality reject).
# ---------------------------------------------------------------------------
class GateBoundaryTests(unittest.TestCase):
    def test_eps_h_equality_boundary_passes(self):
        gate_verdict = _require("gate_verdict")
        self.assertEqual(gate_verdict(1e-5), "PASS")

    def test_scs_equality_boundary_is_minus_five_and_passes(self):
        gate_verdict = _require("gate_verdict")
        scs_from_eps_h = _require("scs_from_eps_h")
        scs = scs_from_eps_h(1e-5)
        self.assertAlmostEqual(scs, -5.0, places=6)
        self.assertEqual(gate_verdict(1e-5), "PASS")

    def test_just_below_threshold_passes(self):
        gate_verdict = _require("gate_verdict")
        self.assertEqual(gate_verdict(9.9999e-6), "PASS")

    def test_just_above_threshold_fails(self):
        gate_verdict = _require("gate_verdict")
        self.assertEqual(gate_verdict(1.00001e-5), "FAIL")

    def test_well_below_threshold_passes(self):
        gate_verdict = _require("gate_verdict")
        self.assertEqual(gate_verdict(1e-8), "PASS")

    def test_well_above_threshold_fails(self):
        gate_verdict = _require("gate_verdict")
        self.assertEqual(gate_verdict(1e-2), "FAIL")

    def test_nan_fails(self):
        gate_verdict = _require("gate_verdict")
        self.assertEqual(gate_verdict(float("nan")), "FAIL")

    def test_inf_fails(self):
        gate_verdict = _require("gate_verdict")
        self.assertEqual(gate_verdict(float("inf")), "FAIL")

    def test_gate_verdict_is_never_rendered_backwards(self):
        """The design-doc §6.3 example inverts the direction (treats
        eps_H > 1e-5 as PASS). Lock the correct direction explicitly."""
        gate_verdict = _require("gate_verdict")
        self.assertEqual(gate_verdict(8.2e-6), "PASS")  # < 1e-5: PASS, not FAIL
        self.assertEqual(gate_verdict(2.0e-5), "FAIL")  # > 1e-5: FAIL, not PASS


class ScsFromEpsHTests(unittest.TestCase):
    def test_zero_eps_h_is_minus_infinity(self):
        scs_from_eps_h = _require("scs_from_eps_h")
        self.assertEqual(scs_from_eps_h(0.0), float("-inf"))

    def test_nonfinite_eps_h_is_nan_scs(self):
        scs_from_eps_h = _require("scs_from_eps_h")
        self.assertTrue(math.isnan(scs_from_eps_h(float("nan"))))
        self.assertTrue(math.isnan(scs_from_eps_h(float("inf"))))


class AggregateGateVerdictTests(unittest.TestCase):
    def test_worst_trajectory_drives_the_aggregate_verdict(self):
        aggregate_gate_verdict = _require("aggregate_gate_verdict")
        result = aggregate_gate_verdict([1e-8, 1e-6, 2.0e-5])
        self.assertEqual(result.eps_h, 2.0e-5)
        self.assertEqual(result.verdict, "FAIL")

    def test_all_trajectories_within_bound_pass(self):
        aggregate_gate_verdict = _require("aggregate_gate_verdict")
        result = aggregate_gate_verdict([1e-8, 1e-7, 1e-5])
        self.assertEqual(result.eps_h, 1e-5)
        self.assertEqual(result.verdict, "PASS")

    def test_a_single_nan_trajectory_fails_the_whole_aggregate(self):
        aggregate_gate_verdict = _require("aggregate_gate_verdict")
        result = aggregate_gate_verdict([1e-8, float("nan"), 1e-9])
        self.assertEqual(result.verdict, "FAIL")
        self.assertTrue(math.isnan(result.eps_h))


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
