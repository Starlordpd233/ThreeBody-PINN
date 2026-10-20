"""Phase 60 (INST-05 d, and the base half of c): a short fixture run through the harness.

The run is a fixture, not a Rung 1 result: its record says so, it lives under a
temporary evidence root, and a second invocation never replaces it. The tests
also pin the GAP-60-05 polish semantics, the data seam's refusals and the arm
path rules, with no corpus beyond the tiny temporary one.
"""

from __future__ import annotations

import dataclasses
import hashlib
import json
import re
import tempfile
import unittest
from collections import OrderedDict
from contextlib import ExitStack
from pathlib import Path
from types import SimpleNamespace
from unittest import mock

import numpy as np
import torch

from pinn.data.adapter import EvidenceRedactionError
from pinn.evaluate import CheckpointOwnershipError, evaluate_run
from pinn.training.config import OptConfig
from pinn.verification import evidence_io, learnability_arms, learnability_data, learnability_run
from pinn.verification.feasibility_scorecard import better_state, load_scorecard, polish_should_stop
from pinn.verification.learnability_arms import (
    FIXTURE_FORMULA_NOTE,
    RUN_SCHEMA,
    SEED,
    ArmSpec,
    FirstResultExists,
    arm_evidence_dir,
    arm_run_dir,
    fixture_arm,
    write_record_exclusive,
)
from pinn.verification.learnability_data import (
    HarnessHalt,
    fixture_context,
    load_arm_data,
    window,
)
from pinn.verification.learnability_losses import data_polish_objective
from pinn.verification.learnability_run import (
    build_arm_network,
    run_arm,
    weights_digest,
)
from pinn.verification.split_allowlist import SplitRefused
from tests.phase60._fixtures import gold_corpus_fixture

FIXTURE_RUNTIME = ("float64", "cpu")
HEX64 = re.compile(r"[0-9a-f]{64}")


def _arm_and_context(fixture):
    spec = fixture_arm(
        train_key=fixture.gold_key, score_key=fixture.gold_key, beside_key=fixture.base_key
    )
    context = fixture_context(
        allowlist=fixture.allowlist, reader=fixture.reader, stats=fixture.stats
    )
    return spec, context


def _run(fixture, root, *, steps=10, clock=None):
    spec, context = _arm_and_context(fixture)
    extra = {} if clock is None else {"clock": clock}
    record = run_arm(
        spec,
        context=context,
        scorecard=load_scorecard(),
        runtime=FIXTURE_RUNTIME,
        evidence_root=root,
        fixture_budget_steps=steps,
        **extra,
    )
    return spec, context, record


def _load_state(path):
    return torch.load(path, map_location="cpu", weights_only=True)


class _FixtureRunCase(unittest.TestCase):
    """Base for tests that need a fresh fixture corpus and a temporary evidence root."""

    def setUp(self):
        stack = ExitStack()
        self.addCleanup(stack.close)
        self.fixture = stack.enter_context(gold_corpus_fixture())
        self.root = Path(stack.enter_context(tempfile.TemporaryDirectory(prefix="phase60-run-")))


