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

import torch

from pinn.architecture_spec import ArchitectureSpec
from pinn.network import build_network
from pinn.verification import diagnostic_variants
from pinn.verification.diagnostic_fit import _receipt_is_a_measurement
from pinn.verification.learnability_arms import SEED

ROOT = Path(__file__).resolve().parents[2]
PHASE65_DIR = ROOT / ".planning/phases/65-probe-on-the-record-fit-harness"
PHASE66_DIR = ROOT / ".planning/phases/66-small-network-control"

#: The harness files the Phase 67 plans edit; their live digests diverge from
#: every Phase 66 registration's recorded pins, which is the planned D-12
#: transition (67-01 edited diagnostic_fit.py; 67-02 edits the variant
#: declarations and, in its logger task, the shared similarity measurement;
#: 67-06 task 2 edits the power gate's remaining-window admission).
#: Historical provenance still verifies at each record's run commit below.
EDITED_PINS = frozenset({
    "pinn/verification/diagnostic_fit.py",
    "pinn/verification/diagnostic_variants.py",
    "pinn/verification/diagnostic_similarity.py",
    "pinn/verification/diagnostic_power.py",
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


class CurrentLockedRawParityTests(unittest.TestCase):
    """Locked raw construction retains parity with production network building."""

    def test_parameters_are_bitwise_equal_to_production_at_the_same_seed(self):
        production = build_network(
            ArchitectureSpec(seed=SEED), dtype=torch.float64, device=torch.device("cpu")
        )
        variant_net = diagnostic_variants.build_variant(
            "locked-12", seed=SEED, dtype=torch.float64, device=torch.device("cpu")
        )
        prod_state = production.state_dict()
        var_state = variant_net.state_dict()
        self.assertEqual(sorted(prod_state), sorted(var_state))
        for name in prod_state:
            self.assertTrue(torch.equal(prod_state[name], var_state[name]), name)

    def test_projected_forward_outputs_are_equal_with_unequal_raw_masses(self):
        production = build_network(
            ArchitectureSpec(seed=SEED), dtype=torch.float64, device=torch.device("cpu")
        )
        variant_net = diagnostic_variants.build_variant(
            "locked-12", seed=SEED, dtype=torch.float64, device=torch.device("cpu")
        )
        generator = torch.Generator(device="cpu").manual_seed(20261028)
        X = torch.randn((6, 14), generator=generator, dtype=torch.float64)
        masses = torch.tensor([[1.7, 0.6, 2.4]], dtype=torch.float64).expand(6, 3)
        with torch.no_grad():
            out_prod = production(X, masses)
            out_var = variant_net(X, masses)
        self.assertTrue(torch.equal(out_prod, out_var))


class HistoricalRawRecordShapeTests(unittest.TestCase):
    """Old raw record shapes have not drifted."""

    RECORD_PATHS = (
        PHASE65_DIR / "evidence/fit/1632-smoke/record.json",
        PHASE66_DIR / "evidence/timing/1632-s42/record.json",
        PHASE66_DIR / "evidence/exp01/main-1632-s42/record.json",
        PHASE66_DIR / "evidence/exp01/repeat-851-s42/record.json",
        PHASE66_DIR / "evidence/exp01/repeat-1632-s41/record.json",
    )

    EXPECTED_KEYS = (
        "access", "artifact_kind", "comparisons", "context", "counted",
        "diagnostic", "logger_parity", "loss", "optimizer", "orbit",
        "registration", "run_id", "runtime", "schema", "scores", "seed",
        "similarity", "source_sha256", "status", "steps", "timing",
        "variant", "weights",
    )

    def test_historical_raw_record_keys_and_variant_shapes_are_exact(self):
        for path in self.RECORD_PATHS:
            with self.subTest(record=path.relative_to(ROOT).as_posix()):
                doc = json.loads(path.read_bytes())
                self.assertEqual(tuple(doc.keys()), self.EXPECTED_KEYS)
                self.assertIn("network", doc["scores"])
                self.assertIn("tier", doc["scores"]["network"])
                for vk in ("name", "depth", "width", "learning_rate", "window_length", "time_features"):
                    self.assertIn(vk, doc["variant"])


class EncodedApplicabilityPreservationTests(unittest.TestCase):
    """Historical logger parity is a raw measurement with no encoded applicability."""

    def test_historical_logger_parity_receipt_is_raw_measurement(self):
        receipt_path = PHASE65_DIR / "evidence/probe/logger-parity.json"
        receipt = json.loads(receipt_path.read_bytes())
        self.assertTrue(_receipt_is_a_measurement(receipt))
        self.assertIsNotNone(receipt["first_layer_frequency"]["median"])
        self.assertIsNotNone(receipt["first_layer_frequency"]["max"])
        self.assertNotIn("frequency_applicability", receipt)
        self.assertNotIn("frequency_reason", receipt)


class PreservedHistoricalArtifactsTests(unittest.TestCase):
    """Preserved Phase 65 and 66 pages, registrations, records and weights retain expected digests."""

    HISTORICAL_ARTIFACTS = {
        "65-smoke-registration": (PHASE65_DIR / "evidence/fit/smoke-registration.json", "ba54e8124a33bb8b172256c6c7150b1f37e3dde1c52c682635bc49e169140d8e"),
        "65-smoke-record": (PHASE65_DIR / "evidence/fit/1632-smoke/record.json", "f6faee77d5278aef139052a694e9e17b3090201aac17000eb9453fadd108d6ea"),
        "65-smoke-weights": (PHASE65_DIR / "evidence/fit/1632-smoke/diagnostic.weights", "12115adda4f9b11538091d40da8922c880a14728ed6e92f883affca85710320e"),
        "65-probe-logger-parity": (PHASE65_DIR / "evidence/probe/logger-parity.json", "4f908f39b500d9976a2cd82fa549db0087b7405bc7443b2f2d33a70b731da6b5"),
        "66-timing-page": (PHASE66_DIR / "66-TIMING-PREDICTION.md", "ec54a05e0c98e6b92d303516c4d19ec466064c296ad6227df0efab7ab3e2aaed"),
        "66-prediction-page": (PHASE66_DIR / "66-PREDICTION.md", "7ec16fe90c34cd01406fe227217916754128a283bc6409ed77f4e1811058d8be"),
        "66-result-page": (PHASE66_DIR / "66-RESULT.md", "bf143995410ae48a57845b5cf7f5500dc059c4fd0af96486a1b43801b88d26a9"),
        "66-review-page": (PHASE66_DIR / "66-REVIEW.md", "ccab30a6766f9e15a9f637994c78f13cafcdd361ec3a0b6bcffd0d1efe109592"),
        "66-timing-reg": (PHASE66_DIR / "evidence/timing/timing-registration.json", "794daa6e334e44c0f3c0c5a040c635614de20d8143629b9f020e71ac998421c6"),
        "66-main-reg": (PHASE66_DIR / "evidence/exp01/main-1632-s42-registration.json", "b0d79585131c198a4c09f9dea4f1667b57eed8e38fb0d0fd3b11e5071964dcce"),
        "66-r851-reg": (PHASE66_DIR / "evidence/exp01/repeat-851-s42-registration.json", "40754fb93ac4b8a4aa70c580ec233b6fbf7f15fb95dad002a969215062646f36"),
        "66-r1632-reg": (PHASE66_DIR / "evidence/exp01/repeat-1632-s41-registration.json", "48a15ad60f4a018c17eab10211153a48df577a292f9853d68eccd4e38592a8f1"),
        "66-timing-record": (PHASE66_DIR / "evidence/timing/1632-s42/record.json", "128fe093dac017e1b9c0da900d07db8d768ccfacb9d8f22088b97a938859d671"),
        "66-main-record": (PHASE66_DIR / "evidence/exp01/main-1632-s42/record.json", "774a5a451bda97c79e39e3e10d146bcde8a5a5551b19a0d3cf59022b4b301007"),
        "66-r851-record": (PHASE66_DIR / "evidence/exp01/repeat-851-s42/record.json", "9166311284ea857ea835813ea74b5ea6a30323d0cb4036341b722dcf56add05b"),
        "66-r1632-record": (PHASE66_DIR / "evidence/exp01/repeat-1632-s41/record.json", "4146675b56990ca145fa9db777f7922476b1d64ab4cf8f708acb1acec2137c2a"),
        "66-timing-weights": (PHASE66_DIR / "evidence/timing/1632-s42/diagnostic.weights", "68b6ac60987557e693fd22f1a062850a5d8f749b6bee8ad508af796f1712dcc7"),
        "66-main-weights": (PHASE66_DIR / "evidence/exp01/main-1632-s42/diagnostic.weights", "bdf95cc1c8b0a148e415892eb2bf9f4ec2eee844f92479ccbd3df3afc0ce31c6"),
        "66-r851-weights": (PHASE66_DIR / "evidence/exp01/repeat-851-s42/diagnostic.weights", "f73519dffd0e23fd6b8f029c8f38e787fdcd436eb60461e8352b409e9422c62c"),
        "66-r1632-weights": (PHASE66_DIR / "evidence/exp01/repeat-1632-s41/diagnostic.weights", "957af465d74fb55455cf44b9836f32b4ae566d9e942ee67fc65bf4ff8530aabb"),
    }

    def test_phase65_and_66_pages_registrations_records_and_weights_are_identical(self):
        for name, (path, expected_digest) in self.HISTORICAL_ARTIFACTS.items():
            with self.subTest(artifact=name):
                self.assertTrue(path.is_file(), f"{path} is missing")
                live = hashlib.sha256(path.read_bytes()).hexdigest()
                self.assertEqual(live, expected_digest, f"{name} digest changed")
