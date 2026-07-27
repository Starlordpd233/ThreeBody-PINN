"""Self-check for the Phase 46 dataset-free fixtures (plan 46-01, Task 2).

Proves the dual-frame generator emits the SAME physical trajectory in two locked
encodings that are each force-consistent and mutually separable — so the CONF-01
probe's arm-identification tests (plan 46-02) measure something real rather than
comparing two arbitrary arrays.

This module exercises FIXTURES ONLY: its sole production import is
``pinn.constants`` (which already exists), and it computes the Newtonian
acceleration inline with the matched-Plummer softened pair form rather than
importing it. It therefore never uses the ``_SKIP_PHRASE`` deferred-skip
convention — every test must run and pass, with zero skips.
"""

from __future__ import annotations

import unittest

import numpy as np

from pinn.constants import D_CHARACTERISTIC_LENGTH, T_CHARACTERISTIC_TIME

from tests.phase46._fixtures import (
    DualFrameTrajectory,
    make_com_offset_trajectory,
    make_degenerate_trajectory,
    make_dual_frame_trajectory,
    make_empty_source,
    make_pairing_confound_trajectory,
    make_stub_split_sources,
)


# Matched-Plummer potential-only softening (gate_metrics.py EPS_INV). NEVER the
# training-time loss-side softening constant from pinn.constants.
_SOFTENING = 1e-10


def _central_second_difference(positions, h):
    """Interior central second difference ``d2r/dt2`` (one-sided-free)."""
    return (positions[2:] - 2.0 * positions[1:-1] + positions[:-2]) / (h * h)


def _newton_acceleration(positions, masses, eps_inv=_SOFTENING):
    """Matched-Plummer softened Newtonian acceleration (G = 1).

    ``a_i = sum_{j != i} m_j (r_j - r_i) / (|r_j - r_i|^2 + eps_inv^2)^(3/2)`` —
    the SAME matched-Plummer pair form as ``gate_metrics`` (``r_safe = sqrt(|dr|^2
    + eps_inv^2)``), never an additive softening.
    """
    acc = np.zeros_like(positions)
    eps_sq = eps_inv * eps_inv
    for i in range(3):
        for j in range(3):
            if i == j:
                continue
            delta = positions[:, j, :] - positions[:, i, :]
            r_sq = (delta * delta).sum(axis=-1, keepdims=True) + eps_sq
            acc[:, i, :] += masses[j] * delta / (r_sq * np.sqrt(r_sq))
    return acc


def _interior_residual(positions, times, masses):
    """Max interior norm of ``d2r/dt2 - a_newton(r, m)`` for a (positions, times) pair."""
    h = float(times[1] - times[0])
    finite_difference = _central_second_difference(positions, h)
    force = _newton_acceleration(positions[1:-1], masses)
    diff = finite_difference - force
    norms = np.linalg.norm(diff.reshape(diff.shape[0], -1), axis=-1)
    return float(norms.max())


def _cross_frame_residual(positions_raw, times_scaled, masses):
    """Residual of the RAW arrays evaluated under the scaled-frame law.

    Differenced over the normalized time ``u = t/T`` but compared to the
    Newtonian acceleration of the raw positions — i.e. treating raw ``r`` as if it
    were ``r'``.
    """
    h_u = float(times_scaled[1] - times_scaled[0])
    finite_difference = _central_second_difference(positions_raw, h_u)
    force = _newton_acceleration(positions_raw[1:-1], masses)
    diff = finite_difference - force
    norms = np.linalg.norm(diff.reshape(diff.shape[0], -1), axis=-1)
    return float(norms.max())


