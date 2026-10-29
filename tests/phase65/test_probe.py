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
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest import mock

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


def _probe_symbol(name):
    """Import the probe module and fetch ``name``, failing assertively when absent.

    Every planned-behavior test goes through this helper so a RED run reports
    assertion failures (the planned behavior is missing), never import or
    attribute errors, which the TDD gate classifies as invalid RED.
    """
    try:
        import pinn.verification.diagnostic_probe as module
    except ImportError as exc:
        raise AssertionError(
            f"pinn.verification.diagnostic_probe must exist: {exc}"
        ) from exc
    if not hasattr(module, name):
        raise AssertionError(f"diagnostic_probe.{name} is missing")
    return getattr(module, name)


def _guard_function(name):
    try:
        from pinn.verification import diagnostic_guard
    except ImportError as exc:
        raise AssertionError(
            f"pinn.verification.diagnostic_guard must import: {exc}"
        ) from exc
    if not hasattr(diagnostic_guard, name):
        raise AssertionError(f"diagnostic_guard.{name} is missing")
    return getattr(diagnostic_guard, name)


class FormatterCellTests(unittest.TestCase):
    """Exact rounding cells: endpoints, inclusion, neighbours, no widened acceptance."""

    def test_cell_endpoints_are_exact_representable_values(self):
        derive_cell = _probe_symbol("derive_cell")
        render = _probe_symbol("render")
        cell = derive_cell(".3f", "1.000")
        lo, hi = cell["lo"], cell["hi"]
        self.assertEqual(render(lo, ".3f"), "1.000")
        self.assertEqual(render(hi, ".3f"), "1.000")
        self.assertNotEqual(render(math.nextafter(lo, -math.inf), ".3f"), "1.000")
        self.assertNotEqual(render(math.nextafter(hi, math.inf), ".3f"), "1.000")
        # Everything strictly between the endpoints renders to the token too.
        self.assertEqual(render(math.nextafter(lo, math.inf), ".3f"), "1.000")
        self.assertEqual(render(math.nextafter(hi, -math.inf), ".3f"), "1.000")
        self.assertTrue(cell["lo_included"] and cell["hi_included"])

    def test_signed_zero_cells_do_not_span_the_sign(self):
        derive_cell = _probe_symbol("derive_cell")
        render = _probe_symbol("render")
        negative = derive_cell(".3f", "-0.000")
        self.assertEqual(math.copysign(1.0, negative["hi"]), -1.0)
        self.assertEqual(math.copysign(1.0, negative["lo"]), -1.0)
        self.assertEqual(render(math.nextafter(negative["hi"], math.inf), ".3f"), "0.000")
        positive = derive_cell(".4f", "0.0000")
        self.assertEqual(math.copysign(1.0, positive["lo"]), 1.0)
        self.assertEqual(
            render(math.nextafter(positive["lo"], -math.inf), ".4f"), "-0.0000"
        )

    def test_ties_do_not_widen_a_cell(self):
        derive_cell = _probe_symbol("derive_cell")
        render = _probe_symbol("render")
        # Python rounds a decimal-midpoint tie to even, so an exact midpoint
        # belongs to the lower cell and is that cell's inclusive upper endpoint.
        self.assertEqual(render(0.125, ".2f"), "0.12")
        cell = derive_cell(".2f", "0.12")
        self.assertEqual(cell["hi"], 0.125)
        self.assertEqual(render(math.nextafter(cell["hi"], math.inf), ".2f"), "0.13")

    def test_exponent_changes_sit_inside_one_cell(self):
        derive_cell = _probe_symbol("derive_cell")
        render = _probe_symbol("render")
        cell = derive_cell(".3g", "1e+03")
        self.assertEqual(render(999.5, ".3g"), "1e+03")
        self.assertLessEqual(cell["lo"], 999.5)
        self.assertGreaterEqual(cell["hi"], 1000.0)
        self.assertNotEqual(render(math.nextafter(cell["lo"], -math.inf), ".3g"), "1e+03")
        self.assertNotEqual(render(math.nextafter(cell["hi"], math.inf), ".3g"), "1e+03")

    def test_3g_omitted_trailing_zeros_never_widen_acceptance(self):
        derive_cell = _probe_symbol("derive_cell")
        render = _probe_symbol("render")
        cell = derive_cell(".3g", "1.9e+08")
        self.assertEqual(render(1.9e8, ".3g"), "1.9e+08")
        # Counting visible digits would read two significant digits and accept
        # any 1.x e+08 value; the true .3g cell is the 1.90e8 rounding cell.
        self.assertEqual(render(1.86e8, ".3g"), "1.86e+08")
        self.assertLess(1.86e8, cell["lo"])
        self.assertEqual(render(1.8999e8, ".3g"), "1.9e+08")
        self.assertGreaterEqual(1.8999e8, cell["lo"])
        self.assertNotEqual(render(math.nextafter(cell["hi"], math.inf), ".3g"), "1.9e+08")

    def test_compare_field_uses_exact_formatter_equality(self):
        compare_field = _probe_symbol("compare_field")
        expected = {"formatter": ".4f", "token": "0.0186"}
        reproduced = compare_field(expected, 0.01862)
        self.assertEqual(reproduced["status"], "reproduced")
        failed = compare_field(expected, 0.018651)
        self.assertEqual(failed["status"], "not_reproduced")

    def test_compare_field_cross_checks_recorded_cells(self):
        compare_field = _probe_symbol("compare_field")
        derive_cell = _probe_symbol("derive_cell")
        cell = derive_cell(".4f", "0.0186")
        good = dict(_probe_symbol("compare_field")(
            {"formatter": ".4f", "token": "0.0186",
             "cell": {"lo_hex": float(cell["lo"]).hex(), "hi_hex": float(cell["hi"]).hex()}},
            0.01862,
        ))
        self.assertEqual(good["status"], "reproduced")
        tampered = {"formatter": ".4f", "token": "0.0186",
                    "cell": {"lo_hex": (0.5).hex(), "hi_hex": (2.0).hex()}}
        with self.assertRaises(ValueError):
            compare_field(tampered, 0.01862)

    def test_membership_and_render_agree_across_preserved_tokens(self):
        compare_field = _probe_symbol("compare_field")
        samples = (
            (".2f", "0.78"), (".2f", "66.38"), (".3f", "-0.000"), (".3f", "1.000"),
            (".3g", "4.97e+07"), (".3g", "51.9"), (".4f", "2.8730"), (".4f", "-0.0019"),
        )
        for formatter, token in samples:
            with self.subTest(formatter=formatter, token=token):
                anchor = float(token)
                for value in (
                    anchor,
                    math.nextafter(anchor, math.inf),
                    math.nextafter(anchor, -math.inf),
                    anchor * 3.0,
                ):
                    verdict = compare_field({"formatter": formatter, "token": token}, value)
                    expected_status = (
                        "reproduced"
                        if format(value, formatter) == token
                        else "not_reproduced"
                    )
                    self.assertEqual(verdict["status"], expected_status)


