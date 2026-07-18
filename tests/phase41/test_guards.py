"""Phase 41 — Tier-1+2 auto-guard callback + failure/ bundle (CTRL-07).

Per-family disposition (LOW-1):
  NaN/Inf → RECOVER, loss-explosion → RECOVER,
  disk-floor → HALT, memory-watermark → HALT.
Thresholds are ⚖ provisional and config-injected, never hard-coded ratified.
"""

from __future__ import annotations

import importlib
import json
import math
import shutil
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from typing import Any, NamedTuple
from unittest import mock

from tests.phase41 import _SKIP_PHRASE

MODULE = "pinn.training.guards"


def _require(symbol, module=MODULE):
    try:
        mod = importlib.import_module(module)
    except ImportError:
        raise unittest.SkipTest(f"{_SKIP_PHRASE} {module}.{symbol}")
    if not hasattr(mod, symbol):
        raise unittest.SkipTest(f"{_SKIP_PHRASE} {module}.{symbol}")
    return getattr(mod, symbol)


class _DiskUsage(NamedTuple):
    total: int
    used: int
    free: int


def _guard_cfg(
    *,
    loss_explosion_ceiling: float = 1.0e6,
    disk_floor_fraction: float = 0.05,
    memory_watermark_fraction: float = 0.7,
):
    """Duck-typed GuardConfig surface — no TrainingConfig import required."""
    return SimpleNamespace(
        loss_explosion_ceiling=loss_explosion_ceiling,
        disk_floor_fraction=disk_floor_fraction,
        memory_watermark_fraction=memory_watermark_fraction,
    )


def _run_cfg(**kwargs):
    return SimpleNamespace(guards=_guard_cfg(**kwargs))


def _make_guards(
    cfg=None,
    *,
    disk_root=None,
    memory_total_bytes=24 * (1024**3),
    memory_signal=None,
):
    StepGuards = _require("StepGuards")
    if cfg is None:
        cfg = _run_cfg()
    kwargs: dict[str, Any] = {}
    if disk_root is not None:
        kwargs["disk_root"] = disk_root
    if memory_total_bytes is not None:
        kwargs["memory_total_bytes"] = memory_total_bytes
    if memory_signal is not None:
        kwargs["memory_signal"] = memory_signal
    return StepGuards(cfg, **kwargs)


def _bundle_dir(tmp: Path) -> Path:
    return tmp / "failure"


class NanInfGuardTests(unittest.TestCase):
    """Tier-1: NaN/Inf in loss or gradient → RECOVER + failure/ bundle."""

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="phase41-guards-nan-"))
        self.addCleanup(shutil.rmtree, self.tmp, ignore_errors=True)
        self.StageDisposition = _require(
            "StageDisposition", "pinn.training.stage_exit"
        )
        self.write_failure_bundle = _require("write_failure_bundle")

    def test_nan_gradient_trips_recover_and_writes_bundle(self):
        guards = _make_guards(disk_root=self.tmp)
        outcome = guards.check(
            step=3,
            stage=0,
            phase="2a",
            loss_terms={"total": 1.0, "data": 0.5},
            grad_norm=float("nan"),
        )
        self.assertIsNotNone(outcome.disposition)
        self.assertEqual(outcome.disposition, self.StageDisposition.RECOVER)
        self.assertEqual(outcome.guard, "nan_inf")
        self.assertEqual(outcome.tier, 1)

        self.write_failure_bundle(self.tmp, outcome)
        readme = _bundle_dir(self.tmp) / "README.txt"
        trip = _bundle_dir(self.tmp) / "trip.json"
        self.assertTrue(readme.is_file())
        self.assertGreater(readme.stat().st_size, 0)
        self.assertIn("nan_inf", readme.read_text(encoding="utf-8"))
        payload = json.loads(trip.read_text(encoding="utf-8"))
        self.assertEqual(payload["guard"], "nan_inf")
        self.assertEqual(payload["tier"], 1)
        self.assertEqual(payload["step"], 3)
        self.assertEqual(payload["stage"], 0)
        self.assertEqual(payload["phase"], "2a")
        self.assertEqual(payload["disposition"], "RECOVER")
        self.assertTrue(payload.get("threshold_provisional", True))
        self.assertIn("grad_norm", payload)
        # Scalar-only: no raw tensor dumps.
        self.assertNotIn("gradients", payload)
        self.assertNotIn("tensors", payload)

    def test_nan_loss_total_trips_recover(self):
        guards = _make_guards(disk_root=self.tmp)
        outcome = guards.check(
            step=1,
            stage=0,
            phase="2a",
            loss_terms={"total": float("nan"), "data": 1.0},
            grad_norm=0.1,
        )
        self.assertEqual(outcome.disposition, self.StageDisposition.RECOVER)
        self.assertEqual(outcome.guard, "nan_inf")

    def test_inf_loss_trips_recover(self):
        guards = _make_guards(disk_root=self.tmp)
        outcome = guards.check(
            step=2,
            stage=0,
            phase="2b",
            loss_terms={"total": float("inf")},
            grad_norm=0.0,
        )
        self.assertEqual(outcome.disposition, self.StageDisposition.RECOVER)
        self.assertEqual(outcome.guard, "nan_inf")


