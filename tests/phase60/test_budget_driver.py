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
import hashlib
import inspect
import json
import math
import tempfile
import textwrap
import unittest
from contextlib import ExitStack
from pathlib import Path
from types import SimpleNamespace
from unittest import mock

import torch

from pinn.training.grad_clip import GradClipper
from pinn.verification import evidence_io, learnability_arms, learnability_losses, learnability_run
from pinn.verification.feasibility_scorecard import (
    OwnerRouted,
    better_state,
    budget_outcome,
    load_scorecard,
    scoring_cadence_ok,
    steps_budget,
    tier_of,
)
from pinn.verification.learnability_arms import FirstResultExists, arm_evidence_dir, fixture_arm
from pinn.verification.learnability_data import HarnessHalt, fixture_context, load_arm_data
from pinn.verification.learnability_run import run_arm, weights_digest
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


# ---------------------------------------------------------------------------
# Task 3: the budget driver's branches, with fakes and fixture runs.
# ---------------------------------------------------------------------------

FROZEN_RATE_MESSAGE = "improvement rate is not determinable without a finite reference-window reading"
BUDGET = 100  # a 5% cadence of 5 steps: readings at 0, 5, ..., 100


class _Fakes:
    """A fake step, a fake reading and a fake clock. Each step costs 1 s and each reading 0.25 s."""

    def __init__(self, energy, *, skip_at=None, skip_reason="non_finite_loss"):
        self.energy = energy
        self.skip_at = skip_at
        self.skip_reason = skip_reason
        self.now = 0.0
        self.steps = []
        self.reads = []
        self.extensions = 0

    def clock(self):
        return self.now

    def step_fn(self, step):
        self.now += 1.0
        if step == self.skip_at:
            return self.skip_reason
        self.steps.append(step)
        return None

    def read_fn(self, step):
        self.now += 0.25
        self.reads.append(step)
        return self.energy(step)

    def on_extend(self):
        self.extensions += 1


def _drive(fakes, *, budget=BUDGET, **options):
    scorecard = options.pop("scorecard", None) or load_scorecard()
    return learnability_run.drive_adam(
        budget=budget, step_fn=fakes.step_fn, read_fn=fakes.read_fn, scorecard=scorecard,
        on_extend=fakes.on_extend, clock=fakes.clock, **options,
    )


def _flat(step):
    """Falls to 0.5 by step 25 and stays there: not improving at either budget."""
    return max(0.5, 1.0 - step / 50.0)


def _still_falling_then_flat(step):
    """Improving over the final quarter of the first budget, flat after it."""
    return 1.0 - min(step, BUDGET) / 200.0


def _falling_throughout(step):
    return math.exp(-3.0 * step / BUDGET)


class ReadingStepTests(unittest.TestCase):
    """The frozen cadence: step 0, every floor(0.05 B) steps, and B; the same interval after an extension."""

    @classmethod
    def setUpClass(cls):
        cls.scorecard = load_scorecard()

    def test_a_budget_of_860_is_read_every_43_steps_and_meets_the_frozen_cadence(self):
        steps = _fn(self, "reading_steps")(860, scorecard=self.scorecard)
        self.assertEqual((steps[0], steps[-1], len(steps)), (0, 860, 21))
        self.assertEqual({right - left for left, right in zip(steps, steps[1:])}, {43})
        self.assertTrue(
            scoring_cadence_ok(steps, 860, scorecard=self.scorecard)
        )

    def test_after_an_extension_the_same_interval_continues_to_2b(self):
        reading_steps = _fn(self, "reading_steps")
        first = reading_steps(860, scorecard=self.scorecard)
        extended = reading_steps(860, scorecard=self.scorecard, through=1720)
        self.assertEqual((extended[0], extended[-1]), (0, 1720))
        self.assertEqual([step for step in extended if step <= 860], first)
        self.assertEqual({right - left for left, right in zip(extended, extended[1:])}, {43})
        self.assertTrue(
            scoring_cadence_ok(extended, 1720, scorecard=self.scorecard)
        )

    def test_a_budget_that_is_not_a_multiple_of_the_interval_is_still_read_at_b_and_2b(self):
        reading_steps = _fn(self, "reading_steps")
        steps = reading_steps(861, scorecard=self.scorecard, through=1722)
        self.assertIn(860, steps)
        self.assertIn(861, steps)
        self.assertEqual(steps[-1], 1722)
        self.assertLessEqual(max(right - left for left, right in zip(steps, steps[1:])), 43)

    def test_a_budget_of_10_reads_every_step_but_cannot_meet_the_cadence(self):
        reading_steps = _fn(self, "reading_steps")
        self.assertEqual(
            reading_steps(10, scorecard=self.scorecard, enforce_cadence=False), list(range(11))
        )
        with self.assertRaises(HarnessHalt):
            reading_steps(10, scorecard=self.scorecard)
        with self.assertRaises(HarnessHalt):
            reading_steps(19, scorecard=self.scorecard)
        self.assertEqual(reading_steps(20, scorecard=self.scorecard), list(range(21)))

    def test_the_interval_is_read_from_the_scorecard_fraction(self):
        reading_steps = _fn(self, "reading_steps")
        looser = SimpleNamespace(
            section=lambda name: {"scoring_cadence_max_fraction": 0.1}
        )
        steps = reading_steps(860, scorecard=looser, enforce_cadence=False)
        self.assertEqual(steps[:3], [0, 86, 172])

    def test_bad_budgets_and_horizons_are_refused(self):
        reading_steps = _fn(self, "reading_steps")
        for bad in (0, -5, 50.0, True, None):
            with self.subTest(budget=bad):
                with self.assertRaises(HarnessHalt):
                    reading_steps(bad, scorecard=self.scorecard)
        with self.assertRaises(HarnessHalt):
            reading_steps(100, scorecard=self.scorecard, through=99)


