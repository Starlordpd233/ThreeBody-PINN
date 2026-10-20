"""Phase 60 (D-01, D-03, D-04, D-05, GAP-60-03): the ratified Adam schedule, the second cosine,
the warmup helper and the trainer's gradient clipper, as the learnability runner uses them.

Unit classes use a tiny linear model on CPU float64. The run-level classes run fixture
arms (CPU float64, a temporary corpus) with spies on the optimizer, the scheduler and
the clipper. Nothing here is a real Rung 1 result.
"""

from __future__ import annotations

import dataclasses
import tempfile
import unittest
from contextlib import ExitStack
from pathlib import Path
from unittest import mock

import torch

from pinn.constants import PHYS05_LAMBDA_E_MAX, PHYS05_LAMBDA_L_MAX, PHYS05_LAMBDA_PHYS_MAX
from pinn.training.config import OptConfig
from pinn.training.grad_clip import (
    DEFAULT_C_STAGE_TABLE,
    DEFAULT_MEDIAN_FLOOR,
    GradClipOutcome,
    GradClipper,
)
from pinn.verification import learnability_arms, learnability_run
from pinn.verification.feasibility_scorecard import load_scorecard
from pinn.verification.learnability_arms import fixture_arm
from pinn.verification.learnability_data import fixture_context
from pinn.verification.learnability_run import run_arm
from tests.phase60._fixtures import gold_corpus_fixture

FIXTURE_RUNTIME = ("float64", "cpu")
TIMING_STEPS = 50  # the frozen minimum; a fixture arm times this many steps by default


def _fn(test, name):
    """A missing runner function is an assertion failure, not an import error."""
    function = getattr(learnability_run, name, None)
    test.assertIsNotNone(function, f"pinn.verification.learnability_run.{name} is missing")
    return function


def _tiny():
    torch.manual_seed(0)
    return torch.nn.Linear(4, 3, dtype=torch.float64)


def _train_step(model, optimizer):
    optimizer.zero_grad(set_to_none=True)
    loss = model(torch.ones(2, 4, dtype=torch.float64)).pow(2).sum()
    loss.backward()
    optimizer.step()


def _lr(optimizer):
    return optimizer.param_groups[0]["lr"]


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


class _FixtureCase(unittest.TestCase):
    """A fresh fixture corpus per test and a helper that runs one fixture arm in a temporary root."""

    def setUp(self):
        stack = ExitStack()
        self.addCleanup(stack.close)
        self.fixture = stack.enter_context(gold_corpus_fixture())
        self.scorecard = load_scorecard()

    def run_fixture(self, *, budget=6, spec_changes=None, evidence_root=None, **options):
        spec, context = _spec_and_context(self.fixture, **(spec_changes or {}))
        with ExitStack() as stack:
            root = evidence_root
            if root is None:
                root = Path(stack.enter_context(tempfile.TemporaryDirectory(prefix="phase60-schedule-")))
            record = run_arm(
                spec, context=context, scorecard=self.scorecard, runtime=FIXTURE_RUNTIME,
                evidence_root=root, fixture_budget_steps=budget, **options,
            )
        return record


