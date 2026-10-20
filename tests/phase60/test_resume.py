"""Phase 60 (SPEC Requirement 8, INST-05): a governed stop resumes exactly, or is refused.

Every class here runs fixture arms on CPU float64 under a temporary root. Nothing is a
Rung 1 result, no real corpus is opened and nothing is written into the repository: the
run tree of a direct ``run_arm`` call sits beside its own evidence root.

``SignalSubprocessTests`` is the only place a real signal is delivered; it runs a small
script in a child process, slows the arm's steps so the signal lands mid-run, and checks
that the child exits 129, 130 or 143 with a checkpoint and a stop marker on disk.
"""

from __future__ import annotations

import dataclasses
import json
import os
import shutil
import signal
import subprocess
import sys
import tempfile
import textwrap
import time
import unittest
from contextlib import ExitStack
from pathlib import Path
from unittest import mock

import numpy as np
import torch

from pinn.verification import learnability_run
from pinn.verification.feasibility_scorecard import load_scorecard
from pinn.verification.learnability_arms import fixture_arm
from pinn.verification.learnability_data import fixture_context
from pinn.verification.learnability_run import (
    ClaimExists,
    GovernedStop,
    ResumeRefused,
    load_resume_checkpoint,
    request_stop,
    run_arm,
)
from tests.phase60._fixtures import gold_corpus_fixture

FIXTURE_RUNTIME = ("float64", "cpu")
BUDGET = 6
TIMING = 50
REPO_ROOT = Path(__file__).resolve().parents[2]
ARM_ID = "fixture-hierarchical-gold-0"
# The trainer's own wording for a polish checkpoint that lost its frozen segment.
SEGMENT_WORDING = (
    "resume checkpoint is missing active L-BFGS segment state; refusing to redraw "
    "samples or causal weights"
)


class _Clock:
    """A counter clock: every read costs one second, so a summed wall time is countable."""

    def __init__(self):
        self.now = 0.0

    def __call__(self):
        self.now += 1.0
        return self.now


def _fixture_arm(fixture, **changes):
    spec = fixture_arm(
        train_key=fixture.gold_key, score_key=fixture.gold_key, beside_key=fixture.base_key
    )
    return dataclasses.replace(spec, **changes) if changes else spec


def _fixture_context(fixture):
    return fixture_context(
        allowlist=fixture.allowlist, reader=fixture.reader, stats=fixture.stats
    )


def _run_tree(evidence_root):
    """The ignored run tree a direct ``run_arm`` call defaults to."""
    return Path(evidence_root) / "runs" / "phase60" / ARM_ID


def _stepper_hook(*, ordinal=2, stop_at=None, signum=signal.SIGINT, lr_sink=None):
    """A drop-in ``_build_stepper`` that observes the run's ``ordinal``-th stepper.

    The timing run builds the first stepper and the arm the second on a fresh run; a
    resumed run builds the arm's first. The hook records the learning rate after every
    step and can request a governed stop after step ``stop_at``.
    """
    real_build = learnability_run._build_stepper
    built = []
    stopped = []

    def build(*args, **kwargs):
        stepper = real_build(*args, **kwargs)
        built.append(stepper)
        if len(built) != ordinal:
            return stepper
        real_step = stepper.step

        def step(number):
            result = real_step(number)
            if lr_sink is not None:
                lr_sink.append(float(stepper.scheduler.get_last_lr()[0]))
            if stop_at is not None and number == stop_at and not stopped:
                stopped.append(number)
                request_stop(signum)
            return result

        stepper.step = step
        return stepper

    return build


def _recording_draw(sink):
    """A drop-in ``draw_collocation_times`` that keeps each ``(generator, times)`` pair."""
    real = learnability_run.draw_collocation_times

    def draw(*args, **kwargs):
        times = real(*args, **kwargs)
        sink.append((args[1], np.array(times, dtype=np.float64, copy=True)))
        return times

    return draw