class DriverBranchTests(unittest.TestCase):
    """drive_adam branches only on the frozen budget_outcome and on divergence."""

    @classmethod
    def setUpClass(cls):
        cls.scorecard = load_scorecard()

    def test_a_flat_curve_completes_at_the_budget_without_an_extension(self):
        fakes = _Fakes(_flat)
        result = _drive(fakes)
        self.assertEqual(result["outcome"], "complete")
        self.assertEqual(fakes.extensions, 0)
        self.assertEqual((result["extended"], result["new_budget_steps"]), (False, None))
        self.assertEqual(result["steps_taken"], BUDGET)
        self.assertEqual(fakes.steps, list(range(1, BUDGET + 1)))
        self.assertEqual(result["reading_steps"], list(range(0, BUDGET + 1, 5)))
        self.assertEqual(
            result["outcome"],
            budget_outcome(result["readings"], BUDGET, extended=False, scorecard=self.scorecard)[
                "outcome"
            ],
        )

    def test_a_curve_still_falling_in_the_final_quarter_extends_once_then_completes(self):
        fakes = _Fakes(_still_falling_then_flat)
        result = _drive(fakes)
        self.assertEqual(fakes.extensions, 1)
        self.assertTrue(result["extended"])
        self.assertEqual(result["new_budget_steps"], 2 * BUDGET)
        self.assertEqual(result["outcome"], "complete")
        self.assertEqual(result["steps_taken"], 2 * BUDGET)
        self.assertEqual(result["reading_steps"], list(range(0, 2 * BUDGET + 1, 5)))
        self.assertEqual(
            budget_outcome(result["readings"], 2 * BUDGET, extended=True, scorecard=self.scorecard),
            {"outcome": "complete"},
        )

    def test_a_curve_that_keeps_falling_after_the_extension_is_inconclusive_with_the_frozen_rate(self):
        fakes = _Fakes(_falling_throughout)
        result = _drive(fakes)
        self.assertEqual(fakes.extensions, 1)
        self.assertEqual(result["outcome"], "inconclusive")
        frozen = budget_outcome(
            result["readings"], 2 * BUDGET, extended=True, scorecard=self.scorecard
        )
        self.assertEqual(frozen["outcome"], "inconclusive")
        self.assertEqual(result["rate_per_step"], frozen["rate_per_step"])
        self.assertGreater(result["rate_per_step"], 0.0)

    def test_the_driver_calls_the_frozen_function_at_b_and_2b_with_the_extended_flag(self):
        fakes = _Fakes(_falling_throughout)
        with mock.patch.object(learnability_run, "budget_outcome", wraps=budget_outcome) as spy:
            _drive(fakes)
        self.assertEqual([call.args[1] for call in spy.call_args_list], [BUDGET, 2 * BUDGET])
        self.assertEqual([call.kwargs["extended"] for call in spy.call_args_list], [False, True])
        self.assertTrue(all(set(call.kwargs) == {"extended", "scorecard"} for call in spy.call_args_list))

    def test_a_zero_error_reference_gives_an_owner_routed_stop_that_propagates(self):
        fakes = _Fakes(lambda step: 0.0)
        with self.assertRaises(OwnerRouted) as caught:
            _drive(fakes)
        self.assertEqual(str(caught.exception), FROZEN_RATE_MESSAGE)
        self.assertEqual(fakes.extensions, 1)

    def test_the_owner_routed_exception_object_is_not_replaced_or_retried(self):
        raised = OwnerRouted(FROZEN_RATE_MESSAGE)
        fakes = _Fakes(_flat)
        with mock.patch.object(learnability_run, "budget_outcome", side_effect=raised) as frozen:
            with self.assertRaises(OwnerRouted) as caught:
                _drive(fakes)
        self.assertIs(caught.exception, raised)
        self.assertEqual(frozen.call_count, 1)
        self.assertEqual(fakes.steps, list(range(1, BUDGET + 1)))

    def test_a_non_finite_reference_window_extends_and_the_extension_has_a_finite_reference(self):
        # With the frozen function an all-NaN reference window gives "extend" at B (the final
        # window is finite). The readings kept from the first budget then give the longer
        # reference window a finite minimum, so the second call decides without a stop.
        fakes = _Fakes(lambda step: float("nan") if step <= 75 else 0.5)
        result = _drive(fakes)
        self.assertEqual(fakes.extensions, 1)
        self.assertEqual(result["outcome"], "complete")

    def test_adam_wall_time_is_the_sum_of_every_step_and_every_reading(self):
        fakes = _Fakes(_flat)
        result = _drive(fakes)
        self.assertEqual(result["adam_seconds"], 100 * 1.0 + 21 * 0.25)
        fakes = _Fakes(_still_falling_then_flat)
        result = _drive(fakes)
        self.assertEqual(result["adam_seconds"], 200 * 1.0 + 41 * 0.25)

    def test_the_driver_is_given_a_positive_integer_budget(self):
        for bad in (0, -1, 2.5, True, None):
            with self.subTest(budget=bad):
                with self.assertRaises(HarnessHalt):
                    _drive(_Fakes(_flat), budget=bad)


