"""Plan 67-02: the internal Fourier time features and diagnostic model.

D-05's encoded designs append ordered harmonic sin/cos pairs after the raw
``[tau, IC13]`` input inside the model: the public contract stays raw14, the
backbone is the existing network class built from a copied spec whose internal
input dimension is 16 (``tau_ic13_fourier1``) or 18 (``tau_ic13_fourier12``),
the mass-weighted COM forward is inherited unchanged, and the whole transform
is differentiable tensor math with persistent frequency/harmonics buffers —
no detach, NumPy hop or external preprocessing interrupts the frozen scorer's
raw-coordinate AD. The phase identity is ``pi * N_in * (tau + 1)`` with
``N_in`` the committed census row of the encoded variant's orbit, so the
analytic first and second raw-tau derivatives are known in closed form.
"""

from __future__ import annotations

import importlib
import math
import unittest

import torch

from pinn.com_projection import project_com
from pinn.constants import T_CHARACTERISTIC_TIME
from pinn.network import SQRSkipResNetSIREN
from pinn.verification.diagnostic_phase67_catalog import PHASE67_REGISTRY
from pinn.verification.diagnostic_variants import build_variant

CPU = torch.device("cpu")
F64 = torch.float64
#: The committed Phase 59 census row for system 1632 (``panels.json``
#: singles), pinned by the catalog tests against the committed file; the
#: encoded exp04 arms' base frequency is N_IN / T_CHARACTERISTIC_TIME.
N_IN = 10.471994061054543
PHASE_COEFFICIENT = math.pi * N_IN


def time_features_module():
    """Import the plan's new module lazily (the RED tree lacks it)."""
    return importlib.import_module("pinn.verification.diagnostic_time_features")


def _raw_inputs(count=6):
    """A tiny synthetic raw14 sample set: increasing tau, fixed IC13."""
    generator = torch.Generator()
    generator.manual_seed(6702)
    tau = torch.linspace(-1.0, 1.0, count, dtype=F64).unsqueeze(1)
    ic13 = torch.randn(1, 13, dtype=F64, generator=generator).expand(count, 13)
    return torch.cat([tau, ic13.contiguous()], dim=1)


