"""Phase 38 / NET-02 — mass-weighted COM projection head test contract.

Wave 2 contract. Tests import ``pinn.com_projection`` (and, for the
forward-path / no-unprojected-consumption structural tests, ``pinn.network``)
inside test methods via PER-SYMBOL deferred imports, so the suite SKIPs
cleanly (never ERRORs) before the production modules land. The project_com
tests turn green at task 38-02-02; the network-dependent structural tests turn
green at task 38-02-03.

Grounding:
  * pinn_architecture.md §5.3 (output frame / hard mass-weighted COM head,
    ``R_COM = sum_j m_j r~_j / sum_j m_j``; ``r_i = r~_i - R_COM``).
  * pinn_architecture.md §10.2 (COM invariance pass criterion
    ``abs(COM) < 1e-10``).
  * .claude/rules/pinn-reference.md (raw ordered masses; tanh-normalized IC13
    mass slots mean raw masses are unrecoverable from the network input).

The projection consumes RAW ordered masses supplied explicitly by the caller
and must handle UNEQUAL (hierarchical) masses — an equal-mass fixture alone
would mask a wrong (plain-mean) projection (cycle-1 HIGH #2 / H1, H2).
"""

import importlib
import math
import unittest

COM_MODULE = "pinn.com_projection"
NETWORK_MODULE = "pinn.network"
RUNTIME_MODULE = "pinn.runtime"


def _load_torch():
    """Import torch; skip cleanly if it is not installed."""
    try:
        import torch
    except ImportError as exc:
        raise unittest.SkipTest(f"torch not installed: {exc}")
    return torch


def _load_runtime():
    try:
        return importlib.import_module(RUNTIME_MODULE)
    except ImportError as exc:
        raise unittest.SkipTest(f"{RUNTIME_MODULE} not implemented: {exc}")


def _require(symbol_name, module_name):
    """Per-symbol deferred import. SkipTest if module OR symbol is absent.

    Per-symbol granularity lets the com_projection-before-network step SKIP
    the not-yet-implemented network-dependent tests rather than ERRORing.
    """
    try:
        module = importlib.import_module(module_name)
    except ImportError as exc:
        raise unittest.SkipTest(f"{module_name} not implemented yet: {exc}")
    if not hasattr(module, symbol_name):
        raise unittest.SkipTest(
            f"{module_name}.{symbol_name} not implemented yet")
    return getattr(module, symbol_name)


def _unequal_masses(torch, dtype, device):
    """Hierarchical-style raw masses (0.1, 1.0, 2.4) on the resolved runtime."""
    return torch.as_tensor((0.1, 1.0, 2.4), dtype=dtype, device=device)


def _equal_masses(torch, dtype, device):
    return torch.as_tensor((1.0, 1.0, 1.0), dtype=dtype, device=device)


