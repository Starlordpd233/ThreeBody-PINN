"""Phase 60 (INST-05 b): a test-split key is refused before any path exists.

Arms hold ``RecordKey`` values from a closed catalog and never accept a path.
Every corpus read goes through ``SplitAllowlist.require`` first, so a key from
the withheld split raises ``SplitRefused`` with no file opened. The open
attestation, which counts opens under the data root, is process-global and
irreversible, so its counts are read in child processes that each own one data
root (60-PATTERNS S7).
"""

from __future__ import annotations

import dataclasses
import json
import subprocess
import sys
import unittest
from contextlib import ExitStack
from pathlib import Path
from unittest import mock

import torch

from pinn.data.types import RecordKey
from pinn.verification.feasibility_scorecard import load_scorecard
from pinn.verification.learnability_arms import ArmSpec, arm_spec, catalog, fixture_arm
from pinn.verification.learnability_data import fixture_context, load_arm_data
from pinn.verification.split_allowlist import SplitRefused
from tests.phase60._fixtures import gold_corpus_fixture

ROOT = Path(__file__).resolve().parents[2]
CPU = torch.device("cpu")


def _load(spec, context, scorecard):
    return load_arm_data(spec, context, scorecard=scorecard, dtype=torch.float64, device=CPU)


class TestSplitRefusalTests(unittest.TestCase):
    """The withheld split is refused before any file is opened, in every role."""

    def setUp(self):
        stack = ExitStack()
        self.addCleanup(stack.close)
        self.fixture = stack.enter_context(gold_corpus_fixture())
        self.context = fixture_context(
            allowlist=self.fixture.allowlist, reader=self.fixture.reader, stats=self.fixture.stats
        )
        # Loaded here: reading the scorecard file is itself an open, which the spies must not see.
        self.scorecard = load_scorecard()

    def _spec(self, **keys):
        roles = dict(
            train_key=self.fixture.gold_key, score_key=self.fixture.gold_key,
            beside_key=self.fixture.base_key,
        )
        roles.update(keys)
        return fixture_arm(**roles)

    def _no_open(self):
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

    def test_the_test_key_is_a_withheld_key(self):
        with self.assertRaises(SplitRefused):
            self.fixture.allowlist.require(self.fixture.test_key)

    def test_a_test_key_in_any_role_is_refused_before_any_open(self):
        for role in ("train_key", "score_key", "beside_key"):
            with self.subTest(role=role):
                spec = self._spec(**{role: self.fixture.test_key})
                stack, spies = self._no_open()
                with stack:
                    with self.assertRaises(SplitRefused):
                        _load(spec, self.context, self.scorecard)
                for spy in spies:
                    self.assertEqual(spy.call_count, 0)
        counts = self.fixture.reader.read_counts()
        self.assertEqual((counts["train"], counts["validation"]), (0, 0))

    def test_an_unknown_key_is_refused_like_a_test_key(self):
        spec = self._spec(train_key=RecordKey("hierarchical", "gold", 999999))
        stack, spies = self._no_open()
        with stack:
            with self.assertRaises(SplitRefused):
                _load(spec, self.context, self.scorecard)
        self.assertEqual([spy.call_count for spy in spies], [0, 0, 0, 0])

    def test_the_refusal_comes_before_the_scored_horizon_is_even_read(self):
        class _NoScorecard:
            def section(self, name):
                raise AssertionError("the scorecard was read before the allowlist was asked")

        spec = self._spec(train_key=self.fixture.test_key)
        with self.assertRaises(SplitRefused):
            _load(spec, self.context, scorecard=_NoScorecard())

    def test_a_string_or_path_is_never_an_arm_record(self):
        keys = dict(
            train_key=self.fixture.gold_key, score_key=self.fixture.gold_key,
            beside_key=self.fixture.base_key,
        )
        for role in keys:
            for bad in ("hierarchical/gold/0", Path("hierarchical/gold/0"), "/etc/passwd", None):
                with self.subTest(role=role, value=bad):
                    with self.assertRaises(TypeError):
                        fixture_arm(**{**keys, role: bad})
                    with self.assertRaises(TypeError):
                        dataclasses.replace(arm_spec("r1-1632"), **{role: bad})

    def test_a_spec_forced_to_hold_a_path_is_still_refused_before_any_open(self):
        spec = self._spec()
        object.__setattr__(spec, "train_key", "hierarchical/gold/0")  # past the frozen dataclass
        stack, spies = self._no_open()
        with stack:
            with self.assertRaises(TypeError):
                _load(spec, self.context, self.scorecard)
        self.assertEqual([spy.call_count for spy in spies], [0, 0, 0, 0])

    def test_the_closed_catalog_holds_record_keys_only(self):
        specs = catalog()
        self.assertEqual(len(specs), 42)
        for arm_id, spec in specs.items():
            with self.subTest(arm_id=arm_id):
                self.assertIsInstance(spec, ArmSpec)
                for key in (spec.train_key, spec.score_key, spec.beside_key):
                    self.assertIsInstance(key, RecordKey)
                    self.assertIn(key.fidelity, ("base", "gold"))

