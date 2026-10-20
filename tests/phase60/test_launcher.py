"""Phase 60 (SCOPE-44): the detached launcher runs one closed arm sequence one arm at a time.

Every test launches stubs (a short ``python -c`` script) under a TemporaryDirectory. No test
starts a real arm, ``caffeinate`` or the learnability runner.
"""

from __future__ import annotations

import ast
import contextlib
import importlib.util
import io
import json
import os
import signal
import subprocess
import sys
import tempfile
import time
import unittest
from datetime import datetime
from pathlib import Path
from unittest import mock

from pinn.verification import learnability_arms

ROOT = Path(__file__).resolve().parents[2]
EVIDENCE = ROOT / ".planning/phases/60-single-system-learnability/evidence"
LAUNCHER = EVIDENCE / "launch_phase60_arm.py"
_SPEC = importlib.util.spec_from_file_location("phase60_launcher", LAUNCHER)
assert _SPEC is not None and _SPEC.loader is not None
launcher = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(launcher)

# A stub arm: it logs its name, process id, session id and time on start and on end, prints one
# line to each stream, waits for the gate file (when it was given one) and exits with its code.
STUB_SOURCE = (
    "import os, sys, time\n"
    "from pathlib import Path\n"
    "log, name, gate, code = sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4])\n"
    "def note(event):\n"
    "    with open(log, 'a') as handle:\n"
    "        handle.write(f'{name} {event} {os.getpid()} {os.getsid(0)} {time.time():.6f}\\n')\n"
    "note('start')\n"
    "print(name + ' stdout', flush=True)\n"
    "print(name + ' stderr', file=sys.stderr, flush=True)\n"
    "deadline = time.time() + 30\n"
    "while gate and not Path(gate).exists():\n"
    "    if time.time() > deadline:\n"
    "        sys.exit(99)\n"
    "    time.sleep(0.02)\n"
    "note('end')\n"
    "sys.exit(code)\n"
)


def stub_argv(log, name, *, gate=None, code=0):
    return [sys.executable, "-c", STUB_SOURCE, str(log), name, "" if gate is None else str(gate), str(code)]


def wait_for(predicate, what, timeout=30.0):
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        value = predicate()
        if value:
            return value
        time.sleep(0.02)
    raise AssertionError(f"{what} did not happen within {timeout}s")


def wait_for_json(path, timeout=30.0):
    def read():
        if not path.is_file():
            return None
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return None

    return wait_for(read, f"{path.name} to be written", timeout)


def read_log(path):
    """The stub log as (name, event, pid, session, time) rows."""
    if not path.is_file():
        return []
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        name, event, pid, session, stamp = line.split()
        rows.append((name, event, int(pid), int(session), float(stamp)))
    return rows


def standard_streams(pid):
    """What descriptors 0, 1 and 2 of a process point at, as ``{fd: path}`` (read with lsof)."""
    shown = subprocess.run(
        ["lsof", "-a", "-p", str(pid), "-d", "0,1,2", "-Fn"], capture_output=True, text=True, check=False,
    )
    if shown.returncode != 0:
        raise AssertionError(f"lsof could not list process {pid}: {shown.stderr.strip()}")
    streams, current = {}, None
    for line in shown.stdout.splitlines():
        if line.startswith("f"):
            current = int(line[1:])
        elif line.startswith("n") and current is not None:
            streams[current] = line[1:]
    return streams


def kill_if_ours(pid, marker, *, group):
    """SIGKILL a process (or its group) a test started, while its command line still names the test root."""
    shown = subprocess.run(
        ["ps", "-o", "command=", "-p", str(pid)], capture_output=True, text=True, check=False,
    ).stdout
    if marker not in shown:
        return
    try:
        (os.killpg if group else os.kill)(pid, signal.SIGKILL)
    except (ProcessLookupError, PermissionError):
        pass


class LauncherTestCase(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix="phase60-launcher-")
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name).resolve()
        self.log = self.root / "stubs.log"
        self.gate = self.root / "gate"
        self.invocation = self.root / "runs/.launch/phase60/stub/invocation-1"
        # Safety net: a command built by the launcher's own argv builder could never start a real
        # arm (caffeinate is replaced by true), and the host probe fails the test if it is reached.
        for name, replacement in (("CAFFEINATE", "/usr/bin/true"),):
            patcher = mock.patch.object(launcher, name, replacement)
            patcher.start()
            self.addCleanup(patcher.stop)
        probe = mock.patch.object(
            launcher, "_assert_host_mps", side_effect=AssertionError("the host probe must not run in a test"),
        )
        probe.start()
        self.addCleanup(probe.stop)

    def new_root(self):
        """Another empty temporary root, for a subtest that needs a clean launch tree."""
        temporary = tempfile.TemporaryDirectory(prefix="phase60-launcher-")
        self.addCleanup(temporary.cleanup)
        return Path(temporary.name).resolve()

    def identity(self, *names, sequence="stub"):
        return {"sequence": sequence, "arm_ids": list(names)}

    def launch(self, argvs, names, *, invocation=None):
        process = launcher.start(
            invocation or self.invocation, argvs, cwd=self.root, identity=self.identity(*names),
        )
        self.addCleanup(kill_if_ours, process["supervisor_pid"], str(self.root), group=True)
        return process

    def launch_from_helper(self, argvs, names, *, invocation=None):
        """Call start() in a helper process of its own session whose standard input is an open pipe.

        Returns ``(helper, process)`` once the helper has recorded the supervisor. The helper then
        sleeps, so a test can hang it up and kill it while the supervisor keeps going.
        """
        invocation = invocation or self.invocation
        code = (
            "import importlib.util, time\n"
            "from pathlib import Path\n"
            f"spec = importlib.util.spec_from_file_location('l', {str(LAUNCHER)!r})\n"
            "l = importlib.util.module_from_spec(spec); spec.loader.exec_module(l)\n"
            f"l.start(Path({str(invocation)!r}), {argvs!r}, cwd=Path({str(self.root)!r}), "
            f"identity={self.identity(*names)!r})\n"
            "time.sleep(60)\n"
        )
        helper = subprocess.Popen(
            [sys.executable, "-B", "-c", code], stdin=subprocess.PIPE, start_new_session=True,
        )
        self.addCleanup(self.stop_helper, helper)
        process = wait_for_json(invocation / "process.json")
        self.addCleanup(kill_if_ours, process["supervisor_pid"], str(self.root), group=True)
        return helper, process

    def stop_helper(self, helper):
        if helper.poll() is None:
            kill_if_ours(helper.pid, str(self.root), group=True)
        helper.wait(timeout=10)
        helper.stdin.close()

    def logged(self):
        return read_log(self.log)


