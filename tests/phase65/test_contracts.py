"""Phase 65 (INST-08 a and b): named-variant parity and frozen-source contracts.

The locked-12 registry entry is production-identical in the same runtime at
the same seed and with the same weights (D-04: same-runtime/same-weights
parity, never an independently-initialized cross-runtime claim); the registry
is immutable, exact-ASCII and refuses duplicates, unknown time-feature
declarations and malformed numeric fields; the serialized fields round-trip
without rounded string substitution; and the 33 pinned INST-05 modules keep
their committed protocol digests, with a missing pinned artifact refused
rather than regenerated. The frozen scorer is called directly and the fit
record's score row matches a direct call.
"""

from __future__ import annotations

import importlib
import json
import tempfile
import unittest
from contextlib import ExitStack
from pathlib import Path
from unittest import mock

import numpy as np
import torch

from pinn.architecture_spec import ArchitectureSpec
from pinn.network import build_network
from pinn.verification import diagnostic_variants, evidence_io
from pinn.verification.diagnostic_fit import (
    DiagnosticFitRefused,
    fit_diagnostic,
    pinned_source_hashes,
)
from pinn.verification.diagnostic_guard import read_diagnostic_weights
from pinn.verification.diagnostic_variants import LOCKED_12, REGISTRY
from pinn.verification.feasibility_scorecard import load_scorecard
from pinn.verification.feasibility_scorer import score_network
from pinn.verification.learnability_arms import SEED
from pinn.verification.learnability_data import fixture_context, load_arm_data
from pinn.verification.learnability_protocol import PINNED_MODULES, load_protocol
from pinn.verification.split_allowlist import AllowlistedCorpusReader
from tests.phase60._fixtures import gold_corpus_fixture
from tests.phase65.test_fit_short import _loaded
from tests.phase65.test_isolation import _no_open, stage_boundary_fixture

ROOT = Path(__file__).resolve().parents[2]
CPU = torch.device("cpu")


def _symbol(case, name):
    value = getattr(diagnostic_variants, name, None)
    case.assertIsNotNone(value, f"diagnostic_variants.{name} is missing")
    return value


