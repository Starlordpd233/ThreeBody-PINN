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

import hashlib
import importlib
import json
import shutil
import tempfile
import time
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
        self.assertEqual(
            record["steps"],
            {"requested": 2, "warmup": 0, "measured": 2, "completed": 2},
        )

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
        self.assertEqual(similarity["cadence"], [0, 2])
        init, final = similarity["entries"]
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


# ---------------------------------------------------------------------------
# Plan 65-06: the guarded real-data CLI, bounded synchronized timing, the
# 600-second whole-run cap and exclusive attempt ownership.
# ---------------------------------------------------------------------------

FIT_REGISTRATION_SCHEMA = "phase65-fit-registration/v1"
ATTEMPT_SCHEMA = "phase65-fit-attempt/v1"


class _InlineQueue:
    """A stand-in for the supervised worker's result queue, in-process."""

    def __init__(self):
        self.payload = None

    def put(self, value):
        self.payload = value


def _sha256_bytes(raw):
    return hashlib.sha256(raw).hexdigest()


def _receipt_bytes(valid=True):
    """A minimal log_similarity receipt (the 65-05 logger-parity shape)."""
    payload = {
        "step": -1,
        "point": "probe-logger-parity",
        "n_points": 1001,
        "layers": [
            {"name": "input", "order": 0, "adjacent_cosine_mean": 0.9993},
            {"name": "h1", "order": 1, "adjacent_cosine_mean": 0.9854},
        ],
        "first_layer_frequency": {"definition": "d", "median": 4.24, "max": 14.88},
        "output_movement": {"definition": "d", "value": 0.0034},
        "output_rate_ratio": {"definition": "d", "value": 4.9e7},
        "times_physical": [0.0, 0.01],
        "tau_values": [-1.0, 1.0],
        "physical_dt_median": {"definition": "d", "value": 0.01},
    }
    if not valid:
        payload.pop("layers")
    return (json.dumps(payload, indent=2) + "\n").encode("utf-8")


def _smoke_settings(**overrides):
    """The registered smoke settings, on the CPU float64 fixture runtime."""
    from pinn.verification.diagnostic_variants import LOCKED_12

    settings = {
        "variant": LOCKED_12.to_json_dict(),
        "seed": 42,
        "runtime": {"dtype": "float64", "device": "cpu"},
        "orbit_key": "hierarchical/gold/0",
        "physical_window": {"t_start": 0.0, "t_end": 10.0},
        "optimizer_steps": 20,
        "warmup_steps": 2,
        "measured_steps": 18,
        "similarity_cadence": [0, 5, 10, 15, 20],
        "whole_run_cap_seconds": 600,
        "optimizer": {
            "kind": "adam_constant_rate",
            "lr": 1e-4,
            "scheduler": None,
            "clipping": None,
            "physics_term": None,
            "polish": None,
        },
        "loss": {"kind": "data_only"},
        "timing_definitions": (
            "synchronized completed-work segments around setup, the 2 warmup "
            "updates, the 18 measured updates, similarity logging and scoring"
        ),
        "reading_rule": {
            "mechanical_pass": "all 20 finite steps, five cadence entries, scores and comparisons present",
            "incomplete": "an interrupted or over-cap attempt stays incomplete and is never a result",
            "out_of_branch": "no E/tier threshold and no expected improvement is imposed",
        },
    }
    settings.update(overrides)
    return settings