def _draw_groups(draws):
    """Draws grouped by generator, in first-use order: the timing run's then the arm's."""
    groups = {}
    for rng, times in draws:
        groups.setdefault(id(rng), []).append(times)
    return list(groups.values())


def _comparable(record):
    """The parts of two records that a resume must leave identical (SPEC Requirement 8)."""
    return {
        "readings": record["budget"]["readings"],
        "reading_steps": record["budget"]["reading_steps"],
        "outcome": record["budget"]["outcome"],
        "extended": record["budget"]["extended"],
        "budget_steps": record["budget"]["budget_steps"],
        "new_budget_steps": record["budget"]["new_budget_steps"],
        "trace_E": [entry["E"] for entry in record["trace"]],
        "trace_steps": [entry["step"] for entry in record["trace"]],
        "adam_digest": record["states"]["adam"]["weights"]["tensor_digest"],
        "polish_digest": record["states"]["polish"]["weights"]["tensor_digest"],
        "adam_file": record["states"]["adam"]["weights"]["sha256"],
        "polish_file": record["states"]["polish"]["weights"]["sha256"],
        "result": record["result"],
        "better_state": record["better_state"],
    }


class ExactContinuationTests(unittest.TestCase):
    """Stopped at Adam step 5, resumed, and finished with the uninterrupted numbers."""

    @classmethod
    def setUpClass(cls):
        stack = ExitStack()
        cls.addClassCleanup(stack.close)
        cls.fixture = stack.enter_context(gold_corpus_fixture())
        cls.root = Path(stack.enter_context(tempfile.TemporaryDirectory(prefix="phase60-exact-")))
        cls.scorecard = load_scorecard()
        cls.context = _fixture_context(cls.fixture)
        cls.spec = _fixture_arm(cls.fixture)

        cls.clock = _Clock()
        cls.plain = cls._run("plain", clock=cls.clock)

        cls.stop_clock = _Clock()
        learnability_run._reset_stop()
        with mock.patch.object(
            learnability_run, "_build_stepper",
            _stepper_hook(stop_at=5, signum=signal.SIGINT),
        ):
            try:
                cls._run("stopped", clock=cls.stop_clock)
            except GovernedStop as stop:
                cls.stop = stop
            else:  # pragma: no cover - a stop that never stopped
                raise AssertionError("the governed stop was not raised")
        cls.tree = _run_tree(cls.root / "stopped")
        cls.checkpoint = torch.load(
            cls.tree / "resume.pt", map_location="cpu", weights_only=True
        )

        cls.timing_calls = []

        def forbidden(*args, **kwargs):
            cls.timing_calls.append(1)
            raise AssertionError("a resume must not run the timing run")

        learnability_run._reset_stop()
        with mock.patch.object(learnability_run, "timing_run", forbidden):
            cls.resumed = cls._run("stopped", resume=True, clock=cls.stop_clock)

    @classmethod
    def _run(cls, name, *, resume=False, clock=None):
        return run_arm(
            cls.spec,
            context=cls.context,
            scorecard=cls.scorecard,
            runtime=FIXTURE_RUNTIME,
            evidence_root=cls.root / name,
            fixture_budget_steps=BUDGET,
            fixture_timing_steps=TIMING,
            resume=resume,
            clock=clock,
        )

    def test_the_stop_writes_a_checkpoint_and_one_marker_and_carries_exit_130(self):
        self.assertEqual(self.stop.exit_code, 130)
        self.assertEqual(self.stop.phase, "adam")
        self.assertEqual(self.stop.step, 5)
        self.assertTrue((self.tree / "resume.pt").is_file())
        self.assertEqual(sorted(path.name for path in self.tree.glob("stop-*.json")), ["stop-1.json"])
        marker = json.loads((self.tree / "stop-1.json").read_bytes())
        self.assertEqual(marker["signal"], "SIGINT")
        self.assertEqual(marker["exit_code"], 130)
        self.assertEqual(marker["phase"], "adam")
        self.assertEqual(marker["step"], 5)
        self.assertEqual(list(self.tree.rglob("*.tmp*")), [])

    def test_the_checkpoint_holds_the_driver_the_budget_and_the_reason_for_the_stop(self):
        self.assertEqual(self.checkpoint["schema"], "phase60-resume/v1")
        self.assertEqual(self.checkpoint["phase"], "adam")
        self.assertEqual(self.checkpoint["budget_steps"], BUDGET)
        self.assertEqual(self.checkpoint["driver"]["budget_steps"], BUDGET)
        self.assertEqual(self.checkpoint["driver"]["stopped_at_step"], 5)
        self.assertIs(self.checkpoint["adam_complete"], False)
        self.assertEqual(self.checkpoint["stops"][0]["phase"], "adam")
        self.assertIsNotNone(self.checkpoint["model"])
        self.assertIsNotNone(self.checkpoint["optimizer"])
        self.assertIsNotNone(self.checkpoint["scheduler"])
        self.assertIsNotNone(self.checkpoint["rng"])
        self.assertEqual(self.checkpoint["protocol_sha256"], None)

    def test_the_resume_does_not_call_the_timing_run_and_does_not_retime_the_budget(self):
        self.assertEqual(self.timing_calls, [])
        self.assertEqual(self.resumed["budget"]["budget_steps"], BUDGET)
        self.assertEqual(self.resumed["timing_runs"], 1)
        self.assertEqual(self.resumed["launch"]["invocations"], 2)
        self.assertEqual(
            [entry["signal"] for entry in self.resumed["launch"]["stops"]], ["SIGINT"]
        )

    def test_the_resumed_record_matches_the_uninterrupted_one_field_for_field(self):
        self.assertEqual(_comparable(self.resumed), _comparable(self.plain))

    def test_the_recorded_adam_seconds_are_the_sum_of_the_two_segments(self):
        self.assertEqual(self.resumed["wall"]["adam_seconds"], self.plain["wall"]["adam_seconds"])
        self.assertGreater(self.checkpoint["driver"]["adam_seconds"], 0.0)
        self.assertLess(
            self.checkpoint["driver"]["adam_seconds"], self.plain["wall"]["adam_seconds"]
        )

    def test_the_trace_covers_every_reading_once(self):
        steps = [entry["step"] for entry in self.resumed["trace"]]
        self.assertEqual(steps, list(range(BUDGET + 1)))
        self.assertEqual(len(steps), len(set(steps)))


