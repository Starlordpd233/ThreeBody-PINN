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

import hashlib
import json
import math
import unittest
from pathlib import Path

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
    times = torch.arange(count, dtype=torch.float64) * 0.01
    # Mirror the loader's window transform so tau and physical time correspond.
    X[:, 0] = 2.0 * times / T - 1.0
    targets = (torch.randn((count, 3, 3), generator=generator, dtype=torch.float64) * variation)
    masses = torch.rand((count, 3), generator=generator, dtype=torch.float64) + 0.5
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
        # The scripted input boundary runs at omega_0 = 0.3 with tau-column
        # weights [0.5, 1.5, 2.5], so the frequency is |w| * omega_0 / pi.
        self.assertEqual(measurement.frequency_median, float(1.5 * 0.3 / math.pi))
        self.assertEqual(measurement.frequency_max, float(2.5 * 0.3 / math.pi))
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
        self.assertTrue(all(layer.calls == 0 for layer in model.hidden_layers))

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


_HISTORICAL_SCRIPT_SHA256 = {
    "probe_time_signal.py": "16db5c8cccf76417f4d18a84811d62b99eea4746d11d6f2322cef349065c9a4f",
    "probe_all_arms.py": "a4dea7d08b750b8cef9fa28c3d354f646922b7eb4463b3b39a2ede18ac9d04c8",
}
_SINGLE_ARM_TOOL_ID = "toolu_01PUFNWxrDDsVrU8DTCH4tX3"
_ALL_ARM_TOOL_ID = "toolu_01NHGWRv6pEQCJmqeAXxqonK"
_HISTORICAL_MESSAGE_SHA256 = {
    _SINGLE_ARM_TOOL_ID: "8e916fea7e5dba57b530230a0befaa4de5f3c492d9d086dbbac89c428fb250bd",
    _ALL_ARM_TOOL_ID: "ec112712c5f690521e3c8bb78bf7f390b5205d2f1856cd332cb6b57984dcae78",
}
_HISTORICAL_TIMESTAMP = {
    _SINGLE_ARM_TOOL_ID: "2026-10-27T14:12:02.670Z",
    _ALL_ARM_TOOL_ID: "2026-10-27T14:14:01.814Z",
}
_EXPECTED_ALL_ARM_ROWS = (
    ("g2s-1632-w060", "init"), ("g2s-1632-w060", "adam"),
    ("g2s-1632-w120", "init"), ("g2s-1632-w120", "adam"),
    ("g2s-1632-w240", "init"), ("g2s-1632-w240", "adam"),
    ("g2s-1632-w480", "init"), ("g2s-1632-w480", "adam"),
    ("r1-1632", "init"), ("r1-1632", "polish"),
    ("r1-4658", "init"), ("r1-4658", "adam"),
    ("r1-851", "init"), ("r1-851", "adam"),
)


def _original_dir():
    return (
        Path(__file__).resolve().parents[2]
        / ".planning/phases/65-probe-on-the-record-fit-harness/evidence/original"
    )


