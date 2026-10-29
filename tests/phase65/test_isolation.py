"""Phase 65 (INST-08 d, Wave 0): intrinsic marker isolation on synthetic artifacts.

``require_not_diagnostic`` is exercised on synthetic JSON records and
``weights_only`` tensor envelopes — renamed, relocated into other directories,
and wrapped in envelopes that also carry every production-required checkpoint
key. The marker lives inside the payload, so none of that launders a
diagnostic artifact into production, while a genuine production payload (the
seven required keys without the marker, or a bare state dict) passes. These
are synthetic cases; no real-record acceptance is claimed.
"""

from __future__ import annotations

import shutil
import tempfile
import unittest
from collections import OrderedDict
from pathlib import Path

import torch

from pinn.training.atomic_io import atomic_write_torch
from pinn.verification import diagnostic_guard as guard
from pinn.verification import evidence_io
from pinn.training.checkpoint import CHECKPOINT_SCHEMA_VERSION


def _diagnostic_record_payload():
    return {
        "schema": "inst08-diagnostic/v1",
        "artifact_kind": "diagnostic",
        "diagnostic": True,
        "counted": False,
        "variant": {"name": "synthetic", "depth": 2, "width": 8},
    }


def _diagnostic_weights_payload():
    return {
        "schema": "inst08-diagnostic-weights/v1",
        "artifact_kind": "diagnostic",
        "diagnostic": True,
        "counted": False,
        "variant": {"name": "synthetic"},
        "seed": 42,
        "runtime": {"dtype": "float64", "device": "cpu"},
        "state_dict": OrderedDict(
            [
                ("layer.weight", torch.zeros((3, 4), dtype=torch.float64)),
                ("layer.bias", torch.ones(3, dtype=torch.float64)),
            ]
        ),
    }


def _production_payload(with_marker):
    """The seven production-required checkpoint keys; optionally plus the marker."""
    payload = {
        "model": {"w": torch.zeros(2, dtype=torch.float64)},
        "optimizer": None,
        "curriculum": {"stage": 0, "phase": "2a"},
        "rng": {"torch": [1, 2, 3]},
        "counters": {"global_step": 0, "epoch": 0},
        "config_identity": {"digest": "abc", "config": {"seed": 0}},
        "schema_version": CHECKPOINT_SCHEMA_VERSION,
    }
    if with_marker:
        payload.update(guard.diagnostic_marker(schema=guard.WEIGHTS_SCHEMA))
    return payload


