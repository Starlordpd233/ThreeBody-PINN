"""Phase 65 (DIAG-09 / INST-08, Wave 0): synthetic measurement edge coverage.

The shared centred-neighbour measurement is exercised on scripted boundary
activations so its reductions are compared directly against the preserved
original semantics — feature-wise centring across time samples, cosine of
successive centred rows at the torch default epsilon — and every unusable
sample set (fewer than two samples, non-finite or non-increasing times,
non-finite values, undefined denominators) is refused before a measurement is
computed. Samples are never sorted, merged or dropped; hooks never survive a
raised forward. No real record is opened by this module.
"""

from __future__ import annotations

import math
import unittest

import torch
import torch.nn.functional as F

from pinn.verification.diagnostic_similarity import measure_time_signal

T = 10.0


class _ScriptedBoundary(torch.nn.Module):
    """A layer boundary whose output rows are scripted, with an omega and weight."""

    def __init__(self, rows, omega_0, weight_column, *, raise_on_call=0):
        super().__init__()
        self._rows = rows
        self.omega_0 = float(omega_0)
        self.weight = torch.nn.Parameter(weight_column)
        self._raise_on_call = raise_on_call
        self.calls = 0

    def forward(self, _x):
        self.calls += 1
        if self._raise_on_call and self.calls >= self._raise_on_call:
            raise RuntimeError("scripted forward failure")
        return self._rows


class _ScriptedNet(torch.nn.Module):
    """input_layer + hidden_layers + a scripted projected output."""

    def __init__(self, boundaries, output_rows, **boundary_kwargs):
        super().__init__()
        self.input_layer = boundaries[0]
        self.hidden_layers = torch.nn.ModuleList(boundaries[1:])
        self._output_rows = output_rows
        self._boundary_kwargs = boundary_kwargs

    def forward(self, x, _masses):
        current = self.input_layer(x)
        for layer in self.hidden_layers:
            current = layer(current)
        # A zero multiple of the leaf keeps the scripted values bit-for-bit while
        # giving the output the autograd graph the rate comparator needs.
        return self._output_rows + 0.0 * x[:, :1]


def _weight_column(values):
    """An (out, in) weight whose first (tau) column is ``values``."""
    out = len(values)
    weight = torch.zeros((out, 4), dtype=torch.float64)
    weight[:, 0] = torch.as_tensor(values, dtype=torch.float64)
    return weight


def _scripted_model(rows_per_boundary, output_rows, *, omega_values=(0.3, 1.1, 2.7)):
    boundaries = [
        _ScriptedBoundary(
            rows, omega_values[index], _weight_column([0.5, 1.5, 2.5][: rows.shape[1]])
        )
        for index, rows in enumerate(rows_per_boundary)
    ]
    return _ScriptedNet(boundaries, output_rows)


def _samples(count=4, variation=1.0):
    generator = torch.Generator().manual_seed(65)
    X = torch.randn((count, 14), generator=generator, dtype=torch.float64)
    targets = (torch.randn((count, 3, 3), generator=generator, dtype=torch.float64) * variation)
    masses = torch.rand((count, 3), generator=generator, dtype=torch.float64) + 0.5
    times = torch.arange(count, dtype=torch.float64) * 0.01
    return X, masses, targets, times


