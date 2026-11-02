"""Plan 67-01 (Phase 67 tracer): one synthetic registered depth-2 run end to end.

A committed fixture registration naming the Phase 67 registry and the EXP-02
depth-2 declaration (width 256, raw [tau, IC13], first omega 30, the locked
hidden omega, rate 1e-4 and the [0, 10] window, per D-03) is admitted through
the existing Phase 65 admission door, launched through the diagnostic_power AC
gate (an injected pmset reader, weekend clock and runner), fitted on the
synthetic gold corpus with a thinned loss-trace stride, published as an
exclusive record and marked weight payload that verify_fit_result accepts, and
read through the new registration-bound Phase 67 reader with the input and
both hidden layer rows present in every similarity entry. A battery reading
refuses before anything is created. No real corpus, no MPS device and no real
orbit is ever reached; the shared helpers live in ``tests.phase67._fixtures``
and import only plain functions and classes, never a ``unittest.TestCase``
subclass, so discovering tests/phase67 never re-runs Phase 65 classes.
"""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from contextlib import ExitStack
from pathlib import Path
from types import SimpleNamespace

import pinn.verification.diagnostic_fit as fit_module
from pinn.verification.diagnostic_fit import (
    DiagnosticFitRefused,
    require_committed_smoke_registration,
    verify_fit_result,
)
from tests.phase60._fixtures import gold_corpus_fixture
from tests.phase65.test_fit_short import _loaded
from tests.phase67._fixtures import (
    fake_clock,
    fake_pmset,
    inline_supervisor,
    patch_data_seam,
    phase67_fixture_registration,
)


