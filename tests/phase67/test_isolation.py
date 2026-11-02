"""Plan 67-06 task 67-06-02: the real metadata and launch isolation gates.

Every real Phase 67 operation is admitted only through the complete chain:
the existing AC-power and weekend-window eligibility plus the new full-cap
remaining-window admission (exact equality admitted, the next instant
refused, DST-exact through UTC arithmetic), a writable-space check against
the registered evidence byte bound, the committed pins, and the exclusive
one-row claim — all before any protected work. A deadline that fires during
admission, metadata, logging, scoring or publication leaves incomplete
evidence and never an accepted success; the outer supervisor owns its
process group, so no caffeinate/fit descendant survives a supervised stop;
and the metadata receipt carries enough aware-time evidence to recheck its
remaining allowance independently. No real corpus or weekend launch is ever
reached: the data and power seams are injected, and the real reader seam is
a tripwire.
"""

from __future__ import annotations

import contextlib
import io
import json
import math
import os
import shutil
import subprocess
import tempfile
import time
import unittest
from contextlib import ExitStack
from datetime import datetime, timedelta, timezone
from pathlib import Path
from unittest import mock
from zoneinfo import ZoneInfo

import pinn.verification.diagnostic_phase67 as phase67_cli
from tests.phase60._fixtures import gold_corpus_fixture
from tests.phase65.test_fit_short import _fit_registration_fixture, _loaded
from tests.phase67._fixtures import fake_pmset, patch_data_seam
from tests.phase67.test_workflow import WORKFLOW_ARMS, _execution, _git

CHICAGO = ZoneInfo("America/Chicago")
AC_LINE = "Now drawing from 'AC Power'"
SATURDAY_NOON = datetime(2026, 10, 31, 12, 0, tzinfo=CHICAGO)
#: Sunday 2026-11-01 closes the weekend at 22:00 CST (DST ended at 02:00).
SUNDAY_CLOSING_UTC = datetime(2026, 11, 1, 22, 0, tzinfo=CHICAGO).astimezone(
    timezone.utc
)


def _ac_power():
    """A picklable pmset reader naming AC power (the spawn-safe seam)."""
    return AC_LINE + "\n"


def _clock_at(moment):
    def read():
        return moment

    return read


def _saturday():
    return SATURDAY_NOON


def _sleeping_loader(orbit_key, window_length):
    """A registered load that outruns the cap (the deadline fixture)."""
    time.sleep(30.0)


def _sleeping_group_operation(queue):
    """A spawned worker that joins its own group and starts a descendant."""
    pid_file = os.environ["PHASE67_GROUP_PID_FILE"]
    os.setpgid(0, 0)
    with open(pid_file, "w", encoding="utf-8") as handle:
        handle.write(f"{os.getpid()} {os.getpgid(0)}\n")
    subprocess.run(["/bin/sleep", "30"], check=False)
    queue.put({"status": "complete"})


