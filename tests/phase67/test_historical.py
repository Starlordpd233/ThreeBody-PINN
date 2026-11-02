"""Plan 67-01: Phase 65/66 historical evidence and the live-pin transition.

In the real repository, read-only git: the Phase 66 code pins the Phase 67
plans have not edited (the seven recorded dependencies minus
:data:`EDITED_PINS`) still hash to every Phase 66 registration's recorded
digests; each Phase 66 run's identity holds at the commit that added its
record (the record's cited registration sha256 and all seven code-dependency
digests, including the now-historical ``diagnostic_fit.py``); and the 11
preserved Phase 65 evidence files of 65-CLOSEOUT.md keep their table hashes.
Fresh new-run admission on the live tree correctly refuses the Phase 66
registrations on a changed dependency while those recorded bytes still
verify at their recorded run commits — the D-12/D-13 separation of
historical provenance from live admission permission. No commit SHA is
hard-coded: each anchor is found by ``--diff-filter=A`` on its record path.
The Phase 66 test_pages live-digest assertions are the inherited live-pin
confusion this plan reports for the narrowly scoped compatibility work in
67-06.
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
PHASE66_DIR = ROOT / ".planning/phases/66-small-network-control"

#: The harness files the Phase 67 plans edit; their live digests diverge from
#: every Phase 66 registration's recorded pins, which is the planned D-12
#: transition (67-01 edited diagnostic_fit.py; 67-02 edits the variant
#: declarations and, in its logger task, the shared similarity measurement).
#: Historical provenance still verifies at each record's run commit below.
EDITED_PINS = frozenset({
    "pinn/verification/diagnostic_fit.py",
    "pinn/verification/diagnostic_variants.py",
    "pinn/verification/diagnostic_similarity.py",
})

#: The Phase 66 registrations and their run records (registration, record).
PHASE66_RUNS = (
    ("exp01/main-1632-s42-registration.json", "exp01/main-1632-s42/record.json"),
    ("exp01/repeat-851-s42-registration.json", "exp01/repeat-851-s42/record.json"),
    ("exp01/repeat-1632-s41-registration.json", "exp01/repeat-1632-s41/record.json"),
    ("timing/timing-registration.json", "timing/1632-s42/record.json"),
)


class HistoricalPhase66Tests(unittest.TestCase):
    """Phase 66 evidence is byte-identical and its identity is run-anchored."""

    @staticmethod
    def _git(*args):
        return subprocess.run(
            ["git", *args], cwd=str(ROOT), capture_output=True, check=True
        ).stdout

    def test_the_six_unedited_pins_equal_the_recorded_digests(self):
        for registration_relative, _record in PHASE66_RUNS:
            doc = json.loads((PHASE66_DIR / "evidence" / registration_relative).read_bytes())
            recorded = {
                entry["path"]: entry["sha256"]
                for entry in doc["code_dependencies"]
            }
            with self.subTest(registration=registration_relative):
                for relative, digest in recorded.items():
                    if relative in EDITED_PINS:
                        continue
                    live = hashlib.sha256((ROOT / relative).read_bytes()).hexdigest()
                    self.assertEqual(live, digest)

    def test_each_run_identity_holds_at_its_record_commit(self):
        for registration_relative, record_relative in PHASE66_RUNS:
            record_path = PHASE66_DIR / "evidence" / record_relative
            registration_path = PHASE66_DIR / "evidence" / registration_relative
            with self.subTest(run=record_relative):
                doc = json.loads(registration_path.read_bytes())
                record = json.loads(record_path.read_bytes())
                record_repo_relative = record_path.relative_to(ROOT).as_posix()
                self.assertEqual(
                    record["registration"]["path"],
                    registration_path.relative_to(ROOT).as_posix(),
                )
                # The anchor is the commit that added the run record — the
                # moment the pinned dependencies describe the code that ran.
                anchor = self._git(
                    "log", "-n1", "--format=%H", "--diff-filter=A", "--",
                    record_repo_relative,
                ).decode().strip()
                self.assertTrue(anchor, "the run record has no introducing commit")
                self._git("merge-base", "--is-ancestor", anchor, "HEAD")
                for entry in doc["code_dependencies"]:
                    committed = self._git("show", f"{anchor}:{entry['path']}")
                    self.assertEqual(
                        hashlib.sha256(committed).hexdigest(), entry["sha256"]
                    )
                registration_at_anchor = self._git(
                    "show", f"{anchor}:{record['registration']['path']}"
                )
                self.assertEqual(
                    hashlib.sha256(registration_at_anchor).hexdigest(),
                    record["registration"]["sha256"],
                )
                self.assertEqual(
                    hashlib.sha256(registration_path.read_bytes()).hexdigest(),
                    record["registration"]["sha256"],
                )

    def test_live_new_run_admission_refuses_the_changed_dependency(self):
        from pinn.verification.diagnostic_guard import (
            DiagnosticRegistrationRefused,
            require_committed_registration,
        )

        for registration_relative, _record in PHASE66_RUNS:
            with self.subTest(registration=registration_relative):
                with self.assertRaises(DiagnosticRegistrationRefused) as refused:
                    require_committed_registration(
                        PHASE66_DIR / "evidence" / registration_relative,
                        repo_root=ROOT,
                        weight_digests=False,
                    )
                recorded = json.loads(
                    (PHASE66_DIR / "evidence" / registration_relative).read_bytes()
                )
                edited = EDITED_PINS & {
                    entry["path"] for entry in recorded["code_dependencies"]
                }
                message = str(refused.exception)
                self.assertTrue(
                    edited and any(path in message for path in edited),
                    f"the refusal names no edited dependency: {message}",
                )


class PreservedPhase65EvidenceTests(unittest.TestCase):
    """The Phase 65 closeout's preserved evidence keeps its committed bytes."""

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
