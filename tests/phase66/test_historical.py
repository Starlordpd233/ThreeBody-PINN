"""Plan 66-01 (EXP-01): the Phase 65 preservation and historical identity.

In the real repository, read-only git: the four smoke-pinned modules the phase
66 plan does not edit still hash to the Phase 65 smoke registration's recorded
digests; the smoke registration's own identity holds at the commit that added
the smoke record (the record's cited registration sha256 and all five
code-dependency digests, including the now-historical ``diagnostic_fit.py``);
and the 11 preserved evidence files of 65-CLOSEOUT.md keep their table hashes.
No commit SHA is hard-coded: the anchor is found by ``--diff-filter=A`` on the
smoke record path. The live smoke registration is never re-checked here — it
is expected to refuse after the phase 66 harness commit, and the refusal is
recorded in the plan summary rather than asserted by a test.
"""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PHASE65_DIR = ROOT / ".planning/phases/65-probe-on-the-record-fit-harness"
SMOKE_REGISTRATION = PHASE65_DIR / "evidence/fit/smoke-registration.json"
SMOKE_RECORD = PHASE65_DIR / "evidence/fit/1632-smoke/record.json"

#: The two smoke-pinned modules this plan and phase 67 never edit.
UNEDITED_PINS = (
    "pinn/verification/diagnostic_guard.py",
    "pinn/verification/diagnostic_data.py",
)

#: The smoke-pinned modules edited across Phase 66 and 67 (D-12/D-13 transition).
EDITED_PINS = (
    "pinn/verification/diagnostic_fit.py",
    "pinn/verification/diagnostic_variants.py",
    "pinn/verification/diagnostic_similarity.py",
)


class HistoricalPhase65Tests(unittest.TestCase):
    """Phase 65 evidence is byte-identical and its smoke identity is anchored."""

    @staticmethod
    def _git(*args):
        return subprocess.run(
            ["git", *args], cwd=str(ROOT), capture_output=True, check=True
        ).stdout

    def test_unedited_pins_equal_the_recorded_digests(self):
        doc = json.loads(SMOKE_REGISTRATION.read_bytes())
        recorded = {entry["path"]: entry["sha256"] for entry in doc["code_dependencies"]}
        for relative in UNEDITED_PINS:
            with self.subTest(path=relative):
                live = hashlib.sha256((ROOT / relative).read_bytes()).hexdigest()
                self.assertEqual(live, recorded[relative])

    def test_live_new_run_admission_refuses_the_changed_dependencies(self):
        from pinn.verification.diagnostic_guard import (
            DiagnosticRegistrationRefused,
            require_committed_registration,
        )

        with self.assertRaises(DiagnosticRegistrationRefused) as caught:
            require_committed_registration(
                SMOKE_REGISTRATION, repo_root=ROOT, weight_digests=False
            )
        message = str(caught.exception)
        self.assertTrue(any(path in message for path in EDITED_PINS))

    def test_the_smoke_identity_holds_at_the_record_commit(self):
        doc = json.loads(SMOKE_REGISTRATION.read_bytes())
        record = json.loads(SMOKE_RECORD.read_bytes())
        record_relative = SMOKE_RECORD.relative_to(ROOT).as_posix()
        registration_relative = record["registration"]["path"]
        self.assertEqual(registration_relative, SMOKE_REGISTRATION.relative_to(ROOT).as_posix())
        # The anchor is the commit that added the smoke record — not the
        # registration's introducing commit, which pins an earlier
        # diagnostic_fit.py (PATTERNS flag 11).
        anchor = self._git(
            "log", "-n1", "--format=%H", "--diff-filter=A", "--", record_relative
        ).decode().strip()
        self.assertTrue(anchor, "the smoke record has no introducing commit")
        self._git("merge-base", "--is-ancestor", anchor, "HEAD")
        for entry in doc["code_dependencies"]:
            with self.subTest(path=entry["path"]):
                committed = self._git("show", f"{anchor}:{entry['path']}")
                self.assertEqual(
                    hashlib.sha256(committed).hexdigest(), entry["sha256"]
                )
        registration_at_anchor = self._git("show", f"{anchor}:{registration_relative}")
        self.assertEqual(
            hashlib.sha256(registration_at_anchor).hexdigest(),
            record["registration"]["sha256"],
        )
        self.assertEqual(
            hashlib.sha256(SMOKE_REGISTRATION.read_bytes()).hexdigest(),
            record["registration"]["sha256"],
        )

    def _preserved_rows(self):
        text = (PHASE65_DIR / "65-CLOSEOUT.md").read_text()
        section = text.split("## Preserved evidence hashes", 1)[1]
        section = section.split("## Transition", 1)[0]
        rows = {}
        for line in section.splitlines():
            match = re.fullmatch(r"\| `([^`]+)` \| `([0-9a-f]{64})` \|", line.strip())
            if match:
                rows[match.group(1)] = match.group(2)
        return rows

    def test_phase65_evidence_hashes_are_unchanged(self):
        rows = self._preserved_rows()
        self.assertEqual(len(rows), 11)
        for relative, digest in rows.items():
            with self.subTest(path=relative):
                live = hashlib.sha256((PHASE65_DIR / relative).read_bytes()).hexdigest()
                self.assertEqual(live, digest)