class ShortRunTests(unittest.TestCase):
    """INST-05(d): one short run, shared by every read-only assertion below."""

    @classmethod
    def setUpClass(cls):
        stack = ExitStack()
        cls.addClassCleanup(stack.close)
        cls.fixture = stack.enter_context(gold_corpus_fixture())
        cls.root = Path(stack.enter_context(tempfile.TemporaryDirectory(prefix="phase60-run-")))
        cls.spec, cls.context, cls.returned = _run(cls.fixture, cls.root)
        cls.arm_dir = arm_evidence_dir(cls.spec.arm_id, evidence_root=cls.root)
        cls.record_bytes = (cls.arm_dir / "record.json").read_bytes()
        cls.record = json.loads(cls.record_bytes)

    def test_record_is_canonical_json_and_matches_what_run_arm_returned(self):
        self.assertEqual(evidence_io.canonical_json_bytes(self.returned), self.record_bytes)

    def test_record_marks_itself_as_a_diagnostic_fixture(self):
        record = self.record
        self.assertEqual(record["schema"], RUN_SCHEMA)
        self.assertIs(record["diagnostic"], True)
        self.assertEqual(record["run_kind"], "fixture")
        self.assertIs(record["counted"], False)
        self.assertEqual(record["budget"]["rule"], "fixture")
        self.assertEqual(record["formula"], {"E_formula": FIXTURE_FORMULA_NOTE, "counts": None})
        self.assertEqual(record["keys"]["train"], "hierarchical/gold/%d" % self.spec.system_id)
        self.assertEqual(record["keys"]["beside"], "hierarchical/base/%d" % self.spec.system_id)
        self.assertEqual(record["first_omega_0"], 30.0)
        self.assertEqual(record["omega_provenance"], "locked")
        self.assertEqual(record["seed"], SEED)
        self.assertEqual(record["runtime"], {"dtype": "float64", "device": "cpu"})
        self.assertIsNone(record["attestation"])
        self.assertEqual(record["mps_fallback_env"], learnability_run._PRE_IMPORT_FALLBACK)
        self.assertEqual(len(record["readout_notes"]), 1)
        self.assertIn("D-04", record["readout_notes"][0])
        self.assertIn("low-rate tail", record["readout_notes"][0])

    def test_record_carries_no_local_path(self):
        text = self.record_bytes.decode("ascii")
        self.assertNotIn(str(Path.home()), text)
        self.assertNotIn(str(self.root), text)
        self.assertNotIn(str(self.fixture.data_root), text)

    def test_readings_run_from_step_zero_to_the_budget(self):
        budget = self.record["budget"]
        self.assertEqual(budget["budget_steps"], 10)
        self.assertEqual(budget["reading_steps"][0], 0)
        self.assertEqual(budget["reading_steps"][-1], 10)
        self.assertEqual([step for step, _ in budget["readings"]], budget["reading_steps"])
        self.assertEqual([entry["step"] for entry in self.record["trace"]], budget["reading_steps"])

    def test_schedule_is_the_stage_zero_cosine_not_the_phase_38_constant_rate(self):
        schedule = self.record["schedule"]
        options = OptConfig()
        self.assertEqual(schedule["lr_stage"], 0)
        self.assertEqual(schedule["lr_k"], options.lr_for_stage(0))
        self.assertEqual(schedule["lr_k"], 1e-3)
        self.assertEqual(schedule["betas"], [0.9, 0.999])
        self.assertEqual(schedule["eps"], 1e-8)
        self.assertEqual(schedule["cosine_t_max"], 10)

    def test_data_points_use_the_real_normalized_ic13_not_the_zero_placeholder(self):
        scorecard = load_scorecard()
        data = load_arm_data(
            self.spec, self.context, scorecard=scorecard, dtype=torch.float64,
            device=torch.device("cpu"),
        )
        tau_ic13 = data.data_points.tau_ic13
        self.assertEqual(tuple(tau_ic13.shape), (24, 14))
        self.assertEqual(float(tau_ic13[0, 0]), -1.0)
        self.assertEqual(float(tau_ic13[-1, 0]), 1.0)
        self.assertGreater(float(tau_ic13[:, 1:].abs().max()), 0.1)
        self.assertTrue(torch.equal(tau_ic13[:, 1:], tau_ic13[:1, 1:].expand(24, 13)))
        self.assertEqual(tuple(data.data_points.masses.shape), (24, 3))
        self.assertEqual(tuple(data.data_points.targets.shape), (24, 3, 3))

    def test_both_states_carry_both_scores_and_weight_hashes(self):
        for name in ("adam", "polish"):
            state = self.record["states"][name]
            self.assertEqual(state["score_gold"]["grid"], "gold")
            self.assertEqual(state["score_base"]["grid"], "base")
            self.assertEqual(state["score_gold"]["n_times"], 24)
            self.assertEqual(state["score_base"]["n_times"], 12)
            self.assertEqual(state["weights"]["file"], f"{name}.weights")
            self.assertRegex(state["weights"]["sha256"], HEX64)
            self.assertRegex(state["weights"]["tensor_digest"], HEX64)

    def test_better_state_is_the_frozen_rule_and_the_result_is_that_states_gold_score(self):
        record = self.record
        chosen = record["better_state"]
        self.assertIn(chosen, ("adam", "polish"))
        adam = record["states"]["adam"]["score_gold"]
        polish = record["states"]["polish"]["score_gold"]
        self.assertEqual(
            chosen,
            better_state(
                {"E": adam["E"], "eps_h": adam["eps_h"]},
                {"E": polish["E"], "eps_h": polish["eps_h"]},
                scorecard=load_scorecard(),
            ),
        )
        selected = record["states"][chosen]["score_gold"]
        self.assertEqual(record["result"]["state"], chosen)
        self.assertEqual(record["result"]["tier"], selected["tier"])
        for field in ("E", "e_in_max", "h", "eps_h"):
            self.assertEqual(record["result"][field], selected[field])

    def test_polish_trace_has_outer_calls_and_names_why_it_stopped(self):
        polish = self.record["states"]["polish"]
        self.assertGreaterEqual(polish["outer_calls"], 1)
        self.assertEqual(len(polish["trace"]), polish["outer_calls"])
        for entry in polish["trace"]:
            objective = entry["objective"]
            self.assertTrue(isinstance(objective, float) or isinstance(objective, str))
        self.assertRegex(polish["stop_reason"], r"^(no_improvement_calls|adam_wall_fraction):")

    def test_weights_files_load_with_weights_only_and_match_the_record(self):
        for name in ("adam", "polish"):
            path = self.arm_dir / f"{name}.weights"
            recorded = self.record["states"][name]["weights"]
            self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), recorded["sha256"])
            state = _load_state(path)
            self.assertIsInstance(state, OrderedDict)
            self.assertEqual(weights_digest(state), recorded["tensor_digest"])
            for tensor in state.values():
                self.assertEqual(tensor.device.type, "cpu")
                self.assertEqual(tensor.dtype, torch.float64)
            model = build_arm_network(30.0, dtype=torch.float64, device=torch.device("cpu"))
            model.load_state_dict(state)

    def test_arm_directory_holds_exactly_the_record_and_two_weights_files(self):
        self.assertEqual(
            sorted(path.name for path in self.arm_dir.iterdir()),
            ["adam.weights", "polish.weights", "record.json"],
        )
        names = {path.name for path in self.root.rglob("*")}
        self.assertNotIn("config.yaml", names)
        self.assertNotIn("splits.json", names)

    def test_second_run_is_refused_before_any_optimizer_step(self):
        with mock.patch.object(torch.optim.Adam, "step") as adam_step, \
                mock.patch.object(torch.optim.LBFGS, "step") as lbfgs_step:
            with self.assertRaises(FirstResultExists):
                _run(self.fixture, self.root)
        self.assertEqual(adam_step.call_count, 0)
        self.assertEqual(lbfgs_step.call_count, 0)
        self.assertEqual((self.arm_dir / "record.json").read_bytes(), self.record_bytes)

    def test_evaluator_refuses_both_weights_files_before_any_claim(self):
        for name in ("adam", "polish"):
            with self.assertRaises(CheckpointOwnershipError):
                evaluate_run(
                    checkpoint_path=self.arm_dir / f"{name}.weights",
                    output_dir=self.arm_dir / "evaluation",
                )
        self.assertEqual(list(self.root.rglob("evaluation-attempt.json")), [])
        self.assertFalse((self.arm_dir / "evaluation").exists())