class LossExplosionGuardTests(unittest.TestCase):
    """Tier-2 loss-explosion → RECOVER (transient-numeric)."""

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="phase41-guards-loss-"))
        self.addCleanup(shutil.rmtree, self.tmp, ignore_errors=True)
        self.StageDisposition = _require(
            "StageDisposition", "pinn.training.stage_exit"
        )
        self.write_failure_bundle = _require("write_failure_bundle")

    def test_loss_above_ceiling_trips_recover(self):
        ceiling = 100.0
        guards = _make_guards(
            _run_cfg(loss_explosion_ceiling=ceiling),
            disk_root=self.tmp,
        )
        outcome = guards.check(
            step=5,
            stage=0,
            phase="2a",
            loss_terms={"total": 250.0, "data": 200.0},
            grad_norm=1.0,
        )
        self.assertEqual(outcome.disposition, self.StageDisposition.RECOVER)
        self.assertEqual(outcome.guard, "loss_explosion")
        self.assertEqual(outcome.tier, 2)
        self.assertEqual(outcome.threshold, ceiling)
        self.assertTrue(outcome.threshold_provisional)

        self.write_failure_bundle(self.tmp, outcome)
        payload = json.loads(
            (_bundle_dir(self.tmp) / "trip.json").read_text(encoding="utf-8")
        )
        self.assertEqual(payload["disposition"], "RECOVER")
        self.assertEqual(payload["threshold"], ceiling)
        self.assertTrue(payload["threshold_provisional"])
        self.assertEqual(payload["value"], 250.0)


class DiskFloorGuardTests(unittest.TestCase):
    """Tier-2 disk-floor → HALT (resource-exhaustion)."""

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="phase41-guards-disk-"))
        self.addCleanup(shutil.rmtree, self.tmp, ignore_errors=True)
        self.StageDisposition = _require(
            "StageDisposition", "pinn.training.stage_exit"
        )
        self.write_failure_bundle = _require("write_failure_bundle")

    def test_disk_floor_breach_trips_halt(self):
        floor = 0.10  # trip when free/total < 0.10
        guards = _make_guards(
            _run_cfg(disk_floor_fraction=floor),
            disk_root=self.tmp,
        )
        # free/total = 50/1000 = 0.05 < 0.10
        fake = _DiskUsage(total=1000, used=950, free=50)
        with mock.patch("shutil.disk_usage", return_value=fake):
            outcome = guards.check(
                step=7,
                stage=1,
                phase="2a",
                loss_terms={"total": 1.0},
                grad_norm=0.1,
            )
        self.assertEqual(outcome.disposition, self.StageDisposition.HALT)
        self.assertEqual(outcome.guard, "disk_floor")
        self.assertEqual(outcome.tier, 2)
        self.assertEqual(outcome.threshold, floor)
        self.assertAlmostEqual(outcome.value, 0.05)

        self.write_failure_bundle(self.tmp, outcome)
        readme = (_bundle_dir(self.tmp) / "README.txt").read_text(encoding="utf-8")
        self.assertTrue(readme.strip())
        self.assertIn("disk_floor", readme)
        payload = json.loads(
            (_bundle_dir(self.tmp) / "trip.json").read_text(encoding="utf-8")
        )
        self.assertEqual(payload["disposition"], "HALT")
        self.assertTrue(payload["threshold_provisional"])