class MeasurementSemanticsTests(unittest.TestCase):
    """The shared reductions against the preserved original semantics."""

    def test_layer_rows_are_deterministic_and_ordered(self):
        rows = torch.randn((4, 5), generator=torch.Generator().manual_seed(1), dtype=torch.float64)
        model = _scripted_model(
            [rows, rows.clone(), rows.clone()], torch.zeros((4, 9), dtype=torch.float64)
        )
        X, masses, targets, times = _samples(4)
        first = measure_time_signal(model, X, masses, targets, times)
        second = measure_time_signal(model, X, masses, targets, times)
        self.assertEqual([row.name for row in first.layers], ["input", "h1", "h2"])
        self.assertEqual([row.order for row in first.layers], [0, 1, 2])
        self.assertEqual(
            [row.adjacent_cosine_mean for row in first.layers],
            [row.adjacent_cosine_mean for row in second.layers],
        )

    def test_centred_rows_match_a_direct_cosine_at_the_original_epsilon(self):
        rows = torch.tensor(
            [[1.0, 0.0, 2.0], [1.5, 0.2, 1.0], [0.5, -0.2, 3.0], [2.0, 0.4, 0.5]],
            dtype=torch.float64,
        )
        model = _scripted_model([rows, rows.flip(0)], torch.zeros((4, 9), dtype=torch.float64))
        X, masses, targets, times = _samples(4)
        measurement = measure_time_signal(model, X, masses, targets, times)
        for row, boundary_rows in zip(measurement.layers, (rows, rows.flip(0))):
            centered = boundary_rows - boundary_rows.mean(dim=0, keepdim=True)
            expected = F.cosine_similarity(centered[:-1], centered[1:], dim=1).mean()
            self.assertEqual(row.adjacent_cosine_mean, float(expected))

    def test_identical_adjacent_rows_keep_the_torch_epsilon_behaviour(self):
        rows = torch.tensor([[2.0, -1.0, 0.5]] * 4, dtype=torch.float64)
        model = _scripted_model([rows, rows], torch.zeros((4, 9), dtype=torch.float64))
        X, masses, targets, times = _samples(4)
        measurement = measure_time_signal(model, X, masses, targets, times)
        zeros = torch.zeros(3, dtype=torch.float64)
        expected = float(F.cosine_similarity(zeros, zeros, dim=0))
        for row in measurement.layers:
            self.assertEqual(row.adjacent_cosine_mean, expected)

    def test_finite_derivatives_and_separate_physical_and_tau_coordinates(self):
        rows = torch.randn((4, 3), generator=torch.Generator().manual_seed(7), dtype=torch.float64)
        output_rows = torch.randn((4, 9), generator=torch.Generator().manual_seed(8), dtype=torch.float64)
        model = _scripted_model([rows], output_rows)
        X, masses, targets, times = _samples(4)
        measurement = measure_time_signal(model, X, masses, targets, times)
        self.assertTrue(math.isfinite(measurement.output_movement))
        self.assertTrue(math.isfinite(measurement.output_rate_ratio))
        self.assertEqual(measurement.frequency_median, float(0.5 * 30.0 / math.pi))
        self.assertEqual(measurement.frequency_max, float(2.5 * 30.0 / math.pi))
        # Physical spacing (0.01) and normalized-tau spacing are recorded separately.
        self.assertAlmostEqual(measurement.physical_dt_median, 0.01, places=15)
        tau_spacings = [
            measurement.tau_values[index + 1] - measurement.tau_values[index]
            for index in range(3)
        ]
        self.assertAlmostEqual(
            measurement.physical_dt_median, tau_spacings[0] * T / 2.0, places=12
        )
        self.assertNotEqual(measurement.physical_dt_median, tau_spacings[0])

    def test_samples_are_never_sorted_merged_or_dropped(self):
        rows = torch.randn((4, 3), generator=torch.Generator().manual_seed(9), dtype=torch.float64)
        model = _scripted_model([rows], torch.zeros((4, 9), dtype=torch.float64))
        X, masses, targets, _uniform = _samples(4)
        irregular = torch.tensor([0.0, 0.01, 0.05, 0.06], dtype=torch.float64)
        measurement = measure_time_signal(model, X, masses, targets, irregular)
        self.assertEqual(
            list(measurement.times_physical), [0.0, 0.01, 0.05, 0.06]
        )
        self.assertEqual(measurement.n_points, 4)