class SequenceTests(unittest.TestCase):
    def test_rung1_is_the_three_panel_arms_in_the_pinned_order(self):
        self.assertEqual(launcher.sequence_arms("rung1"), ("r1-1632", "r1-851", "r1-4658"))

    def test_a_single_arm_sequence_names_one_catalog_arm(self):
        self.assertEqual(launcher.sequence_arms("arm:g2c-851-w120"), ("g2c-851-w120",))

    def test_every_closed_name_resolves_to_its_catalog_arms(self):
        self.assertEqual(len(learnability_arms.SEQUENCES), 51)
        for name, arm_ids in learnability_arms.SEQUENCES.items():
            with self.subTest(name=name):
                self.assertEqual(launcher.sequence_arms(name), tuple(arm_ids))

    def test_any_other_name_is_refused(self):
        for name in (
            "rung3", "../rung1", "arm:r1-9999", "arm:", "", "RUNG1", " rung1", "rung1/", "rung1\n",
            "arm:r1-1632 ", "sweep-4658", None, 5, ["rung1"],
        ):
            with self.subTest(name=name), self.assertRaises(launcher.LaunchError):
                launcher.sequence_arms(name)

    def test_the_governed_stop_codes_are_the_catalog_signal_exit_codes(self):
        self.assertEqual(launcher.GOVERNED_STOP_CODES, (129, 130, 143))
        self.assertEqual(
            launcher.GOVERNED_STOP_CODES,
            (learnability_arms.EXIT_SIGHUP, learnability_arms.EXIT_SIGINT, learnability_arms.EXIT_SIGTERM),
        )


class ArmArgvTests(unittest.TestCase):
    def test_a_fresh_arm_command_is_caffeinate_over_the_pinned_runner(self):
        self.assertEqual(
            launcher.arm_argv("r1-1632", resume=False),
            [
                "/usr/bin/caffeinate", "-is",
                "<home>/miniforge3/envs/pinn-train/bin/python",
                "-B", "-m", "pinn.verification.learnability_run", "r1-1632",
            ],
        )

    def test_a_resume_appends_the_resume_flag_and_nothing_else(self):
        fresh = launcher.arm_argv("r1-851", resume=False)
        self.assertEqual(launcher.arm_argv("r1-851", resume=True), fresh + ["--resume"])

    def test_an_id_outside_the_catalog_is_refused(self):
        for arm_id in ("r1-9999", "../r1-1632", "r1-1632 ", "", "R1-1632", "fixture-gold-0-1", None, 7):
            with self.subTest(arm_id=arm_id), self.assertRaises(launcher.LaunchError):
                launcher.arm_argv(arm_id, resume=False)

    def test_every_catalog_arm_has_a_command_made_of_strings_only(self):
        for arm_id in learnability_arms.catalog():
            for resume in (False, True):
                argv = launcher.arm_argv(arm_id, resume=resume)
                with self.subTest(arm_id=arm_id, resume=resume):
                    self.assertIsInstance(argv, list)
                    self.assertTrue(all(isinstance(item, str) for item in argv))
                    self.assertEqual(argv[:6], launcher.arm_argv("r1-1632", resume=False)[:6])
                    self.assertEqual(argv[6], arm_id)
                    self.assertEqual(len(argv), 8 if resume else 7)


class ExitDescriptionTests(unittest.TestCase):
    def test_return_codes_map_to_exit_codes_and_signal_names(self):
        for returncode, expected in (
            (0, (0, None)),
            (3, (3, None)),
            (130, (130, None)),
            (-9, (137, "SIGKILL")),
            (-1, (129, "SIGHUP")),
            (-2, (130, "SIGINT")),
            (-15, (143, "SIGTERM")),
            (-60, (188, "SIG60")),
        ):
            with self.subTest(returncode=returncode):
                self.assertEqual(launcher.describe_exit(returncode), expected)


class SupervisorOrderTests(LauncherTestCase):
    def test_start_returns_before_the_first_stub_ends_and_the_stubs_never_overlap(self):
        argvs = [stub_argv(self.log, "a", gate=self.gate), stub_argv(self.log, "b", gate=self.gate)]
        process = self.launch(argvs, ("a", "b"))
        # start() has returned while the first stub is still held at its gate.
        wait_for(self.logged, "the first stub to start")
        self.assertEqual([(row[0], row[1]) for row in self.logged()], [("a", "start")])
        self.assertFalse((self.invocation / "arm-1.json").exists())
        self.assertFalse((self.invocation / "exit.json").exists())
        self.gate.write_text("open", encoding="utf-8")
        exit_record = wait_for_json(self.invocation / "exit.json")
        rows = self.logged()
        self.assertEqual(
            [(row[0], row[1]) for row in rows],
            [("a", "start"), ("a", "end"), ("b", "start"), ("b", "end")],
        )
        stamps = [row[4] for row in rows]
        self.assertEqual(stamps, sorted(stamps))
        # The second stub starts only after the first's exit was recorded.
        first = json.loads((self.invocation / "arm-1.json").read_text(encoding="utf-8"))
        first_end = datetime.fromisoformat(first["end_utc"]).timestamp()
        second_start = [row[4] for row in rows if row[:2] == ("b", "start")][0]
        self.assertGreaterEqual(second_start, first_end)
        for index, name in enumerate(("a", "b"), start=1):
            arm = json.loads((self.invocation / f"arm-{index}.json").read_text(encoding="utf-8"))
            self.assertEqual(
                (arm["arm_id"], arm["returncode"], arm["exit_code"], arm["signal"]), (name, 0, 0, None),
            )
            self.assertGreater(arm["wall_clock_secs"], 0.0)
            self.assertIn("start_utc", arm)
            self.assertIsInstance(arm["pid"], int)
        self.assertEqual(
            (exit_record["completed_arms"], exit_record["stopped_arm"], exit_record["stopped_code"],
             exit_record["signal"]),
            (2, None, None, None),
        )
        self.assertGreater(exit_record["wall_clock_secs"], 0.0)
        self.assertIsInstance(process["supervisor_pid"], int)


class StopAtFailureTests(LauncherTestCase):
    def test_a_first_stub_exiting_3_stops_the_sequence_before_the_second_starts(self):
        argvs = [stub_argv(self.log, "a", code=3), stub_argv(self.log, "b")]
        self.launch(argvs, ("a", "b"))
        exit_record = wait_for_json(self.invocation / "exit.json")
        self.assertEqual([row[0] for row in self.logged()], ["a", "a"])
        self.assertFalse((self.invocation / "arm-2.json").exists())
        arm = json.loads((self.invocation / "arm-1.json").read_text(encoding="utf-8"))
        self.assertEqual((arm["returncode"], arm["exit_code"], arm["signal"]), (3, 3, None))
        self.assertEqual(
            (exit_record["completed_arms"], exit_record["stopped_arm"], exit_record["stopped_code"],
             exit_record["signal"]),
            (0, "a", 3, None),
        )

    def test_a_failure_after_a_success_counts_the_completed_arm(self):
        argvs = [stub_argv(self.log, "a"), stub_argv(self.log, "b", code=130), stub_argv(self.log, "c")]
        self.launch(argvs, ("a", "b", "c"))
        exit_record = wait_for_json(self.invocation / "exit.json")
        self.assertEqual(sorted({row[0] for row in self.logged()}), ["a", "b"])
        self.assertEqual(
            (exit_record["completed_arms"], exit_record["stopped_arm"], exit_record["stopped_code"]),
            (1, "b", 130),
        )
        self.assertFalse((self.invocation / "arm-3.json").exists())