class LearningRateTests(_FixtureCase):
    """D-01, D-04, D-05: LR_k = 1e-3 x 0.7^k from the trainer's own configuration."""

    def test_adam_takes_the_ratified_rate_and_constants_for_each_stage(self):
        make_adam = _fn(self, "make_adam")
        for stage, expected in ((0, 1e-3), (4, 2.401e-4), (6, 1.17649e-4)):
            with self.subTest(stage=stage):
                optimizer = make_adam(_tiny(), stage)
                self.assertIsInstance(optimizer, torch.optim.Adam)
                self.assertAlmostEqual(_lr(optimizer), expected, places=15)
                self.assertEqual(optimizer.defaults["betas"], (0.9, 0.999))
                self.assertEqual(optimizer.defaults["eps"], 1e-8)

    def test_the_rate_comes_from_the_trainers_configuration_not_a_literal(self):
        make_adam = _fn(self, "make_adam")
        with mock.patch.object(OptConfig, "lr_for_stage", return_value=0.123) as rate:
            optimizer = make_adam(_tiny(), 3)
        rate.assert_called_once_with(3)
        self.assertEqual(_lr(optimizer), 0.123)

    def test_the_catalog_gives_every_data_only_arm_stage_zero_and_each_probe_its_own_stage(self):
        catalog = learnability_arms.catalog()
        data_only = [arm_id for arm_id, spec in catalog.items() if spec.loss_arm == "data_only"]
        for prefix in ("r1-", "g2s-", "g2c-", "c-r1u-", "p1-", "c-p1-"):
            self.assertTrue(any(arm_id.startswith(prefix) for arm_id in data_only), prefix)
        for arm_id in data_only:
            with self.subTest(arm_id=arm_id):
                self.assertEqual((catalog[arm_id].lr_stage, catalog[arm_id].clip_stage), (0, 0))
        for arm_id, stage in (
            ("p2b-2279", 4), ("p2b-3418", 6), ("c-p2b-2279", 4), ("c-p2b-3418", 6),
        ):
            with self.subTest(arm_id=arm_id):
                self.assertEqual((catalog[arm_id].lr_stage, catalog[arm_id].clip_stage), (stage, stage))

    def test_a_run_uses_its_arms_stage_for_the_timing_run_and_the_arm(self):
        make_adam = _fn(self, "make_adam")
        starts = []
        real_step = torch.optim.Adam.step

        def recording_step(optimizer, *args, **kwargs):
            starts.append(optimizer.param_groups[0]["lr"])
            return real_step(optimizer, *args, **kwargs)

        with mock.patch.object(torch.optim.Adam, "step", recording_step), \
                mock.patch.object(learnability_run, "make_adam", wraps=make_adam) as spy:
            record = self.run_fixture(budget=4, spec_changes={"lr_stage": 4, "clip_stage": 4})
        self.assertEqual(record["schedule"]["lr_stage"], 4)
        self.assertEqual(record["schedule"]["lr_k"], OptConfig().lr_for_stage(4))
        self.assertEqual([call.args[1] for call in spy.call_args_list], [4, 4])
        self.assertAlmostEqual(starts[0], 2.401e-4, places=15)  # the timing run's first step
        self.assertAlmostEqual(starts[TIMING_STEPS], 2.401e-4, places=15)  # the arm's first step


