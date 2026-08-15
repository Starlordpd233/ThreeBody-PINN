"""D-24 band-record fixture tests for Plan 50-07 Task 2."""
from __future__ import annotations

import json
import re
import tempfile
import unittest
from pathlib import Path

from tests.phase50._evidence_fixtures import (
    BAND_RECORD_REL,
    LEDGER_REL,
    SOURCE_MANIFEST_REL,
    clone_complete,
    fail_closed_message,
    fence,
    write_text,
)
from tests.phase50.test_evidence_builder import load_ledger


JSON_FENCE = re.compile(r"```json\n(.*?)\n```", re.S)
FORBIDDEN = (
    "winner",
    "statistically significant",
    "p-value",
    "confidence interval",
    "caused by",
    "design verdict",
    "ranked first",
)


class BandRecordTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.fx = clone_complete(Path(self.tmp.name) / "band")
        extracted = self.fx.extract()
        self.assertEqual(extracted.returncode, 0, extracted.stderr)

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def test_valid_three_seed_band_recomputes_and_stays_descriptive(self) -> None:
        built = self.fx.band()
        self.assertEqual(built.returncode, 0, built.stderr)
        verified = self.fx.verify(
            "band",
            ["--source-manifest", str(SOURCE_MANIFEST_REL), "--band-record", str(BAND_RECORD_REL)],
        )
        self.assertEqual(verified.returncode, 0, verified.stderr)
        self.assertIn("BAND-RECORD-OK", verified.stdout)
        self.assertIn("DESCRIPTIVE-OK", verified.stdout)
        text = self.fx.path(BAND_RECORD_REL).read_text(encoding="utf-8")
        payload = json.loads(JSON_FENCE.search(text).group(1))
        self.assertEqual(payload["schema"], "phase50-band-record/v2")
        self.assertEqual(set(payload["seeds"]), {"41", "42", "43"})
        lowered = text.lower()
        for needle in FORBIDDEN:
            self.assertNotIn(needle, lowered)
        self.assertIn("compound", lowered)
        seed42 = payload["seeds"]["42"]
        for key in (
            "gate_eps_h",
            "gate_scs",
            "gate_verdict",
            "gate_status",
            "gate_n_trajectories",
            "gate_n_nonfinite",
            "gate_sidecar",
            "gate_schema_version",
        ):
            self.assertIn(key, seed42["gate"])
        self.assertIn("quantiles", seed42)
        self.assertIn("front_high_water", seed42)
        self.assertIn("split_hash_qualification", payload)

    def test_missing_seed_cannot_produce_a_band(self) -> None:
        ledger = load_ledger(self.fx.root)
        ledger["records"] = [
            record for record in ledger["records"] if record["run_name"] != "stage0-rerun-seed43"
        ]
        write_text(self.fx.path(LEDGER_REL), "# ledger\n\n" + fence(ledger))
        built = self.fx.band()
        self.assertNotEqual(built.returncode, 0)
        self.assertFalse(self.fx.path(BAND_RECORD_REL).exists())

    def test_unhealthy_gate_status_cannot_produce_a_band(self) -> None:
        summary = json.loads(
            (self.fx.attempt_roots["stage0-rerun-seed41"] / "summary.json").read_text(encoding="utf-8")
        )
        summary["validation"]["gate_status"] = "failed:TypeError"
        write_text(
            self.fx.attempt_roots["stage0-rerun-seed41"] / "summary.json",
            json.dumps(summary, indent=2) + "\n",
        )
        built = self.fx.band()
        self.assertNotEqual(built.returncode, 0)
        self.assertIn("FAIL-CLOSED", fail_closed_message(built))

    def test_resume_cannot_produce_a_band(self) -> None:
        ledger = load_ledger(self.fx.root)
        for record in ledger["records"]:
            if record["run_name"] == "stage0-rerun-seed42":
                record["invocations"][0]["launch_kind"] = "resume"
        write_text(self.fx.path(LEDGER_REL), "# ledger\n\n" + fence(ledger))
        built = self.fx.band()
        self.assertNotEqual(built.returncode, 0)
        self.assertFalse(self.fx.path(BAND_RECORD_REL).exists())