class SignalDeathTests(LauncherTestCase):
    def test_a_sigkill_death_is_recorded_as_137_and_stops_the_sequence(self):
        argvs = [stub_argv(self.log, "a", gate=self.root / "never"), stub_argv(self.log, "b")]
        self.launch(argvs, ("a", "b"))
        rows = wait_for(self.logged, "the first stub to start")
        pid = rows[0][2]
        self.addCleanup(kill_if_ours, pid, str(self.root), group=False)
        os.kill(pid, signal.SIGKILL)
        exit_record = wait_for_json(self.invocation / "exit.json")
        arm = json.loads((self.invocation / "arm-1.json").read_text(encoding="utf-8"))
        self.assertEqual(
            (arm["arm_id"], arm["pid"], arm["returncode"], arm["exit_code"], arm["signal"]),
            ("a", pid, -9, 137, "SIGKILL"),
        )
        self.assertEqual(
            (exit_record["completed_arms"], exit_record["stopped_arm"], exit_record["stopped_code"],
             exit_record["signal"]),
            (0, "a", 137, "SIGKILL"),
        )
        self.assertEqual({row[0] for row in self.logged()}, {"a"})
        self.assertFalse((self.invocation / "arm-2.json").exists())


class LaunchRecordTests(LauncherTestCase):
    def run_two_stubs(self):
        argvs = [stub_argv(self.log, "a"), stub_argv(self.log, "b")]
        process = self.launch(argvs, ("a", "b"))
        wait_for_json(self.invocation / "exit.json")
        return process, argvs

    def test_the_invocation_holds_exactly_the_documented_files(self):
        self.run_two_stubs()
        self.assertEqual(
            sorted(path.name for path in self.invocation.iterdir()),
            ["arm-1.json", "arm-2.json", "exit.json", "launch.json", "output.log", "process.json",
             "supervisor.err", "supervisor.out"],
        )

    def test_launch_json_records_the_plan_and_no_working_directory(self):
        _process, argvs = self.run_two_stubs()
        launch = json.loads((self.invocation / "launch.json").read_text(encoding="utf-8"))
        self.assertEqual(
            set(launch), {"schema", "sequence", "arm_ids", "argvs", "requested_utc"},
        )
        self.assertEqual(launch["schema"], "phase60-detached-launch/v1")
        self.assertEqual(launch["sequence"], "stub")
        self.assertEqual(launch["arm_ids"], ["a", "b"])
        self.assertEqual(launch["argvs"], argvs)

    def test_process_json_records_a_new_session_led_by_the_supervisor(self):
        process, _argvs = self.run_two_stubs()
        recorded = json.loads((self.invocation / "process.json").read_text(encoding="utf-8"))
        self.assertEqual(recorded, process)
        self.assertEqual(set(recorded), {"supervisor_pid", "session_id", "process_group", "start_utc"})
        self.assertEqual(recorded["session_id"], recorded["supervisor_pid"])
        self.assertEqual(recorded["process_group"], recorded["supervisor_pid"])
        self.assertNotEqual(recorded["session_id"], os.getsid(0))
        self.assertNotEqual(recorded["process_group"], os.getpgid(0))
        sessions = {row[3] for row in self.logged()}
        self.assertEqual(sessions, {recorded["session_id"]})

    def test_output_log_keeps_both_streams_of_every_arm_in_order(self):
        self.run_two_stubs()
        text = (self.invocation / "output.log").read_text(encoding="utf-8")
        self.assertEqual(text.splitlines(), ["a stdout", "a stderr", "b stdout", "b stderr"])

    def test_the_supervisor_has_no_standard_input_and_writes_only_to_its_own_files(self):
        # The launching helper's standard input is an open pipe, so a supervisor that merely
        # inherited it would show that pipe here instead of /dev/null.
        _helper, process = self.launch_from_helper([stub_argv(self.log, "a", gate=self.gate)], ("a",))
        wait_for(self.logged, "the stub to start")
        self.assertEqual(
            standard_streams(process["supervisor_pid"]),
            {
                0: "/dev/null",
                1: str(self.invocation / "supervisor.out"),
                2: str(self.invocation / "supervisor.err"),
            },
        )
        self.gate.write_text("open", encoding="utf-8")
        wait_for_json(self.invocation / "exit.json")

    def test_an_existing_empty_invocation_directory_is_refused(self):
        self.invocation.mkdir(parents=True)
        with self.assertRaises(FileExistsError):
            launcher.start(
                self.invocation, [stub_argv(self.log, "a")], cwd=self.root, identity=self.identity("a"),
            )
        self.assertEqual(list(self.invocation.iterdir()), [])

    def test_the_supervisor_and_its_arms_run_in_the_given_working_directory(self):
        where = [sys.executable, "-c", "import os; print(os.getcwd())"]
        self.launch([where], ("a",))
        wait_for_json(self.invocation / "exit.json")
        self.assertEqual(
            (self.invocation / "output.log").read_text(encoding="utf-8").splitlines(), [str(self.root)],
        )

    def test_a_missing_working_directory_is_refused_before_anything_is_written(self):
        with self.assertRaises(launcher.LaunchError):
            launcher.start(
                self.invocation, [stub_argv(self.log, "a")], cwd=self.root / "absent",
                identity=self.identity("a"),
            )
        self.assertFalse((self.root / "runs").exists())

    def test_every_json_record_is_created_exclusively(self):
        target = self.root / "record.json"
        launcher._write_json(target, {"first": True})
        with self.assertRaises(FileExistsError):
            launcher._write_json(target, {"second": True})
        self.assertEqual(json.loads(target.read_text(encoding="utf-8")), {"first": True})

    def test_an_invocation_directory_is_never_reused(self):
        self.run_two_stubs()
        with self.assertRaises(FileExistsError):
            launcher.start(
                self.invocation, [stub_argv(self.log, "c")], cwd=self.root, identity=self.identity("c"),
            )
        launch = json.loads((self.invocation / "launch.json").read_text(encoding="utf-8"))
        self.assertEqual(launch["arm_ids"], ["a", "b"])

    def test_a_second_supervisor_on_a_finished_invocation_runs_nothing_and_changes_nothing(self):
        self.run_two_stubs()
        before = (self.invocation / "exit.json").read_bytes()
        with self.assertRaises(FileExistsError):
            launcher.supervise(self.invocation)
        self.assertEqual((self.invocation / "exit.json").read_bytes(), before)
        self.assertEqual(sum(1 for row in self.logged() if row[1] == "start"), 2)

    def test_a_malformed_plan_is_refused_before_anything_is_written(self):
        good = stub_argv(self.log, "a")
        cases = {
            "no arms": ([], ()),
            "fewer names than commands": ([good, good], ("a",)),
            "a non-string element": ([[sys.executable, 7]], ("a",)),
            "an empty command": ([[]], ("a",)),
            "a shell string instead of a list": (["echo hi"], ("a",)),
            "a nameless arm": ([good], ("",)),
        }
        for label, (argvs, names) in cases.items():
            with self.subTest(label), self.assertRaises(launcher.LaunchError):
                launcher.start(self.invocation, argvs, cwd=self.root, identity=self.identity(*names))
            self.assertFalse((self.root / "runs").exists(), label)
        with self.assertRaises(launcher.LaunchError):
            launcher.start(self.invocation, [good], cwd=self.root, identity={"sequence": "stub"})
        self.assertFalse((self.root / "runs").exists())


