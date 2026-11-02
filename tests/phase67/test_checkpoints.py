"""Plan 67-04 task 67-04-01: the registered science checkpoint schedule.

D-08/D-10 (through 67-RESEARCH's budget recommendation): timing and science
share one normalized schedule — five similarity events at 0, N/4, N/2, 3N/4
and N and three frozen ``score_network`` checkpoints at N/2, 3N/4 and N — and
the fit measures those actual costs. The pure Phase 67 cadence, score-cadence
and loss-stride functions, the admission gate that validates the exact
registered schedule before any data or model exists, the fit loop that times
every logger and scorer event individually (synchronized, disjoint from the
synchronized optimizer durations, inside the whole-run deadline), the
endpoint score reused from the final checkpoint without a fourth scoring
call, and the registration-bound verification of the recorded checkpoints
are proven here on the synthetic seam. The historical default path — no
score cadence — is proven unchanged. No real corpus, no MPS device and no
real orbit is ever reached.
"""

from __future__ import annotations

import copy
import json
import shutil
import tempfile
import unittest
from contextlib import ExitStack
from pathlib import Path
from types import SimpleNamespace
from unittest import mock

import pinn.verification.diagnostic_fit as fit_module
from pinn.verification.diagnostic_fit import (
    DiagnosticFitRefused,
    validate_smoke_settings,
    verify_fit_result,
)
from tests.phase60._fixtures import gold_corpus_fixture
from tests.phase65.test_fit_short import _loaded, _smoke_settings
from tests.phase67._fixtures import (
    fake_clock,
    fake_pmset,
    inline_supervisor,
    patch_data_seam,
    phase67_fixture_registration,
    phase67_settings,
)

#: The registered schedule at the small synthetic scale: N = 100 (the smallest
#: step count the Phase 67 cadence is defined at), 20 warmup, the five
#: normalized similarity events and the three frozen-score checkpoints, under
#: the registered 900-second timing cap.
STEPS = 100
WARMUP = 20
CADENCE = [0, 25, 50, 75, STEPS]
SCORE_CADENCE = [50, 75, STEPS]
STRIDE = 1  # ceil(100 / 1000)
CAP = 900.0


def _p67():
    """The new module, imported lazily so a missing module fails per test."""
    from pinn.verification import diagnostic_phase67

    return diagnostic_phase67


def _schedule_settings(**overrides):
    """Phase 67 fixture settings carrying the exact registered schedule."""
    settings = phase67_settings(
        optimizer_steps=STEPS,
        warmup_steps=WARMUP,
        measured_steps=STEPS - WARMUP,
        similarity_cadence=list(CADENCE),
        score_cadence=list(SCORE_CADENCE),
        loss_trace_stride=STRIDE,
        whole_run_cap_seconds=CAP,
    )
    settings.update(overrides)
    return settings


def _attested(spec, context, data):
    """The verify gate's access evidence, the tracer's shim."""
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
    return context


