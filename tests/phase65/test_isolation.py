"""Phase 65 (INST-08 d): Stage-0 TRAIN data-boundary and marker isolation.

Two isolation surfaces. First (Wave 0): ``require_not_diagnostic`` is
exercised on synthetic JSON records and ``weights_only`` tensor envelopes —
renamed, relocated into other directories, and wrapped in envelopes that also
carry every production-required checkpoint key. The marker lives inside the
payload, so none of that launders a diagnostic artifact into production, while
a genuine production payload passes.

Second (Plan 65-02, D-09): every diagnostic corpus operation — target or
ancillary — is refused unless its orbit sits in the training split at manifest
stage 0, before the reader, an ``exists`` call or any corpus path is touched.
Admission is proven on a synthetic manifest whose orbit stages and splits are
controlled per system, and on the seven committed Phase 60 arm specs against
the real split metadata alone (no corpus file is opened). No real-record
acceptance is claimed.
"""

from __future__ import annotations

import hashlib
import importlib
import json
import shutil
import tempfile
import unittest
from collections import OrderedDict
from contextlib import ExitStack, contextmanager
from pathlib import Path
from tempfile import TemporaryDirectory
from types import SimpleNamespace
from unittest import mock

import numpy as np
import torch

import pinn.data.splits as splits_module
from pinn.data.preprocessing import NormalizationStats
from pinn.data.splits import SplitRatios
from pinn.data.types import RecordKey
from pinn.training.atomic_io import atomic_write_torch
from pinn.training.checkpoint import CHECKPOINT_SCHEMA_VERSION
from pinn.verification import diagnostic_guard as guard
from pinn.verification import evidence_io
from pinn.verification.feasibility_scorecard import load_scorecard
from pinn.verification.learnability_arms import arm_spec, fixture_arm
from pinn.verification.learnability_data import fixture_context, load_arm_data
from pinn.verification.split_allowlist import (
    GENERATION7_SPLITS_REL,
    AllowlistedCorpusReader,
    SplitAllowlist,
    SplitRefused,
    expected_splits_sha256,
)
from tests.phase39._fixtures import TinyCorpus

ROOT = Path(__file__).resolve().parents[2]
CPU = torch.device("cpu")
# The seven committed Phase 60 arms whose records the Phase 65 boundary must
# still admit (65-CONTEXT D-06; every key is hierarchical, stage-0, train).
COMMITTED_ARMS = (
    "r1-1632", "r1-851", "r1-4658",
    "g2s-1632-w060", "g2s-1632-w120", "g2s-1632-w240", "g2s-1632-w480",
)


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


# ---------------------------------------------------------------------------
# Plan 65-02 (D-09): the Stage-0 training data boundary.
# ---------------------------------------------------------------------------


def _diagnostic_data(case):
    """Import the Phase 65 diagnostic data boundary, failing loudly if absent."""
    try:
        return importlib.import_module("pinn.verification.diagnostic_data")
    except ImportError as exc:
        case.fail(f"pinn.verification.diagnostic_data is missing: {exc}")


def _no_open():
    """Spies that raise if any file is opened while they are active."""
    def opened(*_args, **_kwargs):
        raise AssertionError("a file was opened")

    stack = ExitStack()
    spies = [
        stack.enter_context(mock.patch("builtins.open", side_effect=opened)),
        stack.enter_context(mock.patch("io.open", side_effect=opened)),
        stack.enter_context(mock.patch("pathlib.Path.open", side_effect=opened)),
        stack.enter_context(mock.patch("pathlib.Path.read_text", side_effect=opened)),
    ]
    return stack, spies


_STAGE_TRAIN_IDS = (0, 3, 7, 100, 101, 102, 103, 104)
_STAGE_VALIDATION_ID = 200
_STAGE_TEST_ID = 201
_STAGE1_ID = 42
_STANDARD_ID = 0


def _manifest_group(variant, identifier, split, base_stage, *, with_gold):
    records = [
        {"variant": variant, "fidelity": "base", "id": identifier, "stage": base_stage}
    ]
    signature = {
        "variant": variant,
        "base_stage": base_stage,
        "gold_stage": "UNASSIGNED" if with_gold else "MISSING_GOLD",
    }
    if with_gold:
        records.append(
            {"variant": variant, "fidelity": "gold", "id": identifier, "stage": "UNASSIGNED"}
        )
    return {
        "physical_key": {"variant": variant, "id": identifier},
        "signature": signature,
        "split": split,
        "records": records,
    }


