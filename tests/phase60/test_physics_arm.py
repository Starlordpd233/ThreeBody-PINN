"""Phase 60 (D-01, D-06, D-08, GAP-60-05, GAP-60-12): a physics arm end to end on the fixture.

Two arms run once each on the tiny corpus: the full ratified loss (Rung 2b) and physics plus
the initial condition only (Rung 2a). Every assertion reads the record they wrote, or the
spies that watched the calls the record is built from.

What the tests prove:

* the ratified schedule is unchanged and the PHYS-05 warmup runs over the arm's own budget;
* one frozen monitor set is drawn from the arm's stream before step 1 and logged, with its
  seven statistics, at exactly the budget-rule readings and nowhere else (D-06);
* nothing in the runner reads ``front_idx`` to branch on it;
* the handoff freezes the rows, the pass-1 causal weights, the bin counts and the loss
  weights once, and the polish redraws nothing (GAP-60-05);
* Rung 2a never evaluates the data term (FEAS-04 arm (a));
* both scored states carry their official scores, their weights and the CPU float64
  cross-check (GAP-60-07);
* the fixture knobs a real arm must never use are refused.
"""

from __future__ import annotations

import math
import re
import tempfile
import unittest
from contextlib import ExitStack
from pathlib import Path
from unittest import mock

import numpy as np

from pinn.verification import learnability_losses, learnability_run
from pinn.verification.feasibility_scorecard import load_scorecard
from pinn.verification.learnability_arms import (
    FIXTURE_FORMULA_NOTE,
    REAL_RUNTIME,
    TIMING_STEPS,
    arm_evidence_dir,
    fixture_arm,
)
from pinn.verification.learnability_data import HarnessHalt, fixture_context
from pinn.verification.learnability_run import run_arm
from tests.phase60._fixtures import gold_corpus_fixture

FIXTURE_RUNTIME = ("float64", "cpu")
HEX64 = re.compile(r"[0-9a-f]{64}")
BUDGET = 6
TIMING_STEPS_FIXTURE = 50
MONITOR_KEYS = {
    "w_min",
    "w_mean",
    "w_max",
    "front_idx",
    "residuals_per_bin",
    "raw_residuals_per_bin",
    "r_ref",
}


class _Recorder:
    """Wraps a callable and appends an event before delegating."""

    def __init__(self, events, label, function):
        self.events = events
        self.label = label
        self.function = function

    def __call__(self, *args, **kwargs):
        self.events.append((self.label, args, kwargs))
        return self.function(*args, **kwargs)