class RemainingWindowTests(unittest.TestCase):
    """The full-cap remaining-window admission at its exact boundaries."""

    def _module(self):
        from pinn.verification import diagnostic_power as power

        return power

    def test_exact_now_plus_cap_equality_is_admitted_for_both_caps(self):
        power = self._module()
        for cap in (900.0, 3540.0):
            now = SUNDAY_CLOSING_UTC - timedelta(seconds=cap)
            local = now.astimezone(CHICAGO)
            evidence = power.require_remaining_window(
                cap, local=local, now=_clock_at(local)
            )
            self.assertEqual(evidence["cap_seconds"], cap)
            self.assertAlmostEqual(
                evidence["remaining_allowance_seconds"], cap, places=6
            )
            self.assertEqual(
                datetime.fromisoformat(evidence["closing_utc"]),
                SUNDAY_CLOSING_UTC,
            )

    def test_the_next_instant_beyond_the_boundary_refuses(self):
        power = self._module()
        for cap in (900.0, 3540.0):
            with self.subTest(cap=cap):
                late = (
                    SUNDAY_CLOSING_UTC - timedelta(seconds=cap)
                ) + timedelta(microseconds=1)
                local = late.astimezone(CHICAGO)
                with self.assertRaises(power.PowerRefused):
                    power.require_remaining_window(
                        cap, local=local, now=_clock_at(local)
                    )

    def test_the_arithmetic_is_dst_exact_across_the_transition(self):
        power = self._module()
        # 01:00 CDT on the Sunday of the fall-back transition; the closing
        # instant is 22:00 CST, one wall-clock hour the UTC arithmetic sees.
        now_utc = datetime(2026, 11, 1, 1, 0, tzinfo=CHICAGO).astimezone(
            timezone.utc
        )
        remaining = (SUNDAY_CLOSING_UTC - now_utc).total_seconds()
        self.assertGreater(remaining, 0.0)
        evidence = power.require_remaining_window(
            remaining - 1.0, local=now_utc.astimezone(CHICAGO),
            now=_clock_at(now_utc.astimezone(CHICAGO)),
        )
        self.assertAlmostEqual(
            evidence["remaining_allowance_seconds"], remaining, places=6
        )
        with self.assertRaises(power.PowerRefused):
            power.require_remaining_window(
                remaining + 1.0, local=now_utc.astimezone(CHICAGO),
                now=_clock_at(now_utc.astimezone(CHICAGO)),
            )

    def test_a_weekday_or_a_naive_clock_refuses_before_the_arithmetic(self):
        power = self._module()
        friday = datetime(2026, 10, 30, 12, 0, tzinfo=CHICAGO)
        with self.assertRaises(power.PowerRefused):
            power.require_remaining_window(900.0, local=friday)
        with self.assertRaises(power.PowerRefused):
            power.require_remaining_window(
                900.0, local=datetime(2026, 10, 31, 12, 0)
            )


class _CaptureFixture:
    """A committed freeze and design, ready for the metadata capture."""

    @classmethod
    def _make(cls, case):
        stack = ExitStack()
        case.addClassCleanup(stack.close)
        fixture = stack.enter_context(gold_corpus_fixture())
        tmp = Path(stack.enter_context(
            tempfile.TemporaryDirectory(prefix="phase67-isolation-")
        ))
        cls.spec, cls.context, cls.scorecard, cls.data = _loaded(fixture)
        if cls.context.attestation is None:
            import types

            cls.context = types.SimpleNamespace(
                **{**vars(cls.context), "attestation": types.SimpleNamespace(
                    summary=lambda: {"test_split_opens": 0}
                )}
            )
        if not hasattr(cls.context.reader, "access_summary"):
            cls.context.reader.access_summary = lambda: {
                "requested": [], "opened": [], "refused_before_open": 0,
                "actual_opens": 1,
            }
        import hashlib

        root, _commit_sha = _fit_registration_fixture(tmp / "repo")
        phase = root / ".planning/phases/67-design-settings-ladders"
        evidence = phase / "evidence"
        evidence.mkdir(parents=True)
        freeze = {
            "schema": "phase67-harness-freeze/v1",
            "files": [
                {"path": "fit_dep.py", "sha256": hashlib.sha256(
                    (root / "fit_dep.py").read_bytes()
                ).hexdigest()},
                {"path": "frozen/scorer.py", "sha256": hashlib.sha256(
                    (root / "frozen/scorer.py").read_bytes()
                ).hexdigest()},
            ],
        }
        (evidence / "harness-freeze.json").write_text(json.dumps(freeze, indent=2))
        execution = _execution(case)
        _git(root, "add", ".planning")
        _git(root, "commit", "-q", "-m", "fixture freeze")
        patches = [
            mock.patch.object(execution, "ARM_ORDER", WORKFLOW_ARMS),
            mock.patch.object(
                execution, "PROVENANCE_REGISTRATION_REL",
                "reg/smoke-registration.json",
            ),
            mock.patch.object(
                execution, "PHASE67_DEPENDENCIES",
                ("fit_dep.py", "frozen/scorer.py"),
            ),
            mock.patch.object(
                execution, "DEFAULT_RUNTIME", {"dtype": "float64", "device": "cpu"}
            ),
        ]
        for patch in patches:
            patch.start()
            case.addClassCleanup(patch.stop)
        stdout, stderr = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(stdout), \
                contextlib.redirect_stderr(stderr):
            code = phase67_cli.main(
                ["prepare-design", "--experiment", "exp02"], repo_root=root
            )
        assert code == 0, stderr.getvalue()
        _git(root, "add", ".planning")
        _git(root, "commit", "-q", "-m", "design")
        cls.root, cls.phase, cls.execution = root, phase, execution
        cls.metadata_dir = phase / "evidence/exp02/metadata"

    @classmethod
    def capture(cls, *, read_power=None, now=None, load_orbit=None,
                supervisor=None):
        from tests.phase67._fixtures import inline_supervisor

        stdout, stderr = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(stdout), \
                contextlib.redirect_stderr(stderr):
            code = phase67_cli.main(
                ["capture-metadata", "--experiment", "exp02"],
                repo_root=cls.root, read_power=read_power, now=now,
                load_orbit=load_orbit,
                supervisor=supervisor or inline_supervisor,
            )
        return code, stdout.getvalue(), stderr.getvalue()

    @classmethod
    def load_orbit(cls, orbit_key, window_length):
        import types

        records = {
            role: {**block, "record_key": orbit_key}
            for role, block in cls.data.records.items()
        }
        return types.SimpleNamespace(**{**vars(cls.data), "records": records})