class CadenceTests(unittest.TestCase):
    """The pure schedule functions and the registered budget-rule numbers."""

    def test_similarity_cadence_is_the_five_normalized_events(self):
        p67 = _p67()
        self.assertEqual(p67.phase67_cadence(1200), [0, 300, 600, 900, 1200])
        self.assertEqual(p67.phase67_cadence(300), [0, 75, 150, 225, 300])
        for n in (300, 1000, 1200, 26800, 100000):
            with self.subTest(n=n):
                self.assertEqual(
                    p67.phase67_cadence(n), [0, n // 4, n // 2, 3 * n // 4, n]
                )

    def test_similarity_cadence_refuses_non_quantum_step_counts(self):
        p67 = _p67()
        for bad in (0, -100, 20, 250, True, 100.0, "100", None):
            with self.subTest(bad=bad):
                with self.assertRaises(ValueError):
                    p67.phase67_cadence(bad)

    def test_score_cadence_is_the_three_frozen_score_events(self):
        p67 = _p67()
        self.assertEqual(p67.phase67_score_cadence(1200), [600, 900, 1200])
        for n in (300, 1200, 40000):
            with self.subTest(n=n):
                score = p67.phase67_score_cadence(n)
                self.assertEqual(score, [n // 2, 3 * n // 4, n])
                self.assertTrue(set(score) <= set(p67.phase67_cadence(n)))
        for bad in (20, 250, 0, None, True):
            with self.subTest(bad=bad):
                with self.assertRaises(ValueError):
                    p67.phase67_score_cadence(bad)

    def test_loss_trace_stride_is_ceil_n_over_1000_with_at_most_1001_entries(self):
        p67 = _p67()
        self.assertEqual(p67.phase67_loss_trace_stride(1000), 1)
        self.assertEqual(p67.phase67_loss_trace_stride(1001), 2)
        self.assertEqual(p67.phase67_loss_trace_stride(1200), 2)
        self.assertEqual(p67.phase67_loss_trace_stride(268000), 268)
        for bad in (0, -1, None, True, 100.0):
            with self.subTest(bad=bad):
                with self.assertRaises(ValueError):
                    p67.phase67_loss_trace_stride(bad)

        def thinning(n, stride):
            trace = list(range(n))[stride - 1::stride]
            if n % stride:
                trace = trace + [n - 1]
            return trace

        for n in range(1, 4002):
            stride = p67.phase67_loss_trace_stride(n)
            with self.subTest(n=n):
                trace = thinning(n, stride)
                self.assertLessEqual(len(trace), 1001, f"n={n}")
                self.assertEqual(trace[-1], n - 1)
        for k in range(1, 401):
            for n in (k * 1000 - 1, k * 1000, k * 1000 + 1):
                stride = p67.phase67_loss_trace_stride(n)
                self.assertLessEqual(
                    p67.phase67_loss_trace_entries(n, stride), 1001, f"n={n}"
                )
                self.assertEqual(
                    len(thinning(n, stride)),
                    p67.phase67_loss_trace_entries(n, stride),
                    f"n={n}",
                )
        for n in (1000000, 5000000):
            stride = p67.phase67_loss_trace_stride(n)
            self.assertLessEqual(p67.phase67_loss_trace_entries(n, stride), 1001)

    def test_the_budget_rule_pins_the_registered_numbers(self):
        p67 = _p67()
        rule = p67.PHASE67_BUDGET_RULE
        self.assertEqual(rule["cap_seconds"], 3540.0)
        self.assertEqual(rule["time_fraction"], 0.75)
        self.assertEqual(rule["rate_margin"], 0.25)
        self.assertEqual(rule["warmup_steps"], 200)
        self.assertEqual(rule["step_quantum"], 100)
        self.assertEqual(rule["min_steps"], 300)
        self.assertEqual(rule["similarity_events"], 5)
        self.assertEqual(rule["score_events"], 3)
        self.assertEqual(rule["loss_trace_entries_max"], 1000)
        self.assertEqual(rule["loss_entry_bytes"], 32)
        self.assertEqual(rule["residual_tolerance"], 1e-9)
        self.assertEqual(rule["size_limit_bytes"], 10485760)
        self.assertEqual(rule["size_fraction"], 0.9)
        # The rule's own timing run carries the same normalized schedule.
        self.assertEqual(rule["timing_steps"], 1200)
        self.assertEqual(rule["timing_warmup"], 200)
        self.assertEqual(rule["timing_measured"], 1000)
        self.assertEqual(rule["timing_cap_seconds"], 900.0)
        self.assertEqual(
            p67.phase67_cadence(rule["timing_steps"]), [0, 300, 600, 900, 1200]
        )
        self.assertEqual(
            p67.phase67_score_cadence(rule["timing_steps"]), [600, 900, 1200]
        )


class ScoreCadenceAdmissionTests(unittest.TestCase):
    """``validate_smoke_settings`` admits exactly the registered schedule."""

    def test_the_registered_schedule_admits_before_any_data_access(self):
        doc = {"settings": _schedule_settings()}
        settings, variant, orbit_key, runtime = validate_smoke_settings(doc)
        self.assertEqual(settings["score_cadence"], SCORE_CADENCE)
        self.assertEqual(variant.name, "exp02-d2-w256-o30")
        self.assertEqual(orbit_key.record_id, 0)
        # The runtime pair is the named (dtype, device).
        self.assertEqual(str(runtime[1]), "cpu")

    def test_a_wrong_score_cadence_refuses(self):
        for bad in ([25, 75, 100], [50, 100], [50, 75, 100, 100], [0, 75, 100]):
            with self.subTest(bad=bad):
                with self.assertRaises(DiagnosticFitRefused) as raised:
                    validate_smoke_settings(
                        {"settings": _schedule_settings(score_cadence=list(bad))}
                    )
                self.assertIn("score cadence", str(raised.exception))

    def test_score_cadence_on_a_non_phase67_registration_refuses(self):
        settings = _smoke_settings(
            optimizer_steps=STEPS,
            warmup_steps=WARMUP,
            measured_steps=STEPS - WARMUP,
            similarity_cadence=list(CADENCE),
            score_cadence=list(SCORE_CADENCE),
            loss_trace_stride=STRIDE,
        )
        with self.assertRaises(DiagnosticFitRefused) as raised:
            validate_smoke_settings({"settings": settings})
        self.assertIn("Phase 67", str(raised.exception))

    def test_a_schedule_with_a_foreign_similarity_cadence_refuses(self):
        foreign = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
        with self.assertRaises(DiagnosticFitRefused) as raised:
            validate_smoke_settings(
                {"settings": _schedule_settings(similarity_cadence=foreign)}
            )
        self.assertIn("similarity", str(raised.exception).lower())

    def test_a_schedule_without_the_bounded_stride_refuses(self):
        with self.assertRaises(DiagnosticFitRefused) as raised:
            validate_smoke_settings(
                {"settings": _schedule_settings(loss_trace_stride=7)}
            )
        self.assertIn("stride", str(raised.exception))

    def test_a_step_count_off_the_quantum_refuses(self):
        with self.assertRaises(DiagnosticFitRefused):
            validate_smoke_settings({
                "settings": phase67_settings(
                    optimizer_steps=90,
                    warmup_steps=20,
                    measured_steps=70,
                    similarity_cadence=[0, 22, 45, 67, 90],
                    score_cadence=[45, 67, 90],
                    loss_trace_stride=1,
                    whole_run_cap_seconds=CAP,
                )
            })


class RegisteredScheduleRunTests(unittest.TestCase):
    """One synthetic registered 100-step run through the exact schedule."""

    @classmethod
    def setUpClass(cls):
        stack = ExitStack()
        cls.addClassCleanup(stack.close)
        fixture = stack.enter_context(gold_corpus_fixture())
        tmp = Path(stack.enter_context(
            tempfile.TemporaryDirectory(prefix="phase67-checkpoints-")
        ))
        spec, context, _scorecard, data = _loaded(fixture)
        context = _attested(spec, context, data)
        root, _commit = phase67_fixture_registration(
            tmp / "repo", **_schedule_settings()
        )
        cls.root = root
        cls.registration = root / "reg/smoke-registration.json"
        cls.output = root / "evidence/schedule/record.json"

        import pinn.verification.diagnostic_power as power

        def runner(argv, *, cwd):
            patch_data_seam(stack, context, data, spec)
            real_score = fit_module.score_network
            real_log = fit_module.log_similarity
            with mock.patch.object(
                fit_module, "score_network", wraps=real_score
            ) as cls.score_spy, mock.patch.object(
                fit_module, "log_similarity", wraps=real_log
            ) as cls.log_spy:
                cls.run_code = fit_module.main(
                    argv[6:], repo_root=root, supervisor=inline_supervisor
                )
            return cls.run_code

        cls.launch_code = power.launch(
            cls.registration, cls.output, repo_root=root,
            read_power=fake_pmset("Now drawing from 'AC Power'"), run=runner,
            now=fake_clock("2026-10-31T12:00:00-05:00"),
        )
        cls.record = json.loads(cls.output.read_bytes())
        cls.run_dir = cls.output.parent

    def test_the_launch_completed_the_registered_schedule(self):
        self.assertEqual(self.launch_code, 0)
        self.assertEqual(self.run_code, 0)
        record = self.record
        self.assertEqual(record["status"], "complete")
        self.assertEqual(record["steps"]["completed"], STEPS)
        self.assertEqual(record["similarity"]["cadence"], CADENCE)
        self.assertEqual(
            [entry["step"] for entry in record["similarity"]["entries"]], CADENCE
        )

    def test_exactly_five_logger_and_three_scorer_events_fire(self):
        self.assertEqual(self.log_spy.call_count, 5)
        self.assertEqual(self.score_spy.call_count, 3)
        events = self.record["timing"]["events"]
        self.assertEqual([event["step"] for event in events["logging"]], CADENCE)
        self.assertEqual(
            [event["step"] for event in events["scoring"]], SCORE_CADENCE
        )

    def test_score_checkpoints_carry_the_frozen_score_and_elapsed(self):
        checkpoints = self.record["score_checkpoints"]
        self.assertEqual([c["step"] for c in checkpoints], SCORE_CADENCE)
        elapsed = []
        for checkpoint in checkpoints:
            score = checkpoint["score"]
            self.assertIn("E", score)
            self.assertIn("tier", score)
            self.assertIsInstance(score["tier"], int)
            value = score["E"]
            self.assertIsNot(value, True)
            self.assertIsInstance(value, (int, float))
            self.assertGreaterEqual(float(value), 0.0)
            self.assertIsInstance(checkpoint["elapsed_seconds"], float)
            self.assertGreaterEqual(checkpoint["elapsed_seconds"], 0.0)
            elapsed.append(checkpoint["elapsed_seconds"])
        self.assertEqual(elapsed, sorted(elapsed))
        self.assertLessEqual(
            elapsed[-1], self.record["timing"]["total_wall_seconds"] + 1e-6
        )

    def test_the_final_checkpoint_supplies_the_endpoint_score(self):
        self.assertEqual(self.score_spy.call_count, 3)  # no fourth scoring call
        self.assertEqual(
            self.record["scores"]["network"],
            self.record["score_checkpoints"][-1]["score"],
        )

    def test_event_costs_are_disjoint_from_the_optimizer_durations(self):
        timing = self.record["timing"]
        events = timing["events"]
        log_events = events["logging"]
        score_events = events["scoring"]
        self.assertEqual(len(log_events), 5)
        self.assertEqual(len(score_events), 3)
        for event in log_events + score_events:
            self.assertGreater(event["seconds"], 0.0)
        log_total = sum(event["seconds"] for event in log_events)
        score_total = sum(event["seconds"] for event in score_events)
        self.assertAlmostEqual(
            timing["phases"]["logging_seconds"], log_total, places=9
        )
        self.assertGreaterEqual(timing["phases"]["scoring_seconds"], score_total)
        self.assertEqual(
            events["publication_io"][0]["seconds"],
            timing["phases"]["publish_seconds"],
        )
        # Disjointness: the synchronized optimizer segments plus every timed
        # in-loop event fit inside the loop wall; the step-0 log event precedes
        # the loop and so is excluded here.
        in_loop = (
            timing["warmup_seconds"]
            + timing["measured_seconds"]
            + sum(event["seconds"] for event in log_events if event["step"] > 0)
            + score_total
        )
        self.assertLessEqual(in_loop, timing["wall_seconds"] + 1e-6)

    def test_the_record_bounds_its_loss_trace_at_the_registered_stride(self):
        loss = self.record["loss"]
        self.assertEqual(loss["trace_stride"], STRIDE)
        self.assertEqual(len(loss["trace"]), STEPS)  # stride 1 keeps every loss
        self.assertEqual(loss["trace"][-1], loss["final"])

    def test_the_registered_schedule_verifies(self):
        report = verify_fit_result(
            self.registration, self.output, repo_root=self.root
        )
        self.assertTrue(report["verified"])

    def test_tampered_score_checkpoints_refuse_verification(self):
        for mutation, fragment in (
            ("steps", "score checkpoints"),
            ("score", "final score checkpoint"),
        ):
            with self.subTest(mutation=mutation):
                tampered = copy.deepcopy(self.record)
                if mutation == "steps":
                    tampered["score_checkpoints"][0]["step"] = 25
                else:
                    tampered["score_checkpoints"][-1]["score"]["E"] = 4.0
                target = self.run_dir.parent / f"tampered-{mutation}"
                target.mkdir(parents=True, exist_ok=True)
                (target / "record.json").write_bytes(
                    json.dumps(tampered, indent=2, sort_keys=True).encode("utf-8")
                    + b"\n"
                )
                shutil.copy2(
                    self.run_dir / "diagnostic.weights",
                    target / "diagnostic.weights",
                )
                with self.assertRaises(DiagnosticFitRefused) as raised:
                    verify_fit_result(
                        self.registration, target / "record.json", repo_root=self.root
                    )
                self.assertIn(fragment, str(raised.exception))


class ScheduleDeadlineTests(unittest.TestCase):
    """The whole-run deadline covers the checkpoint events themselves."""

    def test_a_deadline_expiry_at_a_checkpoint_refuses_and_publishes_nothing(self):
        stack = ExitStack()
        self.addCleanup(stack.close)
        fixture = stack.enter_context(gold_corpus_fixture())
        root = Path(stack.enter_context(
            tempfile.TemporaryDirectory(prefix="phase67-deadline-")
        ))
        spec, context, scorecard, data = _loaded(fixture)
        from pinn.verification.diagnostic_phase67_catalog import PHASE67_REGISTRY

        # A deterministic clock: everything runs at t = 0 until the first
        # frozen-score checkpoint completes, after which the clock jumps past
        # the deadline, so the after-event check is exactly what fires.
        state = {"expired": False}

        def fake_clock():
            return 1e6 if state["expired"] else 0.0

        real_score = fit_module.score_network

        def scoring_then_expire(*args, **kwargs):
            result = real_score(*args, **kwargs)
            state["expired"] = True
            return result

        with mock.patch.object(
            fit_module, "score_network", side_effect=scoring_then_expire
        ):
            with self.assertRaises(DiagnosticFitRefused) as raised:
                fit_module.fit_diagnostic(
                    PHASE67_REGISTRY["exp02-d2-w256-o30"],
                    data,
                    context=context,
                    scorecard=scorecard,
                    runtime=("float64", "cpu"),
                    out_dir=root / "run",
                    steps=STEPS,
                    warmup_steps=WARMUP,
                    cadence=list(CADENCE),
                    score_cadence=list(SCORE_CADENCE),
                    loss_trace_stride=STRIDE,
                    deadline_seconds=100.0,
                    seed=42,
                    variant_registry="phase67",
                    clock=fake_clock,
                )
        self.assertIn(
            "frozen-score checkpoint at step 50", str(raised.exception)
        )
        self.assertEqual(list(root.rglob("*")), [])


class HistoricalPathControls(unittest.TestCase):
    """A fit without a registered score cadence gains no new fields or events."""

    @classmethod
    def setUpClass(cls):
        stack = ExitStack()
        cls.addClassCleanup(stack.close)
        fixture = stack.enter_context(gold_corpus_fixture())
        tmp = Path(stack.enter_context(
            tempfile.TemporaryDirectory(prefix="phase67-historical-")
        ))
        spec, context, _scorecard, data = _loaded(fixture)
        context = _attested(spec, context, data)
        root, _commit = phase67_fixture_registration(
            tmp / "repo",
            optimizer_steps=4,
            warmup_steps=2,
            measured_steps=2,
            similarity_cadence=[0, 4],
        )
        cls.root = root
        cls.registration = root / "reg/smoke-registration.json"
        cls.output = root / "evidence/historical/record.json"

        import pinn.verification.diagnostic_power as power

        def runner(argv, *, cwd):
            patch_data_seam(stack, context, data, spec)
            return fit_module.main(
                argv[6:], repo_root=root, supervisor=inline_supervisor
            )

        cls.launch_code = power.launch(
            cls.registration, cls.output, repo_root=root,
            read_power=fake_pmset("Now drawing from 'AC Power'"), run=runner,
            now=fake_clock("2026-10-31T12:00:00-05:00"),
        )
        cls.record = json.loads(cls.output.read_bytes())
        cls.run_dir = cls.output.parent

    def test_the_run_completes_with_the_historical_shape(self):
        self.assertEqual(self.launch_code, 0)
        record = self.record
        self.assertEqual(record["status"], "complete")
        self.assertEqual(record["steps"]["completed"], 4)
        self.assertNotIn("score_checkpoints", record)
        self.assertNotIn("events", record["timing"])
        self.assertIsNone(record["loss"].get("trace_stride"))
        self.assertIn("logging_seconds", record["timing"]["phases"])
        self.assertIn("scoring_seconds", record["timing"]["phases"])

    def test_the_historical_run_verifies(self):
        report = verify_fit_result(
            self.registration, self.output, repo_root=self.root
        )
        self.assertTrue(report["verified"])

    def test_unregistered_score_checkpoints_refuse_verification(self):
        tampered = copy.deepcopy(self.record)
        tampered["score_checkpoints"] = [
            {"step": 2, "score": {"E": 1.0, "tier": 0}, "elapsed_seconds": 0.5},
            {"step": 4, "score": {"E": 0.5, "tier": 0}, "elapsed_seconds": 0.9},
        ]
        target = self.run_dir.parent / "tampered-unregistered"
        target.mkdir(parents=True, exist_ok=True)
        (target / "record.json").write_bytes(
            json.dumps(tampered, indent=2, sort_keys=True).encode("utf-8") + b"\n"
        )
        shutil.copy2(
            self.run_dir / "diagnostic.weights", target / "diagnostic.weights"
        )
        with self.assertRaises(DiagnosticFitRefused) as raised:
            verify_fit_result(
                self.registration, target / "record.json", repo_root=self.root
            )
        self.assertIn(
            "score checkpoints its registration does not declare",
            str(raised.exception),
        )


if __name__ == "__main__":
    unittest.main()
