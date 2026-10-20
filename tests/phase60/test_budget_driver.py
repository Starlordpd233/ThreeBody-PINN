"""Phase 60 (INST-05, FEAS-03): the frozen budget rule on a fixture arm, and its branches.

The tracer runs one fixture arm through its own timing run, the frozen budget,
the scoring cadence, the frozen budget outcome and the polish, and recomputes
the budget numbers from the record. The unit classes drive the budget driver with
fakes (no training) and run fixture arms on CPU float64. Nothing here is a real
Rung 1 result, and no test opens the real corpus.
"""

from __future__ import annotations

import ast
import dataclasses
import inspect
import json
import tempfile
import textwrap
import unittest
from contextlib import ExitStack
from pathlib import Path
from types import SimpleNamespace
from unittest import mock

import torch

from pinn.verification import learnability_arms, learnability_run
from pinn.verification.feasibility_scorecard import budget_outcome, load_scorecard, steps_budget
from pinn.verification.learnability_arms import arm_evidence_dir, fixture_arm
from pinn.verification.learnability_data import HarnessHalt, fixture_context, load_arm_data
from pinn.verification.learnability_run import run_arm
from tests.phase60._fixtures import gold_corpus_fixture

FIXTURE_RUNTIME = ("float64", "cpu")
CPU = torch.device("cpu")
CAP_HOURS = 3.0  # budget_rule.cap_hours_single_system in the frozen scorecard


def _fn(test, name):
    """A missing runner function is an assertion failure, not an import error."""
    function = getattr(learnability_run, name, None)
    test.assertIsNotNone(function, f"pinn.verification.learnability_run.{name} is missing")
    return function


def _spec_and_context(fixture, **changes):
    spec = fixture_arm(
        train_key=fixture.gold_key, score_key=fixture.gold_key, beside_key=fixture.base_key
    )
    if changes:
        spec = dataclasses.replace(spec, **changes)
    context = fixture_context(
        allowlist=fixture.allowlist, reader=fixture.reader, stats=fixture.stats
    )
    return spec, context


def _final_budget(budget):
    """The last step the arm was budgeted to reach: B, or the extension's 2B."""
    return budget["new_budget_steps"] if budget["extended"] else budget["budget_steps"]


