"""Network autograd path, context columns, and the velocity-source guard."""

from __future__ import annotations

import ast
import inspect
import math
import pathlib
import unittest

import numpy as np
import torch

from pinn.architecture_spec import ArchitectureSpec
from pinn.constants import EPS_SOFT, T_CHARACTERISTIC_TIME
from pinn.network import build_network
from pinn.physics_residual import componentwise_du, physics_residual, softened_acceleration
from pinn.training.config import R_REF_ARTIFACT_RELATIVE_PATH, load_frozen_r_ref_artifact
from pinn.verification import feasibility_scorer as scorer
from pinn.verification.feasibility_scorecard import load_scorecard, tier_of
from pinn.verification.feasibility_scorer import (
    ScoringInputError,
    score_trajectory,
)
from tests.phase39.test_prohibitions import executable_source_from_text
from tests.phase59._fixtures import lagrange_rotation

ROOT = pathlib.Path(__file__).resolve().parents[2]
SCORER_PATH = ROOT / "pinn" / "verification" / "feasibility_scorer.py"
_BANNED = {"compute_trajectory_gate_metrics", "compute_validation_gate"}
_REQUIRED = {"matched_plummer_hamiltonian_series", "trajectory_eps_h"}
_EXPORTS = (
    "ScoreResult",
    "ScoringInputError",
    "FRAME_NAME",
    "VELOCITY_SOURCES",
    "TIER_DEFINING_SOURCES",
    "position_errors",
    "tier_defining_error",
    "valid_horizon",
    "eps_h_from_velocities",
    "score_trajectory",
    "network_trajectory",
    "score_network",
    "fd_context_eps_h",
    "physics_residual_context",
    "load_governed_r_ref",
)
_MASSES = np.array([1.0, 0.8, 0.6], dtype=np.float64)
_IC13 = np.linspace(-0.9, 0.9, 13, dtype=np.float64)
_TIMES = np.linspace(0.0, 10.0, 41, dtype=np.float64)


def _names(text: str) -> set[str]:
    """Names in executable code.

    ``executable_source_from_text`` drops docstrings and comments, then
    strips indentation, so the stripped text is not parsed. The AST is the
    original text, restricted to lines that helper still returns.
    """
    executable_lines = set(executable_source_from_text(text).splitlines())
    tree = ast.parse(text)
    source_lines = text.splitlines()
    found: set[str] = set()
    for node in ast.walk(tree):
        lineno = getattr(node, "lineno", None)
        if lineno is None or source_lines[lineno - 1].strip() not in executable_lines:
            continue
        if isinstance(node, ast.Name):
            found.add(node.id)
        elif isinstance(node, ast.Attribute):
            found.add(node.attr)
        elif isinstance(node, ast.alias):
            found.add(node.asname or node.name.split(".")[-1])
    return found


def _model():
    return build_network(
        ArchitectureSpec(seed=7), dtype=torch.float64, device=torch.device("cpu")
    )


def _closure(model):
    ic13 = torch.as_tensor(_IC13, dtype=torch.float64, device=torch.device("cpu"))
    masses = torch.as_tensor(_MASSES, dtype=torch.float64, device=torch.device("cpu"))

    def traj(u_scalar):
        tau = (2.0 * u_scalar - 1.0).reshape(1)
        tau_ic13 = torch.cat([tau, ic13], dim=0).unsqueeze(0)
        pos = model(tau_ic13, masses.unsqueeze(0))
        return pos.reshape(3, 3)

    return traj


class AutogradVelocityTests(unittest.TestCase):
    def test_matches_componentwise_du_and_central_difference(self):
        network_trajectory = getattr(scorer, "network_trajectory", None)
        self.assertIsNotNone(network_trajectory, "network_trajectory")
        model = _model()
        model.eval()
        positions, velocities = network_trajectory(
            model,
            _IC13,
            _MASSES,
            _TIMES,
            dtype=torch.float64,
            device=torch.device("cpu"),
        )
        traj = _closure(model)
        u = torch.as_tensor(
            _TIMES / T_CHARACTERISTIC_TIME,
            dtype=torch.float64,
            device=torch.device("cpu"),
        )
        direct = torch.func.vmap(lambda s: traj(s).reshape(-1))(u)
        direct = direct.detach().cpu().numpy().reshape(-1, 3, 3)
        first, _second = componentwise_du(traj, u)
        autograd = first.detach().cpu().numpy().reshape(-1, 3, 3)
        self.assertTrue(np.allclose(positions, direct, rtol=0.0, atol=1e-12))
        self.assertTrue(np.allclose(velocities, autograd, rtol=0.0, atol=1e-12))
        step = 1e-6
        forward = torch.func.vmap(lambda s: traj(s).reshape(-1))(u + step)
        backward = torch.func.vmap(lambda s: traj(s).reshape(-1))(u - step)
        finite = ((forward - backward) / (2.0 * step)).detach().cpu().numpy().reshape(-1, 3, 3)
        finite_scale = np.linalg.norm(finite)
        self.assertLessEqual(np.linalg.norm(velocities - finite) / finite_scale, 1e-6)