class ReadingRuleTests(unittest.TestCase):
    """The registered reading rule: retained, withdrawn, and separately reported."""

    def _evaluate(self, entries):
        return _probe_symbol("evaluate_reading_rule")(entries)

    def test_all_reproduced_fields_retain_the_lead(self):
        entries = [
            {"field_id": "a/init/frequency_median", "availability": "measured",
             "status": "reproduced"},
            {"field_id": "a/init/out_move", "availability": "measured",
             "status": "reproduced"},
        ]
        rule = self._evaluate(entries)
        self.assertEqual(rule["verdict"], "retained")
        self.assertFalse(rule["scope49_proposal"])

    def test_any_failed_required_comparison_withdraws_with_a_scope49_proposal(self):
        entries = [
            {"field_id": "a/init/frequency_median", "availability": "measured",
             "status": "reproduced"},
            {"field_id": "a/polish/rate_ratio", "availability": "measured",
             "status": "not_reproduced"},
        ]
        rule = self._evaluate(entries)
        self.assertEqual(rule["verdict"], "withdrawn")
        self.assertTrue(rule["scope49_proposal"])
        self.assertIn("a/polish/rate_ratio", rule["failed_required"])

    def test_preserved_only_fields_are_reported_and_never_flip_the_verdict(self):
        entries = [
            {"field_id": "supplement/adam/moving/h3", "availability": "preserved_only"},
            {"field_id": "a/init/frequency_median", "availability": "measured",
             "status": "reproduced"},
        ]
        rule = self._evaluate(entries)
        self.assertEqual(rule["verdict"], "retained")
        self.assertIn("supplement/adam/moving/h3", rule["not_measured"])

    def test_provenance_limitations_are_reported_separately(self):
        entries = [
            {"field_id": "missing/source/block", "availability": "provenance_limitation",
             "reason": "the original output for this figure is absent from the source"},
            {"field_id": "a/init/frequency_median", "availability": "measured",
             "status": "reproduced"},
        ]
        rule = self._evaluate(entries)
        self.assertEqual(rule["verdict"], "retained")
        self.assertIn("missing/source/block", rule["provenance_limitations"])

    def test_new_measurements_are_recorded_without_a_historical_target(self):
        entry = _probe_symbol("new_measurement_entry")(
            "arm/r1-1632/init", "h5", 0.9123, deep_min_token="0.925", deep_max_token="1.000"
        )
        self.assertEqual(entry["status"], "new_measurement")
        self.assertEqual(entry["value"], 0.9123)
        self.assertIn("delta", entry)
        rule = self._evaluate([entry])
        self.assertEqual(rule["verdict"], "retained")
        self.assertIn("arm/r1-1632/init/h5", rule["new_measurements"])


def _sha256_bytes(raw):
    return hashlib.sha256(raw).hexdigest()


