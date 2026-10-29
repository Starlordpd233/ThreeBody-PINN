"""Phase 65 (INST-08 e, Wave 0 tracer): one synthetic fit-to-score-to-record path.

A tiny fixture orbit from the Phase 60 synthetic corpus takes two finite
constant-rate Adam steps through the named locked-12 diagnostic variant, is
measured by the shared centred-neighbour similarity logger at initialization
and at the final step once each, is scored by the frozen FEAS-01 scorer beside
the window-mean constant and two-Kepler comparisons on the same window, and
publishes one canonical diagnostic record plus an intrinsically marked tensor
payload. No real corpus, dataset resolver, sealed arm runner or admission is
ever reached; the spies prove it.
"""

from __future__ import annotations

import importlib
import shutil
import tempfile
import unittest
from collections import OrderedDict
from contextlib import ExitStack
from pathlib import Path
from types import SimpleNamespace
from unittest import mock

import numpy as np
import torch

from pinn.constants import T_CHARACTERISTIC_TIME
from pinn.training.atomic_io import atomic_write_torch
from pinn.verification import evidence_io, learnability_data, learnability_protocol, learnability_run
from pinn.verification.feasibility_scorecard import load_scorecard
from pinn.verification.feasibility_scorer import score_network, score_trajectory
from pinn.verification.learnability_arms import SEED, FirstResultExists, fixture_arm
from pinn.verification.learnability_data import fixture_context, load_arm_data
from pinn.verification.two_kepler import NotApplicable, two_kepler_prediction
from tests.phase60._fixtures import gold_corpus_fixture

FIXTURE_RUNTIME = ("float64", "cpu")
CPU = torch.device("cpu")
HEX64 = __import__("re").compile(r"[0-9a-f]{64}")


def _module(case, name):
    try:
        return importlib.import_module(f"pinn.verification.{name}")
    except ImportError as exc:  # the module is created by this plan
        case.fail(f"pinn.verification.{name} is missing: {exc}")


def _symbol(case, module, name):
    value = getattr(module, name, None)
    case.assertIsNotNone(value, f"{module.__name__}.{name} is missing")
    return value


class Wave0ModuleTests(unittest.TestCase):
    """The four Phase 65 Wave 0 modules and their planned symbols exist."""

    def test_the_wave0_modules_and_symbols_exist(self):
        variants = _module(self, "diagnostic_variants")
        similarity = _module(self, "diagnostic_similarity")
        fit = _module(self, "diagnostic_fit")
        guard = _module(self, "diagnostic_guard")
        for name in ("DiagnosticVariant", "build_variant", "resolve_variant"):
            _symbol(self, variants, name)
        for name in ("measure_time_signal",):
            _symbol(self, similarity, name)
        for name in ("fit_diagnostic", "log_similarity"):
            _symbol(self, fit, name)
        for name in (
            "DiagnosticArtifactRefused", "require_not_diagnostic",
            "read_diagnostic_record", "read_diagnostic_weights",
        ):
            _symbol(self, guard, name)


def _loaded(fixture):
    """The fixture data seam: an arm spec, context, scorecard and loaded data."""
    spec = fixture_arm(
        train_key=fixture.gold_key,
        score_key=fixture.gold_key,
        beside_key=fixture.base_key,
    )
    context = fixture_context(
        allowlist=fixture.allowlist, reader=fixture.reader, stats=fixture.stats
    )
    scorecard = load_scorecard()
    data = load_arm_data(
        spec, context, scorecard=scorecard, dtype=torch.float64, device=CPU
    )
    return spec, context, scorecard, data


class _FitCase(unittest.TestCase):
    """Base: the tiny synthetic corpus, the fixture data seam and a temp evidence root."""


