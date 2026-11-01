"""Plan 66-01 (EXP-01): the phase 66 catalog and its sealed-catalog contract.

Importing the phase 66 catalog leaves the sealed Phase 65 registry exactly
``locked-12``; the phase 66 registry is a fresh ``register_variant`` copy
holding ``locked-12`` then ``exp01-d1-w384-o1000``; duplicates refuse in both
directions; the EXP-01 fields match the plan (D-04, D-05, D-06) and build the
production class at 157,065 parameters on CPU float64 at seed 42 while the
architecture spec stays locked; and the catalog module imports no harness
module, so no cycle or data path exists.
"""

from __future__ import annotations

import ast
import math
import unittest
from pathlib import Path

import torch

from pinn.architecture_spec import ArchitectureSpec
from pinn.network import SQRSkipResNetSIREN
from pinn.verification import diagnostic_variants
from pinn.verification.diagnostic_phase66 import (
    EXP01_VARIANT,
    PHASE66_REGISTRY,
    REGISTRIES,
)
from pinn.verification.diagnostic_variants import LOCKED_12, REGISTRY, build_variant, register_variant

CPU = torch.device("cpu")


class Phase66CatalogTests(unittest.TestCase):
    """The phase 66 catalog: sealed identity, registration semantics, fields,
    parameter count, initialization bound and the import direction."""

    def test_importing_phase66_leaves_the_sealed_registry_unchanged(self):
        self.assertEqual(list(REGISTRY), ["locked-12"])
        self.assertIs(REGISTRY["locked-12"], LOCKED_12)
        with self.assertRaises(TypeError):
            REGISTRY["extra"] = LOCKED_12
        with self.assertRaises(TypeError):
            PHASE66_REGISTRY["extra"] = LOCKED_12

    def test_phase66_registry_is_a_register_variant_copy_and_registries_is_closed(self):
        self.assertIsNot(PHASE66_REGISTRY, REGISTRY)
        self.assertEqual(
            list(PHASE66_REGISTRY), ["locked-12", "exp01-d1-w384-o1000"]
        )
        self.assertIs(PHASE66_REGISTRY["locked-12"], LOCKED_12)
        self.assertIs(PHASE66_REGISTRY["exp01-d1-w384-o1000"], EXP01_VARIANT)
        self.assertEqual(list(REGISTRIES), ["phase66"])
        self.assertIs(REGISTRIES["phase66"], PHASE66_REGISTRY)
        with self.assertRaises(TypeError):
            REGISTRIES["phase65"] = REGISTRY

    def test_duplicates_are_refused_in_both_directions(self):
        with self.assertRaises(diagnostic_variants.VariantRefused) as locked:
            register_variant(LOCKED_12, into=PHASE66_REGISTRY)
        self.assertIn("locked-12", str(locked.exception))
        with self.assertRaises(diagnostic_variants.VariantRefused) as exp01:
            register_variant(EXP01_VARIANT, into=PHASE66_REGISTRY)
        self.assertIn("exp01-d1-w384-o1000", str(exp01.exception))

    def test_exp01_fields_match_the_plan(self):
        self.assertEqual(EXP01_VARIANT.name, "exp01-d1-w384-o1000")
        self.assertEqual(EXP01_VARIANT.time_features, "raw_tau_ic13")
        self.assertEqual(EXP01_VARIANT.depth, 1)
        self.assertEqual(EXP01_VARIANT.width, 384)
        self.assertEqual(EXP01_VARIANT.first_omega_0, 1000.0)
        self.assertEqual(EXP01_VARIANT.hidden_omega_0, 1.0)
        self.assertEqual(EXP01_VARIANT.learning_rate, 1e-4)
        self.assertEqual(EXP01_VARIANT.window_length, 10.0)

    def test_exp01_builds_the_production_class_at_the_planned_parameter_count(self):
        model = build_variant(EXP01_VARIANT, seed=42, dtype=torch.float64, device=CPU)
        parameters = sum(parameter.numel() for parameter in model.parameters())
        self.assertEqual(parameters, 157065)
        locked = build_variant(LOCKED_12, seed=42, dtype=torch.float64, device=CPU)
        self.assertEqual(
            sum(parameter.numel() for parameter in locked.parameters()), 795657
        )
        self.assertLess(parameters, 795657)
        self.assertIsInstance(model, SQRSkipResNetSIREN)
        self.assertEqual(model.input_layer.omega_0, 1000.0)
        self.assertEqual(len(model.hidden_layers), 1)

    def test_the_architecture_spec_stays_locked_at_depth_one(self):
        with self.assertRaises(ValueError):
            ArchitectureSpec(hidden_depth=1)

    def test_the_step0_first_layer_frequency_sits_in_the_planned_band(self):
        model = build_variant(EXP01_VARIANT, seed=42, dtype=torch.float64, device=CPU)
        frequencies = model.input_layer.weight[:, 0].detach().abs() * 1000.0 / math.pi
        maximum = float(frequencies.max())
        self.assertGreaterEqual(maximum, 0.95 * 1000.0 / (14 * math.pi))
        self.assertLessEqual(maximum, 1000.0 / (14 * math.pi))

    def test_the_catalog_imports_no_harness_module(self):
        forbidden = {
            "pinn.verification.diagnostic_fit",
            "pinn.verification.diagnostic_guard",
            "pinn.verification.diagnostic_data",
            "pinn.verification.diagnostic_similarity",
            "pinn.verification.diagnostic_power",
        }
        source = Path(diagnostic_variants.__file__).parent / "diagnostic_phase66.py"
        tree = ast.parse(source.read_text())
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    self.assertNotIn(alias.name, forbidden)
            elif isinstance(node, ast.ImportFrom) and node.module:
                self.assertNotIn(node.module, forbidden)
                for name in forbidden:
                    self.assertFalse(
                        node.module.startswith(f"{name}."),
                        f"the catalog imports harness module {node.module}",
                    )
