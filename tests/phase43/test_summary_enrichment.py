"""Phase 43 Plan 05 summary enrichment contract (ACC-04)."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from pinn.training.summary import finalize_summary


def _write_json(path: Path, payload: object) -> Path:
    path.write_text(json.dumps(payload) + "\n", encoding="utf-8")
    return path


def _write_jsonl(path: Path, records: list[dict[str, object]]) -> Path:
    path.write_text(
        "".join(json.dumps(record) + "\n" for record in records),
        encoding="utf-8",
    )
    return path


class SummaryEnrichmentTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory(prefix="phase43-summary-")
        self.root = Path(self.tmp.name)
        (self.root / "config.yaml").write_text("run:\n  run_name: current\n")
        self.header = {
            "run_name": "current",
            "start_utc": "2026-07-21T00:00:00+00:00",
            "end_utc": "2026-07-21T00:05:00+00:00",
            "wall_clock_secs": 300.0,
            "device": "mps",
            "precision": "fp32",
            "seed": 7,
        }
        self.losses = {
            "data": 1.0,
            "ic": 2.0,
            "phys": 3.0,
            "energy": 4.0,
            "angmom": 5.0,
            "total": 15.0,
        }

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def test_finished_summary_uses_one_payload_and_fixed_section_order(self) -> None:
        validation_path = _write_jsonl(
            self.root / "validation.jsonl",
            [
                {"step": 10, "final_val_loss": 3.5, "trend": "unavailable"},
                {"step": 20, "final_val_loss": 2.5, "trend": "improving"},
            ],
        )
        curriculum_path = _write_jsonl(
            self.root / "curriculum.jsonl",
            [{"stage": 0, "phase": "2a", "step": 20}],
        )
        metrics_path = _write_json(
            self.root / "metrics.json",
            {
                "eps_h": 8.0e-6,
                "scs": -5.09691,
                "verdict": "PASS",
                "n_test_trajectories": 4,
            },
        )
        prior_path = _write_json(
            self.root / "prior-summary.json",
            {
                "disposition": "finished",
                "run_name": "seed-3",
                "test_preview": {"eps_h": 9.0e-6, "scs": -5.04576, "verdict": "PASS"},
            },
        )

        finalize_summary(
            self.root,
            disposition="finished",
            header=self.header,
            final_losses=self.losses,
            curriculum_path=curriculum_path,
            validation_records_path=validation_path,
            metrics_path=metrics_path,
            prior_summary_path=prior_path,
        )

        payload = json.loads((self.root / "summary.json").read_text())
        md = (self.root / "summary.md").read_text()
        self.assertEqual(
            payload["validation"],
            {"final_val_loss": 2.5, "trend": "improving", "step": 20},
        )
        self.assertEqual(payload["test_preview"]["eps_h"], 8.0e-6)
        self.assertEqual(payload["test_preview"]["verdict"], "PASS")
        self.assertEqual(payload["comparison"]["prior_run_name"], "seed-3")
        self.assertEqual(payload["comparison"]["prior_eps_h"], 9.0e-6)

        headings = [
            "## Run header",
            "## Final losses",
            "## Validation summary",
            "## Curriculum progression",
            "## Test-set preview",
            "## Comparison hint",
            "## Honesty notes",
        ]
        offsets = [md.index(heading) for heading in headings]
        self.assertEqual(offsets, sorted(offsets))
        self.assertIn("final_val_loss: 2.5", md)
        self.assertIn("eps_H: 8e-06", md)
        self.assertIn("prior_run: seed-3", md)

    def test_missing_persisted_inputs_are_unavailable_and_empty_curriculum_is_named(self) -> None:
        finalize_summary(
            self.root,
            disposition="finished",
            header=self.header,
            final_losses=self.losses,
            curriculum_path=self.root / "missing-curriculum.jsonl",
            validation_records_path=self.root / "missing-validation.jsonl",
            metrics_path=self.root / "missing-metrics.json",
            prior_summary_path=self.root / "missing-prior.json",
        )

        payload = json.loads((self.root / "summary.json").read_text())
        md = (self.root / "summary.md").read_text()
        self.assertIsNone(payload["validation"])
        self.assertIsNone(payload["test_preview"])
        self.assertIsNone(payload["comparison"])
        self.assertIn("(validation records unavailable)", md)
        self.assertIn("(no curriculum records)", md)
        self.assertIn("(test metrics unavailable)", md)
        self.assertIn("(named prior summary unavailable)", md)


if __name__ == "__main__":
    unittest.main()