class ShortFitTests(_FitCase):
    """INST-08(e): one short synthetic diagnostic run, shared by the assertions below."""

    @classmethod
    def setUpClass(cls):
        stack = ExitStack()
        cls.addClassCleanup(stack.close)
        cls.fixture = stack.enter_context(gold_corpus_fixture())
        cls.root = Path(stack.enter_context(tempfile.TemporaryDirectory(prefix="phase65-fit-")))
        cls.spec, cls.context, cls.scorecard, cls.data = _loaded(cls.fixture)
        cls.fit = _module(cls, "diagnostic_fit")
        cls.variants = _module(cls, "diagnostic_variants")
        cls.guard = _module(cls, "diagnostic_guard")
        # The sealed Phase 60 entry points and the real-corpus resolver must never be
        # reached by a diagnostic fit; the spies raise if they are.
        with mock.patch.object(
            learnability_data, "open_real_context", side_effect=AssertionError("resolver")
        ) as cls.resolver_spy, mock.patch.object(
            learnability_run, "run_arm", side_effect=AssertionError("sealed runner")
        ) as cls.run_arm_spy, mock.patch.object(
            learnability_protocol, "admit_arm", side_effect=AssertionError("sealed admission")
        ) as cls.admit_spy:
            cls.record = cls.fit.fit_diagnostic(
                "locked-12",
                cls.data,
                context=cls.context,
                scorecard=cls.scorecard,
                runtime=FIXTURE_RUNTIME,
                evidence_root=cls.root,
                steps=2,
                times_physical=cls.data.score.times,
                seed=SEED,
            )
        cls.run_dir = cls.root / "diagnostics" / "locked-12-hierarchical-gold-0"
        cls.record_bytes = (cls.run_dir / "record.json").read_bytes()

    def _rebuild_final_model(self):
        model = self.variants.build_variant(
            "locked-12", seed=SEED, dtype=torch.float64, device=CPU
        )
        payload = self.guard.read_diagnostic_weights(self.run_dir / "weights.pt")
        model.load_state_dict(payload["state_dict"])
        return model, payload

    def test_record_is_canonical_json_and_matches_what_fit_returned(self):
        self.assertEqual(evidence_io.canonical_json_bytes(self.record), self.record_bytes)

    def test_record_carries_intrinsic_diagnostic_identity(self):
        record = self.record
        self.assertEqual(record["schema"], "inst08-diagnostic/v1")
        self.assertEqual(record["artifact_kind"], "diagnostic")
        self.assertIs(record["diagnostic"], True)
        self.assertIs(record["counted"], False)

    def test_record_names_variant_seed_runtime_and_steps(self):
        record = self.record
        variant = record["variant"]
        self.assertEqual(variant["name"], "locked-12")
        self.assertIs(variant["registered"], True)
        self.assertEqual(variant["depth"], 12)
        self.assertEqual(variant["width"], 256)
        self.assertEqual(variant["time_features"], "raw_tau_ic13")
        self.assertEqual(variant["learning_rate"], 1e-4)
        self.assertEqual(variant["window_length"], 10.0)
        self.assertEqual(record["seed"], SEED)
        self.assertEqual(record["runtime"], {"dtype": "float64", "device": "cpu"})
        self.assertEqual(record["steps"], {"requested": 2, "completed": 2})

    def test_the_two_adam_steps_really_changed_the_weights(self):
        model, payload = self._rebuild_final_model()
        fresh = self.variants.build_variant(
            "locked-12", seed=SEED, dtype=torch.float64, device=CPU
        )
        initial = fresh.state_dict()
        final = payload["state_dict"]
        self.assertEqual(sorted(initial), sorted(final))
        self.assertFalse(all(torch.equal(initial[name], final[name]) for name in initial))
        init_digest = learnability_run.weights_digest(initial)
        self.assertNotEqual(init_digest, self.record["weights"]["tensor_digest"])
        self.assertRegex(self.record["weights"]["sha256"], HEX64)
        self.assertEqual(self.record["weights"]["file"], "weights.pt")

    def test_similarity_covers_initialization_and_the_final_step_once_each(self):
        similarity = self.record["similarity"]
        self.assertEqual(similarity["cadence"], ["init", "final"])
        init, final = similarity["init"], similarity["final"]
        self.assertEqual(init["point"], "init")
        self.assertEqual(init["step"], 0)
        self.assertEqual(final["point"], "final")
        self.assertEqual(final["step"], 2)
        expected_layers = ["input"] + [f"h{index}" for index in range(1, 13)]
        for entry in (init, final):
            self.assertEqual([row["name"] for row in entry["layers"]], expected_layers)
            self.assertEqual(
                [row["order"] for row in entry["layers"]], list(range(len(expected_layers)))
            )
            self.assertEqual(entry["n_points"], int(self.data.data_points.tau_ic13.shape[0]))
            self.assertEqual(len(entry["times_physical"]), entry["n_points"])
            self.assertEqual(len(entry["tau_values"]), entry["n_points"])
            for key in ("output_movement", "output_rate_ratio"):
                self.assertTrue(np.isfinite(entry[key]["value"]), key)
            for key in ("median", "max"):
                self.assertTrue(np.isfinite(entry["first_layer_frequency"][key]), key)
        # The physical spacing of adjacent samples is recorded as physical time, and the
        # normalized-tau spacing is recorded separately (D-05): they are not the same number.
        physical = np.asarray(init["times_physical"], dtype=np.float64)
        tau = np.asarray(init["tau_values"], dtype=np.float64)
        self.assertGreater(init["physical_dt_median"]["value"], 0.0)
        self.assertAlmostEqual(
            init["physical_dt_median"]["value"], float(np.median(np.diff(physical))), places=12
        )
        self.assertNotEqual(
            init["physical_dt_median"]["value"], float(np.median(np.diff(tau)))
        )

    def test_optimizer_block_is_constant_rate_adam_with_no_scheduler_or_physics(self):
        optimizer = self.record["optimizer"]
        self.assertEqual(optimizer["kind"], "adam_constant_rate")
        self.assertEqual(optimizer["lr"], 1e-4)
        self.assertEqual(optimizer["betas"], [0.9, 0.999])
        self.assertEqual(optimizer["eps"], 1e-8)
        self.assertIsNone(optimizer["scheduler"])
        self.assertIsNone(optimizer["physics_term"])
        self.assertIsNone(optimizer["polish"])
        self.assertTrue(self.record["timing"]["basis"].startswith("optimizer steps only"))
        self.assertEqual(self.record["timing"]["completed_steps"], 2)
        self.assertGreater(self.record["timing"]["wall_seconds"], 0.0)
        self.assertEqual(len(self.record["loss"]["trace"]), 2)
        self.assertTrue(np.isfinite(self.record["loss"]["final"]))

    def test_network_score_is_the_entire_frozen_scorer_output(self):
        model, _payload = self._rebuild_final_model()
        direct = score_network(
            model,
            self.data.ic13,
            self.data.masses,
            self.data.score.positions,
            self.data.score.inner_pair,
            self.data.score.times,
            scorecard=self.scorecard,
            dtype=torch.float64,
            device=CPU,
            grid=self.data.score.grid,
        ).to_json_dict()
        self.assertEqual(self.record["scores"]["network"], direct)
        for key in (
            "E", "e_sys_max", "e_in_max", "h", "eps_h", "tier", "velocity_source",
            "grid", "frame", "n_times", "R_sys", "physics_residual_mean",
            "physics_residual_max",
        ):
            self.assertIn(key, direct)
        self.assertEqual(direct["velocity_source"], "autograd")
        self.assertEqual(direct["grid"], "gold")

    def test_comparison_rows_match_direct_recomputation_on_the_same_window(self):
        rows = {row["comparison"]: row for row in self.record["comparisons"]}
        self.assertEqual(sorted(rows), ["two_kepler", "window_mean_constant"])
        view = self.data.score
        positions = np.asarray(view.positions, dtype=np.float64)
        times = np.asarray(view.times, dtype=np.float64)
        masses = np.asarray(self.data.masses, dtype=np.float64)
        inner_pair = tuple(int(slot) for slot in view.inner_pair)
        constant = np.broadcast_to(
            positions.mean(axis=0, keepdims=True), positions.shape
        ).copy()
        direct_constant = score_trajectory(
            constant, np.zeros_like(constant), positions, masses, inner_pair, times,
            velocity_source="analytic", scorecard=self.scorecard, grid=view.grid,
        ).to_json_dict()
        self.assertEqual(rows["window_mean_constant"]["score"], direct_constant)
        self.assertEqual(rows["window_mean_constant"]["predictor"]["velocities"], "zero")
        elapsed = (times - times[0]) / T_CHARACTERISTIC_TIME
        r0 = self.data.true_r0.detach().cpu().numpy().astype(np.float64).reshape(3, 3)
        v0 = self.data.true_v0.detach().cpu().numpy().astype(np.float64).reshape(3, 3)
        try:
            predicted, predicted_v = two_kepler_prediction(r0, v0, masses, inner_pair, elapsed)
        except NotApplicable as exc:
            self.assertIs(rows["two_kepler"].get("applicable"), False)
            self.assertEqual(rows["two_kepler"]["failure"], "not_applicable")
            self.assertEqual(rows["two_kepler"]["reason"], exc.reason)
            self.assertNotIn("score", rows["two_kepler"])
        except RuntimeError as exc:
            # The frozen formula's Newton solver can fail to converge on the
            # synthetic fixture's near-radial geometry; that failure carries its
            # own reason and never becomes a successful score either.
            self.assertIs(rows["two_kepler"].get("applicable"), False)
            self.assertEqual(rows["two_kepler"]["failure"], "solver_did_not_converge")
            self.assertEqual(rows["two_kepler"]["reason"], str(exc))
            self.assertNotIn("score", rows["two_kepler"])
        else:
            self.assertIs(rows["two_kepler"].get("applicable"), True)
            direct_kepler = score_trajectory(
                predicted, predicted_v, positions, masses, inner_pair, times,
                velocity_source="analytic", scorecard=self.scorecard, grid=view.grid,
            ).to_json_dict()
            self.assertEqual(rows["two_kepler"]["score"], direct_kepler)

    def test_the_diagnostic_reader_reads_the_result(self):
        guard = self.guard
        record = guard.read_diagnostic_record(self.run_dir / "record.json")
        self.assertEqual(record, self.record)
        payload = guard.read_diagnostic_weights(self.run_dir / "weights.pt")
        self.assertEqual(payload["schema"], "inst08-diagnostic-weights/v1")
        self.assertIs(payload["diagnostic"], True)
        for tensor in payload["state_dict"].values():
            self.assertEqual(tensor.device.type, "cpu")

    def test_marker_rejection_survives_file_renames_and_relocation(self):
        with tempfile.TemporaryDirectory(prefix="phase65-reloc-") as raw:
            moved = Path(raw)
            json_copy = moved / "run-final.json"
            shutil.copyfile(self.run_dir / "record.json", json_copy)
            weights_copy = moved / "nested" / "model.weights"
            weights_copy.parent.mkdir(parents=True)
            shutil.copyfile(self.run_dir / "weights.pt", weights_copy)
            for path in (json_copy, weights_copy):
                with self.subTest(path=path.name):
                    with self.assertRaises(self.guard.DiagnosticArtifactRefused):
                        self.guard.require_not_diagnostic(path)
            # Control: a bare production-style state dict is not a diagnostic artifact.
            plain = moved / "production.weights"
            state = OrderedDict(
                (name, tensor.detach().cpu().clone())
                for name, tensor in self.variants.build_variant(
                    "locked-12", seed=SEED, dtype=torch.float64, device=CPU
                ).state_dict().items()
            )
            atomic_write_torch(plain, state)
            self.assertIsNone(self.guard.require_not_diagnostic(plain))

    def test_second_fit_is_refused_before_any_optimizer_step(self):
        with mock.patch.object(torch.optim.Adam, "step") as adam_step:
            with self.assertRaises(FirstResultExists):
                self.fit.fit_diagnostic(
                    "locked-12",
                    self.data,
                    context=self.context,
                    scorecard=self.scorecard,
                    runtime=FIXTURE_RUNTIME,
                    evidence_root=self.root,
                    steps=2,
                    times_physical=self.data.score.times,
                    seed=SEED,
                )
        self.assertEqual(adam_step.call_count, 0)
        self.assertEqual((self.run_dir / "record.json").read_bytes(), self.record_bytes)

    def test_no_dataset_resolver_or_sealed_entry_point_was_called(self):
        self.assertEqual(self.resolver_spy.call_count, 0)
        self.assertEqual(self.run_arm_spy.call_count, 0)
        self.assertEqual(self.admit_spy.call_count, 0)

    def test_access_counts_and_source_hashes_are_recorded(self):
        record = self.record
        reads = record["access"]["reads"]
        self.assertEqual(set(reads), {"train", "validation", "refusals"})
        self.assertGreaterEqual(reads["train"], 2)  # the gold and base records of the fixture
        self.assertEqual(reads["validation"], 0)
        sources = record["source_sha256"]
        self.assertEqual(len(sources), 33)
        for digest in sources.values():
            self.assertRegex(digest, HEX64)