def _summary_for(signature, groups, ratios):
    """The signature summary the production Hamilton allocator would write."""
    from collections import Counter

    names = ("train", "validation", "test")
    counts = Counter(group["split"] for group in groups
                     if group["signature"] == signature)
    size = sum(counts.values())
    quotas, expected = splits_module._hamilton_counts(size, ratios)
    quota = {name: float(value) for name, value in zip(names, quotas)}
    deviations = tuple(
        {
            "split": name,
            "quota": quota[name],
            "count": int(expected[index]),
            "delta": float(splits_module.Decimal(expected[index]) - quotas[index]),
        }
        for index, name in enumerate(names)
        if splits_module.Decimal(expected[index]) != quotas[index]
    )
    return {
        "signature": signature,
        "quota": quota,
        "counts": {name: int(expected[index]) for index, name in enumerate(names)},
        "deviations": list(deviations),
    }


@contextmanager
def stage_boundary_fixture():
    """A tiny corpus under a hand-written manifest with controlled orbit stages.

    Split membership per signature follows the production Hamilton allocation
    (so the manifest parses), but which physical system sits in which split is
    the fixture's choice:

    * hierarchical ids 0, 3, 7, 100..104 — train, orbit stage 0 (base+gold);
      ids 0, 3, 7 have real Brutus files, so gold id 7 is the readable key.
    * hierarchical id 200 — validation, orbit stage 0.
    * hierarchical id 201 — test (withheld), orbit stage 0.
    * hierarchical id 42 — train, orbit stage 1 (later stage).
    * standard id 0 — train, orbit stage UNASSIGNED (no stage assignment).
    """
    with TinyCorpus() as corpus, TemporaryDirectory(prefix="phase65-stage-") as run_tmp:
        ratios = SplitRatios()
        groups = []
        for identifier in _STAGE_TRAIN_IDS:
            groups.append(_manifest_group("hierarchical", identifier, "train", 0, with_gold=True))
        groups.append(_manifest_group("hierarchical", _STAGE_VALIDATION_ID, "validation", 0, with_gold=True))
        groups.append(_manifest_group("hierarchical", _STAGE_TEST_ID, "test", 0, with_gold=True))
        groups.append(_manifest_group("hierarchical", _STAGE1_ID, "train", 1, with_gold=True))
        groups.append(_manifest_group("standard", _STANDARD_ID, "train", "UNASSIGNED", with_gold=True))
        signatures = [
            _summary_for(signature, groups, ratios)
            for signature in (
                {"variant": "hierarchical", "base_stage": 0, "gold_stage": "UNASSIGNED"},
                {"variant": "hierarchical", "base_stage": 1, "gold_stage": "UNASSIGNED"},
                {"variant": "standard", "base_stage": "UNASSIGNED", "gold_stage": "UNASSIGNED"},
            )
        ]
        payload = {
            "schema_version": 1,
            "algorithm": "group-signature-hamilton-v1",
            "tie_order": ["train", "validation", "test"],
            "seed": 11,
            "ratios": ratios.as_dict(),
            "signatures": signatures,
            "groups": groups,
        }
        raw = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
        manifest_path = Path(run_tmp) / "splits.json"
        manifest_path.write_bytes(raw)
        allowlist = SplitAllowlist.from_manifest(
            manifest_path, expected_sha256=hashlib.sha256(raw).hexdigest()
        )
        yield SimpleNamespace(
            data_root=Path(corpus.data_root),
            data_root_source="fixture",
            blacklist_path=Path(corpus.blacklist_path),
            allowlist=allowlist,
            stats=NormalizationStats(
                slot_means=np.zeros(12), slot_stds=np.ones(12), e_scale=1.0
            ),
            valid_gold=RecordKey("hierarchical", "gold", 7),
            valid_base=RecordKey("hierarchical", "base", 7),
            stage1_gold=RecordKey("hierarchical", "gold", _STAGE1_ID),
            unassigned_gold=RecordKey("standard", "gold", _STANDARD_ID),
            unassigned_base=RecordKey("standard", "base", _STANDARD_ID),
            validation_gold=RecordKey("hierarchical", "gold", _STAGE_VALIDATION_ID),
            test_gold=RecordKey("hierarchical", "gold", _STAGE_TEST_ID),
            unknown_key=RecordKey("hierarchical", "gold", 999999),
        )


class StageBoundaryModuleTests(unittest.TestCase):
    """The Phase 65 diagnostic data boundary module and its planned symbols."""

    def test_the_diagnostic_data_module_and_symbols_exist(self):
        module = _diagnostic_data(self)
        for name in (
            "Stage0TrainingReader", "Stage0TrainingRefused", "require_stage0_training",
            "load_diagnostic_data", "one_orbit_spec",
        ):
            self.assertTrue(
                hasattr(module, name), f"diagnostic_data.{name} is missing"
            )