class StaticShapeTests(unittest.TestCase):
    def setUp(self):
        self.tree = ast.parse(LAUNCHER.read_text(encoding="utf-8"))

    def test_the_launcher_installs_no_signal_handlers(self):
        handler_installers = {"signal", "set_wakeup_fd", "siginterrupt", "pthread_sigmask"}
        for node in ast.walk(self.tree):
            if isinstance(node, ast.Call):
                func = node.func
                installs = (
                    isinstance(func, ast.Attribute)
                    and isinstance(func.value, ast.Name)
                    and func.value.id == "signal"
                    and func.attr in handler_installers
                )
                self.assertFalse(installs, ast.dump(func))
            if isinstance(node, ast.ImportFrom) and node.module == "signal":
                self.assertFalse(
                    {alias.name for alias in node.names} & handler_installers, ast.dump(node),
                )

    def test_no_command_is_run_through_a_shell(self):
        for node in ast.walk(self.tree):
            if not isinstance(node, ast.Call):
                continue
            self.assertNotIn("shell", [keyword.arg for keyword in node.keywords], ast.dump(node.func))
            func = node.func
            shells = (
                isinstance(func, ast.Attribute)
                and isinstance(func.value, ast.Name)
                and func.value.id == "os"
                and func.attr in {"system", "popen"}
            )
            self.assertFalse(shells, ast.dump(func))

    def test_loading_the_launcher_imports_nothing_from_the_repository(self):
        # The supervisor sits idle for hours beside a memory-bound arm: it stays standard-library only.
        code = (
            "import importlib.util, sys\n"
            f"spec = importlib.util.spec_from_file_location('l', {str(LAUNCHER)!r})\n"
            "module = importlib.util.module_from_spec(spec)\n"
            "spec.loader.exec_module(module)\n"
            "assert 'torch' not in sys.modules and 'numpy' not in sys.modules, 'heavy import'\n"
            "assert not any(n == 'pinn' or n.startswith('pinn.') for n in sys.modules), 'pinn import'\n"
        )
        completed = subprocess.run(
            [sys.executable, "-B", "-c", code], capture_output=True, text=True, check=False, timeout=60,
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)


RUNG1 = ("r1-1632", "r1-851", "r1-4658")
COMPLETE = {
    "completed_arms": 3, "stopped_arm": None, "stopped_code": None, "signal": None, "wall_clock_secs": 1.0,
}


def stopped(arm_id, code, *, signal_name=None):
    """An exit.json for a sequence that stopped at ``arm_id`` with exit code ``code``."""
    return {
        "completed_arms": RUNG1.index(arm_id), "stopped_arm": arm_id, "stopped_code": code,
        "signal": signal_name, "wall_clock_secs": 1.0,
    }


class RecordedLaunchTestCase(LauncherTestCase):
    """Hand-written launch records for the rung1 sequence under a temporary root: no process starts."""

    sequence = "rung1"

    @property
    def launch_dir(self):
        return self.root / "runs/.launch/phase60" / self.sequence

    def write_invocation(self, ordinal, *, exit_record=None, supervisor_pid=None, finished=0, root=None):
        directory = (root or self.root) / "runs/.launch/phase60" / self.sequence / f"invocation-{ordinal}"
        directory.mkdir(parents=True)
        plan = {
            "schema": launcher.LAUNCH_SCHEMA, "sequence": self.sequence, "arm_ids": list(RUNG1),
            "argvs": [["true"], ["true"], ["true"]], "requested_utc": "t",
        }
        (directory / "launch.json").write_text(json.dumps(plan), encoding="utf-8")
        if supervisor_pid is not None:
            process = {
                "supervisor_pid": supervisor_pid, "session_id": supervisor_pid,
                "process_group": supervisor_pid, "start_utc": "t",
            }
            (directory / "process.json").write_text(json.dumps(process), encoding="utf-8")
        for index in range(1, finished + 1):
            (directory / f"arm-{index}.json").write_text("{}", encoding="utf-8")
        if exit_record is not None:
            (directory / "exit.json").write_text(json.dumps(exit_record), encoding="utf-8")
        return directory


class InvocationTests(RecordedLaunchTestCase):
    def test_a_fresh_launch_is_invocation_one_and_asking_creates_nothing(self):
        self.assertEqual(
            launcher.next_invocation_dir(self.root, "rung1", resume=False),
            (1, self.launch_dir / "invocation-1"),
        )
        self.assertFalse((self.root / "runs").exists())

    def test_a_fresh_launch_refuses_when_the_sequence_launch_directory_exists(self):
        self.launch_dir.mkdir(parents=True)
        with self.assertRaisesRegex(launcher.LaunchError, "already exists"):
            launcher.next_invocation_dir(self.root, "rung1", resume=False)

    def test_a_fresh_launch_refuses_even_over_a_finished_sequence(self):
        self.write_invocation(1, exit_record=COMPLETE)
        with self.assertRaisesRegex(launcher.LaunchError, "already exists"):
            launcher.next_invocation_dir(self.root, "rung1", resume=False)

    def test_a_resume_with_no_previous_invocation_refuses(self):
        with self.assertRaisesRegex(launcher.LaunchError, "no earlier"):
            launcher.next_invocation_dir(self.root, "rung1", resume=True)
        self.launch_dir.mkdir(parents=True)
        with self.assertRaisesRegex(launcher.LaunchError, "no earlier"):
            launcher.next_invocation_dir(self.root, "rung1", resume=True)

    def test_each_sequence_has_its_own_launch_directory(self):
        self.write_invocation(1, exit_record=COMPLETE)
        self.assertEqual(
            launcher.next_invocation_dir(self.root, "sweep-1632", resume=False),
            (1, self.root / "runs/.launch/phase60/sweep-1632/invocation-1"),
        )

    def test_a_single_arm_sequence_keeps_its_colon_in_the_directory_name(self):
        ordinal, directory = launcher.next_invocation_dir(self.root, "arm:r1-1632", resume=False)
        self.assertEqual(
            (ordinal, directory), (1, self.root / "runs/.launch/phase60/arm:r1-1632/invocation-1"),
        )
        directory.mkdir(parents=True)
        self.assertTrue(directory.is_dir())

    def test_a_gap_in_the_invocation_numbers_is_refused(self):
        self.write_invocation(1, exit_record=stopped("r1-851", 130))
        self.write_invocation(3, exit_record=stopped("r1-851", 130))
        with self.assertRaisesRegex(launcher.LaunchError, "not consecutive"):
            launcher.next_invocation_dir(self.root, "rung1", resume=True)

    def test_an_unknown_sequence_is_refused_and_nothing_is_created(self):
        for name in ("rung3", "../rung1", "arm:", "arm:r1-9999"):
            for resume in (False, True):
                with self.subTest(name=name, resume=resume), self.assertRaises(launcher.LaunchError):
                    launcher.next_invocation_dir(self.root, name, resume=resume)
        self.assertFalse((self.root / "runs").exists())


