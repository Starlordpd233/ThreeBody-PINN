"""Phase 60 (60-RESEARCH Assumption A1): the frozen L-BFGS polish on MPS float32.

No repository test or committed run had exercised ``torch.optim.LBFGS`` on the
MPS device, and the SPEC fixes MPS float32 for the polish. This smoke runs the
optimizer exactly as the frozen scorecard configures it (history size, outer-call
iteration cap and strong-Wolfe line search all read from the ``lbfgs_polish``
section) on a tiny network and on one outer call of the production network, and
proves that the optimizer state survives ``torch.save`` and
``torch.load(..., weights_only=True)``.

A failure here is not repaired in this test. The line search, the dtype and the
device are fixed by the SPEC, so a failure stops the phase for the owner: no CPU
fallback and no other line search. The MPS presence rule is the one of
``tests.phase60.test_scorer_mps``.
"""

from __future__ import annotations

import math
import tempfile
import unittest
from pathlib import Path

import torch

from pinn.architecture_spec import ArchitectureSpec
from pinn.loss_catalog import data_huber_loss
from pinn.network import build_network
from pinn.verification.feasibility_scorecard import load_scorecard
from pinn.verification.learnability_arms import SEED
from tests.phase60.test_scorer_mps import mps_device_or_stop

POINTS = 64
OUTER_CALLS = 3
TINY_SEED = 1234
MASSES = (1.0, 0.8, 0.6)


def _lbfgs(parameters):
    """An L-BFGS optimizer configured by the frozen scorecard, never by literals."""
    settings = load_scorecard().section("lbfgs_polish")
    return torch.optim.LBFGS(
        list(parameters),
        history_size=int(settings["lbfgs_history_size"]),
        max_iter=int(settings["lbfgs_max_iter"]),
        line_search_fn=str(settings["lbfgs_line_search"]),
    )


def _closure(network, objective):
    """The L-BFGS closure: clear gradients, evaluate, backpropagate, return the loss."""
    def closure():
        network.zero_grad(set_to_none=True)
        loss = objective()
        loss.backward()
        return loss
    return closure


def _outer_call(optimizer, closure):
    """One ``LBFGS.step``: the objective at the start of the call, as a float."""
    return float(optimizer.step(closure).detach())


def _parameters_are_finite(network):
    return all(bool(torch.isfinite(parameter).all()) for parameter in network.parameters())


def _tiny_network(device):
    """Two inputs, 32 tanh units, one output, float32 on ``device``; seeded weights."""
    with torch.random.fork_rng(devices=[]):
        torch.manual_seed(TINY_SEED)
        network = torch.nn.Sequential(
            torch.nn.Linear(2, 32), torch.nn.Tanh(), torch.nn.Linear(32, 1)
        )
    return network.to(device=device, dtype=torch.float32)


def _tiny_problem(device):
    """An 8 by 8 grid on [-1, 1]^2 and a smooth target on it: 64 float32 points."""
    axis = torch.linspace(-1.0, 1.0, 8)
    grid = torch.stack(torch.meshgrid(axis, axis, indexing="ij"), dim=-1).reshape(-1, 2)
    target = torch.sin(grid[:, :1] + 2.0 * grid[:, 1:])
    return grid.contiguous().to(device), target.contiguous().to(device)


def _production_problem(device):
    """64 points of a smooth three-body path with its mass-weighted centre removed.

    Returns ``(tau_ic13, masses, targets)``: the network input rows ``[tau, IC13]``,
    the masses per row and the ``(64, 3, 3)`` target positions.
    """
    u = torch.linspace(0.0, 1.0, POINTS)
    tau = (2.0 * u - 1.0).reshape(-1, 1)
    ic13 = torch.linspace(-0.9, 0.9, 13).reshape(1, 13).expand(POINTS, 13)
    tau_ic13 = torch.cat([tau, ic13], dim=1)
    masses = torch.tensor(MASSES).reshape(1, 3).expand(POINTS, 3)
    angle = 2.0 * math.pi * u.reshape(-1, 1) + torch.tensor([0.0, 2.0, 4.0]).reshape(1, 3)
    positions = torch.stack(
        [torch.cos(angle), torch.sin(angle), 0.1 * torch.sin(angle)], dim=-1
    )
    weights = masses.reshape(POINTS, 3, 1)
    positions = positions - (weights * positions).sum(dim=1, keepdim=True) / weights.sum(
        dim=1, keepdim=True
    )
    return (
        tau_ic13.contiguous().to(device),
        masses.contiguous().to(device),
        positions.contiguous().to(device),
    )


