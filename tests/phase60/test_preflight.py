"""Phase 60 (SPEC Requirement 8): the assigned-record preflight, with no fallback.

Every record an arm trains on, is scored on or reports beside is checked before
the first arm launches. A key is ``ok``, ``refused`` (not a train or validation
record), ``missing`` (allowlisted, no file), ``empty`` (a file with no complete
snapshot), or ``unreadable`` (a file the reader or the admission gate rejects).
A blocked key is reported as blocked; no other fidelity, variant or id is ever
read in its place.

The function is reached through a helper, so a run against code that does not
have it yet fails on the planned behavior instead of at import.
"""

from __future__ import annotations

import dataclasses
import json
import re
import shutil
import tempfile
import unittest
from contextlib import ExitStack
from pathlib import Path
from unittest import mock

import torch

from pinn.data.adapter import BRUTUS_FOLDER_TABLE, BRUTUS_SUBDIR
from pinn.data.types import PhysicalKey, RecordKey
from pinn.verification import evidence_io, learnability_data
from pinn.verification.feasibility_scorecard import load_scorecard
from pinn.verification.learnability_arms import fixture_arm
from pinn.verification.learnability_data import fixture_context, load_arm_data
from tests.phase60._fixtures import gold_corpus_fixture

HEX64 = re.compile(r"[0-9a-f]{64}")
KEY_TEXT = re.compile(r"\b(?:hierarchical|standard)/(?:base|gold)/\d+\b")

# A complete block is a "t N t_cpu" header and three "m x y z vx vy vz" rows.
_ONE_BLOCK = "0.0 1 0.0\n1.0 0 0 0 0 0 0\n1.0 1 0 0 0 0 0\n1.0 0 1 0 0 0 0\n"
_BAD_NUMBER = "0.0 1 0.0\nx 0 0 0 0 0 0\n1.0 1 0 0 0 0 0\n1.0 0 1 0 0 0 0\n"


def _preflight(case):
    function = getattr(learnability_data, "preflight_records", None)
    case.assertIsNotNone(function, "pinn.verification.learnability_data.preflight_records is missing")
    return function


def _record_path(data_root, key):
    folder = next(
        name for name, pair in BRUTUS_FOLDER_TABLE.items() if pair == (key.variant, key.fidelity)
    )
    return Path(data_root) / BRUTUS_SUBDIR / folder / f"brutus_{key.variant}_{key.id:04d}.txt"


class _Horizon:
    """A scorecard stand-in that only names the scored horizon."""

    def __init__(self, t_max):
        self._t_max = t_max

    def section(self, name):
        if name != "scoring_grid":
            raise KeyError(name)
        return {"t_max": self._t_max}