class ProjectComCoreTests(unittest.TestCase):
    """§5.3 / §10.2 — pure, idempotent, mass-weighted COM subtraction."""

    def test_project_com_zero_com_fp64(self):
        torch = _load_torch()
        project_com = _require("project_com", COM_MODULE)
        runtime = _load_runtime()
        spec = runtime.resolve_runtime("float64", "cpu")
        positions = torch.randn(9, dtype=spec.dtype, device=spec.torch_device)
        masses = _unequal_masses(torch, spec.dtype, spec.torch_device)
        projected = project_com(positions, masses,
                                dtype=spec.dtype, device=spec.torch_device)
        # Reshape to (3 bodies, 3 dims) and verify mass-weighted COM ~ 0.
        p3 = projected.reshape(3, 3)
        com = (masses.unsqueeze(-1) * p3).sum(dim=0) / masses.sum()
        self.assertLess(com.abs().max().item(), 1e-10,
                        "fp64 mass-weighted COM must vanish (< 1e-10, §10.2)")

    def test_project_com_zero_com_fp32(self):
        torch = _load_torch()
        project_com = _require("project_com", COM_MODULE)
        runtime = _load_runtime()
        spec = runtime.resolve_runtime("float32", "mps")
        if not torch.backends.mps.is_available():
            self.skipTest("MPS unavailable")
        positions = torch.randn(9, dtype=spec.dtype, device=spec.torch_device)
        masses = _unequal_masses(torch, spec.dtype, spec.torch_device)
        projected = project_com(positions, masses,
                                dtype=spec.dtype, device=spec.torch_device)
        p3 = projected.reshape(3, 3)
        com = (masses.unsqueeze(-1) * p3).sum(dim=0) / masses.sum()
        # fp32 tolerance is looser than the fp64 §10.2 bound (documented).
        self.assertLess(com.abs().max().item(), 1e-4,
                        "fp32 mass-weighted COM must vanish within fp32 tol")

    def test_project_com_is_idempotent(self):
        torch = _load_torch()
        project_com = _require("project_com", COM_MODULE)
        runtime = _load_runtime()
        spec = runtime.resolve_runtime("float64", "cpu")
        positions = torch.randn(9, dtype=spec.dtype, device=spec.torch_device)
        masses = _unequal_masses(torch, spec.dtype, spec.torch_device)
        once = project_com(positions, masses,
                           dtype=spec.dtype, device=spec.torch_device)
        twice = project_com(once, masses,
                            dtype=spec.dtype, device=spec.torch_device)
        self.assertTrue(torch.allclose(once, twice, atol=1e-12, rtol=0),
                        "double projection must be a fixed point (idempotent)")

    def test_project_com_equal_mass_equals_plain_mean(self):
        torch = _load_torch()
        project_com = _require("project_com", COM_MODULE)
        runtime = _load_runtime()
        spec = runtime.resolve_runtime("float64", "cpu")
        positions = torch.randn(9, dtype=spec.dtype, device=spec.torch_device)
        equal = _equal_masses(torch, spec.dtype, spec.torch_device)
        projected = project_com(positions, equal,
                                dtype=spec.dtype, device=spec.torch_device)
        # With equal masses the mass-weighted COM reduces to the plain mean.
        p3 = positions.reshape(3, 3)
        plain_mean = p3 - p3.mean(dim=0, keepdim=True)
        self.assertTrue(
            torch.allclose(projected.reshape(3, 3), plain_mean,
                           atol=1e-12, rtol=0),
            "equal-mass projection must equal the plain unweighted mean")

    def test_project_com_unequal_mass_uses_weighting(self):
        torch = _load_torch()
        project_com = _require("project_com", COM_MODULE)
        runtime = _load_runtime()
        spec = runtime.resolve_runtime("float64", "cpu")
        positions = torch.randn(9, dtype=spec.dtype, device=spec.torch_device)
        unequal = _unequal_masses(torch, spec.dtype, spec.torch_device)
        equal = _equal_masses(torch, spec.dtype, spec.torch_device)
        out_unequal = project_com(positions, unequal,
                                  dtype=spec.dtype, device=spec.torch_device)
        out_equal = project_com(positions, equal,
                                dtype=spec.dtype, device=spec.torch_device)
        # For a generic input the unequal-mass projection must DIFFER from the
        # equal-mass (plain-mean) projection — proving the mass weighting is
        # actually applied, not silently replaced by a plain mean.
        self.assertFalse(
            torch.allclose(out_unequal, out_equal, atol=1e-9, rtol=0),
            "unequal-mass projection must differ from equal-mass projection")

    def test_project_com_runs_fp64_cpu(self):
        torch = _load_torch()
        project_com = _require("project_com", COM_MODULE)
        runtime = _load_runtime()
        spec = runtime.resolve_runtime("float64", "cpu")
        positions = torch.randn(9, dtype=spec.dtype, device=spec.torch_device)
        masses = _unequal_masses(torch, spec.dtype, spec.torch_device)
        out = project_com(positions, masses,
                          dtype=spec.dtype, device=spec.torch_device)
        self.assertEqual(tuple(out.shape), (9,))
        self.assertTrue(torch.isfinite(out).all().item())

    def test_project_com_runs_fp32_mps(self):
        torch = _load_torch()
        project_com = _require("project_com", COM_MODULE)
        runtime = _load_runtime()
        spec = runtime.resolve_runtime("float32", "mps")
        if not torch.backends.mps.is_available():
            self.skipTest("MPS unavailable")
        positions = torch.randn(9, dtype=spec.dtype, device=spec.torch_device)
        masses = _unequal_masses(torch, spec.dtype, spec.torch_device)
        out = project_com(positions, masses,
                          dtype=spec.dtype, device=spec.torch_device)
        self.assertEqual(tuple(out.shape), (9,))
        self.assertTrue(torch.isfinite(out).all().item())

    def test_project_com_batched_input(self):
        torch = _load_torch()
        project_com = _require("project_com", COM_MODULE)
        runtime = _load_runtime()
        spec = runtime.resolve_runtime("float64", "cpu")
        n = 5
        positions = torch.randn(n, 9, dtype=spec.dtype, device=spec.torch_device)
        masses = _unequal_masses(torch, spec.dtype, spec.torch_device)
        out = project_com(positions, masses,
                          dtype=spec.dtype, device=spec.torch_device)
        self.assertEqual(tuple(out.shape), (n, 9))
        # Per-sample mass-weighted COM must vanish for each row.
        p3 = out.reshape(n, 3, 3)
        com = (masses.unsqueeze(-1) * p3).sum(dim=1) / masses.sum()
        self.assertLess(com.abs().max().item(), 1e-10,
                        "batched per-sample COM must vanish (< 1e-10)")

    def test_project_com_batched_per_sample_masses(self):
        torch = _load_torch()
        project_com = _require("project_com", COM_MODULE)
        runtime = _load_runtime()
        spec = runtime.resolve_runtime("float64", "cpu")
        n = 4
        positions = torch.randn(n, 9, dtype=spec.dtype, device=spec.torch_device)
        # Per-sample unequal masses (n, 3).
        masses = torch.tensor(
            [[0.1, 1.0, 2.4], [0.5, 0.5, 2.0], [1.0, 1.0, 1.0], [2.4, 1.0, 0.1]],
            dtype=spec.dtype, device=spec.torch_device)
        out = project_com(positions, masses,
                          dtype=spec.dtype, device=spec.torch_device)
        p3 = out.reshape(n, 3, 3)
        com = (masses.unsqueeze(-1) * p3).sum(dim=1) / masses.sum(dim=1, keepdim=True)
        self.assertLess(com.abs().max().item(), 1e-10,
                        "per-sample mass-weighted COM must vanish (< 1e-10)")


