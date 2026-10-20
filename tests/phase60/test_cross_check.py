"""Phase 60 (SPEC Requirement 3, GAP-60-07, SPEC Requirement 7): the CPU float64 cross-check
and the counting rule.

Two things are guarded here. First, every scored state is re-scored on the CPU in float64
beside the official score: agreement lets the arm proceed, and any difference in the tier or
in the counts boolean stops for the owner and never lets the better of the two scores through.
Second, a counted arm compares its position error with the committed two-Kepler formula
through the frozen ``counts`` (strictly less), while a probe never calls ``counts`` at all.

Every arm in this module is a fixture arm on the tiny corpus; nothing reads the real one.
"""

from __future__ import annotations

import dataclasses
import json
import tempfile
import unittest
from contextlib import ExitStack
from pathlib import Path
from typing import Any
from unittest import mock

import numpy as np
import torch

from pinn.verification import learnability_run
from pinn.verification.feasibility_scorer import ScoreResult
from pinn.verification.feasibility_scorecard import (
    OwnerRouted,
    counts,
    load_scorecard,
    tier_of,
)
from pinn.verification.learnability_arms import (
    FORMULA_NOT_APPLICABLE,
    arm_evidence_dir,
    fixture_arm,
)
from pinn.verification.learnability_data import fixture_context, load_arm_data
from pinn.verification.learnability_run import (
    CrossCheckDisagreement,
    cross_check_state,
    run_arm,
)
from tests.phase60._fixtures import gold_corpus_fixture

FIXTURE_RUNTIME = ("float64", "cpu")
CPU = torch.device("cpu")
FIXTURE_FORMULA_SHA = "a" * 64


class _Accounted:
    """One recorded call to ``counts``."""

    def __init__(self, args: tuple, kwargs: dict):
        self.tier = args[0]
        self.E = args[1]
        self.formula = args[2]
        self.pair = (args[0], args[1])


class _Recorder:
    def __init__(self, function):
        self.function = function
        self.calls: list[_Accounted] = []

    def __call__(self, *args, **kwargs) -> Any:
        self.calls.append(_Accounted(args, kwargs))
        return self.function(*args, **kwargs)

    @property
    def pairs(self):
        return {call.pair for call in self.calls}


class _FixtureCase(unittest.TestCase):
    def setUp(self):
        stack = ExitStack()
        self.addCleanup(stack.close)
        self.fixture = stack.enter_context(gold_corpus_fixture())
        self.root = Path(stack.enter_context(tempfile.TemporaryDirectory(prefix="phase60-cc-")))
        self.scorecard = load_scorecard()
        self.context = fixture_context(
            allowlist=self.fixture.allowlist, reader=self.fixture.reader, stats=self.fixture.stats
        )

    def spec(self, **changes):
        base = fixture_arm(
            train_key=self.fixture.gold_key,
            score_key=self.fixture.gold_key,
            beside_key=self.fixture.base_key,
        )
        return dataclasses.replace(base, **changes) if changes else base

    def run_fixture(self, spec, **options):
        settings = dict(
            context=self.context,
            scorecard=self.scorecard,
            runtime=FIXTURE_RUNTIME,
            evidence_root=self.root,
            fixture_budget_steps=2,
            fixture_timing_steps=50,
        )
        settings.update(options)
        return run_arm(spec, **settings)

    def arm_dir(self, spec):
        return arm_evidence_dir(spec.arm_id, evidence_root=self.root)

    def state_dict(self, first_omega_0=30.0):
        model = learnability_run.build_arm_network(
            first_omega_0, dtype=torch.float64, device=CPU
        )
        return {name: tensor.detach().cpu() for name, tensor in model.state_dict().items()}

    def arm_data(self, spec):
        return load_arm_data(
            spec, self.context, scorecard=self.scorecard, dtype=torch.float64, device=CPU
        )