class GateOrderingTests(unittest.TestCase, _CaptureFixture):
    """Every refusal lands before any protected work exists."""

    @classmethod
    def setUpClass(cls):
        cls._make(cls)

    def _assert_nothing_created(self):
        self.assertFalse(self.metadata_dir.exists())

    def test_01_battery_refuses_before_anything_is_created(self):
        code, _out, err = self.capture(
            read_power=fake_pmset("Now drawing from 'Battery Power'"),
            now=_saturday,
        )
        self.assertEqual(code, 2)
        self.assertIn("PHASE67-REFUSED", err)
        self._assert_nothing_created()

    def test_02_a_weekday_refuses_before_anything_is_created(self):
        friday = _clock_at(datetime(2026, 10, 30, 12, 0, tzinfo=CHICAGO))
        code, _out, err = self.capture(read_power=_ac_power, now=friday)
        self.assertEqual(code, 2)
        self.assertIn("weekend window", err)
        self._assert_nothing_created()

    def test_03_a_late_sunday_without_the_full_allowance_refuses(self):
        from pinn.verification.diagnostic_power import (
            WINDOW_SUNDAY_LAST_HOUR,
            require_remaining_window,
        )

        late = datetime(2026, 11, 1, 21, 50, tzinfo=CHICAGO)
        with self.assertRaises(Exception):
            require_remaining_window(900.0, local=late)
        code, _out, err = self.capture(
            read_power=_ac_power, now=_clock_at(late)
        )
        self.assertEqual(code, 2)
        self.assertIn("remaining", err)
        self._assert_nothing_created()

    def test_04_insufficient_disk_refuses_before_the_claim(self):
        usage = shutil.disk_usage(str(self.root))
        with mock.patch.object(
            shutil, "disk_usage", return_value=usage._replace(free=0)
        ), mock.patch.object(
            self.execution, "_require_free_bytes",
            self.execution._require_free_bytes,
        ):
            code, _out, err = self.capture(
                read_power=_ac_power, now=_saturday,
                load_orbit=self.load_orbit,
            )
        self.assertEqual(code, 2)
        self.assertIn("PHASE67-REFUSED", err)
        self._assert_nothing_created()

    def test_05_a_dirty_freeze_refuses_before_the_gates_run(self):
        freeze = self.phase / "evidence/harness-freeze.json"
        original = freeze.read_bytes()
        freeze.write_bytes(original + b"# drifted\n")
        try:
            code, _out, err = self.capture(
                read_power=_ac_power, now=_saturday,
                load_orbit=self.load_orbit,
            )
            self.assertEqual(code, 2)
            self.assertIn("PHASE67-REFUSED", err)
            self._assert_nothing_created()
        finally:
            freeze.write_bytes(original)

    def test_06_a_good_capture_records_the_remaining_window_evidence(self):
        import pinn.verification.diagnostic_data as diagnostic_data

        with mock.patch.object(
            diagnostic_data, "open_diagnostic_context",
            side_effect=AssertionError("the real corpus seam was reached"),
        ):
            code, _out, err = self.capture(
                read_power=_ac_power, now=_saturday, load_orbit=self.load_orbit
            )
        self.assertEqual(code, 0, err)
        receipt = json.loads(
            (self.metadata_dir / "power-gate.json").read_bytes()
        )
        block = receipt["remaining_window"]
        self.assertEqual(block["cap_seconds"], 900.0)
        closing = datetime.fromisoformat(block["closing_utc"])
        checked = datetime.fromisoformat(receipt["checked_utc"])
        self.assertGreaterEqual(closing, checked + timedelta(seconds=900.0))
        # The evidence is independently recheckable from the receipt itself.
        recomputed = (closing - checked).total_seconds()
        self.assertAlmostEqual(
            recomputed, block["remaining_allowance_seconds"], delta=2.0
        )

    def test_07_a_second_capture_refuses_at_the_exclusive_claim(self):
        code, _out, err = self.capture(
            read_power=_ac_power, now=_saturday, load_orbit=self.load_orbit
        )
        self.assertEqual(code, 2)
        self.assertIn("PHASE67-REFUSED", err)

    def test_09_the_default_loader_routes_through_the_stage0_reader(self):
        import pinn.verification.diagnostic_phase67_execution as execution

        context = mock.MagicMock()
        with mock.patch.object(
            execution, "_open_diagnostic_context", return_value=context,
        ) as opened, mock.patch.object(
            execution, "_load_diagnostic_data", return_value=object(),
        ) as loader, mock.patch.object(
            execution, "_one_orbit_spec", return_value=object(),
        ) as spec:
            execution._default_load_orbit("hierarchical/gold/1632", 10.0)
        opened.assert_called_once()
        loader.assert_called_once()
        spec.assert_called_once()


