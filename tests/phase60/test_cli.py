"""Phase 60 (SPEC Requirement 8, SCOPE-44): the real-arm command line.

The runner takes one catalog arm id and nothing else: no runtime, no precision and no
path. Admission comes first, a run takes the single launch lock and records its own PID,
and one top-level handler maps the three governed exits. Every test patches the corpus
open and ``run_arm``; the repository root is redirected to a temporary directory, so
nothing is written into the checkout and nothing trains.
"""

from __future__ import annotations

import io
import json
import os
import shutil
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest import mock

from pinn.verification import evidence_io, learnability_run
from pinn.verification.feasibility_scorecard import OwnerRouted
from pinn.verification.learnability_arms import REAL_RUNTIME, SEED
from pinn.verification.learnability_protocol import AdmissionRefused
from pinn.verification.learnability_run import (
    CrossCheckDisagreement,
    GovernedStop,
    main,
)

ARM = "r1-1632"
ADMISSION = {
    "arm_id": ARM,
    "first_omega_0": 30.0,
    "clip_enabled": True,
}


class _CliCase(unittest.TestCase):
    """A temporary repository root, a captured stdout and a corpus that must not open."""

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="phase60-cli-"))
        self.addCleanup(shutil.rmtree, self.tmp, True)
        patcher = mock.patch.object(learnability_run, "_repo_root", lambda: self.tmp)
        patcher.start()
        self.addCleanup(patcher.stop)
        learnability_run._reset_stop()
        self.addCleanup(learnability_run._reset_stop)

    @property
    def evidence(self):
        return self.tmp / learnability_run.EVIDENCE_REL

    def run_main(self, argv):
        printed = io.StringIO()
        with redirect_stdout(printed), redirect_stderr(printed):
            code = main(argv)
        return code, printed.getvalue()

    def no_corpus(self):
        """A patch that fails the test if the real corpus is opened or a record is read."""
        def forbidden(*args, **kwargs):
            raise AssertionError("the corpus was opened")

        return mock.patch.object(learnability_run, "open_real_context", forbidden)


class ArgvTests(_CliCase):
    """One catalog arm id, and only ``--resume`` or ``--admit-only`` beside it."""

    def test_the_parser_accepts_the_three_legal_forms(self):
        for argv, resume, admit_only in (
            ([ARM], False, False),
            ([ARM, "--resume"], True, False),
            ([ARM, "--admit-only"], False, True),
        ):
            with self.subTest(argv=argv):
                arm_id, parsed_resume, parsed_admit = learnability_run._parse_argv(argv)
                self.assertEqual((arm_id, parsed_resume, parsed_admit), (ARM, resume, admit_only))

    def test_an_unknown_id_is_refused_before_admission(self):
        with mock.patch.object(learnability_run, "admit_arm") as admit, self.no_corpus():
            code, printed = self.run_main(["not-an-arm"])
        self.assertEqual(code, 2)
        self.assertTrue(printed.startswith("ADMIT-REFUSED: "), printed)
        self.assertEqual(admit.call_count, 0)

    def test_a_fixture_id_is_not_a_catalog_arm(self):
        with mock.patch.object(learnability_run, "admit_arm") as admit, self.no_corpus():
            code, printed = self.run_main(["fixture-hierarchical-gold-0"])
        self.assertEqual(code, 2)
        self.assertTrue(printed.startswith("ADMIT-REFUSED: "), printed)
        self.assertEqual(admit.call_count, 0)

    def test_a_path_is_refused(self):
        with mock.patch.object(learnability_run, "admit_arm") as admit, self.no_corpus():
            code, _printed = self.run_main(["/tmp/somewhere/r1-1632"])
        self.assertEqual(code, 2)
        self.assertEqual(admit.call_count, 0)

    def test_a_runtime_or_precision_flag_does_not_exist(self):
        for flag in ("--device", "--precision", "--runtime", "--seed"):
            with self.subTest(flag=flag):
                with mock.patch.object(learnability_run, "admit_arm") as admit, self.no_corpus():
                    code, printed = self.run_main([ARM, flag, "float64"])
                self.assertEqual(code, 2)
                self.assertIn("USAGE-REFUSED", printed)
                self.assertEqual(admit.call_count, 0)

    def test_the_two_flags_are_mutually_exclusive_and_appear_once(self):
        for argv in (
            [ARM, "--resume", "--admit-only"],
            [ARM, "--resume", "--resume"],
            [ARM, "--admit-only", "--admit-only"],
        ):
            with self.subTest(argv=argv):
                with mock.patch.object(learnability_run, "admit_arm") as admit, self.no_corpus():
                    code, _printed = self.run_main(argv)
                self.assertEqual(code, 2)
                self.assertEqual(admit.call_count, 0)

    def test_a_second_arm_id_is_refused(self):
        with mock.patch.object(learnability_run, "admit_arm") as admit, self.no_corpus():
            code, _printed = self.run_main([ARM, "r1-851"])
        self.assertEqual(code, 2)
        self.assertEqual(admit.call_count, 0)

    def test_no_arm_id_is_refused(self):
        with mock.patch.object(learnability_run, "admit_arm") as admit, self.no_corpus():
            code, _printed = self.run_main([])
        self.assertEqual(code, 2)
        self.assertEqual(admit.call_count, 0)

    def test_the_runner_has_no_runtime_precision_or_path_argument(self):
        import inspect

        parameters = inspect.signature(learnability_run.run_arm).parameters
        for name in ("runtime", "dtype", "device", "precision", "path"):
            with self.subTest(name=name):
                if name == "runtime":
                    # The runtime is a parameter of run_arm but the command line never
                    # supplies one: main always passes the real pair.
                    self.assertIn(name, parameters)
                else:
                    self.assertNotIn(name, parameters)