class CosineTests(unittest.TestCase):
    """D-03: the cosine reaches zero over its length; the extension is a second cosine."""

    def test_the_cosine_runs_from_the_stage_rate_to_exactly_zero(self):
        make_adam, make_cosine = _fn(self, "make_adam"), _fn(self, "make_cosine")
        model = _tiny()
        optimizer = make_adam(model, 0)
        scheduler = make_cosine(optimizer, 10)
        self.assertEqual(_lr(optimizer), 1e-3)
        for step in range(10):
            _train_step(model, optimizer)
            scheduler.step()
            if step == 4:
                self.assertAlmostEqual(_lr(optimizer), 5e-4, places=15)
        self.assertEqual(_lr(optimizer), 0.0)

    def test_the_cosine_length_is_at_least_one_step(self):
        make_adam, make_cosine = _fn(self, "make_adam"), _fn(self, "make_cosine")
        scheduler = make_cosine(make_adam(_tiny(), 0), 0)
        self.assertEqual(scheduler.T_max, 1)

    def test_the_second_cosine_trace_equals_the_first_exactly(self):
        make_adam, make_cosine = _fn(self, "make_adam"), _fn(self, "make_cosine")
        start_second_cosine = _fn(self, "start_second_cosine")
        length = 10
        model = _tiny()
        optimizer = make_adam(model, 0)
        scheduler = make_cosine(optimizer, length)
        trace = []
        for _ in range(length):
            trace.append(_lr(optimizer))
            _train_step(model, optimizer)
            scheduler.step()
        scheduler = start_second_cosine(optimizer, length)
        for _ in range(length):
            trace.append(_lr(optimizer))
            _train_step(model, optimizer)
            scheduler.step()
        self.assertEqual(trace[:length], trace[length:])
        self.assertEqual(max(abs(a - b) for a, b in zip(trace[:length], trace[length:])), 0.0)
        self.assertEqual(trace[length], 1e-3)

    def test_every_parameter_group_goes_back_to_its_own_initial_rate(self):
        start_second_cosine = _fn(self, "start_second_cosine")
        first, second = torch.nn.Parameter(torch.ones(2)), torch.nn.Parameter(torch.ones(2))
        optimizer = torch.optim.Adam([{"params": [first]}, {"params": [second], "lr": 5e-4}], lr=1e-3)
        scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=4)
        for _ in range(4):
            optimizer.step()
            scheduler.step()
        self.assertEqual([group["lr"] for group in optimizer.param_groups], [0.0, 0.0])
        start_second_cosine(optimizer, 4)
        self.assertEqual([group["lr"] for group in optimizer.param_groups], [1e-3, 5e-4])

    def test_the_adam_object_and_its_moments_survive_the_restart(self):
        make_adam, make_cosine = _fn(self, "make_adam"), _fn(self, "make_cosine")
        start_second_cosine = _fn(self, "start_second_cosine")
        model = _tiny()
        optimizer = make_adam(model, 0)
        scheduler = make_cosine(optimizer, 6)
        for _ in range(6):
            _train_step(model, optimizer)
            scheduler.step()
        parameters = list(model.parameters())
        before = {
            id(p): (optimizer.state[p]["exp_avg"], optimizer.state[p]["exp_avg"].clone(),
                    optimizer.state[p]["exp_avg_sq"].clone(), float(optimizer.state[p]["step"]))
            for p in parameters
        }
        with mock.patch("torch.optim.Adam") as rebuilt:
            new_scheduler = start_second_cosine(optimizer, 6)
        self.assertEqual(rebuilt.call_count, 0)
        self.assertIsInstance(new_scheduler, torch.optim.lr_scheduler.CosineAnnealingLR)
        self.assertEqual(new_scheduler.T_max, 6)
        for p in parameters:
            tensor, copy, square, step = before[id(p)]
            self.assertIs(optimizer.state[p]["exp_avg"], tensor)
            self.assertTrue(torch.equal(optimizer.state[p]["exp_avg"], copy))
            self.assertTrue(torch.equal(optimizer.state[p]["exp_avg_sq"], square))
            self.assertEqual(float(optimizer.state[p]["step"]), step)

    def test_continuing_the_first_scheduler_past_its_length_is_not_a_second_cosine(self):
        make_adam, make_cosine = _fn(self, "make_adam"), _fn(self, "make_cosine")
        start_second_cosine = _fn(self, "start_second_cosine")
        length = 8

        def tail(restart):
            model = _tiny()
            optimizer = make_adam(model, 0)
            scheduler = make_cosine(optimizer, length)
            for _ in range(length):
                _train_step(model, optimizer)
                scheduler.step()
            if restart:
                scheduler = start_second_cosine(optimizer, length)
            trace = []
            for _ in range(length):
                trace.append(_lr(optimizer))
                _train_step(model, optimizer)
                scheduler.step()
            return trace

        continued, restarted = tail(False), tail(True)
        self.assertEqual(continued[0], 0.0)
        self.assertEqual(restarted[0], 1e-3)
        self.assertNotEqual(continued, restarted)


class WarmupTests(unittest.TestCase):
    """D-01: the PHYS-05 warmup is min(2000, floor(0.1 B)) and is not repeated on the extension."""

    def test_the_warmup_length_is_the_smaller_of_2000_and_a_tenth_of_the_budget(self):
        make_scheduled_weights = _fn(self, "make_scheduled_weights")
        for budget, expected in ((860, 86), (30000, 2000), (20000, 2000), (19999, 1999), (10, 1), (9, 0)):
            with self.subTest(budget=budget):
                weights = make_scheduled_weights(budget, 0)
                self.assertEqual(weights.warmup_length, expected)
                self.assertEqual(weights.n_adam_k, budget)

    def test_the_ramp_reaches_its_maximum_at_the_end_of_the_warmup_and_is_not_repeated(self):
        make_scheduled_weights = _fn(self, "make_scheduled_weights")
        weights = make_scheduled_weights(860, 0)
        self.assertEqual(weights.current(0).lambda_phys, 0.0)
        self.assertEqual(weights.current(43).lambda_phys, 0.5)
        self.assertEqual(weights.current(86).lambda_phys, 1.0)
        for epoch in (860, 861, 1000, 1719):  # B, past B, and 2B - 1 on the extension
            with self.subTest(epoch=epoch):
                self.assertEqual(weights.current(epoch).lambda_phys, 1.0)

    def test_the_stage_maxima_are_the_phys05_table_entries(self):
        make_scheduled_weights = _fn(self, "make_scheduled_weights")
        for stage, energy in ((0, 0.0), (4, 1.0), (6, 1.0)):
            with self.subTest(stage=stage):
                current = make_scheduled_weights(860, stage).current(860)
                self.assertEqual(current.lambda_phys, PHYS05_LAMBDA_PHYS_MAX[stage])
                self.assertEqual(current.lambda_e, PHYS05_LAMBDA_E_MAX[stage])
                self.assertEqual(current.lambda_l, PHYS05_LAMBDA_L_MAX[stage])
                self.assertEqual((current.lambda_e, current.lambda_l), (energy, energy))
                self.assertEqual((current.lambda_data, current.lambda_ic), (1.0, 1.0))