def _extend_once():
    """The frozen budget outcome with the one extension forced: extend, then complete."""
    def outcome(readings, budget, *, extended, scorecard):
        if not extended:
            return {"outcome": "extend", "new_budget_steps": 2 * budget}
        return {"outcome": "complete"}

    return outcome


class ExtensionResumeTests(unittest.TestCase):
    """A stop exactly at step B resumes into the same extension decision."""

    @classmethod
    def setUpClass(cls):
        stack = ExitStack()
        cls.addClassCleanup(stack.close)
        cls.fixture = stack.enter_context(gold_corpus_fixture())
        cls.root = Path(stack.enter_context(tempfile.TemporaryDirectory(prefix="phase60-extend-")))
        cls.scorecard = load_scorecard()
        cls.context = _fixture_context(cls.fixture)
        cls.spec = _fixture_arm(cls.fixture)
        cls.common = dict(
            context=cls.context, scorecard=cls.scorecard, runtime=FIXTURE_RUNTIME,
            fixture_budget_steps=BUDGET, fixture_timing_steps=TIMING, clock=_Clock(),
        )

    def test_a_stop_at_the_budget_resumes_into_the_extension_with_the_same_lr_trace(self):
        plain_lrs = []
        with mock.patch.object(learnability_run, "budget_outcome", _extend_once()), \
                mock.patch.object(
                    learnability_run, "_build_stepper", _stepper_hook(lr_sink=plain_lrs)
                ):
            plain = run_arm(
                self.spec, evidence_root=self.root / "plain", **self.common
            )
        self.assertTrue(plain["budget"]["extended"])
        self.assertEqual(len(plain_lrs), 2 * BUDGET)

        learnability_run._reset_stop()
        first_lrs = []
        with mock.patch.object(learnability_run, "budget_outcome", _extend_once()), \
                mock.patch.object(
                    learnability_run, "_build_stepper",
                    _stepper_hook(stop_at=BUDGET, lr_sink=first_lrs),
                ):
            with self.assertRaises(GovernedStop) as caught:
                run_arm(self.spec, evidence_root=self.root / "stopped", **self.common)
        self.assertEqual(caught.exception.exit_code, 130)
        self.assertEqual(len(first_lrs), BUDGET)
        checkpoint = torch.load(
            _run_tree(self.root / "stopped") / "resume.pt",
            map_location="cpu", weights_only=True,
        )
        self.assertIs(checkpoint["driver"]["extended"], False)
        self.assertEqual(checkpoint["driver"]["stopped_at_step"], BUDGET)

        learnability_run._reset_stop()
        second_lrs = []
        with mock.patch.object(learnability_run, "budget_outcome", _extend_once()), \
                mock.patch.object(
                    learnability_run, "_build_stepper", _stepper_hook(ordinal=1, lr_sink=second_lrs)
                ):
            resumed = run_arm(
                self.spec, evidence_root=self.root / "stopped", resume=True, **self.common
            )
        self.assertEqual(len(second_lrs), BUDGET)
        self.assertEqual(first_lrs + second_lrs, plain_lrs)
        self.assertTrue(resumed["budget"]["extended"])
        self.assertEqual(resumed["budget"]["new_budget_steps"], 2 * BUDGET)
        self.assertEqual(resumed["schedule"]["cosines"], 2)
        self.assertEqual(_comparable(resumed), _comparable(plain))