class ResumeGateTests(RecordedLaunchTestCase):
    def test_exactly_the_governed_stop_codes_allow_a_resume(self):
        for code in launcher.GOVERNED_STOP_CODES:
            root = self.new_root()
            record = stopped("r1-851", code)
            self.write_invocation(1, exit_record=record, root=root)
            with self.subTest(code=code):
                self.assertEqual(
                    launcher.next_invocation_dir(root, "rung1", resume=True),
                    (2, root / "runs/.launch/phase60/rung1/invocation-2"),
                )

    def test_a_hand_written_record_without_a_signal_key_is_a_graceful_stop(self):
        for code in launcher.GOVERNED_STOP_CODES:
            record = {"stopped_arm": "r1-851", "stopped_code": code}
            self.assertEqual(launcher.resume_arm_ids(record, "rung1"), ("r1-851", "r1-4658"))

    def test_a_resume_starts_the_stopped_arm_with_resume_then_the_arms_after_it(self):
        record = stopped("r1-851", 130)
        self.assertEqual(
            launcher.resume_argvs(record, "rung1"),
            [launcher.arm_argv("r1-851", resume=True), launcher.arm_argv("r1-4658", resume=False)],
        )
        self.assertEqual(launcher.resume_arm_ids(record, "rung1"), ("r1-851", "r1-4658"))

    def test_a_stop_in_the_first_arm_resumes_all_three_and_a_stop_in_the_last_only_the_last(self):
        self.assertEqual(
            launcher.resume_argvs(stopped("r1-1632", 129), "rung1"),
            [launcher.arm_argv("r1-1632", resume=True), launcher.arm_argv("r1-851", resume=False),
             launcher.arm_argv("r1-4658", resume=False)],
        )
        self.assertEqual(
            launcher.resume_argvs(stopped("r1-4658", 143), "rung1"),
            [launcher.arm_argv("r1-4658", resume=True)],
        )

    def test_a_resume_of_a_resume_continues_from_the_latest_stop(self):
        self.write_invocation(1, exit_record=stopped("r1-851", 130))
        second = self.write_invocation(2, exit_record=stopped("r1-4658", 143))
        ordinal, directory = launcher.next_invocation_dir(self.root, "rung1", resume=True)
        self.assertEqual((ordinal, directory), (3, second.parent / "invocation-3"))
        latest = json.loads((second / "exit.json").read_text(encoding="utf-8"))
        self.assertEqual(
            launcher.resume_argvs(latest, "rung1"), [launcher.arm_argv("r1-4658", resume=True)],
        )

    def test_every_other_ending_goes_to_the_owner(self):
        endings = {
            "complete (no stopped arm)": COMPLETE,
            "stopped_code 0": stopped("r1-851", 0),
            "exit 1 (any failure)": stopped("r1-851", 1),
            "refused arm (2)": stopped("r1-851", 2),
            "owner-routed arm (3)": stopped("r1-851", 3),
            "SIGKILL death (137)": stopped("r1-851", 137, signal_name="SIGKILL"),
            "SIGHUP death, handler never ran (129)": stopped("r1-851", 129, signal_name="SIGHUP"),
            "SIGINT death, handler never ran (130)": stopped("r1-851", 130, signal_name="SIGINT"),
            "SIGTERM death, handler never ran (143)": stopped("r1-851", 143, signal_name="SIGTERM"),
            "128": stopped("r1-851", 128),
            "131": stopped("r1-851", 131),
            "144": stopped("r1-851", 144),
            "255": stopped("r1-851", 255),
            "governed code without a stopped arm": {**stopped("r1-851", 130), "stopped_arm": None},
            "governed code with an empty arm": {**stopped("r1-851", 130), "stopped_arm": ""},
            "no stopped_code": {**stopped("r1-851", 130), "stopped_code": None},
            "a string code": {**stopped("r1-851", 130), "stopped_code": "130"},
            "an arm outside the sequence": {**stopped("r1-851", 130), "stopped_arm": "r2b-1632"},
            "a made-up arm": {**stopped("r1-851", 130), "stopped_arm": "nope"},
            "a non-string arm": {**stopped("r1-851", 130), "stopped_arm": 5},
        }
        for label, record in endings.items():
            root = self.new_root()
            self.write_invocation(1, exit_record=record, root=root)
            with self.subTest(label):
                with self.assertRaisesRegex(launcher.LaunchError, "owner"):
                    launcher.next_invocation_dir(root, "rung1", resume=True)
                with self.assertRaisesRegex(launcher.LaunchError, "owner"):
                    launcher.resume_argvs(record, "rung1")
                self.assertFalse((root / "runs/.launch/phase60/rung1/invocation-2").exists())

    def test_a_previous_invocation_without_an_exit_record_goes_to_the_owner(self):
        self.write_invocation(1, supervisor_pid=os.getpid())
        with self.assertRaisesRegex(launcher.LaunchError, "owner.*no exit"):
            launcher.next_invocation_dir(self.root, "rung1", resume=True)

    def test_an_unreadable_exit_record_refuses_the_resume(self):
        for label, text in (("not json", "{"), ("a list", "[130]"), ("empty", "")):
            root = self.new_root()
            directory = self.write_invocation(1, root=root)
            (directory / "exit.json").write_text(text, encoding="utf-8")
            with self.subTest(label), self.assertRaises(launcher.LaunchError):
                launcher.next_invocation_dir(root, "rung1", resume=True)

    def test_the_resume_commands_keep_the_closed_catalog(self):
        with self.assertRaises(launcher.LaunchError):
            launcher.resume_argvs(stopped("r1-851", 130), "rung3")