class ForwardProjectionContractTests(unittest.TestCase):
    """NET-02 / CTX-21 — forward(tau_ic13, masses) returns projected-only; the
    raw 9-dim tensor is reachable only via the explicitly named internal hook,
    and the mass weighting reaches the projection INSIDE forward (an
    unequal-mass fixture is used so an equal-mass substitute cannot pass)."""

    def _build_model(self, torch):
        build_network = _require("build_network", NETWORK_MODULE)
        ArchitectureSpec = _require("ArchitectureSpec", NETWORK_MODULE)
        runtime = _load_runtime()
        spec = runtime.resolve_runtime("float64", "cpu")
        model = build_network(ArchitectureSpec(),
                              dtype=spec.dtype, device=spec.torch_device)
        return model, spec

    def test_forward_return_equals_project_com_of_unprojected_hook(self):
        torch = _load_torch()
        model, spec = self._build_model(torch)
        tau_ic13 = torch.randn(14, dtype=spec.dtype, device=spec.torch_device)
        masses = _unequal_masses(torch, spec.dtype, spec.torch_device)
        # The public forward must equal project_com applied to the raw hook
        # output — the projection is structural, not a convention.
        self.assertTrue(hasattr(model, "_forward_unprojected"),
                        "model must expose an explicitly named internal hook "
                        "for the raw 9-dim tensor")
        raw = model._forward_unprojected(tau_ic13)
        public = model.forward(tau_ic13, masses)
        project_com = _require("project_com", COM_MODULE)
        expected = project_com(raw, masses,
                               dtype=spec.dtype, device=spec.torch_device)
        self.assertTrue(torch.allclose(public, expected, atol=1e-12, rtol=0),
                        "public forward must equal project_com(raw, masses)")

    def test_forward_mass_weighting_reaches_projection(self):
        torch = _load_torch()
        model, spec = self._build_model(torch)
        tau_ic13 = torch.randn(14, dtype=spec.dtype, device=spec.torch_device)
        unequal = _unequal_masses(torch, spec.dtype, spec.torch_device)
        equal = _equal_masses(torch, spec.dtype, spec.torch_device)
        out_unequal = model.forward(tau_ic13, unequal)
        out_equal = model.forward(tau_ic13, equal)
        # If forward IGNORED masses (used an equal-mass mean internally), these
        # two would be identical. They must differ — proving the explicitly
        # supplied masses reach the projection inside forward.
        self.assertFalse(
            torch.allclose(out_unequal, out_equal, atol=1e-9, rtol=0),
            "forward must pass the explicitly supplied masses through to the "
            "projection; unequal- and equal-mass outputs must differ")

    def test_no_public_accessor_for_unprojected_output(self):
        torch = _load_torch()
        model, spec = self._build_model(torch)
        tau_ic13 = torch.randn(14, dtype=spec.dtype, device=spec.torch_device)
        masses = _unequal_masses(torch, spec.dtype, spec.torch_device)
        public = model.forward(tau_ic13, masses)
        raw = model._forward_unprojected(tau_ic13)
        # The public forward output must NOT equal the raw (unprojected)
        # tensor — the projection materially changes the output.
        self.assertFalse(
            torch.allclose(public, raw, atol=1e-9, rtol=0),
            "public forward must return the PROJECTED output, not the raw")
        # The raw hook is the explicitly private (leading-underscore) name.
        self.assertTrue(callable(getattr(model, "_forward_unprojected", None)),
                        "raw output must be exposed only via a private hook")


if __name__ == "__main__":
    unittest.main()
