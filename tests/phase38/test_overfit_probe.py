"""Contract tests for Phase 38 rung 4, the single-trajectory overfit probe (NET-05).

Authored tests-first (38-06-01). Deferred import SKIPs until the probe lands.
Every probe invocation uses a tmp ``--evidence-root`` so the real phase evidence
tree is never polluted by the suite.
"""

from __future__ import annotations

import ast
import importlib
import json
import math
import pathlib
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

import torch

from pinn.constants import D_CHARACTERISTIC_LENGTH, T_CHARACTERISTIC_TIME


ROOT = pathlib.Path(__file__).resolve().parents[2]
MODULE = "pinn.verification.overfit_probe"
PROBE_PATH = ROOT / "pinn" / "verification" / "overfit_probe.py"
SOFT_ENERGY_NOT_EVALUATED = "not evaluated — requires Phase 39/40 metadata"
IC13_PLACEHOLDER_NOTE = (
    "zeros(13) — Phase-38 overfit smoke; physically-normalized IC13 deferred to Phase 39"
)


def _load_probe():
    try:
        return importlib.import_module(MODULE)
    except ImportError as exc:
        raise unittest.SkipTest(f"{MODULE} has not landed yet: {exc}") from exc


def _executable_source(path: pathlib.Path) -> str:
    source = path.read_text(encoding="utf-8")
    tree = ast.parse(source, filename=str(path))
    docstring_lines: set[int] = set()
    for node in ast.walk(tree):
        if isinstance(node, (ast.Module, ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
            doc = ast.get_docstring(node, clean=False)
            if doc and node.body and isinstance(node.body[0], ast.Expr):
                expr = node.body[0]
                for lineno in range(expr.lineno, (expr.end_lineno or expr.lineno) + 1):
                    docstring_lines.add(lineno)
    return "\n".join(
        line.strip()
        for lineno, line in enumerate(source.splitlines(), start=1)
        if lineno not in docstring_lines and line.strip() and not line.lstrip().startswith("#")
    )


def _write_synthetic_brutus(
    path: pathlib.Path,
    *,
    com_offset: float = 0.0,
    n_snapshots: int = 2,
) -> pathlib.Path:
    """Write a complete COM-centered (or offset) Brutus fixture under tmp.

    Spans t=0..10 so the completeness gate (final_time >= 9.5) passes. Positions
    are a simple smooth function of time so a single-trajectory overfit is
    learnable. When ``com_offset`` is nonzero every body is translated by that
    amount along +x (raw units), producing a mass-weighted COM offset.
    """
    masses = [1.0, 1.0, 1.0]
    lines: list[str] = []
    for step in range(n_snapshots):
        t = 10.0 * step / max(n_snapshots - 1, 1)
        u = t / T_CHARACTERISTIC_TIME
        # Dimensionless r' for three bodies (COM=0), then convert to raw via D.
        r_prime = [
            [1.0 * math.cos(u), 1.0 * math.sin(u), 0.0],
            [-0.5 * math.cos(u), -0.5 * math.sin(u) + 0.5, 0.0],
            [-0.5 * math.cos(u), -0.5 * math.sin(u) - 0.5, 0.0],
        ]
        # Enforce exact COM zero in r' before optional raw offset.
        cx = sum(r_prime[i][0] for i in range(3)) / 3.0
        cy = sum(r_prime[i][1] for i in range(3)) / 3.0
        for i in range(3):
            r_prime[i][0] -= cx
            r_prime[i][1] -= cy
        lines.append(f"{t:.12f} 3 0.0")
        for mass, rp in zip(masses, r_prime):
            raw = [rp[0] * D_CHARACTERISTIC_LENGTH + com_offset,
                   rp[1] * D_CHARACTERISTIC_LENGTH,
                   rp[2] * D_CHARACTERISTIC_LENGTH]
            # Rough velocities from d(r')/du * (D/T); not used by data loss.
            v_prime = [-1.0 * math.sin(u), 1.0 * math.cos(u), 0.0]
            if rp is r_prime[1]:
                v_prime = [0.5 * math.sin(u), -0.5 * math.cos(u), 0.0]
            if rp is r_prime[2]:
                v_prime = [0.5 * math.sin(u), -0.5 * math.cos(u), 0.0]
            v_raw = [v * (D_CHARACTERISTIC_LENGTH / T_CHARACTERISTIC_TIME) for v in v_prime]
            lines.append(
                f"{mass:.12f} {raw[0]:.15e} {raw[1]:.15e} {raw[2]:.15e} "
                f"{v_raw[0]:.15e} {v_raw[1]:.15e} {v_raw[2]:.15e}"
            )
        lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


class OverfitProbeTests(unittest.TestCase):
    """Rung 4: >=1e3x data-loss reduction, fail-loud, full-stack diagnostics."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory(prefix="phase38-overfit-")
        self.addCleanup(self._tmp.cleanup)
        self.tmp = pathlib.Path(self._tmp.name)
        self.fixture = _write_synthetic_brutus(self.tmp / "brutus_0000.txt")
        self.sim_data_marker = self.tmp / "simulation_data_sentinel"
        self.sim_data_marker.write_text("untouched\n", encoding="utf-8")

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
        self.assertNotEqual(
            self._run_cli(root, "--device", "cpu", "--path", str(self.fixture)).returncode, 0)
        self.assertNotEqual(
            self._run_cli(root, "--precision", "float64", "--path", str(self.fixture)).returncode, 0)
        self.assertNotEqual(
            self._run_cli(root, "--precision", "float64", "--device", "cpu").returncode, 0)
        self.assertNotEqual(self._run_cli(
            root, "--precision", "float64", "--device", "cpu", "--path", str(self.fixture),
            "--variant", "standard_quasi_random", "--id", "0",
        ).returncode, 0)
        self.assertNotEqual(self._run_cli(
            root, "--precision", "float64", "--device", "cpu",
            "--variant", "standard_quasi_random",
        ).returncode, 0)

    def test_pass_gate_records_ratio_lr_ic13_and_diagnostics(self):
        probe = _load_probe()
        root = self._evidence_root("pass")
        # Calibrated knobs for the 2-snapshot synthetic fixture: SIREN first_omega_0=30
        # converges under Adam at 1e-4 (SIREN-typical); default 1e-3 is still the CLI default.
        code = probe.main([
            "--precision", "float64", "--device", "cpu",
            "--path", str(self.fixture),
            "--evidence-root", str(root),
            "--max-steps", "5000",
            "--lr", "1e-4",
        ])
        self.assertEqual(code, 0, "expected PASS (>=1e3x data-loss reduction)")
        raw = self._only_raw(root)
        self.assertTrue(raw["passed"])
        self.assertGreaterEqual(raw["ratio"], 1e3)
        self.assertIn("initial_loss", raw)
        self.assertIn("floor_loss", raw)
        self.assertIn("steps", raw)
        self.assertEqual(raw["lr"], 1e-4)
        self.assertIn("ic13_placeholder", raw)
        self.assertIn("zeros(13)", raw["ic13_placeholder"])
        self.assertIn("Phase 39", raw["ic13_placeholder"])
        # Input-available diagnostics at initial + final must be finite numbers.
        for step_key in ("initial", "final"):
            diag = raw["diagnostics"][step_key]
            for term in ("data", "ic", "causal_physics", "angular_momentum"):
                self.assertTrue(math.isfinite(float(diag[term])), f"{step_key}.{term} not finite")
            self.assertEqual(diag["soft_energy"], SOFT_ENERGY_NOT_EVALUATED)
        self.assertTrue((next(root.glob("*/raw.json")).parent / "summary.md").is_file())
        # Nothing under the real planning evidence tree for this run (tmp root only).
        self.assertTrue(str(root).startswith(str(self.tmp)))

    def test_soft_energy_evaluated_when_eps_h_supplied(self):
        probe = _load_probe()
        root = self._evidence_root("eps-h")
        code = probe.main([
            "--precision", "float64", "--device", "cpu",
            "--path", str(self.fixture),
            "--evidence-root", str(root),
            "--max-steps", "5000",
            "--lr", "1e-4",
            "--eps-h", "1e-4",
        ])
        self.assertEqual(code, 0)
        raw = self._only_raw(root)
        for step_key in ("initial", "final"):
            se = raw["diagnostics"][step_key]["soft_energy"]
            self.assertIsInstance(se, (int, float))
            self.assertTrue(math.isfinite(float(se)))

    def test_cap_without_target_fails(self):
        probe = _load_probe()
        root = self._evidence_root("cap")
        code = probe.main([
            "--precision", "float64", "--device", "cpu",
            "--path", str(self.fixture),
            "--evidence-root", str(root),
            "--max-steps", "1",
            "--lr", "1e-3",
        ])
        self.assertNotEqual(code, 0)
        raw = self._only_raw(root)
        self.assertFalse(raw["passed"])
        self.assertEqual(raw["fail_reason"], "cap_without_target")
        self.assertIn("ratio", raw)

    def test_nan_data_loss_fails_loudly(self):
        probe = _load_probe()
        root = self._evidence_root("nan")
        original = probe.data_huber_loss
        call_count = {"n": 0}

        def nan_after_first(*args, **kwargs):
            call_count["n"] += 1
            if call_count["n"] == 1:
                return original(*args, **kwargs)
            return torch.tensor(float("nan"), dtype=torch.float64)

        with mock.patch.object(probe, "data_huber_loss", side_effect=nan_after_first):
            code = probe.main([
                "--precision", "float64", "--device", "cpu",
                "--path", str(self.fixture),
                "--evidence-root", str(root),
                "--max-steps", "10",
            ])
        self.assertNotEqual(code, 0)
        raw = self._only_raw(root)
        self.assertFalse(raw["passed"])
        self.assertEqual(raw["fail_reason"], "non_finite_data_loss")
        self.assertIn("step", raw)

    def test_non_finite_diagnostic_fails(self):
        probe = _load_probe()
        root = self._evidence_root("diag-nan")
        original = probe.causal_physics_loss

        def nan_causal(*args, **kwargs):
            return torch.tensor(float("nan"), dtype=torch.float64)

        with mock.patch.object(probe, "causal_physics_loss", side_effect=nan_causal):
            code = probe.main([
                "--precision", "float64", "--device", "cpu",
                "--path", str(self.fixture),
                "--evidence-root", str(root),
                "--max-steps", "5",
            ])
        self.assertNotEqual(code, 0)
        raw = self._only_raw(root)
        self.assertFalse(raw["passed"])
        self.assertEqual(raw["fail_reason"], "non_finite_diagnostic")
        self.assertIn("causal_physics", raw.get("fail_term", ""))

    def test_com_offset_warning_threshold(self):
        probe = _load_probe()
        # Offset large enough in raw units that r' COM exceeds 1e-3.
        offset_fixture = _write_synthetic_brutus(
            self.tmp / "brutus_offset.txt",
            com_offset=0.1 * D_CHARACTERISTIC_LENGTH,  # 0.1 in r' units
        )
        root = self._evidence_root("com-warn")
        code = probe.main([
            "--precision", "float64", "--device", "cpu",
            "--path", str(offset_fixture),
            "--evidence-root", str(root),
            "--max-steps", "5",
            "--lr", "1e-3",
            "--com-offset-warn-threshold", "1e-3",
        ])
        # Cap may FAIL; warning must be recorded either way.
        raw = self._only_raw(root)
        self.assertTrue(raw["com_offset_warning"])
        self.assertGreater(raw["mass_weighted_com_offset"], 1e-3)

        # COM=0 default does not warn.
        root2 = self._evidence_root("com-ok")
        probe.main([
            "--precision", "float64", "--device", "cpu",
            "--path", str(self.fixture),
            "--evidence-root", str(root2),
            "--max-steps", "5",
            "--lr", "1e-3",
        ])
        raw2 = self._only_raw(root2)
        self.assertFalse(raw2["com_offset_warning"])
        self.assertLess(raw2["mass_weighted_com_offset"], 1e-3)

    def test_lr_default_is_1e_minus_3(self):
        probe = _load_probe()
        root = self._evidence_root("lr-default")
        # Cap-fail path is enough to write evidence with the default LR.
        probe.main([
            "--precision", "float64", "--device", "cpu",
            "--path", str(self.fixture),
            "--evidence-root", str(root),
            "--max-steps", "1",
        ])
        raw = self._only_raw(root)
        self.assertEqual(raw["lr"], 1e-3)

    def test_source_has_no_precision_default(self):
        _load_probe()
        executable = _executable_source(PROBE_PATH)
        self.assertIn('add_argument("--precision", required=True', executable)
        self.assertNotIn('add_argument("--precision", default=', executable)
        self.assertNotIn("set_default_dtype", executable)
        self.assertNotIn("is_available", executable)

    def test_no_writes_under_simulation_data_path_string(self):
        """Evidence root must not land under simulation_data (path-form check)."""
        probe = _load_probe()
        root = self._evidence_root("no-sim")
        probe.main([
            "--precision", "float64", "--device", "cpu",
            "--path", str(self.fixture),
            "--evidence-root", str(root),
            "--max-steps", "1",
        ])
        for path in root.rglob("*"):
            self.assertNotIn("simulation_data", path.parts)


if __name__ == "__main__":
    unittest.main()
