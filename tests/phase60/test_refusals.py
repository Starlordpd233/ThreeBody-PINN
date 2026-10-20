"""Phase 60 (INST-05 c, override half, and e): the override record end to end.

One fixture arm runs at ``first_omega_0 = 60`` through the separate omega
builder, and its record and weights are refused by the evaluator and by the
production checkpoint store, exactly as Plan 60-01's locked-setting record is.
A second class proves that an unauthorized setting is refused by ``run_arm``
before any data is read or any network is built, and that nothing is written.

The new symbols are reached through small helpers, so a run against code that
does not have them yet fails on the planned behavior instead of at import.
"""

from __future__ import annotations

import importlib
import shutil
import tempfile
import unittest
from contextlib import ExitStack
from pathlib import Path
from unittest import mock

import torch

from pinn.evaluate import CheckpointOwnershipError, evaluate_run
from pinn.training.atomic_io import atomic_write_torch
from pinn.training.checkpoint import (
    CHECKPOINT_SCHEMA_VERSION,
    NoValidCheckpointError,
    TorchSaveCheckpointStore,
)
from pinn.verification import learnability_arms, learnability_run
from pinn.verification.feasibility_scorecard import load_scorecard
from pinn.verification.feasibility_scorer import score_network
from pinn.verification.learnability_arms import SEED, arm_evidence_dir, fixture_arm
from pinn.verification.learnability_data import fixture_context, load_arm_data
from pinn.verification.learnability_run import build_arm_network, run_arm
from tests.phase60._fixtures import gold_corpus_fixture

FIXTURE_RUNTIME = ("float64", "cpu")
CPU = torch.device("cpu")


def _arms_symbol(case, name):
    value = getattr(learnability_arms, name, None)
    case.assertIsNotNone(value, f"pinn.verification.learnability_arms.{name} is missing")
    return value


def _omega_builder(case):
    try:
        module = importlib.import_module("pinn.verification.diagnostic_architecture")
    except ImportError as exc:  # the module is created by this plan
        case.fail(f"pinn.verification.diagnostic_architecture is missing: {exc}")
    return module.build_network_with_first_omega


def _fixture_spec(fixture, **changes):
    return fixture_arm(
        train_key=fixture.gold_key,
        score_key=fixture.gold_key,
        beside_key=fixture.base_key,
        **changes,
    )


def _context(fixture):
    return fixture_context(
        allowlist=fixture.allowlist, reader=fixture.reader, stats=fixture.stats
    )


def _run(fixture, root, **changes):
    spec = _fixture_spec(fixture, **changes)
    record = run_arm(
        spec,
        context=_context(fixture),
        scorecard=load_scorecard(),
        runtime=FIXTURE_RUNTIME,
        evidence_root=root,
        fixture_budget_steps=5,
    )
    return spec, record


def _valid_production_payload():
    """The smallest payload the production store accepts: the seven required keys."""
    return {
        "model": {"w": torch.zeros(2, dtype=torch.float64)},
        "optimizer": None,
        "curriculum": {"stage": 0, "phase": "2a"},
        "rng": {"torch": [1, 2, 3]},
        "counters": {"global_step": 0, "epoch": 0},
        "config_identity": {"digest": "abc", "config": {"seed": 0}},
        "schema_version": CHECKPOINT_SCHEMA_VERSION,
    }


