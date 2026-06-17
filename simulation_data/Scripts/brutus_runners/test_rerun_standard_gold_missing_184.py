import importlib.util
import io
import json
import os
import sys
import tempfile
import textwrap
import unittest
from contextlib import redirect_stderr
from pathlib import Path


MODULE_PATH = Path(__file__).with_name("rerun_standard_gold_missing_184.py")


def load_runner():
    spec = importlib.util.spec_from_file_location("rerun_standard_gold_missing_184", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class StandardGoldRerunTests(unittest.TestCase):
    def setUp(self):
        self.runner = load_runner()

    def test_parse_missing_ids_requires_exact_184_ids(self):
        ids = self.runner.parse_missing_ids(
            Path("simulation_data/Documentation/standard_quasi_random_ids_not_in_gold.md")
        )

        self.assertEqual(184, len(ids))
        self.assertEqual("0038", ids[0])
        self.assertEqual("3958", ids[-1])
        self.assertEqual(len(ids), len(set(ids)))

    def test_build_command_uses_standard_gold_default_contract(self):
        ic_path = Path("simulation_data/Data/ic_final/ic_standard_quasi_random/ic_standard_0038.txt")
        cmd = self.runner.build_brutus_command(Path("brutus_Newton-main/brutus"), ic_path)

        self.assertEqual(
            [
                "brutus_Newton-main/brutus",
                "1e-13",
                "130",
                "0",
                "10",
                "0.01",
                "3",
                str(ic_path),
            ],
            cmd,
        )

    def test_validate_accepts_standard_gold_default_footer_and_first_snapshot(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            ic_path = tmp_path / "ic_standard_0038.txt"
            output_path = tmp_path / "brutus_standard_0038.txt"
            ic_path.write_text(
                "\n".join(
                    [
                        "1.0 1.1 1.2 1.3 1.4 1.5 1.6",
                        "2.0 2.1 2.2 2.3 2.4 2.5 2.6",
                        "3.0 3.1 3.2 3.3 3.4 3.5 3.6",
                    ]
                )
                + "\n"
            )
            output_path.write_text(
                "\n".join(
                    [
                        "0 3 0",
                        "1.0 1.1 1.2 1.3 1.4 1.5 1.6",
                        "2.0 2.1 2.2 2.3 2.4 2.5 2.6",
                        "3.0 3.1 3.2 3.3 3.4 3.5 3.6",
                        "10.01 3 123.456",
                        "1.7 1.8 1.9 2.0 2.1 2.2 1.6",
                        "2.7 2.8 2.9 3.0 3.1 3.2 2.6",
                        "3.7 3.8 3.9 4.0 4.1 4.2 3.6",
                        (
                            "Result: filename= /tmp/ic_standard_0038.txt N= 3 "
                            "t_begin= 0 t_end= 10.01 dt= 0.01 eta= 0.277971 "
                            "tol= 1e-13 Lw= 130 t_cpu= 123.456"
                        ),
                    ]
                )
                + "\n"
            )

            result = self.runner.validate_output(output_path, ic_path)

        self.assertTrue(result.ok, result.errors)
        self.assertEqual("1e-13", result.footer["tol"])
        self.assertEqual("130", result.footer["Lw"])

    def test_validate_rejects_base_standard_and_data05_parameter_families(self):
        base_footer = (
            "Result: filename= /tmp/ic_standard_0038.txt N= 3 "
            "t_begin= 0 t_end= 10.03 dt= 0.17 eta= 0.277971 "
            "tol= 1e-13 Lw= 118 t_cpu= 1"
        )
        data05_footer = (
            "Result: filename= /tmp/ic_standard_0038.txt N= 3 "
            "t_begin= 0 t_end= 10 dt= 0.08 eta= 0.263027 "
            "tol= 1e-15 Lw= 130 t_cpu= 1"
        )

        for footer in (base_footer, data05_footer):
            with self.subTest(footer=footer), tempfile.TemporaryDirectory() as tmp:
                tmp_path = Path(tmp)
                ic_path = tmp_path / "ic_standard_0038.txt"
                output_path = tmp_path / "brutus_standard_0038.txt"
                ic_path.write_text(
                    "1 1 1 1 1 1 1\n2 2 2 2 2 2 2\n3 3 3 3 3 3 3\n"
                )
                output_path.write_text(
                    "\n".join(
                        [
                            "0 3 0",
                            "1 1 1 1 1 1 1",
                            "2 2 2 2 2 2 2",
                            "3 3 3 3 3 3 3",
                            "10.0 3 1",
                            "1 1 1 1 1 1 1",
                            "2 2 2 2 2 2 2",
                            "3 3 3 3 3 3 3",
                            footer,
                        ]
                    )
                    + "\n"
                )

                result = self.runner.validate_output(output_path, ic_path)

                self.assertFalse(result.ok)
                self.assertTrue(any("dt" in error or "tol" in error or "Lw" in error for error in result.errors))

    def test_validated_staged_output_can_be_promoted_without_overwrite(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            staging = tmp_path / "staging"
            final = tmp_path / "final"
            staging.mkdir()
            final.mkdir()
            source = staging / "brutus_standard_0038.txt"
            source.write_text("output\n")

            promoted = self.runner.promote_outputs(["0038"], staging, final)

            self.assertEqual([final / "brutus_standard_0038.txt"], promoted)
            self.assertEqual("output\n", (final / "brutus_standard_0038.txt").read_text())

            with self.assertRaises(FileExistsError):
                self.runner.promote_outputs(["0038"], staging, final)

    def test_resume_skips_only_valid_staged_outputs(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            manifest_path = tmp_path / "run_manifest.json"
            manifest_path.write_text(
                json.dumps(
                    {
                        "0038": {"status": "success", "validation": {"ok": True}},
                        "0042": {"status": "failed", "validation": {"ok": False}},
                    }
                )
            )

            manifest = self.runner.load_manifest(manifest_path)

            self.assertTrue(self.runner.should_skip_for_resume("0038", manifest))
            self.assertFalse(self.runner.should_skip_for_resume("0042", manifest))
            self.assertFalse(self.runner.should_skip_for_resume("0049", manifest))

    def test_output_progress_tracks_last_snapshot_and_file_idle_time(self):
        with tempfile.TemporaryDirectory() as tmp:
            output_path = Path(tmp) / "brutus_standard_0038.txt"
            output_path.write_text(
                "\n".join(
                    [
                        "0 3 0",
                        "1 1 1 1 1 1 1",
                        "2 2 2 2 2 2 2",
                        "3 3 3 3 3 3 3",
                        "1.01 3 7.8",
                        "1 1 1 1 1 1 1",
                        "2 2 2 2 2 2 2",
                        "3 3 3 3 3 3 3",
                    ]
                )
                + "\n"
            )
            os.utime(output_path, (880.0, 880.0))

            progress = self.runner.read_output_progress(output_path, now=1000.0)

        self.assertEqual(2, progress.snapshot_count)
        self.assertAlmostEqual(1.01, progress.final_time)
        self.assertEqual(120.0, progress.idle_seconds)
        self.assertIsNone(self.runner.stall_reason(progress, stall_seconds=121))
        self.assertIn("no new timestep", self.runner.stall_reason(progress, stall_seconds=120))

    def test_run_one_marks_process_stalled_when_output_stops_advancing(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            ic_path = tmp_path / "ic_standard_9999.txt"
            output_path = tmp_path / "brutus_standard_9999.txt"
            fake_brutus = tmp_path / "fake_brutus.py"
            ic_text = "1 1 1 1 1 1 1\n2 2 2 2 2 2 2\n3 3 3 3 3 3 3\n"
            ic_path.write_text(ic_text)
            fake_brutus.write_text(
                textwrap.dedent(
                    """
                    import sys
                    import time

                    print("0 3 0", flush=True)
                    print("1 1 1 1 1 1 1", flush=True)
                    print("2 2 2 2 2 2 2", flush=True)
                    print("3 3 3 3 3 3 3", flush=True)
                    time.sleep(5)
                    """
                ).lstrip()
            )

            original_ic_path_for_id = self.runner.ic_path_for_id
            original_staged_output_path_for_id = self.runner.staged_output_path_for_id
            original_build_brutus_command = self.runner.build_brutus_command
            try:
                self.runner.ic_path_for_id = lambda id_str: ic_path
                self.runner.staged_output_path_for_id = lambda id_str: output_path
                self.runner.build_brutus_command = lambda brutus_bin, ic: [sys.executable, str(fake_brutus)]

                result = self.runner.run_one(
                    "9999",
                    timeout_seconds=30,
                    stall_seconds=0.2,
                    stall_check_seconds=0.05,
                    state=None,
                )
            finally:
                self.runner.ic_path_for_id = original_ic_path_for_id
                self.runner.staged_output_path_for_id = original_staged_output_path_for_id
                self.runner.build_brutus_command = original_build_brutus_command

        self.assertEqual("stalled", result["status"])
        self.assertIn("no new timestep", result["reason"])

    def test_main_returns_130_on_keyboard_interrupt(self):
        original_parse_missing_ids = self.runner.parse_missing_ids
        original_preflight = self.runner.preflight
        original_print_preflight = self.runner.print_preflight
        original_run_batch = self.runner.run_batch
        try:
            self.runner.parse_missing_ids = lambda: ["0038"]
            self.runner.preflight = lambda ids: []
            self.runner.print_preflight = lambda ids, args: None

            def raise_interrupt(ids, args):
                raise KeyboardInterrupt

            self.runner.run_batch = raise_interrupt

            stderr = io.StringIO()
            with redirect_stderr(stderr):
                self.assertEqual(130, self.runner.main([]))
            self.assertIn("Interrupted by user", stderr.getvalue())
        finally:
            self.runner.parse_missing_ids = original_parse_missing_ids
            self.runner.preflight = original_preflight
            self.runner.print_preflight = original_print_preflight
            self.runner.run_batch = original_run_batch


if __name__ == "__main__":
    unittest.main()
