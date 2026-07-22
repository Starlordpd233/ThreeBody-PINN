"""Phase 43 Plan 05 summary honesty and non-success backstops."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from pinn.training.summary import finalize_summary


class SummaryHonestyTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory(prefix="phase43-summary-honesty-")
        self.root = Path(self.tmp.name)
        self.header = {"run_name": "honesty", "seed": 11}

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def test_finished_summary_states_all_three_honesty_rules(self) -> None:
        finalize_summary(
            self.root,
            disposition="finished",
            header=self.header,
            final_losses={"total": 1.0},
            curriculum_path=None,
            validation_records_path=None,
            metrics_path=None,
            prior_summary_path=None,
        )
        md = (self.root / "summary.md").read_text()
        self.assertIn("Healthy validation does not mean the model works.", md)
        self.assertIn("Run-to-run comparison does not prove progress.", md)
        self.assertIn("A clean loss curve does not establish correct physics.", md)

    def test_failed_and_interrupted_summaries_are_null_only_and_skip_metric_sections(self) -> None:
        # These are deliberately malformed. The non-success early return must not
        # attempt to parse any persisted metric-bearing artifact.
        invalid = self.root / "invalid.json"
        invalid.write_text("{not json", encoding="utf-8")
        for disposition in ("failed", "interrupted"):
            with self.subTest(disposition=disposition):
                finalize_summary(
                    self.root,
                    disposition=disposition,
                    header=self.header,
                    final_losses={"total": 123.0},
                    curriculum_path=invalid,
                    validation_records_path=invalid,
                    metrics_path=invalid,
                    prior_summary_path=invalid,
                )
                payload = json.loads((self.root / "summary.json").read_text())
                md = (self.root / "summary.md").read_text()
                self.assertEqual(payload["disposition"], disposition)
                self.assertTrue(all(value is None for value in payload["final_losses"].values()))
                self.assertIsNone(payload["validation"])
                self.assertIsNone(payload["test_preview"])
                self.assertIsNone(payload["comparison"])
                self.assertEqual(payload["curriculum"], [])
                self.assertIn(f"**Status:** {disposition}", md)
                for heading in (
                    "## Final losses",
                    "## Validation summary",
                    "## Curriculum progression",
                    "## Test-set preview",
                    "## Comparison hint",
                ):
                    self.assertNotIn(heading, md)


if __name__ == "__main__":
    unittest.main()
