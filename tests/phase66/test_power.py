"""Plan 66-02 (EXP-01): the fail-closed AC-power and weekend-window launch gate.

One test per behavior bullet of task 66-02-01: the anchored ``pmset`` first-line
parse, the refuse-on-everything-else ``require_ac_power`` matrix (including the
exact default argv), the owner's verbatim weekend window (D-08: plugged in "for
the weekend only. not weekdays") enforced in code as Saturday all day and
Sunday before 22:00 in America/Chicago, the launch order (power, window,
resolve, output-exists precheck, the metadata-only ``check_fit_registration``
admission precheck, then the exclusive receipt, then the child), the exact
receipt contract, and the read-only ``check`` subcommand. Every case injects
the pmset reader, the window clock and the runner; the real ``pmset`` and the
real clock are never used in the unit suite, and the live verdict is the
separate acceptance command (``diagnostic_power check``).
"""

from __future__ import annotations

import contextlib
import io
import json
import subprocess
import sys
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path
from types import SimpleNamespace
from unittest import mock
from zoneinfo import ZoneInfo

from pinn.verification import diagnostic_power as power
from tests.phase66.test_tracer import fake_pmset, phase66_fixture_registration

CHICAGO = ZoneInfo("America/Chicago")
AC_LINE = "Now drawing from 'AC Power'"
#: The Saturday the harness work is staged on (the tracer's injected clock).
SATURDAY_NOON = datetime(2026, 10, 31, 12, 0, tzinfo=CHICAGO)


def clock_at(moment):
    """A zero-argument callable giving the injected aware datetime."""
    return lambda: moment


class _GuardedSubprocess:
    """A subprocess shim for diagnostic_power whose ``run`` is a tripwire.

    The Phase 60 test_launcher safety-net precedent: the unit suite injects
    the pmset reader and the runner, so nothing may reach the module's real
    ``subprocess.run``; the shim keeps the constants the exercised paths name
    and fails the test on contact.
    """

    DEVNULL = subprocess.DEVNULL
    PIPE = subprocess.PIPE
    TimeoutExpired = subprocess.TimeoutExpired
    CompletedProcess = subprocess.CompletedProcess

    def run(self, *args, **kwargs):
        raise AssertionError(
            "diagnostic_power reached subprocess.run; the unit suite injects "
            "the pmset reader and the runner, so nothing should reach it"
        )


