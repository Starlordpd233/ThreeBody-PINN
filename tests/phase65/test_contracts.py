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
from tests.phase60._fixtures import gold_corpus_fixture
from tests.phase65.test_fit_short import _loaded

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


if __name__ == "__main__":
    unittest.main()