class HistoricalSourceTests(unittest.TestCase):
    """The preserved 2026-10-27 originals are byte-exact and durably scoped.

    The preserved scripts are only read and hashed here — importing or executing
    them is forbidden (the preservation check must never run the originals).
    """

    def _read_bytes(self, name):
        path = _original_dir() / name
        if not path.is_file():
            self.fail(f"preserved source artifact is missing: {name}")
        return path.read_bytes()

    def _stdout_document(self):
        try:
            payload = json.loads(self._read_bytes("stdout.json").decode("utf-8"))
        except ValueError as exc:
            self.fail(f"stdout.json is not valid JSON: {exc}")
        if payload.get("schema") != "phase65-original-stdout/v1":
            self.fail(f"unexpected stdout schema: {payload.get('schema')!r}")
        return payload

    def _message(self, tool_use_id):
        for message in self._stdout_document()["messages"]:
            if message.get("tool_use_id") == tool_use_id:
                return message
        self.fail(f"stdout.json is missing the historical message {tool_use_id}")

    def test_preserved_script_hashes_match_the_context_hashes(self):
        for name, expected in _HISTORICAL_SCRIPT_SHA256.items():
            with self.subTest(script=name):
                raw = self._read_bytes(name)
                self.assertEqual(hashlib.sha256(raw).hexdigest(), expected)
                self.assertEqual(
                    len(raw),
                    4040 if name == "probe_time_signal.py" else 3145,
                    "byte count drifted from the recorded original",
                )

    def test_both_numerical_messages_are_preserved_verbatim(self):
        for tool_use_id, expected_sha in _HISTORICAL_MESSAGE_SHA256.items():
            with self.subTest(message=tool_use_id):
                message = self._message(tool_use_id)
                raw = message["text"].encode("utf-8")
                self.assertEqual(hashlib.sha256(raw).hexdigest(), expected_sha)
                self.assertEqual(message["sha256"], expected_sha)
                self.assertEqual(message["byte_count"], len(raw))
                self.assertEqual(message["timestamp"], _HISTORICAL_TIMESTAMP[tool_use_id])
        # The extraction is scoped: the single-arm message carries the per-layer
        # tables, the all-arm message carries the 14-row table; both are complete.
        self.assertIn("== trained r1-1632, adam state", self._message(_SINGLE_ARM_TOOL_ID)["text"])
        self.assertIn("adj h3..h12 range", self._message(_ALL_ARM_TOOL_ID)["text"])

    def _all_arm_rows(self):
        text = self._message(_ALL_ARM_TOOL_ID)["text"]
        rows = []
        for line in text.splitlines():
            fields = line.split()
            if len(fields) == 10 and fields[6] == "to":
                rows.append(fields)
        return rows

    def test_the_all_arm_table_holds_exactly_the_14_state_rows(self):
        rows = self._all_arm_rows()
        observed = tuple((fields[0], fields[1]) for fields in rows)
        self.assertEqual(len(rows), 14)
        self.assertEqual(observed, _EXPECTED_ALL_ARM_ROWS)
        # Signed zero and formatting are preserved verbatim in the table cells.
        by_key = {(fields[0], fields[1]): fields for fields in rows}
        self.assertEqual(by_key[("g2s-1632-w240", "adam")][4], "-0.000")
        self.assertEqual(by_key[("r1-4658", "adam")][4], "-0.000")
        self.assertEqual(by_key[("g2s-1632-w480", "init")][9], "1.61e+03")
        self.assertEqual(by_key[("r1-1632", "polish")][9], "4.97e+07")
        self.assertEqual(by_key[("r1-1632", "polish")][7], "0.018")
        self.assertEqual(by_key[("r1-1632", "init")][8], "2.8730")

    def test_the_r1_1632_adam_polish_supplement_is_distinct(self):
        single = self._message(_SINGLE_ARM_TOOL_ID)["text"]
        adam_block = single.split("== trained r1-1632, adam state", 1)[1]
        polish_block = single.split("== trained r1-1632, polish state", 1)[1]
        # The distinct individual deep-layer values, at the single-arm .4f format.
        self.assertIn("h3", adam_block)
        self.assertIn("0.0186", adam_block)
        self.assertIn("0.0177", polish_block)
        # The single-arm output fields, at their own original formatters.
        self.assertIn("0.0035", adam_block)
        self.assertIn("5.19e+07", adam_block)
        self.assertIn("0.0034", polish_block)
        self.assertIn("4.97e+07", polish_block)
        # The all-arm range for the same state is a DIFFERENT field (.3f over
        # h3..h12): the individual polish h3 value is never merged into it.
        all_rows = {(fields[0], fields[1]): fields for fields in self._all_arm_rows()}
        self.assertEqual(all_rows[("r1-1632", "polish")][7], "0.018")
        self.assertNotIn("0.0177", " ".join(all_rows[("r1-1632", "polish")]))

    def test_the_manifest_records_re_derivable_provenance(self):
        try:
            manifest = json.loads(self._read_bytes("source-manifest.json").decode("utf-8"))
        except ValueError as exc:
            self.fail(f"source-manifest.json is not valid JSON: {exc}")
        if manifest.get("schema") != "phase65-source-manifest/v1":
            self.fail(f"unexpected manifest schema: {manifest.get('schema')!r}")
        source = manifest["extraction_source"]
        self.assertEqual(
            source["message_lines"][_SINGLE_ARM_TOOL_ID], 332, "single-arm line drifted"
        )
        self.assertEqual(source["message_lines"][_ALL_ARM_TOOL_ID], 353, "all-arm line drifted")
        self.assertTrue(source["session_file"].endswith("acb49c49-444a-46ea-a66b-792086b740d2.jsonl"))
        recovery = manifest["recovery_provenance"]
        self.assertEqual(recovery["snapshots"]["probe_time_signal.py"], "85ac6b7d6b97691b@v2")
        self.assertEqual(recovery["snapshots"]["probe_all_arms.py"], "4f2e7a23e12db4e1@v2")
        for entry, expected in zip(manifest["scripts"], _HISTORICAL_SCRIPT_SHA256.items()):
            name, sha = expected
            self.assertEqual(entry["path"], f"evidence/original/{name}")
            self.assertEqual(entry["sha256"], sha)
        for entry in manifest["messages"]:
            self.assertEqual(entry["sha256"], _HISTORICAL_MESSAGE_SHA256[entry["tool_use_id"]])


if __name__ == "__main__":
    unittest.main()