def _fit_registration_fixture(root, kind="matching", settings_extra=None, receipt_raw=None):
    """A minimal committed fit registration inside a throwaway git repository.

    ``kind`` selects the broken variant: matching, missing (an artifact is
    deleted), untracked (the registration file is never committed), staged_only
    (added but uncommitted), dirty (modified after commit), changed_dependency
    (a listed code dependency changes content after the registration commit),
    receipt_tampered (the receipt changes after the registration commit),
    receipt_invalid (the receipt is committed but is not a measurement),
    receipt_after_run (the receipt is first committed after the recorded run
    commit, byte-faithful to its publication — the 65-05 shape, which admits),
    run_commit_bytes_differ (the receipt changed after its own introduction)
    and run_commit_not_ancestor (the recorded run commit does not exist).
    """
    import subprocess

    def git(*args, check=True):
        return subprocess.run(
            ["git", *args], cwd=str(root), capture_output=True, text=True, check=check
        )

    root.mkdir(parents=True, exist_ok=True)
    git("init", "-q")
    git("config", "user.email", "fixture@example.com")
    git("config", "user.name", "fixture")
    git("config", "maintenance.auto", "false")
    git("config", "gc.auto", "0")

    reg = root / "reg"
    reg.mkdir()
    page_raw = b"# fixture smoke prediction page\n"
    probe_raw = b'{"schema": "probe-result-stand-in", "reading_rule": {"verdict": "retained"}}\n'
    dep_raw = b"FIT_DEPENDENCY = 1\n"
    frozen_raw = b"FROZEN = True\n"
    receipt = _receipt_bytes(valid=(kind != "receipt_invalid")) if receipt_raw is None else receipt_raw
    (reg / "PREDICTION.md").write_bytes(page_raw)
    (reg / "probe-result.json").write_bytes(probe_raw)
    (reg / "logger-parity.json").write_bytes(receipt)
    (root / "fit_dep.py").write_bytes(dep_raw)
    frozen = root / "frozen"
    frozen.mkdir()
    (frozen / "scorer.py").write_bytes(frozen_raw)

    def entry(rel, raw):
        return {"path": rel, "sha256": _sha256_bytes(raw)}

    # Commit the probe-run evidence first: the receipt's recorded run commit
    # must be a real ancestor of everything that follows. For
    # receipt_after_run the receipt is first committed AFTER that run commit
    # (the 65-05 provenance shape), byte-faithful from its introduction on.
    # For run_commit_bytes_differ the receipt is changed (and committed
    # again) after its introduction, so the committed bytes differ from the
    # receipt's bytes at its introducing commit.
    evidence_paths = ["reg/PREDICTION.md", "reg/probe-result.json",
                      "fit_dep.py", "frozen/scorer.py"]
    if kind != "receipt_after_run":
        evidence_paths.append("reg/logger-parity.json")
    git("add", *evidence_paths)
    git("commit", "-q", "-m", "fixture evidence as produced by the probe run")
    run_commit = git("rev-parse", "HEAD").stdout.strip()
    if kind == "receipt_after_run":
        git("add", "reg/logger-parity.json")
        git("commit", "-q", "-m", "receipt materialized from the run's recorded entry")
        run_commit = git("rev-parse", "HEAD~1").stdout.strip()
    if kind == "run_commit_bytes_differ":
        changed = _receipt_bytes() + b"# regenerated\n"
        (reg / "logger-parity.json").write_bytes(changed)
        git("add", "reg/logger-parity.json")
        git("commit", "-q", "-m", "receipt regenerated after the run")
        receipt = changed

    settings = _smoke_settings(**(settings_extra or {}))
    doc = {
        "schema": FIT_REGISTRATION_SCHEMA,
        "title": "fixture smoke registration",
        "committed_before": "the first real optimizer step",
        "page": entry("reg/PREDICTION.md", page_raw),
        "settings": settings,
        "logger_parity": {
            "receipt": entry("reg/logger-parity.json", receipt),
            "run_commit": (
                "0" * 64 if kind == "run_commit_not_ancestor" else run_commit
            ),
            "arm": "r1-1632",
            "state": "polish",
        },
        "context": {
            "probe_result": entry("reg/probe-result.json", probe_raw),
            "probe_verdict": "retained",
            "note": "the retained lead is recorded, not required",
        },
        "code_dependencies": [entry("fit_dep.py", dep_raw)],
        "frozen": [entry("frozen/scorer.py", frozen_raw)],
    }
    registration_raw = (json.dumps(doc, indent=2) + "\n").encode("utf-8")
    (reg / "smoke-registration.json").write_bytes(registration_raw)

    if kind == "untracked":
        return root
    if kind == "staged_only":
        git("add", "reg/smoke-registration.json")
        return root
    git("add", "reg/smoke-registration.json")
    git("commit", "-q", "-m", "fixture registration")
    commit = git("rev-parse", "HEAD").stdout.strip()

    if kind == "missing":
        (reg / "PREDICTION.md").unlink()
    elif kind == "dirty":
        (reg / "smoke-registration.json").write_bytes(registration_raw + b"# drifted\n")
    elif kind == "changed_dependency":
        (root / "fit_dep.py").write_bytes(b"FIT_DEPENDENCY = 2\n")
        git("add", "fit_dep.py")
        git("commit", "-q", "-m", "change the dependency after registration")
    elif kind == "receipt_tampered":
        (reg / "logger-parity.json").write_bytes(_receipt_bytes() + b"# tampered\n")
        git("add", "reg/logger-parity.json")
        git("commit", "-q", "-m", "tamper the receipt after registration")
    return root, commit


def _fit_symbols(case):
    fit = _module(case, "diagnostic_fit")
    return fit, {
        "admission": _symbol(case, fit, "require_committed_smoke_registration"),
        "check": _symbol(case, fit, "check_fit_registration"),
        "verify": _symbol(case, fit, "verify_fit_result"),
        "run_smoke": _symbol(case, fit, "run_registered_smoke"),
        "worker": _symbol(case, fit, "_smoke_worker"),
        "supervised": _symbol(case, fit, "_run_supervised"),
        "main": _symbol(case, fit, "main"),
    }