class PolishSemanticsTests(_FixtureRunCase):
    """GAP-60-05: improvement, the stop rule and the polish state."""

    def _unchanged_lbfgs(self, clock_state, advance=0.0):
        def step(optimizer, closure):
            clock_state["now"] += advance
            return torch.tensor(1.0)

        return mock.patch.object(torch.optim.LBFGS, "step", step)

    def _adam_clock(self, clock_state, per_step=100.0):
        real_step = torch.optim.Adam.step

        def step(optimizer, *args, **kwargs):
            clock_state["now"] += per_step
            return real_step(optimizer, *args, **kwargs)

        return mock.patch.object(torch.optim.Adam, "step", step)

    def test_stop_rule_runs_after_every_outer_call_with_the_summed_adam_wall(self):
        with mock.patch.object(
            learnability_run, "polish_should_stop", wraps=polish_should_stop
        ) as spy:
            _spec, _context, record = _run(self.fixture, self.root, steps=3)
        polish = record["states"]["polish"]
        self.assertGreaterEqual(spy.call_count, polish["outer_calls"])
        for index, entry in enumerate(polish["trace"]):
            call = spy.call_args_list[index]
            self.assertEqual(
                call.args,
                (entry["calls_without_improvement"], entry["elapsed_seconds"],
                 record["wall"]["adam_seconds"]),
            )
            self.assertEqual(set(call.kwargs), {"scorecard"})

    def test_five_calls_without_a_lower_objective_stop_the_polish(self):
        clock_state = {"now": 0.0}
        with self._adam_clock(clock_state), self._unchanged_lbfgs(clock_state):
            _spec, _context, record = _run(
                self.fixture, self.root, steps=2, clock=lambda: clock_state["now"]
            )
        polish = record["states"]["polish"]
        self.assertEqual(record["wall"]["adam_seconds"], 200.0)
        self.assertEqual(polish["outer_calls"], 5)
        self.assertEqual(
            [entry["calls_without_improvement"] for entry in polish["trace"]], [1, 2, 3, 4, 5]
        )
        self.assertFalse(any(entry["improved"] for entry in polish["trace"]))
        self.assertTrue(polish["stop_reason"].startswith("no_improvement_calls: 5 "))
        self.assertEqual(
            polish["weights"]["tensor_digest"], record["states"]["adam"]["weights"]["tensor_digest"]
        )
        self.assertEqual(record["better_state"], "adam")

    def test_quarter_of_the_adam_wall_stops_the_polish(self):
        clock_state = {"now": 0.0}
        with self._adam_clock(clock_state), self._unchanged_lbfgs(clock_state, advance=300.0):
            _spec, _context, record = _run(
                self.fixture, self.root, steps=2, clock=lambda: clock_state["now"]
            )
        polish = record["states"]["polish"]
        self.assertEqual(record["wall"]["adam_seconds"], 200.0)
        self.assertEqual(polish["outer_calls"], 1)
        self.assertEqual(polish["trace"][0]["elapsed_seconds"], 300.0)
        self.assertTrue(polish["stop_reason"].startswith("adam_wall_fraction:"))

    def test_improvement_is_strictly_below_the_best_so_far_starting_at_the_adam_result(self):
        clock_state = {"now": 0.0}
        scripted = [1.0, 0.9, 0.9, 0.8, 0.8, 0.8, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7]
        with self._adam_clock(clock_state), self._unchanged_lbfgs(clock_state), \
                mock.patch.object(
                    learnability_run, "data_polish_objective",
                    side_effect=[torch.tensor(value, dtype=torch.float64) for value in scripted],
                ):
            _spec, _context, record = _run(
                self.fixture, self.root, steps=2, clock=lambda: clock_state["now"]
            )
        trace = record["states"]["polish"]["trace"]
        self.assertEqual([entry["objective"] for entry in trace], scripted[1:])
        self.assertEqual(
            [entry["improved"] for entry in trace],
            [True, False, True, False, False, True, False, False, False, False, False],
        )
        self.assertEqual(
            [entry["calls_without_improvement"] for entry in trace],
            [0, 1, 0, 1, 2, 0, 1, 2, 3, 4, 5],
        )
        self.assertEqual(
            [entry["best_objective"] for entry in trace],
            [0.9, 0.9, 0.8, 0.8, 0.8, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7],
        )
        self.assertTrue(record["states"]["polish"]["stop_reason"].startswith("no_improvement_calls:"))

    def test_the_baseline_is_the_objective_at_the_adam_result(self):
        spec, context, record = _run(self.fixture, self.root, steps=2)
        data = load_arm_data(
            spec, context, scorecard=load_scorecard(), dtype=torch.float64,
            device=torch.device("cpu"),
        )
        model = build_arm_network(30.0, dtype=torch.float64, device=torch.device("cpu"))
        arm_dir = arm_evidence_dir(spec.arm_id, evidence_root=self.root)
        model.load_state_dict(_load_state(arm_dir / "adam.weights"))
        baseline = float(
            data_polish_objective(
                model, data.data_points, chunk_size=OptConfig().lbfgs_chunk_size,
                dtype=torch.float64, device=torch.device("cpu"),
            )
        )
        first = record["states"]["polish"]["trace"][0]
        self.assertEqual(first["improved"], first["objective"] < baseline)
        self.assertAlmostEqual(
            first["best_objective"], min(baseline, first["objective"]), places=12
        )

    def test_a_non_finite_outer_call_keeps_the_parameters_from_before_it(self):
        def poison(optimizer, closure):
            with torch.no_grad():
                optimizer.param_groups[0]["params"][0].add_(float("nan"))
            return torch.tensor(1.0)

        with mock.patch.object(torch.optim.LBFGS, "step", poison):
            _spec, _context, record = _run(self.fixture, self.root, steps=2)
        polish = record["states"]["polish"]
        self.assertEqual(polish["outer_calls"], 1)
        self.assertTrue(polish["trace"][0]["restored"])
        self.assertTrue(polish["stop_reason"].startswith("non_finite:"))
        self.assertEqual(
            polish["weights"]["tensor_digest"], record["states"]["adam"]["weights"]["tensor_digest"]
        )
        self.assertEqual(polish["score_gold"], record["states"]["adam"]["score_gold"])
        self.assertEqual(record["better_state"], "adam")