_CHILD_SCRIPT = """
import json
import sys
from pathlib import Path

import torch

from pinn.data.adapter import BRUTUS_FOLDER_TABLE, BRUTUS_SUBDIR
from pinn.verification.evidence_io import record_key_str
from pinn.verification.feasibility_scorecard import load_scorecard
from pinn.verification.learnability_arms import fixture_arm
from pinn.verification.learnability_data import fixture_context, load_arm_data, preflight_records
from pinn.verification.split_allowlist import SplitRefused, install_open_attestation
from tests.phase60._fixtures import gold_corpus_fixture

mode = sys.argv[1]
cpu = torch.device("cpu")
with gold_corpus_fixture() as fx:
    attestation = install_open_attestation(
        data_root=fx.data_root,
        data_root_source=fx.data_root_source,
        withheld_basenames=fx.allowlist.withheld_basenames(),
        split_by_basename=fx.allowlist.split_by_basename(),
    )
    context = fixture_context(
        allowlist=fx.allowlist, reader=fx.reader, stats=fx.stats, attestation=attestation
    )
    scorecard = load_scorecard()
    out = {
        "mode": mode,
        "labels": {
            "gold": record_key_str(fx.gold_key),
            "base": record_key_str(fx.base_key),
            "test": record_key_str(fx.test_key),
        },
    }
    if mode == "harness":
        good = fixture_arm(train_key=fx.gold_key, score_key=fx.gold_key, beside_key=fx.base_key)
        load_arm_data(good, context, scorecard=scorecard, dtype=torch.float64, device=cpu)
        bad = fixture_arm(train_key=fx.test_key, score_key=fx.gold_key, beside_key=fx.base_key)
        try:
            load_arm_data(bad, context, scorecard=scorecard, dtype=torch.float64, device=cpu)
            out["refused"] = False
        except SplitRefused:
            out["refused"] = True
        report = preflight_records(
            [fx.gold_key, fx.base_key, fx.test_key], context, scorecard=scorecard
        )
        out["preflight"] = {key: entry["status"] for key, entry in report.items()}
    else:
        key = fx.test_key
        folder = next(
            name for name, pair in BRUTUS_FOLDER_TABLE.items()
            if pair == (key.variant, key.fidelity)
        )
        path = Path(fx.data_root) / BRUTUS_SUBDIR / folder / f"brutus_{key.variant}_{key.id:04d}.txt"
        out["withheld_file_exists"] = path.is_file()
        try:
            path.read_text(encoding="utf-8")
            out["blocked"] = False
        except SplitRefused:
            out["blocked"] = True
    out["summary"] = attestation.summary()
    print(json.dumps(out))
"""


def _child(mode):
    completed = subprocess.run(
        [sys.executable, "-B", "-c", _CHILD_SCRIPT, mode],
        cwd=str(ROOT), capture_output=True, text=True, timeout=300,
    )
    if completed.returncode != 0:
        raise AssertionError(f"child process failed:\n{completed.stderr}")
    return json.loads(completed.stdout.strip().splitlines()[-1])


class AttestationTests(unittest.TestCase):
    """The open attestation of a process that loads, refuses and preflights."""

    def test_a_refused_test_key_leaves_every_test_counter_at_zero(self):
        result = _child("harness")
        self.assertIs(result["refused"], True)
        summary = result["summary"]
        self.assertEqual(summary["test_split_opened"], 0)
        self.assertEqual(summary["blocked_attempts"], 0)
        self.assertEqual(summary["refused_before_open"], 0)
        self.assertEqual(summary["opened"]["validation"], 0)
        self.assertEqual(summary["opened"]["other_under_root"], 0)
        # Two records read by load_arm_data and the same two by the preflight, one open each;
        # the test key adds none.
        self.assertEqual(summary["opened"]["train"], 4)

    def test_the_preflight_reports_the_test_key_as_refused_in_that_process(self):
        result = _child("harness")
        labels = result["labels"]
        self.assertEqual(
            result["preflight"],
            {labels["gold"]: "ok", labels["base"]: "ok", labels["test"]: "refused"},
        )

    def test_the_hook_is_live_in_such_a_process_so_the_zeros_mean_something(self):
        result = _child("control")
        self.assertIs(result["withheld_file_exists"], True)
        self.assertIs(result["blocked"], True)
        summary = result["summary"]
        self.assertEqual(summary["blocked_attempts"], 1)
        self.assertEqual(summary["test_split_opened"], 0)
        self.assertEqual(summary["opened"]["train"], 0)


if __name__ == "__main__":
    unittest.main()
