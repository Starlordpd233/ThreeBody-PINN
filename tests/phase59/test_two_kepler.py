"""Phase 59 (FEAS-07; D-15): the two-Kepler formula against an independent integrator."""

from __future__ import annotations

import unittest

import numpy as np

from pinn.verification import two_kepler
from tests.phase59._fixtures import hierarchical_circular


def _rk4(s0, v0, mu, t_end, step):
    """Fixed-step RK4 of r'' = -mu r / |r|^3, sampled at every whole time unit."""
    state = np.concatenate([np.asarray(s0, float), np.asarray(v0, float)])

    def rate(y):
        r = y[:3]
        return np.concatenate([y[3:], -mu * r / np.linalg.norm(r) ** 3])

    n_steps = int(round(t_end / step))
    per_unit = int(round(1.0 / step))
    samples = [state.copy()]
    for index in range(1, n_steps + 1):
        k1 = rate(state)
        k2 = rate(state + 0.5 * step * k1)
        k3 = rate(state + 0.5 * step * k2)
        k4 = rate(state + step * k3)
        state = state + (step / 6.0) * (k1 + 2.0 * k2 + 2.0 * k3 + k4)
        if index % per_unit == 0:
            samples.append(state.copy())
    return np.asarray(samples)


def _periapsis_state(e, mu, a=1.0):
    r_p = a * (1.0 - e)
    v_p = np.sqrt(mu * (1.0 + e) / (a * (1.0 - e)))
    return np.array([r_p, 0.0, 0.0]), np.array([0.0, v_p, 0.1 * v_p])


def _relative(actual, expected):
    return float(np.max(np.linalg.norm(actual - expected, axis=-1) / np.linalg.norm(expected, axis=-1)))


def _eccentric_hierarchy():
    masses = np.array([1.0, 0.8, 0.6])
    r0 = np.array([[-0.12, 0.02, 0.0], [0.18, -0.03, 0.01], [1.5, 0.4, -0.05]])
    v0 = np.array([[0.1, -1.2, 0.02], [-0.1, 1.5, -0.03], [-0.3, 1.3, 0.02]])
    return r0, v0, masses


class KeplerVsRK4Tests(unittest.TestCase):
    def test_matches_rk4_for_four_eccentricities(self) -> None:
        mu = 1.8
        times = np.arange(0.0, 10.0 + 0.5, 1.0)
        for e in (0.0, 0.1, 0.3, 0.5):
            with self.subTest(e=e):
                s0, v0 = _periapsis_state(e, mu)
                reference = _rk4(s0, v0, mu, 10.0, 1e-4)
                s, v = two_kepler.propagate_bound(s0, v0, mu, times)
                self.assertLessEqual(_relative(s, reference[:, :3]), 1e-6)
                self.assertLessEqual(_relative(v, reference[:, 3:]), 1e-6)


class IdentityTests(unittest.TestCase):
    def test_zero_elapsed_time_returns_the_initial_state(self) -> None:
        s0, v0 = _periapsis_state(0.3, 1.8)
        s, v = two_kepler.propagate_bound(s0, v0, 1.8, np.array([0.0]))
        np.testing.assert_allclose(s[0], s0, rtol=0.0, atol=1e-15)
        np.testing.assert_allclose(v[0], v0, rtol=0.0, atol=1e-15)
        r0, v0_bodies, masses = _eccentric_hierarchy()
        positions, velocities = two_kepler.two_kepler_prediction(
            r0, v0_bodies, masses, (0, 1), np.array([0.0]),
        )
        np.testing.assert_allclose(positions[0], r0, rtol=0.0, atol=1e-15)
        np.testing.assert_allclose(velocities[0], v0_bodies, rtol=0.0, atol=1e-15)


class UnboundTests(unittest.TestCase):
    def test_an_unbound_orbit_is_not_applicable(self) -> None:
        mu = 2.0
        s0 = np.array([1.0, 0.0, 0.0])
        for speed in (2.0, 3.0):
            with self.subTest(speed=speed):
                with self.assertRaises(two_kepler.NotApplicable) as caught:
                    two_kepler.propagate_bound(s0, np.array([0.0, speed, 0.0]), mu, np.array([1.0]))
                self.assertIn("unbound", caught.exception.reason)

    def test_an_unbound_outer_body_names_the_orbit(self) -> None:
        r0, v0, masses = _eccentric_hierarchy()
        v0 = v0.copy()
        v0[2] = [0.0, 6.0, 0.0]
        with self.assertRaises(two_kepler.NotApplicable) as caught:
            two_kepler.two_kepler_prediction(r0, v0, masses, (0, 1), np.array([1.0]))
        self.assertIn("outer orbit", caught.exception.reason)
        self.assertIn("unbound", caught.exception.reason)