class CaptureDeadlineTests(unittest.TestCase, _CaptureFixture):
    """A deadline during the metadata work leaves incomplete evidence."""

    @classmethod
    def setUpClass(cls):
        cls._make(cls)

    def test_a_cap_expired_capture_publishes_nothing_and_stays_incomplete(self):
        execution = _execution(self)

        def early_deadline(target, args, *, timeout, **kwargs):
            # The registered cap is the real 900-second rule (the spawned
            # child re-admits it against the unpatched module, so the fixture
            # cannot shrink it); this deadline fixture fires the SAME
            # supervised stop early, while the registered load sleeps far
            # beyond it, to prove the mechanism: the group is stopped, the
            # attempt stays incomplete and nothing is published.
            return execution._run_outer_supervised(
                target, args, timeout=6.0, **kwargs
            )

        started = time.monotonic()
        code, _out, err = self.capture(
            read_power=_ac_power, now=_saturday, load_orbit=_sleeping_loader,
            supervisor=early_deadline,
        )
        elapsed = time.monotonic() - started
        self.assertEqual(code, 2)
        self.assertLess(elapsed, 20.0, "the outer cap did not bound the work")
        attempt = json.loads(
            (self.metadata_dir / "attempt.json").read_bytes()
        )
        self.assertEqual(attempt["status"], "incomplete")
        self.assertIn("cap", attempt["reason"])
        self.assertFalse((self.metadata_dir / "record.json").exists())
        self.assertFalse((self.metadata_dir / "power-gate.json").exists())

    def test_the_outer_supervisor_owns_the_worker_process_group(self):
        import multiprocessing

        execution = _execution(self)
        with tempfile.NamedTemporaryFile(
            prefix="phase67-group-pids-", suffix=".txt", delete=False
        ) as handle:
            pid_file = handle.name
        self.addCleanup(os.unlink, pid_file)
        environment = {**os.environ, "PHASE67_GROUP_PID_FILE": pid_file}
        context = multiprocessing.get_context("spawn")
        with mock.patch.object(execution, "_SUPERVISOR_CONTEXT", context), \
                mock.patch.dict(os.environ, environment):
            started = time.monotonic()
            status, payload = execution._run_outer_supervised(
                _sleeping_group_operation, timeout=2.0,
            )
        self.assertEqual(status, "timeout")
        self.assertIsNone(payload)
        self.assertLess(time.monotonic() - started, 15.0)
        with open(pid_file, encoding="utf-8") as handle:
            worker_pid, group_pid = (int(value) for value in handle.read().split())
        self.assertEqual(worker_pid, group_pid, "the worker did not own its group")
        time.sleep(0.3)
        alive_group = subprocess.run(
            ["ps", "-g", str(group_pid), "-o", "pid="],
            capture_output=True, text=True, check=False,
        ).stdout.split()
        self.assertEqual(
            alive_group, [], "a descendant survived the supervised stop",
        )