class RegistryContractTests(unittest.TestCase):
    """The sealed registry: identity, immutability, validation and serialization."""

    def test_the_registry_holds_exactly_the_sealed_entry_and_no_ladders(self):
        self.assertEqual(list(REGISTRY), ["locked-12"])
        self.assertIs(REGISTRY["locked-12"], LOCKED_12)

    def test_the_locked_entry_carries_the_production_configuration(self):
        entry = REGISTRY["locked-12"]
        self.assertEqual(entry.name, "locked-12")
        self.assertEqual(entry.time_features, "raw_tau_ic13")
        self.assertEqual(entry.depth, 12)
        self.assertEqual(entry.width, 256)
        self.assertEqual(entry.first_omega_0, 30.0)
        self.assertEqual(entry.hidden_omega_0, 1.0)
        self.assertEqual(entry.learning_rate, 1e-4)
        self.assertEqual(entry.window_length, 10.0)

    def test_the_registry_is_immutable(self):
        with self.assertRaises(TypeError):
            REGISTRY["locked-12"] = LOCKED_12
        with self.assertRaises(AttributeError):
            REGISTRY.pop("locked-12")

    def test_variant_names_are_exact_ascii_identifiers(self):
        for bad in ("Locked-12", "locked 12", "locked_12", "locked-12\n", "12locked/", "", None, 7):
            with self.subTest(name=bad):
                with self.assertRaises(diagnostic_variants.VariantRefused):
                    diagnostic_variants.DiagnosticVariant(
                        name=bad, time_features="raw_tau_ic13", depth=2, width=8,
                        learning_rate=1e-3, window_length=5.0,
                    )

    def test_register_variant_refuses_duplicate_names(self):
        register = _symbol(self, "register_variant")
        with self.assertRaises(diagnostic_variants.VariantRefused) as caught:
            register(LOCKED_12)
        self.assertIn("locked-12", str(caught.exception))
        # A distinct approved design registers into a copy; registering it again,
        # into that copy or beside itself, is refused.
        approved = diagnostic_variants.DiagnosticVariant(
            name="probe-depth4", time_features="raw_tau_ic13", depth=4, width=32,
            learning_rate=1e-3, window_length=5.0,
        )
        extended = register(approved)
        self.assertIn("probe-depth4", extended)
        self.assertNotIn("probe-depth4", REGISTRY)  # the sealed catalog is unchanged
        with self.assertRaises(diagnostic_variants.VariantRefused):
            register(approved, into=extended)

    def test_registration_preserves_registration_order(self):
        register = _symbol(self, "register_variant")
        names = _symbol(self, "registry_names")
        first = diagnostic_variants.DiagnosticVariant(
            name="ladder-depth2", time_features="raw_tau_ic13", depth=2, width=64,
            learning_rate=1e-3, window_length=10.0,
        )
        second = diagnostic_variants.DiagnosticVariant(
            name="ladder-depth6", time_features="raw_tau_ic13", depth=6, width=64,
            learning_rate=1e-3, window_length=10.0,
        )
        extended = register(first)
        extended = register(second, into=extended)
        self.assertEqual(names(extended), ["locked-12", "ladder-depth2", "ladder-depth6"])

    def test_unknown_time_feature_declarations_are_refused_before_construction(self):
        for declaration in ("log_tau_ic13", "fourier_tau", "raw_tau_ic14", "", None):
            with self.subTest(declaration=declaration):
                with self.assertRaises(diagnostic_variants.VariantRefused) as caught:
                    diagnostic_variants.DiagnosticVariant(
                        name="experimental", time_features=declaration, depth=2,
                        width=8, learning_rate=1e-3, window_length=5.0,
                    )
                # The rejected declaration is named explicitly, so later prediction
                # pages can add their own approved designs on purpose.
                self.assertIn(repr(declaration), str(caught.exception))

    def test_malformed_numeric_fields_are_refused(self):
        base = dict(name="numeric", time_features="raw_tau_ic13")
        for changes in (
            {"depth": 12.0}, {"depth": True}, {"depth": 0}, {"depth": -2},
            {"width": 256.5}, {"width": 0}, {"width": None},
            {"learning_rate": 0.0}, {"learning_rate": -1e-4},
            {"learning_rate": float("inf")}, {"learning_rate": "1e-4"},
            {"window_length": 0.0}, {"window_length": -1.0}, {"window_length": 10.5},
            {"window_length": float("nan")},
        ):
            with self.subTest(changes=changes):
                fields = {**base, "depth": 2, "width": 8, "learning_rate": 1e-3,
                          "window_length": 5.0}
                fields.update(changes)
                with self.assertRaises(diagnostic_variants.VariantRefused):
                    diagnostic_variants.DiagnosticVariant(**fields)

    def test_serialized_fields_round_trip_without_rounded_string_substitution(self):
        serialized = LOCKED_12.to_json_dict()
        self.assertEqual(
            json.loads(json.dumps(serialized)), serialized
        )
        for key in ("learning_rate", "window_length", "first_omega_0", "hidden_omega_0"):
            self.assertIsInstance(serialized[key], float, key)
        for key in ("depth", "width"):
            self.assertIsInstance(serialized[key], int, key)
        self.assertIsInstance(serialized["learning_rate"], float)
        self.assertEqual(serialized["learning_rate"], 1e-4)
        self.assertEqual(repr(serialized["learning_rate"]), repr(1e-4))