class RefusalTests(_FitCase):
    """Typed refusals fire before an optimizer step or any publication."""

    def setUp(self):
        stack = ExitStack()
        self.addCleanup(stack.close)
        self.fixture = stack.enter_context(gold_corpus_fixture())
        self.root = Path(stack.enter_context(tempfile.TemporaryDirectory(prefix="phase65-refuse-")))
        self.spec, self.context, self.scorecard, self.data = _loaded(self.fixture)
        self.fit = _module(self, "diagnostic_fit")
        self.variants = _module(self, "diagnostic_variants")
        self.similarity = _module(self, "diagnostic_similarity")

    def _fit(self, variant="locked-12", data=None, **overrides):
        options = dict(
            context=self.context,
            scorecard=self.scorecard,
            runtime=FIXTURE_RUNTIME,
            evidence_root=self.root,
            steps=2,
            times_physical=self.data.score.times,
            seed=SEED,
        )
        options.update(overrides)
        return self.fit.fit_diagnostic(variant, self.data if data is None else data, **options)

    def _assert_nothing_written(self):
        self.assertEqual(list(self.root.rglob("*")), [])

    def test_null_and_unknown_variants_are_refused(self):
        for bad in (None, "no-such-variant", 7):
            with self.subTest(variant=bad):
                with self.assertRaises(self.variants.VariantRefused):
                    self._fit(variant=bad)
        self._assert_nothing_written()

    def test_bad_step_counts_are_refused(self):
        for bad in (0, -1, 2.5, True, None):
            with self.subTest(steps=bad):
                with self.assertRaises(self.fit.DiagnosticFitRefused):
                    self._fit(steps=bad)
        self._assert_nothing_written()

    def test_empty_and_singleton_inputs_are_refused_before_any_step(self):
        tau = self.data.data_points.tau_ic13
        masses = self.data.data_points.masses
        targets = self.data.data_points.targets
        times = np.asarray(self.data.score.times, dtype=np.float64)
        for count in (0, 1):
            with self.subTest(count=count):
                points = SimpleNamespace(
                    tau_ic13=tau[:count].clone(),
                    masses=masses[:count].clone(),
                    targets=targets[:count].clone(),
                )
                data = SimpleNamespace(
                    data_points=points,
                    score=self.data.score,
                    records=self.data.records,
                )
                with mock.patch.object(torch.optim.Adam, "step") as adam_step:
                    with self.assertRaises(
                        (self.fit.DiagnosticFitRefused, self.similarity.MeasurementRefused)
                    ):
                        self._fit(data=data, times_physical=times[:count])
                self.assertEqual(adam_step.call_count, 0)
        for points in (None, SimpleNamespace(tau_ic13=None, masses=None, targets=None)):
            with self.subTest(points=points):
                data = SimpleNamespace(
                    data_points=points, score=self.data.score, records=self.data.records
                )
                with self.assertRaises(self.fit.DiagnosticFitRefused):
                    self._fit(data=data)
        self._assert_nothing_written()

    def test_zero_target_variation_is_refused(self):
        tau = self.data.data_points.tau_ic13
        masses = self.data.data_points.masses
        flat = self.data.data_points.targets[:1].expand(tau.shape[0], 3, 3)
        points = SimpleNamespace(tau_ic13=tau.clone(), masses=masses.clone(), targets=flat.clone())
        data = SimpleNamespace(
            data_points=points, score=self.data.score, records=self.data.records
        )
        with mock.patch.object(torch.optim.Adam, "step") as adam_step:
            with self.assertRaises(self.similarity.MeasurementRefused):
                self._fit(data=data)
        self.assertEqual(adam_step.call_count, 0)
        self._assert_nothing_written()

    def test_a_non_finite_loss_refuses_before_the_update_and_publishes_nothing(self):
        spoiled = torch.tensor(float("inf"), dtype=torch.float64)
        with mock.patch.object(
            self.fit, "data_only_loss", side_effect=[spoiled]
        ), mock.patch.object(torch.optim.Adam, "step") as adam_step:
            with self.assertRaises(self.fit.DiagnosticFitRefused):
                self._fit()
        self.assertEqual(adam_step.call_count, 0)
        self._assert_nothing_written()


if __name__ == "__main__":
    unittest.main()