class DivergenceTests(unittest.TestCase):
    """GAP-60-06: a skipped step ends Adam at the last finite state. No reading is invented."""

    @classmethod
    def setUpClass(cls):
        cls.scorecard = load_scorecard()

    def _diverge(self, reason, step, energy=_flat):
        fakes = _Fakes(energy, skip_at=step, skip_reason=reason)
        with mock.patch.object(learnability_run, "budget_outcome", wraps=budget_outcome) as spy:
            result = _drive(fakes)
        return fakes, result, spy

    def test_a_non_finite_loss_at_step_7_stops_after_six_steps_without_calling_the_rule(self):
        fakes, result, spy = self._diverge("non_finite_loss", 7)
        self.assertEqual(result["outcome"], "diverged")
        self.assertEqual(result["diverged_at_step"], 7)
        self.assertEqual(result["diverged_by"], "non_finite_loss")
        self.assertEqual(result["steps_taken"], 6)
        self.assertEqual(fakes.steps, [1, 2, 3, 4, 5, 6])
        self.assertEqual(spy.call_count, 0)
        self.assertEqual(result["reading_steps"], [0, 5])
        self.assertEqual(fakes.reads, [0, 5])
        self.assertEqual(fakes.extensions, 0)
        self.assertIsNone(result["rate_per_step"])

    def test_a_non_finite_clip_outcome_at_step_3_behaves_the_same(self):
        fakes, result, spy = self._diverge("non_finite_clip_outcome", 3)
        self.assertEqual(result["outcome"], "diverged")
        self.assertEqual((result["diverged_at_step"], result["steps_taken"]), (3, 2))
        self.assertEqual(result["diverged_by"], "non_finite_clip_outcome")
        self.assertEqual(spy.call_count, 0)
        self.assertEqual(result["reading_steps"], [0])

    def test_a_divergence_after_the_extension_keeps_the_one_call_made_at_b(self):
        fakes, result, spy = self._diverge("non_finite_loss", 130, _still_falling_then_flat)
        self.assertEqual(result["outcome"], "diverged")
        self.assertEqual(result["diverged_at_step"], 130)
        self.assertTrue(result["extended"])
        self.assertEqual(result["new_budget_steps"], 2 * BUDGET)
        self.assertEqual(spy.call_count, 1)
        self.assertEqual(fakes.extensions, 1)
        self.assertEqual(result["reading_steps"][-1], 125)

    def test_the_skipped_step_still_counts_in_the_adam_wall_time(self):
        fakes, result, _spy = self._diverge("non_finite_loss", 7)
        self.assertEqual(result["adam_seconds"], 7 * 1.0 + 2 * 0.25)