class FixtureGatingTests(_FixtureRunCase):
    """A fixture budget is legal only for a fixture arm on a fixture context."""

    def _run_arm(self, spec, context, **overrides):
        options = dict(
            context=context, scorecard=load_scorecard(), runtime=FIXTURE_RUNTIME,
            evidence_root=self.root, fixture_budget_steps=2,
        )
        options.update(overrides)
        return run_arm(spec, **options)

    def _assert_nothing_written(self):
        self.assertEqual(list(self.root.rglob("*")), [])

    def test_a_real_arm_cannot_use_a_fixture_budget(self):
        spec, context = _arm_and_context(self.fixture)
        with self.assertRaises(HarnessHalt):
            self._run_arm(dataclasses.replace(spec, run_kind="real"), context)
        self._assert_nothing_written()

    def test_a_real_context_cannot_use_a_fixture_budget(self):
        spec, context = _arm_and_context(self.fixture)
        with self.assertRaises(HarnessHalt):
            self._run_arm(spec, dataclasses.replace(context, run_kind="real"))
        self._assert_nothing_written()

    def test_a_fixture_budget_is_required_and_must_be_a_positive_integer(self):
        spec, context = _arm_and_context(self.fixture)
        for bad in (None, 0, -3, 2.5, True):
            with self.subTest(budget=bad):
                with self.assertRaises(HarnessHalt):
                    self._run_arm(spec, context, fixture_budget_steps=bad)
        self._assert_nothing_written()

    def test_only_the_data_only_loss_arm_is_trained_here(self):
        spec, context = _arm_and_context(self.fixture)
        for loss_arm in ("physics_ic", "full"):
            with self.subTest(loss_arm=loss_arm):
                with self.assertRaises(HarnessHalt):
                    self._run_arm(dataclasses.replace(spec, loss_arm=loss_arm), context)
        self._assert_nothing_written()

    def test_a_spec_with_an_unauthorized_omega_is_refused_before_anything_is_written(self):
        # Plan 60-23 routes the first-layer frequency, so this refusal now comes from
        # the override check (INST-05(e)). Plan 60-01 had a runner that halted on any
        # non-locked setting and a builder that built the locked network only.
        spec, context = _arm_and_context(self.fixture)
        for changes in ({"grid_omega": 60.0}, {"omega_provenance": "g2_sweep_override"}):
            with self.subTest(changes=changes):
                with self.assertRaises(learnability_arms.OverrideRefused):
                    self._run_arm(dataclasses.replace(spec, **changes), context)
        self._assert_nothing_written()

    def test_the_runtime_is_a_named_pair_with_no_availability_probe(self):
        spec, context = _arm_and_context(self.fixture)
        for bad in (("float16", "cpu"), ("float64", "no-such-device"), "float64", None):
            with self.subTest(runtime=bad):
                with self.assertRaises(HarnessHalt):
                    self._run_arm(spec, context, runtime=bad)
        self._assert_nothing_written()