class ClipperTests(_FixtureCase):
    """GAP-60-03: the trainer's clipper on every Adam step, at the arm's stage, never in the polish."""

    def _spied_run(self, **options):
        _fn(self, "make_clipper")
        real_clip = GradClipper.clip
        real_lbfgs = torch.optim.LBFGS.step
        marker = {}

        def lbfgs_step(optimizer, closure):
            marker.setdefault("clip_calls_at_polish_start", clip_spy.call_count)
            return real_lbfgs(optimizer, closure)

        with mock.patch.object(GradClipper, "clip", autospec=True, side_effect=real_clip) as clip_spy, \
                mock.patch.object(torch.optim.LBFGS, "step", lbfgs_step):
            record = self.run_fixture(**options)
        return record, clip_spy, marker

    def test_the_clipper_has_the_trainers_stage_table_and_median_floor(self):
        make_clipper = _fn(self, "make_clipper")
        clipper = make_clipper()
        self.assertIsInstance(clipper, GradClipper)
        state = clipper.state_dict()
        self.assertEqual(state["c_stage_table"], DEFAULT_C_STAGE_TABLE)
        self.assertEqual(state["median_floor"], DEFAULT_MEDIAN_FLOOR)
        self.assertEqual((DEFAULT_C_STAGE_TABLE[0], DEFAULT_C_STAGE_TABLE[4], DEFAULT_C_STAGE_TABLE[6]), (8.5, 3.0, 3.0))
        self.assertEqual(DEFAULT_MEDIAN_FLOOR, 1e-6)

    def test_one_clip_per_adam_step_at_the_arms_stage_and_none_during_the_polish(self):
        record, clip_spy, marker = self._spied_run(budget=6)
        budget = record["budget"]
        steps = budget["new_budget_steps"] if budget["extended"] else budget["budget_steps"]
        self.assertEqual(marker["clip_calls_at_polish_start"], TIMING_STEPS + steps)
        self.assertEqual(clip_spy.call_count, TIMING_STEPS + steps)
        self.assertEqual({call.kwargs["stage"] for call in clip_spy.call_args_list}, {0})

    def test_the_stage_follows_the_arms_clip_stage(self):
        for stage, multiplier in ((4, 3.0), (6, 3.0)):
            with self.subTest(stage=stage):
                record, clip_spy, _marker = self._spied_run(
                    budget=3, spec_changes={"lr_stage": stage, "clip_stage": stage}
                )
                self.assertEqual({call.kwargs["stage"] for call in clip_spy.call_args_list}, {stage})
                self.assertEqual(record["clip"]["stage"], stage)
                self.assertEqual(record["clip"]["multiplier"], multiplier)

    def test_the_record_holds_the_stage_multiplier_floor_flag_and_count(self):
        record, _clip_spy, _marker = self._spied_run(budget=6)
        clip = record["clip"]
        self.assertEqual(sorted(clip), ["clipped_steps", "enabled", "median_floor", "multiplier", "stage"])
        self.assertEqual((clip["stage"], clip["multiplier"], clip["median_floor"]), (0, 8.5, 1e-6))
        self.assertIs(clip["enabled"], True)
        self.assertIsInstance(clip["clipped_steps"], int)
        budget = record["budget"]
        steps = budget["new_budget_steps"] if budget["extended"] else budget["budget_steps"]
        self.assertTrue(0 <= clip["clipped_steps"] <= steps)

    def test_a_veto_turns_the_clipper_off_for_the_timing_run_and_the_arm(self):
        record, clip_spy, _marker = self._spied_run(budget=4, clip_enabled=False)
        self.assertEqual(clip_spy.call_count, 0)
        self.assertEqual(record["clip"]["enabled"], False)
        self.assertEqual(record["clip"]["clipped_steps"], 0)
        self.assertEqual((record["clip"]["stage"], record["clip"]["multiplier"]), (0, 8.5))

    def test_a_step_is_clipped_only_when_its_norm_is_above_the_clip_value(self):
        _fn(self, "make_clipper")
        for norm, clipped in ((2.0, True), (1.0, False), (0.5, False)):
            with self.subTest(norm=norm):
                outcome = GradClipOutcome(
                    non_finite=False, clip_value=1.0, total_norm=torch.tensor(norm), window_len=1
                )
                with mock.patch.object(GradClipper, "clip", autospec=True, return_value=outcome):
                    record = self.run_fixture(budget=3)
                budget = record["budget"]
                steps = budget["new_budget_steps"] if budget["extended"] else budget["budget_steps"]
                # The timing run's own steps are not counted: only the arm's.
                self.assertEqual(record["clip"]["clipped_steps"], steps if clipped else 0)

    def test_each_run_gets_a_fresh_clipper_for_the_timing_run_and_for_the_arm(self):
        make_clipper = _fn(self, "make_clipper")
        created = []

        def recording_make_clipper():
            clipper = make_clipper()
            created.append(clipper)
            return clipper

        with mock.patch.object(learnability_run, "make_clipper", recording_make_clipper):
            self.run_fixture(budget=3)
        self.assertEqual(len(created), 2)
        self.assertIsNot(created[0], created[1])