class PolishResumeTests(unittest.TestCase):
    """A stop in the second polish outer call restores the state from before that call."""

    @classmethod
    def setUpClass(cls):
        stack = ExitStack()
        cls.addClassCleanup(stack.close)
        cls.fixture = stack.enter_context(gold_corpus_fixture())
        cls.root = Path(stack.enter_context(tempfile.TemporaryDirectory(prefix="phase60-polish-")))
        cls.scorecard = load_scorecard()
        cls.context = _fixture_context(cls.fixture)
        cls.spec = _fixture_arm(cls.fixture)
        cls.clock = _Clock()
        cls.common = dict(
            context=cls.context, scorecard=cls.scorecard, runtime=FIXTURE_RUNTIME,
            fixture_budget_steps=BUDGET, fixture_timing_steps=TIMING, clock=cls.clock,
        )
        cls.plain = run_arm(cls.spec, evidence_root=cls.root / "plain", **cls.common)

        real_step = torch.optim.LBFGS.step
        calls = {"n": 0}

        def step(optimizer, closure):
            calls["n"] += 1
            if calls["n"] == 2:
                request_stop(signal.SIGTERM)
            return real_step(optimizer, closure)

        learnability_run._reset_stop()
        with mock.patch.object(torch.optim.LBFGS, "step", step):
            try:
                run_arm(cls.spec, evidence_root=cls.root / "stopped", **cls.common)
            except GovernedStop as stop:
                cls.stop = stop
            else:  # pragma: no cover - a stop that never stopped
                raise AssertionError("the governed stop was not raised")
        cls.tree = _run_tree(cls.root / "stopped")
        cls.checkpoint = torch.load(
            cls.tree / "resume.pt", map_location="cpu", weights_only=True
        )
        learnability_run._reset_stop()
        cls.resumed = run_arm(
            cls.spec, evidence_root=cls.root / "stopped", resume=True, **cls.common
        )

    def test_the_polish_stop_exits_143_with_a_checkpoint_and_one_marker(self):
        self.assertEqual(self.stop.exit_code, 143)
        self.assertEqual(self.stop.phase, "polish")
        self.assertTrue((self.tree / "resume.pt").is_file())
        self.assertEqual(sorted(path.name for path in self.tree.glob("stop-*.json")), ["stop-1.json"])
        self.assertEqual(list(self.tree.rglob("*.tmp*")), [])
        marker = json.loads((self.tree / "stop-1.json").read_bytes())
        self.assertEqual((marker["signal"], marker["exit_code"]), ("SIGTERM", 143))

    def test_the_checkpoint_carries_the_segment_the_lbfgs_state_and_the_counters(self):
        self.assertEqual(self.checkpoint["phase"], "polish")
        self.assertIsNotNone(self.checkpoint["lbfgs"])
        self.assertIsNotNone(self.checkpoint["segment"])
        self.assertEqual(self.checkpoint["polish"]["outer_calls"], 1)
        self.assertIs(self.checkpoint["adam_complete"], True)
        self.assertIsNotNone(self.checkpoint["adam"])

    def test_the_resume_finishes_identically_and_excludes_the_aborted_call(self):
        self.assertGreaterEqual(self.plain["states"]["polish"]["outer_calls"], 2)
        self.assertEqual(
            self.resumed["states"]["polish"]["outer_calls"],
            self.plain["states"]["polish"]["outer_calls"],
        )
        self.assertEqual(
            [entry["E"] for entry in self.resumed["states"]["polish"]["trace"]],
            [entry["E"] for entry in self.plain["states"]["polish"]["trace"]],
        )
        self.assertEqual(
            self.resumed["states"]["polish"]["weights"]["tensor_digest"],
            self.plain["states"]["polish"]["weights"]["tensor_digest"],
        )
        self.assertEqual(
            self.resumed["wall"]["polish_seconds"], self.plain["wall"]["polish_seconds"]
        )
        self.assertEqual(_comparable(self.resumed), _comparable(self.plain))