class AgreementTests(_FixtureCase):
    """GAP-60-07: the CPU float64 re-score is reported beside the official score."""

    def test_cross_check_state_scores_the_saved_weights_on_the_cpu_in_float64(self):
        spec = self.spec()
        result, counted = cross_check_state(
            self.state_dict(), spec, self.arm_data(spec), 30.0,
            scorecard=self.scorecard, formula=None,
        )
        self.assertIsInstance(result, ScoreResult)
        self.assertEqual(result.grid, "gold")
        self.assertEqual(result.velocity_source, "autograd")
        self.assertIsNone(counted)

    def test_a_counted_state_also_returns_its_counts_boolean(self):
        spec = self.spec(counted=True)
        _result, counted = cross_check_state(
            self.state_dict(), spec, self.arm_data(spec), 30.0,
            scorecard=self.scorecard, formula=1e9,
        )
        self.assertIsInstance(counted, bool)

    def test_the_arm_proceeds_when_tier_and_counts_agree_and_records_both_states(self):
        spec = self.spec()
        record = self.run_fixture(spec)
        for state in ("adam", "polish"):
            block = record["states"][state]["cross_check"]
            self.assertEqual(sorted(block), ["E", "counts", "eps_h", "tier"])
            self.assertEqual(block["tier"], record["states"][state]["score_gold"]["tier"])
            self.assertIsNone(block["counts"])
            self.assertIsInstance(block["E"], float)
            self.assertIsInstance(block["eps_h"], float)
        self.assertTrue((self.arm_dir(spec) / "record.json").is_file())

    def test_the_cross_check_scores_the_same_float32_rounded_ic13(self):
        captured = {}
        real = learnability_run.score_network

        def spy(model, ic13, masses, ref_positions, inner_pair, times, **kwargs):
            captured.setdefault("ic13", []).append(ic13)
            captured.setdefault("dtype", []).append(kwargs.get("dtype"))
            captured.setdefault("device", []).append(kwargs.get("device"))
            return real(model, ic13, masses, ref_positions, inner_pair, times, **kwargs)

        spec = self.spec()
        data = self.arm_data(spec)
        with mock.patch.object(learnability_run, "score_network", spy):
            cross_check_state(
                self.state_dict(), spec, data, 30.0,
                scorecard=self.scorecard, formula=None,
            )
        expected = np.asarray(data.ic13, dtype=np.float32).astype(np.float64)
        self.assertTrue(np.array_equal(captured["ic13"][0], expected))
        self.assertEqual(captured["dtype"], [torch.float64])
        self.assertEqual([item.type for item in captured["device"]], ["cpu"])


class DisagreementTests(_FixtureCase):
    """SPEC Requirement 3: a tier or counts difference stops for the owner, never the better score."""

    def _disagree_on_the_second_state(self, *, tier_shift: int = 0, flip_counts: bool = False):
        """Patch the CPU path so the polish state's cross-check differs from the official one."""
        real = learnability_run.cross_check_state
        calls = {"n": 0}

        def patched(*args, **kwargs):
            calls["n"] += 1
            result, counted = real(*args, **kwargs)
            if calls["n"] == 2:  # adam is scored first, the polish state second
                if tier_shift:
                    result = dataclasses.replace(result, tier=int(result.tier) + tier_shift)
                if flip_counts and counted is not None:
                    counted = not counted
            return result, counted

        return mock.patch.object(learnability_run, "cross_check_state", patched)

    def test_a_tier_difference_writes_the_owner_stop_and_raises(self):
        spec = self.spec()
        with self._disagree_on_the_second_state(tier_shift=1):
            with self.assertRaises(CrossCheckDisagreement) as caught:
                self.run_fixture(spec)
        message = str(caught.exception)
        self.assertIn("polish", message)
        arm_dir = self.arm_dir(spec)
        self.assertFalse((arm_dir / "record.json").exists())
        stop = json.loads((arm_dir / "owner-stop.json").read_text(encoding="utf-8"))
        self.assertEqual(stop["stage"], "cross_check")
        self.assertEqual(stop["reason"], message)
        self.assertEqual(stop["details"]["state"], "polish")
        official = stop["details"]["official"]
        self.assertEqual(sorted(official), ["E", "counts", "eps_h", "tier"])
        self.assertEqual(sorted(stop["details"]["cross_check"]), ["E", "counts", "eps_h", "tier"])
        self.assertEqual(stop["details"]["cross_check"]["tier"], official["tier"] + 1)
        # Both scored states' weights were written before the stop was recorded.
        self.assertTrue((arm_dir / "adam.weights").is_file())
        self.assertTrue((arm_dir / "polish.weights").is_file())
        loaded = torch.load(arm_dir / "polish.weights", map_location="cpu", weights_only=True)
        self.assertTrue(loaded)

    def test_the_cpu_score_never_reaches_the_better_state_rule(self):
        spec = self.spec()
        with mock.patch.object(
            learnability_run, "better_state", wraps=learnability_run.better_state
        ) as rule, self._disagree_on_the_second_state(tier_shift=1):
            with self.assertRaises(CrossCheckDisagreement):
                self.run_fixture(spec)
        self.assertEqual(rule.call_count, 0)

    def test_a_counts_difference_also_stops_the_arm(self):
        spec = self.spec(counted=True)
        with mock.patch.object(
            learnability_run, "formula_reference",
            return_value=({int(spec.system_id): 1e9}, FIXTURE_FORMULA_SHA),
        ), self._disagree_on_the_second_state(flip_counts=True):
            with self.assertRaises(CrossCheckDisagreement) as caught:
                self.run_fixture(spec)
        self.assertIn("counts", str(caught.exception))
        stop = json.loads(
            (self.arm_dir(spec) / "owner-stop.json").read_text(encoding="utf-8")
        )
        self.assertEqual(stop["stage"], "cross_check")
        self.assertIsNotNone(stop["details"]["official"]["counts"])
        self.assertIsNot(
            stop["details"]["official"]["counts"], stop["details"]["cross_check"]["counts"]
        )

    def test_a_disagreement_on_the_adam_state_stops_before_the_polish_writes_weights(self):
        spec = self.spec()
        real = learnability_run.cross_check_state

        def patched(*args, **kwargs):
            result, counted = real(*args, **kwargs)
            return dataclasses.replace(result, tier=(int(result.tier) + 1) % 4), counted

        with mock.patch.object(learnability_run, "cross_check_state", patched):
            with self.assertRaises(CrossCheckDisagreement):
                self.run_fixture(spec)
        arm_dir = self.arm_dir(spec)
        self.assertTrue((arm_dir / "adam.weights").is_file())
        self.assertFalse((arm_dir / "polish.weights").exists())
        self.assertFalse((arm_dir / "record.json").exists())


