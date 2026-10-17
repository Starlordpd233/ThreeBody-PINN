"""Phase 59 DIAG-07 tests for JX-5, JX-2, JX-4 and JX-3. The driver is loaded by path.

CPU float64 tiny networks only. No test writes a checkpoint.
"""

from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path
from unittest import mock

import numpy as np
import torch


ROOT = Path(__file__).resolve().parents[2]
DIAG07 = ROOT / ".planning/phases/59-read-only-baseline-scorecard/evidence/diag07"
COMMON = DIAG07 / "diag07_common.py"
DRIVER = DIAG07 / "jx02_jx05.py"
_LOADED = {}


def load_driver():
    """Load jx02_jx05.py under a unique module name with its sibling library bound."""
    if "driver" in _LOADED:
        return _LOADED["driver"]
    spec = importlib.util.spec_from_file_location("phase59_diag07_common_panels", COMMON)
    common = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(common)
    with mock.patch.dict(sys.modules, {"diag07_common": common}):
        spec = importlib.util.spec_from_file_location("phase59_jx02_jx05", DRIVER)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
    _LOADED["driver"] = module
    return module


def _network(seed=3):
    from pinn.architecture_spec import ArchitectureSpec
    from pinn.network import build_network

    return build_network(
        ArchitectureSpec(seed=seed), dtype=torch.float64, device=torch.device("cpu"),
    )


def _ic13(seed=11):
    return np.random.default_rng(seed).uniform(-0.8, 0.8, size=13)


MASSES = np.array([1.0, 0.8, 0.6])
F64 = torch.float64
CPU = torch.device("cpu")


class SubsetRuleTests(unittest.TestCase):
    def test_every_sixteenth_row_of_4096(self) -> None:
        driver = load_driver()
        rows = driver.subset_rows(4096)
        self.assertEqual(rows.tolist(), list(range(0, 4096, 16)))
        self.assertEqual(rows.size, 256)
        self.assertEqual(int(rows[-1]), 4080)


class MixedDerivativeTests(unittest.TestCase):
    def test_mixed_derivative_matches_a_finite_difference_of_autograd_velocity(self) -> None:
        driver = load_driver()
        model = _network()
        ic13 = _ic13()
        u_rows = np.array([0.05, 0.37, 0.81])
        norms = driver.mixed_derivative_norms(
            model, ic13, MASSES, u_rows, dtype=F64, device=CPU,
        )
        mass = torch.as_tensor(MASSES, dtype=F64).reshape(1, 3)

        def velocity(u, ic_vector):
            def positions(u_scalar):
                tau = (2.0 * u_scalar - 1.0).reshape(1)
                inp = torch.cat([tau, ic_vector]).unsqueeze(0)
                return model(inp, mass).reshape(-1)

            return torch.func.jacrev(positions)(torch.as_tensor(u, dtype=F64))

        step = 1e-6
        for row, u in enumerate(u_rows):
            columns = []
            for slot in range(13):
                plus = torch.as_tensor(ic13, dtype=F64).clone()
                minus = plus.clone()
                plus[slot] += step
                minus[slot] -= step
                columns.append((velocity(u, plus) - velocity(u, minus)) / (2.0 * step))
            expected = float(torch.linalg.vector_norm(torch.stack(columns, dim=1).detach()))
            with self.subTest(row=row):
                self.assertLessEqual(abs(norms[row] - expected), 1e-5 * expected)

    def test_no_grad_context_gives_the_same_norms(self) -> None:
        driver = load_driver()
        model = _network()
        ic13 = _ic13()
        u_rows = np.array([0.2, 0.6])
        plain = driver.mixed_derivative_norms(model, ic13, MASSES, u_rows, dtype=F64, device=CPU)
        with torch.no_grad():
            quiet = driver.mixed_derivative_norms(model, ic13, MASSES, u_rows, dtype=F64, device=CPU)
        np.testing.assert_allclose(quiet, plain, rtol=1e-12, atol=0.0)


class SkipBranchTests(unittest.TestCase):
    def test_branches_sum_to_the_block_and_derivatives_add(self) -> None:
        driver = load_driver()
        model = _network()
        ic13 = _ic13()
        u_rows = np.array([0.1, 0.5, 0.9])
        rows, values, derivatives = driver.branch_scales(
            model, ic13, u_rows, dtype=F64, device=CPU, return_values=True,
        )
        self.assertEqual([row["hidden_layer_index"] for row in rows], [0, 2, 4, 6, 8, 10])
        self.assertEqual(tuple(values.shape[:3]), (3, 6, 3))
        torch.testing.assert_close(
            values[:, :, 0] + values[:, :, 1], values[:, :, 2], rtol=0.0, atol=1e-12,
        )
        torch.testing.assert_close(
            derivatives[:, :, 0] + derivatives[:, :, 1], derivatives[:, :, 2],
            rtol=0.0, atol=1e-10,
        )

    def test_block_outputs_follow_the_model_forward(self) -> None:
        driver = load_driver()
        model = _network()
        ic13 = _ic13()
        u = 0.42
        _rows, values, derivatives = driver.branch_scales(
            model, ic13, np.array([u]), dtype=F64, device=CPU, return_values=True,
        )
        ic = torch.as_tensor(ic13, dtype=F64)

        def hidden(u_scalar):
            tau = (2.0 * u_scalar - 1.0).reshape(1)
            x = model.input_layer(torch.cat([tau, ic]).unsqueeze(0))
            outputs = []
            for index, layer in enumerate(model.hidden_layers):
                x = layer(x)
                if index in (0, 2, 4, 6, 8, 10):
                    outputs.append(x.reshape(-1))
            return torch.stack(outputs)

        u_tensor = torch.as_tensor(u, dtype=F64)
        torch.testing.assert_close(values[0, :, 2], hidden(u_tensor), rtol=0.0, atol=1e-12)
        h = 1e-6
        numeric = (hidden(u_tensor + h) - hidden(u_tensor - h)) / (2.0 * h)
        torch.testing.assert_close(derivatives[0, :, 2], numeric, rtol=1e-5, atol=1e-6)


if __name__ == "__main__":
    unittest.main()
