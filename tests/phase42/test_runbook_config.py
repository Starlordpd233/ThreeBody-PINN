"""Phase 42 / Plan 07 — runbook config contract (OPS-01 / OPS-06)."""

from __future__ import annotations

import unittest
from pathlib import Path

from pinn.training.config import MonitorConfig, TrainingConfig
from pinn.training.config_yaml import load_config


ROOT = Path(__file__).resolve().parents[2]
CONFIG_PATH = ROOT / "configs" / "stage0-example.yaml"
RUNBOOK_PATH = (
    ROOT
    / "docs"
    / "runbooks"
    / "training"
    / "2026-07-18-stage0-training-operator-runbook.md"
)


class RunbookConfigTests(unittest.TestCase):
    """OPS-01 / OPS-06: runbook config loads and validates the operator surface."""

    def test_runbook_config_loads(self):
        config = load_config(CONFIG_PATH)

        self.assertIsInstance(config, TrainingConfig)
        self.assertEqual(config.run.log_every, 100)
        self.assertIsInstance(config.run.monitor, MonitorConfig)
        self.assertEqual(config.run.monitor.heartbeat_secs, 30)

    def test_runbook_has_mandated_sections(self):
        text = RUNBOOK_PATH.read_text(encoding="utf-8")

        for heading in (
            "## Mental Model",
            "## The Five Entry Points",
            "## Error Surface",
            "## M5-Pro Notes",
        ):
            with self.subTest(heading=heading):
                self.assertIn(heading, text)


if __name__ == "__main__":
    unittest.main()