class FixtureBudgetTracerTests(unittest.TestCase):
    """One fixture arm, end to end, and the budget numbers recomputed from its record."""

    @classmethod
    def setUpClass(cls):
        stack = ExitStack()
        cls.addClassCleanup(stack.close)
        cls.fixture = stack.enter_context(gold_corpus_fixture())
        cls.root = Path(stack.enter_context(tempfile.TemporaryDirectory(prefix="phase60-budget-")))
        cls.scorecard = load_scorecard()
        cls.spec, cls.context = _spec_and_context(cls.fixture)
        cls.record = run_arm(
            cls.spec,
            context=cls.context,
            scorecard=cls.scorecard,
            runtime=FIXTURE_RUNTIME,
            evidence_root=cls.root,
            fixture_budget_steps=12,
            fixture_timing_steps=50,
        )
        cls.arm_dir = arm_evidence_dir(cls.spec.arm_id, evidence_root=cls.root)
        cls.on_disk = json.loads((cls.arm_dir / "record.json").read_bytes())

    def test_the_timing_run_is_recorded_with_its_steps_and_wall_time(self):
        timing = self.on_disk["timing"]
        self.assertEqual(sorted(timing), ["seconds_per_step", "steps", "wall_seconds"])
        self.assertEqual(timing["steps"], 50)
        self.assertGreater(timing["wall_seconds"], 0.0)
        self.assertGreater(timing["seconds_per_step"], 0.0)
        self.assertEqual(timing["seconds_per_step"], timing["wall_seconds"] / timing["steps"])

    def test_the_frozen_budget_is_the_frozen_function_of_the_recorded_timing(self):
        timing = self.on_disk["timing"]
        self.assertEqual(
            self.on_disk["budget"]["frozen_budget_steps"],
            steps_budget(CAP_HOURS, timing["wall_seconds"], timing["steps"], scorecard=self.scorecard),
        )

    def test_a_fixture_arm_runs_its_own_small_budget_and_says_so(self):
        budget = self.on_disk["budget"]
        self.assertEqual(budget["rule"], "fixture")
        self.assertEqual(budget["budget_steps"], 12)
        self.assertEqual(self.on_disk["schedule"]["cosine_t_max"], 12)
        self.assertFalse(budget["cadence_enforced"])

    def test_readings_run_from_step_zero_to_the_final_budget(self):
        budget = self.on_disk["budget"]
        self.assertEqual(budget["reading_steps"][0], 0)
        self.assertEqual(budget["reading_steps"][-1], _final_budget(budget))
        self.assertEqual([step for step, _ in budget["readings"]], budget["reading_steps"])
        self.assertEqual([entry["step"] for entry in self.on_disk["trace"]], budget["reading_steps"])

    def test_the_outcome_is_the_frozen_outcome_of_the_recorded_readings(self):
        budget = self.on_disk["budget"]
        if budget["outcome"] == "diverged":
            self.assertIsNotNone(budget["diverged_at_step"])
            return
        recomputed = budget_outcome(
            budget["readings"], _final_budget(budget), extended=budget["extended"],
            scorecard=self.scorecard,
        )
        self.assertEqual(budget["outcome"], recomputed["outcome"])
        self.assertEqual(budget["rate_per_step"], recomputed.get("rate_per_step"))
        self.assertIsNone(budget["diverged_at_step"])
        self.assertEqual(self.on_disk["schedule"]["cosines"], 2 if budget["extended"] else 1)

    def test_adam_wall_time_covers_the_steps_and_the_readings(self):
        wall = self.on_disk["wall"]
        self.assertGreater(wall["adam_seconds"], 0.0)
        self.assertLessEqual(wall["adam_seconds"], wall["total_seconds"])

    def test_the_arm_starts_from_its_own_seed_42_initialization_not_the_timed_network(self):
        data = load_arm_data(
            self.spec, self.context, scorecard=self.scorecard, dtype=torch.float64, device=CPU
        )
        fresh = learnability_run._score(
            learnability_run.build_arm_network(30.0, dtype=torch.float64, device=CPU),
            data, data.score, scorecard=self.scorecard, dtype=torch.float64, device=CPU,
        )
        self.assertEqual(self.on_disk["budget"]["readings"][0], [0, fresh.E])

    def test_no_timing_weights_are_kept(self):
        self.assertEqual(
            sorted(path.name for path in self.arm_dir.iterdir()),
            ["adam.weights", "polish.weights", "record.json"],
        )

    def test_drive_adam_has_no_numeric_literal_but_zero_and_one(self):
        driver = _fn(self, "drive_adam")
        tree = ast.parse(textwrap.dedent(inspect.getsource(driver)))
        numbers = {
            node.value
            for node in ast.walk(tree)
            if isinstance(node, ast.Constant)
            and isinstance(node.value, (int, float))
            and not isinstance(node.value, bool)
        }
        self.assertLessEqual(numbers, {0, 1}, "drive_adam holds a threshold literal")