class _Arms:
    """Two fixture physics arms run once, with every call the record is built from recorded."""

    def __init__(self):
        self.stack = ExitStack()
        self.fixture = self.stack.enter_context(gold_corpus_fixture())
        self.root = Path(self.stack.enter_context(tempfile.TemporaryDirectory(prefix="phase60-phys-")))
        self.scorecard = load_scorecard()
        self.context = fixture_context(
            allowlist=self.fixture.allowlist, reader=self.fixture.reader, stats=self.fixture.stats
        )
        self.records = {}
        self.events = {}
        self.adam_steps = {}
        self.data_calls = {}
        self.draw_results = {}

        for loss_arm in ("full", "physics_ic"):
            self._run(loss_arm)

    def _spec(self, loss_arm):
        return fixture_arm(
            train_key=self.fixture.base_key,
            score_key=self.fixture.gold_key,
            beside_key=self.fixture.base_key,
            loss_arm=loss_arm,
        )

    def _run(self, loss_arm):
        events = []
        self.events[loss_arm] = events
        steps = []
        self.adam_steps[loss_arm] = steps
        data_calls = []
        self.data_calls[loss_arm] = data_calls
        draws = []
        self.draw_results[loss_arm] = draws

        real_step = learnability_run.physics_adam_step
        real_pass1 = learnability_run.physics_pass1
        real_monitor = learnability_run.frozen_monitor_log
        real_draw = learnability_run.draw_collocation_times
        real_polish = learnability_run.physics_polish_objective
        real_data_loss = learnability_losses.data_only_loss

        def record_step(*args, **kwargs):
            steps.append(kwargs.get("data_points"))
            return real_step(*args, **kwargs)

        def record_data_loss(*args, **kwargs):
            data_calls.append(1)
            return real_data_loss(*args, **kwargs)

        def record_draw(*args, **kwargs):
            times = real_draw(*args, **kwargs)
            draws.append(times)
            return times

        spec = self._spec(loss_arm)
        arm_root = self.root / loss_arm
        with mock.patch.object(
            learnability_run, "physics_adam_step",
            _Recorder(events, "step", record_step),
        ), mock.patch.object(
            learnability_run, "physics_pass1", _Recorder(events, "pass1", real_pass1),
        ), mock.patch.object(
            learnability_run, "frozen_monitor_log", _Recorder(events, "monitor", real_monitor),
        ), mock.patch.object(
            learnability_run, "draw_collocation_times", _Recorder(events, "draw", record_draw),
        ), mock.patch.object(
            learnability_run, "physics_polish_objective", _Recorder(events, "polish", real_polish),
        ), mock.patch.object(
            learnability_losses, "data_only_loss", record_data_loss,
        ):
            record = run_arm(
                spec,
                context=self.context,
                scorecard=self.scorecard,
                runtime=FIXTURE_RUNTIME,
                evidence_root=arm_root,
                fixture_budget_steps=BUDGET,
                fixture_timing_steps=TIMING_STEPS_FIXTURE,
                fixture_n_slots=1,
                fixture_r_ref=1.0,
            )
        self.records[loss_arm] = record
        self.specs = getattr(self, "specs", {})
        self.specs[loss_arm] = spec
        self.arm_dirs = getattr(self, "arm_dirs", {})
        self.arm_dirs[loss_arm] = arm_evidence_dir(spec.arm_id, evidence_root=arm_root)

    def timeline(self, loss_arm):
        """The arm's own events, with the timing run's steps and draws separated out.

        The timing run builds its own model and its own generator, so the arm's are the
        model of the last Adam step and the generator of the last draw (the handoff draw).
        """
        events = self.events[loss_arm]
        positions = {}
        for index, (label, _args, _kwargs) in enumerate(events):
            positions.setdefault(label, []).append(index)
        arm_model = events[positions["step"][-1]][1][0]
        arm_rng = events[positions["draw"][-1]][1][1]
        return {
            "events": events,
            "positions": positions,
            "arm_model": arm_model,
            "arm_rng": arm_rng,
            "steps": [i for i in positions.get("step", []) if events[i][1][0] is arm_model],
            "draws": [i for i in positions.get("draw", []) if events[i][1][1] is arm_rng],
            "monitors": positions.get("monitor", []),
            "pass1": positions.get("pass1", []),
            "polish": positions.get("polish", []),
        }

    def close(self):
        self.stack.close()


