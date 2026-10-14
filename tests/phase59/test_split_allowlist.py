"""Phase 59 allowlist: hash check, refusal before any path, one admitted read."""

from __future__ import annotations

import contextlib
import hashlib
import io
import json
import sys
import types
import unittest
from pathlib import Path
from unittest import mock

from pinn.data.types import RecordKey
from pinn.verification import split_allowlist
from tests.phase39.test_prohibitions import ALLOWED_CORPUS_READERS
from tests.phase59._corpus_fixtures import tiny_split_fixture


_RETENTION_SHA = "5846ae5b55104e55a85d644875c3da187200c3d521f52a9298876d656c6d8903"


def _reader(fx, *, data_root=None):
    allowlist = split_allowlist.SplitAllowlist.from_manifest(
        fx.manifest_path, expected_sha256=fx.manifest_sha256
    )
    root = fx.data_root if data_root is None else data_root
    return allowlist, split_allowlist.AllowlistedCorpusReader(
        allowlist=allowlist,
        data_root=root,
        data_root_source="explicit",
        blacklist_path=fx.blacklist_path,
    )


def _freeze_module(*, refuse):
    module = types.ModuleType("pinn.verification.evidence_io")

    class FreezeNotEstablished(Exception):
        pass

    module.FreezeNotEstablished = FreezeNotEstablished
    if refuse:
        def require_frozen_scorecard():
            raise FreezeNotEstablished("scorecard freeze is not established")
    else:
        def require_frozen_scorecard():
            return {"freeze_commit": "f" * 40, "head": "a" * 40}

    module.require_frozen_scorecard = require_frozen_scorecard
    return module


class ManifestHashTests(unittest.TestCase):
    def test_wrong_expected_sha256_names_the_hash(self):
        expected = "0" * 64
        with tiny_split_fixture() as fx:
            with self.assertRaises(ValueError) as caught:
                split_allowlist.SplitAllowlist.from_manifest(
                    fx.manifest_path, expected_sha256=expected
                )
        self.assertIn(expected, str(caught.exception))

    def test_tampered_hamilton_counts_raise_from_the_manifest_parser(self):
        with tiny_split_fixture() as fx:
            payload = json.loads(fx.manifest_path.read_text(encoding="utf-8"))
            payload["signatures"][0]["counts"]["train"] += 1
            raw = json.dumps(payload).encode("utf-8")
            tampered = fx.manifest_path.with_name("tampered-splits.json")
            tampered.write_bytes(raw)
            digest = hashlib.sha256(raw).hexdigest()
            with self.assertRaisesRegex(ValueError, "Hamilton"):
                split_allowlist.SplitAllowlist.from_manifest(
                    tampered, expected_sha256=digest
                )


class RefusalBeforeOpenTests(unittest.TestCase):
    def test_require_returns_train_or_validation_and_refuses_the_rest(self):
        with tiny_split_fixture() as fx:
            allowlist, _reader_unused = _reader(fx)
            self.assertIn(allowlist.require(fx.allowed_key), ("train", "validation"))
            with self.assertRaises(split_allowlist.SplitRefused) as refused:
                allowlist.require(fx.test_key)
            self.assertIn("refused before any path is built", str(refused.exception))
            unknown = RecordKey("hierarchical", "base", 999999)
            with self.assertRaises(split_allowlist.SplitRefused):
                allowlist.require(unknown)

    def test_test_split_read_does_not_open_a_file(self):
        def opened(*_args, **_kwargs):
            raise AssertionError("opened")

        with tiny_split_fixture() as fx:
            _allowlist, reader = _reader(fx)
            with mock.patch("builtins.open", side_effect=opened), \
                    mock.patch("io.open", side_effect=opened), \
                    mock.patch("pathlib.Path.open", side_effect=opened), \
                    mock.patch("pathlib.Path.read_text", side_effect=opened) as spy:
                with self.assertRaises(split_allowlist.SplitRefused):
                    reader.read(fx.test_key_with_file)
            spy.assert_not_called()