class CountsTests(_FixtureCase):
    """SPEC Requirement 7 and FEAS-01 (v): the frozen counting rule, strictly less."""

    def test_equal_error_does_not_count(self):
        self.assertFalse(counts(1, 0.5, 0.5, scorecard=self.scorecard))
        self.assertTrue(counts(1, 0.4, 0.5, scorecard=self.scorecard))

    def test_a_non_finite_energy_error_stays_eligible_at_tier_one(self):
        tier = tier_of(0.1, float("nan"), scorecard=self.scorecard)
        self.assertEqual(tier, 1)
        self.assertTrue(counts(tier, 0.1, 0.5, scorecard=self.scorecard))

    def test_a_tier_zero_never_counts(self):
        self.assertFalse(counts(0, 0.001, 0.5, scorecard=self.scorecard))

    def test_a_counted_arm_calls_counts_on_each_scored_state_with_the_official_values(self):
        spec = self.spec(counted=True)
        recorder = _Recorder(learnability_run.counts)
        with mock.patch.object(
            learnability_run, "formula_reference",
            return_value=({int(spec.system_id): 1e9}, FIXTURE_FORMULA_SHA),
        ), mock.patch.object(learnability_run, "counts", recorder):
            record = self.run_fixture(spec)
        self.assertEqual(record["formula"]["source_sha256"], FIXTURE_FORMULA_SHA)
        self.assertEqual(record["formula"]["E_formula"], 1e9)
        self.assertIsInstance(record["formula"]["counts"], bool)
        official = {
            (record["states"][state]["score_gold"]["tier"], record["states"][state]["score_gold"]["E"])
            for state in ("adam", "polish")
        }
        cross = {
            (record["states"][state]["cross_check"]["tier"], record["states"][state]["cross_check"]["E"])
            for state in ("adam", "polish")
        }
        self.assertTrue(official <= recorder.pairs)
        self.assertTrue(cross <= recorder.pairs)
        # Two official calls, one per scored state; two cross-check calls; one on the result.
        self.assertEqual(len(recorder.calls), 5)

    def test_a_missing_formula_writes_the_stop_and_re_raises_the_same_exception(self):
        spec = self.spec(counted=True)
        stop = OwnerRouted("two-Kepler formula not applicable on a counted system")
        with mock.patch.object(
            learnability_run, "formula_reference", return_value=({}, FIXTURE_FORMULA_SHA),
        ), mock.patch.object(learnability_run, "counts", side_effect=stop):
            with self.assertRaises(OwnerRouted) as caught:
                self.run_fixture(spec)
        self.assertIs(caught.exception, stop)
        arm_dir = self.arm_dir(spec)
        self.assertFalse((arm_dir / "record.json").exists())
        record = json.loads((arm_dir / "owner-stop.json").read_text(encoding="utf-8"))
        self.assertEqual(record["stage"], "counts")
        self.assertEqual(record["reason"], str(stop))
        self.assertEqual(record["details"]["arm_id"], spec.arm_id)
        self.assertIsNone(record["details"]["E_formula"])


class ProbeCountsTests(_FixtureCase):
    """SPEC Requirement 7: a probe is never counted and never calls counts."""

    def test_a_probe_arm_calls_counts_zero_times(self):
        spec = self.spec(rung="probe-2b", loss_arm="data_only")
        self.assertFalse(spec.counted)
        recorder = _Recorder(learnability_run.counts)
        with mock.patch.object(learnability_run, "counts", recorder):
            record = self.run_fixture(spec)
        self.assertEqual(recorder.calls, [])
        self.assertEqual(
            record["formula"],
            {"E_formula": FORMULA_NOT_APPLICABLE, "counts": None, "source_sha256": None},
        )

    def test_an_uncounted_probe_record_carries_the_ratified_note(self):
        spec = self.spec(rung="probe-2b")
        record = self.run_fixture(spec)
        self.assertEqual(record["formula"]["E_formula"], FORMULA_NOT_APPLICABLE)
        self.assertIsNone(record["formula"]["counts"])
        self.assertTrue(
            any("D-05" in note for note in record["readout_notes"]),
            record["readout_notes"],
        )


if __name__ == "__main__":
    unittest.main()