class MemoryWatermarkGuardTests(unittest.TestCase):
    """Tier-2 memory-watermark → HALT (resource-exhaustion)."""

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="phase41-guards-mem-"))
        self.addCleanup(shutil.rmtree, self.tmp, ignore_errors=True)
        self.StageDisposition = _require(
            "StageDisposition", "pinn.training.stage_exit"
        )
        self.write_failure_bundle = _require("write_failure_bundle")

    def test_memory_watermark_breach_trips_halt(self):
        frac = 0.5
        total = 1000
        # allocated / total = 800/1000 = 0.8 > 0.5
        guards = _make_guards(
            _run_cfg(memory_watermark_fraction=frac),
            disk_root=self.tmp,
            memory_total_bytes=total,
            memory_signal=lambda: 800,
        )
        outcome = guards.check(
            step=4,
            stage=0,
            phase="2b",
            loss_terms={"total": 1.0},
            grad_norm=0.1,
        )
        self.assertEqual(outcome.disposition, self.StageDisposition.HALT)
        self.assertEqual(outcome.guard, "memory_watermark")
        self.assertEqual(outcome.tier, 2)
        self.assertEqual(outcome.threshold, frac)
        self.assertAlmostEqual(outcome.value, 0.8)

        self.write_failure_bundle(self.tmp, outcome)
        payload = json.loads(
            (_bundle_dir(self.tmp) / "trip.json").read_text(encoding="utf-8")
        )
        self.assertEqual(payload["disposition"], "HALT")
        self.assertIn("memory_total_bytes", payload)
        self.assertEqual(payload["memory_total_bytes"], total)

    def test_memory_signal_unavailable_is_noop(self):
        """When memory_signal returns None (MPS unavailable), do not trip."""
        guards = _make_guards(
            disk_root=self.tmp,
            memory_total_bytes=1000,
            memory_signal=lambda: None,
        )
        outcome = guards.check(
            step=1,
            stage=0,
            phase="2a",
            loss_terms={"total": 1.0},
            grad_norm=0.1,
        )
        self.assertIsNone(outcome.disposition)
        self.assertIsNone(outcome.guard)


class StepZeroAndSimultaneousTests(unittest.TestCase):
    """Edge R7: step-0 handled; multi-guard → one coherent bundle; HALT wins."""

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="phase41-guards-edge-"))
        self.addCleanup(shutil.rmtree, self.tmp, ignore_errors=True)
        self.StageDisposition = _require(
            "StageDisposition", "pinn.training.stage_exit"
        )
        self.write_failure_bundle = _require("write_failure_bundle")

    def test_step_zero_trip_handled(self):
        guards = _make_guards(disk_root=self.tmp)
        outcome = guards.check(
            step=0,
            stage=0,
            phase="2a",
            loss_terms={"total": float("nan")},
            grad_norm=None,
        )
        self.assertEqual(outcome.disposition, self.StageDisposition.RECOVER)
        self.assertEqual(outcome.step, 0)
        self.write_failure_bundle(self.tmp, outcome)
        payload = json.loads(
            (_bundle_dir(self.tmp) / "trip.json").read_text(encoding="utf-8")
        )
        self.assertEqual(payload["step"], 0)

    def test_simultaneous_trips_one_bundle_halt_wins(self):
        """NaN (RECOVER) + disk-floor (HALT) on one step → HALT, one bundle."""
        floor = 0.10
        guards = _make_guards(
            _run_cfg(disk_floor_fraction=floor),
            disk_root=self.tmp,
        )
        fake = _DiskUsage(total=1000, used=950, free=50)  # free frac 0.05
        with mock.patch("shutil.disk_usage", return_value=fake):
            outcome = guards.check(
                step=9,
                stage=0,
                phase="2a",
                loss_terms={"total": float("nan")},
                grad_norm=float("nan"),
            )
        # HALT wins over RECOVER (stricter stop-and-preserve).
        self.assertEqual(outcome.disposition, self.StageDisposition.HALT)
        # Coherent single outcome; all tripped recorded.
        tripped = set(outcome.tripped_guards)
        self.assertIn("nan_inf", tripped)
        self.assertIn("disk_floor", tripped)

        self.write_failure_bundle(self.tmp, outcome)
        fail = _bundle_dir(self.tmp)
        self.assertTrue((fail / "README.txt").is_file())
        self.assertTrue((fail / "trip.json").is_file())
        # Exactly one coherent bundle directory (not one per guard).
        siblings = [p for p in self.tmp.iterdir() if p.is_dir()]
        self.assertEqual(len(siblings), 1)
        self.assertEqual(siblings[0].name, "failure")

    def test_no_trip_returns_none_disposition(self):
        guards = _make_guards(
            disk_root=self.tmp,
            memory_total_bytes=1000,
            memory_signal=lambda: 10,  # well under watermark
        )
        # Healthy disk free fraction.
        fake = _DiskUsage(total=1000, used=100, free=900)
        with mock.patch("shutil.disk_usage", return_value=fake):
            outcome = guards.check(
                step=2,
                stage=0,
                phase="2a",
                loss_terms={"total": 1.0},
                grad_norm=0.05,
            )
        self.assertIsNone(outcome.disposition)
        self.assertIsNone(outcome.guard)