class LaunchGateTests(unittest.TestCase, _CaptureFixture):
    """The launch-row gates: admission, cap coverage and exclusivity."""

    @classmethod
    def setUpClass(cls):
        cls._make(cls)

    def test_01_launch_row_passes_the_registered_cap_to_the_outer_supervisor(self):
        execution = _execution(self)
        from tests.phase67._fixtures import inline_supervisor

        # a committed metadata capture precedes the timing registrations
        code, _out, err = self.capture(
            read_power=_ac_power, now=_saturday, load_orbit=self.load_orbit
        )
        self.assertEqual(code, 0, err)
        _git(self.root, "add", ".planning")
        _git(self.root, "commit", "-q", "-m", "metadata")
        stdout, stderr = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(stdout), \
                contextlib.redirect_stderr(stderr):
            code = phase67_cli.main(
                ["register-timing", "--experiment", "exp02"],
                repo_root=self.root,
            )
        self.assertEqual(code, 0, stderr.getvalue())
        _git(self.root, "add", ".planning")
        _git(self.root, "commit", "-q", "-m", "timing")

        timeouts = {}

        def supervisor(target, args, *, timeout, **kwargs):
            timeouts["timeout"] = timeout
            return inline_supervisor(target, args, timeout=timeout, **kwargs)

        def runner(argv, *, cwd):
            return 0

        stdout, stderr = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(stdout), \
                contextlib.redirect_stderr(stderr):
            code = phase67_cli.main(
                ["launch-row", "--experiment", "exp02", "--kind", "timing",
                 "--case", "main-1632-s42", "--arm", "d2"],
                repo_root=self.root, read_power=_ac_power, run=runner,
                now=_saturday, supervisor=supervisor,
            )
        self.assertEqual(code, 0, stderr.getvalue())
        self.assertEqual(timeouts.get("timeout"), 900.0)

    def test_02_an_mps_registration_refuses_when_mps_is_unavailable(self):
        import torch

        # One timing registration names the production mps runtime; the fit
        # door must refuse it while MPS is unavailable (D-07), before any
        # corpus open or launch.
        matrix = json.loads(
            (self.phase / "evidence/exp02/timing-matrix.json").read_bytes()
        )
        registration = self.phase / matrix["rows"][0]["registration_path"]
        doc = json.loads(registration.read_bytes())
        doc["settings"]["runtime"] = {"dtype": "float32", "device": "mps"}
        registration.write_text(json.dumps(doc, indent=2, sort_keys=True) + "\n")
        _git(self.root, "add", ".planning")
        _git(self.root, "commit", "-q", "-m", "mps registration")
        if torch.backends.mps.is_available():
            unavailable = mock.patch.object(
                torch.backends.mps, "is_available", return_value=False
            )
        else:
            unavailable = contextlib.nullcontext()
        with unavailable:
            stdout, stderr = io.StringIO(), io.StringIO()
            with contextlib.redirect_stdout(stdout), \
                    contextlib.redirect_stderr(stderr):
                code = phase67_cli.main(
                    ["check-matrix", "--experiment", "exp02", "--kind", "timing"],
                    repo_root=self.root,
                )
        self.assertEqual(code, 2)
        self.assertIn("PHASE67-REFUSED", stderr.getvalue())
        self.assertIn("MPS is not available", stderr.getvalue())