def _on_cpu(value):
    """The same nested structure with every tensor detached and moved to the CPU."""
    if isinstance(value, torch.Tensor):
        return value.detach().to("cpu")
    if isinstance(value, dict):
        return {key: _on_cpu(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return type(value)(_on_cpu(item) for item in value)
    return value


def _same_structure(left, right):
    """True when two nested optimizer states hold the same keys, tensors and numbers."""
    if isinstance(left, torch.Tensor) or isinstance(right, torch.Tensor):
        return (
            isinstance(left, torch.Tensor)
            and isinstance(right, torch.Tensor)
            and left.dtype == right.dtype
            and torch.equal(left, right)
        )
    if isinstance(left, dict) and isinstance(right, dict):
        return left.keys() == right.keys() and all(
            _same_structure(left[key], right[key]) for key in left
        )
    if isinstance(left, (list, tuple)) and isinstance(right, (list, tuple)):
        return len(left) == len(right) and all(
            _same_structure(a, b) for a, b in zip(left, right)
        )
    return left == right


class TinyNetworkLbfgsTests(unittest.TestCase):
    def setUp(self):
        self.device = mps_device_or_stop(self)
        self.network = _tiny_network(self.device)
        self.inputs, self.target = _tiny_problem(self.device)

    def _objective(self):
        return torch.nn.functional.mse_loss(self.network(self.inputs), self.target)

    def test_outer_calls_stay_finite_and_the_objective_never_increases(self):
        optimizer = _lbfgs(self.network.parameters())
        closure = _closure(self.network, self._objective)
        objectives = [_outer_call(optimizer, closure) for _ in range(OUTER_CALLS)]
        with torch.no_grad():
            final = float(self._objective())
        self.assertEqual(len(objectives), OUTER_CALLS)
        for value in objectives + [final]:
            self.assertTrue(math.isfinite(value), objectives + [final])
        for earlier, later in zip(objectives, objectives[1:] + [final]):
            self.assertLessEqual(later, earlier, objectives + [final])
        self.assertLess(final, objectives[0], objectives + [final])
        self.assertTrue(_parameters_are_finite(self.network))


class StateRoundTripTests(unittest.TestCase):
    def setUp(self):
        self.device = mps_device_or_stop(self)
        self.network = _tiny_network(self.device)
        self.inputs, self.target = _tiny_problem(self.device)

    def _objective(self):
        return torch.nn.functional.mse_loss(self.network(self.inputs), self.target)

    def test_state_survives_torch_save_and_weights_only_load_and_resumes(self):
        optimizer = _lbfgs(self.network.parameters())
        closure = _closure(self.network, self._objective)
        optimizer.step(closure)

        live = optimizer.state_dict()
        live_inner = next(iter(live["state"].values()))
        self.assertGreater(live_inner["n_iter"], 0)
        self.assertTrue(live_inner["old_dirs"], "the curvature history is empty")
        self.assertEqual(live_inner["d"].device.type, "mps")

        saved = _on_cpu(live)
        self.assertEqual(next(iter(saved["state"].values()))["d"].device.type, "cpu")
        with tempfile.TemporaryDirectory(prefix="phase60-lbfgs-") as temporary:
            path = Path(temporary) / "optimizer.state"
            torch.save(saved, path)
            loaded = torch.load(path, map_location="cpu", weights_only=True)
        self.assertTrue(_same_structure(loaded, saved))

        resumed = _lbfgs(self.network.parameters())
        resumed.load_state_dict(loaded)
        objective = _outer_call(resumed, closure)
        self.assertTrue(math.isfinite(objective), objective)
        self.assertTrue(_parameters_are_finite(self.network))


class ProductionNetworkLbfgsTests(unittest.TestCase):
    def test_one_outer_call_on_the_production_network_stays_finite(self):
        device = mps_device_or_stop(self)
        network = build_network(ArchitectureSpec(seed=SEED), dtype=torch.float32, device=device)
        tau_ic13, masses, targets = _production_problem(device)

        def objective():
            prediction = network(tau_ic13, masses).reshape(-1, 3, 3)
            return data_huber_loss(prediction, targets, dtype=torch.float32, device=device)

        optimizer = _lbfgs(network.parameters())
        start = _outer_call(optimizer, _closure(network, objective))
        with torch.no_grad():
            end = float(objective())
        self.assertTrue(math.isfinite(start), start)
        self.assertTrue(math.isfinite(end), end)
        self.assertLess(end, start)
        self.assertTrue(_parameters_are_finite(network))


if __name__ == "__main__":
    unittest.main()