class StepGuardTests(_FixtureCase):
    """GAP-60-06: the loss and the clip outcome are checked before optimizer.step()."""

    def _run_counting_adam_steps(self, *, loss_wrapper=None, clip_side_effect=None, **options):
        real_adam = torch.optim.Adam.step
        adam_steps = []

        def counting_step(optimizer, *args, **kwargs):
            adam_steps.append(1)
            return real_adam(optimizer, *args, **kwargs)

        patches = [mock.patch.object(torch.optim.Adam, "step", counting_step)]
        if loss_wrapper is not None:
            patches.append(mock.patch.object(learnability_run, "data_only_loss", loss_wrapper))
        if clip_side_effect is not None:
            patches.append(
                mock.patch.object(GradClipper, "clip", autospec=True, side_effect=clip_side_effect)
            )
        with ExitStack() as stack:
            for patch in patches:
                stack.enter_context(patch)
            record = self.run_fixture(**options)
        return record, len(adam_steps)

    def test_a_non_finite_clip_outcome_skips_the_step_and_ends_adam_at_the_last_finite_state(self):
        _fn(self, "make_clipper")
        real_clip = GradClipper.clip
        calls = {"count": 0}

        def clip(clipper, params, *, stage):
            calls["count"] += 1
            if calls["count"] == TIMING_STEPS + 3:  # the third step of the arm
                return GradClipOutcome(
                    non_finite=True, clip_value=None, total_norm=torch.tensor(float("nan")),
                    window_len=0,
                )
            return real_clip(clipper, params, stage=stage)

        record, adam_steps = self._run_counting_adam_steps(clip_side_effect=clip, budget=10)
        self.assertEqual(adam_steps, TIMING_STEPS + 2)
        budget = record["budget"]
        self.assertEqual((budget["outcome"], budget["diverged_at_step"]), ("diverged", 3))
        self.assertEqual(budget["diverged_by"], "non_finite_clip_outcome")

    def test_a_finite_loss_with_a_non_finite_gradient_is_a_non_finite_clip_outcome(self):
        _fn(self, "make_clipper")
        real_loss = learnability_run.data_only_loss
        calls = {"count": 0}

        class NanGradient(torch.autograd.Function):
            @staticmethod
            def forward(ctx, value):
                return value.clone()

            @staticmethod
            def backward(ctx, grad):
                return grad * float("nan")

        def loss(*args, **kwargs):
            calls["count"] += 1
            value = real_loss(*args, **kwargs)
            return NanGradient.apply(value) if calls["count"] == TIMING_STEPS + 2 else value

        record, adam_steps = self._run_counting_adam_steps(loss_wrapper=loss, budget=10)
        self.assertEqual(adam_steps, TIMING_STEPS + 1)
        self.assertEqual(record["budget"]["diverged_at_step"], 2)
        self.assertEqual(record["budget"]["diverged_by"], "non_finite_clip_outcome")

    def test_with_the_clipper_off_a_non_finite_gradient_still_skips_the_step(self):
        _fn(self, "make_clipper")
        real_loss = learnability_run.data_only_loss
        calls = {"count": 0}

        class NanGradient(torch.autograd.Function):
            @staticmethod
            def forward(ctx, value):
                return value.clone()

            @staticmethod
            def backward(ctx, grad):
                return grad * float("nan")

        def loss(*args, **kwargs):
            calls["count"] += 1
            value = real_loss(*args, **kwargs)
            return NanGradient.apply(value) if calls["count"] == TIMING_STEPS + 2 else value

        record, adam_steps = self._run_counting_adam_steps(
            loss_wrapper=loss, budget=10, clip_enabled=False
        )
        self.assertEqual(adam_steps, TIMING_STEPS + 1)
        self.assertEqual(record["budget"]["diverged_at_step"], 2)
        self.assertEqual(record["budget"]["diverged_by"], "non_finite_gradient")

    def test_a_non_finite_loss_skips_the_step_before_the_gradient_is_considered(self):
        _fn(self, "make_clipper")
        real_loss = learnability_run.data_only_loss
        calls = {"count": 0}

        def loss(*args, **kwargs):
            calls["count"] += 1
            value = real_loss(*args, **kwargs)
            return value * float("nan") if calls["count"] == TIMING_STEPS + 4 else value

        record, adam_steps = self._run_counting_adam_steps(loss_wrapper=loss, budget=10)
        self.assertEqual(adam_steps, TIMING_STEPS + 3)
        budget = record["budget"]
        self.assertEqual((budget["outcome"], budget["diverged_at_step"]), ("diverged", 4))
        self.assertEqual(budget["diverged_by"], "non_finite_loss")

    def test_the_state_adam_ended_in_is_scored_even_when_no_reading_covered_it(self):
        # A budget of 40 reads every 2 steps. A skip at step 6 leaves the state after step 5,
        # which no reading covers (the last one was at step 4).
        _fn(self, "make_clipper")
        real_loss = learnability_run.data_only_loss
        calls = {"count": 0}

        def loss(*args, **kwargs):
            calls["count"] += 1
            value = real_loss(*args, **kwargs)
            return value * float("nan") if calls["count"] == TIMING_STEPS + 6 else value

        with tempfile.TemporaryDirectory(prefix="phase60-unread-") as root:
            record, adam_steps = self._run_counting_adam_steps(
                loss_wrapper=loss, budget=40, evidence_root=Path(root)
            )
            spec, context = _spec_and_context(self.fixture)
            arm_dir = learnability_arms.arm_evidence_dir(spec.arm_id, evidence_root=Path(root))
            state = torch.load(arm_dir / "adam.weights", map_location="cpu", weights_only=True)
        self.assertEqual(adam_steps, TIMING_STEPS + 5)
        budget = record["budget"]
        self.assertEqual(budget["diverged_at_step"], 6)
        self.assertEqual(budget["reading_steps"], [0, 2, 4])
        data = learnability_run.load_arm_data(
            spec, context, scorecard=self.scorecard, dtype=torch.float64, device=torch.device("cpu")
        )
        model = learnability_run.build_arm_network(30.0, dtype=torch.float64, device=torch.device("cpu"))
        model.load_state_dict(state)
        rescored = learnability_run._score(
            model, data, data.score, scorecard=self.scorecard, dtype=torch.float64,
            device=torch.device("cpu"),
        )
        adam_score = record["states"]["adam"]["score_gold"]
        self.assertEqual(adam_score["E"], rescored.to_json_dict()["E"])
        self.assertNotEqual(adam_score["E"], budget["readings"][-1][1])
        self.assertEqual(budget["readings"][-1][0], 4)