class PreflightTests(unittest.TestCase):
    def setUp(self):
        stack = ExitStack()
        self.addCleanup(stack.close)
        self.fixture = stack.enter_context(gold_corpus_fixture())
        self.tmp = Path(stack.enter_context(tempfile.TemporaryDirectory(prefix="phase60-preflight-")))
        self.context = fixture_context(
            allowlist=self.fixture.allowlist, reader=self.fixture.reader, stats=self.fixture.stats
        )
        self.scorecard = load_scorecard()
        self.preflight = _preflight(self)
        # A train-split gold record the manifest lists but the corpus has no file for. Its base
        # sibling is made readable, so a preflight that fell back to another fidelity would
        # find something to read.
        self.missing_key = [
            key
            for key in self.fixture.allowlist.records("train", variant="hierarchical", fidelity="gold")
            if not _record_path(self.fixture.data_root, key).exists()
        ][-1]
        self.sibling_key = RecordKey("hierarchical", "base", self.missing_key.id)
        self.fixture.allowlist.require(self.sibling_key)
        sibling_path = _record_path(self.fixture.data_root, self.sibling_key)
        self.assertFalse(sibling_path.exists())
        shutil.copyfile(_record_path(self.fixture.data_root, self.fixture.base_key), sibling_path)
        # Train-split base records the manifest lists but the corpus has no file for.
        spare = [
            key
            for key in self.fixture.allowlist.records("train", variant="hierarchical", fidelity="base")
            if not _record_path(self.fixture.data_root, key).exists()
        ]
        self.assertGreaterEqual(len(spare), 6)
        self.spare = spare

    def _write(self, key, content):
        path = _record_path(self.fixture.data_root, key)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return path

    def _six(self):
        """allowed base, allowed gold, test key, a key with no file, an empty file, a malformed file."""
        empty_key, bad_key = self.spare[0], self.spare[1]
        self._write(empty_key, "")
        self._write(bad_key, _BAD_NUMBER)
        return [
            self.fixture.base_key, self.fixture.gold_key, self.fixture.test_key,
            self.missing_key, empty_key, bad_key,
        ]

    def _run(self, keys, **options):
        options.setdefault("scorecard", self.scorecard)
        return self.preflight(keys, self.context, **options)

    # ------------------------------------------------------------------ the six statuses

    def test_the_six_keys_report_ok_ok_refused_missing_empty_unreadable(self):
        keys = self._six()
        report = self._run(keys)
        self.assertEqual(
            [entry["status"] for entry in report.values()],
            ["ok", "ok", "refused", "missing", "empty", "unreadable"],
        )
        self.assertEqual(list(report), [evidence_io.record_key_str(key) for key in keys])

    def test_the_blocked_entries_have_exactly_these_fields(self):
        keys = self._six()
        report = self._run(keys)
        refused, missing, empty, unreadable = (report[evidence_io.record_key_str(k)] for k in keys[2:])
        self.assertEqual(refused, {"status": "refused"})
        self.assertEqual(missing, {"status": "missing", "split": "train"})
        self.assertEqual(empty, {"status": "empty", "split": "train", "n_snapshots": 0})
        self.assertEqual(
            sorted(unreadable), ["error_type", "message", "split", "status"]
        )
        self.assertEqual(unreadable["split"], "train")
        self.assertEqual(unreadable["error_type"], "ValueError")
        self.assertIn("could not convert", unreadable["message"])

    def test_an_ok_entry_carries_the_counts_the_hash_and_the_inner_pair(self):
        report = self._run([self.fixture.base_key, self.fixture.gold_key])
        base = report[evidence_io.record_key_str(self.fixture.base_key)]
        gold = report[evidence_io.record_key_str(self.fixture.gold_key)]
        self.assertEqual(sorted(gold), sorted(base))
        self.assertEqual(
            sorted(gold),
            ["dt_out_measured", "inner_pair", "n_snapshots", "n_within_t", "split", "status",
             "windowed_sha256"],
        )
        self.assertEqual((gold["status"], gold["split"], base["split"]), ("ok", "train", "train"))
        self.assertEqual((gold["n_snapshots"], gold["n_within_t"]), (24, 24))
        self.assertEqual((base["n_snapshots"], base["n_within_t"]), (12, 12))
        for entry in (base, gold):
            self.assertRegex(entry["windowed_sha256"], HEX64)
            self.assertGreater(entry["dt_out_measured"], 0.0)
            self.assertEqual(len(entry["inner_pair"]), 2)
            self.assertTrue(all(isinstance(slot, int) and 0 <= slot <= 2 for slot in entry["inner_pair"]))
        self.assertNotEqual(base["windowed_sha256"], gold["windowed_sha256"])

    def test_the_window_count_uses_the_scorecard_horizon(self):
        keys = [self.fixture.base_key, self.fixture.gold_key]
        short = self._run(keys, scorecard=_Horizon(5.0))
        gold = short[evidence_io.record_key_str(self.fixture.gold_key)]
        base = short[evidence_io.record_key_str(self.fixture.base_key)]
        # 24 gold and 12 base points on [0, 10]: 12 and 6 are within 5.
        self.assertEqual((gold["n_snapshots"], gold["n_within_t"]), (24, 12))
        self.assertEqual((base["n_snapshots"], base["n_within_t"]), (12, 6))
        full = self._run(keys)
        self.assertEqual(full[evidence_io.record_key_str(self.fixture.gold_key)]["n_within_t"], 24)

    def test_an_ok_hash_equals_the_hash_an_arm_record_carries(self):
        spec = fixture_arm(
            train_key=self.fixture.gold_key, score_key=self.fixture.gold_key,
            beside_key=self.fixture.base_key,
        )
        data = load_arm_data(
            spec, self.context, scorecard=self.scorecard, dtype=torch.float64, device=torch.device("cpu")
        )
        report = self._run([self.fixture.gold_key, self.fixture.base_key])
        gold = report[evidence_io.record_key_str(self.fixture.gold_key)]
        base = report[evidence_io.record_key_str(self.fixture.base_key)]
        self.assertEqual(gold["windowed_sha256"], data.records["train"]["windowed_sha256"])
        self.assertEqual(base["windowed_sha256"], data.records["beside"]["windowed_sha256"])
        self.assertEqual(gold["n_within_t"], data.records["train"]["n_within_t"])

    # ------------------------------------------------------------------ how files are classified

    def test_a_file_with_no_complete_snapshot_block_is_empty(self):
        cases = {
            "zero bytes": "",
            "blank lines": "\n\n   \n",
            "text without blocks": "not a brutus file\nat all\n",
            "a partial block only": "0.0 1 0.0\n1.0 0 0 0 0 0 0\n",
        }
        keys = []
        for index, (label, content) in enumerate(cases.items()):
            key = self.spare[index]
            self._write(key, content)
            keys.append((label, key))
        report = self._run([key for _label, key in keys])
        for label, key in keys:
            with self.subTest(file=label):
                self.assertEqual(
                    report[evidence_io.record_key_str(key)],
                    {"status": "empty", "split": "train", "n_snapshots": 0},
                )

    def test_a_file_that_cannot_be_parsed_or_admitted_is_unreadable(self):
        one_block, bad_number, no_utf8 = self.spare[0], self.spare[1], self.spare[2]
        self._write(one_block, _ONE_BLOCK)
        self._write(bad_number, _BAD_NUMBER)
        _record_path(self.fixture.data_root, no_utf8).write_bytes(b"\xff\xfe\x00 not utf-8 \xff")
        report = self._run([one_block, bad_number, no_utf8])
        entries = [report[evidence_io.record_key_str(key)] for key in (one_block, bad_number, no_utf8)]
        self.assertEqual([entry["status"] for entry in entries], ["unreadable"] * 3)
        self.assertEqual(
            [entry["error_type"] for entry in entries],
            ["NotAdmitted", "ValueError", "UnicodeDecodeError"],
        )
        self.assertIn("insufficient_snapshots", entries[0]["message"])

    def test_a_directory_in_place_of_a_file_is_unreadable_and_its_path_is_redacted(self):
        key = self.spare[0]
        path = _record_path(self.fixture.data_root, key)
        path.mkdir(parents=True)
        entry = self._run([key])[evidence_io.record_key_str(key)]
        self.assertEqual((entry["status"], entry["error_type"]), ("unreadable", "IsADirectoryError"))
        message = entry["message"]
        self.assertNotIn(str(self.fixture.data_root), message)
        self.assertNotIn(str(path), message)
        self.assertNotIn(str(Path.home()), message)
        self.assertNotIn("/", message.replace("<path>", ""))
        self.assertLessEqual(len(message), 240)

    def test_a_snapshot_count_of_zero_after_a_read_is_empty(self):
        real_load = learnability_data.load_reference

        def no_snapshots(reader, key):
            return dataclasses.replace(real_load(reader, key), n_snapshots=0)

        with mock.patch.object(learnability_data, "load_reference", no_snapshots):
            entry = self._run([self.fixture.gold_key])[evidence_io.record_key_str(self.fixture.gold_key)]
        self.assertEqual(entry, {"status": "empty", "split": "train", "n_snapshots": 0})

    def test_an_error_the_preflight_does_not_classify_is_not_swallowed(self):
        for error in (RuntimeError("boom"), KeyError("k"), TypeError("t"), AttributeError("a")):
            with self.subTest(error=type(error).__name__):
                with mock.patch.object(learnability_data, "load_reference", side_effect=error):
                    with self.assertRaises(type(error)):
                        self._run([self.fixture.gold_key])

    # ------------------------------------------------------------------ no fallback, no path

    def test_a_blocked_key_never_reads_another_record(self):
        keys = self._six()
        reader = self.fixture.reader
        with mock.patch.object(reader, "read", wraps=reader.read) as read, \
                mock.patch.object(reader, "exists", wraps=reader.exists) as exists:
            report = self._run(keys)
        read_keys = {call.args[0] for call in read.call_args_list}
        exists_keys = {call.args[0] for call in exists.call_args_list}
        self.assertEqual(read_keys, {keys[0], keys[1], keys[4], keys[5]})
        self.assertNotIn(self.fixture.test_key, exists_keys | read_keys)
        self.assertNotIn(self.missing_key, read_keys)
        # The missing gold record has a readable base sibling; it is neither probed nor read.
        self.assertTrue(_record_path(self.fixture.data_root, self.sibling_key).is_file())
        self.assertNotIn(self.sibling_key, exists_keys | read_keys)
        self.assertEqual(exists_keys, {keys[0], keys[1], keys[3], keys[4], keys[5]})
        # No entry names a record other than the six asked about.
        named = set(KEY_TEXT.findall(json.dumps(report, sort_keys=True)))
        self.assertEqual(named, {evidence_io.record_key_str(key) for key in keys})

    def test_a_refused_key_opens_no_file(self):
        def opened(*_args, **_kwargs):
            raise AssertionError("opened")

        with mock.patch("builtins.open", side_effect=opened) as plain, \
                mock.patch("io.open", side_effect=opened) as io_open, \
                mock.patch("pathlib.Path.open", side_effect=opened) as path_open, \
                mock.patch("pathlib.Path.read_text", side_effect=opened) as read_text:
            report = self._run([self.fixture.test_key, RecordKey("hierarchical", "base", 999999)])
        self.assertEqual([entry["status"] for entry in report.values()], ["refused", "refused"])
        for spy in (plain, io_open, path_open, read_text):
            self.assertEqual(spy.call_count, 0)
        counts = self.fixture.reader.read_counts()
        self.assertEqual((counts["train"], counts["validation"], counts["refusals"]), (0, 0, 0))

    def test_the_report_names_no_path_and_is_canonical_json(self):
        keys = self._six()
        path_key = self.spare[2]
        _record_path(self.fixture.data_root, path_key).mkdir(parents=True)
        report = self._run(keys + [path_key])
        raw = evidence_io.canonical_json_bytes(report)
        evidence_io.guard_redaction(raw, data_root=self.fixture.data_root)
        text = raw.decode("ascii")
        for private in (str(self.fixture.data_root), str(self.tmp), str(Path.home())):
            self.assertNotIn(private, text)
        self.assertEqual(json.loads(text), report)

    def test_a_key_that_is_not_a_record_key_is_a_type_error_before_any_record_is_touched(self):
        reader = self.fixture.reader
        for bad in ("hierarchical/gold/0", Path("hierarchical/gold/0"), PhysicalKey("hierarchical", 0), None, 7):
            with self.subTest(key=bad):
                with mock.patch.object(reader, "read", wraps=reader.read) as read, \
                        mock.patch.object(reader, "exists", wraps=reader.exists) as exists:
                    with self.assertRaises(TypeError):
                        self._run([self.fixture.gold_key, bad])
                self.assertEqual((read.call_count, exists.call_count), (0, 0))

    def test_no_keys_give_an_empty_report_and_a_repeated_key_one_entry(self):
        self.assertEqual(self._run([]), {})
        report = self._run([self.fixture.gold_key, self.fixture.gold_key])
        self.assertEqual(list(report), [evidence_io.record_key_str(self.fixture.gold_key)])


if __name__ == "__main__":
    unittest.main()