class AdmitOnlyTests(_CliCase):
    """``--admit-only`` prints the admission line and creates nothing."""

    def test_admit_ok_prints_the_arm_and_exits_zero_without_a_run_tree(self):
        with mock.patch.object(learnability_run, "admit_arm", return_value=dict(ADMISSION)) as admit, \
                self.no_corpus():
            code, printed = self.run_main([ARM, "--admit-only"])
        self.assertEqual(code, 0)
        self.assertEqual(printed, f"ADMIT-OK {ARM}\n")
        self.assertEqual(admit.call_args.kwargs["resume"], False)
        self.assertFalse((self.tmp / "runs" / "phase60" / ARM).exists())

    def test_a_refused_admission_prints_the_reason_and_exits_two(self):
        with mock.patch.object(
            learnability_run, "admit_arm",
            side_effect=AdmissionRefused("the run protocol is not tracked and clean"),
        ), self.no_corpus():
            code, printed = self.run_main([ARM, "--admit-only"])
        self.assertEqual(code, 2)
        self.assertEqual(printed, "ADMIT-REFUSED: the run protocol is not tracked and clean\n")
        self.assertFalse((self.tmp / "runs" / "phase60" / ARM).exists())

    def test_a_run_that_is_refused_prints_the_same_line_and_exits_two(self):
        with mock.patch.object(
            learnability_run, "admit_arm", side_effect=AdmissionRefused("no protocol")
        ), self.no_corpus():
            code, printed = self.run_main([ARM])
        self.assertEqual(code, 2)
        self.assertEqual(printed, "ADMIT-REFUSED: no protocol\n")

    def test_admit_only_never_asks_for_a_resume(self):
        with mock.patch.object(learnability_run, "admit_arm", return_value=dict(ADMISSION)) as admit, \
                self.no_corpus():
            self.run_main([ARM, "--admit-only"])
        self.assertEqual(admit.call_args.args, (ARM,))
        self.assertEqual(admit.call_args.kwargs["resume"], False)


