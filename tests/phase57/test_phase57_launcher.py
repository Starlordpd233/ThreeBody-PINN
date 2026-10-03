"""GAP-57-12 L1: the detached Phase-57 launcher outlives its caller and records exits."""

from __future__ import annotations

import importlib.util
import json
import os
import re
import shlex
import signal
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE = ROOT / ".planning/phases/57-corrected-re-run-the-preserved-evaluation/evidence"
LAUNCHER = EVIDENCE / "launch_phase57_run.py"
SPEC = importlib.util.spec_from_file_location("phase57_launcher", LAUNCHER)
assert SPEC is not None and SPEC.loader is not None
launcher = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(launcher)


def wait_for_json(path: Path, timeout: float = 20.0) -> dict:
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        if path.is_file():
            try:
                return json.loads(path.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                pass
        time.sleep(0.05)
    raise AssertionError(f"{path} was not written within {timeout}s")


class TrainerCommandTests(unittest.TestCase):
    def test_command_is_the_generation_six_form_with_the_new_run_name(self) -> None:
        text = (EVIDENCE / "run-ledger.md").read_text(encoding="utf-8")
        ledger = json.loads(re.search(r"```json\n(.*?)\n```", text, re.S).group(1))
        [record] = [r for r in ledger["records"] if r.get("run_name") == "stage0-v23g6-seed42"]
        expected = record["invocations"][0]["command"].replace("v23g6", "v23g7")
        self.assertEqual(
            shlex.join(launcher.trainer_argv("stage0-v23g7-seed42", resume=False)), expected,
        )

    def test_resume_appends_resume_latest(self) -> None:
        argv = launcher.trainer_argv("stage0-v23g7-seed41", resume=True)
        self.assertEqual(argv[-3:], ["--stage-0-only", "--resume", "latest"])

    def test_rejects_run_names_outside_generation_seven(self) -> None:
        for name in ("stage0-v23g6-seed42", "stage0-v23g7-seed44"):
            with self.subTest(name=name), self.assertRaises(launcher.LaunchError):
                launcher.trainer_argv(name, resume=False)


class InvocationDirectoryTests(unittest.TestCase):
    def setUp(self) -> None:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.name = "stage0-v23g7-seed42"
        self.launch_dir = self.root / "runs/.launch" / self.name

    def previous_exit(self, exit_code: int) -> None:
        (self.root / "runs" / self.name).mkdir(parents=True)
        first = self.launch_dir / "invocation-1"
        first.mkdir(parents=True)
        (first / "exit.json").write_text(json.dumps({"exit_code": exit_code}))

    def test_fresh_launch_is_invocation_one(self) -> None:
        self.assertEqual(
            launcher.next_invocation_dir(self.root, self.name, resume=False),
            (1, self.launch_dir / "invocation-1"),
        )

    def test_fresh_launch_refuses_existing_run_or_launch_output(self) -> None:
        for existing in (self.root / "runs" / self.name, self.launch_dir):
            with self.subTest(existing=existing):
                existing.mkdir(parents=True)
                with self.assertRaisesRegex(launcher.LaunchError, "already exists"):
                    launcher.next_invocation_dir(self.root, self.name, resume=False)
                existing.rmdir()

    def test_resume_requires_a_governed_interrupted_predecessor(self) -> None:
        with self.assertRaisesRegex(launcher.LaunchError, "no earlier"):
            launcher.next_invocation_dir(self.root, self.name, resume=True)
        self.previous_exit(1)
        with self.assertRaisesRegex(launcher.LaunchError, "governed interrupted"):
            launcher.next_invocation_dir(self.root, self.name, resume=True)

    def test_resume_after_interrupted_stop_is_the_next_invocation(self) -> None:
        self.previous_exit(130)
        self.assertEqual(
            launcher.next_invocation_dir(self.root, self.name, resume=True),
            (2, self.launch_dir / "invocation-2"),
        )


class DetachedSupervisorTests(unittest.TestCase):
    def setUp(self) -> None:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.invocation = self.root / "runs/.launch/fake/invocation-1"
        self.identity = {"run_name": "fake", "invocation_ordinal": 1, "launch_kind": "fresh"}

    def kill_later(self, pid: int) -> None:
        def cleanup() -> None:
            try:
                os.kill(pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
        self.addCleanup(cleanup)

    def test_records_output_session_and_exit_code(self) -> None:
        argv = [sys.executable, "-c", (
            "import os, sys; print('sid', os.getsid(0), flush=True); "
            "sys.stderr.write('trace line\\n'); sys.exit(3)"
        )]
        process = launcher.start(self.invocation, argv, cwd=self.root, identity=self.identity)
        self.kill_later(process["trainer_pid"])
        exit_record = wait_for_json(self.invocation / "exit.json")
        self.assertEqual(
            (exit_record["returncode"], exit_record["exit_code"], exit_record["signal"]), (3, 3, None),
        )
        self.assertEqual(exit_record["trainer_pid"], process["trainer_pid"])
        self.assertNotEqual(process["session_id"], os.getsid(0))
        output = (self.invocation / "output.log").read_text(encoding="utf-8")
        self.assertIn(f"sid {process['session_id']}", output)
        self.assertIn("trace line", output)
        launch = json.loads((self.invocation / "launch.json").read_text(encoding="utf-8"))
        self.assertEqual(launch["command"], shlex.join(argv))
        self.assertEqual(launch["mode"], "detached-session")

    def test_records_a_signal_death(self) -> None:
        argv = [sys.executable, "-c", "import time; time.sleep(60)"]
        process = launcher.start(self.invocation, argv, cwd=self.root, identity=self.identity)
        self.kill_later(process["trainer_pid"])
        os.kill(process["trainer_pid"], signal.SIGKILL)
        exit_record = wait_for_json(self.invocation / "exit.json")
        self.assertEqual(
            (exit_record["returncode"], exit_record["exit_code"], exit_record["signal"]),
            (-9, 137, "SIGKILL"),
        )

    def test_trainer_survives_a_hangup_and_kill_of_the_launching_process_group(self) -> None:
        # Mirrors the generation-6 loss: the caller's whole process group goes away.
        helper_code = (
            "import importlib.util, sys, time\n"
            "from pathlib import Path\n"
            f"spec = importlib.util.spec_from_file_location('l', {str(LAUNCHER)!r})\n"
            "l = importlib.util.module_from_spec(spec); spec.loader.exec_module(l)\n"
            f"l.start(Path({str(self.invocation)!r}), [sys.executable, '-c', "
            "\"import time; time.sleep(1.5); print('trainer finished', flush=True)\"], "
            f"cwd=Path({str(self.root)!r}), identity={self.identity!r})\n"
            "time.sleep(60)\n"
        )
        helper = subprocess.Popen([sys.executable, "-c", helper_code], start_new_session=True)
        self.kill_later(helper.pid)
        process = wait_for_json(self.invocation / "process.json")
        self.kill_later(process["trainer_pid"])
        os.killpg(helper.pid, signal.SIGHUP)
        os.killpg(helper.pid, signal.SIGKILL)
        helper.wait(timeout=10)
        exit_record = wait_for_json(self.invocation / "exit.json")
        self.assertEqual(exit_record["returncode"], 0)
        self.assertIn("trainer finished", (self.invocation / "output.log").read_text(encoding="utf-8"))

    def test_refuses_to_reuse_an_invocation_directory(self) -> None:
        self.invocation.mkdir(parents=True)
        with self.assertRaises(FileExistsError):
            launcher.start(self.invocation, [sys.executable, "-c", "pass"], cwd=self.root, identity=self.identity)


if __name__ == "__main__":
    unittest.main()