class PhysicsTracerTests(unittest.TestCase):
    """Both physics loss arms run end to end under the trainer's composition."""

    @classmethod
    def setUpClass(cls):
        cls.arms = _Arms()
        cls.addClassCleanup(cls.arms.close)

    def test_both_physics_loss_arms_write_a_record_with_both_scored_states(self):
        for loss_arm in ("full", "physics_ic"):
            with self.subTest(loss_arm=loss_arm):
                record = self.arms.records[loss_arm]
                self.assertEqual(record["loss_arm"], loss_arm)
                for state in ("adam", "polish"):
                    block = record["states"][state]
                    self.assertIn("score_gold", block)
                    self.assertIn("score_base", block)
                    self.assertEqual(block["weights"]["file"], f"{state}.weights")
                    self.assertEqual(
                        sorted(block["cross_check"]), ["E", "counts", "eps_h", "tier"]
                    )
                self.assertEqual(
                    sorted(path.name for path in self.arms.arm_dirs[loss_arm].iterdir()),
                    ["adam.weights", "polish.weights", "record.json"],
                )

    def test_the_monitor_log_is_recorded_at_exactly_the_reading_steps(self):
        for loss_arm in ("full", "physics_ic"):
            with self.subTest(loss_arm=loss_arm):
                record = self.arms.records[loss_arm]
                self.assertEqual(
                    [entry["step"] for entry in record["monitor_log"]],
                    record["budget"]["reading_steps"],
                )
                self.assertEqual(record["monitor_log"][0]["step"], 0)
                self.assertEqual(
                    record["monitor_log"][-1]["step"], record["budget"]["budget_steps"]
                )

    def test_every_monitor_entry_carries_the_seven_statistics(self):
        for loss_arm in ("full", "physics_ic"):
            with self.subTest(loss_arm=loss_arm):
                for entry in self.arms.records[loss_arm]["monitor_log"]:
                    self.assertEqual(set(entry), MONITOR_KEYS | {"step"})
                    self.assertEqual(len(entry["residuals_per_bin"]), 16)
                    self.assertEqual(len(entry["raw_residuals_per_bin"]), 16)
                    self.assertGreaterEqual(entry["front_idx"], -1)
                    self.assertLess(entry["front_idx"], 16)

    def test_the_monitor_runs_at_the_readings_and_nowhere_else(self):
        for loss_arm in ("full", "physics_ic"):
            with self.subTest(loss_arm=loss_arm):
                line = self.arms.timeline(loss_arm)
                readings = self.arms.records[loss_arm]["budget"]["reading_steps"]
                self.assertEqual(len(line["monitors"]), len(readings))
                self.assertEqual(len(line["steps"]), len(readings) - 1)
                # Reading 0 is taken before the first Adam step, so the first monitor call
                # sits before it too, and no monitor call follows the last step.
                self.assertLess(line["monitors"][0], line["steps"][0])
                self.assertGreater(line["monitors"][-1], line["steps"][-1])

    def test_the_frozen_monitor_set_is_drawn_before_the_first_step(self):
        for loss_arm in ("full", "physics_ic"):
            with self.subTest(loss_arm=loss_arm):
                line = self.arms.timeline(loss_arm)
                self.assertLess(line["draws"][0], line["monitors"][0])
                self.assertLess(line["draws"][0], line["steps"][0])

    def test_the_timing_run_uses_its_own_generator_from_the_same_seed(self):
        for loss_arm in ("full", "physics_ic"):
            with self.subTest(loss_arm=loss_arm):
                line = self.arms.timeline(loss_arm)
                events = line["events"]
                timing_rng = events[line["positions"]["draw"][0]][1][1]
                arm_rng = line["arm_rng"]
                self.assertIsNot(timing_rng, arm_rng)
                # Both start from seed 42 on the same record, so their first draws agree.
                draws = self.arms.draw_results[loss_arm]
                self.assertTrue(np.array_equal(draws[0], draws[len(draws) - len(line["draws"])]))
                # The timing run trained the same physics step 50 times.
                self.assertEqual(
                    len(line["positions"]["step"]) - len(line["steps"]), TIMING_STEPS_FIXTURE
                )

    def test_nothing_in_the_runner_reads_a_front_index_to_branch(self):
        # D-06: the monitor log is copied wholesale into the record; the runner never names
        # the statistic, so no value of it can steer a branch.
        source = Path(learnability_run.__file__).read_text(encoding="utf-8")
        self.assertNotIn("front_idx", source)
        self.assertIn("**frozen_monitor_log(", source)

    def test_the_warmup_is_the_phys05_rule_over_the_arms_own_budget(self):
        for loss_arm in ("full", "physics_ic"):
            with self.subTest(loss_arm=loss_arm):
                record = self.arms.records[loss_arm]
                budget = record["budget"]["budget_steps"]
                self.assertEqual(record["schedule"]["warmup_steps"], min(2000, math.floor(0.1 * budget)))

    def test_the_handoff_records_the_frozen_rows_weights_and_loss_weights(self):
        for loss_arm in ("full", "physics_ic"):
            with self.subTest(loss_arm=loss_arm):
                handoff = self.arms.records[loss_arm]["handoff"]
                self.assertEqual(sorted(handoff), ["rows_sha256", "w_n", "weights"])
                self.assertRegex(handoff["rows_sha256"], HEX64)
                self.assertEqual(len(handoff["w_n"]), 16)
                self.assertTrue(all(isinstance(value, float) for value in handoff["w_n"]))
                self.assertEqual(
                    sorted(handoff["weights"]),
                    ["lambda_data", "lambda_e", "lambda_ic", "lambda_l", "lambda_phys"],
                )

    def test_the_polish_redraws_nothing_after_the_handoff(self):
        for loss_arm in ("full", "physics_ic"):
            with self.subTest(loss_arm=loss_arm):
                line = self.arms.timeline(loss_arm)
                self.assertEqual(len(line["pass1"]), 1)
                # One draw for the frozen monitor set, one per Adam step, one at the handoff.
                self.assertEqual(len(line["draws"]), len(line["steps"]) + 2)
                self.assertLess(line["steps"][-1], line["pass1"][0])
                self.assertLess(line["pass1"][0], line["polish"][0])
                self.assertLess(max(line["draws"]), line["polish"][0])

    def test_rung_two_a_never_evaluates_a_data_term(self):
        record = self.arms.records["physics_ic"]
        self.assertEqual(record["loss_arm"], "physics_ic")
        steps = self.arms.adam_steps["physics_ic"]
        self.assertTrue(steps)
        self.assertTrue(all(points is None for points in steps))
        self.assertEqual(self.arms.data_calls["physics_ic"], [])

    def test_rung_two_b_trains_on_the_records_own_points(self):
        record = self.arms.records["full"]
        self.assertEqual(record["loss_arm"], "full")
        steps = self.arms.adam_steps["full"]
        self.assertTrue(steps)
        self.assertTrue(all(points is not None for points in steps))
        self.assertNotEqual(self.arms.data_calls["full"], [])

    def test_the_reference_in_force_and_the_scorer_context_are_recorded(self):
        for loss_arm in ("full", "physics_ic"):
            with self.subTest(loss_arm=loss_arm):
                record = self.arms.records[loss_arm]
                self.assertEqual(record["r_ref"]["value"], 1.0)
                self.assertIn("fixture", record["r_ref"]["note"])
                context_ref = record["scorer_context_r_ref"]
                self.assertEqual(
                    context_ref["path"], "pinn/verification/artifacts/r_ref_stage0.json"
                )
                self.assertRegex(context_ref["sha256"], HEX64)

    def test_a_stage_zero_physics_arm_records_no_energy_scale_because_none_is_used(self):
        for loss_arm in ("full", "physics_ic"):
            with self.subTest(loss_arm=loss_arm):
                record = self.arms.records[loss_arm]
                self.assertNotIn("s_h", record)
                self.assertEqual(record["handoff"]["weights"]["lambda_e"], 0.0)
                self.assertEqual(record["handoff"]["weights"]["lambda_l"], 0.0)

    def test_a_fixture_physics_arm_still_records_the_fixture_formula(self):
        for loss_arm in ("full", "physics_ic"):
            with self.subTest(loss_arm=loss_arm):
                self.assertEqual(
                    self.arms.records[loss_arm]["formula"],
                    {"E_formula": FIXTURE_FORMULA_NOTE, "counts": None},
                )