class DiagnosticEnvelopeTests(unittest.TestCase):
    """Diagnostic identity survives renaming, relocation and added production keys."""

    def setUp(self):
        directory = tempfile.TemporaryDirectory(prefix="phase65-iso-")
        self.addCleanup(directory.cleanup)
        self.tmp = Path(directory.name)

    def _written_record(self, directory, name):
        directory.mkdir(parents=True, exist_ok=True)
        path = directory / name
        path.write_bytes(evidence_io.canonical_json_bytes(_diagnostic_record_payload()))
        return path

    def _written_weights(self, directory, name, payload=None):
        directory.mkdir(parents=True, exist_ok=True)
        path = directory / name
        atomic_write_torch(path, payload or _diagnostic_weights_payload())
        return path

    def test_renamed_and_relocated_json_records_are_refused(self):
        original = self._written_record(self.tmp / "a", "record.json")
        targets = [
            self._written_record(self.tmp / "b", "final-result.json"),
            self._written_record(self.tmp / "deep" / "nested" / "c", "weights.json"),
        ]
        shutil.copyfile(original, self.tmp / "b" / "renamed-copy.json")
        targets.append(self.tmp / "b" / "renamed-copy.json")
        for path in targets:
            with self.subTest(path=path):
                with self.assertRaises(guard.DiagnosticArtifactRefused):
                    guard.require_not_diagnostic(path)

    def test_renamed_and_relocated_tensor_envelopes_are_refused(self):
        original = self._written_weights(self.tmp / "a", "weights.pt")
        relocated = self._written_weights(self.tmp / "elsewhere", "model.weights")
        moved_copy = self.tmp / "deep" / "state.pt"
        moved_copy.parent.mkdir(parents=True)
        shutil.copyfile(original, moved_copy)
        for path in (original, relocated, moved_copy):
            with self.subTest(path=path.name):
                payload = torch.load(path, map_location="cpu", weights_only=True)
                self.assertIs(payload["diagnostic"], True)  # marker preserved inside
                with self.assertRaises(guard.DiagnosticArtifactRefused):
                    guard.require_not_diagnostic(path)

    def test_a_nested_marker_cannot_be_smuggled_past_the_guard(self):
        payload = {
            "model": {"w": torch.zeros(2)},
            "metadata": {"diagnostic": True},
        }
        path = self._written_weights(self.tmp, "smuggled.pt", payload)
        with self.assertRaises(guard.DiagnosticArtifactRefused):
            guard.require_not_diagnostic(path)

    def test_production_envelopes_with_the_marker_added_are_still_refused(self):
        laundered = self._written_weights(
            self.tmp, "laundered.pt", _production_payload(with_marker=True)
        )
        with self.assertRaises(guard.DiagnosticArtifactRefused):
            guard.require_not_diagnostic(laundered)

    def test_genuine_production_payloads_pass_the_guard(self):
        production = self._written_weights(
            self.tmp, "production.pt", _production_payload(with_marker=False)
        )
        self.assertIsNone(guard.require_not_diagnostic(production))
        bare = self._written_weights(
            self.tmp,
            "bare.weights",
            OrderedDict(
                [
                    ("layer.weight", torch.zeros((3, 4), dtype=torch.float64)),
                    ("layer.bias", torch.ones(3, dtype=torch.float64)),
                ]
            ),
        )
        self.assertIsNone(guard.require_not_diagnostic(bare))
        plain_json = self.tmp / "summary.json"
        plain_json.write_bytes(evidence_io.canonical_json_bytes({"ok": 1}))
        self.assertIsNone(guard.require_not_diagnostic(plain_json))

    def test_a_phase60_style_diagnostic_record_is_refused_by_content(self):
        path = self.tmp / "phase60-record.json"
        path.write_bytes(
            evidence_io.canonical_json_bytes(
                {"schema": "phase60-harness-run/v1", "diagnostic": True, "counted": False}
            )
        )
        with self.assertRaises(guard.DiagnosticArtifactRefused):
            guard.require_not_diagnostic(path)

    def test_the_diagnostic_readers_refuse_non_diagnostic_files(self):
        plain = self.tmp / "plain.json"
        plain.write_bytes(evidence_io.canonical_json_bytes({"schema": "other/v1"}))
        with self.assertRaises(guard.DiagnosticArtifactRefused):
            guard.read_diagnostic_record(plain)
        bare = self._written_weights(
            self.tmp,
            "bare2.weights",
            OrderedDict([("layer.weight", torch.zeros((3, 4), dtype=torch.float64))]),
        )
        with self.assertRaises(guard.DiagnosticArtifactRefused):
            guard.read_diagnostic_weights(bare)
        good = self._written_record(self.tmp / "good", "record.json")
        self.assertEqual(
            guard.read_diagnostic_record(good)["schema"], "inst08-diagnostic/v1"
        )

    def test_the_typed_refusal_is_exported_for_production_wiring(self):
        self.assertTrue(issubclass(guard.DiagnosticArtifactRefused, RuntimeError))
        path = self._written_record(self.tmp, "record.json")
        try:
            guard.require_not_diagnostic(path)
        except guard.DiagnosticArtifactRefused as exc:
            self.assertIn("record.json", str(exc))
            self.assertIn("diagnostic", str(exc))
        else:
            self.fail("the diagnostic record was not refused")


if __name__ == "__main__":
    unittest.main()
