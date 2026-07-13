"""Phase 38 NET-01 foundation — locked science constants contract.

Wave-1 contract. Tests import ``pinn.constants`` inside test methods so module
compilation is the only green condition before the production module lands;
the suite turns green only when ``pinn/constants.py`` is implemented.
"""

from __future__ import annotations

import importlib
import pathlib
import unittest

ROOT_IMPORT = "pinn.constants"

# Tolerance for the raw-mass D ≃ cbrt(G T^2) cross-check (plan: 1e-3).
_D_TOL = 1e-3


def _load_constants():
    """Import the production constants module; skip if it does not exist yet.

    Wave-1 RED package: deferred-import skip guard so the suite is SKIP (not
    ERROR) until ``pinn/constants.py`` lands.
    """
    try:
        module = importlib.import_module(ROOT_IMPORT)
    except ImportError as exc:
        raise unittest.SkipTest(
            f"pinn.constants not implemented until Wave 1 production: {exc}"
        )
    return module


class ConstantsTests(unittest.TestCase):
    """Locked science constants against framework-spec formulas (CTX-15/30)."""

    def test_characteristic_length_matches_raw_mass_d(self):
        constants = _load_constants()
        # ctl_instruction.md §2.5 / PIPE-09: raw-mass D = (G T^2)^(1/3) ≈ 4.6416
        self.assertAlmostEqual(
            constants.D_CHARACTERISTIC_LENGTH, 4.6416, delta=_D_TOL
        )

    def test_characteristic_time_is_dataset_horizon(self):
        constants = _load_constants()
        # pinn_architecture.md Table 2 'Unit System': T = t_max; t_end = 10
        self.assertEqual(constants.T_CHARACTERISTIC_TIME, 10.0)

    def test_d_and_t_are_mutually_consistent_under_pipe09(self):
        constants = _load_constants()
        # PIPE-09 with G=1: D^3 = G T^2  ⇒  D ≈ cbrt(T^2)
        d = constants.D_CHARACTERISTIC_LENGTH
        t = constants.T_CHARACTERISTIC_TIME
        self.assertAlmostEqual(d, (t * t) ** (1.0 / 3.0), delta=_D_TOL)

    def test_eps_soft_is_training_plummer(self):
        constants = _load_constants()
        # pinn_architecture.md §3.2/§3.4: eps_train = 1e-5
        self.assertEqual(constants.EPS_SOFT, 1e-5)

    def test_siren_omega_defaults(self):
        constants = _load_constants()
        # pinn_architecture.md §2.2/§2.4 (ARCH-01)
        self.assertEqual(constants.SIREN_FIRST_OMEGA_0, 30.0)
        self.assertEqual(constants.SIREN_HIDDEN_OMEGA_0, 1.0)

    def test_huber_deltas(self):
        constants = _load_constants()
        # §3.1 delta_r = 1; §3.4 soft-energy delta = 1.0; §3.5 angmom delta = 1.0
        self.assertEqual(constants.HUBER_DELTA_DATA, 1.0)
        self.assertEqual(constants.HUBER_DELTA_ENERGY, 1.0)
        self.assertEqual(constants.HUBER_DELTA_ANGMOM, 1.0)

    def test_eps_l(self):
        constants = _load_constants()
        # pinn_architecture.md §3.5
        self.assertEqual(constants.EPS_L, 1e-8)

    def test_causal_weights(self):
        constants = _load_constants()
        # pinn_architecture.md §3.2 (D-04 Option A): eta_c = 1, w_1 = 1
        self.assertEqual(constants.CAUSAL_ETA_C, 1.0)
        self.assertEqual(constants.CAUSAL_W1, 1.0)

    def test_constants_are_plain_python_floats(self):
        constants = _load_constants()
        names = (
            "D_CHARACTERISTIC_LENGTH",
            "T_CHARACTERISTIC_TIME",
            "EPS_SOFT",
            "SIREN_FIRST_OMEGA_0",
            "SIREN_HIDDEN_OMEGA_0",
            "HUBER_DELTA_DATA",
            "HUBER_DELTA_ENERGY",
            "HUBER_DELTA_ANGMOM",
            "EPS_L",
            "CAUSAL_ETA_C",
            "CAUSAL_W1",
        )
        for name in names:
            value = getattr(constants, name)
            self.assertIsInstance(
                value, float, f"{name} must be a plain Python float"
            )

    def test_module_source_cites_framework_specs(self):
        """CTX-15: each constant carries an inline framework-spec citation."""
        repo_root = pathlib.Path(__file__).resolve().parents[2]
        constants_py = repo_root / "pinn" / "constants.py"
        if not constants_py.exists():
            self.skipTest("pinn/constants.py not implemented yet")
        source = constants_py.read_text(encoding="utf-8")
        # Gate-4 structural check: section-anchor / file citations present.
        required_substrings = (
            "pinn_architecture.md",
            "ctl_instruction.md",
            "§2.5",
            "PIPE-09",
            "§2.2",
            "§2.4",
            "§3.1",
            "§3.2",
            "§3.4",
            "§3.5",
            "Table 2",
            "§5.3.1",
        )
        for needle in required_substrings:
            self.assertIn(
                needle,
                source,
                f"constants.py source must cite {needle!r}",
            )

    def test_no_torch_import_required_to_read_values(self):
        constants = _load_constants()
        # Constants are dtype-agnostic pure Python; no torch needed on import.
        import ast

        repo_root = pathlib.Path(__file__).resolve().parents[2]
        constants_py = repo_root / "pinn" / "constants.py"
        if not constants_py.exists():
            self.skipTest("pinn/constants.py not implemented yet")
        tree = ast.parse(constants_py.read_text(encoding="utf-8"))
        imported = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported.extend(alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imported.append(node.module)
        self.assertFalse(
            any(name == "torch" or name.startswith("torch.") for name in imported),
            "pinn.constants must not import torch",
        )
        # Smoke: reading a value does not require torch.
        _ = constants.D_CHARACTERISTIC_LENGTH


if __name__ == "__main__":
    unittest.main()