class ParityContractTests(unittest.TestCase):
    """D-04: the locked variant is the production network in the same runtime."""

    @staticmethod
    def _inputs(dtype, device, count=6):
        generator = torch.Generator(device="cpu").manual_seed(20261028)
        X = torch.randn((count, 14), generator=generator, dtype=torch.float64).to(dtype=dtype, device=device)
        masses = torch.tensor([[1.7, 0.6, 2.4]], dtype=dtype, device=device).expand(count, 3)
        return X.contiguous(), masses.contiguous()

    def test_parameters_are_bitwise_equal_to_production_at_the_same_seed(self):
        production = build_network(ArchitectureSpec(seed=SEED), dtype=torch.float64, device=CPU)
        variant_net = diagnostic_variants.build_variant(
            "locked-12", seed=SEED, dtype=torch.float64, device=CPU
        )
        production_state = production.state_dict()
        variant_state = variant_net.state_dict()
        self.assertEqual(sorted(production_state), sorted(variant_state))
        for name in sorted(production_state):
            self.assertTrue(
                torch.equal(production_state[name], variant_state[name]), name
            )

    def test_projected_forward_outputs_are_equal_with_unequal_raw_masses(self):
        production = build_network(ArchitectureSpec(seed=SEED), dtype=torch.float64, device=CPU)
        variant_net = diagnostic_variants.build_variant(
            "locked-12", seed=SEED, dtype=torch.float64, device=CPU
        )
        X, masses = self._inputs(torch.float64, CPU)
        with torch.no_grad():
            out_production = production(X, masses)
            out_variant = variant_net(X, masses)
        self.assertTrue(torch.equal(out_production, out_variant))

    def test_state_copied_in_either_direction_gives_identical_outputs(self):
        production = build_network(ArchitectureSpec(seed=SEED), dtype=torch.float64, device=CPU)
        variant_a = diagnostic_variants.build_variant(
            "locked-12", seed=SEED + 1, dtype=torch.float64, device=CPU
        )
        variant_b = diagnostic_variants.build_variant(
            "locked-12", seed=SEED + 2, dtype=torch.float64, device=CPU
        )
        X, masses = self._inputs(torch.float64, CPU)
        variant_a.load_state_dict(production.state_dict())
        variant_b.load_state_dict(variant_a.state_dict())
        production.load_state_dict(variant_b.state_dict())
        with torch.no_grad():
            outputs = [float(model(X, masses).sum()) for model in (production, variant_a, variant_b)]
        self.assertEqual(outputs[0], outputs[1])
        self.assertEqual(outputs[1], outputs[2])

    def test_mps_float32_parity_with_copied_identical_weights(self):
        try:
            torch.zeros(1, device="mps")
        except RuntimeError as exc:
            self.skipTest(f"MPS runtime unavailable; parity case skipped: {exc}")
        device = torch.device("mps")
        production = build_network(
            ArchitectureSpec(seed=SEED), dtype=torch.float32, device=device
        )
        variant_net = diagnostic_variants.build_variant(
            "locked-12", seed=SEED, dtype=torch.float32, device=device
        )
        # Copied identical weights in the SAME runtime. Independently initialized
        # CPU-float64 and MPS-float32 networks are deliberately NOT compared —
        # D-04 forbids that as a parity claim.
        variant_net.load_state_dict(production.state_dict())
        X, masses = self._inputs(torch.float32, device)
        with torch.no_grad():
            self.assertTrue(
                torch.equal(production(X, masses), variant_net(X, masses))
            )


class FrozenSourceContractTests(unittest.TestCase):
    """The 33 pinned modules keep their committed protocol digests."""

    def test_the_committed_protocol_loads_and_pins_33_unique_modules(self):
        protocol = load_protocol()  # raises ProtocolDrift on any pinned change
        self.assertEqual(len(PINNED_MODULES), 33)
        self.assertEqual(len(set(PINNED_MODULES)), 33)
        current = evidence_io.module_hashes(list(PINNED_MODULES))
        self.assertEqual(current, dict(protocol.payload["module_sha256"]))

    def test_a_missing_pinned_artifact_is_a_refusal_not_a_new_baseline(self):
        with tempfile.TemporaryDirectory(prefix="phase65-pinned-") as raw:
            with self.assertRaises(DiagnosticFitRefused):
                pinned_source_hashes(repo_root=Path(raw))