class _Horizon:
    """A scorecard stand-in that only names the scored horizon."""

    def __init__(self, t_max):
        self._t_max = t_max

    def section(self, name):
        if name != "scoring_grid":
            raise KeyError(name)
        return {"t_max": self._t_max}


class DataSeamTests(_FixtureRunCase):
    def test_every_view_and_the_training_points_stop_at_the_scored_horizon(self):
        spec, context = _arm_and_context(self.fixture)
        data = load_arm_data(
            spec, context, scorecard=_Horizon(5.0), dtype=torch.float64,
            device=torch.device("cpu"),
        )
        # 24 gold points on [0, 10] and 12 base points on [0, 10]: 12 and 6 are within 5.
        self.assertEqual(data.records["train"]["n_snapshots"], 24)
        self.assertEqual(data.records["train"]["n_within_t"], 12)
        self.assertEqual(data.records["beside"]["n_within_t"], 6)
        self.assertEqual(tuple(data.data_points.tau_ic13.shape), (12, 14))
        self.assertEqual(tuple(data.data_points.targets.shape), (12, 3, 3))
        self.assertEqual(data.score.times.shape, (12,))
        self.assertEqual(data.score.positions.shape, (12, 3, 3))
        self.assertEqual(data.beside.times.shape, (6,))
        self.assertLessEqual(float(data.score.times.max()), 5.0 + 1e-9)
        self.assertLessEqual(float(data.beside.times.max()), 5.0 + 1e-9)
        self.assertLess(float(data.data_points.tau_ic13[-1, 0]), 0.0)

    def test_window_drops_the_1002nd_gold_snapshot(self):
        times = np.round(np.arange(1002) * 0.01, 2)
        reference = SimpleNamespace(
            times=times, positions=np.zeros((1002, 3, 3)), velocities=np.ones((1002, 3, 3))
        )
        kept_times, kept_positions, kept_velocities = window(reference, 10.0)
        self.assertEqual(kept_times.shape, (1001,))
        self.assertEqual(float(kept_times[-1]), 10.0)
        self.assertEqual(kept_positions.shape, (1001, 3, 3))
        self.assertEqual(kept_velocities.shape, (1001, 3, 3))

    def test_a_withheld_key_is_refused_before_any_record_is_read(self):
        spec, context = _arm_and_context(self.fixture)
        withheld = dataclasses.replace(spec, score_key=self.fixture.test_key)
        before = self.fixture.reader.read_counts()
        with self.assertRaises(SplitRefused):
            load_arm_data(
                withheld, context, scorecard=load_scorecard(), dtype=torch.float64,
                device=torch.device("cpu"),
            )
        self.assertEqual(self.fixture.reader.read_counts()["train"], before["train"])
        self.assertEqual(self.fixture.reader.read_counts()["validation"], before["validation"])

    def test_a_path_is_not_an_arm_record(self):
        spec, _context = _arm_and_context(self.fixture)
        with self.assertRaises(TypeError):
            dataclasses.replace(spec, train_key="hierarchical/gold/0")

    def test_records_whose_raw_ic13_differ_halt_the_arm(self):
        spec, context = _arm_and_context(self.fixture)
        real_load = learnability_data.load_reference

        def perturbed(reader, key):
            reference = real_load(reader, key)
            if key.fidelity == "base":
                return dataclasses.replace(reference, raw_ic13=reference.raw_ic13 + 1.0)
            return reference

        with mock.patch.object(learnability_data, "load_reference", perturbed):
            with self.assertRaises(HarnessHalt):
                load_arm_data(
                    spec, context, scorecard=load_scorecard(), dtype=torch.float64,
                    device=torch.device("cpu"),
                )

    def test_the_summary_names_each_record_and_its_windowed_hash(self):
        spec, context = _arm_and_context(self.fixture)
        data = load_arm_data(
            spec, context, scorecard=load_scorecard(), dtype=torch.float64,
            device=torch.device("cpu"),
        )
        self.assertEqual(sorted(data.records), ["beside", "score", "train"])
        for summary in data.records.values():
            self.assertEqual(summary["split"], "train")
            self.assertEqual(summary["n_within_t"], summary["n_snapshots"])
            self.assertRegex(summary["windowed_sha256"], HEX64)
        self.assertEqual(data.records["train"], data.records["score"])
        self.assertEqual(data.records["beside"]["n_snapshots"], 12)