class MeasurementRefusalTests(unittest.TestCase):
    """Unusable sample sets are refused before a measurement is computed."""

    def _refused(self, X, masses, targets, times, model=None):
        rows = torch.randn((4, 3), generator=torch.Generator().manual_seed(2), dtype=torch.float64)
        model = model or _scripted_model([rows], torch.zeros((4, 9), dtype=torch.float64))
        return measure_time_signal(model, X, masses, targets, times)

    def _assert_refused_before_forward(self, count, mutate):
        rows = torch.randn((max(count, 2), 3), dtype=torch.float64)
        model = _scripted_model([rows], torch.zeros((max(count, 2), 9), dtype=torch.float64))
        X, masses, targets, times = _samples(max(count, 2))
        X, masses, targets, times = (
            X[:count], masses[:count], targets[:count], times[:count]
        )
        X, masses, targets, times = mutate(X, masses, targets, times)
        with self.assertRaises(ValueError):
            self._refused(X, masses, targets, times, model=model)
        self.assertEqual(model.input_layer.calls, 0)
        self.assertEqual([layer.calls for layer in model.hidden_layers], [0])

    def test_fewer_than_two_samples_are_refused_before_the_forward(self):
        for count in (0, 1):
            with self.subTest(count=count):
                self._assert_refused_before_forward(
                    count, lambda X, m, t, ti: (X, m, t, ti)
                )

    def test_non_finite_times_are_refused_before_the_forward(self):
        for bad in (float("nan"), float("inf")):
            with self.subTest(value=bad):
                def mutate(X, masses, targets, times):
                    times = times.clone()
                    times[1] = bad
                    return X, masses, targets, times
                self._assert_refused_before_forward(4, mutate)

    def test_non_increasing_times_are_refused_rather_than_sorted(self):
        for times in (
            [0.0, 0.02, 0.01, 0.03],
            [0.0, 0.01, 0.01, 0.02],
            [0.03, 0.02, 0.01, 0.0],
        ):
            with self.subTest(times=times):
                def mutate(X, masses, targets, _times):
                    return X, masses, targets, torch.tensor(times, dtype=torch.float64)
                self._assert_refused_before_forward(4, mutate)

    def test_non_finite_samples_are_refused_before_the_forward(self):
        def poison_targets(X, masses, targets, times):
            targets = targets.clone()
            targets[2, 1, 1] = float("nan")
            return X, masses, targets, times

        def poison_inputs(X, masses, targets, times):
            X = X.clone()
            X[0, 3] = float("inf")
            return X, masses, targets, times

        def poison_masses(X, masses, targets, times):
            masses = masses.clone()
            masses[1, 2] = float("nan")
            return X, masses, targets, times

        for mutate in (poison_targets, poison_inputs, poison_masses):
            with self.subTest(mutate=mutate.__name__):
                self._assert_refused_before_forward(4, mutate)

    def test_null_data_is_refused(self):
        rows = torch.randn((4, 3), dtype=torch.float64)
        model = _scripted_model([rows], torch.zeros((4, 9), dtype=torch.float64))
        X, masses, targets, times = _samples(4)
        for X_bad, masses_bad, targets_bad, times_bad in (
            (None, masses, targets, times),
            (X, None, targets, times),
            (X, masses, None, times),
            (X, masses, targets, None),
        ):
            with self.subTest(which="null field"):
                with self.assertRaises(ValueError):
                    self._refused(X_bad, masses_bad, targets_bad, times_bad, model=model)
        self.assertEqual(model.input_layer.calls, 0)

    def test_zero_target_variation_is_refused_before_the_forward(self):
        X, masses, targets, times = _samples(4)
        flat = targets[:1].expand(4, 3, 3).clone()
        self._assert_refused_before_forward(4, lambda X, m, _t, ti: (X, m, flat, ti))

    def test_hooks_are_removed_after_a_raised_forward(self):
        rows = torch.randn((4, 3), dtype=torch.float64)
        boundaries = [
            _ScriptedBoundary(rows, 30.0, _weight_column([0.5, 1.5, 2.5])),
            _ScriptedBoundary(rows, 1.0, _weight_column([0.5, 1.5, 2.5]), raise_on_call=1),
        ]
        model = _ScriptedNet(boundaries, torch.zeros((4, 9), dtype=torch.float64))
        X, masses, targets, times = _samples(4)
        with self.assertRaises(RuntimeError):
            measure_time_signal(model, X, masses, targets, times)
        self.assertEqual(len(model.input_layer._forward_hooks), 0)
        for layer in model.hidden_layers:
            self.assertEqual(len(layer._forward_hooks), 0)
        # The same model still measures once the scripted failure is gone.
        boundaries[1]._raise_on_call = 0
        measurement = measure_time_signal(model, X, masses, targets, times)
        self.assertEqual(len(measurement.layers), 2)
        self.assertEqual(len(model.hidden_layers[0]._forward_hooks), 0)


if __name__ == "__main__":
    unittest.main()