class Phase67TracerTests(unittest.TestCase):
    """The tracer: the AC case runs one synthetic registered Phase 67 depth-2
    run end to end and a battery reading refuses before anything is created."""

    def test_the_ac_case_runs_one_synthetic_phase67_run_end_to_end(self):
        stack = ExitStack()
        self.addCleanup(stack.close)
        fixture = stack.enter_context(gold_corpus_fixture())
        tmp = Path(stack.enter_context(
            tempfile.TemporaryDirectory(prefix="phase67-tracer-")
        ))
        spec, context, _scorecard, data = _loaded(fixture)
        # The verify gate requires access evidence: give the fixture context a
        # summary-capable attestation and a Stage-0 style reader summary, the
        # Phase 66 tracer pattern.
        if context.attestation is None:
            context = SimpleNamespace(
                **{
                    **vars(context),
                    "attestation": SimpleNamespace(
                        summary=lambda: {"test_split_opens": 0, "withheld_refusals": 0}
                    ),
                }
            )
        if not hasattr(context.reader, "access_summary"):
            context.reader.access_summary = lambda: {
                "requested": [], "opened": [], "refused_before_open": 0,
                "actual_opens": 1,
            }
        root, _commit = phase67_fixture_registration(tmp / "repo", loss_trace_stride=3)
        registration = root / "reg/smoke-registration.json"
        output = root / "evidence/ac/record.json"

        # The admission door: the committed Phase 67 registration admits
        # through the existing Phase 65 gate before anything else runs.
        try:
            require_committed_smoke_registration(registration, repo_root=root)
        except DiagnosticFitRefused as exc:
            self.fail(f"the phase 67 registration refused admission: {exc}")

        # The launch path: on AC the receipt is written and the fit CLI runs
        # in-process, with the inline supervisor and the patched data seam.
        import pinn.verification.diagnostic_power as power

        argv_seen = []

        def runner(argv, *, cwd):
            argv_seen.append(list(argv))
            self.assertEqual(
                argv,
                ["/usr/bin/caffeinate", "-is", sys.executable, "-B", "-m",
                 "pinn.verification.diagnostic_fit", "run",
                 "--registration", str(registration.resolve()),
                 "--output", str(output.resolve())],
            )
            patch_data_seam(stack, context, data, spec)
            return fit_module.main(
                argv[6:], repo_root=root, supervisor=inline_supervisor
            )

        code = power.launch(
            registration, output, repo_root=root,
            read_power=fake_pmset("Now drawing from 'AC Power'"), run=runner,
            now=fake_clock("2026-10-31T12:00:00-05:00"),
        )
        self.assertEqual(code, 0)
        self.assertEqual(len(argv_seen), 1)

        receipt = json.loads((output.parent / "power-gate.json").read_bytes())
        self.assertEqual(receipt["power_source"], "AC Power")
        self.assertEqual(receipt["registration"], "reg/smoke-registration.json")
        self.assertEqual(receipt["output"], "evidence/ac/record.json")

        record = json.loads(output.read_bytes())
        self.assertEqual(record["status"], "complete")
        self.assertEqual(record["variant"]["registry"], "phase67")
        self.assertIs(record["variant"]["registered"], True)
        self.assertEqual(record["variant"]["name"], "exp02-d2-w256-o30")
        # Every similarity entry carries the input row and both hidden rows,
        # in order (D-11: every-layer logging at depth 2).
        for entry in record["similarity"]["entries"]:
            self.assertEqual(
                [row["name"] for row in entry["layers"]], ["input", "h1", "h2"]
            )
        self.assertEqual(record["steps"]["completed"], 20)
        self.assertEqual(record["loss"]["trace_stride"], 3)
        self.assertEqual(len(record["loss"]["trace"]), 7)
        self.assertEqual(record["loss"]["trace"][-1], record["loss"]["final"])
        self.assertIsNotNone(record["access"]["attestation"])

        # The published weights are the intrinsically marked diagnostic
        # payload for the registered variant, never a bare state dict.
        from pinn.verification.diagnostic_guard import read_diagnostic_weights

        payload = read_diagnostic_weights(output.parent / "diagnostic.weights")
        self.assertIs(payload["diagnostic"], True)
        self.assertEqual(payload["variant"]["name"], "exp02-d2-w256-o30")

        report = verify_fit_result(registration, output, repo_root=root)
        self.assertTrue(report["verified"])

        # The registration-bound Phase 67 reader: a clean audit with the
        # registered identity, and both frozen comparisons once scores are
        # requested.
        from pinn.verification.diagnostic_phase67_records import read_phase67_record

        reading = read_phase67_record(registration, output.parent, repo_root=root)
        self.assertEqual(reading["mechanical_problems"], [])
        self.assertEqual(reading["setting_problems"], [])
        self.assertEqual(reading["variant"]["name"], "exp02-d2-w256-o30")
        self.assertEqual(reading["variant"]["registry"], "phase67")
        self.assertEqual(reading["variant"]["depth"], 2)
        self.assertEqual(reading["orbit_key"], "hierarchical/gold/0")
        self.assertEqual(reading["seed"], 42)
        self.assertEqual(reading["layers"], ["input", "h1", "h2"])
        self.assertNotIn("scores", reading)

        scored = read_phase67_record(
            registration, output.parent, repo_root=root, include_scores=True
        )
        self.assertIn("E", scored["scores"]["network"])
        self.assertIn("tier", scored["scores"]["network"])
        self.assertEqual(
            {row["comparison"] for row in scored["scores"]["comparisons"]},
            {"window_mean_constant", "two_kepler"},
        )

    def test_the_battery_case_refuses_before_anything_is_created(self):
        stack = ExitStack()
        self.addCleanup(stack.close)
        tmp = Path(stack.enter_context(
            tempfile.TemporaryDirectory(prefix="phase67-battery-")
        ))
        root, _commit = phase67_fixture_registration(tmp / "repo")
        registration = root / "reg/smoke-registration.json"
        output = root / "evidence/battery/record.json"
        import pinn.verification.diagnostic_power as power

        def runner(argv, *, cwd):
            raise AssertionError("the launcher started a fit on battery")

        code = power.launch(
            registration, output, repo_root=root,
            read_power=fake_pmset("Now drawing from 'Battery Power'"), run=runner,
            now=fake_clock("2026-10-31T12:00:00-05:00"),
        )
        self.assertEqual(code, 2)
        self.assertFalse(output.parent.exists())