class ArmPathRuleTests(unittest.TestCase):
    """T-60-05: an arm id is a plain lowercase token and never a path."""

    def test_plain_ids_are_accepted(self):
        root = Path("evidence-root")
        self.assertEqual(
            arm_evidence_dir("r1-1632", evidence_root=root), root / "arms" / "r1-1632"
        )
        self.assertEqual(
            arm_run_dir("r1-1632", repo_root=Path("repo")), Path("repo/runs/phase60/r1-1632")
        )

    def test_ids_that_could_escape_the_tree_are_refused(self):
        for bad in ("", "..", "../x", "a/b", "a\\b", "A1", "x y", "x\n", "x.y", "/abs", None, 7):
            with self.subTest(arm_id=bad):
                with self.assertRaises(ValueError):
                    arm_evidence_dir(bad, evidence_root=Path("root"))
                with self.assertRaises(ValueError):
                    arm_run_dir(bad, repo_root=Path("repo"))

    def test_the_fixture_arm_is_uncounted_stage_zero_and_named_for_its_record(self):
        with gold_corpus_fixture() as fixture:
            spec = fixture_arm(
                train_key=fixture.gold_key, score_key=fixture.gold_key,
                beside_key=fixture.base_key,
            )
        self.assertEqual(spec.arm_id, "fixture-hierarchical-gold-%d" % fixture.gold_key.id)
        self.assertEqual((spec.run_kind, spec.counted), ("fixture", False))
        self.assertEqual((spec.lr_stage, spec.clip_stage), (0, 0))
        self.assertEqual((spec.loss_arm, spec.omega_provenance, spec.grid_omega), ("data_only", "locked", None))

    def test_the_spec_validates_its_closed_vocabularies(self):
        with gold_corpus_fixture() as fixture:
            spec = fixture_arm(
                train_key=fixture.gold_key, score_key=fixture.gold_key,
                beside_key=fixture.base_key,
            )
        for changes in (
            {"loss_arm": "everything"},
            {"omega_provenance": "whatever"},
            {"run_kind": "pretend"},
            {"arm_id": "../escape"},
        ):
            with self.subTest(changes=changes):
                with self.assertRaises(ValueError):
                    dataclasses.replace(spec, **changes)
        self.assertIsInstance(spec, ArmSpec)