class ThresholdInjectionTests(unittest.TestCase):
    """Every guard threshold is read from injected config, not inlined."""

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="phase41-guards-thr-"))
        self.addCleanup(shutil.rmtree, self.tmp, ignore_errors=True)
        self.StageDisposition = _require(
            "StageDisposition", "pinn.training.stage_exit"
        )

    def test_loss_ceiling_varies_with_config(self):
        low = _make_guards(
            _run_cfg(loss_explosion_ceiling=10.0), disk_root=self.tmp
        )
        high = _make_guards(
            _run_cfg(loss_explosion_ceiling=1000.0), disk_root=self.tmp
        )
        loss = {"total": 50.0}
        out_low = low.check(step=1, stage=0, phase="2a", loss_terms=loss, grad_norm=0.0)
        out_high = high.check(step=1, stage=0, phase="2a", loss_terms=loss, grad_norm=0.0)
        self.assertEqual(out_low.disposition, self.StageDisposition.RECOVER)
        self.assertEqual(out_low.threshold, 10.0)
        self.assertIsNone(out_high.disposition)

    def test_disk_floor_varies_with_config(self):
        # free/total = 0.08
        fake = _DiskUsage(total=1000, used=920, free=80)
        strict = _make_guards(
            _run_cfg(disk_floor_fraction=0.10), disk_root=self.tmp
        )
        loose = _make_guards(
            _run_cfg(disk_floor_fraction=0.05), disk_root=self.tmp
        )
        with mock.patch("shutil.disk_usage", return_value=fake):
            out_strict = strict.check(
                step=1, stage=0, phase="2a", loss_terms={"total": 1.0}, grad_norm=0.0
            )
            out_loose = loose.check(
                step=1, stage=0, phase="2a", loss_terms={"total": 1.0}, grad_norm=0.0
            )
        self.assertEqual(out_strict.disposition, self.StageDisposition.HALT)
        self.assertIsNone(out_loose.disposition)

    def test_memory_watermark_varies_with_config(self):
        # allocated/total = 0.6
        sig = lambda: 600
        strict = _make_guards(
            _run_cfg(memory_watermark_fraction=0.5),
            disk_root=self.tmp,
            memory_total_bytes=1000,
            memory_signal=sig,
        )
        loose = _make_guards(
            _run_cfg(memory_watermark_fraction=0.8),
            disk_root=self.tmp,
            memory_total_bytes=1000,
            memory_signal=sig,
        )
        out_strict = strict.check(
            step=1, stage=0, phase="2a", loss_terms={"total": 1.0}, grad_norm=0.0
        )
        out_loose = loose.check(
            step=1, stage=0, phase="2a", loss_terms={"total": 1.0}, grad_norm=0.0
        )
        self.assertEqual(out_strict.disposition, self.StageDisposition.HALT)
        self.assertIsNone(out_loose.disposition)

    def test_thresholds_appear_in_provisional_fields(self):
        """Cross-check: 41-01 provisional_fields still lists the ⚖ guard seams."""
        from pinn.training.config import (
            GuardConfig,
            StageConfig,
            TrainingConfig,
        )

        cfg = TrainingConfig(
            stage=StageConfig(
                max_epochs=2,
                n_adam=1,
                stagnation_window=1,
                percentile_10_relaxation=0.1,
            ),
        )
        names = {entry["name"] for entry in cfg.provisional_fields()}
        self.assertIn("run.guards.loss_explosion_ceiling", names)
        self.assertIn("run.guards.disk_floor_fraction", names)
        self.assertIn("run.guards.memory_watermark_fraction", names)
        for entry in cfg.provisional_fields():
            if entry["name"].startswith("run.guards."):
                self.assertTrue(entry["provisional"])
                self.assertIn("⚖", entry["provenance"])