class FixtureKnobTests(unittest.TestCase):
    """A real arm refuses every fixture knob before anything is read or written."""

    def test_a_real_arm_refuses_the_fixture_slot_count_and_timing_knobs(self):
        with gold_corpus_fixture() as fixture:
            import dataclasses

            spec = dataclasses.replace(
                fixture_arm(
                    train_key=fixture.base_key,
                    score_key=fixture.gold_key,
                    beside_key=fixture.base_key,
                    loss_arm="physics_ic",
                ),
                run_kind="real",
            )
            context = dataclasses.replace(
                fixture_context(
                    allowlist=fixture.allowlist, reader=fixture.reader, stats=fixture.stats
                ),
                run_kind="real",
            )
            for knob in (
                {"fixture_n_slots": 1},
                {"fixture_timing_steps": TIMING_STEPS_FIXTURE},
                {"fixture_budget_steps": BUDGET},
                {"fixture_r_ref": 1.0},
            ):
                with self.subTest(knob=knob), tempfile.TemporaryDirectory(
                    prefix="phase60-real-knob-"
                ) as root:
                    with self.assertRaises(HarnessHalt):
                        run_arm(
                            spec,
                            context=context,
                            scorecard=load_scorecard(),
                            runtime=FIXTURE_RUNTIME,
                            evidence_root=Path(root),
                            **knob,
                        )
                    self.assertEqual(list(Path(root).rglob("*")), [])

    def test_the_slot_count_must_be_a_positive_integer(self):
        with gold_corpus_fixture() as fixture:
            spec = fixture_arm(
                train_key=fixture.base_key,
                score_key=fixture.gold_key,
                beside_key=fixture.base_key,
                loss_arm="physics_ic",
            )
            context = fixture_context(
                allowlist=fixture.allowlist, reader=fixture.reader, stats=fixture.stats
            )
            for bad in (0, -1, 1.5, True):
                with self.subTest(slots=bad), tempfile.TemporaryDirectory(
                    prefix="phase60-slots-"
                ) as root:
                    with self.assertRaises(HarnessHalt):
                        run_arm(
                            spec,
                            context=context,
                            scorecard=load_scorecard(),
                            runtime=FIXTURE_RUNTIME,
                            evidence_root=Path(root),
                            fixture_budget_steps=BUDGET,
                            fixture_timing_steps=TIMING_STEPS_FIXTURE,
                            fixture_n_slots=bad,
                            fixture_r_ref=1.0,
                        )
                    self.assertEqual(list(Path(root).rglob("*")), [])

    def test_a_real_physics_arm_without_an_admission_names_what_it_needs(self):
        with gold_corpus_fixture() as fixture:
            import dataclasses

            spec = dataclasses.replace(
                fixture_arm(
                    train_key=fixture.base_key,
                    score_key=fixture.gold_key,
                    beside_key=fixture.base_key,
                    loss_arm="physics_ic",
                ),
                run_kind="real",
            )
            context = dataclasses.replace(
                fixture_context(
                    allowlist=fixture.allowlist, reader=fixture.reader, stats=fixture.stats
                ),
                run_kind="real",
            )
            with tempfile.TemporaryDirectory(prefix="phase60-real-ref-") as root:
                with self.assertRaises(HarnessHalt) as caught:
                    run_arm(
                        spec,
                        context=context,
                        scorecard=load_scorecard(),
                        runtime=FIXTURE_RUNTIME,
                        evidence_root=Path(root),
                    )
                self.assertIn("r_ref", str(caught.exception))
                self.assertEqual(list(Path(root).rglob("*")), [])


class ModuleContractTests(unittest.TestCase):
    """The exports and constants Plan 60-11 names, and nothing that types a fixture as real."""

    def test_the_named_exports_exist(self):
        for name in (
            "CrossCheckDisagreement",
            "cross_check_state",
            "build_real_record",
            "validate_record",
            "REQUIRED_REAL_FIELDS",
            "R_REF_NOTE",
            "formula_reference",
        ):
            with self.subTest(name=name):
                self.assertTrue(hasattr(learnability_run, name), name)

    def test_the_real_runtime_is_the_protocol_runtime(self):
        self.assertEqual(REAL_RUNTIME, ("float32", "mps"))
        self.assertEqual(TIMING_STEPS["physics"], TIMING_STEPS_FIXTURE)

    def test_the_note_constant_is_the_ratified_wording(self):
        self.assertEqual(
            learnability_run.R_REF_NOTE, "Stage-0 reference in force, applied unchanged"
        )


if __name__ == "__main__":
    unittest.main()