class ExclusiveWriterTests(unittest.TestCase):
    def test_a_record_is_created_once_and_never_replaced(self):
        with tempfile.TemporaryDirectory(prefix="phase60-write-") as tmp:
            path = Path(tmp) / "arms" / "x" / "record.json"
            digest = write_record_exclusive(path, {"b": 2, "a": float("nan")})
            first = path.read_bytes()
            self.assertEqual(hashlib.sha256(first).hexdigest(), digest)
            self.assertEqual(first, evidence_io.canonical_json_bytes({"b": 2, "a": float("nan")}))
            with self.assertRaises(FirstResultExists):
                write_record_exclusive(path, {"replacement": True})
            self.assertEqual(path.read_bytes(), first)

    def test_a_record_naming_the_home_directory_is_refused_and_not_created(self):
        with tempfile.TemporaryDirectory(prefix="phase60-write-") as tmp:
            path = Path(tmp) / "record.json"
            with self.assertRaises(EvidenceRedactionError):
                write_record_exclusive(path, {"where": str(Path.home())})
            self.assertFalse(path.exists())

    def test_a_record_cannot_be_written_inside_the_data_root(self):
        with tempfile.TemporaryDirectory(prefix="phase60-write-") as tmp:
            data_root = Path(tmp) / "Data"
            data_root.mkdir()
            with self.assertRaises(ValueError):
                write_record_exclusive(data_root / "record.json", {"a": 1}, data_root=data_root)
            self.assertFalse((data_root / "record.json").exists())


if __name__ == "__main__":
    unittest.main()
