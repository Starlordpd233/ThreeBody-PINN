"""Phase 43 / 43-07 — pilot calibration and owner-ratified config seams."""

from __future__ import annotations

import ast
import tempfile
import unittest
from pathlib import Path

from pinn.training.config import RunConfig
from pinn.training.config_yaml import load_config, resolved_config_to_dict


_REPO_ROOT = Path(__file__).resolve().parents[2]
_STAGE0_EXAMPLE = _REPO_ROOT / "configs" / "stage0-example.yaml"
_TRAIN_SOURCE = _REPO_ROOT / "pinn" / "train.py"


def _write_config(path: Path, recover_retries: object) -> Path:
    path.write_text(
        "\n".join(
            (
                "run:",
                "  seed: 7",
                "  precision: float64",
                "  device: cpu",
                f"  recover_retries: {recover_retries}",
                "stage:",
                "  max_epochs: 2",
                "  n_adam: 2",
                "  stagnation_window: 10",
                "  percentile_10_relaxation: 0.1",
                "opt: {}",
                "loss: {}",
                "",
            )
        ),
        encoding="utf-8",
    )
    return path


class RecoverRetryConfigTests(unittest.TestCase):
    def test_yaml_accepts_and_round_trips_exact_non_negative_integer(self):
        for value in (0, 3):
            with self.subTest(value=value), tempfile.TemporaryDirectory() as tmp:
                cfg = load_config(_write_config(Path(tmp) / "config.yaml", value))

            self.assertEqual(cfg.run.recover_retries, value)
            self.assertEqual(
                resolved_config_to_dict(cfg)["run"]["recover_retries"],
                value,
            )

    def test_yaml_rejects_invalid_retry_counts(self):
        for invalid_yaml in ("-1", "true", "1.5", "'2'"):
            with self.subTest(invalid_yaml=invalid_yaml):
                with tempfile.TemporaryDirectory() as tmp:
                    path = _write_config(
                        Path(tmp) / "config.yaml",
                        invalid_yaml,
                    )
                    with self.assertRaisesRegex(ValueError, "recover_retries"):
                        load_config(path)

    def test_run_config_rejects_invalid_retry_counts(self):
        for invalid in (-1, True, 1.5, "2"):
            with self.subTest(invalid=invalid):
                with self.assertRaisesRegex(ValueError, "recover_retries"):
                    RunConfig(recover_retries=invalid)  # type: ignore[arg-type]

    def test_stage0_example_loads_with_unratified_owner_slot(self):
        config = load_config(_STAGE0_EXAMPLE)
        text = _STAGE0_EXAMPLE.read_text(encoding="utf-8")

        self.assertEqual(config.run.recover_retries, 0)
        self.assertIn("recover_retries: <owner-provided", text)
        self.assertNotIn("recover_retries: 1", text)


class TrainRecoverRetryHandoffTests(unittest.TestCase):
    def test_train_passes_exact_config_value_without_literal_bypass(self):
        tree = ast.parse(_TRAIN_SOURCE.read_text(encoding="utf-8"))
        calls = [
            node
            for node in ast.walk(tree)
            if isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id == "CurriculumController"
        ]
        self.assertEqual(len(calls), 1)
        keyword = next(
            (kw for kw in calls[0].keywords if kw.arg == "recover_retries"),
            None,
        )
        self.assertIsNotNone(keyword, "train must explicitly hand off recover_retries")
        self.assertEqual(
            ast.dump(keyword.value, include_attributes=False),
            ast.dump(
                ast.parse("config.run.recover_retries", mode="eval").body,
                include_attributes=False,
            ),
        )


if __name__ == "__main__":
    unittest.main()