class Stage0AdmissionTests(unittest.TestCase):
    """D-09: train split plus manifest stage 0 before any reader or path work."""

    def setUp(self):
        stack = ExitStack()
        self.addCleanup(stack.close)
        self.fixture = stack.enter_context(stage_boundary_fixture())
        self.data = _diagnostic_data(self)
        self.allowlist = self.fixture.allowlist
        # Loaded here: reading the scorecard file is itself an open, which the spies must not see.
        self.scorecard = load_scorecard()

    def _guarded_reader(self):
        return self.data.Stage0TrainingReader(
            allowlist=self.allowlist,
            data_root=self.fixture.data_root,
            data_root_source=self.fixture.data_root_source,
            blacklist_path=self.fixture.blacklist_path,
        )

    def _guarded_context(self, reader):
        return fixture_context(
            allowlist=self.allowlist, reader=reader, stats=self.fixture.stats
        )

    def test_a_valid_stage0_train_gold_key_is_admitted_and_reads(self):
        reader = self._guarded_reader()
        self.assertIsInstance(reader, AllowlistedCorpusReader)
        admitted = reader.read(self.fixture.valid_gold)
        self.assertEqual(admitted.split, "train")
        summary = reader.access_summary()
        self.assertEqual(summary["actual_opens"], 1)
        entry = summary["opened"][0]
        self.assertEqual(entry["record_key"], "hierarchical/gold/7")
        self.assertEqual(entry["split"], "train")
        self.assertEqual(entry["stage"], 0)
        self.assertEqual(entry["record_stage"], "UNASSIGNED")
        self.assertEqual(reader.read_counts(), {"train": 1, "validation": 0, "refusals": 0})

    def test_disallowed_keys_refuse_before_any_open_in_read_and_exists(self):
        disallowed = (
            ("validation", self.fixture.validation_gold),
            ("stage-1", self.fixture.stage1_gold),
            ("unassigned", self.fixture.unassigned_gold),
            ("unassigned-base", self.fixture.unassigned_base),
            ("test", self.fixture.test_gold),
            ("unknown", self.fixture.unknown_key),
        )
        for label, key in disallowed:
            with self.subTest(label=label):
                reader = self._guarded_reader()
                stack, spies = _no_open()
                with stack:
                    with self.assertRaises(SplitRefused):
                        reader.read(key)
                    with self.assertRaises(SplitRefused):
                        reader.exists(key)
                for spy in spies:
                    self.assertEqual(spy.call_count, 0)
                self.assertEqual(reader.read_counts(), {"train": 0, "validation": 0, "refusals": 0})
                summary = reader.access_summary()
                self.assertEqual(summary["actual_opens"], 0)
                self.assertEqual(summary["refused_before_open"], 2)  # one read plus one exists

    def test_the_refusal_names_the_reason_without_any_path(self):
        self.data = _diagnostic_data(self)
        reader = self._guarded_reader()
        for key, expected in (
            (self.fixture.validation_gold, "validation"),
            (self.fixture.stage1_gold, "stage"),
            (self.fixture.unassigned_gold, "stage"),
        ):
            with self.subTest(key=key):
                with self.assertRaises(self.data.Stage0TrainingRefused) as caught:
                    reader.read(key)
                message = str(caught.exception)
                self.assertIn("hierarchical" if key.variant == "hierarchical" else "standard", message)
                self.assertNotIn(str(self.fixture.data_root), message)
                self.assertTrue(issubclass(self.data.Stage0TrainingRefused, SplitRefused))

    def test_require_stage0_training_reports_split_and_both_stages(self):
        for key, record_stage in ((self.fixture.valid_gold, "UNASSIGNED"), (self.fixture.valid_base, 0)):
            with self.subTest(fidelity=key.fidelity):
                report = self.data.require_stage0_training(self.allowlist, key)
                self.assertEqual(report["split"], "train")
                self.assertEqual(report["stage"], 0)
                self.assertEqual(report["record_stage"], record_stage)

    def test_a_non_record_key_is_a_type_error(self):
        reader = self._guarded_reader()
        for bad in ("hierarchical/gold/7", Path("hierarchical/gold/7"), None):
            with self.subTest(bad=bad):
                with self.assertRaises(TypeError):
                    reader.read(bad)
                with self.assertRaises(TypeError):
                    self.data.require_stage0_training(self.allowlist, bad)