class _NoDataNoOptimizer:
    """Spies that fail the test the moment data is resolved or Adam steps.

    Both the fit module's own imported references and the data module's
    definitions are patched, so the spy holds however the admission reaches
    the seam.
    """

    def __call__(self, case):
        import pinn.verification.diagnostic_data as diagnostic_data

        stack = ExitStack()
        for module in (case.fit, diagnostic_data):
            stack.enter_context(mock.patch.object(
                module, "open_diagnostic_context", create=True,
                side_effect=AssertionError("diagnostic context opened"),
            ))
            stack.enter_context(mock.patch.object(
                module, "load_diagnostic_data", create=True,
                side_effect=AssertionError("corpus data loaded"),
            ))
            stack.enter_context(mock.patch.object(
                module, "one_orbit_spec", create=True,
                side_effect=AssertionError("orbit spec built"),
            ))
        stack.enter_context(mock.patch.object(
            torch.optim.Adam, "step", side_effect=AssertionError("optimizer stepped"),
        ))
        return stack


class FitRegistrationAdmissionTests(unittest.TestCase):
    """The fit registration admission: committed-clean settings, parity receipt —
    all before any data access or optimizer construction."""

    def setUp(self):
        self.stack = ExitStack()
        self.addCleanup(self.stack.close)
        self.tmp = Path(self.stack.enter_context(
            tempfile.TemporaryDirectory(prefix="phase65-fitreg-")
        ))
        self.fit, self.symbols = _fit_symbols(self)
        self.guard = _module(self, "diagnostic_guard")
        self.nodata = self.stack.enter_context(_NoDataNoOptimizer()(self))

    def test_a_committed_matching_registration_admits(self):
        root, commit = _fit_registration_fixture(self.tmp / "ok")
        admitted_root, doc = self.symbols["admission"](
            root / "reg/smoke-registration.json", repo_root=root
        )
        self.assertEqual(admitted_root, root.resolve())
        self.assertEqual(doc["schema"], FIT_REGISTRATION_SCHEMA)
        self.assertEqual(doc["settings"]["optimizer_steps"], 20)

    def test_absent_untracked_staged_and_dirty_registrations_refuse_before_any_access(self):
        for kind in ("missing", "untracked", "staged_only", "dirty"):
            with self.subTest(kind=kind):
                branch = self.tmp / kind
                _fit_registration_fixture(branch, kind=kind)
                with self.assertRaises(self.guard.DiagnosticRegistrationRefused):
                    self.symbols["admission"](
                        branch / "reg/smoke-registration.json", repo_root=branch
                    )

    def test_a_changed_code_dependency_refuses_before_any_access(self):
        root, _commit = _fit_registration_fixture(self.tmp / "dep", kind="changed_dependency")
        with self.assertRaises(self.guard.DiagnosticRegistrationRefused):
            self.symbols["admission"](root / "reg/smoke-registration.json", repo_root=root)

    def test_a_tampered_parity_receipt_refuses_before_any_access(self):
        root, _commit = _fit_registration_fixture(self.tmp / "tamper", kind="receipt_tampered")
        with self.assertRaises(self.guard.DiagnosticRegistrationRefused):
            self.symbols["admission"](root / "reg/smoke-registration.json", repo_root=root)

    def test_a_receipt_that_is_not_a_measurement_refuses(self):
        root, _commit = _fit_registration_fixture(self.tmp / "invalid", kind="receipt_invalid")
        with self.assertRaises(self.fit.DiagnosticFitRefused):
            self.symbols["admission"](root / "reg/smoke-registration.json", repo_root=root)

    def test_a_receipt_first_published_after_the_run_commit_admits(self):
        # The 65-05 provenance shape: the receipt was materialized from the
        # run's recorded entry after the run commit; it admits when it is
        # byte-faithful from its own introduction onward.
        root, _commit = _fit_registration_fixture(
            self.tmp / "after-run", kind="receipt_after_run"
        )
        _root, doc = self.symbols["admission"](
            root / "reg/smoke-registration.json", repo_root=root
        )
        self.assertEqual(doc["logger_parity"]["arm"], "r1-1632")

    def test_receipt_bytes_changed_since_the_run_commit_refuse(self):
        root, _commit = _fit_registration_fixture(
            self.tmp / "runcode", kind="run_commit_bytes_differ"
        )
        with self.assertRaises(self.fit.DiagnosticFitRefused):
            self.symbols["admission"](root / "reg/smoke-registration.json", repo_root=root)

    def test_a_run_commit_that_is_not_an_ancestor_refuses(self):
        root, _commit = _fit_registration_fixture(
            self.tmp / "noancestor", kind="run_commit_not_ancestor"
        )
        with self.assertRaises(self.fit.DiagnosticFitRefused):
            self.symbols["admission"](root / "reg/smoke-registration.json", repo_root=root)

    def test_cap_at_or_above_one_hour_refuses_before_any_access(self):
        for cap in (3600, 7200):
            with self.subTest(cap=cap):
                root, _commit = _fit_registration_fixture(
                    self.tmp / f"cap{cap}",
                    settings_extra={"whole_run_cap_seconds": cap},
                )
                with self.assertRaises(self.fit.DiagnosticFitRefused):
                    self.symbols["admission"](
                        root / "reg/smoke-registration.json", repo_root=root
                    )

    def test_a_cap_below_the_hour_boundary_passes_the_cap_gate(self):
        root, _commit = _fit_registration_fixture(
            self.tmp / "cap-ok", settings_extra={"whole_run_cap_seconds": 3599.5}
        )
        _root, doc = self.symbols["admission"](
            root / "reg/smoke-registration.json", repo_root=root
        )
        self.assertEqual(doc["settings"]["whole_run_cap_seconds"], 3599.5)

    def test_inconsistent_settings_refuse_before_any_access(self):
        cases = {
            "duplicate_cadence": {"similarity_cadence": [0, 5, 5, 15, 20]},
            "cadence_misses_steps": {"similarity_cadence": [0, 5, 10, 15]},
            "cadence_beyond_steps": {"similarity_cadence": [0, 5, 10, 15, 21]},
            "warmup_ge_steps": {"warmup_steps": 20},
            "unknown_variant": {"variant": {**_smoke_settings()["variant"], "name": "no-such"}},
            "variant_field_drift": {"variant": {**_smoke_settings()["variant"], "width": 128}},
            "window_drift": {"physical_window": {"t_start": 0.0, "t_end": 9.0}},
            "measured_mismatch": {"measured_steps": 17},
            "clipping_enabled": {"optimizer": {**_smoke_settings()["optimizer"], "clipping": 8.5}},
            "scheduler_enabled": {"optimizer": {**_smoke_settings()["optimizer"], "scheduler": "cosine"}},
            "missing_reading_rule": {"reading_rule": None},
            "bad_orbit_key": {"orbit_key": "hierarchical/gold"},
        }
        for name, extra in cases.items():
            with self.subTest(case=name):
                root, _commit = _fit_registration_fixture(
                    self.tmp / name, settings_extra=extra
                )
                with self.assertRaises(self.fit.DiagnosticFitRefused):
                    self.symbols["admission"](
                        root / "reg/smoke-registration.json", repo_root=root
                    )

    def test_an_mps_registration_without_mps_refuses_before_any_access(self):
        root, _commit = _fit_registration_fixture(
            self.tmp / "mps",
            settings_extra={"runtime": {"dtype": "float32", "device": "mps"}},
        )
        with mock.patch("torch.backends.mps.is_available", return_value=False):
            with self.assertRaises(self.fit.DiagnosticFitRefused):
                self.symbols["admission"](
                    root / "reg/smoke-registration.json", repo_root=root
                )

    def test_an_mps_registration_with_mps_available_passes_the_runtime_gate(self):
        root, _commit = _fit_registration_fixture(
            self.tmp / "mps-ok",
            settings_extra={"runtime": {"dtype": "float32", "device": "mps"}},
        )
        with mock.patch("torch.backends.mps.is_available", return_value=True):
            _root, doc = self.symbols["admission"](
                root / "reg/smoke-registration.json", repo_root=root
            )
        self.assertEqual(doc["settings"]["runtime"]["device"], "mps")


