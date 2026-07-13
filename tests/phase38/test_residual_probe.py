"""Contract tests for Phase 38 rung 3, the residual-on-ground-truth probe.

The RK4 fixture intentionally reimplements the softened force below.  It never
imports ``pinn.physics_residual.softened_acceleration`` so Gate B cannot pass
by sharing a production-force bug with the trajectory generator.
"""

from __future__ import annotations

import importlib
import json
import math
import pathlib
import random
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

import torch

from pinn.constants import D_CHARACTERISTIC_LENGTH, EPS_SOFT, T_CHARACTERISTIC_TIME


ROOT = pathlib.Path(__file__).resolve().parents[2]
MODULE = "pinn.verification.residual_probe"


def _load_probe():
    """Defer production import so the RED suite skips before the module exists."""
    try:
        return importlib.import_module(MODULE)
    except ImportError as exc:
        raise unittest.SkipTest(f"{MODULE} has not landed yet: {exc}") from exc


def _inline_softened_acceleration(positions: torch.Tensor, masses: torch.Tensor) -> torch.Tensor:
    """Independent test-local §3.2 force, not a production import."""
    difference = positions.unsqueeze(0) - positions.unsqueeze(1)
    squared_distance = (difference * difference).sum(dim=-1)
    safe_distance = torch.sqrt(squared_distance + EPS_SOFT * EPS_SOFT)
    weights = masses.unsqueeze(0) * safe_distance.pow(-3)
    weights = weights * (1.0 - torch.eye(3, dtype=positions.dtype))
    return (difference * weights.unsqueeze(-1)).sum(dim=1)


def _rk4_step(positions: torch.Tensor, velocities: torch.Tensor,
              masses: torch.Tensor, du: float) -> tuple[torch.Tensor, torch.Tensor]:
    """One independent fixed-step RK4 advance on the dimensionless u/r' leaf."""
    def derivative(p: torch.Tensor, v: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor]:
        return v, _inline_softened_acceleration(p, masses)

    k1_p, k1_v = derivative(positions, velocities)
    k2_p, k2_v = derivative(positions + 0.5 * du * k1_p, velocities + 0.5 * du * k1_v)
    k3_p, k3_v = derivative(positions + 0.5 * du * k2_p, velocities + 0.5 * du * k2_v)
    k4_p, k4_v = derivative(positions + du * k3_p, velocities + du * k3_v)
    return (
        positions + du * (k1_p + 2 * k2_p + 2 * k3_p + k4_p) / 6,
        velocities + du * (k1_v + 2 * k2_v + 2 * k3_v + k4_v) / 6,
    )


def _write_rk4_brutus_fixture(path: pathlib.Path, *, wrong_d: bool = False) -> pathlib.Path:
    """Create a complete Brutus-format fixture from a seeded, independent RK4 run.

    The generator is intentionally pinned to ``du=1e-3``.  It evolves in
    dimensionless ``(u, r', v')`` coordinates then writes raw Brutus columns as
    ``t=T*u``, ``r=D*r'``, and ``v=(D/T)*v'``.  ``wrong_d`` deliberately writes
    a mismatched length scale so Gate B remains falsifiable.
    """
    dtype = torch.float64
    masses = torch.ones(3, dtype=dtype)
    rng = random.Random(3804)
    angle = rng.uniform(-math.pi, math.pi)
    radius = 1.8
    omega = math.sqrt(math.sqrt(3.0) / (3.0 * radius) ** 3)
    positions = torch.tensor([
        [radius * math.cos(angle + 2 * math.pi * body / 3),
         radius * math.sin(angle + 2 * math.pi * body / 3), 0.0]
        for body in range(3)
    ], dtype=dtype)
    velocities = torch.stack((-omega * positions[:, 1], omega * positions[:, 0],
                              torch.zeros(3, dtype=dtype)), dim=1)

    du = 1e-3
    length_scale = D_CHARACTERISTIC_LENGTH * (1.7 if wrong_d else 1.0)
    lines: list[str] = []
    for step in range(1001):
        raw_time = T_CHARACTERISTIC_TIME * step * du
        lines.append(f"{raw_time:.12f} 3 0.0")
        for mass, position, velocity in zip(masses, positions, velocities):
            raw_position = position * length_scale
            raw_velocity = velocity * (length_scale / T_CHARACTERISTIC_TIME)
            lines.append(
                f"{mass.item():.12f} {raw_position[0].item():.15e} "
                f"{raw_position[1].item():.15e} {raw_position[2].item():.15e} "
                f"{raw_velocity[0].item():.15e} {raw_velocity[1].item():.15e} "
                f"{raw_velocity[2].item():.15e}"
            )
        lines.append("")
        if step < 1000:
            positions, velocities = _rk4_step(positions, velocities, masses, du)
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


