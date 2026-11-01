"""Plan 66-01 (EXP-01 Wave 0 tracer): one synthetic EXP-01 run end to end.

A committed fixture registration naming the Phase 66 registry and the EXP-01
variant is admitted through the existing Phase 65 admission door, launched
through the diagnostic_power AC gate (an injected pmset reader and an injected
runner), fitted on the synthetic gold corpus with a thinned loss-trace stride,
published as an exclusive record that verify_fit_result accepts, and read
through the EXP-01 reading-rule classifier. A battery reading refuses before
anything is created. No real corpus, no MPS device and no real orbit is ever
reached; the helpers import only plain functions and classes from
tests.phase65.test_fit_short, never a unittest.TestCase subclass, so
discovering tests/phase66 never re-runs Phase 65 classes.
"""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from contextlib import ExitStack
from pathlib import Path
from types import SimpleNamespace
from unittest import mock

import pinn.verification.diagnostic_fit as fit_module
from pinn.verification.diagnostic_fit import (
    DiagnosticFitRefused,
    require_committed_smoke_registration,
    verify_fit_result,
)
from tests.phase60._fixtures import gold_corpus_fixture
from tests.phase65.test_fit_short import (
    _InlineQueue,
    _fit_registration_fixture,
    _loaded,
    _smoke_settings,
)


def phase66_settings(**overrides):
    """The Phase 65 fixture settings carrying the EXP-01 variant and registry.

    The variant block is built through the sealed Phase 65 variant class so a
    RED run fails at the sealed-catalog door (the Phase 66 catalog does not
    exist yet); admission's byte-agreement loop ties the block to the registry
    entry, and the catalog tests pin EXP01_VARIANT to the same fields.
    """
    from pinn.verification.diagnostic_variants import DiagnosticVariant

    variant = DiagnosticVariant(
        name="exp01-d1-w384-o1000",
        time_features="raw_tau_ic13",
        depth=1,
        width=384,
        learning_rate=1e-4,
        window_length=10.0,
        first_omega_0=1000.0,
    )
    extra = {"variant": variant.to_json_dict(), "variant_registry": "phase66"}
    extra.update(overrides)
    return _smoke_settings(**extra)


def phase66_fixture_registration(root, **settings_extra):
    """A committed fixture registration with the EXP-01 variant and registry."""
    return _fit_registration_fixture(
        root, settings_extra=phase66_settings(**settings_extra)
    )


def patch_data_seam(stack, context, data, spec):
    """Route the run body to the fixture data seam on both harness modules.

    Exactly AttemptOwnershipTests._patched_data: open_diagnostic_context,
    load_diagnostic_data and one_orbit_spec are patched on
    pinn.verification.diagnostic_fit and on pinn.verification.diagnostic_data.
    """
    import pinn.verification.diagnostic_data as diagnostic_data

    for module in (fit_module, diagnostic_data):
        stack.enter_context(mock.patch.object(
            module, "open_diagnostic_context", create=True,
            return_value=context,
        ))
        stack.enter_context(mock.patch.object(
            module, "load_diagnostic_data", create=True, return_value=data,
        ))
        stack.enter_context(mock.patch.object(
            module, "one_orbit_spec", create=True, return_value=spec,
        ))
    return stack


def inline_supervisor(target, args, *, timeout, **kwargs):
    """Run the supervised worker in-process over an _InlineQueue."""
    queue = _InlineQueue()
    target(*args, queue)
    return ("exited", queue.payload)


def fake_pmset(first_line):
    """An injectable pmset reader whose stdout begins with ``first_line``."""

    def read_power():
        return first_line + "\n"

    return read_power


def fake_clock(iso_text):
    """An injectable weekend-window clock giving the aware datetime in ``iso_text``.

    The tracer runs on every weekday, so both launch cases inject a Saturday
    in America/Chicago (plan 66-02's weekend window, D-08).
    """
    from datetime import datetime

    moment = datetime.fromisoformat(iso_text)
    return lambda: moment


class Phase66TracerTests(unittest.TestCase):
    """The tracer: the AC case runs one synthetic EXP-01 run end to end and a
    battery reading refuses before anything is created."""

    def test_the_ac_case_runs_one_synthetic_exp01_run_end_to_end(self):
        stack = ExitStack()
        self.addCleanup(stack.close)
        fixture = stack.enter_context(gold_corpus_fixture())
        tmp = Path(stack.enter_context(
            tempfile.TemporaryDirectory(prefix="phase66-tracer-")
        ))
        spec, context, _scorecard, data = _loaded(fixture)
        # The verify gate requires access evidence: give the fixture context a
        # summary-capable attestation and a Stage-0 style reader summary, the
        # VerifyResultTests.setUp pattern.
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
        root, _commit = phase66_fixture_registration(tmp / "repo", loss_trace_stride=3)
        registration = root / "reg/smoke-registration.json"
        output = root / "evidence/ac/record.json"

        # The admission door: the committed phase 66 registration admits
        # through the existing Phase 65 gate before anything else runs.
        try:
            require_committed_smoke_registration(registration, repo_root=root)
        except DiagnosticFitRefused as exc:
            self.fail(f"the phase 66 registration refused admission: {exc}")

        # The launch path: on AC the receipt is written and the fit CLI runs
        # in-process, with the inline supervisor and the patched data seam.
        import pinn.verification.diagnostic_power as power
        from pinn.verification.diagnostic_phase66 import classify_exp01, tier1_e_max
        from pinn.verification.feasibility_scorecard import load_scorecard

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
        self.assertEqual(record["variant"]["registry"], "phase66")
        self.assertIs(record["variant"]["registered"], True)
        for entry in record["similarity"]["entries"]:
            self.assertEqual(
                [row["name"] for row in entry["layers"]], ["input", "h1"]
            )
        self.assertEqual(record["steps"]["completed"], 20)
        self.assertEqual(record["loss"]["trace_stride"], 3)
        self.assertEqual(len(record["loss"]["trace"]), 7)
        self.assertEqual(record["loss"]["trace"][-1], record["loss"]["final"])

        report = verify_fit_result(registration, output, repo_root=root)
        self.assertTrue(report["verified"])

        e_const = next(
            row["score"]["E"] for row in record["comparisons"]
            if row["comparison"] == "window_mean_constant"
        )
        label = classify_exp01(
            record["scores"]["network"]["E"],
            e_const,
            tier1_max=tier1_e_max(load_scorecard()),
        )
        self.assertIn(label, ("tier1", "near", "between", "other"))

    def test_the_battery_case_refuses_before_anything_is_created(self):
        stack = ExitStack()
        self.addCleanup(stack.close)
        tmp = Path(stack.enter_context(
            tempfile.TemporaryDirectory(prefix="phase66-battery-")
        ))
        root, _commit = phase66_fixture_registration(tmp / "repo")
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
