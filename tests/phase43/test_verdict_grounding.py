"""Phase 43 / 43-08 — receipt-grounded owner verdict contract."""

from __future__ import annotations

import re
import unittest
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
        validate_verdict_grounding(self.text)

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
        self.assertEqual(fields["owner_decision_date"], "2026-07-22")
        self.assertRegex(self.text, r"block\s+full-platform expansion")
        self.assertIn("does not claim that the remedy is known", self.text)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
