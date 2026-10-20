"""Phase 60 (SCOPE-44): the detached launcher runs one closed arm sequence one arm at a time.

Every test launches stubs (a short ``python -c`` script) under a TemporaryDirectory. No test
starts a real arm, ``caffeinate`` or the learnability runner.
"""

from __future__ import annotations

import ast
import importlib.util
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


if __name__ == "__main__":
    unittest.main()
