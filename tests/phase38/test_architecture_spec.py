"""Phase 38 NET-01 foundation — frozen ArchitectureSpec contract.

Wave-1 contract. Tests import ``pinn.architecture_spec`` inside test methods so
module compilation is the only green condition before the production module
lands; the suite turns green only when ``pinn/architecture_spec.py`` exists.
"""

from __future__ import annotations

import importlib
import unittest

ROOT_IMPORT = "pinn.architecture_spec"


def _load_architecture_spec():
    """Import the production architecture_spec module; skip if missing.

    Wave-1 RED package: deferred-import skip guard so the suite is SKIP (not
    ERROR) until ``pinn/architecture_spec.py`` lands.
    """
    try:
        module = importlib.import_module(ROOT_IMPORT)
    except ImportError as exc:
        raise unittest.SkipTest(
            f"pinn.architecture_spec not implemented until Wave 1 production: {exc}"
        )
    return module


class ArchitectureSpecTests(unittest.TestCase):
    """Frozen, fail-closed, config-supplied architecture topology (CTX-18..20)."""

    def test_default_topology(self):
        mod = _load_architecture_spec()
        spec = mod.ArchitectureSpec()
        self.assertEqual(spec.input_dim, 14)
        self.assertEqual(spec.output_dim, 9)
        self.assertEqual(spec.hidden_depth, 12)
        self.assertEqual(spec.hidden_width, 256)
        self.assertEqual(spec.first_omega_0, 30.0)
        self.assertEqual(spec.hidden_omega_0, 1.0)
        self.assertIs(spec.layernorm_elementwise_affine, False)
        self.assertEqual(spec.layernorm_eps, 1e-5)
        self.assertEqual(spec.power_p, 2)
        # Alternating skip / odd-layer LayerNorm cadence (ARCH-02).
        cadence = spec.skip_cadence
        self.assertIsNotNone(cadence)
        cadence_text = cadence if isinstance(cadence, str) else str(cadence)
        self.assertIn("alternat", cadence_text.lower())
        # Seed field exists and is a documented deterministic default.
        self.assertTrue(hasattr(spec, "seed"))
        self.assertIsInstance(spec.seed, int)

    def test_siren_omega_defaults_sourced_from_constants(self):
        mod = _load_architecture_spec()
        constants = importlib.import_module("pinn.constants")
        spec = mod.ArchitectureSpec()
        self.assertEqual(spec.first_omega_0, constants.SIREN_FIRST_OMEGA_0)
        self.assertEqual(spec.hidden_omega_0, constants.SIREN_HIDDEN_OMEGA_0)

    def test_frozen_immutability(self):
        mod = _load_architecture_spec()
        spec = mod.ArchitectureSpec()
        with self.assertRaises((AttributeError, TypeError)):
            spec.input_dim = 13
        with self.assertRaises((AttributeError, TypeError)):
            spec.hidden_width = 128
        with self.assertRaises((AttributeError, TypeError)):
            spec.seed = 999

    def test_out_of_contract_input_dim_raises_naming_field(self):
        mod = _load_architecture_spec()
        with self.assertRaises(ValueError) as ctx:
            mod.ArchitectureSpec(input_dim=13)
        self.assertIn("input_dim", str(ctx.exception))

    def test_out_of_contract_output_dim_raises_naming_field(self):
        mod = _load_architecture_spec()
        with self.assertRaises(ValueError) as ctx:
            mod.ArchitectureSpec(output_dim=8)
        self.assertIn("output_dim", str(ctx.exception))

    def test_nonpositive_depth_raises_naming_field(self):
        mod = _load_architecture_spec()
        with self.assertRaises(ValueError) as ctx:
            mod.ArchitectureSpec(hidden_depth=0)
        self.assertIn("hidden_depth", str(ctx.exception))
        with self.assertRaises(ValueError) as ctx:
            mod.ArchitectureSpec(hidden_depth=-1)
        self.assertIn("hidden_depth", str(ctx.exception))

    def test_nonpositive_width_raises_naming_field(self):
        mod = _load_architecture_spec()
        with self.assertRaises(ValueError) as ctx:
            mod.ArchitectureSpec(hidden_width=-4)
        self.assertIn("hidden_width", str(ctx.exception))

    def test_wrong_power_p_raises_naming_field(self):
        mod = _load_architecture_spec()
        with self.assertRaises(ValueError) as ctx:
            mod.ArchitectureSpec(power_p=3)
        self.assertIn("power_p", str(ctx.exception))

    def test_negative_layernorm_eps_raises_naming_field(self):
        mod = _load_architecture_spec()
        with self.assertRaises(ValueError) as ctx:
            mod.ArchitectureSpec(layernorm_eps=-1e-5)
        self.assertIn("layernorm_eps", str(ctx.exception))

    def test_no_precision_or_device_field(self):
        """CTX-20: precision/device flow only through resolve_runtime."""
        mod = _load_architecture_spec()
        spec = mod.ArchitectureSpec()
        self.assertFalse(hasattr(spec, "precision"))
        self.assertFalse(hasattr(spec, "device"))
        self.assertFalse(hasattr(spec, "dtype"))
        self.assertFalse(hasattr(spec, "torch_device"))
        self.assertFalse(hasattr(spec, "requested_device"))
        # Class-level: fields tuple must not include precision/device names.
        field_names = {f.name for f in spec.__dataclass_fields__.values()}
        forbidden = {
            "precision",
            "device",
            "dtype",
            "torch_device",
            "requested_device",
        }
        self.assertTrue(
            field_names.isdisjoint(forbidden),
            f"ArchitectureSpec must not carry precision/device fields; got {field_names & forbidden}",
        )


if __name__ == "__main__":
    unittest.main()