class LifecycleTests(_CliCase):
    """A run: process.json first, the one-launch lock, the real runtime, one release."""

    def _run(self, *, admission=None, run_arm_side_effect=None, argv=(ARM,)):
        context = object()
        protocol = object()
        recorded = {}

        def fake_run_arm(spec, **kwargs):
            recorded["spec"] = spec
            recorded["kwargs"] = kwargs
            recorded["process"] = json.loads(
                (self.tmp / "runs" / "phase60" / spec.arm_id / "process.json").read_bytes()
            )
            recorded["locked"] = (self.evidence / "logs" / "launch.lock.log").is_file()
            if run_arm_side_effect is not None:
                raise run_arm_side_effect
            return {"arm_id": spec.arm_id}

        with mock.patch.object(
            learnability_run, "admit_arm", return_value=dict(admission or ADMISSION)
        ), mock.patch.object(
            learnability_run, "open_real_context", return_value=context
        ) as opened, mock.patch.object(
            learnability_run, "load_protocol", return_value=protocol
        ) as loaded, mock.patch.object(
            learnability_run, "load_scorecard", return_value="card"
        ) as card, mock.patch.object(
            learnability_run, "run_arm", side_effect=fake_run_arm
        ) as ran:
            code, printed = self.run_main(list(argv))
        return code, printed, recorded, (opened, loaded, card, ran)

    def test_a_run_writes_process_json_before_run_arm_and_takes_the_lock(self):
        code, printed, recorded, _patches = self._run()
        self.assertEqual(code, 0)
        self.assertEqual(printed, f"ADMIT-OK {ARM}\n")
        process = recorded["process"]
        self.assertEqual(process["pid"], os.getpid())
        self.assertEqual(process["arm_id"], ARM)
        self.assertIs(process["resume"], False)
        self.assertIsInstance(process["available_memory_bytes"], int)
        self.assertGreaterEqual(process["available_memory_bytes"], 0)
        self.assertIn("utc_started", process)
        self.assertTrue(recorded["locked"])

    def test_a_resume_asks_admission_and_run_arm_for_a_resume(self):
        code, _printed, recorded, _patches = self._run(argv=(ARM, "--resume"))
        self.assertEqual(code, 0)
        self.assertIs(recorded["process"]["resume"], True)
        self.assertIs(recorded["kwargs"]["resume"], True)

    def test_the_run_passes_the_real_runtime_the_admission_and_its_clip_flag(self):
        code, _printed, recorded, (opened, loaded, card, ran) = self._run()
        self.assertEqual(code, 0)
        kwargs = recorded["kwargs"]
        self.assertEqual(kwargs["runtime"], REAL_RUNTIME)
        self.assertEqual(SEED, 42)
        self.assertEqual(kwargs["admission"]["arm_id"], ARM)
        self.assertIs(kwargs["clip_enabled"], True)
        self.assertEqual(kwargs["resume"], False)
        self.assertEqual(kwargs["evidence_root"], self.evidence)
        self.assertEqual(kwargs["scorecard"], "card")
        self.assertEqual(kwargs["run_dir"], self.tmp / "runs" / "phase60" / ARM)
        self.assertIsNotNone(kwargs["protocol"])
        self.assertEqual(ran.call_count, 1)

    def test_the_lock_is_released_on_the_success_path(self):
        self._run()
        self.assertFalse((self.evidence / "logs" / "launch.lock.log").exists())

    def test_the_lock_is_released_when_run_arm_fails(self):
        with self.assertRaises(RuntimeError):
            self._run(run_arm_side_effect=RuntimeError("boom"))
        self.assertFalse((self.evidence / "logs" / "launch.lock.log").exists())

    def test_a_second_concurrent_run_refuses_with_launch_refused_and_exit_two(self):
        self.evidence.mkdir(parents=True, exist_ok=True)
        run_id = evidence_io.begin_long_step(
            "phase60", "r1-851",
            command=["other"], evidence_root=self.evidence,
        )
        self.addCleanup(
            lambda: (self.evidence / "logs" / "launch.lock.log").unlink(missing_ok=True)
        )
        with mock.patch.object(
            learnability_run, "admit_arm", return_value=dict(ADMISSION)
        ), mock.patch.object(
            learnability_run, "open_real_context"
        ) as opened, mock.patch.object(
            learnability_run, "run_arm"
        ) as ran:
            code, printed = self.run_main([ARM])
        self.assertEqual(code, 2)
        lines = printed.splitlines()
        self.assertEqual(lines[0], f"ADMIT-OK {ARM}")
        self.assertTrue(lines[-1].startswith("LAUNCH-REFUSED: "), printed)
        self.assertEqual(opened.call_count, 0)
        self.assertEqual(ran.call_count, 0)
        self.assertTrue((self.evidence / "logs" / "launch.lock.log").is_file())
        self.assertTrue(run_id)


class ExitMappingTests(_CliCase):
    """One top-level handler: OWNER-ROUTED with exit 3 once, and the governed codes."""

    def _main_with(self, side_effect):
        with mock.patch.object(
            learnability_run, "admit_arm", return_value=dict(ADMISSION)
        ), mock.patch.object(
            learnability_run, "open_real_context", return_value=object()
        ), mock.patch.object(
            learnability_run, "load_protocol", return_value=object()
        ), mock.patch.object(
            learnability_run, "load_scorecard", return_value="card"
        ), mock.patch.object(
            learnability_run, "run_arm", side_effect=side_effect
        ) as ran:
            code, printed = self.run_main([ARM])
        return code, printed, ran

    def test_owner_routed_prints_the_message_and_exits_three_without_a_retry(self):
        for raised in (OwnerRouted("the formula row is missing"), CrossCheckDisagreement("tier 2 vs 1")):
            with self.subTest(raised=type(raised).__name__):
                code, printed, ran = self._main_with(raised)
                self.assertEqual(code, 3)
                self.assertEqual(
                    printed.splitlines(),
                    [f"ADMIT-OK {ARM}", f"OWNER-ROUTED: {raised}"],
                )
                self.assertEqual(ran.call_count, 1)

    def test_a_governed_stop_exits_its_own_code(self):
        for signum_name, code_expected in (("SIGHUP", 129), ("SIGINT", 130), ("SIGTERM", 143)):
            with self.subTest(signal=signum_name):
                stop = GovernedStop(code_expected, signal_name=signum_name, phase="adam", step=2)
                code, printed, ran = self._main_with(stop)
                self.assertEqual(code, code_expected)
                self.assertEqual(printed, f"ADMIT-OK {ARM}\n")
                self.assertEqual(ran.call_count, 1)
    def test_an_unexpected_runtime_error_propagates(self):
        with self.assertRaises(RuntimeError) as caught:
            self._main_with(RuntimeError("not governed"))
        self.assertEqual(str(caught.exception), "not governed")

    def test_a_harness_halt_propagates(self):
        from pinn.verification.learnability_data import HarnessHalt

        with self.assertRaises(HarnessHalt):
            self._main_with(HarnessHalt("a missing record"))

    def test_the_lock_is_released_on_an_owner_routed_exit(self):
        self._main_with(OwnerRouted("stop"))
        self.assertFalse((self.evidence / "logs" / "launch.lock.log").exists())


if __name__ == "__main__":
    unittest.main()