class FourierEncoderTests(unittest.TestCase):
    """The feature declarations, layout, phase identity and refusals."""

    def test_the_module_exports_the_planned_declarations(self):
        module = time_features_module()
        for name in ("DiagnosticTimeFeatures", "DiagnosticTimeFeatureNetwork",
                     "FOURIER_TIME_FEATURES", "FeatureRefused"):
            self.assertTrue(hasattr(module, name), name)
        self.assertEqual(module.FOURIER_TIME_FEATURES, {
            "tau_ic13_fourier1": (1,),
            "tau_ic13_fourier12": (1, 2),
        })

    def test_encoding_appends_ordered_harmonic_pairs_after_the_raw_input(self):
        module = time_features_module()
        features = module.DiagnosticTimeFeatures(
            (1, 2), N_IN / T_CHARACTERISTIC_TIME, dtype=F64, device=CPU
        )
        raw = _raw_inputs()
        encoded = features(raw)
        self.assertEqual(tuple(encoded.shape), (raw.shape[0], 18))
        self.assertTrue(torch.equal(encoded[:, :14], raw))
        phase = PHASE_COEFFICIENT * (raw[:, 0] + 1.0)
        for column, expected in (
            (14, torch.sin(phase)),
            (15, torch.cos(phase)),
            (16, torch.sin(2.0 * phase)),
            (17, torch.cos(2.0 * phase)),
        ):
            self.assertTrue(torch.allclose(
                encoded[:, column], expected, rtol=0.0, atol=1e-12
            ), f"column {column}")

    def test_the_phase_identity_equals_the_registered_conversion(self):
        module = time_features_module()
        features = module.DiagnosticTimeFeatures(
            (1,), N_IN / T_CHARACTERISTIC_TIME, dtype=F64, device=CPU
        )
        # f = N_in / T cycles per physical time unit and phase = 2*pi*f*t with
        # t = T*(tau+1)/2, which the encoder must realize as pi*N_in*(tau+1).
        t_characteristic = features.t_characteristic
        self.assertEqual(t_characteristic, T_CHARACTERISTIC_TIME)
        tau = torch.linspace(-0.75, 0.9, 11, dtype=F64)
        physical = t_characteristic * (tau + 1.0) / 2.0
        expected = torch.sin(2.0 * math.pi * (N_IN / t_characteristic) * physical)
        encoded = features(torch.cat([tau.unsqueeze(1), torch.zeros(11, 13)], dim=1))
        self.assertTrue(torch.allclose(
            encoded[:, 14], expected, rtol=0.0, atol=1e-12
        ))

    def test_first_and_second_raw_tau_derivatives_match_the_harmonics(self):
        module = time_features_module()
        features = module.DiagnosticTimeFeatures(
            (1, 2), N_IN / T_CHARACTERISTIC_TIME, dtype=F64, device=CPU
        )
        raw = _raw_inputs(8)
        leaf = raw.clone().requires_grad_(True)
        encoded = features(leaf)
        for harmonic in (1, 2):
            coefficient = PHASE_COEFFICIENT * harmonic
            phase = coefficient * (leaf[:, 0] + 1.0)
            for kind, column in (("sin", 12 + 2 * harmonic),
                                 ("cos", 13 + 2 * harmonic)):
                column_tensor = encoded[:, column].sum()
                first = torch.autograd.grad(
                    column_tensor, leaf, create_graph=True
                )[0][:, 0]
                second = torch.autograd.grad(
                    first.sum(), leaf, create_graph=True
                )[0][:, 0]
                if kind == "sin":
                    analytic_first = coefficient * torch.cos(phase)
                    analytic_second = -(coefficient ** 2) * torch.sin(phase)
                else:
                    analytic_first = -coefficient * torch.sin(phase)
                    analytic_second = -(coefficient ** 2) * torch.cos(phase)
                self.assertTrue(torch.allclose(
                    first, analytic_first, rtol=0.0, atol=1e-9
                ), f"harmonic {harmonic} {kind} first derivative")
                self.assertTrue(torch.allclose(
                    second, analytic_second, rtol=0.0, atol=1e-6
                ), f"harmonic {harmonic} {kind} second derivative")

    def test_the_raw_columns_carry_no_cross_tau_gradient(self):
        module = time_features_module()
        features = module.DiagnosticTimeFeatures(
            (1,), N_IN / T_CHARACTERISTIC_TIME, dtype=F64, device=CPU
        )
        raw = _raw_inputs(5)
        leaf = raw.clone().requires_grad_(True)
        encoded = features(leaf)
        gradient = torch.autograd.grad(encoded[:, 3].sum(), leaf)[0][:, 0]
        self.assertTrue(torch.equal(gradient, torch.zeros_like(gradient)))

    def test_malformed_and_mismatched_inputs_refuse(self):
        module = time_features_module()
        features = module.DiagnosticTimeFeatures(
            (1,), N_IN / T_CHARACTERISTIC_TIME, dtype=F64, device=CPU
        )
        for bad in (torch.zeros(4, 13), torch.zeros(4, 15), [0.0] * 14, None):
            with self.subTest(bad=type(bad).__name__):
                with self.assertRaises(module.FeatureRefused):
                    features(bad)
        for frequency in (0.0, -1.0, float("inf"), float("nan"), True, "1e0", None):
            with self.subTest(frequency=frequency):
                with self.assertRaises(module.FeatureRefused):
                    module.DiagnosticTimeFeatures(
                        (1,), frequency, dtype=F64, device=CPU
                    )
        for harmonics in ((), (0,), (2, 1), (1, 1), (1.5,), (True,), "1"):
            with self.subTest(harmonics=harmonics):
                with self.assertRaises(module.FeatureRefused):
                    module.DiagnosticTimeFeatures(
                        harmonics, N_IN / 10.0, dtype=F64, device=CPU
                    )

    def test_buffers_survive_a_state_dict_round_trip(self):
        module = time_features_module()
        features = module.DiagnosticTimeFeatures(
            (1, 2), N_IN / T_CHARACTERISTIC_TIME, dtype=F64, device=CPU
        )
        state = features.state_dict()
        self.assertIn("frequency_cycles", state)
        self.assertIn("harmonics", state)
        restored = module.DiagnosticTimeFeatures(
            (1, 2), 0.5, dtype=F64, device=CPU
        )
        restored.load_state_dict(state)
        self.assertTrue(torch.equal(
            restored.frequency_cycles, features.frequency_cycles
        ))
        self.assertTrue(torch.equal(restored.harmonics, features.harmonics))
        raw = _raw_inputs(4)
        self.assertTrue(torch.equal(restored(raw), features(raw)))
        self.assertIsNot(restored.frequency_cycles, features.frequency_cycles)
        self.assertEqual(
            [float(value) for value in restored.frequency_cycles.tolist()],
            [N_IN / 10.0, 2.0 * N_IN / 10.0],
        )
        self.assertEqual(
            [int(value) for value in restored.harmonics.tolist()], [1, 2]
        )