class DualFrameForceConsistencyTest(unittest.TestCase):
    """Both matched frames are force-consistent; the two frames are separable."""

    @classmethod
    def setUpClass(cls):
        cls.trajectory = make_dual_frame_trajectory()

    def test_raw_frame_force_consistent(self):
        residual = _interior_residual(
            self.trajectory.positions_raw, self.trajectory.times_raw, self.trajectory.masses
        )
        self.assertLessEqual(residual, self.trajectory.finite_difference_tolerance)

    def test_scaled_frame_force_consistent(self):
        residual = _interior_residual(
            self.trajectory.positions_scaled,
            self.trajectory.times_scaled,
            self.trajectory.masses,
        )
        self.assertLessEqual(residual, self.trajectory.finite_difference_tolerance)

    def test_frames_are_separable(self):
        cross = _cross_frame_residual(
            self.trajectory.positions_raw,
            self.trajectory.times_scaled,
            self.trajectory.masses,
        )
        # Strict inequality: separability, not a fixed magnitude.
        self.assertGreater(cross, self.trajectory.finite_difference_tolerance)
        raw_matched = _interior_residual(
            self.trajectory.positions_raw, self.trajectory.times_raw, self.trajectory.masses
        )
        self.assertGreater(cross, raw_matched)

    def test_scaled_encoding_is_the_locked_transform(self):
        t = self.trajectory
        self.assertEqual(t.D, float(D_CHARACTERISTIC_LENGTH))
        self.assertEqual(t.T, float(T_CHARACTERISTIC_TIME))
        np.testing.assert_allclose(t.positions_scaled, t.positions_raw / t.D, rtol=0, atol=1e-12)
        np.testing.assert_allclose(
            t.velocities_scaled, t.velocities_raw * t.T / t.D, rtol=0, atol=1e-12
        )
        np.testing.assert_allclose(t.times_scaled, t.times_raw / t.T, rtol=0, atol=1e-12)

    def test_lagrange_com_is_stationary_at_origin(self):
        t = self.trajectory
        total_mass = t.masses.sum()
        com = (t.masses.reshape(1, 3, 1) * t.positions_raw).sum(axis=1) / total_mass
        self.assertLess(float(np.abs(com).max()), 1e-10)

    def test_tolerance_is_a_positive_finite_number(self):
        tol = self.trajectory.finite_difference_tolerance
        self.assertTrue(np.isfinite(tol))
        self.assertGreater(tol, 0.0)


class DegenerateFixtureTest(unittest.TestCase):
    def test_non_finite_positions(self):
        trajectory = make_degenerate_trajectory("non_finite")
        self.assertTrue(np.isnan(trajectory.positions_raw).any())

    def test_coincident_bodies(self):
        trajectory = make_degenerate_trajectory("coincident")
        separation = trajectory.positions_raw[:, 1, :] - trajectory.positions_raw[:, 0, :]
        self.assertLess(float(np.abs(separation).max()), 1e-14)

    def test_single_snapshot(self):
        trajectory = make_degenerate_trajectory("single_snapshot")
        self.assertEqual(trajectory.positions_raw.shape[0], 1)

    def test_empty_source_has_no_records(self):
        source = make_empty_source()
        self.assertEqual(source.record_keys(), ())


class ConfoundFixtureTest(unittest.TestCase):
    def test_pairing_confound_records_permutation(self):
        base = make_dual_frame_trajectory()
        confounded, permutation = make_pairing_confound_trajectory()
        # The confounded fixture keeps the SAME positions, rolls the mass vector.
        np.testing.assert_allclose(confounded.positions_raw, base.positions_raw, rtol=0, atol=1e-12)
        np.testing.assert_allclose(
            confounded.masses, base.masses[list(permutation)], rtol=0, atol=1e-12
        )
        self.assertNotEqual(tuple(confounded.masses), tuple(base.masses))
        self.assertEqual(len(permutation), 3)

    def test_com_offset_matches_injected_offset_and_drift(self):
        trajectory, offset, drift = make_com_offset_trajectory()
        masses = trajectory.masses
        total_mass = masses.sum()
        com = (masses.reshape(1, 3, 1) * trajectory.positions_raw).sum(axis=1) / total_mass
        np.testing.assert_allclose(com[0], offset, rtol=0, atol=1e-10)
        times = trajectory.times_raw
        measured_drift = (com[-1] - com[0]) / (times[-1] - times[0])
        np.testing.assert_allclose(measured_drift, drift, rtol=0, atol=1e-8)


class StubSourceContractTest(unittest.TestCase):
    def test_disjoint_non_empty_split_sources(self):
        train, validation = make_stub_split_sources()
        self.assertGreater(len(train.record_keys()), 0)
        self.assertGreater(len(validation.record_keys()), 0)
        self.assertTrue(set(train.record_keys()).isdisjoint(set(validation.record_keys())))

    def test_insertion_order_is_not_sorted(self):
        _, validation = make_stub_split_sources()
        keys = list(validation.records_at_or_below(0))
        self.assertNotEqual(keys, sorted(keys))


if __name__ == "__main__":
    unittest.main()