class NonInterferenceTests(unittest.TestCase):
    def test_parameters_and_mode_are_unchanged(self):
        network_trajectory = getattr(scorer, "network_trajectory", None)
        self.assertIsNotNone(network_trajectory, "network_trajectory")
        for training in (True, False):
            with self.subTest(training=training):
                model = _model()
                model.train(training)
                before = [p.detach().clone() for p in model.parameters()]
                network_trajectory(
                    model,
                    _IC13,
                    _MASSES,
                    _TIMES,
                    dtype=torch.float64,
                    device=torch.device("cpu"),
                )
                for old, param in zip(before, model.parameters()):
                    self.assertTrue(torch.equal(old, param.detach()))
                    self.assertIsNone(param.grad)
                self.assertEqual(bool(model.training), training)


class ChunkingTests(unittest.TestCase):
    def test_microbatches_match_and_repeat(self):
        network_trajectory = getattr(scorer, "network_trajectory", None)
        self.assertIsNotNone(network_trajectory, "network_trajectory")
        model = _model()
        kwargs = dict(
            model=model,
            ic13=_IC13,
            masses=_MASSES,
            times=_TIMES,
            dtype=torch.float64,
            device=torch.device("cpu"),
        )
        small = network_trajectory(**kwargs, microbatch_size=7)
        large = network_trajectory(**kwargs, microbatch_size=64)
        self.assertTrue(np.allclose(small[0], large[0], rtol=0.0, atol=1e-12))
        self.assertTrue(np.allclose(small[1], large[1], rtol=0.0, atol=1e-12))
        again = network_trajectory(**kwargs, microbatch_size=64)
        self.assertTrue(np.array_equal(large[0], again[0]))
        self.assertTrue(np.array_equal(large[1], again[1]))


class ScoreNetworkTests(unittest.TestCase):
    def test_velocity_source_is_autograd(self):
        score_network = getattr(scorer, "score_network", None)
        self.assertIsNotNone(score_network, "score_network")
        model = _model()
        reference, _velocities, _omega = lagrange_rotation(_TIMES, masses=_MASSES)
        result = score_network(
            model,
            _IC13,
            _MASSES,
            reference,
            (0, 1),
            _TIMES,
            scorecard=load_scorecard(),
            dtype=torch.float64,
            device=torch.device("cpu"),
            grid="gold",
        )
        self.assertEqual(result.velocity_source, "autograd")


class FiniteDifferenceContextTests(unittest.TestCase):
    def test_context_column_is_finite_and_not_tier_defining(self):
        fd_context = getattr(scorer, "fd_context_eps_h", None)
        self.assertIsNotNone(fd_context, "fd_context_eps_h")
        positions, velocities, _omega = lagrange_rotation(_TIMES, masses=_MASSES)
        value = fd_context(positions, _TIMES / T_CHARACTERISTIC_TIME, _MASSES)
        self.assertIsInstance(value, float)
        self.assertTrue(math.isfinite(value))
        with self.assertRaises(ScoringInputError):
            score_trajectory(
                positions,
                velocities,
                positions,
                _MASSES,
                (0, 1),
                _TIMES,
                velocity_source="finite_difference_context",
                scorecard=load_scorecard(),
                grid="gold",
            )
        names = _names(inspect.getsource(fd_context))
        self.assertNotIn("score_trajectory", names)