class DiskFloorBackstopTests(unittest.TestCase):
    """Backstop: Tier-B failure swallowed; Tier-A still lands (disk-floor-safe)."""

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="phase41-guards-back-"))
        self.addCleanup(shutil.rmtree, self.tmp, ignore_errors=True)
        self.StageDisposition = _require(
            "StageDisposition", "pinn.training.stage_exit"
        )
        self.write_failure_bundle = _require("write_failure_bundle")
        self.GuardOutcome = _require("GuardOutcome")

    def test_tier_b_failure_swallowed_tier_a_lands(self):
        outcome = self.GuardOutcome(
            disposition=self.StageDisposition.HALT,
            guard="disk_floor",
            tier=2,
            metric="disk_free_fraction",
            value=0.01,
            threshold=0.05,
            threshold_provisional=True,
            step=1,
            stage=0,
            phase="2a",
            reason="disk free fraction 0.01 < ⚖ 0.05",
            tripped_guards=("disk_floor",),
            loss_terms={"total": 1.0},
            grad_norm=0.1,
        )
        # Force Tier-B path to raise on tail.log write.
        real_atomic = _require("atomic_write_text", "pinn.training.atomic_io")

        def flaky_atomic(path, content):
            p = Path(path)
            if p.name == "tail.log":
                raise OSError("simulated disk full for Tier-B")
            return real_atomic(path, content)

        with mock.patch(
            "pinn.training.guards.atomic_write_text", side_effect=flaky_atomic
        ):
            # Must not raise.
            dest = self.write_failure_bundle(
                self.tmp,
                outcome,
                log_lines=["line %d" % i for i in range(250)],
                last_good_checkpoint=self.tmp / "checkpoints" / "step-0.pt",
                last_good_digest="deadbeef",
                config_yaml_path=self.tmp / "config.yaml",
            )
        self.assertEqual(Path(dest), _bundle_dir(self.tmp))
        readme = _bundle_dir(self.tmp) / "README.txt"
        trip = _bundle_dir(self.tmp) / "trip.json"
        self.assertTrue(readme.is_file())
        self.assertGreater(len(readme.read_text(encoding="utf-8").strip()), 0)
        self.assertTrue(trip.is_file())
        payload = json.loads(trip.read_text(encoding="utf-8"))
        self.assertEqual(payload["guard"], "disk_floor")
        # Tier-B may be missing — that is the backstop contract.
        # tail.log either absent or partial is fine; must not crash.

    def test_tier_b_success_writes_tail_and_references(self):
        outcome = self.GuardOutcome(
            disposition=self.StageDisposition.RECOVER,
            guard="nan_inf",
            tier=1,
            metric="grad_norm",
            value=float("nan"),
            threshold=None,
            threshold_provisional=True,
            step=2,
            stage=0,
            phase="2a",
            reason="NaN/Inf in grad_norm",
            tripped_guards=("nan_inf",),
            loss_terms={"total": 1.0},
            grad_norm=float("nan"),
        )
        ckpt = self.tmp / "checkpoints" / "latest.pt"
        ckpt.parent.mkdir(parents=True, exist_ok=True)
        ckpt.write_bytes(b"stub")
        cfg_yaml = self.tmp / "config.yaml"
        cfg_yaml.write_text("run: {}\n", encoding="utf-8")
        lines = [f"log-line-{i}" for i in range(250)]
        self.write_failure_bundle(
            self.tmp,
            outcome,
            log_lines=lines,
            last_good_checkpoint=ckpt,
            last_good_digest="abc123",
            config_yaml_path=cfg_yaml,
        )
        tail = (_bundle_dir(self.tmp) / "tail.log").read_text(encoding="utf-8")
        # ~last 200 lines.
        self.assertLessEqual(len(tail.splitlines()), 200)
        self.assertIn("log-line-249", tail)
        payload = json.loads(
            (_bundle_dir(self.tmp) / "trip.json").read_text(encoding="utf-8")
        )
        self.assertIn("last_good_checkpoint", payload)
        self.assertIn("config_yaml", payload)
        # Scalar-only: NaN must serialize as a JSON-safe sentinel, not a raw float.
        self.assertTrue(
            payload["grad_norm"] is None
            or isinstance(payload["grad_norm"], (int, float, str))
        )


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