class FitCheckRegistrationTests(unittest.TestCase):
    """check-registration is metadata-only: a real ancestor commit, no corpus
    opens and no weight reads."""

    def setUp(self):
        self.stack = ExitStack()
        self.addCleanup(self.stack.close)
        self.tmp = Path(self.stack.enter_context(
            tempfile.TemporaryDirectory(prefix="phase65-fitcheck-")
        ))
        self.fit, self.symbols = _fit_symbols(self)
        self.guard = _module(self, "diagnostic_guard")

    def test_a_committed_registration_reports_a_real_ancestor_commit(self):
        root, commit = _fit_registration_fixture(self.tmp / "ok")
        with mock.patch.object(
            self.guard, "read_diagnostic_weights",
            side_effect=AssertionError("weight bytes read"),
        ), mock.patch.object(
            self.fit, "open_diagnostic_context",
            side_effect=AssertionError("diagnostic context opened"),
            create=True,
        ):
            report = self.symbols["check"](
                root / "reg/smoke-registration.json", repo_root=root
            )
        self.assertTrue(report["committed"])
        self.assertEqual(report["registration_commit"], commit)
        self.assertGreaterEqual(len(report["artifacts"]), 4)

    def test_an_uncommitted_registration_refuses(self):
        root = _fit_registration_fixture(self.tmp / "untracked", kind="untracked")
        with self.assertRaises(self.guard.DiagnosticRegistrationRefused):
            self.symbols["check"](root / "reg/smoke-registration.json", repo_root=root)