class ResidualContextTests(unittest.TestCase):
    def test_autograd_residual_matches_the_trainer_definition(self):
        network_trajectory = getattr(scorer, "network_trajectory", None)
        physics_context = getattr(scorer, "physics_residual_context", None)
        load_r = getattr(scorer, "load_governed_r_ref", None)
        self.assertIsNotNone(network_trajectory, "network_trajectory")
        self.assertIsNotNone(physics_context, "physics_residual_context")
        self.assertIsNotNone(load_r, "load_governed_r_ref")
        model = _model()
        model.eval()
        positions, _velocities, accelerations = network_trajectory(
            model,
            _IC13,
            _MASSES,
            _TIMES,
            dtype=torch.float64,
            device=torch.device("cpu"),
            want_acceleration=True,
        )
        traj = _closure(model)
        u = torch.as_tensor(
            _TIMES / T_CHARACTERISTIC_TIME,
            dtype=torch.float64,
            device=torch.device("cpu"),
        )
        _first, second = componentwise_du(traj, u)
        expected_acc = second.detach().cpu().numpy().reshape(-1, 3, 3)
        self.assertTrue(np.allclose(accelerations, expected_acc, rtol=0.0, atol=1e-12))
        r_ref = load_r()
        artifact = load_frozen_r_ref_artifact(ROOT / R_REF_ARTIFACT_RELATIVE_PATH)
        self.assertEqual(r_ref, artifact)
        residual = physics_residual(
            traj,
            u,
            torch.as_tensor(_MASSES, dtype=torch.float64, device=torch.device("cpu")),
            dtype=torch.float64,
            device=torch.device("cpu"),
        )
        rbar = (residual**2).sum(dim=(-2, -1)) / 3.0 / r_ref
        context = physics_context(positions, accelerations, _MASSES, r_ref=r_ref)
        self.assertAlmostEqual(context["mean"], float(rbar.detach().mean()), delta=1e-12)
        self.assertAlmostEqual(context["max"], float(rbar.detach().max()), delta=1e-12)

        times = np.linspace(0.0, 1.0, 9, dtype=np.float64)
        orbit, _vel, omega = lagrange_rotation(times, masses=_MASSES)
        analytic = -omega**2 * orbit
        force = softened_acceleration(
            orbit,
            _MASSES,
            eps_soft=EPS_SOFT,
            dtype=torch.float64,
            device=torch.device("cpu"),
        )
        raw_residual = torch.as_tensor(analytic, dtype=torch.float64) - force
        self.assertLess(
            float(raw_residual.abs().max()),
            1e-8 * float(force.abs().max()),
        )
        error = torch.tensor([0.2, -0.1, 0.05], dtype=torch.float64)
        bumped = force.clone()
        bumped[:, 0, :] = bumped[:, 0, :] + error
        bumped_context = physics_context(orbit, bumped, _MASSES, r_ref=r_ref)
        expected = float(torch.dot(error, error) / 3.0 / r_ref)
        # Same formula. The two reductions differ by a unit in the last place.
        ulp = abs(expected) * np.finfo(np.float64).eps
        self.assertLessEqual(abs(bumped_context["mean"] - expected), 4.0 * ulp)
        self.assertLessEqual(abs(bumped_context["max"] - expected), 4.0 * ulp)

        score_network = getattr(scorer, "score_network", None)
        self.assertIsNotNone(score_network, "score_network")
        reference, _velocities, _omega = lagrange_rotation(_TIMES, masses=_MASSES)
        result = score_network(
            model,
            _IC13,
            _MASSES,
            reference,
            (0, 1),
            _TIMES,
            scorecard=load_scorecard(),
            dtype=torch.float64,
            device=torch.device("cpu"),
            grid="gold",
        )
        self.assertTrue(math.isfinite(result.physics_residual_mean))
        self.assertTrue(math.isfinite(result.physics_residual_max))
        self.assertEqual(result.tier, tier_of(result.E, result.eps_h, scorecard=load_scorecard()))
        replaced = result.__class__(
            **{
                **{field: getattr(result, field) for field in result.__dataclass_fields__},
                "physics_residual_mean": float("nan"),
                "physics_residual_max": float("nan"),
            }
        )
        self.assertEqual(replaced.tier, result.tier)
        self.assertNotIn("physics_residual_mean", inspect.signature(tier_of).parameters)
        self.assertNotIn("physics_residual_max", inspect.signature(tier_of).parameters)


class ScorerVelocitySourceTests(unittest.TestCase):
    def test_scorer_uses_the_gate_hamiltonian_not_the_finite_difference_gate(self):
        names = _names(SCORER_PATH.read_text(encoding="utf-8"))
        self.assertFalse(names & _BANNED)
        self.assertTrue(_REQUIRED <= names)

    def test_detector_flags_an_injected_call(self):
        injected = "compute_trajectory_gate_metrics(positions, times, masses)\n"
        self.assertIn("compute_trajectory_gate_metrics", _names(injected))
        self.assertTrue(_names(injected) & _BANNED)


class PublicSurfaceTests(unittest.TestCase):
    def test_exports_exist(self):
        for name in _EXPORTS:
            with self.subTest(name=name):
                self.assertTrue(hasattr(scorer, name), name)


if __name__ == "__main__":
    unittest.main()