class Phase66PowerTests(unittest.TestCase):
    """The launch gate matrix: power, weekend window, prechecks, receipt, check."""

    def setUp(self):
        stack = contextlib.ExitStack()
        self.addCleanup(stack.close)
        # Safety net: a real caffeinate child could never start a fit, and the
        # module's subprocess.run fails the test if anything reaches it.
        stack.enter_context(mock.patch.object(power, "CAFFEINATE", "/usr/bin/true"))
        stack.enter_context(mock.patch.object(power, "subprocess", _GuardedSubprocess()))
        self.stack = stack

    def temporary(self, prefix):
        return Path(self.stack.enter_context(
            tempfile.TemporaryDirectory(prefix=prefix)
        ))

    # -- power_source ------------------------------------------------------

    def test_power_source_reads_the_exact_first_line(self):
        self.assertEqual(power.power_source(AC_LINE + "\n"), "AC Power")

    def test_power_source_returns_other_source_tokens_verbatim(self):
        self.assertEqual(
            power.power_source("Now drawing from 'Battery Power'\n"), "Battery Power"
        )
        self.assertEqual(
            power.power_source("Now drawing from 'UPS Power'\n"), "UPS Power"
        )

    def test_power_source_returns_none_for_empty_garbage_and_a_later_line(self):
        for text in (
            "",
            "totally unexpected pmset output\n",
            "Battery level: 88%\nNow drawing from 'AC Power'\n",
        ):
            with self.subTest(text=text):
                self.assertIsNone(power.power_source(text))

    # -- require_ac_power --------------------------------------------------

    def test_require_ac_power_passes_only_on_the_ac_source(self):
        first_line = power.require_ac_power(read_power=fake_pmset(AC_LINE))
        self.assertEqual(first_line, AC_LINE)

    def test_require_ac_power_refuses_every_unrecognized_reading(self):
        for first_line in (
            "Now drawing from 'Battery Power'",
            "Now drawing from 'UPS Power'",
            "",
            "totally unexpected pmset output",
            "Battery level: 88%\nNow drawing from 'AC Power'",
        ):
            with self.subTest(first_line=first_line):
                with self.assertRaises(power.PowerRefused):
                    power.require_ac_power(read_power=fake_pmset(first_line))

    def test_require_ac_power_refuses_pmset_read_failures(self):
        def nonzero_exit():
            raise power.PowerRefused("/usr/bin/pmset -g batt exited 1; refusing to launch")

        def missing_binary():
            raise FileNotFoundError(2, "No such file or directory", "/usr/bin/pmset")

        def os_error():
            raise OSError("pmset is unreadable")

        def timeout():
            raise subprocess.TimeoutExpired(cmd="/usr/bin/pmset", timeout=10.0)

        for reader in (nonzero_exit, missing_binary, os_error, timeout):
            with self.subTest(reader=reader.__name__):
                with self.assertRaises(power.PowerRefused):
                    power.require_ac_power(read_power=reader)

    def test_the_default_reader_calls_pmset_with_the_exact_fixed_argv(self):
        recorded = {}

        def fake_run(argv, **kwargs):
            recorded["argv"] = list(argv)
            recorded["kwargs"] = dict(kwargs)
            return subprocess.CompletedProcess(
                argv, 0, stdout=AC_LINE + "\n", stderr=""
            )

        with mock.patch.object(
            power, "subprocess", SimpleNamespace(run=fake_run, DEVNULL=subprocess.DEVNULL)
        ):
            first_line = power.require_ac_power()
        self.assertEqual(first_line, AC_LINE)
        self.assertEqual(recorded["argv"], ["/usr/bin/pmset", "-g", "batt"])
        self.assertNotIn("shell", recorded["kwargs"])
        self.assertIn("timeout", recorded["kwargs"])

    # -- require_weekend_window -------------------------------------------

    def test_the_weekend_window_passes_saturday_and_sunday_evening(self):
        for moment in (
            datetime(2026, 10, 31, 0, 0, tzinfo=CHICAGO),
            datetime(2026, 10, 31, 23, 59, tzinfo=CHICAGO),
            datetime(2026, 11, 1, 21, 59, tzinfo=CHICAGO),
        ):
            with self.subTest(moment=moment.isoformat()):
                local = power.require_weekend_window(clock_at(moment))
                self.assertEqual(local.isoweekday(), moment.isoweekday())
                self.assertEqual(local.isoformat(), moment.isoformat())

    def test_the_weekend_window_refuses_sunday_22_and_every_weekday(self):
        refusals = [datetime(2026, 11, 1, 22, 0, tzinfo=CHICAGO)]
        refusals.append(datetime(2026, 11, 13, 23, 59, tzinfo=CHICAGO))
        refusals.extend(
            datetime(2026, 11, 9 + offset, 12, 0, tzinfo=CHICAGO)
            for offset in range(5)  # Monday to Friday noon, after the
            # 2026-11-07 07:30 amendment deadline admits earlier weekdays
        )
        for moment in refusals:
            with self.subTest(moment=moment.isoformat()):
                with self.assertRaises(power.PowerRefused):
                    power.require_weekend_window(clock_at(moment))

    def test_the_owner_amendment_admits_weekdays_before_its_deadline(self):
        # 2026-11-06 owner instruction ("continue with amendment"): weekdays
        # are admitted through AMENDMENT_DEADLINE_LOCAL, Sunday night still
        # refuses, and the deadline is the weekday closing instant.
        tuesday = datetime(2026, 11, 3, 11, 45, tzinfo=CHICAGO)
        local = power.require_weekend_window(clock_at(tuesday))
        self.assertEqual(local.isoformat(), tuesday.isoformat())
        with self.assertRaises(power.PowerRefused):
            power.require_weekend_window(
                clock_at(datetime(2026, 11, 1, 22, 0, tzinfo=CHICAGO))
            )
        closing = power.weekend_closing_utc(local)
        self.assertEqual(closing.isoformat(), "2026-11-07T13:30:00+00:00")

    def test_the_weekend_window_refuses_a_naive_clock_and_a_failed_zone(self):
        with self.assertRaises(power.PowerRefused):
            power.require_weekend_window(clock_at(datetime(2026, 10, 31, 12, 0)))
        broken_zone = mock.Mock(side_effect=RuntimeError("zone database unavailable"))
        with mock.patch.object(power, "ZoneInfo", broken_zone):
            with self.assertRaises(power.PowerRefused):
                power.require_weekend_window(clock_at(SATURDAY_NOON))

    def test_the_weekend_window_converts_a_utc_instant_to_the_window_zone(self):
        # Sunday 03:30 UTC is Saturday 22:30 in America/Chicago (CDT): inside.
        moment = datetime(2026, 11, 1, 3, 30, tzinfo=timezone.utc)
        local = power.require_weekend_window(clock_at(moment))
        self.assertEqual(local.isoweekday(), 6)
        self.assertEqual(local.isoformat(), "2026-10-31T22:30:00-05:00")

    def test_the_window_constants_name_the_zone_and_the_sunday_hour(self):
        self.assertEqual(power.WINDOW_TIMEZONE, "America/Chicago")
        self.assertEqual(power.WINDOW_SUNDAY_LAST_HOUR, 22)

    # -- launch refusals ---------------------------------------------------

    def _fixture(self, tmp, name):
        root, _commit = phase66_fixture_registration(Path(tmp) / name)
        return root

    def test_launch_refuses_on_battery_before_anything_is_created(self):
        tmp = self.temporary("phase66-power-battery-")
        root = self._fixture(tmp, "repo")
        registration = root / "reg/smoke-registration.json"
        output = root / "evidence/battery/record.json"
        with mock.patch(
            "pinn.verification.diagnostic_fit.check_fit_registration",
            side_effect=AssertionError("the admission precheck ran on battery"),
        ) as admission:
            def runner(argv, *, cwd):
                raise AssertionError("the launcher started a fit on battery")

            stderr = io.StringIO()
            with contextlib.redirect_stderr(stderr):
                code = power.launch(
                    registration, output, repo_root=root,
                    read_power=fake_pmset("Now drawing from 'Battery Power'"),
                    run=runner, now=clock_at(SATURDAY_NOON),
                )
        self.assertEqual(code, 2)
        self.assertIn("POWER-REFUSED", stderr.getvalue())
        admission.assert_not_called()
        self.assertFalse(output.parent.exists())

    def test_launch_refuses_outside_the_weekend_window(self):
        tmp = self.temporary("phase66-power-window-")
        root = self._fixture(tmp, "repo")
        registration = root / "reg/smoke-registration.json"
        output = root / "evidence/window/record.json"
        sunday_22 = datetime(2026, 11, 1, 22, 0, tzinfo=CHICAGO)
        with mock.patch(
            "pinn.verification.diagnostic_fit.check_fit_registration",
            side_effect=AssertionError("the admission precheck ran outside the window"),
        ) as admission:
            def runner(argv, *, cwd):
                raise AssertionError("the launcher started a fit outside the window")

            stderr = io.StringIO()
            with contextlib.redirect_stderr(stderr):
                code = power.launch(
                    registration, output, repo_root=root,
                    read_power=fake_pmset(AC_LINE), run=runner,
                    now=clock_at(sunday_22),
                )
        self.assertEqual(code, 2)
        self.assertIn("POWER-REFUSED", stderr.getvalue())
        admission.assert_not_called()
        self.assertFalse(output.parent.exists())

    def test_launch_refuses_when_the_output_record_already_exists(self):
        tmp = self.temporary("phase66-power-spent-")
        root = self._fixture(tmp, "repo")
        registration = root / "reg/smoke-registration.json"
        output = root / "evidence/spent/record.json"
        output.parent.mkdir(parents=True)
        output.write_bytes(b"{}\n")

        def runner(argv, *, cwd):
            raise AssertionError("the launcher started a fit over a spent directory")

        stderr = io.StringIO()
        with contextlib.redirect_stderr(stderr):
            code = power.launch(
                registration, output, repo_root=root,
                read_power=fake_pmset(AC_LINE), run=runner,
                now=clock_at(SATURDAY_NOON),
            )
        self.assertEqual(code, 2)
        self.assertIn("POWER-REFUSED", stderr.getvalue())
        self.assertFalse((output.parent / "power-gate.json").exists())

    def test_launch_refuses_an_inadmissible_registration_before_writing(self):
        tmp = self.temporary("phase66-power-dirty-")
        root = self._fixture(tmp, "repo")
        registration = root / "reg/smoke-registration.json"
        output = root / "evidence/dirty/record.json"
        # The fixture's enumerated code dependency changes after the
        # registration commit, so the metadata-only admission refuses.
        (root / "fit_dep.py").write_bytes(b"FIT_DEPENDENCY = 2\n")

        def runner(argv, *, cwd):
            raise AssertionError("the launcher started a fit on a dirty registration")

        stderr = io.StringIO()
        with contextlib.redirect_stderr(stderr):
            code = power.launch(
                registration, output, repo_root=root,
                read_power=fake_pmset(AC_LINE), run=runner,
                now=clock_at(SATURDAY_NOON),
            )
        self.assertEqual(code, 2)
        self.assertIn("POWER-REFUSED", stderr.getvalue())
        self.assertFalse(output.parent.exists())

    def test_launch_refuses_paths_resolving_outside_the_repository(self):
        tmp = self.temporary("phase66-power-outside-")
        root = self._fixture(tmp, "repo")
        registration = root / "reg/smoke-registration.json"
        output = tmp / "outside/record.json"

        def runner(argv, *, cwd):
            raise AssertionError("the launcher started a fit outside the repository")

        stderr = io.StringIO()
        with contextlib.redirect_stderr(stderr):
            code = power.launch(
                registration, output, repo_root=root,
                read_power=fake_pmset(AC_LINE), run=runner,
                now=clock_at(SATURDAY_NOON),
            )
        self.assertEqual(code, 2)
        self.assertIn("POWER-REFUSED", stderr.getvalue())
        self.assertFalse(output.parent.exists())

    # -- the AC launch path -------------------------------------------------

    def test_launch_on_ac_inside_the_window_writes_the_planned_receipt_and_argv(self):
        tmp = self.temporary("phase66-power-ac-")
        root = self._fixture(tmp, "repo")
        registration = root / "reg/smoke-registration.json"
        output = root / "evidence/ac/record.json"
        argv_seen = []

        def runner(argv, *, cwd):
            argv_seen.append(list(argv))
            return 0

        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            # Re-pin the production caffeinate constant for the exact-argv
            # assertion; the runner is injected, so no real child can start.
            with mock.patch.object(power, "CAFFEINATE", "/usr/bin/caffeinate"):
                code = power.launch(
                    registration, output, repo_root=root,
                    read_power=fake_pmset(AC_LINE), run=runner,
                    now=clock_at(SATURDAY_NOON),
                )
        self.assertEqual(code, 0)
        self.assertEqual(len(argv_seen), 1)
        self.assertEqual(
            argv_seen[0],
            ["/usr/bin/caffeinate", "-is", sys.executable, "-B", "-m",
             "pinn.verification.diagnostic_fit", "run",
             "--registration", str(registration.resolve()),
             "--output", str(output.resolve())],
        )
        self.assertEqual(
            stdout.getvalue(),
            "POWER-OK source=AC Power isoweekday=6"
            " receipt=evidence/ac/power-gate.json\n",
        )
        receipt_raw = (output.parent / "power-gate.json").read_bytes()
        receipt = json.loads(receipt_raw)
        self.assertEqual(
            set(receipt),
            {"schema", "checked_utc", "power_source", "pmset_first_line",
             "registration", "output", "load_average", "launched", "window"},
        )
        self.assertEqual(receipt["schema"], "phase66-power-gate/v1")
        self.assertEqual(receipt["power_source"], "AC Power")
        self.assertEqual(receipt["pmset_first_line"], AC_LINE)
        self.assertEqual(receipt["registration"], "reg/smoke-registration.json")
        self.assertEqual(receipt["output"], "evidence/ac/record.json")
        self.assertEqual(
            receipt["launched"],
            {"module": "pinn.verification.diagnostic_fit", "subcommand": "run"},
        )
        self.assertNotIn(b"/Users/", receipt_raw)
        window = receipt["window"]
        self.assertEqual(
            set(window), {"timezone", "local_time", "isoweekday"}
        )
        self.assertEqual(window["timezone"], "America/Chicago")
        self.assertEqual(window["isoweekday"], 6)
        parsed = datetime.fromisoformat(window["local_time"])
        self.assertIsNotNone(parsed.utcoffset())
        self.assertEqual(parsed.microsecond, 0)

    def test_a_second_launch_into_the_same_directory_refuses_at_the_receipt(self):
        tmp = self.temporary("phase66-power-receipt-")
        root = self._fixture(tmp, "repo")
        registration = root / "reg/smoke-registration.json"
        output = root / "evidence/ac/record.json"
        runs = []

        def runner(argv, *, cwd):
            runs.append(list(argv))
            return 0

        with contextlib.redirect_stdout(io.StringIO()):
            code = power.launch(
                registration, output, repo_root=root,
                read_power=fake_pmset(AC_LINE), run=runner,
                now=clock_at(SATURDAY_NOON),
            )
        self.assertEqual(code, 0)
        stderr = io.StringIO()
        with contextlib.redirect_stderr(stderr):
            code = power.launch(
                registration, output, repo_root=root,
                read_power=fake_pmset(AC_LINE), run=runner,
                now=clock_at(SATURDAY_NOON),
            )
        self.assertEqual(code, 2)
        self.assertIn("POWER-REFUSED", stderr.getvalue())
        self.assertEqual(len(runs), 1)
        receipt = json.loads((output.parent / "power-gate.json").read_bytes())
        self.assertEqual(receipt["power_source"], "AC Power")

    # -- the read-only check subcommand -------------------------------------

    def test_check_prints_power_ok_inside_the_window_and_writes_nothing(self):
        tmp = self.temporary("phase66-power-check-")
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            code = power.main(
                ["check"], repo_root=tmp,
                read_power=fake_pmset(AC_LINE), now=clock_at(SATURDAY_NOON),
            )
        self.assertEqual(code, 0)
        self.assertEqual(stdout.getvalue(), "POWER-OK source=AC Power isoweekday=6\n")
        self.assertEqual(list(tmp.iterdir()), [])

    def test_check_refuses_outside_the_window_and_on_battery(self):
        sunday_22 = datetime(2026, 11, 1, 22, 0, tzinfo=CHICAGO)
        stderr = io.StringIO()
        with contextlib.redirect_stderr(stderr):
            code = power.main(
                ["check"], read_power=fake_pmset(AC_LINE), now=clock_at(sunday_22)
            )
        self.assertEqual(code, 2)
        self.assertIn("POWER-REFUSED", stderr.getvalue())
        stderr = io.StringIO()
        with contextlib.redirect_stderr(stderr):
            code = power.main(
                ["check"], read_power=fake_pmset("Now drawing from 'Battery Power'"),
                now=clock_at(SATURDAY_NOON),
            )
        self.assertEqual(code, 2)
        self.assertIn("POWER-REFUSED", stderr.getvalue())

    def test_main_returns_2_for_an_empty_argv_unknown_command_and_missing_flags(self):
        self.assertEqual(power.main([]), 2)
        self.assertEqual(power.main(["bogus"]), 2)
        self.assertEqual(power.main(["launch"]), 2)
        self.assertEqual(power.main(["launch", "--registration", "x"]), 2)


if __name__ == "__main__":
    unittest.main()