class PhysicsResumeTests(unittest.TestCase):
    """A physics arm resumed at an Adam step draws the same collocation rows it would have."""

    def test_the_resumed_steps_draw_exactly_the_uninterrupted_rows(self):
        with ExitStack() as stack:
            fixture = stack.enter_context(gold_corpus_fixture())
            root = Path(stack.enter_context(tempfile.TemporaryDirectory(prefix="phase60-phys-resume-")))
            scorecard = load_scorecard()
            context = _fixture_context(fixture)
            spec = _fixture_arm(fixture, loss_arm="full")
            common = dict(
                context=context, scorecard=scorecard, runtime=FIXTURE_RUNTIME,
                fixture_budget_steps=BUDGET, fixture_timing_steps=TIMING,
                fixture_n_slots=1, fixture_r_ref=1.0, clock=_Clock(),
            )
            plain_draws = []
            with mock.patch.object(
                learnability_run, "draw_collocation_times", _recording_draw(plain_draws)
            ):
                plain = run_arm(spec, evidence_root=root / "plain", **common)

            learnability_run._reset_stop()
            first_draws = []
            with mock.patch.object(
                learnability_run, "draw_collocation_times", _recording_draw(first_draws)
            ), mock.patch.object(
                learnability_run, "_build_stepper",
                _stepper_hook(stop_at=5, signum=signal.SIGTERM),
            ):
                with self.assertRaises(GovernedStop) as caught:
                    run_arm(spec, evidence_root=root / "stopped", **common)
            self.assertEqual(caught.exception.exit_code, 143)

            learnability_run._reset_stop()
            second_draws = []
            with mock.patch.object(
                learnability_run, "draw_collocation_times", _recording_draw(second_draws)
            ):
                resumed = run_arm(
                    spec, evidence_root=root / "stopped", resume=True, **common
                )

        plain_arm = _draw_groups(plain_draws)[1]
        first_arm = _draw_groups(first_draws)[1]
        second_arm = _draw_groups(second_draws)[0]
        # The first draw of a segment is the frozen monitor set (the resumed segment
        # redraws one and then restores the generator) and the last is the handoff.
        self.assertEqual(len(plain_arm), BUDGET + 2)
        self.assertEqual(len(first_arm), 5 + 1)
        self.assertEqual(len(second_arm), (BUDGET - 5) + 2)
        for produced, expected in zip(first_arm[1:] + second_arm[1:-1], plain_arm[1:-1]):
            np.testing.assert_array_equal(produced, expected)
        self.assertEqual(
            resumed["states"]["polish"]["weights"]["tensor_digest"],
            plain["states"]["polish"]["weights"]["tensor_digest"],
        )
        self.assertEqual(_comparable(resumed), _comparable(plain))