class ExtensionRunTests(_FixtureCase):
    """D-03 in a run: the frozen rule grants the extension, and the arm runs a second cosine."""

    def test_the_extension_is_a_second_cosine_on_the_same_optimizer_with_moments_kept(self):
        _fn(self, "start_second_cosine")
        budget = 6
        seen = []
        real_step = torch.optim.Adam.step

        def recording_step(optimizer, *args, **kwargs):
            first_state = next(iter(optimizer.state.values()), None)
            seen.append(
                {
                    "optimizer": id(optimizer),
                    "lr": optimizer.param_groups[0]["lr"],
                    "moment": None if first_state is None else id(first_state["exp_avg"]),
                    "count": 0 if first_state is None else int(first_state["step"]),
                }
            )
            return real_step(optimizer, *args, **kwargs)

        script = [
            {"outcome": "extend", "new_budget_steps": 2 * budget},
            {"outcome": "complete"},
        ]
        scheduler_spy = mock.Mock(wraps=torch.optim.lr_scheduler.CosineAnnealingLR)
        with mock.patch.object(torch.optim.Adam, "step", recording_step), \
                mock.patch.object(learnability_run, "budget_outcome", side_effect=script) as frozen, \
                mock.patch("torch.optim.lr_scheduler.CosineAnnealingLR", scheduler_spy):
            record = self.run_fixture(budget=budget)
        arm = seen[TIMING_STEPS:]
        self.assertEqual(len(arm), 2 * budget)
        learning_rates = [entry["lr"] for entry in arm]
        self.assertEqual(learning_rates[:budget], learning_rates[budget:])
        self.assertEqual(learning_rates[0], OptConfig().lr_for_stage(0))
        self.assertEqual(len({entry["optimizer"] for entry in arm}), 1)
        self.assertEqual({entry["moment"] for entry in arm[1:]}, {arm[1]["moment"]})
        self.assertEqual([entry["count"] for entry in arm], list(range(2 * budget)))
        self.assertEqual(
            [call.kwargs["T_max"] for call in scheduler_spy.call_args_list],
            [TIMING_STEPS, budget, budget],
        )
        self.assertEqual(record["schedule"]["cosines"], 2)
        self.assertEqual(record["schedule"]["cosine_t_max"], budget)
        self.assertEqual([call.args[1] for call in frozen.call_args_list], [budget, 2 * budget])
        self.assertEqual([call.kwargs["extended"] for call in frozen.call_args_list], [False, True])
        self.assertEqual(record["budget"]["reading_steps"][-1], 2 * budget)


