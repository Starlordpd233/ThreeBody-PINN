"""Phase 43 / 43-08 — receipt-grounded owner verdict contract."""

from __future__ import annotations

import json
import re
import tempfile
import unittest
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
VERDICT_PATH = (
    ROOT
    / ".planning/phases/43-verification-stage-0-pilot-acceptance/43-VERDICT.md"
)

REQUIRED_CITATIONS = {
    "receipt_citation": "runs/stage0-pilot-seed42/evaluation/evaluation-receipt.json",
    "seed_citation": ".planning/phases/43-verification-stage-0-pilot-acceptance/43-CALIBRATION.md",
    "timing_citation": ".planning/phases/43-verification-stage-0-pilot-acceptance/evidence/smoke/README.md",
    "seams_citation": "pinn/STATUS.md",
}

SYNTHETIC_RECEIPT = {
    "schema_version": "phase43-evaluation-receipt/v1",
    "verdict": "FAIL",
    "eps_h": 237.2086056078468,
    "scs": 2.3751304405952904,
    "checkpoint_sha256": "checkpoint-digest",
    "config_sha256": "config-digest",
    "splits_sha256": "splits-digest",
    "timestamp": "2026-07-22T12:23:13.553360+00:00",
}
SYNTHETIC_RECEIPT_CITATION = "synthetic/evaluation-receipt.json"


def _synthetic_verdict(
    *,
    gate: str = "FAIL",
    verdict: str = "adjust",
    owner_decision: str = "adjust",
    owner_decision_date: str = "2026-07-22",
) -> str:
    receipt = SYNTHETIC_RECEIPT
    return f"""---
schema_version: phase43-verdict/v1
status: owner-signed
gate: {gate}
verdict: {verdict}
recommendation: adjust
owner_decision: {owner_decision}
owner_decision_date: {owner_decision_date}
receipt_citation: {SYNTHETIC_RECEIPT_CITATION}
seed_citation: {REQUIRED_CITATIONS["seed_citation"]}
timing_citation: {REQUIRED_CITATIONS["timing_citation"]}
seams_citation: {REQUIRED_CITATIONS["seams_citation"]}
---

# Synthetic owner verdict

Receipt gate: `{receipt["verdict"]}`
eps_H = {receipt["eps_h"]}
SCS = {receipt["scs"]}
checkpoint `{receipt["checkpoint_sha256"]}`
config `{receipt["config_sha256"]}`
splits `{receipt["splits_sha256"]}`
"""


def _write_synthetic_receipt(base: Path) -> Path:
    path = base / SYNTHETIC_RECEIPT_CITATION
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(SYNTHETIC_RECEIPT), encoding="utf-8")
    return path


def _frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---\n"):
        raise ValueError("verdict artifact requires YAML-style frontmatter")
    try:
        block = text.split("---\n", 2)[1]
    except IndexError as exc:  # pragma: no cover - defensive malformed input
        raise ValueError("unterminated verdict frontmatter") from exc
    fields: dict[str, str] = {}
    for line in block.splitlines():
        if not line.strip() or line.startswith((" ", "\t")):
            continue
        key, separator, value = line.partition(":")
        if separator:
            fields[key.strip()] = value.strip()
    return fields


def validate_verdict_grounding(text: str) -> None:
    fields = _frontmatter(text)
    gate = fields.get("gate", "").upper()
    verdict = fields.get("verdict", "").lower()
    if gate == "FAIL" and verdict == "go":
        raise ValueError("gate FAIL cannot carry an unqualified verdict: go")
    if verdict not in {"pending-owner", "go", "adjust", "rethink"}:
        raise ValueError(f"unsupported verdict state: {verdict!r}")
    for key, expected_path in REQUIRED_CITATIONS.items():
        if fields.get(key) != expected_path or expected_path not in text:
            raise ValueError(f"missing required {key}: {expected_path}")
    owner_decision = fields.get("owner_decision", "").lower()
    if verdict == "pending-owner":
        if owner_decision not in {"null", "pending"}:
            raise ValueError("draft must preserve the pending owner-decision seam")
        return
    if owner_decision != verdict:
        raise ValueError("final verdict must match the owner decision")
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", fields.get("owner_decision_date", "")):
        raise ValueError("final verdict requires a dated owner sign-off")


class VerdictGroundingTests(unittest.TestCase):
    def setUp(self):
        self.text = VERDICT_PATH.read_text(encoding="utf-8")

    def test_current_verdict_is_receipt_seed_timing_and_seam_grounded(self):
        receipt_path = ROOT / REQUIRED_CITATIONS["receipt_citation"]
        if not receipt_path.is_file():
            self.skipTest("gitignored real evaluation receipt is not present")
        validate_verdict_grounding(self.text, receipt_base=ROOT)

    def test_receipt_mismatched_go_is_rejected(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            receipt_base = Path(temp_dir)
            _write_synthetic_receipt(receipt_base)
            mismatched = _synthetic_verdict(
                gate="PASS", verdict="go", owner_decision="go"
            )
            with self.assertRaisesRegex(ValueError, "receipt verdict"):
                validate_verdict_grounding(
                    mismatched, receipt_base=receipt_base
                )

    def test_quoted_yaml_gate_is_typed_and_validates(self):
        quoted = _synthetic_verdict(gate='"FAIL"')
        self.assertEqual(_frontmatter(quoted)["gate"], "FAIL")
        with tempfile.TemporaryDirectory() as temp_dir:
            receipt_base = Path(temp_dir)
            _write_synthetic_receipt(receipt_base)
            validate_verdict_grounding(quoted, receipt_base=receipt_base)

    def test_invalid_calendar_date_is_rejected(self):
        invalid = _synthetic_verdict(owner_decision_date="2026-13-45")
        with tempfile.TemporaryDirectory() as temp_dir:
            receipt_base = Path(temp_dir)
            _write_synthetic_receipt(receipt_base)
            with self.assertRaisesRegex(ValueError, "owner_decision_date"):
                validate_verdict_grounding(
                    invalid, receipt_base=receipt_base
                )

    def test_failing_gate_rejects_unqualified_go(self):
        unsupported = self.text.replace(
            "verdict: adjust", "verdict: go", 1
        ).replace("owner_decision: adjust", "owner_decision: go", 1)
        with self.assertRaisesRegex(ValueError, "unqualified verdict: go"):
            validate_verdict_grounding(unsupported)

    def test_missing_receipt_seed_timing_or_seam_citation_is_rejected(self):
        for key, expected_path in REQUIRED_CITATIONS.items():
            with self.subTest(citation=key):
                missing = self.text.replace(f"{key}: {expected_path}", f"{key}:", 1)
                with self.assertRaisesRegex(ValueError, f"missing required {key}"):
                    validate_verdict_grounding(missing)

    def test_owner_adjust_decision_and_dated_sign_off_are_persisted(self):
        fields = _frontmatter(self.text)
        self.assertEqual(fields["status"], "owner-signed")
        self.assertEqual(fields["verdict"], "adjust")
        self.assertEqual(fields["owner_decision"], "adjust")
        self.assertEqual(fields["owner_decision_date"], date(2026, 7, 22))
        self.assertRegex(self.text, r"block\s+full-platform expansion")
        self.assertIn("does not claim that the remedy is known", self.text)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