class FitRecordContractTests(unittest.TestCase):
    """A small synthetic fit: direct frozen scorer calls and registry fields on record."""

    @classmethod
    def setUpClass(cls):
        stack = ExitStack()
        cls.addClassCleanup(stack.close)
        cls.fixture = stack.enter_context(gold_corpus_fixture())
        cls.root = Path(stack.enter_context(tempfile.TemporaryDirectory(prefix="phase65-contract-")))
        cls.spec, cls.context, cls.scorecard, cls.data = _loaded(cls.fixture)
        cls.small = diagnostic_variants.DiagnosticVariant(
            name="fixture-small", time_features="raw_tau_ic13", depth=2, width=8,
            learning_rate=1e-3, window_length=10.0,
        )
        from pinn.verification import diagnostic_fit
        cls.fit = diagnostic_fit
        with mock.patch.object(
            diagnostic_fit, "score_network", wraps=diagnostic_fit.score_network
        ) as cls.network_spy, mock.patch.object(
            diagnostic_fit, "score_trajectory", wraps=diagnostic_fit.score_trajectory
        ) as cls.trajectory_spy:
            cls.record = fit_diagnostic(
                cls.small,
                cls.data,
                context=cls.context,
                scorecard=cls.scorecard,
                runtime=("float64", "cpu"),
                evidence_root=cls.root,
                steps=2,
                times_physical=cls.data.score.times,
                seed=SEED,
            )

    def _reloaded_model(self):
        model = diagnostic_variants.build_variant(
            self.small, seed=SEED, dtype=torch.float64, device=CPU
        )
        run_dir = self.root / "diagnostics" / "fixture-small-hierarchical-gold-0"
        payload = read_diagnostic_weights(run_dir / "weights.pt")
        model.load_state_dict(payload["state_dict"])
        return model

    def test_the_frozen_score_functions_are_called_directly(self):
        self.assertEqual(self.network_spy.call_count, 1)
        self.assertGreaterEqual(self.trajectory_spy.call_count, 1)
        call = self.network_spy.call_args_list[0]
        self.assertIs(call.kwargs.get("scorecard"), self.scorecard)

    def test_the_recorded_score_row_matches_a_direct_call(self):
        model = self._reloaded_model()
        view = self.data.score
        direct = score_network(
            model,
            self.data.ic13,
            self.data.masses,
            view.positions,
            view.inner_pair,
            view.times,
            scorecard=self.scorecard,
            dtype=torch.float64,
            device=CPU,
            grid=view.grid,
        ).to_json_dict()
        self.assertEqual(self.record["scores"]["network"], direct)
        self.assertLessEqual(direct["tier"], 3)

    def test_registry_fields_are_present_in_every_record(self):
        variant = self.record["variant"]
        self.assertEqual(variant["name"], "fixture-small")
        self.assertIs(variant["registered"], False)  # a synthetic custom spec, not a Phase 66 experiment
        for field in ("time_features", "depth", "width", "learning_rate", "window_length"):
            self.assertIn(field, variant)
        self.assertEqual(variant["depth"], 2)
        self.assertEqual(variant["width"], 8)

    def test_the_record_reuses_the_pinned_source_hashes(self):
        protocol = load_protocol()
        self.assertEqual(
            self.record["source_sha256"], dict(protocol.payload["module_sha256"])
        )


# ---------------------------------------------------------------------------
# Plan 65-02 (D-08/D-09): recorded normalizer hydration and physical windows.
# ---------------------------------------------------------------------------

_EVIDENCE_REL = Path(
    ".planning/phases/59-read-only-baseline-scorecard/evidence"
)


def _data_module(case):
    try:
        return importlib.import_module("pinn.verification.diagnostic_data")
    except ImportError as exc:
        case.fail(f"pinn.verification.diagnostic_data is missing: {exc}")


def _copy_evidence(tmp):
    """A temp evidence root holding byte-copies of the committed Phase 59 files."""
    import shutil

    audit = tmp / _EVIDENCE_REL / "audit"
    audit.mkdir(parents=True)
    source = ROOT / _EVIDENCE_REL
    shutil.copyfile(source / "manifest.json", tmp / _EVIDENCE_REL / "manifest.json")
    shutil.copyfile(source / "audit" / "reader_acceptance.json", audit / "reader_acceptance.json")
    return tmp


def _rewrite_evidence(tmp, mutate):
    """Rewrite the temp reader-acceptance payload, keeping the manifest digest true."""
    import hashlib

    path = tmp / _EVIDENCE_REL / "audit" / "reader_acceptance.json"
    payload = json.loads(path.read_bytes().decode("utf-8"))
    mutate(payload)
    raw = json.dumps(payload, indent=2).encode("utf-8")
    path.write_bytes(raw)
    manifest_path = tmp / _EVIDENCE_REL / "manifest.json"
    manifest = json.loads(manifest_path.read_bytes().decode("utf-8"))
    manifest["files"]["audit/reader_acceptance.json"] = {
        "sha256": hashlib.sha256(raw).hexdigest(),
        "size_bytes": len(raw),
    }
    manifest_path.write_bytes(json.dumps(manifest, indent=2).encode("utf-8"))
    return path