class ResumeRefusalTests(unittest.TestCase):
    """Every refusal SPEC Requirement 8 names, including the trainer's segment wording."""

    @classmethod
    def setUpClass(cls):
        stack = ExitStack()
        cls.addClassCleanup(stack.close)
        cls.fixture = stack.enter_context(gold_corpus_fixture())
        cls.root = Path(stack.enter_context(tempfile.TemporaryDirectory(prefix="phase60-refuse-")))
        cls.scorecard = load_scorecard()
        cls.context = _fixture_context(cls.fixture)
        cls.spec = _fixture_arm(cls.fixture)
        real_step = torch.optim.LBFGS.step
        calls = {"n": 0}

        def step(optimizer, closure):
            calls["n"] += 1
            if calls["n"] == 2:
                request_stop(signal.SIGTERM)
            return real_step(optimizer, closure)

        learnability_run._reset_stop()
        with mock.patch.object(torch.optim.LBFGS, "step", step):
            try:
                run_arm(
                    cls.spec, context=cls.context, scorecard=cls.scorecard,
                    runtime=FIXTURE_RUNTIME, evidence_root=cls.root / "stopped",
                    fixture_budget_steps=BUDGET, fixture_timing_steps=TIMING, clock=_Clock(),
                )
            except GovernedStop:
                pass
        cls.tree = _run_tree(cls.root / "stopped")

    def setUp(self):
        learnability_run._reset_stop()
        self.addCleanup(learnability_run._reset_stop)
        self.copy = Path(tempfile.mkdtemp(prefix="case-", dir=str(self.root)))
        self.tree_copy = self.copy / "tree"
        shutil.copytree(self.tree, self.tree_copy)

    def _load(self, **overrides):
        settings = dict(arm_id=ARM_ID, protocol_sha256=None, module_sha256={})
        settings.update(overrides)
        return load_resume_checkpoint(self.tree_copy, **settings)

    def test_the_untouched_checkpoint_loads(self):
        self.assertEqual(self._load()["phase"], "polish")

    def test_a_missing_checkpoint_is_refused(self):
        (self.tree_copy / "resume.pt").unlink()
        with self.assertRaises(ResumeRefused):
            self._load()

    def test_a_missing_stop_marker_is_refused(self):
        for marker in self.tree_copy.glob("stop-*.json"):
            marker.unlink()
        with self.assertRaises(ResumeRefused):
            self._load()

    def test_another_arm_id_is_refused(self):
        with self.assertRaises(ResumeRefused):
            self._load(arm_id="r1-1632")

    def test_a_changed_protocol_digest_is_refused(self):
        with self.assertRaises(ResumeRefused):
            self._load(protocol_sha256="0" * 64)

    def test_a_changed_module_digest_is_refused(self):
        with self.assertRaises(ResumeRefused):
            self._load(module_sha256={"pinn/verification/learnability_run.py": "0" * 64})

    def test_a_polish_checkpoint_without_its_segment_is_refused_with_the_trainer_wording(self):
        payload = self._load()
        payload["segment"] = None
        torch.save(payload, self.tree_copy / "resume.pt")
        with self.assertRaises(ResumeRefused) as caught:
            self._load()
        self.assertEqual(str(caught.exception), SEGMENT_WORDING)

    def test_a_resume_through_run_arm_refuses_a_tampered_segment(self):
        payload = self._load()
        payload["segment"] = None
        torch.save(payload, self.tree_copy / "resume.pt")
        with self.assertRaises(ResumeRefused) as caught:
            run_arm(
                self.spec, context=self.context, scorecard=self.scorecard,
                runtime=FIXTURE_RUNTIME, evidence_root=self.root / "tampered",
                fixture_budget_steps=BUDGET, fixture_timing_steps=TIMING,
                resume=True, run_dir=self.tree_copy, clock=_Clock(),
            )
        self.assertEqual(str(caught.exception), SEGMENT_WORDING)

    def test_a_fresh_run_over_a_claimed_tree_is_refused(self):
        with self.assertRaises(ClaimExists):
            run_arm(
                self.spec, context=self.context, scorecard=self.scorecard,
                runtime=FIXTURE_RUNTIME, evidence_root=self.root / "fresh",
                fixture_budget_steps=BUDGET, fixture_timing_steps=TIMING,
                run_dir=self.tree_copy, clock=_Clock(),
            )