class TimingRunTests(unittest.TestCase):
    """GAP-60-04: a separate run of the exact arm configuration, every step timed."""

    @classmethod
    def setUpClass(cls):
        stack = ExitStack()
        cls.addClassCleanup(stack.close)
        cls.fixture = stack.enter_context(gold_corpus_fixture())
        cls.scorecard = load_scorecard()
        cls.spec, cls.context = _spec_and_context(cls.fixture)
        cls.data = load_arm_data(
            cls.spec, cls.context, scorecard=cls.scorecard, dtype=torch.float64, device=CPU
        )

    def _timing(self, **options):
        settings = dict(
            context=self.context, scorecard=self.scorecard, runtime=FIXTURE_RUNTIME,
            first_omega_0=30.0, steps=50, data=self.data,
        )
        settings.update(options)
        return _fn(self, "timing_run")(self.spec, **settings)

    def test_it_returns_the_steps_the_wall_time_and_seconds_per_step(self):
        timing = self._timing()
        self.assertEqual(sorted(timing), ["seconds_per_step", "steps", "wall_seconds"])
        self.assertEqual(timing["steps"], 50)
        self.assertGreater(timing["wall_seconds"], 0.0)
        self.assertEqual(timing["seconds_per_step"], timing["wall_seconds"] / 50)

    def test_the_clock_is_read_once_before_and_once_after_the_steps_with_a_sync_before_each(self):
        events = []

        def clock():
            events.append("clock")
            return float(len(events))

        steps = []
        real_loss = learnability_run.data_only_loss

        def counting_loss(*args, **kwargs):
            events.append("step")
            steps.append(1)
            return real_loss(*args, **kwargs)

        with mock.patch.object(
            learnability_run, "_synchronize", side_effect=lambda device: events.append("sync")
        ), mock.patch.object(learnability_run, "data_only_loss", counting_loss):
            timing = self._timing(clock=clock)
        self.assertEqual(len(steps), 50)
        self.assertEqual(events[:2], ["sync", "clock"])
        self.assertEqual(events[-2:], ["sync", "clock"])
        self.assertEqual(events.count("clock"), 2)
        self.assertEqual(events.count("sync"), 2)
        # The first step is inside the timed region: no warm-up step is left out.
        self.assertEqual(events[2], "step")
        self.assertEqual(timing["wall_seconds"], float(len(events)) - 2.0)

    def test_a_timing_run_shorter_than_the_frozen_minimum_is_refused(self):
        for bad in (49, 0, -1, 50.0, True, None):
            with self.subTest(steps=bad):
                with self.assertRaises(HarnessHalt):
                    self._timing(steps=bad)

    def test_synchronize_acts_only_on_an_mps_device(self):
        synchronize = _fn(self, "_synchronize")
        with mock.patch.object(torch.mps, "synchronize") as sync:
            synchronize(CPU)
            synchronize(SimpleNamespace(type="cuda"))
            self.assertEqual(sync.call_count, 0)
            synchronize(SimpleNamespace(type="mps"))
            self.assertEqual(sync.call_count, 1)

    def test_the_step_counts_are_500_for_a_data_only_arm_and_50_with_a_physics_term(self):
        steps_for = _fn(self, "timing_steps_for")
        self.assertEqual(steps_for(self.spec, scorecard=self.scorecard), 500)
        self.assertEqual(learnability_arms.TIMING_STEPS, {"data_only": 500, "physics": 50})
        for loss_arm in ("physics_ic", "full"):
            with self.subTest(loss_arm=loss_arm):
                spec = dataclasses.replace(self.spec, loss_arm=loss_arm)
                self.assertEqual(steps_for(spec, scorecard=self.scorecard), 50)

    def test_a_step_count_below_the_frozen_minimum_is_refused(self):
        steps_for = _fn(self, "timing_steps_for")
        with mock.patch.object(learnability_run, "TIMING_STEPS", {"data_only": 49, "physics": 50}):
            with self.assertRaises(HarnessHalt):
                steps_for(self.spec, scorecard=self.scorecard)
        with mock.patch.object(learnability_run, "TIMING_STEPS", {"data_only": 500, "physics": 49}):
            with self.assertRaises(HarnessHalt):
                steps_for(self.spec, scorecard=self.scorecard)

    def test_the_budget_is_the_frozen_steps_budget_at_the_scorecard_cap(self):
        from_timing = _fn(self, "budget_from_timing")
        timing = {"steps": 50, "wall_seconds": 600.0, "seconds_per_step": 12.0}
        self.assertEqual(from_timing(timing, scorecard=self.scorecard), 900)
        for wall, steps in ((3.7, 50), (123.456, 500), (0.0123, 50)):
            with self.subTest(wall=wall, steps=steps):
                timing = {"steps": steps, "wall_seconds": wall, "seconds_per_step": wall / steps}
                self.assertEqual(
                    from_timing(timing, scorecard=self.scorecard),
                    steps_budget(CAP_HOURS, wall, steps, scorecard=self.scorecard),
                )


