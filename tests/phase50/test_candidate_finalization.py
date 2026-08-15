"""Structural candidate and final-manifest fixture tests for Plan 50-07 Task 3."""
from __future__ import annotations

import json
import re
import tempfile
import unittest
from pathlib import Path

from tests.phase50._evidence_fixtures import (
    BAND_RECORD_REL,
    CANDIDATE_REL,
    FINAL_MANIFEST_REL,
    LEDGER_REL,
    SOURCE_MANIFEST_REL,
    clone_complete,
    fail_closed_message,
    fence,
    write_text,
)
from tests.phase50.test_evidence_builder import load_ledger

JSON_FENCE = re.compile(r"```json\n(.*?)\n```", re.S)


class CandidateFinalizationTests(unittest.TestCase):
    def _prepare(self, variant: str):
        self.tmp = tempfile.TemporaryDirectory()
        self.fx = clone_complete(Path(self.tmp.name) / variant, candidate_variant=variant)
        extracted = self.fx.extract()
        self.assertEqual(extracted.returncode, 0, extracted.stderr)
        built = self.fx.band()
        self.assertEqual(built.returncode, 0, built.stderr)
        return self.fx

    def tearDown(self) -> None:
        if hasattr(self, "tmp"):
            self.tmp.cleanup()

    def test_eligible_seed42_is_selected(self) -> None:
        fx = self._prepare("primary42")
        cand = fx.candidate()
        self.assertEqual(cand.returncode, 0, cand.stderr)
        finalized = fx.finalize()
        self.assertEqual(finalized.returncode, 0, finalized.stderr)
        verified = fx.verify(
            "candidate",
            [
                "--source-manifest",
                str(SOURCE_MANIFEST_REL),
                "--band-record",
                str(BAND_RECORD_REL),
                "--candidate",
                str(CANDIDATE_REL),
            ],
        )
        self.assertEqual(verified.returncode, 0, verified.stderr)
        self.assertIn("CANDIDATE-OK", verified.stdout)
        self.assertIn("HASHES-OK", verified.stdout)
        receipt = json.loads(fx.path(CANDIDATE_REL).read_text(encoding="utf-8"))
        self.assertEqual(receipt["run_name"], "stage0-rerun-seed42")
        self.assertTrue(receipt["facts"]["42"]["eligible"])
        everything = fx.verify("all", ["--manifest", str(FINAL_MANIFEST_REL)])
        self.assertEqual(everything.returncode, 0, everything.stderr)
        self.assertIn("PHASE50-EVIDENCE-OK", everything.stdout)
        manifest = json.loads(fx.path(FINAL_MANIFEST_REL).read_text(encoding="utf-8"))
        self.assertNotIn(str(FINAL_MANIFEST_REL), manifest.get("files", {}))

    def test_ineligible_42_falls_back_to_41(self) -> None:
        fx = self._prepare("fallback41")
        self.assertEqual(fx.candidate().returncode, 0)
        receipt = json.loads(fx.path(CANDIDATE_REL).read_text(encoding="utf-8"))
        self.assertEqual(receipt["run_name"], "stage0-rerun-seed41")
        self.assertFalse(receipt["facts"]["42"]["eligible"])
        self.assertTrue(receipt["facts"]["41"]["eligible"])

    def test_fallback_to_43_when_42_and_41_ineligible(self) -> None:
        fx = self._prepare("fallback43")
        self.assertEqual(fx.candidate().returncode, 0)
        receipt = json.loads(fx.path(CANDIDATE_REL).read_text(encoding="utf-8"))
        self.assertEqual(receipt["run_name"], "stage0-rerun-seed43")

    def test_no_eligible_seed_writes_null_candidate(self) -> None:
        fx = self._prepare("none")
        self.assertEqual(fx.candidate().returncode, 0)
        receipt = json.loads(fx.path(CANDIDATE_REL).read_text(encoding="utf-8"))
        self.assertIsNone(receipt.get("run_name"))
        self.assertTrue(receipt.get("owner_stop"))

    def test_partial_generation_cannot_finalize(self) -> None:
        fx = self._prepare("primary42")
        ledger = load_ledger(fx.root)
        ledger["records"] = [record for record in ledger["records"] if "seed43" not in record["run_name"]]
        write_text(fx.path(LEDGER_REL), "# ledger\n\n" + fence(ledger))
        self.assertNotEqual(fx.candidate().returncode, 0)
        self.assertFalse(fx.path(CANDIDATE_REL).exists())

    def test_held_out_materialization_fails(self) -> None:
        fx = self._prepare("primary42")
        eval_dir = fx.attempt_roots["stage0-rerun-seed42"] / "evaluation"
        eval_dir.mkdir()
        (eval_dir / "evaluation-attempt.json").write_text("{}\n", encoding="utf-8")
        proc = fx.candidate()
        self.assertNotEqual(proc.returncode, 0)
        self.assertIn("FAIL-CLOSED", fail_closed_message(proc))