class TimingInterruptTests(unittest.TestCase):
    """A stop during the timing run leaves no budget and the resume repeats it."""

    def test_the_resume_repeats_the_timing_run_and_records_a_second_one(self):
        with ExitStack() as stack:
            fixture = stack.enter_context(gold_corpus_fixture())
            root = Path(stack.enter_context(tempfile.TemporaryDirectory(prefix="phase60-timing-")))
            scorecard = load_scorecard()
            context = _fixture_context(fixture)
            spec = _fixture_arm(fixture)
            common = dict(
                context=context, scorecard=scorecard, runtime=FIXTURE_RUNTIME,
                fixture_budget_steps=BUDGET, fixture_timing_steps=TIMING, clock=_Clock(),
            )
            learnability_run._reset_stop()
            with mock.patch.object(
                learnability_run, "_build_stepper",
                _stepper_hook(ordinal=1, stop_at=3, signum=signal.SIGHUP),
            ):
                with self.assertRaises(GovernedStop) as caught:
                    run_arm(spec, evidence_root=root / "stopped", **common)
            self.assertEqual(caught.exception.exit_code, 129)
            self.assertEqual(caught.exception.phase, "timing")
            tree = _run_tree(root / "stopped")
            checkpoint = torch.load(tree / "resume.pt", map_location="cpu", weights_only=True)
            self.assertEqual(checkpoint["phase"], "timing")
            self.assertIsNone(checkpoint["timing"])
            self.assertEqual(checkpoint["timing_runs"], 1)
            self.assertEqual(list(tree.rglob("*.tmp*")), [])

            learnability_run._reset_stop()
            with mock.patch.object(
                learnability_run, "timing_run", wraps=learnability_run.timing_run
            ) as timed:
                resumed = run_arm(spec, evidence_root=root / "stopped", resume=True, **common)
            self.assertEqual(timed.call_count, 1)
        self.assertEqual(resumed["timing_runs"], 2)
        self.assertEqual(resumed["budget"]["budget_steps"], BUDGET)
        self.assertEqual(resumed["launch"]["invocations"], 2)
        self.assertEqual(resumed["launch"]["stops"][0]["phase"], "timing")
        self.assertEqual(resumed["launch"]["stops"][0]["signal"], "SIGHUP")


# ---------------------------------------------------------------------------
# Real signals in a child process.
# ---------------------------------------------------------------------------