class DiagnosticNetworkTests(unittest.TestCase):
    """The diagnostic subclass: public raw contract, COM, bounds, scorer AD."""

    def _model(self, name):
        return build_variant(
            PHASE67_REGISTRY[name], seed=42, dtype=F64, device=CPU
        )

    def test_encoded_models_keep_the_public_raw_contract_and_com(self):
        module = time_features_module()
        model = self._model("exp04-locked-f1")
        self.assertIsInstance(model, SQRSkipResNetSIREN)
        self.assertIsInstance(model, module.DiagnosticTimeFeatureNetwork)
        self.assertEqual(model.input_layer.in_features, 16)
        self.assertEqual(model.internal_input_dimension, 16)
        raw = _raw_inputs(6)
        masses = torch.tensor([0.4, 1.0, 0.8], dtype=F64)
        out = model(raw, masses)
        self.assertEqual(tuple(out.shape), (6, 9))
        raw_positions = model._forward_unprojected(raw)
        projected = project_com(raw_positions, masses, dtype=F64, device=CPU)
        self.assertTrue(torch.allclose(out, projected, rtol=0.0, atol=0.0))

    def test_the_harmonic_designs_reach_14_16_18_internal_dimensions(self):
        raw = self._model("exp04-locked-raw")
        f1 = self._model("exp04-locked-f1")
        f12 = self._model("exp04-locked-f12")
        self.assertEqual(raw.input_layer.in_features, 14)
        self.assertEqual(f1.input_layer.in_features, 16)
        self.assertEqual(f12.input_layer.in_features, 18)
        self.assertEqual(f12.internal_input_dimension, 18)

    def test_the_exp01_backbone_keeps_its_actual_settings(self):
        module = time_features_module()
        model = self._model("exp04-exp01-f12")
        self.assertIsInstance(model, module.DiagnosticTimeFeatureNetwork)
        self.assertEqual(len(model.hidden_layers), 1)
        self.assertEqual(model.input_layer.out_features, 384)
        self.assertEqual(model.input_layer.omega_0, 1000.0)
        self.assertEqual(model.input_layer.in_features, 18)

    def test_the_first_layer_fan_in_bound_is_one_over_the_internal_dimension(self):
        module = time_features_module()
        for name, internal in (("exp04-locked-f1", 16),
                               ("exp04-locked-f12", 18),
                               ("exp04-exp01-f1", 16)):
            with self.subTest(variant=name):
                model = self._model(name)
                self.assertEqual(model.first_layer_fan_in_bound, 1.0 / internal)
                weights = model.input_layer.weight.detach()
                self.assertLessEqual(float(weights.abs().max()),
                                     1.0 / internal + 1e-12)
                self.assertGreater(float(weights.abs().max()),
                                   0.9 / internal)

    def test_encoded_buffers_survive_a_model_state_dict_round_trip(self):
        module = time_features_module()
        model = self._model("exp04-locked-f12")
        state = model.state_dict()
        self.assertIn("features.frequency_cycles", state)
        self.assertIn("features.harmonics", state)
        restored = self._model("exp04-exp01-f12")  # different topology entirely
        with self.assertRaises(RuntimeError):
            restored.load_state_dict(state)
        rebuilt = self._model("exp04-locked-f12")
        rebuilt.load_state_dict(state)
        raw = _raw_inputs(4)
        masses = torch.tensor([0.4, 1.0, 0.8], dtype=F64)
        self.assertTrue(torch.allclose(
            rebuilt(raw, masses), model(raw, masses), rtol=0.0, atol=0.0
        ))

    def test_seeded_encoded_construction_is_deterministic(self):
        first = self._model("exp04-locked-f1")
        second = self._model("exp04-locked-f1")
        state_a, state_b = first.state_dict(), second.state_dict()
        self.assertEqual(list(state_a), list(state_b))
        for key in state_a:
            self.assertTrue(torch.equal(state_a[key], state_b[key]), key)

    def test_parallel_constructions_share_no_mutable_state(self):
        first = self._model("exp04-locked-f1")
        second = self._model("exp04-locked-f1")
        self.assertIsNot(first.features.frequency_cycles,
                         second.features.frequency_cycles)
        self.assertIsNot(first.features.harmonics, second.features.harmonics)
        before = first.features.frequency_cycles.clone()
        second.features.frequency_cycles.zero_()
        self.assertTrue(torch.equal(first.features.frequency_cycles, before))

    def test_the_frozen_scorer_differentiates_the_encoded_model(self):
        from contextlib import ExitStack

        from pinn.verification.feasibility_scorer import (
            network_trajectory,
            score_network,
        )
        from tests.phase65.test_fit_short import _loaded
        from tests.phase60._fixtures import gold_corpus_fixture

        with ExitStack() as stack:
            fixture = stack.enter_context(gold_corpus_fixture())
            _spec, _context, scorecard, data = _loaded(fixture)
            model = self._model("exp04-locked-f1")
            view = data.score
            positions, velocities = network_trajectory(
                model,
                data.ic13,
                data.masses,
                view.times,
                dtype=F64,
                device=CPU,
            )
            self.assertEqual(positions.shape[0], len(view.times))
            self.assertTrue(bool(torch.isfinite(torch.as_tensor(positions)).all()))
            self.assertTrue(bool(torch.isfinite(torch.as_tensor(velocities)).all()))
            score = score_network(
                model,
                data.ic13,
                data.masses,
                view.positions,
                view.inner_pair,
                view.times,
                scorecard=scorecard,
                dtype=F64,
                device=CPU,
                grid=view.grid,
            ).to_json_dict()
        self.assertIn("E", score)
        self.assertTrue(math.isfinite(float(score["E"])))
        self.assertEqual(score["velocity_source"], "autograd")


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