class Stage0LoadTests(unittest.TestCase):
    """The diagnostic adapter: all-key validation, then the existing data seam."""

    def setUp(self):
        stack = ExitStack()
        self.addCleanup(stack.close)
        self.fixture = stack.enter_context(stage_boundary_fixture())
        self.data = _diagnostic_data(self)
        self.reader = self.data.Stage0TrainingReader(
            allowlist=self.fixture.allowlist,
            data_root=self.fixture.data_root,
            data_root_source=self.fixture.data_root_source,
            blacklist_path=self.fixture.blacklist_path,
        )
        self.context = fixture_context(
            allowlist=self.fixture.allowlist, reader=self.reader, stats=self.fixture.stats
        )
        # Loaded here: reading the scorecard file is itself an open, which the spies must not see.
        self.scorecard = load_scorecard()

    def _spec(self, **roles):
        chosen = dict(
            train_key=self.fixture.valid_gold,
            score_key=self.fixture.valid_gold,
            beside_key=self.fixture.valid_gold,
        )
        chosen.update(roles)
        return fixture_arm(**chosen)

    def test_an_invalid_ancillary_key_blocks_an_otherwise_valid_target(self):
        for role, key in (
            ("beside_key", self.fixture.stage1_gold),
            ("score_key", self.fixture.validation_gold),
            ("beside_key", self.fixture.unassigned_gold),
            ("train_key", self.fixture.test_gold),
        ):
            with self.subTest(role=role):
                spec = self._spec(**{role: key})
                stack, spies = _no_open()
                with stack:
                    with self.assertRaises(SplitRefused):
                        self.data.load_diagnostic_data(
                            spec, self.context, scorecard=self.scorecard,
                            dtype=torch.float64, device=CPU,
                        )
                for spy in spies:
                    self.assertEqual(spy.call_count, 0)
                summary = self.reader.access_summary()
                self.assertEqual(summary["actual_opens"], 0)  # the valid target was never opened
                self.assertEqual(self.reader.read_counts()["train"], 0)

    def test_a_one_orbit_gold_spec_opens_exactly_one_record(self):
        spec = self.data.one_orbit_spec(self.fixture.valid_gold)
        loaded = self.data.load_diagnostic_data(
            spec, self.context, scorecard=self.scorecard, dtype=torch.float64, device=CPU
        )
        summary = self.reader.access_summary()
        self.assertEqual(summary["actual_opens"], 1)
        self.assertEqual(len(summary["requested"]), 3)
        self.assertEqual({entry["record_key"] for entry in summary["requested"]}, {"hierarchical/gold/7"})
        self.assertEqual(sorted(loaded.records), ["beside", "score", "train"])

    def test_an_admitted_record_reaches_existing_preprocessing_unchanged(self):
        spec = self.data.one_orbit_spec(self.fixture.valid_gold)
        guarded = self.data.load_diagnostic_data(
            spec, self.context, scorecard=self.scorecard, dtype=torch.float64, device=CPU
        )
        plain_context = fixture_context(
            allowlist=self.fixture.allowlist,
            reader=AllowlistedCorpusReader(
                allowlist=self.fixture.allowlist,
                data_root=self.fixture.data_root,
                data_root_source=self.fixture.data_root_source,
                blacklist_path=self.fixture.blacklist_path,
            ),
            stats=self.fixture.stats,
        )
        plain = load_arm_data(
            spec, plain_context, scorecard=self.scorecard, dtype=torch.float64, device=CPU
        )
        self.assertTrue(torch.equal(guarded.data_points.tau_ic13, plain.data_points.tau_ic13))
        self.assertTrue(torch.equal(guarded.data_points.targets, plain.data_points.targets))
        self.assertTrue(torch.equal(guarded.data_points.masses, plain.data_points.masses))
        np.testing.assert_array_equal(guarded.ic13, plain.ic13)
        np.testing.assert_array_equal(guarded.masses, plain.masses)  # raw masses unchanged
        np.testing.assert_array_equal(guarded.score.times, plain.score.times)
        np.testing.assert_array_equal(guarded.score.positions, plain.score.positions)
        self.assertEqual(guarded.score.inner_pair, plain.score.inner_pair)  # body order unchanged


class CommittedArmBoundaryTests(unittest.TestCase):
    """The seven committed Phase 60 arms pass the boundary on metadata alone."""

    def test_every_key_of_every_committed_arm_is_admitted_without_any_open(self):
        data = _diagnostic_data(self)
        allowlist = SplitAllowlist.from_manifest(
            ROOT / GENERATION7_SPLITS_REL, expected_sha256=expected_splits_sha256(ROOT)
        )
        stack, spies = _no_open()
        with stack:
            for arm_id in COMMITTED_ARMS:
                spec = arm_spec(arm_id)
                for name in ("train_key", "score_key", "beside_key"):
                    key = getattr(spec, name)
                    with self.subTest(arm=arm_id, role=name):
                        report = data.require_stage0_training(allowlist, key)
                        self.assertEqual(report["split"], "train")
                        self.assertEqual(report["stage"], 0)
        for spy in spies:
            self.assertEqual(spy.call_count, 0)


if __name__ == "__main__":
    unittest.main()
