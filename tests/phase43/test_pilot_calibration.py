"""Phase 43 / 43-07 — pilot calibration and owner-ratified config seams."""

from __future__ import annotations

import ast
import json
import re
import tempfile
import unittest
from pathlib import Path

from pinn.training.config import RunConfig
from pinn.training.config_yaml import load_config, resolved_config_to_dict


_REPO_ROOT = Path(__file__).resolve().parents[2]
_STAGE0_EXAMPLE = _REPO_ROOT / "configs" / "stage0-example.yaml"
_TRAIN_SOURCE = _REPO_ROOT / "pinn" / "train.py"
_CALIBRATION = (
    _REPO_ROOT
    / ".planning"
    / "phases"
    / "43-verification-stage-0-pilot-acceptance"
    / "43-CALIBRATION.md"
)
_PILOT_EVIDENCE = _CALIBRATION.parent / "evidence" / "pilot" / "README.md"


def _load_evidence_manifest() -> dict[str, object]:
    text = _PILOT_EVIDENCE.read_text(encoding="utf-8")
    match = re.search(
        r"<!-- phase43-pilot-schema: phase43-pilot/v1 -->\s*```json\s*(.*?)\s*```",
        text,
        re.DOTALL,
    )
    if match is None:
        raise AssertionError("pilot evidence must expose the phase43-pilot/v1 JSON block")
    return json.loads(match.group(1))


def _summarize_fixture(records: list[dict[str, object]]) -> dict[str, object]:
    retained = list(records)
    completed = sum(record.get("disposition") == "finished" for record in retained)
    return {
        "records": retained,
        "completed_seed_count": completed,
        "confidence": "HIGH" if completed >= 2 else "LOW",
    }


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


class PilotCalibrationEvidenceTests(unittest.TestCase):
    def test_manifest_has_traceable_completed_seed_band_and_required_schema(self):
        manifest = _load_evidence_manifest()
        records = manifest["records"]

        self.assertEqual(manifest["schema"], "phase43-pilot/v1")
        self.assertGreaterEqual(len(records), 2)
        self.assertEqual({record["seed"] for record in records}, {41, 42, 43})
        self.assertTrue(manifest["confidence_rule"]["diverged_seeds_retained"])
        for record in records:
            with self.subTest(seed=record["seed"]):
                for field in (
                    "run_path",
                    "state",
                    "disposition",
                    "final_losses",
                    "validation",
                    "peak_memory",
                    "wall_clock_secs",
                    "final_s_per_step_ema",
                    "checkpoints",
                    "failure_files",
                    "sha256",
                ):
                    self.assertIn(field, record)
                self.assertEqual(record["steps_completed"], 300)
                self.assertTrue(record["all_steps_finite"])

        observed = _summarize_fixture(records)
        self.assertEqual(observed["completed_seed_count"], 3)
        self.assertEqual(observed["confidence"], "HIGH")
        self.assertEqual(manifest["rollup"]["confidence"], "HIGH")

    def test_diverged_fixture_is_retained_in_band(self):
        fixture = [
            {"seed": 11, "disposition": "finished"},
            {"seed": 12, "disposition": "diverged"},
        ]

        observed = _summarize_fixture(fixture)

        self.assertEqual(observed["records"], fixture)
        self.assertEqual(
            [record["seed"] for record in observed["records"]],
            [11, 12],
        )

    def test_fewer_than_two_completed_seeds_is_low_confidence(self):
        fixture = [
            {"seed": 11, "disposition": "finished"},
            {"seed": 12, "disposition": "diverged"},
            {"seed": 13, "disposition": "failed"},
        ]

        observed = _summarize_fixture(fixture)

        self.assertEqual(observed["completed_seed_count"], 1)
        self.assertEqual(observed["confidence"], "LOW")

    def test_candidates_are_observation_linked_and_await_owner_ratification(self):
        manifest = _load_evidence_manifest()
        calibration = _CALIBRATION.read_text(encoding="utf-8")
        refs = manifest["candidate_observation_refs"]

        self.assertEqual(
            set(refs),
            {
                "loss_explosion_ceiling",
                "disk_floor_fraction",
                "memory_watermark_fraction",
                "recover_retries",
            },
        )
        self.assertTrue(all(refs[field] for field in refs))
        self.assertIn("AWAITING-OWNER-RATIFICATION", calibration)
        self.assertIn("60811735040.0", calibration)
        self.assertIn("0.13837178548177084", calibration)
        self.assertIn("Owner sign-off:** pending", calibration)


if __name__ == "__main__":
    unittest.main()