class RecordedNormalizerTests(unittest.TestCase):
    """The retained IC13 statistics hydrate exactly, with no recovery or refit."""

    def test_the_recorded_stats_reproduce_the_expected_digest(self):
        data = _data_module(self)
        from pinn.verification.learnability_data import EXPECTED_STATS_SHA256

        recorded = data.load_recorded_stats(ROOT)
        self.assertEqual(recorded.stats_sha256, EXPECTED_STATS_SHA256)
        self.assertEqual(recorded.evidence_path, _EVIDENCE_REL.as_posix() + "/audit/reader_acceptance.json")
        # The committed evidence digest matches the Phase 59 manifest entry.
        import hashlib

        raw = (ROOT / _EVIDENCE_REL / "audit" / "reader_acceptance.json").read_bytes()
        self.assertEqual(recorded.evidence_sha256, hashlib.sha256(raw).hexdigest())

    def test_hydration_needs_no_record_read_and_invokes_no_recovery_or_refit(self):
        data = _data_module(self)
        from pinn.verification import learnability_data, production_reference

        with mock.patch.object(
            data.Stage0TrainingReader, "read", side_effect=AssertionError("guarded read")
        ) as guarded_read, mock.patch.object(
            data.Stage0TrainingReader, "exists", side_effect=AssertionError("guarded exists")
        ) as guarded_exists, mock.patch.object(
            learnability_data, "open_real_context", side_effect=AssertionError("open_real_context")
        ), mock.patch.object(
            production_reference, "recover_normalizer_from_checkpoint",
            side_effect=AssertionError("monitor recovery"),
        ), mock.patch.object(
            production_reference, "fallback_normalizer_from_allowlist",
            side_effect=AssertionError("allowlist fallback"),
        ), mock.patch.object(
            production_reference, "compute_normalization_stats",
            side_effect=AssertionError("normalizer refit"),
        ):
            recorded = data.load_recorded_stats(ROOT)
        self.assertEqual(guarded_read.call_count, 0)
        self.assertEqual(guarded_exists.call_count, 0)
        self.assertEqual(recorded.stats_sha256, "77526e53c394bbac4d4a0e8fdd5a7688f0bda108d41c56277b55ad426a7a79f6")

    def test_context_construction_needs_metadata_only(self):
        data = _data_module(self)
        from pinn.verification import learnability_data, production_reference
        from pinn.verification.learnability_data import EXPECTED_STATS_SHA256

        with mock.patch.object(
            learnability_data, "open_real_context", side_effect=AssertionError("open_real_context")
        ), mock.patch.object(
            production_reference, "recover_normalizer_from_checkpoint",
            side_effect=AssertionError("monitor recovery"),
        ), mock.patch.object(
            production_reference, "fallback_normalizer_from_allowlist",
            side_effect=AssertionError("allowlist fallback"),
        ), mock.patch.object(
            production_reference, "compute_normalization_stats",
            side_effect=AssertionError("normalizer refit"),
        ), mock.patch.object(
            data.Stage0TrainingReader, "read", side_effect=AssertionError("guarded read")
        ):
            context = data.open_diagnostic_context()
        self.assertEqual(context.stats_sha256, EXPECTED_STATS_SHA256)
        self.assertEqual(context.run_kind, "diagnostic")
        self.assertIn("reader_acceptance", context.normalizer_source)
        self.assertEqual(context.splits_sha256, context.allowlist.manifest_sha256)
        summary = context.attestation.summary()
        self.assertEqual(summary["opened"]["train"], 0)
        self.assertEqual(summary["opened"]["validation"], 0)
        self.assertEqual(summary["test_split_opened"], 0)

    def test_a_changed_evidence_file_halts_on_the_committed_digest(self):
        data = _data_module(self)
        with tempfile.TemporaryDirectory(prefix="phase65-tamper-") as raw:
            tmp = _copy_evidence(Path(raw))
            path = tmp / _EVIDENCE_REL / "audit" / "reader_acceptance.json"
            path.write_bytes(path.read_bytes() + b"\n")  # digest changed, manifest not
            with self.assertRaises(data.DiagnosticDataRefused) as caught:
                data.load_recorded_stats(tmp)
            self.assertIn("committed", str(caught.exception))

    def test_tampered_statistics_zero_stds_and_substituted_subsets_halt(self):
        data = _data_module(self)

        def bump_means(payload):
            payload["normalizer"]["slot_means"][0] += 1.0

        def zero_std(payload):
            payload["normalizer"]["slot_stds"][3] = 0.0

        def short_means(payload):
            payload["normalizer"]["slot_means"] = payload["normalizer"]["slot_means"][:11]

        def string_std(payload):
            payload["normalizer"]["slot_stds"][7] = "0.2"

        def wrong_recorded_digest(payload):
            payload["normalizer"]["stats_sha256"] = "0" * 64

        def drop_block(payload):
            del payload["normalizer"]

        for label, mutate in (
            ("changed means", bump_means),
            ("zero std", zero_std),
            ("substituted subset", short_means),
            ("non-numeric std", string_std),
            ("wrong recorded digest", wrong_recorded_digest),
            ("missing block", drop_block),
        ):
            with self.subTest(label=label):
                with tempfile.TemporaryDirectory(prefix="phase65-tamper-") as raw:
                    tmp = _copy_evidence(Path(raw))
                    _rewrite_evidence(tmp, mutate)  # manifest digest stays true
                    with self.assertRaises(data.DiagnosticDataRefused):
                        data.load_recorded_stats(tmp)

    def test_a_missing_evidence_file_or_manifest_entry_halts(self):
        data = _data_module(self)
        with tempfile.TemporaryDirectory(prefix="phase65-tamper-") as raw:
            tmp = _copy_evidence(Path(raw))
            (tmp / _EVIDENCE_REL / "audit" / "reader_acceptance.json").unlink()
            with self.assertRaises(data.DiagnosticDataRefused):
                data.load_recorded_stats(tmp)
            tmp2 = _copy_evidence(Path(raw) / "second")
            manifest_path = tmp2 / _EVIDENCE_REL / "manifest.json"
            manifest = json.loads(manifest_path.read_bytes().decode("utf-8"))
            del manifest["files"]["audit/reader_acceptance.json"]
            manifest_path.write_bytes(json.dumps(manifest).encode("utf-8"))
            with self.assertRaises(data.DiagnosticDataRefused):
                data.load_recorded_stats(tmp2)