class StatusTests(RecordedLaunchTestCase):
    def lines(self, root=None):
        """The status lines, checking that what was returned is exactly what was printed."""
        printed = io.StringIO()
        with contextlib.redirect_stdout(printed):
            returned = launcher.status("rung1", repo_root=root or self.root)
        self.assertEqual(printed.getvalue(), "".join(line + "\n" for line in returned))
        return returned

    def write_arm_process(self, arm_id, payload):
        directory = self.root / "runs/phase60" / arm_id
        directory.mkdir(parents=True, exist_ok=True)
        (directory / "process.json").write_text(
            payload if isinstance(payload, str) else json.dumps(payload), encoding="utf-8",
        )

    def test_no_launch_directory_is_not_launched_and_creates_nothing(self):
        self.assertEqual(self.lines(), ["SEQUENCE-NOT-LAUNCHED"])
        self.assertFalse((self.root / "runs").exists())

    def test_a_live_supervisor_without_an_exit_record_is_running(self):
        self.write_invocation(1, supervisor_pid=os.getpid())
        self.assertEqual(self.lines(), ["SEQUENCE-RUNNING"])

    def test_the_running_arm_process_id_is_printed_on_a_second_line(self):
        self.write_invocation(1, supervisor_pid=os.getpid(), finished=1)
        self.write_arm_process("r1-851", {"pid": 4242, "arm_id": "r1-851", "resume": False})
        self.write_arm_process("r1-1632", {"pid": 111})
        self.assertEqual(self.lines(), ["SEQUENCE-RUNNING", "ARM-PID 4242"])

    def test_only_the_running_arms_process_file_is_read(self):
        self.write_invocation(1, supervisor_pid=os.getpid(), finished=1)
        self.write_arm_process("r1-1632", {"pid": 111})
        self.write_arm_process("r1-4658", {"pid": 333})
        self.assertEqual(self.lines(), ["SEQUENCE-RUNNING"])

    def test_an_unusable_arm_process_file_adds_no_line(self):
        self.write_invocation(1, supervisor_pid=os.getpid())
        for label, payload in (
            ("not json", "{"), ("no pid", {"arm_id": "r1-1632"}), ("a string pid", {"pid": "4242"}),
            ("a boolean pid", {"pid": True}),
        ):
            self.write_arm_process("r1-1632", payload)
            with self.subTest(label):
                self.assertEqual(self.lines(), ["SEQUENCE-RUNNING"])
            (self.root / "runs/phase60/r1-1632/process.json").unlink()

    def test_every_arm_recorded_but_no_exit_yet_is_still_running_without_an_arm_pid(self):
        self.write_invocation(1, supervisor_pid=os.getpid(), finished=3)
        self.write_arm_process("r1-4658", {"pid": 333})
        self.assertEqual(self.lines(), ["SEQUENCE-RUNNING"])

    def test_an_exit_record_without_a_stopped_arm_is_complete(self):
        self.write_invocation(1, exit_record=COMPLETE, finished=3)
        self.assertEqual(self.lines(), ["SEQUENCE-COMPLETE"])

    def test_a_stopped_arm_reports_the_arm_and_the_code(self):
        self.write_invocation(1, exit_record=stopped("r1-851", 130), finished=2)
        self.assertEqual(self.lines(), ["SEQUENCE-STOPPED r1-851 130"])
        other = self.new_root()
        self.write_invocation(1, exit_record=stopped("r1-1632", 137, signal_name="SIGKILL"), root=other)
        self.assertEqual(self.lines(other), ["SEQUENCE-STOPPED r1-1632 137"])

    def test_the_latest_invocation_decides(self):
        self.write_invocation(1, exit_record=stopped("r1-851", 130))
        self.write_invocation(2, supervisor_pid=os.getpid())
        self.assertEqual(self.lines(), ["SEQUENCE-RUNNING"])

    def test_a_supervisor_that_is_gone_without_an_exit_record_goes_to_the_owner(self):
        gone = subprocess.Popen([sys.executable, "-c", "pass"])
        gone.wait()
        self.write_invocation(1, supervisor_pid=gone.pid)
        with self.assertRaisesRegex(launcher.LaunchError, "owner"):
            launcher.status("rung1", repo_root=self.root)

    def test_a_recorded_process_id_that_is_not_a_single_process_is_never_probed_as_alive(self):
        # os.kill(0, 0) would succeed for the caller's own process group, so a zero must read as gone.
        for pid in (0, -1, None, "123", True):
            root = self.new_root()
            self.write_invocation(1, supervisor_pid=pid, root=root)
            with self.subTest(pid=pid), self.assertRaisesRegex(launcher.LaunchError, "owner"):
                launcher.status("rung1", repo_root=root)

    def test_an_unreadable_exit_record_is_refused_not_guessed(self):
        directory = self.write_invocation(1, supervisor_pid=os.getpid())
        (directory / "exit.json").write_text("{", encoding="utf-8")
        with self.assertRaises(launcher.LaunchError):
            launcher.status("rung1", repo_root=self.root)

    def test_a_launch_directory_without_an_invocation_is_refused(self):
        self.launch_dir.mkdir(parents=True)
        with self.assertRaises(launcher.LaunchError):
            launcher.status("rung1", repo_root=self.root)

    def test_an_unknown_sequence_is_refused_and_nothing_is_created(self):
        with self.assertRaises(launcher.LaunchError):
            launcher.status("rung3", repo_root=self.root)
        self.assertFalse((self.root / "runs").exists())

    def test_a_real_supervisor_reads_running_and_then_complete(self):
        ordinal, directory = launcher.next_invocation_dir(self.root, "rung1", resume=False)
        process = launcher.start(
            directory, [stub_argv(self.log, "a", gate=self.gate)], cwd=self.root,
            identity={"sequence": "rung1", "arm_ids": ["r1-1632"]},
        )
        self.addCleanup(kill_if_ours, process["supervisor_pid"], str(self.root), group=True)
        wait_for(self.logged, "the stub to start")
        self.write_arm_process("r1-1632", {"pid": 777})
        self.assertEqual(self.lines(), ["SEQUENCE-RUNNING", "ARM-PID 777"])
        self.gate.write_text("open", encoding="utf-8")
        wait_for_json(directory / "exit.json")
        self.assertEqual(self.lines(), ["SEQUENCE-COMPLETE"])


def admission_stub(log, outcomes):
    """A command builder: each arm's command logs its id, prints its canned text and exits with its code."""
    program = (
        "import sys; open(sys.argv[1], 'a').write(sys.argv[2] + '\\n'); "
        "sys.stdout.write(sys.argv[3]); sys.exit(int(sys.argv[4]))"
    )

    def build(arm_id):
        text, code = outcomes[arm_id]
        return [sys.executable, "-c", program, str(log), arm_id, text, str(code)]

    return build


ALL_ADMITTED = {arm_id: (f"ADMIT-OK {arm_id}\n", 0) for arm_id in RUNG1}


class DryRunTests(LauncherTestCase):
    def dry_run(self, outcomes, sequence="rung1"):
        printed, errors = io.StringIO(), io.StringIO()
        build = admission_stub(self.log, outcomes)
        with contextlib.redirect_stdout(printed), contextlib.redirect_stderr(errors):
            try:
                launcher.dry_run(sequence, cwd=self.root, command_builder=build)
                error = None
            except launcher.LaunchError as exc:
                error = exc
        probed = self.log.read_text(encoding="utf-8").split() if self.log.is_file() else []
        return error, printed.getvalue(), errors.getvalue(), probed

    def test_the_default_admission_command_is_the_runner_with_admit_only(self):
        self.assertEqual(
            launcher.admit_argv("r1-1632"),
            [
                "<home>/miniforge3/envs/pinn-train/bin/python", "-B", "-m",
                "pinn.verification.learnability_run", "r1-1632", "--admit-only",
            ],
        )
        with self.assertRaises(launcher.LaunchError):
            launcher.admit_argv("../r1-1632")

    def test_every_arm_admitted_passes_and_the_runner_lines_are_relayed(self):
        error, printed, _errors, probed = self.dry_run(ALL_ADMITTED)
        self.assertIsNone(error)
        self.assertEqual(printed.splitlines(), [f"ADMIT-OK {arm_id}" for arm_id in RUNG1])
        self.assertEqual(probed, list(RUNG1))

    def test_a_bare_admit_ok_line_is_enough(self):
        outcomes = {arm_id: ("ADMIT-OK\n", 0) for arm_id in RUNG1}
        error, _printed, _errors, _probed = self.dry_run(outcomes)
        self.assertIsNone(error)

    def test_one_refusal_fails_the_dry_run_but_every_arm_is_still_probed(self):
        outcomes = {**ALL_ADMITTED, "r1-851": ("ADMIT-REFUSED: no protocol\n", 2)}
        error, printed, _errors, probed = self.dry_run(outcomes)
        self.assertIsInstance(error, launcher.LaunchError)
        self.assertIn("r1-851", str(error))
        self.assertNotIn("r1-1632", str(error))
        self.assertEqual(probed, list(RUNG1))
        self.assertIn("ADMIT-REFUSED: no protocol", printed)

    def test_anything_short_of_a_clean_admit_ok_is_a_refusal(self):
        cases = {
            "ADMIT-OK but a non-zero exit": ("ADMIT-OK r1-851\n", 1),
            "a clean exit with no admission line": ("all good\n", 0),
            "a clean exit with no output at all": ("", 0),
            "both tokens": ("ADMIT-OK r1-851\nADMIT-REFUSED: later\n", 0),
            "the token only inside a longer word": ("NOT-ADMIT-OK r1-851\n", 0),
        }
        for label, outcome in cases.items():
            outcomes = {**ALL_ADMITTED, "r1-851": outcome}
            self.log.unlink(missing_ok=True)
            with self.subTest(label):
                error, _printed, _errors, _probed = self.dry_run(outcomes)
                self.assertIsInstance(error, launcher.LaunchError)
                self.assertIn("r1-851", str(error))

    def test_a_dry_run_starts_no_supervisor_and_writes_nothing(self):
        with mock.patch.object(launcher, "start") as start, mock.patch.object(launcher, "supervise") as supervise:
            error, _printed, _errors, _probed = self.dry_run(ALL_ADMITTED)
        self.assertIsNone(error)
        start.assert_not_called()
        supervise.assert_not_called()
        self.assertFalse((self.root / "runs").exists())

    def test_the_dry_run_uses_the_closed_sequences_only(self):
        with self.assertRaises(launcher.LaunchError):
            launcher.dry_run("rung3", cwd=self.root, command_builder=admission_stub(self.log, ALL_ADMITTED))
        self.assertFalse(self.log.exists())