class ResidualProbeTests(unittest.TestCase):
    """Gate A must be autograd-independent and Gate B must check real kinematics."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory(prefix="phase38-residual-")
        self.addCleanup(self._tmp.cleanup)
        self.tmp = pathlib.Path(self._tmp.name)
        self.fixture = _write_rk4_brutus_fixture(self.tmp / "brutus_0000.txt")

    def _evidence_root(self, name: str) -> pathlib.Path:
        return self.tmp / "evidence" / name

    def _run_cli(self, evidence_root: pathlib.Path, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, "-m", MODULE, *args, "--evidence-root", str(evidence_root)],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )

    @staticmethod
    def _only_raw(evidence_root: pathlib.Path) -> dict:
        raw_paths = sorted(evidence_root.glob("*/raw.json"))
        if len(raw_paths) != 1:
            raise AssertionError(f"expected one evidence run under {evidence_root}, found {raw_paths}")
        return json.loads(raw_paths[0].read_text(encoding="utf-8"))

    def test_cli_requires_arm_flags_and_exactly_one_trajectory_form(self):
        _load_probe()
        root = self._evidence_root("cli")
        self.assertNotEqual(self._run_cli(root, "--device", "cpu", "--path", str(self.fixture)).returncode, 0)
        self.assertNotEqual(self._run_cli(root, "--precision", "float64", "--path", str(self.fixture)).returncode, 0)
        self.assertNotEqual(self._run_cli(root, "--precision", "float64", "--device", "cpu").returncode, 0)
        self.assertNotEqual(self._run_cli(
            root, "--precision", "float64", "--device", "cpu", "--path", str(self.fixture),
            "--variant", "standard_quasi_random", "--id", "0",
        ).returncode, 0)
        self.assertNotEqual(self._run_cli(
            root, "--precision", "float64", "--device", "cpu", "--variant", "standard_quasi_random",
        ).returncode, 0)

    def test_dual_gate_pass_records_provenance_and_u_leaf_evidence(self):
        _load_probe()
        root = self._evidence_root("pass")
        completed = self._run_cli(
            root, "--precision", "float64", "--device", "cpu", "--path", str(self.fixture),
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertIn("Gate A", completed.stdout)
        self.assertIn("Gate B", completed.stdout)
        self.assertIn("PASS", completed.stdout)
        raw = self._only_raw(root)
        self.assertTrue(raw["gate_a"]["passed"])
        self.assertTrue(raw["gate_b"]["passed"])
        self.assertLess(raw["gate_a"]["max_relative_error"], 1e-5)
        self.assertLess(raw["gate_b"]["median_relative_error"], 1e-1)
        self.assertEqual(raw["provenance"]["path"], str(self.fixture))
        self.assertIn("sha256", raw["provenance"])
        self.assertEqual(raw["finite_difference"]["time_leaf"], "u = t/T")
        self.assertEqual(raw["finite_difference"]["velocity_map"], "v_raw * (T/D)")
        self.assertEqual(raw["finite_difference"]["scheme"], "central; one-sided endpoints")
        self.assertIn("mass_weighted_com_offset", raw)
        self.assertIn("excluded_snapshot_count", raw)
        run_dir = next(root.glob("*/raw.json")).parent
        self.assertTrue((run_dir / "summary.md").is_file())

    def test_gate_a_fails_when_direct_force_is_mutated_but_autograd_reference_is_not(self):
        probe = _load_probe()
        root = self._evidence_root("gate-a-mutated")
        original = probe.softened_acceleration

        def mutated_force(*args, **kwargs):
            return original(*args, **kwargs) * 1.1

        with mock.patch.object(probe, "softened_acceleration", side_effect=mutated_force):
            code = probe.main([
                "--precision", "float64", "--device", "cpu", "--path", str(self.fixture),
                "--evidence-root", str(root),
            ])
        self.assertNotEqual(code, 0)
        raw = self._only_raw(root)
        self.assertFalse(raw["gate_a"]["passed"])
        self.assertTrue(raw["gate_b"]["passed"])

    def test_gate_b_fails_for_wrong_length_scale(self):
        _load_probe()
        wrong_fixture = _write_rk4_brutus_fixture(self.tmp / "brutus_wrong_d.txt", wrong_d=True)
        root = self._evidence_root("gate-b-wrong-d")
        completed = self._run_cli(
            root, "--precision", "float64", "--device", "cpu", "--path", str(wrong_fixture),
        )
        self.assertNotEqual(completed.returncode, 0)
        raw = self._only_raw(root)
        self.assertTrue(raw["gate_a"]["passed"])
        self.assertFalse(raw["gate_b"]["passed"])
        self.assertGreater(raw["gate_b"]["median_relative_error"], 1e-1)

    def test_evidence_is_non_overwriting_and_stays_in_tmp_root(self):
        _load_probe()
        root = self._evidence_root("non-overwrite")
        first = self._run_cli(root, "--precision", "float64", "--device", "cpu", "--path", str(self.fixture))
        second = self._run_cli(root, "--precision", "float64", "--device", "cpu", "--path", str(self.fixture))
        self.assertEqual(first.returncode, 0, first.stderr)
        self.assertEqual(second.returncode, 0, second.stderr)
        raw_paths = sorted(root.glob("*/raw.json"))
        self.assertEqual(len(raw_paths), 2)
        self.assertTrue(all(path.is_relative_to(self.tmp) for path in raw_paths))


if __name__ == "__main__":
    unittest.main()