class BoundedSynchronizedTimingTests(unittest.TestCase):
    """The bounded fit: 2 warmup + measured split, exact cadence, synchronized
    segments with recorded overhead, and deadline refusals."""

    def setUp(self):
        stack = ExitStack()
        self.addCleanup(stack.close)
        self.fixture = stack.enter_context(gold_corpus_fixture())
        self.root = Path(stack.enter_context(
            tempfile.TemporaryDirectory(prefix="phase65-bounded-")
        ))
        self.spec, self.context, self.scorecard, self.data = _loaded(self.fixture)
        self.fit = _module(self, "diagnostic_fit")

    def _bounded_fit(self, *, steps=20, warmup=2, cadence=(0, 5, 10, 15, 20), **overrides):
        options = dict(
            context=self.context,
            scorecard=self.scorecard,
            runtime=FIXTURE_RUNTIME,
            evidence_root=self.root,
            steps=steps,
            warmup_steps=warmup,
            cadence=list(cadence),
            times_physical=self.data.score.times,
            seed=SEED,
        )
        options.update(overrides)
        return self.fit.fit_diagnostic("locked-12", self.data, **options)

    def test_the_measured_rate_denominator_is_the_measured_steps_only(self):
        record = self._bounded_fit()
        timing = record["timing"]
        self.assertEqual(
            timing["steps"],
            {"requested": 20, "warmup": 2, "measured": 18, "completed": 20},
        )
        self.assertAlmostEqual(
            timing["seconds_per_step"],
            timing["measured_seconds"] / 18,
            places=12,
        )
        # The denominator must not be the 20 requested steps.
        self.assertNotAlmostEqual(
            timing["seconds_per_step"], timing["measured_seconds"] / 20, places=6
        )
        self.assertGreater(timing["warmup_seconds"], 0.0)
        self.assertGreater(timing["measured_seconds"], 0.0)
        self.assertLess(timing["measured_seconds"], timing["wall_seconds"])
        self.assertAlmostEqual(
            timing["end_to_end_seconds_per_completed_step"],
            timing["total_wall_seconds"] / 20,
            places=12,
        )
        self.assertIn("warmup", timing["seconds_per_step_basis"])
        self.assertIn("not steady-state", timing["seconds_per_step_basis"])

    def test_the_five_cadence_entries_are_exactly_the_registered_steps(self):
        record = self._bounded_fit()
        similarity = record["similarity"]
        self.assertEqual(similarity["cadence"], [0, 5, 10, 15, 20])
        entries = similarity["entries"]
        self.assertEqual([entry["step"] for entry in entries], [0, 5, 10, 15, 20])
        self.assertEqual(len({entry["step"] for entry in entries}), 5)
        self.assertEqual(entries[0]["point"], "init")
        self.assertEqual(entries[-1]["point"], "final")
        for entry in entries:
            self.assertTrue(entry["layers"])
            self.assertTrue(np.isfinite(entry["output_movement"]["value"]))

    def test_synchronization_rides_every_timed_segment_and_is_recorded(self):
        from pinn.verification.learnability_run import _synchronize as real_sync

        with mock.patch.object(
            self.fit, "_synchronize", wraps=real_sync
        ) as sync_spy:
            record = self._bounded_fit(steps=4, warmup=2, cadence=[0, 4])
        timing = record["timing"]
        # Two boundary syncs per update, plus the phase boundaries.
        self.assertGreaterEqual(sync_spy.call_count, 2 * 4 + 2)
        self.assertEqual(timing["sync"]["sample_count"], sync_spy.call_count)
        self.assertGreaterEqual(timing["sync"]["overhead_seconds"], 0.0)
        self.assertEqual(
            timing["steps"],
            {"requested": 4, "warmup": 2, "measured": 2, "completed": 4},
        )

    def test_phase_seconds_are_recorded_separately(self):
        record = self._bounded_fit(steps=4, warmup=2, cadence=[0, 4])
        phases = record["timing"]["phases"]
        for name in ("setup_seconds", "logging_seconds", "scoring_seconds", "publish_seconds"):
            self.assertIn(name, phases)
            self.assertGreaterEqual(phases[name], 0.0)
        self.assertGreater(phases["logging_seconds"], 0.0)
        self.assertGreater(phases["scoring_seconds"], 0.0)

    def test_an_expired_deadline_refuses_between_updates_and_publishes_nothing(self):
        import pinn.verification.diagnostic_fit as fit_module

        real_loss = fit_module.data_only_loss

        def slow_loss(*args, **kwargs):
            time.sleep(0.05)
            return real_loss(*args, **kwargs)

        with mock.patch.object(fit_module, "data_only_loss", side_effect=slow_loss):
            with mock.patch.object(torch.optim.Adam, "step") as adam_step:
                with self.assertRaises(self.fit.DiagnosticFitRefused):
                    self._bounded_fit(steps=4, warmup=0, cadence=[0, 4], deadline_seconds=0.05)
        self.assertLessEqual(adam_step.call_count, 1)
        self.assertEqual(list(self.root.rglob("*")), [])

    def test_a_deadline_at_or_above_one_hour_is_refused(self):
        with self.assertRaises(self.fit.DiagnosticFitRefused):
            self._bounded_fit(steps=2, warmup=0, cadence=[0, 2], deadline_seconds=3600)
        self.assertEqual(list(self.root.rglob("*")), [])

    def test_a_mid_run_non_finite_loss_stays_incomplete_and_publishes_nothing(self):
        import pinn.verification.diagnostic_fit as fit_module

        real_loss = fit_module.data_only_loss
        calls = {"n": 0}

        def flaky_loss(*args, **kwargs):
            calls["n"] += 1
            if calls["n"] >= 2:
                return torch.tensor(float("inf"), dtype=torch.float64)
            return real_loss(*args, **kwargs)

        with mock.patch.object(fit_module, "data_only_loss", side_effect=flaky_loss):
            with mock.patch.object(torch.optim.Adam, "step") as adam_step:
                with self.assertRaises(self.fit.DiagnosticFitRefused):
                    self._bounded_fit(steps=4, warmup=2, cadence=[0, 4])
        self.assertLessEqual(adam_step.call_count, 1)
        self.assertEqual(list(self.root.rglob("*")), [])