class RefusalPrecedesIOTests(unittest.TestCase):
    def test_missing_root_refuses_a_test_key_and_misses_an_allowed_file(self):
        with tiny_split_fixture() as fx:
            _allowlist, reader = _reader(
                fx, data_root=Path("/nonexistent/phase59-allowlist-root")
            )
            with self.assertRaises(split_allowlist.SplitRefused):
                reader.read(fx.test_key)
            with self.assertRaises(FileNotFoundError):
                reader.read(fx.allowed_key)


class AllowedReadTests(unittest.TestCase):
    def test_allowed_tiny_record_is_admitted(self):
        with tiny_split_fixture() as fx:
            _allowlist, reader = _reader(fx)
            admitted = reader.read(fx.allowed_key)
        self.assertIsInstance(admitted, split_allowlist.AdmittedRead)
        self.assertEqual(admitted.admission.disposition, "admit")
        self.assertGreater(int(admitted.parsed.times.shape[0]), 0)


class RecordEnumerationTests(unittest.TestCase):
    def test_train_records_are_sorted_and_exclude_the_test_split(self):
        with tiny_split_fixture() as fx:
            allowlist, _reader_unused = _reader(fx)
            keys = allowlist.records("train", variant="hierarchical", fidelity="base")
            self.assertEqual(keys, tuple(sorted(keys)))
            self.assertNotIn(fx.test_key, keys)
            self.assertNotIn(fx.test_key_with_file, keys)
            self.assertTrue(all(key.physical_key in allowlist.allowed for key in keys))
            self.assertTrue(all(key.physical_key not in allowlist.withheld for key in keys))
            with self.assertRaises(split_allowlist.SplitRefused):
                allowlist.records("test", variant="hierarchical", fidelity="base")


class ExpectedHashTests(unittest.TestCase):
    def test_expected_splits_sha256_is_the_generation7_retention_value(self):
        self.assertEqual(split_allowlist.expected_splits_sha256(), _RETENTION_SHA)


class CliFreezeGuardTests(unittest.TestCase):
    def test_freeze_refusal_returns_before_probe(self):
        module = _freeze_module(refuse=True)
        stderr = io.StringIO()
        with mock.patch.dict(sys.modules, {"pinn.verification.evidence_io": module}):
            with mock.patch(
                "pinn.verification.split_allowlist.probe",
                side_effect=AssertionError("probe was reached"),
            ) as probe:
                with contextlib.redirect_stderr(stderr):
                    code = split_allowlist.main(["--probe-split", "test"])
        self.assertEqual(code, 1)
        self.assertIn("FREEZE-REFUSED", stderr.getvalue())
        probe.assert_not_called()

    def test_freeze_ok_prints_the_commit_and_calls_probe_once(self):
        module = _freeze_module(refuse=False)
        stderr = io.StringIO()
        payload = {
            "probe_split": "test",
            "record": {"variant": "hierarchical", "fidelity": "base", "id": 1},
            "outcome": "refused_before_path",
            "n_snapshots": None,
            "data_root_source": "explicit",
        }
        with mock.patch.dict(sys.modules, {"pinn.verification.evidence_io": module}):
            with mock.patch(
                "pinn.verification.split_allowlist.probe", return_value=payload
            ) as probe:
                with contextlib.redirect_stderr(stderr):
                    code = split_allowlist.main(["--probe-split", "test"])
        self.assertEqual(code, 0)
        text = stderr.getvalue()
        self.assertIn("FREEZE-OK", text)
        self.assertIn("f" * 40, text)
        probe.assert_called_once()


class ProhibitionsAllowlistTests(unittest.TestCase):
    def test_allowed_corpus_readers_gained_only_the_choke_point(self):
        self.assertEqual(
            ALLOWED_CORPUS_READERS,
            {
                "pinn/data/adapter.py",
                "pinn/verification/fixture_loader.py",
                "pinn/verification/target_frame_probe.py",
                "pinn/verification/split_allowlist.py",
            },
        )


if __name__ == "__main__":
    unittest.main()