class CommandLineTests(LauncherTestCase):
    def main(self, *argv, **kwargs):
        printed, errors = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(printed), contextlib.redirect_stderr(errors):
            code = launcher.main(list(argv), repo_root=self.root, **kwargs)
        return code, printed.getvalue(), errors.getvalue()

    def test_status_prints_the_state_and_exits_zero(self):
        self.assertEqual(
            self.main("--sequence", "rung1", "--status"), (0, "SEQUENCE-NOT-LAUNCHED\n", ""),
        )
        self.assertFalse((self.root / "runs").exists())

    def test_dry_run_exits_zero_only_when_every_arm_prints_admit_ok(self):
        build = admission_stub(self.log, ALL_ADMITTED)
        code, printed, errors = self.main("--sequence", "rung1", "--dry-run", command_builder=build)
        self.assertEqual((code, errors), (0, ""))
        self.assertEqual(printed.count("ADMIT-OK"), 3)
        refused = admission_stub(self.log, {**ALL_ADMITTED, "r1-4658": ("ADMIT-REFUSED: x\n", 2)})
        code, printed, errors = self.main("--sequence", "rung1", "--dry-run", command_builder=refused)
        self.assertEqual(code, 1)
        self.assertIn("FAIL-CLOSED", errors)
        self.assertIn("r1-4658", errors)

    def test_the_actions_are_mutually_exclusive(self):
        for flags in (
            ("--status", "--dry-run"), ("--status", "--resume"), ("--dry-run", "--resume"),
            ("--status", "--supervise", "somewhere"),
        ):
            with self.subTest(flags=flags):
                with self.assertRaises(SystemExit) as caught:
                    self.main("--sequence", "rung1", *flags)
                self.assertEqual(caught.exception.code, 2)

    def test_a_sequence_is_required_and_flags_cannot_be_abbreviated(self):
        for argv in ((), ("--status",), ("--sequence", "rung1", "--stat"), ("--sequence", "rung1", "--dry")):
            with self.subTest(argv=argv):
                with self.assertRaises(SystemExit) as caught:
                    self.main(*argv)
                self.assertEqual(caught.exception.code, 2)

    def test_an_unknown_sequence_fails_closed_for_every_action_and_creates_nothing(self):
        build = admission_stub(self.log, ALL_ADMITTED)
        for flags in ((), ("--resume",), ("--dry-run",), ("--status",)):
            with self.subTest(flags=flags):
                code, printed, errors = self.main("--sequence", "rung3", *flags, command_builder=build)
                self.assertEqual((code, printed), (1, ""))
                self.assertIn("FAIL-CLOSED", errors)
        self.assertFalse((self.root / "runs").exists())
        self.assertFalse(self.log.exists())

    def test_a_launch_prints_the_sequence_and_invocation_and_returns_without_waiting(self):
        fake = self.root / "runs/.launch/phase60/rung1/invocation-1"
        with mock.patch.object(launcher, "launch", return_value=(1, fake)) as launch:
            code, printed, errors = self.main("--sequence", "rung1")
        self.assertEqual((code, printed, errors), (0, "LAUNCHED rung1 invocation-1\n", ""))
        launch.assert_called_once_with("rung1", resume=False, repo_root=self.root)

    def test_a_resume_prints_the_new_invocation(self):
        fake = self.root / "runs/.launch/phase60/rung1/invocation-2"
        with mock.patch.object(launcher, "launch", return_value=(2, fake)) as launch:
            code, printed, _errors = self.main("--sequence", "rung1", "--resume")
        self.assertEqual((code, printed), (0, "LAUNCHED rung1 invocation-2\n"))
        launch.assert_called_once_with("rung1", resume=True, repo_root=self.root)

    def test_a_refused_launch_exits_one_and_prints_nothing_on_standard_output(self):
        with mock.patch.object(launcher, "launch", side_effect=launcher.LaunchError("arm cannot resume; owner decides")):
            code, printed, errors = self.main("--sequence", "rung1", "--resume")
        self.assertEqual((code, printed), (1, ""))
        self.assertIn("FAIL-CLOSED", errors)
        self.assertIn("owner decides", errors)

    def test_the_internal_supervise_action_needs_no_sequence(self):
        with mock.patch.object(launcher, "supervise", return_value=0) as supervise:
            code, _printed, _errors = self.main("--supervise", str(self.root / "somewhere"))
        self.assertEqual(code, 0)
        supervise.assert_called_once_with(self.root / "somewhere")