SIGNAL_SCRIPT = textwrap.dedent(
    """
    import sys, time
    from pathlib import Path
    from unittest import mock

    from pinn.verification import learnability_run
    from pinn.verification.feasibility_scorecard import load_scorecard
    from pinn.verification.learnability_arms import fixture_arm
    from pinn.verification.learnability_data import fixture_context
    from tests.phase60._fixtures import gold_corpus_fixture

    root = Path(sys.argv[1])

    with gold_corpus_fixture() as fixture:
        context = fixture_context(
            allowlist=fixture.allowlist, reader=fixture.reader, stats=fixture.stats
        )
        spec = fixture_arm(
            train_key=fixture.gold_key,
            score_key=fixture.gold_key,
            beside_key=fixture.base_key,
        )
        real_build = learnability_run._build_stepper
        built = []

        def build(*args, **kwargs):
            stepper = real_build(*args, **kwargs)
            built.append(stepper)
            if len(built) == 2:
                real_step = stepper.step

                def step(number):
                    print("ARM-STEP", flush=True)
                    time.sleep(0.15)
                    return real_step(number)

                stepper.step = step
            return stepper

        learnability_run.install_stop_handlers()
        try:
            with mock.patch.object(learnability_run, "_build_stepper", build):
                learnability_run.run_arm(
                    spec,
                    context=context,
                    scorecard=load_scorecard(),
                    runtime=("float64", "cpu"),
                    evidence_root=root / "evidence",
                    fixture_budget_steps=40,
                    fixture_timing_steps=50,
                )
        except learnability_run.GovernedStop as stop:
            sys.exit(int(stop.exit_code))
        sys.exit(0)
    """
)


class SignalSubprocessTests(unittest.TestCase):
    """SIGHUP, SIGINT and SIGTERM checkpoint and exit 129, 130 and 143. SIGKILL cannot."""

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="phase60-signal-"))
        self.addCleanup(shutil.rmtree, self.tmp, True)
        self.script = self.tmp / "run_fixture_arm.py"
        self.script.write_text(SIGNAL_SCRIPT, encoding="utf-8")

    def _launch(self):
        environment = dict(os.environ)
        environment["PYTHONPATH"] = str(REPO_ROOT)
        return subprocess.Popen(
            [sys.executable, "-B", str(self.script), str(self.tmp)],
            cwd=str(REPO_ROOT),
            env=environment,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
        )

    def _wait_for_the_arm(self, process):
        deadline = time.monotonic() + 180.0
        while time.monotonic() < deadline:
            line = process.stdout.readline()
            if line == "":
                break
            if line.strip() == "ARM-STEP":
                return
        self.fail("the child never reached an Adam step of the arm")

    def _tree(self):
        return self.tmp / "evidence" / "runs" / "phase60" / ARM_ID

    def _assert_stopped(self, signum, code, name):
        process = self._launch()
        try:
            self._wait_for_the_arm(process)
            os.kill(process.pid, signum)
            output = process.communicate(timeout=240.0)[0]
        finally:
            if process.poll() is None:
                process.kill()
                process.wait(timeout=60)
        self.assertEqual(process.returncode, code, msg=output)
        tree = self._tree()
        self.assertTrue((tree / "resume.pt").is_file(), output)
        self.assertEqual(sorted(path.name for path in tree.glob("stop-*.json")), ["stop-1.json"])
        self.assertEqual(list(tree.rglob("*.tmp*")), [])
        marker = json.loads((tree / "stop-1.json").read_bytes())
        self.assertEqual((marker["signal"], marker["exit_code"]), (name, code))

    def test_sighup_exits_129_with_a_checkpoint(self):
        self._assert_stopped(signal.SIGHUP, 129, "SIGHUP")

    def test_sigint_exits_130_with_a_checkpoint(self):
        self._assert_stopped(signal.SIGINT, 130, "SIGINT")

    def test_sigterm_exits_143_with_a_checkpoint(self):
        self._assert_stopped(signal.SIGTERM, 143, "SIGTERM")

    def test_sigkill_leaves_no_stop_marker_and_the_resume_is_refused(self):
        process = self._launch()
        try:
            self._wait_for_the_arm(process)
            os.kill(process.pid, signal.SIGKILL)
            process.communicate(timeout=240.0)
        finally:
            if process.poll() is None:
                process.kill()
                process.wait(timeout=60)
        self.assertEqual(process.returncode, -signal.SIGKILL)
        tree = self._tree()
        self.assertEqual(sorted(path.name for path in tree.glob("stop-*.json")), [])
        with self.assertRaises(ResumeRefused):
            load_resume_checkpoint(
                tree, arm_id=ARM_ID, protocol_sha256=None, module_sha256={}
            )


if __name__ == "__main__":
    unittest.main()