class _FixtureCase(unittest.TestCase):
    def setUp(self):
        stack = ExitStack()
        self.addCleanup(stack.close)
        self.fixture = stack.enter_context(gold_corpus_fixture())
        self.root = Path(stack.enter_context(tempfile.TemporaryDirectory(prefix="phase60-driver-")))
        self.scorecard = load_scorecard()
        self.spec, self.context = _spec_and_context(self.fixture)
        self.arm_dir = arm_evidence_dir(self.spec.arm_id, evidence_root=self.root)

    def run_fixture(self, *, budget=6, spec=None, **options):
        return run_arm(
            self.spec if spec is None else spec, context=self.context, scorecard=self.scorecard,
            runtime=FIXTURE_RUNTIME, evidence_root=self.root, fixture_budget_steps=budget,
            fixture_timing_steps=50, **options,
        )


class OwnerStopTests(_FixtureCase):
    """T-60-11: an undeterminable improvement rate reaches the owner. Nothing catches it and retries."""

    def _zero_error_scorer(self):
        real = learnability_run.score_network

        def scorer(*args, **kwargs):
            return dataclasses.replace(real(*args, **kwargs), E=0.0)

        return mock.patch.object(learnability_run, "score_network", scorer)

    def test_the_frozen_stop_from_a_real_run_writes_the_stop_record_and_re_raises(self):
        with self._zero_error_scorer():
            with self.assertRaises(OwnerRouted) as caught:
                self.run_fixture(budget=6)
        self.assertEqual(str(caught.exception), FROZEN_RATE_MESSAGE)
        self.assertEqual(
            sorted(path.name for path in self.arm_dir.iterdir()), ["adam.weights", "owner-stop.json"]
        )
        stop = json.loads((self.arm_dir / "owner-stop.json").read_bytes())
        self.assertEqual(stop["schema"], "phase60-owner-stop/v1")
        self.assertIs(stop["diagnostic"], True)
        self.assertEqual(stop["stage"], "budget_outcome")
        self.assertEqual(stop["reason"], FROZEN_RATE_MESSAGE)
        details = stop["details"]
        self.assertEqual(details["arm_id"], self.spec.arm_id)
        self.assertEqual(details["budget_steps"], 6)
        self.assertIs(details.get("extended"), True)
        self.assertEqual(details["readings"][0][0], 0)
        self.assertEqual(details["readings"][-1][0], 12)
        self.assertEqual(sorted(details["timing"]), ["seconds_per_step", "steps", "wall_seconds"])
        weights = details["weights"]
        data = (self.arm_dir / "adam.weights").read_bytes()
        self.assertEqual(weights["file"], "adam.weights")
        self.assertEqual(weights["sha256"], hashlib.sha256(data).hexdigest())
        state = torch.load(self.arm_dir / "adam.weights", map_location="cpu", weights_only=True)
        self.assertEqual(weights["tensor_digest"], weights_digest(state))

    def test_the_same_exception_object_comes_back_and_nothing_is_retried(self):
        raised = OwnerRouted(FROZEN_RATE_MESSAGE)
        drive = learnability_run.drive_adam
        timing = learnability_run.timing_run
        with mock.patch.object(learnability_run, "budget_outcome", side_effect=raised) as frozen, \
                mock.patch.object(learnability_run, "drive_adam", wraps=drive) as driven, \
                mock.patch.object(learnability_run, "timing_run", wraps=timing) as timed:
            with self.assertRaises(OwnerRouted) as caught:
                self.run_fixture(budget=4)
        self.assertIs(caught.exception, raised)
        self.assertEqual((frozen.call_count, driven.call_count, timed.call_count), (1, 1, 1))
        self.assertFalse((self.arm_dir / "record.json").exists())
        self.assertFalse((self.arm_dir / "polish.weights").exists())

    def test_a_second_launch_is_refused_because_the_stop_record_exists(self):
        with mock.patch.object(learnability_run, "budget_outcome", side_effect=OwnerRouted("stop")):
            with self.assertRaises(OwnerRouted):
                self.run_fixture(budget=4)
        before = {path.name: path.read_bytes() for path in self.arm_dir.iterdir()}
        with mock.patch.object(torch.optim.Adam, "step") as adam_step, \
                mock.patch.object(torch.optim.LBFGS, "step") as lbfgs_step, \
                mock.patch.object(learnability_run, "load_arm_data") as read, \
                mock.patch.object(learnability_run, "build_arm_network") as build:
            with self.assertRaises(FirstResultExists):
                self.run_fixture(budget=4)
        self.assertEqual((adam_step.call_count, lbfgs_step.call_count), (0, 0))
        self.assertEqual((read.call_count, build.call_count), (0, 0))
        self.assertEqual({path.name: path.read_bytes() for path in self.arm_dir.iterdir()}, before)

    def test_the_stop_record_is_created_once_and_is_canonical_json(self):
        write_owner_stop = _fn(self, "write_owner_stop")
        digest = write_owner_stop(
            self.arm_dir, stage="budget_outcome", reason=FROZEN_RATE_MESSAGE, details={"b": 2, "a": 1}
        )
        raw = (self.arm_dir / "owner-stop.json").read_bytes()
        self.assertEqual(hashlib.sha256(raw).hexdigest(), digest)
        self.assertEqual(
            raw,
            evidence_io.canonical_json_bytes(
                {
                    "schema": "phase60-owner-stop/v1", "diagnostic": True, "stage": "budget_outcome",
                    "reason": FROZEN_RATE_MESSAGE, "details": {"b": 2, "a": 1},
                }
            ),
        )
        with self.assertRaises(FirstResultExists):
            write_owner_stop(self.arm_dir, stage="budget_outcome", reason="again", details={})
        self.assertEqual((self.arm_dir / "owner-stop.json").read_bytes(), raw)
        for bad in ("", None, 3):
            with self.subTest(stage=bad):
                with self.assertRaises(HarnessHalt):
                    write_owner_stop(self.arm_dir, stage=bad, reason="x", details={})

    def test_the_only_handler_for_an_owner_stop_re_raises(self):
        source = inspect.getsource(learnability_run)
        tree = ast.parse(source)
        found = []
        for function in ast.walk(tree):
            if not isinstance(function, ast.FunctionDef):
                continue
            for node in ast.walk(function):
                if isinstance(node, ast.ExceptHandler) and "OwnerRouted" in ast.dump(node.type or ast.Constant(0)):
                    found.append((function.name, node.body[-1]))
        self.assertEqual([name for name, _ in found], ["run_arm"])
        last = found[0][1]
        self.assertIsInstance(last, ast.Raise)
        self.assertIsNone(last.exc)