class EncodedReceiptTests(unittest.TestCase):
    """The encoded logger-parity receipt branch in the fit admission."""

    def setUp(self):
        stack = contextlib.ExitStack()
        self.addCleanup(stack.close)
        self._stack = stack

    def _enter(self, manager):
        return self._stack.enter_context(manager)

    def _registration(self, receipt_raw):
        raw = Path(self._enter(tempfile.TemporaryDirectory(
            prefix="phase67-encoded-"
        )))
        root, _commit = _fit_registration_fixture(
            raw / "repo", receipt_raw=receipt_raw
        )
        return root, root / "reg/smoke-registration.json"

    def _encoded_receipt(self):
        payload = {
            "step": -1,
            "point": "probe-logger-parity",
            "n_points": 1001,
            "layers": [
                {"name": "input", "order": 0, "adjacent_cosine_mean": 0.9993},
                {"name": "h1", "order": 1, "adjacent_cosine_mean": 0.9854},
            ],
            "first_layer_frequency": {"definition": "d", "median": None,
                                      "max": None},
            "frequency_applicability": False,
            "frequency_reason": "column zero describes only the raw tau channel",
            "feature_frequency_cycles": [1.0471994061054543],
            "feature_harmonics": [1],
            "internal_input_dimension": 16,
            "output_movement": {"definition": "d", "value": 0.0034},
            "output_rate_ratio": {"definition": "d", "value": 4.9e7},
            "times_physical": [0.0, 0.01],
            "tau_values": [-1.0, 1.0],
        }
        return (json.dumps(payload, indent=2) + "\n").encode("utf-8")

    def test_an_encoded_shaped_receipt_admits_as_a_measurement(self):
        import pinn.verification.diagnostic_fit as fit_module

        root, registration = self._registration(self._encoded_receipt())
        _root, doc = fit_module.require_committed_smoke_registration(
            registration, repo_root=root
        )
        self.assertEqual(doc["schema"], "phase65-fit-registration/v1")

    def test_a_malformed_encoded_receipt_still_refuses(self):
        import pinn.verification.diagnostic_fit as fit_module

        raw = self._encoded_receipt()
        for mutation in (
            lambda doc: doc.update(frequency_applicability=True),
            lambda doc: doc.pop("frequency_reason"),
            lambda doc: doc.update(feature_frequency_cycles=["nope"]),
            lambda doc: doc.update(internal_input_dimension="sixteen"),
        ):
            with self.subTest(mutation=mutation):
                payload = json.loads(raw.decode("utf-8"))
                mutation(payload)
                bad = (json.dumps(payload, indent=2) + "\n").encode("utf-8")
                root, registration = self._registration(bad)
                with self.assertRaises(fit_module.DiagnosticFitRefused):
                    fit_module.require_committed_smoke_registration(
                        registration, repo_root=root
                    )


if __name__ == "__main__":
    unittest.main()