class RefusalTests(unittest.TestCase):
    """INST-05(c): harness weights are refused, with and without an override."""

    @classmethod
    def setUpClass(cls):
        stack = ExitStack()
        cls.addClassCleanup(stack.close)
        cls.fixture = stack.enter_context(gold_corpus_fixture())
        cls.plain_root = Path(stack.enter_context(tempfile.TemporaryDirectory(prefix="phase60-plain-")))
        cls.override_root = Path(stack.enter_context(tempfile.TemporaryDirectory(prefix="phase60-omega60-")))
        cls.plain_spec, cls.plain_record = _run(cls.fixture, cls.plain_root)
        cls.override_spec, cls.override_record = _run(
            cls.fixture,
            cls.override_root,
            omega_provenance="g2_sweep_override",
            grid_omega=60.0,
        )
        cls.cases = {
            "plain": (cls.plain_root, cls.plain_spec),
            "override": (cls.override_root, cls.override_spec),
        }

    def _weights_files(self):
        for label, (root, spec) in self.cases.items():
            arm_dir = arm_evidence_dir(spec.arm_id, evidence_root=root)
            for name in ("adam", "polish"):
                yield label, root, arm_dir, arm_dir / f"{name}.weights"

    def test_the_override_record_names_the_setting_it_ran_at(self):
        record = self.override_record
        self.assertEqual(record["first_omega_0"], 60.0)
        self.assertEqual(record["grid_omega"], 60.0)
        self.assertEqual(record["omega_provenance"], "g2_sweep_override")
        self.assertEqual(record["loss_arm"], "data_only")
        self.assertIs(record["diagnostic"], True)
        self.assertEqual(record["run_kind"], "fixture")
        self.assertIs(record["counted"], False)

    def test_the_locked_record_names_no_grid_setting(self):
        record = self.plain_record
        self.assertEqual(record["first_omega_0"], 30.0)
        self.assertIsNone(record["grid_omega"])
        self.assertEqual(record["omega_provenance"], "locked")

    def test_the_override_run_really_trained_and_was_scored_at_omega_60(self):
        arm_dir = arm_evidence_dir(self.override_spec.arm_id, evidence_root=self.override_root)
        state = torch.load(arm_dir / "adam.weights", map_location="cpu", weights_only=True)
        scorecard = load_scorecard()
        data = load_arm_data(
            self.override_spec, _context(self.fixture), scorecard=scorecard,
            dtype=torch.float64, device=CPU,
        )

        def rescored_error(model):
            model.load_state_dict(state)
            return score_network(
                model, data.ic13, data.masses, data.score.positions, data.score.inner_pair,
                data.score.times, scorecard=scorecard, dtype=torch.float64, device=CPU,
                grid=data.score.grid,
            ).E

        recorded = self.override_record["states"]["adam"]["score_gold"]["E"]
        at_60 = rescored_error(
            _omega_builder(self)(60.0, seed=SEED, dtype=torch.float64, device=CPU)
        )
        at_30 = rescored_error(build_arm_network(30.0, dtype=torch.float64, device=CPU))
        scale = max(1.0, abs(recorded))
        self.assertAlmostEqual(at_60, recorded, delta=1e-9 * scale)
        self.assertGreater(abs(at_30 - recorded), 1e-6 * scale)

    def test_arm_directories_hold_only_the_record_and_two_weights_files(self):
        for label, _root, arm_dir, _weights in self._weights_files():
            with self.subTest(record=label):
                self.assertEqual(
                    sorted(path.name for path in arm_dir.iterdir()),
                    ["adam.weights", "polish.weights", "record.json"],
                )

    def test_the_evaluator_refuses_every_weights_file_before_any_claim(self):
        for label, root, arm_dir, weights in self._weights_files():
            with self.subTest(record=label, file=weights.name):
                self.assertTrue(weights.is_file())
                with self.assertRaises(CheckpointOwnershipError):
                    evaluate_run(checkpoint_path=weights, output_dir=arm_dir / "evaluation")
                self.assertEqual(list(root.rglob("evaluation-attempt.json")), [])
                self.assertFalse((arm_dir / "evaluation").exists())

    def test_the_production_checkpoint_store_refuses_every_weights_file(self):
        for label, _root, _arm_dir, weights in self._weights_files():
            with self.subTest(record=label, file=weights.name):
                with tempfile.TemporaryDirectory(prefix="phase60-store-") as raw:
                    store_root = Path(raw)
                    store = TorchSaveCheckpointStore(store_root)
                    # Control: a payload with the seven production keys loads from this
                    # same root, so the refusal below is about the file's content.
                    control = store_root / "stage-0-control.pt"
                    atomic_write_torch(control, _valid_production_payload())
                    self.assertEqual(store.load_checkpoint(control)["schema_version"], CHECKPOINT_SCHEMA_VERSION)
                    inside = store_root / f"{label}-{weights.name}"
                    shutil.copyfile(weights, inside)
                    self.assertTrue(inside.is_file())
                    with self.assertRaises(NoValidCheckpointError):
                        store.load_checkpoint(inside)


class OverrideOrderTests(unittest.TestCase):
    """INST-05(e): an unauthorized setting is refused before anything is read or built."""

    def setUp(self):
        stack = ExitStack()
        self.addCleanup(stack.close)
        self.fixture = stack.enter_context(gold_corpus_fixture())
        self.root = Path(stack.enter_context(tempfile.TemporaryDirectory(prefix="phase60-order-")))

    def _assert_refused_before_anything(self, spec, **run_options):
        refused = _arms_symbol(self, "OverrideRefused")
        with mock.patch.object(
            learnability_run, "build_arm_network", side_effect=AssertionError("network built")
        ) as build, mock.patch.object(
            learnability_run, "load_arm_data", side_effect=AssertionError("data read")
        ) as read:
            with self.assertRaises(refused):
                run_arm(
                    spec,
                    context=_context(self.fixture),
                    scorecard=load_scorecard(),
                    runtime=FIXTURE_RUNTIME,
                    evidence_root=self.root,
                    fixture_budget_steps=5,
                    **run_options,
                )
        self.assertEqual(build.call_count, 0)
        self.assertEqual(read.call_count, 0)
        self.assertEqual(list(self.root.rglob("*")), [])

    def test_a_full_loss_arm_with_a_sweep_override_is_refused(self):
        spec = _fixture_spec(
            self.fixture, loss_arm="full", omega_provenance="g2_sweep_override", grid_omega=60.0
        )
        self._assert_refused_before_anything(spec)

    def test_no_physics_arm_may_carry_a_grid_override(self):
        for loss_arm in ("physics_ic", "full"):
            for provenance in ("g2_sweep_override", "confirmation_override"):
                with self.subTest(loss_arm=loss_arm, provenance=provenance):
                    spec = _fixture_spec(
                        self.fixture, loss_arm=loss_arm, omega_provenance=provenance,
                        grid_omega=60.0,
                    )
                    self._assert_refused_before_anything(spec)

    def test_a_grid_override_without_its_grid_value_is_refused(self):
        spec = _fixture_spec(self.fixture, omega_provenance="g2_sweep_override")
        self._assert_refused_before_anything(spec)

    def test_a_locked_arm_that_carries_a_grid_value_is_refused(self):
        spec = _fixture_spec(self.fixture, grid_omega=60.0)
        self._assert_refused_before_anything(spec)

    def test_an_owner_approved_arm_without_a_ruling_is_refused(self):
        spec = _fixture_spec(self.fixture, omega_provenance="owner_approved")
        self._assert_refused_before_anything(spec)


if __name__ == "__main__":
    unittest.main()