class DivergenceRunTests(_FixtureCase):
    """GAP-60-06 in a run: Adam stops at the last finite state, which is scored, polished and chosen from."""

    def _nan_loss_at(self, call_number):
        real = learnability_losses.data_huber_loss
        calls = {"count": 0}

        def flaky(*args, **kwargs):
            calls["count"] += 1
            value = real(*args, **kwargs)
            return value * float("nan") if calls["count"] == call_number else value

        return mock.patch.object(learnability_losses, "data_huber_loss", flaky)

    def test_an_injected_non_finite_loss_ends_adam_and_the_polish_and_chooser_still_run(self):
        adam_steps, lbfgs_calls = [], []
        real_adam, real_lbfgs = torch.optim.Adam.step, torch.optim.LBFGS.step

        def counting(optimizer, *args, **kwargs):
            adam_steps.append(1)
            return real_adam(optimizer, *args, **kwargs)

        def lbfgs_spy(optimizer, closure):
            lbfgs_calls.append(1)
            return real_lbfgs(optimizer, closure)

        with self._nan_loss_at(50 + 7), \
                mock.patch.object(torch.optim.Adam, "step", counting), \
                mock.patch.object(torch.optim.LBFGS, "step", lbfgs_spy), \
                mock.patch.object(learnability_run, "budget_outcome", wraps=budget_outcome) as frozen, \
                mock.patch.object(learnability_run, "make_adam", wraps=learnability_run.make_adam) as made:
            record = self.run_fixture(budget=12)
        budget = record["budget"]
        self.assertEqual((budget["outcome"], budget["diverged_at_step"]), ("diverged", 7))
        self.assertEqual(budget["diverged_by"], "non_finite_loss")
        self.assertEqual(len(adam_steps), 50 + 6)
        self.assertEqual(frozen.call_count, 0)
        self.assertEqual(budget["reading_steps"], list(range(7)))
        self.assertIsNone(budget["cadence_ok"])
        self.assertIs(budget["extended"], False)
        self.assertGreaterEqual(len(lbfgs_calls), 1)
        self.assertEqual(made.call_count, 2)  # the timing run and the one arm: no restart
        adam = record["states"]["adam"]["score_gold"]
        polish = record["states"]["polish"]["score_gold"]
        self.assertEqual(adam["E"], budget["readings"][-1][1])
        chosen = better_state(
            {"E": adam["E"], "eps_h": adam["eps_h"]},
            {"E": polish["E"], "eps_h": polish["eps_h"]},
            scorecard=self.scorecard,
        )
        self.assertEqual(record["better_state"], chosen)
        selected = record["states"][chosen]["score_gold"]
        self.assertEqual(record["result"]["tier"], selected["tier"])
        self.assertEqual(record["result"]["E"], selected["E"])
        self.assertEqual(
            sorted(path.name for path in self.arm_dir.iterdir()),
            ["adam.weights", "polish.weights", "record.json"],
        )
        self.assertGreater(record["wall"]["adam_seconds"], 0.0)

    def test_a_diverged_arm_is_a_result_and_is_not_run_again(self):
        with self._nan_loss_at(50 + 3):
            self.run_fixture(budget=8)
        with self.assertRaises(FirstResultExists):
            self.run_fixture(budget=8)

    def test_adam_weights_that_are_not_finite_stop_the_arm_before_any_polish(self):
        real_drive = learnability_run.drive_adam

        def poisoned(**kwargs):
            result = real_drive(**kwargs)
            model = kwargs["step_fn"].__self__.model
            with torch.no_grad():
                next(model.parameters()).fill_(float("nan"))
            return result

        with mock.patch.object(learnability_run, "drive_adam", poisoned), \
                mock.patch.object(torch.optim.LBFGS, "step") as lbfgs:
            with self.assertRaises(HarnessHalt):
                self.run_fixture(budget=4)
        self.assertEqual(lbfgs.call_count, 0)
        self.assertFalse((self.arm_dir / "record.json").exists())
        self.assertFalse((self.arm_dir / "polish.weights").exists())