class TimingParityTests(_FixtureCase):
    """GAP-60-04: the timing run is the arm's own configuration, and the arm does not inherit from it."""

    def test_the_timing_run_and_the_arm_share_record_loss_frequency_and_stage(self):
        _fn(self, "make_adam")
        points = []
        real_loss = learnability_run.data_only_loss

        def spying_loss(model, data_points, *, dtype, device):
            points.append(data_points)
            return real_loss(model, data_points, dtype=dtype, device=device)

        with mock.patch.object(learnability_run, "data_only_loss", spying_loss), \
                mock.patch.object(
                    learnability_run, "build_arm_network", wraps=learnability_run.build_arm_network
                ) as build, \
                mock.patch.object(learnability_run, "make_adam", wraps=learnability_run.make_adam) as adam:
            record = self.run_fixture(budget=3, spec_changes={"lr_stage": 4, "clip_stage": 4})
        self.assertEqual(len(build.call_args_list), 2)
        self.assertEqual(build.call_args_list[0], build.call_args_list[1])
        self.assertEqual(build.call_args_list[0].args, (30.0,))
        self.assertEqual(adam.call_args_list[0].args[1], adam.call_args_list[1].args[1])
        timing_steps = record["timing"]["steps"]
        self.assertTrue(all(item is points[0] for item in points))
        self.assertGreaterEqual(len(points), timing_steps + 3)


if __name__ == "__main__":
    unittest.main()