def _fixture_registration(root, kind="matching", expectations_extra=None):
    """A minimal committed probe registration inside a throwaway git repository.

    ``kind`` selects the broken variant: matching, missing (an artifact is
    deleted), untracked (the expectations file is never committed), staged_only
    (added but uncommitted), dirty (modified after commit), changed_dependency
    (a listed code dependency changes content after the registration commit),
    weight_changed (committed weight bytes no longer match the digest),
    unrelated_dirty (an unlisted file is dirty — which must NOT refuse),
    unordered (arms not in committed-record path order) and duplicate (the same
    arm listed twice). ``expectations_extra`` is merged into the expectations
    document before it is written (run-test probe rows).
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
    # A cached-template maintenance run can repack loose objects mid-test
    # (Phase 60 lesson); disable it for the throwaway repository.
    git("config", "maintenance.auto", "false")
    git("config", "gc.auto", "0")

    reg = root / "reg"
    reg.mkdir()
    page_raw = b"# fixture prediction page\n"
    manifest_raw = b'{"schema": "fixture/v1"}\n'
    stdout_raw = b'{"messages": []}\n'
    script_raw = b"# original script stand-in\n"
    dep_raw = b"DEPENDENCY = 1\n"
    frozen_raw = b"FROZEN = True\n"
    (reg / "PREDICTION.md").write_bytes(page_raw)
    (reg / "source-manifest.json").write_bytes(manifest_raw)
    (reg / "stdout.json").write_bytes(stdout_raw)
    (reg / "probe.py").write_bytes(script_raw)
    (root / "code_dep.py").write_bytes(dep_raw)
    frozen = root / "frozen"
    frozen.mkdir()
    (frozen / "scorer.py").write_bytes(frozen_raw)
    arm = root / "arms" / "r1-1632"
    arm.mkdir(parents=True)
    record_raw = b'{"arm_id": "r1-1632"}\n'
    weights_raw = b"weights-bytes"
    (arm / "record.json").write_bytes(record_raw)
    (arm / "adam.weights").write_bytes(weights_raw)

    second = root / "arms" / "r1-851"
    if kind in ("unordered", "duplicate"):
        second.mkdir(parents=True)
        (second / "record.json").write_bytes(b'{"arm_id": "r1-851"}\n')
        (second / "adam.weights").write_bytes(b"weights-851")

    def entry(rel, raw):
        return {"path": rel, "sha256": _sha256_bytes(raw)}

    arms = [
        {
            "arm_id": "r1-1632",
            "record": entry("arms/r1-1632/record.json", record_raw),
            "weights": {"adam": entry("arms/r1-1632/adam.weights", weights_raw)},
        }
    ]
    if kind == "unordered":
        # r1-851's record path sorts BEFORE r1-1632's, so putting it first is
        # genuinely out of stable committed-record path order.
        arms.insert(0, {
            "arm_id": "r1-851",
            "record": entry("arms/r1-851/record.json", b'{"arm_id": "r1-851"}\n'),
            "weights": {"adam": entry("arms/r1-851/adam.weights", b"weights-851")},
        })
    if kind == "duplicate":
        arms.append(dict(arms[0]))

    expectations = {
        "schema": "phase65-probe-registration/v1",
        "page": entry("reg/PREDICTION.md", page_raw),
        "source": {
            "manifest": entry("reg/source-manifest.json", manifest_raw),
            "stdout": entry("reg/stdout.json", stdout_raw),
            "scripts": [entry("reg/probe.py", script_raw)],
        },
        "code_dependencies": [entry("code_dep.py", dep_raw)],
        "frozen": [entry("frozen/scorer.py", frozen_raw)],
        "arms": arms,
    }
    if expectations_extra:
        expectations.update(expectations_extra)
    expectations_raw = (json.dumps(expectations, indent=2) + "\n").encode("utf-8")
    (reg / "expectations.json").write_bytes(expectations_raw)

    paths = [
        "reg/PREDICTION.md", "reg/source-manifest.json", "reg/stdout.json",
        "reg/probe.py", "code_dep.py", "frozen/scorer.py",
        "arms/r1-1632/record.json", "arms/r1-1632/adam.weights",
    ]
    if kind in ("unordered", "duplicate"):
        paths += ["arms/r1-851/record.json", "arms/r1-851/adam.weights"]
    if kind == "untracked":
        git("add", *paths)
        git("commit", "-q", "-m", "fixture without the expectations file")
        return root
    if kind == "staged_only":
        git("add", *paths)
        git("add", "reg/expectations.json")
        return root
    git("add", *paths)
    git("add", "reg/expectations.json")
    git("commit", "-q", "-m", "fixture registration")

    if kind == "missing":
        (reg / "PREDICTION.md").unlink()
    elif kind == "dirty":
        (reg / "expectations.json").write_bytes(expectations_raw + b"# drifted\n")
    elif kind == "changed_dependency":
        (root / "code_dep.py").write_bytes(b"DEPENDENCY = 2\n")
        git("add", "code_dep.py")
        git("commit", "-q", "-m", "change the dependency after registration")
    elif kind == "weight_changed":
        (arm / "adam.weights").write_bytes(b"weights-bytes-tampered")
        git("add", "arms/r1-1632/adam.weights")
        git("commit", "-q", "-m", "change the weights after registration")
    elif kind == "unrelated_dirty":
        (root / "unrelated.txt").write_text("user-owned scratch\n")
    return root


class RegistrationAdmissionTests(unittest.TestCase):
    """require_committed_registration: tracked/clean, digests, order — before any load."""

    def test_a_matching_committed_fixture_passes(self):
        require = _guard_function("require_committed_registration")
        with tempfile.TemporaryDirectory() as tmp:
            repo = _fixture_registration(Path(tmp) / "repo")
            require(repo / "reg/expectations.json", repo_root=repo)

    def test_a_matching_fixture_tolerates_an_unrelated_dirty_file(self):
        require = _guard_function("require_committed_registration")
        with tempfile.TemporaryDirectory() as tmp:
            repo = _fixture_registration(Path(tmp) / "repo", kind="unrelated_dirty")
            require(repo / "reg/expectations.json", repo_root=repo)

    def _refused(self, kind):
        require = _guard_function("require_committed_registration")
        with tempfile.TemporaryDirectory() as tmp:
            repo = _fixture_registration(Path(tmp) / "repo", kind=kind)
            with mock.patch.object(torch, "load", side_effect=AssertionError("weights loaded")), \
                    mock.patch(
                        "pinn.verification.diagnostic_data.open_diagnostic_context",
                        side_effect=AssertionError("corpus context opened"),
                    ), mock.patch(
                        "pinn.verification.diagnostic_data.load_diagnostic_data",
                        side_effect=AssertionError("corpus data read"),
                    ):
                require(repo / "reg/expectations.json", repo_root=repo)

    def test_missing_artifacts_refuse(self):
        with self.assertRaises(Exception):
            self._refused("missing")

    def test_untracked_registrations_refuse(self):
        with self.assertRaises(Exception):
            self._refused("untracked")

    def test_staged_only_registrations_refuse(self):
        with self.assertRaises(Exception):
            self._refused("staged_only")

    def test_dirty_registrations_refuse(self):
        with self.assertRaises(Exception):
            self._refused("dirty")

    def test_changed_dependencies_refuse(self):
        with self.assertRaises(Exception):
            self._refused("changed_dependency")

    def test_changed_weight_bytes_refuse_before_any_load(self):
        with self.assertRaises(Exception):
            self._refused("weight_changed")

    def test_out_of_order_arms_refuse(self):
        with self.assertRaises(Exception):
            self._refused("unordered")

    def test_duplicate_arms_refuse(self):
        with self.assertRaises(Exception):
            self._refused("duplicate")

    def test_check_registration_mode_skips_weight_bytes(self):
        require = _guard_function("require_committed_registration")
        with tempfile.TemporaryDirectory() as tmp:
            repo = _fixture_registration(Path(tmp) / "repo")
            (repo / "arms/r1-1632/adam.weights").unlink()
            require(repo / "reg/expectations.json", repo_root=repo, weight_digests=False)
            with self.assertRaises(Exception):
                require(repo / "reg/expectations.json", repo_root=repo)


class CheckRegistrationTests(unittest.TestCase):
    """check-registration: read-only committed-identity report, zero data access."""

    def test_a_committed_registration_reports_its_commit_and_hashes(self):
        check_registration = _probe_symbol("check_registration")
        with tempfile.TemporaryDirectory() as tmp:
            repo = _fixture_registration(Path(tmp) / "repo")
            with mock.patch.object(torch, "load", side_effect=AssertionError("weights loaded")), \
                    mock.patch(
                        "pinn.verification.diagnostic_data.open_diagnostic_context",
                        side_effect=AssertionError("corpus context opened"),
                    ):
                report = check_registration(repo / "reg/expectations.json", repo_root=repo)
        self.assertTrue(report["committed"])
        self.assertTrue(report["registration_commit"])
        self.assertIn("reg/expectations.json", {a["path"] for a in report["artifacts"]})

    def test_an_uncommitted_registration_refuses(self):
        check_registration = _probe_symbol("check_registration")
        with tempfile.TemporaryDirectory() as tmp:
            repo = _fixture_registration(Path(tmp) / "repo", kind="dirty")
            with self.assertRaises(Exception):
                check_registration(repo / "reg/expectations.json", repo_root=repo)


def _expectations_with_rows(fields_by_row, *, supplement_fields=None):
    """Extra registration content naming scripted measured tokens for a run test."""
    return {
        "probe": {
            "arms": [
                {
                    "arm_id": "r1-1632",
                    "first_omega_0": 30.0,
                    "rows": [
                        {"state": "init", "fields": fields_by_row["init"]},
                        {"state": "adam", "fields": fields_by_row["adam"]},
                    ],
                    "new_measurements": True,
                }
            ],
            "supplement": {
                "arm_id": "r1-1632",
                "states": {
                    "adam": {"fields": supplement_fields or {}},
                },
            },
            "logger_parity": {"arm_id": "r1-1632", "state": "adam"},
        }
    }


class ProbeRunGateTests(unittest.TestCase):
    """The read-only runner: admission first, exclusive attempts, no optimizer."""

    def _setup(self, *, kind="matching", perturb=False, extra=None):
        run_probe = _probe_symbol("run_probe")
        rows = torch.randn((4, 5), generator=torch.Generator().manual_seed(11), dtype=torch.float64)
        # Four boundaries (input + h1..h3) so the deep-layer new-measurement
        # recording has an h3..h12 population to label.
        boundaries = [rows, rows.clone(), rows.clone(), rows.flip(0)]
        output_rows = torch.randn((4, 9), generator=torch.Generator().manual_seed(12), dtype=torch.float64)
        model = _scripted_model(boundaries, output_rows, omega_values=(0.3, 1.1, 2.7, 0.9))
        X, masses, targets, times = _samples(4)
        measurement = measure_time_signal(model, X, masses, targets, times)

        def token(value, formatter):
            return format(value, formatter)

        def row_fields(perturbed):
            fields = {
                "frequency_median": {"formatter": ".2f", "token": token(measurement.frequency_median, ".2f")},
                "adj_h1": {"formatter": ".3f", "token": token(
                    [row for row in measurement.layers if row.name == "h1"][0].adjacent_cosine_mean, ".3f")},
                "out_move": {"formatter": ".4f", "token": token(measurement.output_movement, ".4f")},
                "rate_ratio": {"formatter": ".3g", "token": token(measurement.output_rate_ratio, ".3g")},
            }
            if perturbed:
                fields["out_move"]["token"] = "9.9900"
            return fields

        fields_by_row = {"init": row_fields(perturb), "adam": row_fields(perturb)}
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        repo = _fixture_registration(
            Path(tmp.name) / "repo", kind=kind,
            expectations_extra=extra if extra is not None else _expectations_with_rows(fields_by_row),
        )
        output_dir = Path(tmp.name) / "output"
        output_dir.mkdir()
        calls = {"data": 0, "models": 0}

        def data_loader(arm_id):
            calls["data"] += 1
            return X, masses, targets, times

        def model_factory(first_omega_0, state, weights_path):
            calls["models"] += 1
            return _scripted_model(boundaries, output_rows, omega_values=(0.3, 1.1, 2.7, 0.9))

        result = run_probe(
            repo / "reg/expectations.json",
            repo_root=repo,
            output_dir=output_dir,
            data_loader=data_loader,
            model_factory=model_factory,
        )
        return {
            "repo": repo, "output_dir": output_dir, "result": result,
            "calls": calls, "run_probe": run_probe,
            "data_loader": data_loader, "model_factory": model_factory,
        }

    def test_a_complete_run_writes_an_exclusive_result_with_a_verdict(self):
        setup = self._setup()
        result = setup["result"]
        self.assertEqual(result["schema"], "phase65-probe-result/v1")
        self.assertEqual(result["status"], "complete")
        self.assertTrue((setup["output_dir"] / "attempt.json").is_file())
        self.assertTrue((setup["output_dir"] / "reproduction.json").is_file())
        self.assertTrue((setup["output_dir"] / "reproduction.stdout.txt").is_file())

    def test_all_matching_fields_reproduce_and_retain_the_lead(self):
        setup = self._setup()
        self.assertEqual(setup["result"]["reading_rule"]["verdict"], "retained")
        self.assertFalse(setup["result"]["reading_rule"]["scope49_proposal"])

    def test_a_perturbed_token_withdraws_but_stays_a_complete_result(self):
        setup = self._setup(perturb=True)
        result = setup["result"]
        self.assertEqual(result["status"], "complete")
        self.assertEqual(result["reading_rule"]["verdict"], "withdrawn")
        self.assertTrue(result["reading_rule"]["scope49_proposal"])
        self.assertTrue(any("out_move" in field for field in result["reading_rule"]["failed_required"]))

    def test_a_second_run_on_the_same_outputs_refuses_and_never_replaces_the_result(self):
        setup = self._setup()
        first = setup["result"]
        output_dir = setup["output_dir"]
        run_probe = setup["run_probe"]
        repo = setup["repo"]
        data_loader = setup["data_loader"]
        model_factory = setup["model_factory"]
        before = (output_dir / "reproduction.json").read_bytes()
        attempt_class = _probe_symbol("AttemptExists")
        with self.assertRaises(attempt_class):
            run_probe(
                repo / "reg/expectations.json", repo_root=repo, output_dir=output_dir,
                data_loader=data_loader, model_factory=model_factory,
            )
        self.assertEqual((output_dir / "reproduction.json").read_bytes(), before)

    def test_an_interrupted_run_stays_incomplete_and_writes_no_result(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = _fixture_registration(
                Path(tmp) / "repo", expectations_extra=_expectations_with_rows(
                    {"init": {}, "adam": {}}
                )
            )
            output_dir = Path(tmp) / "output"
            output_dir.mkdir()
            run_probe = _probe_symbol("run_probe")
            calls = {"data": 0}

            def data_loader(arm_id):
                calls["data"] += 1
                raise RuntimeError("synthetic interruption")

            with self.assertRaises(RuntimeError):
                run_probe(
                    repo / "reg/expectations.json", repo_root=repo, output_dir=output_dir,
                    data_loader=data_loader,
                    model_factory=lambda *args: _scripted_model(
                        [torch.zeros((4, 5))], torch.zeros((4, 9))
                    ),
                )
            self.assertEqual(calls["data"], 1, "no automatic numerical retry is allowed")
            attempt = json.loads((output_dir / "attempt.json").read_text())
            self.assertEqual(attempt["status"], "incomplete")
            self.assertFalse((output_dir / "reproduction.json").exists())

    def test_the_loader_is_called_once_per_arm(self):
        setup = self._setup()
        calls = setup["calls"]
        # One data load per arm (the logger-parity measurement reuses it). Two
        # model builds: the init reconstruction and the trained state — the
        # logger-parity measurement reuses the registered state's cached model.
        self.assertEqual(calls["data"], 1)
        self.assertEqual(calls["models"], 2)

    def test_an_uncommitted_registration_refuses_before_any_access(self):
        run_probe = _probe_symbol("run_probe")
        with tempfile.TemporaryDirectory() as tmp:
            repo = _fixture_registration(Path(tmp) / "repo", kind="dirty")
            output_dir = Path(tmp) / "output"
            output_dir.mkdir()
            with mock.patch.object(torch, "load", side_effect=AssertionError("weights loaded")), \
                    mock.patch(
                        "pinn.verification.diagnostic_data.open_diagnostic_context",
                        side_effect=AssertionError("corpus context opened"),
                    ), mock.patch(
                        "pinn.verification.diagnostic_data.load_diagnostic_data",
                        side_effect=AssertionError("corpus data read"),
                    ):
                with self.assertRaises(Exception):
                    run_probe(
                        repo / "reg/expectations.json", repo_root=repo,
                        output_dir=output_dir,
                        data_loader=lambda arm_id: (_ for _ in ()).throw(
                            AssertionError("data read")),
                        model_factory=lambda *args: (_ for _ in ()).throw(
                            AssertionError("model built")),
                    )
            self.assertFalse((output_dir / "attempt.json").exists())

    def test_the_run_records_zero_attempted_steps_and_matching_digests(self):
        setup = self._setup()
        result = setup["result"]
        self.assertEqual(result["interlock"]["attempted_steps"], 0)
        self.assertEqual(
            result["interlock"]["parameter_digest_before"],
            result["interlock"]["parameter_digest_after"],
        )

    def test_individual_deep_layers_are_recorded_as_new_measurements(self):
        setup = self._setup()
        result = setup["result"]
        deep = [
            entry for entry in result["new_measurements"]
            if entry["field_id"].endswith("/h3")
        ]
        self.assertTrue(deep)
        self.assertTrue(all(entry["status"] == "new_measurement" for entry in deep))

    def test_logger_parity_is_recorded_from_the_registered_state(self):
        setup = self._setup()
        result = setup["result"]
        parity = result["logger_parity"]
        self.assertEqual(parity["arm_id"], "r1-1632")
        self.assertEqual(parity["state"], "adam")
        self.assertEqual(parity["entry"]["point"], "probe-logger-parity")
        self.assertIn("layers", parity["entry"])


class OptimizerInterlockTests(unittest.TestCase):
    """The probe-only interlock: no optimizer construction or step is possible."""

    def test_optimizer_construction_is_refused_under_the_interlock(self):
        interlock = _probe_symbol("optimizer_interlock")
        refused = _probe_symbol("ProbeInterlockRefused")
        with self.assertRaises(refused):
            with interlock():
                torch.optim.Adam([torch.nn.Parameter(torch.zeros(1))], lr=1e-3)

    def test_optimizer_steps_are_refused_under_the_interlock(self):
        interlock = _probe_symbol("optimizer_interlock")
        refused = _probe_symbol("ProbeInterlockRefused")
        optimizer = torch.optim.SGD([torch.nn.Parameter(torch.zeros(1))], lr=0.1)
        with self.assertRaises(refused):
            with interlock():
                optimizer.step()

    def test_construction_works_again_after_the_interlock_releases(self):
        interlock = _probe_symbol("optimizer_interlock")
        with interlock():
            pass
        torch.optim.Adam([torch.nn.Parameter(torch.zeros(1))], lr=1e-3)

    def test_parameter_tampering_during_measurement_is_refused(self):
        run_probe = _probe_symbol("run_probe")
        refused = _probe_symbol("ProbeInterlockRefused")

        class _TamperingBoundary(_ScriptedBoundary):
            def forward(self, _x):
                with torch.no_grad():
                    self.weight.add_(1.0)
                return super().forward(_x)

        rows = torch.zeros((4, 5), dtype=torch.float64)
        tampering = _TamperingBoundary(rows, 0.3, _weight_column([0.5, 1.5, 2.5]))
        with tempfile.TemporaryDirectory() as tmp:
            repo = _fixture_registration(
                Path(tmp) / "repo",
                expectations_extra=_expectations_with_rows({"init": {}, "adam": {}}),
            )
            output_dir = Path(tmp) / "output"
            output_dir.mkdir()
            with self.assertRaises(refused):
                run_probe(
                    repo / "reg/expectations.json", repo_root=repo, output_dir=output_dir,
                    data_loader=lambda arm_id: _samples(4),
                    model_factory=lambda *args: _ScriptedNet(
                        [tampering], torch.zeros((4, 9), dtype=torch.float64)
                    ),
                )
            attempt = json.loads((output_dir / "attempt.json").read_text())
            self.assertEqual(attempt["status"], "incomplete")
            self.assertFalse((output_dir / "reproduction.json").exists())


class ProbeCliTests(unittest.TestCase):
    """The CLI surface: check-registration / run / verify-result flags and exits."""

    def test_check_registration_cli_exits_zero_on_a_committed_registration(self):
        main = _probe_symbol("main")
        with tempfile.TemporaryDirectory() as tmp:
            repo = _fixture_registration(Path(tmp) / "repo")
            self.assertEqual(
                main(
                    ["check-registration", "--registration",
                     str(repo / "reg/expectations.json")],
                    repo_root=str(repo),
                ),
                0,
            )

    def test_check_registration_cli_exits_nonzero_when_uncommitted(self):
        main = _probe_symbol("main")
        with tempfile.TemporaryDirectory() as tmp:
            repo = _fixture_registration(Path(tmp) / "repo", kind="dirty")
            self.assertEqual(
                main(
                    ["check-registration", "--registration",
                     str(repo / "reg/expectations.json")],
                    repo_root=str(repo),
                ),
                2,
            )

    def test_run_cli_refuses_before_any_access_when_uncommitted(self):
        main = _probe_symbol("main")
        with tempfile.TemporaryDirectory() as tmp:
            repo = _fixture_registration(Path(tmp) / "repo", kind="dirty")
            output_dir = Path(tmp) / "output"
            output_dir.mkdir()
            with mock.patch.object(torch, "load", side_effect=AssertionError("weights loaded")), \
                    mock.patch(
                        "pinn.verification.diagnostic_data.open_diagnostic_context",
                        side_effect=AssertionError("corpus context opened"),
                    ):
                self.assertEqual(
                    main(
                        ["run", "--registration", str(repo / "reg/expectations.json"),
                         "--result", str(output_dir / "reproduction.json"),
                         "--output", str(output_dir)],
                        repo_root=str(repo),
                    ),
                    2,
                )
            self.assertFalse((output_dir / "attempt.json").exists())

    def test_run_cli_requires_all_three_flags(self):
        main = _probe_symbol("main")
        with tempfile.TemporaryDirectory() as tmp:
            repo = _fixture_registration(Path(tmp) / "repo")
            self.assertEqual(
                main(["run", "--registration", str(repo / "reg/expectations.json")],
                     repo_root=str(repo)),
                2,
            )

    def test_verify_result_cli_recomputes_the_branch_and_run_commit(self):
        main = _probe_symbol("main")
        setup = self._run_setup()
        repo, output_dir = setup["repo"], setup["output_dir"]
        self.assertEqual(
            main(["verify-result", "--result", str(output_dir / "reproduction.json")],
                 repo_root=str(repo)),
            0,
        )
        # A later committed change to a dependency does NOT invalidate the
        # result: verify checks the recorded run commit, not current bytes.
        (repo / "code_dep.py").write_bytes(b"DEPENDENCY = 2\n")
        subprocess.run(["git", "add", "code_dep.py"], cwd=str(repo), check=True,
                       capture_output=True)
        subprocess.run(["git", "commit", "-q", "-m", "later change"], cwd=str(repo),
                       check=True, capture_output=True)
        self.assertEqual(
            main(["verify-result", "--result", str(output_dir / "reproduction.json")],
                 repo_root=str(repo)),
            0,
        )

    def test_verify_result_refuses_a_result_whose_verdict_was_tampered(self):
        main = _probe_symbol("main")
        setup = self._run_setup()
        repo, output_dir = setup["repo"], setup["output_dir"]
        result = json.loads((output_dir / "reproduction.json").read_text())
        # Record one required field as failed while still claiming the retained
        # branch: the recomputed reading rule contradicts the recorded verdict.
        result["field_verdicts"][0]["status"] = "not_reproduced"
        (output_dir / "tampered.json").write_text(json.dumps(result))
        self.assertEqual(
            main(["verify-result", "--result", str(output_dir / "tampered.json")],
                 repo_root=str(repo)),
            2,
        )

    def test_verify_result_logger_parity_flag_compares_the_recorded_entry(self):
        main = _probe_symbol("main")
        setup = self._run_setup()
        repo, output_dir = setup["repo"], setup["output_dir"]
        parity_path = output_dir / "parity.json"
        parity_path.write_text(json.dumps(setup["result"]["logger_parity"]["entry"]))
        self.assertEqual(
            main(["verify-result", "--result", str(output_dir / "reproduction.json"),
                  "--logger-parity", str(parity_path)],
                 repo_root=str(repo)),
            0,
        )
        altered = dict(setup["result"]["logger_parity"]["entry"])
        altered["point"] = "somewhere-else"
        (output_dir / "parity2.json").write_text(json.dumps(altered))
        self.assertEqual(
            main(["verify-result", "--result", str(output_dir / "reproduction.json"),
                  "--logger-parity", str(output_dir / "parity2.json")],
                 repo_root=str(repo)),
            2,
        )

    def _run_setup(self):
        """One successful synthetic run on a committed fixture, returned once."""
        rows = torch.randn((4, 5), generator=torch.Generator().manual_seed(21), dtype=torch.float64)
        boundaries = [rows, rows.clone(), rows.clone(), rows.flip(0)]
        output_rows = torch.randn((4, 9), generator=torch.Generator().manual_seed(22), dtype=torch.float64)
        model = _scripted_model(boundaries, output_rows, omega_values=(0.3, 1.1, 2.7, 0.9))
        X, masses, targets, times = _samples(4)
        measurement = measure_time_signal(model, X, masses, targets, times)
        fields = {
            "frequency_median": {"formatter": ".2f", "token": format(measurement.frequency_median, ".2f")},
            "adj_h1": {"formatter": ".3f", "token": format(
                [row for row in measurement.layers if row.name == "h1"][0].adjacent_cosine_mean, ".3f")},
            "out_move": {"formatter": ".4f", "token": format(measurement.output_movement, ".4f")},
            "rate_ratio": {"formatter": ".3g", "token": format(measurement.output_rate_ratio, ".3g")},
        }
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        repo = _fixture_registration(
            Path(tmp.name) / "repo",
            expectations_extra=_expectations_with_rows({"init": fields, "adam": fields}),
        )
        output_dir = Path(tmp.name) / "output"
        output_dir.mkdir()
        result = _probe_symbol("run_probe")(
            repo / "reg/expectations.json", repo_root=repo, output_dir=output_dir,
            data_loader=lambda arm_id: (X, masses, targets, times),
            model_factory=lambda *args: _scripted_model(boundaries, output_rows, omega_values=(0.3, 1.1, 2.7, 0.9)),
        )
        return {"repo": repo, "output_dir": output_dir, "result": result}


class RegistrationContentTests(unittest.TestCase):
    """The real registration derives from the preserved stdout and is exact."""

    @classmethod
    def _phase_dir(cls):
        return (
            Path(__file__).resolve().parents[2]
            / ".planning/phases/65-probe-on-the-record-fit-harness"
        )

    @classmethod
    def _registration(cls):
        path = cls._phase_dir() / "evidence/probe/expectations.json"
        if not path.is_file():
            cls.fail("the registration expectations file is missing")
        try:
            return json.loads(path.read_text())
        except ValueError as exc:
            cls.fail(f"expectations.json is not valid JSON: {exc}")

    def _stdout_text(self):
        document = json.loads(
            (self._phase_dir() / "evidence/original/stdout.json").read_text()
        )
        return {m["tool_use_id"]: m["text"] for m in document["messages"]}

    def test_the_registration_names_seven_arms_in_committed_record_order(self):
        doc = self._registration()
        arms = doc["arms"]
        paths = [arm["record"]["path"] for arm in arms]
        self.assertEqual(len(arms), 7)
        self.assertEqual(paths, sorted(paths))
        self.assertEqual(
            [arm["arm_id"] for arm in arms],
            ["g2s-1632-w060", "g2s-1632-w120", "g2s-1632-w240", "g2s-1632-w480",
             "r1-1632", "r1-4658", "r1-851"],
        )
        better = {arm["arm_id"]: arm["better_state"] for arm in arms}
        self.assertEqual(
            better,
            {"g2s-1632-w060": "adam", "g2s-1632-w120": "adam",
             "g2s-1632-w240": "adam", "g2s-1632-w480": "adam",
             "r1-1632": "polish", "r1-4658": "adam", "r1-851": "adam"},
        )

    def test_every_registered_token_appears_in_the_preserved_stdout(self):
        doc = self._registration()
        texts = self._stdout_text()
        joined = "\n".join(texts.values())
        missing = []
        for arm in doc["probe"]["arms"]:
            for row in arm["rows"]:
                for name, entry in row["fields"].items():
                    if entry["token"] not in joined:
                        missing.append(f"{arm['arm_id']}/{row['state']}/{name}")
        for state, entry in doc["probe"]["supplement"]["states"].items():
            for name, field_entry in entry["fields"].items():
                if field_entry["token"] not in joined:
                    missing.append(f"supplement/{state}/{name}")
        self.assertEqual(missing, [])

    def test_every_recorded_cell_matches_its_formatter(self):
        doc = self._registration()
        derive_cell = _probe_symbol("derive_cell")
        checked = 0

        def check(entry, where):
            nonlocal checked
            cell = derive_cell(entry["formatter"], entry["token"])
            self.assertEqual(float.fromhex(entry["cell"]["lo_hex"]), cell["lo"], where)
            self.assertEqual(float.fromhex(entry["cell"]["hi_hex"]), cell["hi"], where)
            self.assertEqual(
                float.fromhex(entry["cell"]["excluded_below_hex"]), cell["excluded_below"], where
            )
            self.assertEqual(
                float.fromhex(entry["cell"]["excluded_above_hex"]), cell["excluded_above"], where
            )
            checked += 1

        for arm in doc["probe"]["arms"]:
            for row in arm["rows"]:
                for name, entry in row["fields"].items():
                    check(entry, f"{arm['arm_id']}/{row['state']}/{name}")
        for state, entry in doc["probe"]["supplement"]["states"].items():
            for name, field_entry in entry["fields"].items():
                check(field_entry, f"supplement/{state}/{name}")
        self.assertGreater(checked, 150)

    def test_the_r1_1632_supplement_keeps_its_individual_h3_values(self):
        doc = self._registration()
        states = doc["probe"]["supplement"]["states"]
        self.assertEqual(states["adam"]["fields"]["adj_h3"]["token"], "0.0186")
        self.assertEqual(states["polish"]["fields"]["adj_h3"]["token"], "0.0177")
        all_rows = {
            (arm["arm_id"], row["state"]): row
            for arm in doc["probe"]["arms"] for row in arm["rows"]
        }
        polish_row = all_rows[("r1-1632", "polish")]
        self.assertEqual(polish_row["fields"]["deep_max"]["token"], "0.018")
        # The all-arm row carries ONLY the range field for the deep layers —
        # no invented individual targets.
        for name in ("adj_h3", "adj_h4", "adj_h5"):
            self.assertNotIn(name, polish_row["fields"])

    def test_other_arms_deep_layers_are_new_measurements_not_targets(self):
        doc = self._registration()
        for arm in doc["probe"]["arms"]:
            if arm["arm_id"] == "r1-1632":
                continue
            for row in arm["rows"]:
                for name in ("adj_h3", "adj_h7", "adj_h12"):
                    self.assertNotIn(name, row["fields"])
                self.assertTrue(row.get("new_measurements"), arm["arm_id"])
        # r1-1632's historical individual values: the init row carries the
        # single-arm init block's per-layer fields, and the Adam/polish
        # supplement carries theirs; the all-arm polish row stays the range.
        rows = {
            row["state"]: row
            for arm in doc["probe"]["arms"] if arm["arm_id"] == "r1-1632"
            for row in arm["rows"]
        }
        self.assertIn("adj_h3", rows["init"]["fields"])
        self.assertNotIn("adj_h3", rows["polish"]["fields"])
        supplement = doc["probe"]["supplement"]["states"]
        self.assertIn("adj_h3", supplement["adam"]["fields"])
        self.assertIn("adj_h3", supplement["polish"]["fields"])
        self.assertFalse(rows["init"].get("new_measurements"))

    def test_preserved_only_fields_carry_their_original_formatters(self):
        doc = self._registration()
        adam = doc["probe"]["supplement"]["states"]["adam"]["fields"]
        self.assertEqual(adam["moving_h1"]["formatter"], ".4f")
        self.assertEqual(adam["moving_h1"]["availability"], "preserved_only")
        self.assertEqual(adam["spike_h12"]["formatter"], ".4f")
        self.assertEqual(adam["skip_siren_h1"]["formatter"], ".1f")

    def test_the_recorded_dependency_and_source_digests_match_disk(self):
        doc = self._registration()
        root = Path(__file__).resolve().parents[2]

        def sha(relative):
            return hashlib.sha256((root / relative).read_bytes()).hexdigest()

        for entry in doc["source"]["scripts"]:
            self.assertEqual(sha(entry["path"]), entry["sha256"], entry["path"])
        for entry in doc["code_dependencies"]:
            self.assertEqual(sha(entry["path"]), entry["sha256"], entry["path"])
        for entry in doc["frozen"]:
            self.assertEqual(sha(entry["path"]), entry["sha256"], entry["path"])
        for arm in doc["arms"]:
            self.assertEqual(sha(arm["record"]["path"]), arm["record"]["sha256"])
            for state, weights in arm["weights"].items():
                self.assertEqual(sha(weights["path"]), weights["sha256"], state)
        self.assertEqual(
            doc["pinned"]["protocol"]["sha256"],
            sha(doc["pinned"]["protocol"]["path"]),
        )

    def test_the_page_is_named_and_the_reading_rule_is_immutable(self):
        doc = self._registration()
        page = self._phase_dir() / "65-PROBE-PREDICTION.md"
        self.assertTrue(page.is_file())
        self.assertEqual(
            hashlib.sha256(page.read_bytes()).hexdigest(), doc["page"]["sha256"]
        )
        self.assertTrue(doc["reading_rule"]["immutable_after_observation"])
        text = page.read_text()
        for branch in ("retained", "withdrawn", "SCOPE-49", "provenance"):
            self.assertIn(branch, text)


if __name__ == "__main__":
    unittest.main()