class LaunchTests(LauncherTestCase):
    """launch() with stub commands: the whole path from the gate to a finished supervisor."""

    def builder(self, codes=None, gate=None):
        codes = codes or {}

        def build(arm_id, *, resume):
            name = arm_id + ("+resume" if resume else "")
            return stub_argv(self.log, name, gate=gate, code=0 if resume else codes.get(arm_id, 0))

        return build

    def run_launch(self, sequence="rung1", *, resume=False, build=None):
        ordinal, directory = launcher.launch(
            sequence, resume=resume, repo_root=self.root, argv_builder=build or self.builder(),
            host_check=lambda: None,
        )
        process = json.loads((directory / "process.json").read_text(encoding="utf-8"))
        self.addCleanup(kill_if_ours, process["supervisor_pid"], str(self.root), group=True)
        return ordinal, directory

    def started(self):
        return [row[0] for row in self.logged() if row[1] == "start"]

    def test_a_fresh_launch_runs_the_whole_sequence_in_order(self):
        ordinal, directory = self.run_launch()
        self.assertEqual((ordinal, directory), (1, self.root / "runs/.launch/phase60/rung1/invocation-1"))
        exit_record = wait_for_json(directory / "exit.json")
        self.assertEqual(self.started(), list(RUNG1))
        self.assertEqual(
            (exit_record["completed_arms"], exit_record["stopped_arm"]), (3, None),
        )

    def test_launch_json_names_the_sequence_the_arms_the_kind_and_the_code_commit(self):
        _ordinal, directory = self.run_launch()
        wait_for_json(directory / "exit.json")
        launch = json.loads((directory / "launch.json").read_text(encoding="utf-8"))
        self.assertEqual(launch["sequence"], "rung1")
        self.assertEqual(launch["arm_ids"], list(RUNG1))
        self.assertEqual(launch["invocation_ordinal"], 1)
        self.assertEqual(launch["launch_kind"], "fresh")
        self.assertEqual(launch["git_head"], launcher._git_head())
        self.assertRegex(launch["git_head"], r"^[0-9a-f]{40}$")
        build = self.builder()
        self.assertEqual(launch["argvs"], [build(arm_id, resume=False) for arm_id in RUNG1])
        self.assertEqual(set(launch), {
            "schema", "sequence", "arm_ids", "invocation_ordinal", "launch_kind", "git_head",
            "argvs", "requested_utc",
        })

    def test_a_failing_host_probe_refuses_before_anything_is_written(self):
        def failing():
            raise launcher.LaunchError("this process cannot see the host Metal device")

        with self.assertRaisesRegex(launcher.LaunchError, "Metal"):
            launcher.launch(
                "rung1", resume=False, repo_root=self.root, argv_builder=self.builder(), host_check=failing,
            )
        self.assertFalse((self.root / "runs").exists())

    def test_an_unknown_sequence_is_refused_before_the_host_probe_runs(self):
        probed = []
        with self.assertRaises(launcher.LaunchError):
            launcher.launch(
                "rung3", resume=False, repo_root=self.root, argv_builder=self.builder(),
                host_check=lambda: probed.append(True),
            )
        self.assertEqual(probed, [])
        self.assertFalse((self.root / "runs").exists())

    def test_a_governed_stop_resumes_the_stopped_arm_with_resume_and_then_the_rest(self):
        _ordinal, first = self.run_launch(build=self.builder(codes={"r1-851": 130}))
        record = wait_for_json(first / "exit.json")
        self.assertEqual((record["stopped_arm"], record["stopped_code"]), ("r1-851", 130))
        self.assertEqual(self.started(), ["r1-1632", "r1-851"])
        ordinal, second = self.run_launch(resume=True)
        self.assertEqual((ordinal, second), (2, first.parent / "invocation-2"))
        done = wait_for_json(second / "exit.json")
        self.assertEqual(self.started(), ["r1-1632", "r1-851", "r1-851+resume", "r1-4658"])
        self.assertEqual((done["completed_arms"], done["stopped_arm"]), (2, None))
        launch = json.loads((second / "launch.json").read_text(encoding="utf-8"))
        self.assertEqual(launch["arm_ids"], ["r1-851", "r1-4658"])
        self.assertEqual((launch["invocation_ordinal"], launch["launch_kind"]), (2, "resume"))
        self.assertEqual(
            launch["argvs"], [stub_argv(self.log, "r1-851+resume"), stub_argv(self.log, "r1-4658")],
        )

    def test_a_stop_that_cannot_resume_goes_to_the_owner_and_starts_nothing(self):
        for code in (137, 2, 3, 1):
            root = self.new_root()
            with self.subTest(code=code):
                ordinal, first = launcher.launch(
                    "rung1", resume=False, repo_root=root,
                    argv_builder=self.builder(codes={"r1-851": code}), host_check=lambda: None,
                )
                process = json.loads((first / "process.json").read_text(encoding="utf-8"))
                self.addCleanup(kill_if_ours, process["supervisor_pid"], str(root), group=True)
                wait_for_json(first / "exit.json")
                with self.assertRaisesRegex(launcher.LaunchError, "owner"):
                    launcher.launch(
                        "rung1", resume=True, repo_root=root, argv_builder=self.builder(),
                        host_check=lambda: None,
                    )
                self.assertFalse((first.parent / "invocation-2").exists())

    def test_an_arm_killed_by_a_signal_cannot_resume_even_though_its_code_is_governed(self):
        def build(arm_id, *, resume):
            if arm_id == "r1-851":
                kill_itself = "import os, signal, time; os.kill(os.getpid(), signal.SIGTERM); time.sleep(30)"
                return [sys.executable, "-c", kill_itself]
            return stub_argv(self.log, arm_id)

        _ordinal, first = self.run_launch(build=build)
        record = wait_for_json(first / "exit.json")
        self.assertEqual(
            (record["stopped_arm"], record["stopped_code"], record["signal"]), ("r1-851", 143, "SIGTERM"),
        )
        with self.assertRaisesRegex(launcher.LaunchError, "owner"):
            self.run_launch(resume=True)
        self.assertFalse((first.parent / "invocation-2").exists())

    def test_a_second_fresh_launch_of_the_same_sequence_is_refused(self):
        _ordinal, first = self.run_launch()
        wait_for_json(first / "exit.json")
        with self.assertRaisesRegex(launcher.LaunchError, "already exists"):
            self.run_launch()
        self.assertEqual(self.started(), list(RUNG1))

    def test_a_resume_after_a_completed_sequence_is_refused(self):
        _ordinal, first = self.run_launch()
        wait_for_json(first / "exit.json")
        with self.assertRaisesRegex(launcher.LaunchError, "owner"):
            self.run_launch(resume=True)

    def test_a_resume_is_refused_while_the_previous_invocation_is_still_running(self):
        _ordinal, first = self.run_launch(build=self.builder(codes={"r1-851": 130}))
        wait_for_json(first / "exit.json")
        _ordinal, second = self.run_launch(resume=True, build=self.builder(gate=self.gate))
        wait_for(lambda: "r1-851+resume" in self.started(), "the resumed arm to start")
        with self.assertRaisesRegex(launcher.LaunchError, "owner"):
            self.run_launch(resume=True)
        self.assertFalse((first.parent / "invocation-3").exists())
        self.gate.write_text("open", encoding="utf-8")
        wait_for_json(second / "exit.json")

    def test_the_arms_run_in_the_repository_root_that_was_given(self):
        def where(arm_id, *, resume):
            return [sys.executable, "-c", "import os; print(os.getcwd())"]

        _ordinal, directory = self.run_launch("arm:r1-1632", build=where)
        wait_for_json(directory / "exit.json")
        self.assertEqual(
            (directory / "output.log").read_text(encoding="utf-8").splitlines(), [str(self.root)],
        )

    def test_a_single_arm_sequence_runs_under_a_directory_named_with_its_colon(self):
        ordinal, directory = self.run_launch("arm:r1-1632")
        self.assertEqual(directory, self.root / "runs/.launch/phase60/arm:r1-1632/invocation-1")
        done = wait_for_json(directory / "exit.json")
        self.assertEqual(self.started(), ["r1-1632"])
        self.assertEqual((ordinal, done["completed_arms"], done["stopped_arm"]), (1, 1, None))


class SurvivalTests(LauncherTestCase):
    def test_the_supervisor_outlives_a_hangup_and_kill_of_the_launching_process_group(self):
        # Mirrors the generation-6 loss: the caller's whole process group goes away mid-arm.
        argvs = [stub_argv(self.log, "a", gate=self.gate), stub_argv(self.log, "b")]
        helper, process = self.launch_from_helper(argvs, ("a", "b"))
        wait_for(self.logged, "the first stub to start")
        self.assertNotEqual(process["process_group"], helper.pid)
        self.assertNotEqual(process["session_id"], helper.pid)
        os.killpg(helper.pid, signal.SIGHUP)
        try:
            os.killpg(helper.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
        helper.wait(timeout=10)
        self.assertLess(helper.returncode, 0)
        os.kill(process["supervisor_pid"], 0)  # the supervisor is still there
        self.assertFalse((self.invocation / "exit.json").exists())
        self.gate.write_text("open", encoding="utf-8")
        exit_record = wait_for_json(self.invocation / "exit.json")
        self.assertEqual(
            (exit_record["completed_arms"], exit_record["stopped_arm"], exit_record["stopped_code"]),
            (2, None, None),
        )
        self.assertEqual(
            [(row[0], row[1]) for row in self.logged()],
            [("a", "start"), ("a", "end"), ("b", "start"), ("b", "end")],
        )


if __name__ == "__main__":
    unittest.main()