class RealArmBudgetTests(unittest.TestCase):
    """A real arm sizes itself from its own timing run. Only the budget is replaced, with a small one."""

    @classmethod
    def setUpClass(cls):
        stack = ExitStack()
        cls.addClassCleanup(stack.close)
        cls.fixture = stack.enter_context(gold_corpus_fixture())
        cls.root = Path(stack.enter_context(tempfile.TemporaryDirectory(prefix="phase60-real-")))
        cls.scorecard = load_scorecard()
        spec, context = _spec_and_context(cls.fixture)
        cls.spec = dataclasses.replace(spec, run_kind="real")
        cls.context = dataclasses.replace(context, run_kind="real")
        with mock.patch.object(learnability_run, "budget_from_timing", return_value=40) as budget:
            cls.record = run_arm(
                cls.spec, context=cls.context, scorecard=cls.scorecard,
                runtime=FIXTURE_RUNTIME, evidence_root=cls.root,
            )
        cls.budget_call = budget.call_args
        cls.budget_calls = budget.call_count

    def test_the_budget_comes_from_the_recorded_timing_through_the_frozen_rule(self):
        self.assertEqual(self.record["run_kind"], "real")
        self.assertEqual(self.record["budget"]["rule"], "frozen")
        self.assertEqual(self.record["budget"]["budget_steps"], 40)
        self.assertEqual(self.record["budget"]["frozen_budget_steps"], 40)
        self.assertEqual(self.budget_calls, 1)
        self.assertEqual(self.budget_call.args[0], self.record["timing"])
        self.assertEqual(set(self.budget_call.kwargs), {"scorecard"})

    def test_a_data_only_arm_times_500_steps(self):
        self.assertEqual(self.record["timing"]["steps"], 500)

    def test_the_frozen_cadence_is_enforced_for_a_real_arm(self):
        budget = self.record["budget"]
        self.assertTrue(budget["cadence_enforced"])
        self.assertTrue(budget["cadence_ok"])
        steps = budget["reading_steps"]
        self.assertEqual(steps[:3], [0, 2, 4])
        self.assertLessEqual(
            max(right - left for left, right in zip(steps, steps[1:])),
            0.05 * _final_budget(budget),
        )

    def test_a_real_arm_refuses_the_fixture_knobs_before_anything_is_written(self):
        with tempfile.TemporaryDirectory(prefix="phase60-real-refuse-") as other:
            for knob in ({"fixture_budget_steps": 5}, {"fixture_timing_steps": 50}):
                with self.subTest(knob=knob):
                    with self.assertRaises(HarnessHalt):
                        run_arm(
                            self.spec, context=self.context, scorecard=self.scorecard,
                            runtime=FIXTURE_RUNTIME, evidence_root=Path(other), **knob,
                        )
            self.assertEqual(list(Path(other).rglob("*")), [])

    def test_a_real_arm_on_a_fixture_context_is_refused(self):
        fixture_ctx = dataclasses.replace(self.context, run_kind="fixture")
        with tempfile.TemporaryDirectory(prefix="phase60-real-refuse-") as other:
            with self.assertRaises(HarnessHalt):
                run_arm(
                    self.spec, context=fixture_ctx, scorecard=self.scorecard,
                    runtime=FIXTURE_RUNTIME, evidence_root=Path(other),
                )
            self.assertEqual(list(Path(other).rglob("*")), [])


if __name__ == "__main__":
    unittest.main()