class TierEdgeTests(_FixtureCase):
    """The tier is the frozen tier_of of the scored E and eps_h. The runner adds no cut of its own."""

    EDGES = (
        (0.1, 0.0, 1),
        (float("nan"), 0.0, 0),
        (0.1, float("nan"), 1),
        (0.10000001, float("nan"), 0),
        (0.01, 1e-5, 3),
        (0.01, 1e-3, 2),
        (0.010000001, 0.0, 1),
    )

    def test_the_frozen_function_gives_the_spec_edges(self):
        for position, energy, expected in self.EDGES:
            with self.subTest(E=position, eps_h=energy):
                self.assertEqual(tier_of(position, energy, scorecard=self.scorecard), expected)

    def test_the_recorded_result_tier_is_the_frozen_tier_of_the_recorded_result(self):
        real = learnability_run.score_network
        for position, energy, expected in self.EDGES:
            with self.subTest(E=position, eps_h=energy):
                def scorer(*args, _p=position, _e=energy, **kwargs):
                    return dataclasses.replace(
                        real(*args, **kwargs), E=_p, eps_h=_e,
                        tier=tier_of(_p, _e, scorecard=self.scorecard),
                    )

                with tempfile.TemporaryDirectory(prefix="phase60-tier-") as root, \
                        mock.patch.object(learnability_run, "score_network", scorer):
                    record = run_arm(
                        self.spec, context=self.context, scorecard=self.scorecard,
                        runtime=FIXTURE_RUNTIME, evidence_root=Path(root),
                        fixture_budget_steps=3, fixture_timing_steps=50,
                    )
                self.assertEqual(record["result"]["tier"], expected)
                self.assertEqual(
                    record["result"]["tier"], tier_of(position, energy, scorecard=self.scorecard)
                )
                self.assertEqual(record["better_state"], "adam")  # a tie keeps Adam


if __name__ == "__main__":
    unittest.main()