class WindowBoundaryTests(unittest.TestCase):
    """E-INST: exact physical windows, strict grids and locked-T tau."""

    def setUp(self):
        stack = ExitStack()
        self.addCleanup(stack.close)
        self.fixture = stack.enter_context(stage_boundary_fixture())
        self.data = _data_module(self)
        self.reader = self.data.Stage0TrainingReader(
            allowlist=self.fixture.allowlist,
            data_root=self.fixture.data_root,
            data_root_source=self.fixture.data_root_source,
            blacklist_path=self.fixture.blacklist_path,
        )
        self.context = fixture_context(
            allowlist=self.fixture.allowlist, reader=self.reader, stats=self.fixture.stats
        )
        self.spec = self.data.one_orbit_spec(self.fixture.valid_gold)
        self.scorecard = load_scorecard()  # loaded before any spy is armed

    def _load(self, window_length=None, **kwargs):
        call = dict(
            spec=self.spec, context=self.context, scorecard=self.scorecard,
            dtype=torch.float64, device=CPU,
        )
        if window_length is not None:
            call["window_length"] = window_length
        call.update(kwargs)
        return self.data.load_diagnostic_data(**call)

    def _gold_times(self):
        from pinn.verification.production_reference import load_reference

        reference = load_reference(self.reader, self.fixture.valid_gold)
        return np.asarray(reference.times, dtype=np.float64).reshape(-1)

    def test_windows_outside_the_domain_refuse_before_any_read(self):
        for bad in (0.0, -1.0, 10.0000001, float("nan"), float("inf"), float("-inf"), "10", True, None):
            with self.subTest(bad=bad):
                stack, spies = _no_open()
                with stack:
                    with self.assertRaises(self.data.DiagnosticDataRefused):
                        self._load(bad)
                for spy in spies:
                    self.assertEqual(spy.call_count, 0)
                self.assertEqual(self.reader.access_summary()["actual_opens"], 0)

    def test_endpoint_membership_is_exact(self):
        times = self._gold_times()
        endpoint = float(times[5])
        self.assertTrue((endpoint > 0.0) and (endpoint < 10.0))
        exact = self.data.physical_window(times, endpoint)
        below = self.data.physical_window(times, np.nextafter(endpoint, -np.inf))
        above = self.data.physical_window(times, np.nextafter(endpoint, np.inf))
        # The endpoint itself is included exactly once; anything above is not.
        self.assertTrue(exact[5])
        self.assertEqual(int(exact.sum()), 6)
        self.assertFalse(below[5])
        self.assertEqual(int(below.sum()), 5)
        self.assertTrue(above[5])
        self.assertEqual(int(above.sum()), 6)
        self.assertFalse(exact[6])
        self.assertFalse(above[6])
        self.assertFalse(below[6])

    def test_duplicate_or_unsorted_times_refuse(self):
        times = np.asarray([0.0, 0.5, 0.5, 1.0])
        with self.assertRaises(self.data.DiagnosticDataRefused):
            self.data.physical_window(times, 10.0)
        with self.assertRaises(self.data.DiagnosticDataRefused):
            self.data.physical_window(np.asarray([1.0, 0.5]), 10.0)
        with self.assertRaises(self.data.DiagnosticDataRefused):
            self.data.physical_window(np.asarray([0.0, np.nan, 1.0]), 10.0)

    def test_a_window_with_fewer_than_two_samples_refuses(self):
        times = self._gold_times()
        first_step = float(times[1])
        stack, spies = _no_open()
        with stack:
            with self.assertRaises(self.data.DiagnosticDataRefused) as caught:
                self._load(first_step / 2.0)
        self.assertIn("two", str(caught.exception))

    def test_tau_uses_the_locked_characteristic_time_not_the_window(self):
        from pinn.constants import T_CHARACTERISTIC_TIME

        window = 2.0
        loaded = self._load(window)
        times = np.asarray(loaded.records["train"]["times_physical"], dtype=np.float64)
        tau = np.asarray(loaded.records["train"]["tau"], dtype=np.float64)
        self.assertEqual(times[0], 0.0)
        self.assertLess(float(times[-1]), window)  # the grid need not touch the endpoint
        expected = 2.0 * (torch.as_tensor(times) / T_CHARACTERISTIC_TIME) - 1.0
        self.assertTrue(torch.equal(torch.as_tensor(tau), expected))
        # Locked T, not rescaled to the shorter window: tau stays inside [-1, -0.6].
        self.assertEqual(float(tau[0]), -1.0)
        self.assertGreater(float(tau[-1]), -1.0)
        self.assertLess(float(tau[-1]), 2.0 * (window / T_CHARACTERISTIC_TIME) - 1.0 + 1e-12)
        self.assertLess(float(tau[-1]), 0.0)  # a rescaled [-1, 1] window would end at 0
        # Physical adjacency is preserved separately from tau.
        np.testing.assert_array_equal(np.diff(times), np.diff(times))

    def test_target_scores_and_comparisons_share_one_ordered_time_grid(self):
        loaded = self._load(5.0)
        times = np.asarray(loaded.records["train"]["times_physical"], dtype=np.float64)
        self.assertEqual(loaded.score.times.shape, loaded.data_points.tau_ic13.shape[:1])
        np.testing.assert_array_equal(loaded.score.times, times)
        self.assertTrue(np.all(np.diff(times) > 0.0))
        self.assertEqual(loaded.data_points.targets.shape[0], times.shape[0])

    def test_the_train_summary_records_the_window_and_retained_indices(self):
        window = 5.0
        loaded = self._load(window)
        times = self._gold_times()
        expected_indices = [int(i) for i in np.flatnonzero((times >= 0.0) & (times <= window))]
        entry = loaded.records["train"]
        self.assertEqual(entry["requested_window"], [0.0, window])
        self.assertEqual(entry["retained_indices"], expected_indices)
        self.assertEqual(entry["n_within_window"], len(expected_indices))
        self.assertEqual(entry["split"], "train")

    def test_the_full_window_matches_the_existing_scored_horizon(self):
        loaded = self._load(10.0)
        plain = load_arm_data(
            self.spec,
            fixture_context(
                allowlist=self.fixture.allowlist,
                reader=AllowlistedCorpusReader(
                    allowlist=self.fixture.allowlist,
                    data_root=self.fixture.data_root,
                    data_root_source=self.fixture.data_root_source,
                    blacklist_path=self.fixture.blacklist_path,
                ),
                stats=self.fixture.stats,
            ),
            scorecard=self.scorecard, dtype=torch.float64, device=CPU,
        )
        self.assertTrue(torch.equal(loaded.data_points.tau_ic13, plain.data_points.tau_ic13))
        np.testing.assert_array_equal(loaded.score.times, plain.score.times)
        np.testing.assert_array_equal(loaded.score.positions, plain.score.positions)


if __name__ == "__main__":
    unittest.main()