class DecoupledFixtureTests(unittest.TestCase):
    def test_reproduces_two_exact_decoupled_orbits(self) -> None:
        times = np.linspace(0.0, 10.0, 401)
        positions, velocities = hierarchical_circular(times)
        masses = np.array([1.0, 0.8, 0.6])
        predicted, predicted_v = two_kepler.two_kepler_prediction(
            positions[0], velocities[0], masses, (0, 1), times,
        )
        scale_r = np.max(np.linalg.norm(positions, axis=-1))
        scale_v = np.max(np.linalg.norm(velocities, axis=-1))
        self.assertLessEqual(float(np.max(np.abs(predicted - positions))) / scale_r, 1e-10)
        self.assertLessEqual(float(np.max(np.abs(predicted_v - velocities))) / scale_v, 1e-10)

    def test_the_inner_pair_can_be_any_two_slots(self) -> None:
        times = np.linspace(0.0, 3.0, 31)
        positions, velocities = hierarchical_circular(times)
        masses = np.array([1.0, 0.8, 0.6])
        order = [2, 0, 1]
        predicted, _v = two_kepler.two_kepler_prediction(
            positions[0][order], velocities[0][order], masses[order], (1, 2), times,
        )
        np.testing.assert_allclose(predicted, positions[:, order], rtol=0.0, atol=1e-10)


class ConservationTests(unittest.TestCase):
    def test_momentum_and_the_centre_of_mass_motion(self) -> None:
        r0, v0, masses = _eccentric_hierarchy()
        times = np.linspace(0.0, 10.0, 257)
        positions, velocities = two_kepler.two_kepler_prediction(r0, v0, masses, (0, 1), times)
        total = float(masses.sum())
        com0 = (masses[:, None] * r0).sum(axis=0) / total
        momentum0 = (masses[:, None] * v0).sum(axis=0)
        expected_mr = total * (com0[None, :] + times[:, None] * momentum0[None, :] / total)
        np.testing.assert_allclose(
            np.einsum("i,tij->tj", masses, positions), expected_mr, rtol=0.0, atol=1e-12,
        )
        np.testing.assert_allclose(
            np.einsum("i,tij->tj", masses, velocities),
            np.broadcast_to(momentum0, (times.size, 3)), rtol=0.0, atol=1e-12,
        )


class FrameTests(unittest.TestCase):
    def test_raw_and_scaled_frames_agree(self) -> None:
        r0, v0, masses = _eccentric_hierarchy()
        T = 10.0
        D = T ** (2.0 / 3.0)
        times = np.linspace(0.0, 10.0, 51)
        raw, _raw_v = two_kepler.two_kepler_prediction(r0, v0, masses, (0, 1), times)
        scaled, _scaled_v = two_kepler.two_kepler_prediction(
            r0 / D, v0 * T / D, masses, (0, 1), times / T,
        )
        np.testing.assert_allclose(scaled * D, raw, rtol=1e-12, atol=1e-13)


class KeplerAccelerationTests(unittest.TestCase):
    def test_accelerations_are_the_second_derivative_of_the_positions(self) -> None:
        r0, v0, masses = _eccentric_hierarchy()
        h = 1e-4
        centres = np.array([0.7, 2.3, 5.1, 8.8])
        stencil = np.concatenate([centres - h, centres, centres + h])
        positions, _v = two_kepler.two_kepler_prediction(r0, v0, masses, (0, 1), stencil)
        minus, middle, plus = np.split(positions, 3)
        numeric = (plus - 2.0 * middle + minus) / h ** 2
        exact = two_kepler.two_kepler_accelerations(middle, masses, (0, 1))
        self.assertLessEqual(
            float(np.max(np.abs(exact - numeric))) / float(np.max(np.abs(exact))), 1e-6,
        )

    def test_inner_relative_acceleration_and_zero_net_force(self) -> None:
        r0, v0, masses = _eccentric_hierarchy()
        times = np.linspace(0.0, 10.0, 33)
        positions, _v = two_kepler.two_kepler_prediction(r0, v0, masses, (0, 1), times)
        acc = two_kepler.two_kepler_accelerations(positions, masses, (0, 1))
        s = positions[:, 1] - positions[:, 0]
        expected = -(masses[0] + masses[1]) * s / np.linalg.norm(s, axis=-1, keepdims=True) ** 3
        np.testing.assert_allclose(acc[:, 1] - acc[:, 0], expected, rtol=1e-12, atol=0.0)
        np.testing.assert_allclose(
            np.einsum("i,tij->tj", masses, acc), np.zeros((times.size, 3)), rtol=0.0, atol=1e-12,
        )

    def test_the_residual_column_never_changes_the_score(self) -> None:
        from pinn.verification import baselines
        from pinn.verification.feasibility_scorecard import load_scorecard
        from pinn.verification.feasibility_scorer import physics_residual_context, score_trajectory

        r0, v0, masses = _eccentric_hierarchy()
        times = np.linspace(0.0, 10.0, 101)
        positions, velocities = two_kepler.two_kepler_prediction(r0, v0, masses, (0, 1), times / 10.0)
        acc = two_kepler.two_kepler_accelerations(positions, masses, (0, 1))
        reference = positions * (1.0 + 1e-6)
        scorecard = load_scorecard()
        plain = score_trajectory(
            positions, velocities, reference, masses, (0, 1), times,
            velocity_source="analytic", scorecard=scorecard, grid="gold",
        )
        with_context = baselines.with_residual_context(plain, positions, acc, masses, r_ref=2.5)
        expected = physics_residual_context(positions, acc, masses, r_ref=2.5)
        left = plain.to_json_dict()
        right = with_context.to_json_dict()
        for name in ("physics_residual_mean", "physics_residual_max"):
            left.pop(name)
            right.pop(name)
        self.assertEqual(left, right)
        self.assertEqual(with_context.physics_residual_mean, expected["mean"])
        self.assertEqual(with_context.physics_residual_max, expected["max"])


if __name__ == "__main__":
    unittest.main()