class AttemptOwnershipTests(unittest.TestCase):
    """Exclusive attempt ownership: one claim, refusals on repeats, incomplete
    status retained on failure, and a supervised worker with graceful timeout."""

    def setUp(self):
        stack = ExitStack()
        self.addCleanup(stack.close)
        self.fixture = stack.enter_context(gold_corpus_fixture())
        self.tmp = Path(stack.enter_context(
            tempfile.TemporaryDirectory(prefix="phase65-attempt-")
        ))
        self.spec, self.context, self.scorecard, self.data = _loaded(self.fixture)
        self.fit, self.symbols = _fit_symbols(self)

    def _registration(self, name, **settings_extra):
        root, commit = _fit_registration_fixture(
            self.tmp / name, settings_extra=settings_extra or None
        )
        return root, root / "reg/smoke-registration.json"

    def _patched_data(self):
        """Route the run body to the fixture data seam: no corpus, no resolver."""
        import pinn.verification.diagnostic_data as diagnostic_data

        stack = ExitStack()
        for module in (self.fit, diagnostic_data):
            stack.enter_context(mock.patch.object(
                module, "open_diagnostic_context", create=True,
                return_value=self.context,
            ))
            stack.enter_context(mock.patch.object(
                module, "load_diagnostic_data", create=True,
                return_value=self.data,
            ))
            stack.enter_context(mock.patch.object(
                module, "one_orbit_spec", create=True, return_value=self.spec,
            ))
        self.addCleanup(stack.close)
        return stack

    def test_a_registered_run_publishes_once_and_marks_the_attempt(self):
        root, registration = self._registration("run-ok")
        self._patched_data()
        output = self.tmp / "out" / "record.json"
        summary = self.symbols["run_smoke"](registration, output, repo_root=root)
        self.assertEqual(summary["status"], "complete")
        record = json.loads(output.read_bytes())
        self.assertEqual(record["status"], "complete")
        self.assertEqual(record["steps"]["completed"], 20)
        attempt = json.loads((output.parent / "attempt.json").read_bytes())
        self.assertEqual(attempt["status"], "published")
        # A second attempt refuses before any optimizer step, and the first
        # record is never replaced.
        first_bytes = output.read_bytes()
        with mock.patch.object(torch.optim.Adam, "step") as adam_step:
            with self.assertRaises(
                (self.fit.DiagnosticFitRefused, FirstResultExists)
            ):
                self.symbols["run_smoke"](registration, output, repo_root=root)
        self.assertEqual(adam_step.call_count, 0)
        self.assertEqual(output.read_bytes(), first_bytes)

    def test_a_refusing_run_marks_the_attempt_incomplete_and_never_publishes(self):
        import pinn.verification.diagnostic_data as diagnostic_data

        root, registration = self._registration("run-refused")
        stack = ExitStack()
        self.addCleanup(stack.close)
        for module in (self.fit, diagnostic_data):
            stack.enter_context(mock.patch.object(
                module, "open_diagnostic_context", create=True,
                return_value=self.context,
            ))
            stack.enter_context(mock.patch.object(
                module, "load_diagnostic_data", create=True,
                side_effect=self.fit.DiagnosticFitRefused("corpus refused"),
            ))
        output = self.tmp / "out2" / "record.json"
        with self.assertRaises(self.fit.DiagnosticFitRefused):
            self.symbols["run_smoke"](registration, output, repo_root=root)
        self.assertFalse(output.exists())
        attempt = json.loads((output.parent / "attempt.json").read_bytes())
        self.assertEqual(attempt["status"], "incomplete")
        self.assertIn("corpus refused", attempt["reason"])

    def test_the_worker_reports_refusals_and_marks_the_attempt_incomplete(self):
        root, registration = self._registration("worker")
        doc = json.loads(registration.read_bytes())
        output = self.tmp / "out3" / "record.json"
        queue = mock.MagicMock()
        with mock.patch.object(
            self.fit, "require_committed_smoke_registration",
            return_value=(root, doc),
        ), mock.patch.object(
            self.fit, "open_diagnostic_context", create=True,
            return_value=self.context,
        ), mock.patch.object(
            self.fit, "one_orbit_spec", create=True, return_value=self.spec,
        ), mock.patch.object(
            self.fit, "load_diagnostic_data",
            side_effect=self.fit.DiagnosticFitRefused("corpus refused"),
        ):
            self.symbols["worker"](str(registration), str(output), str(root), queue)
        attempt = json.loads((output.parent / "attempt.json").read_bytes())
        self.assertEqual(attempt["status"], "incomplete")
        self.assertIn("corpus refused", attempt["reason"])
        self.assertFalse(output.exists())
        self.assertTrue(queue.put.called)

    def test_a_supervised_worker_is_terminated_at_the_timeout(self):
        done = []

        def sleeping_worker(*args):
            time.sleep(30)
            done.append(True)

        started = time.monotonic()
        status, payload = self.symbols["supervised"](
            sleeping_worker, (), timeout=0.5, context_method="fork"
        )
        elapsed = time.monotonic() - started
        self.assertEqual(status, "timeout")
        self.assertIsNone(payload)
        self.assertFalse(done)
        self.assertLess(elapsed, 15.0)

    def test_a_completing_worker_reports_its_payload(self):
        def quick_worker(*args):
            args[-1].put({"status": "complete", "completed_steps": 20})

        status, payload = self.symbols["supervised"](
            quick_worker, (), timeout=10.0, context_method="fork"
        )
        self.assertEqual(status, "exited")
        self.assertEqual(payload["status"], "complete")

    def test_a_repeated_cli_run_refuses_before_the_worker_body_runs_again(self):
        root, registration = self._registration("cli-dup")
        self._patched_data()
        output = self.tmp / "cli-dup-out" / "record.json"

        def inline_supervisor(target, args, *, timeout, **kwargs):
            queue = _InlineQueue()
            target(*args, queue)
            return ("exited", queue.payload)

        first = self.symbols["main"](
            ["run", "--registration", str(registration), "--output", str(output)],
            repo_root=root, supervisor=inline_supervisor,
        )
        self.assertEqual(first, 0)
        with mock.patch.object(torch.optim.Adam, "step") as adam_step:
            second = self.symbols["main"](
                ["run", "--registration", str(registration), "--output", str(output)],
                repo_root=root, supervisor=inline_supervisor,
            )
        self.assertEqual(second, 2)
        self.assertEqual(adam_step.call_count, 0)

    def test_a_cli_timeout_marks_the_attempt_incomplete(self):
        root, registration = self._registration("cli-timeout", whole_run_cap_seconds=1)
        output = self.tmp / "cli-timeout-out" / "record.json"
        with mock.patch.object(
            self.fit, "run_registered_smoke",
            side_effect=lambda *a, **k: time.sleep(30),
        ):
            code = self.symbols["main"](
                ["run", "--registration", str(registration), "--output", str(output)],
                repo_root=root, context_method="fork",
            )
        self.assertEqual(code, 2)
        self.assertFalse(output.exists())
        attempt = json.loads((output.parent / "attempt.json").read_bytes())
        self.assertEqual(attempt["status"], "incomplete")
        self.assertIn("wall_cap_expired", attempt["reason"])


class VerifyResultTests(unittest.TestCase):
    """verify-result re-checks an existing record against the committed
    registration without retraining or opening the corpus."""

    def setUp(self):
        stack = ExitStack()
        self.addCleanup(stack.close)
        self.fixture = stack.enter_context(gold_corpus_fixture())
        self.tmp = Path(stack.enter_context(
            tempfile.TemporaryDirectory(prefix="phase65-verify-")
        ))
        self.spec, self.context, self.scorecard, self.data = _loaded(self.fixture)
        # The verify gate requires access evidence: give the fixture context a
        # summary-capable attestation and a Stage-0 style reader summary.
        if self.context.attestation is None:
            fake_attestation = SimpleNamespace(
                summary=lambda: {"test_split_opens": 0, "withheld_refusals": 0}
            )
            self.context = SimpleNamespace(
                **{**vars(self.context), "attestation": fake_attestation}
            )
        if not hasattr(self.context.reader, "access_summary"):
            self.context.reader.access_summary = lambda: {
                "requested": [], "opened": [], "refused_before_open": 0,
                "actual_opens": 1,
            }
        self.fit, self.symbols = _fit_symbols(self)

    def _registration(self, name, **settings_extra):
        root, commit = _fit_registration_fixture(
            self.tmp / name, settings_extra=settings_extra or None
        )
        return root, root / "reg/smoke-registration.json", commit

    def _record(self, out_dir, registration_path, root):
        model_root = self.tmp / "evidence"
        doc = json.loads(registration_path.read_bytes())
        record = self.fit.fit_diagnostic(
            "locked-12",
            self.data,
            context=self.context,
            scorecard=self.scorecard,
            runtime=FIXTURE_RUNTIME,
            evidence_root=model_root,
            out_dir=out_dir,
            steps=20,
            warmup_steps=2,
            cadence=[0, 5, 10, 15, 20],
            times_physical=self.data.score.times,
            seed=SEED,
            registration_provenance={
                "path": registration_path.relative_to(root).as_posix(),
                "sha256": _sha256_bytes(registration_path.read_bytes()),
            },
            logger_parity_provenance={
                "receipt_path": doc["logger_parity"]["receipt"]["path"],
                "receipt_sha256": doc["logger_parity"]["receipt"]["sha256"],
                "run_commit": doc["logger_parity"]["run_commit"],
            },
        )
        return record

    def test_a_complete_agreeing_record_verifies(self):
        root, registration, _commit = self._registration("verify-ok")
        out_dir = self.tmp / "result"
        self._record(out_dir, registration, root)
        report = self.symbols["verify"](registration, out_dir / "record.json", repo_root=root)
        self.assertTrue(report["verified"])

    def test_tampered_weights_refuse_verification(self):
        root, registration, _commit = self._registration("verify-tamper")
        out_dir = self.tmp / "result-tamper"
        self._record(out_dir, registration, root)
        weights_path = out_dir / "weights.pt"
        weights_path.write_bytes(weights_path.read_bytes() + b"# tampered\n")
        with self.assertRaises(self.fit.DiagnosticFitRefused):
            self.symbols["verify"](registration, out_dir / "record.json", repo_root=root)

    def test_a_step_count_disagreement_refuses_verification(self):
        root, registration, _commit = self._registration(
            "verify-steps", optimizer_steps=19, measured_steps=17
        )
        out_dir = self.tmp / "result-steps"
        self._record(out_dir, registration, root)
        with self.assertRaises(self.fit.DiagnosticFitRefused):
            self.symbols["verify"](registration, out_dir / "record.json", repo_root=root)

    def test_a_missing_timing_field_refuses_verification(self):
        root, registration, _commit = self._registration("verify-timing")
        out_dir = self.tmp / "result-timing"
        self._record(out_dir, registration, root)
        record = json.loads((out_dir / "record.json").read_bytes())
        del record["timing"]["seconds_per_step"]
        (out_dir / "record.json").write_bytes(
            (json.dumps(record, indent=2, sort_keys=True) + "\n").encode("utf-8")
        )
        with self.assertRaises(self.fit.DiagnosticFitRefused):
            self.symbols["verify"](registration, out_dir / "record.json", repo_root=root)


class FitCliSurfaceTests(unittest.TestCase):
    """The diagnostic_fit command line: check-registration / run / verify-result
    with their required flags; unknown commands and missing flags refuse."""

    def setUp(self):
        self.fit, self.symbols = _fit_symbols(self)

    def test_unknown_and_missing_commands_refuse(self):
        for argv in ([], ["bogus"], ["--registration", "x"]):
            with self.subTest(argv=argv):
                self.assertEqual(self.symbols["main"](argv), 2)

    def test_each_command_requires_its_flags(self):
        cases = [
            ["check-registration"],
            ["run"],
            ["run", "--registration", "r"],
            ["verify-result"],
            ["verify-result", "--registration", "r"],
        ]
        for argv in cases:
            with self.subTest(argv=argv):
                self.assertEqual(self.symbols["main"](argv), 2)


if __name__ == "__main__":
    unittest.main()
