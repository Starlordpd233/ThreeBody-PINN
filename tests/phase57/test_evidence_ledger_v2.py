"""Focused checks for Phase-57 process provenance and generation selection."""

from __future__ import annotations

import contextlib
import hashlib
import importlib.util
import io
import json
import shutil
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import torch
import yaml


ROOT = Path(__file__).resolve().parents[2]
VERIFIER = (
    ROOT
    / ".planning/phases/57-corrected-re-run-the-preserved-evaluation/evidence/verify_phase57_evidence.py"
)
SPEC = importlib.util.spec_from_file_location("phase57_evidence_verifier_v2", VERIFIER)
assert SPEC is not None and SPEC.loader is not None
verifier = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(verifier)


class GenerationSevenConfigTests(unittest.TestCase):
    def test_generation_seven_changes_only_the_run_identity(self) -> None:
        for suffix in ("smoke", "seed41", "seed42", "seed43"):
            with self.subTest(suffix=suffix):
                old = yaml.safe_load((ROOT / f"configs/stage0-v23g6-{suffix}.yaml").read_text())
                new = yaml.safe_load((ROOT / f"configs/stage0-v23g7-{suffix}.yaml").read_text())
                self.assertEqual(old["run"].pop("run_name"), f"stage0-v23g6-{suffix}")
                self.assertEqual(new["run"].pop("run_name"), f"stage0-v23g7-{suffix}")
                self.assertEqual(new, old)


class AdmissionConfigTests(unittest.TestCase):
    def setUp(self) -> None:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        (self.root / "configs").mkdir()
        for suffix in ("smoke", "seed41", "seed42", "seed43"):
            name = f"stage0-v23g7-{suffix}.yaml"
            shutil.copyfile(ROOT / "configs" / name, self.root / "configs" / name)
        patcher = mock.patch.object(verifier, "REPO_ROOT", self.root)
        patcher.start()
        self.addCleanup(patcher.stop)

    def test_admission_rejects_config_that_fails_strict_load(self) -> None:
        smoke = self.root / "configs/stage0-v23g7-smoke.yaml"
        smoke.write_text(smoke.read_text() + "\nunknown_top_level: true\n")
        with self.assertRaisesRegex(verifier.VerifyError, "strict-load"):
            verifier._assert_config_contract()

    def test_admission_rejects_unreachable_admitted_corpus(self) -> None:
        smoke = self.root / "configs/stage0-v23g7-smoke.yaml"
        smoke.write_text(
            smoke.read_text() + f"\n  root: {self.root / 'missing-corpus'}\n"
        )
        with self.assertRaisesRegex(verifier.VerifyError, "corpus"):
            verifier._assert_config_contract()


class BlockedStateContractTests(unittest.TestCase):
    def setUp(self) -> None:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        evidence = self.root / verifier.EVIDENCE_REL
        evidence.mkdir(parents=True)
        patcher = mock.patch.object(verifier, "REPO_ROOT", self.root)
        patcher.start()
        self.addCleanup(patcher.stop)

    def test_generation_one_blocked_state_is_verified_from_ledger_digest(self) -> None:
        historical = self.root / verifier.HISTORICAL_BLOCKED_STATE_REL
        historical.write_text('{"run_name":"stage0-v23-smoke"}\n')
        ledger = {
            "records": [{
                "band_generation": 1,
                "blocked_state_path": str(verifier.HISTORICAL_BLOCKED_STATE_REL),
                "blocked_state_sha256": verifier.sha256_file(historical),
            }]
        }
        verifier.assert_generation_one_blocked_state_retained(ledger)

    def test_current_blocked_state_reader_ignores_historical_singleton(self) -> None:
        (self.root / verifier.HISTORICAL_BLOCKED_STATE_REL).write_text("not-json")
        current = self.root / verifier.CURRENT_BLOCKED_STATE_REL
        current.write_text('{"band_generation":7,"run_name":"stage0-v23g7-smoke"}\n')
        self.assertEqual(verifier._blocked_state()["band_generation"], 7)

    def test_generation_four_blocked_state_is_verified_from_ledger_digest(self) -> None:
        historical = self.root / verifier.EVIDENCE_REL / "blocked-state-g4.json"
        source = self.root / "configs/stage0-v23g4-smoke.yaml"
        source.parent.mkdir(parents=True, exist_ok=True)
        source.write_text("run:\n  run_name: stage0-v23g4-smoke\n")
        artifact = self.root / "runs/stage0-v23g4-smoke"
        artifact.mkdir(parents=True)
        (artifact / "config.yaml").write_text("run:\n  run_name: stage0-v23g4-smoke\n")
        artifact_hashes = {"config.yaml": verifier.sha256_file(artifact / "config.yaml")}
        historical.write_text(json.dumps({
            "band_generation": 4,
            "run_name": "stage0-v23g4-smoke",
            "evaluation": "preserved-unspent",
            "terminal": False,
            "config": {"source_sha256": verifier.sha256_file(source)},
            "run_artifact_hashes": artifact_hashes,
        }))
        ledger = {
            "band_generations": [{"band_generation": 4, "status": "blocked"}],
            "records": [{
                "band_generation": 4,
                "run_name": "stage0-v23g4-smoke",
                "git_head": "a" * 40,
                "config_path": "configs/stage0-v23g4-smoke.yaml",
                "config_sha256": verifier.sha256_file(source),
                "artifact_dir": "runs/stage0-v23g4-smoke",
                "blocked_state_path": str(verifier.EVIDENCE_REL / "blocked-state-g4.json"),
                "blocked_state_sha256": verifier.sha256_file(historical),
                "artifact_hashes": artifact_hashes,
                "invocations": [{}],
            }],
        }
        with mock.patch.object(verifier, "_assert_invocations"):
            verifier.assert_generation_four_blocked_state_retained(ledger)
            (artifact / "config.yaml").write_text("tampered\n")
            with self.assertRaisesRegex(verifier.VerifyError, "retained artifact bytes"):
                verifier.assert_generation_four_blocked_state_retained(ledger)


class GenerationSixRetentionTests(unittest.TestCase):
    """GAP-57-12 R1: the retained generation-6 attempt re-derives from Git and disk."""

    @staticmethod
    def ledger_with(run_name: str, mutate) -> dict:
        ledger = verifier.load_ledger()
        for record in ledger["records"]:
            if record.get("run_name") == run_name:
                mutate(record)
        return ledger

    def test_committed_generation_six_attempt_rederives(self) -> None:
        verifier.assert_generation_six_retained(verifier.load_ledger())

    def test_rejects_changed_retained_bytes(self) -> None:
        real = verifier.sha256_file

        def drifted(path: Path) -> str:
            return "0" * 64 if str(path).endswith("stage0-v23g6-seed42/summary.md") else real(path)

        with mock.patch.object(verifier, "sha256_file", side_effect=drifted):
            with self.assertRaisesRegex(verifier.VerifyError, "bytes differ from manifest"):
                verifier.assert_generation_six_retained(verifier.load_ledger())

    def test_rejects_ledger_hash_drift(self) -> None:
        ledger = self.ledger_with(
            "stage0-v23g6-seed42",
            lambda record: record["artifact_hashes"].update({"status.json": "0" * 64}),
        )
        with self.assertRaisesRegex(verifier.VerifyError, "ledger hashes"):
            verifier.assert_generation_six_retained(ledger)

    def test_rejects_the_lost_process_rewritten_as_finished(self) -> None:
        ledger = self.ledger_with(
            "stage0-v23g6-seed42",
            lambda record: record["invocations"][0].update({"exit_code": 0, "disposition": "finished"}),
        )
        with self.assertRaisesRegex(verifier.VerifyError, "process-lost"):
            verifier.assert_generation_six_retained(ledger)


class GenerationSevenRetentionTests(unittest.TestCase):
    """GAP-57-13 A: the terminal generation-7 band re-derives from Git and disk."""

    @staticmethod
    def terminal() -> dict:
        return json.loads((ROOT / verifier.EVIDENCE_REL / "terminal-state.json").read_text())

    def test_committed_generation_seven_band_rederives(self) -> None:
        verifier.assert_generation_seven_retained(verifier.load_ledger(), self.terminal())

    def test_rejects_ledger_hash_drift(self) -> None:
        ledger = verifier.load_ledger()
        for record in ledger["records"]:
            if record.get("run_name") == "stage0-v23g7-smoke":
                record["artifact_hashes"]["status.json"] = "0" * 64
        with self.assertRaisesRegex(verifier.VerifyError, "ledger hashes"):
            verifier.assert_generation_seven_retained(ledger, self.terminal())

    def test_rejects_terminal_state_pointing_at_other_bytes(self) -> None:
        terminal = self.terminal()
        terminal["guard_trip"]["sha256"] = "0" * 64
        with self.assertRaisesRegex(verifier.VerifyError, "trip or checkpoint hashes"):
            verifier.assert_generation_seven_retained(verifier.load_ledger(), terminal)


class Seed42SetupTests(unittest.TestCase):
    def setUp(self) -> None:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        patcher = mock.patch.object(verifier, "REPO_ROOT", self.root)
        patcher.start()
        self.addCleanup(patcher.stop)
        self.smoke = self.root / "runs/stage0-v23g7-smoke"
        self.graded = self.root / "runs/stage0-v23g7-seed42"
        for run in (self.smoke, self.graded):
            run.mkdir(parents=True)
            (run / "splits.json").write_text('{"seed":42,"groups":[]}\n')
            (run / "training_metadata.json").write_text(
                json.dumps({"s_h": 22.321729071058996, "n_train": 1812})
            )
            (run / "status.json").write_text(json.dumps({
                "state": "finished" if run == self.smoke else "initializing",
                "run_name": run.name,
            }))
        (self.smoke / "summary.json").write_text(json.dumps({
            "disposition": "finished", "run_name": self.smoke.name,
        }))
        (self.graded / "preflight.json").write_text('{"preflight_status":"passed"}\n')

    def test_passes_only_actual_byte_and_scalar_equality(self) -> None:
        result = verifier._assert_seed42_setup(before_other_seeds=True)
        self.assertEqual(result["n_train"], 1812)
        self.assertEqual(result["s_h"], 22.321729071058996)
        self.assertEqual(result["splits_sha256"], verifier.sha256_file(self.smoke / "splits.json"))

    def test_rejects_same_parsed_split_with_different_bytes(self) -> None:
        (self.graded / "splits.json").write_text('{ "seed": 42, "groups": [] }\n')
        with self.assertRaisesRegex(verifier.VerifyError, "splits.json bytes differ"):
            verifier._assert_seed42_setup(before_other_seeds=True)

    def test_rejects_metadata_mismatch(self) -> None:
        for field, value in (("s_h", 23.0), ("n_train", 1813)):
            with self.subTest(field=field):
                metadata = {"s_h": 22.321729071058996, "n_train": 1812}
                metadata[field] = value
                (self.graded / "training_metadata.json").write_text(json.dumps(metadata))
                with self.assertRaisesRegex(verifier.VerifyError, field):
                    verifier._assert_seed42_setup(before_other_seeds=True)

    def test_rejects_missing_graded_setup(self) -> None:
        (self.graded / "training_metadata.json").unlink()
        with self.assertRaisesRegex(verifier.VerifyError, "graded seed-42 metadata"):
            verifier._assert_seed42_setup(before_other_seeds=True)

    def test_rejects_prior_launch_of_other_graded_seed(self) -> None:
        (self.root / "runs/stage0-v23g7-seed41").mkdir()
        with self.assertRaisesRegex(verifier.VerifyError, "before seeds 41 or 43"):
            verifier._assert_seed42_setup(before_other_seeds=True)

    def test_rejects_unpassed_preflight(self) -> None:
        (self.graded / "preflight.json").write_text('{"preflight_status":"failed"}\n')
        with self.assertRaisesRegex(verifier.VerifyError, "preflight has not passed"):
            verifier._assert_seed42_setup(before_other_seeds=True)


class InvocationEvidenceTests(unittest.TestCase):
    def setUp(self) -> None:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        patcher = mock.patch.object(verifier, "REPO_ROOT", self.root)
        patcher.start()
        self.addCleanup(patcher.stop)
        # These cases exercise the current run's process contract; historical
        # retention has its own focused tests.
        for name in (
            "assert_generation_one_blocked_state_retained",
            "assert_generation_three_blocked_state_retained",
            "assert_generation_four_blocked_state_retained",
            "assert_generation_five_retained",
            "assert_generation_six_retained",
        ):
            retention_patcher = mock.patch.object(verifier, name)
            retention_patcher.start()
            self.addCleanup(retention_patcher.stop)
        setup_patcher = mock.patch.object(verifier, "_assert_seed42_setup")
        setup_patcher.start()
        self.addCleanup(setup_patcher.stop)
        self.config_rel = "configs/stage0-v23g7-seed42.yaml"
        self.config = self.root / self.config_rel
        self.config.parent.mkdir(parents=True)
        self.config.write_text("run:\n  run_name: stage0-v23g7-seed42\n")
        self.config_sha = verifier.sha256_file(self.config)
        self.run_rel = "runs/stage0-v23g7-seed42"
        self.run = self.root / self.run_rel
        self.run.mkdir(parents=True)
        self.head = "a" * 40

    def invocation(self, ordinal: int, *, kind: str, command_suffix: str = "",
                   disposition: str = "finished", exit_code: int = 0) -> dict:
        start_minute = 0 if ordinal == 1 else 2
        end_minute = start_minute + 1
        return {
            "invocation_ordinal": ordinal,
            "launch_kind": kind,
            "command": (
                f"python -m pinn.train --config {self.config_rel} "
                f"--stage-0-only{command_suffix}"
            ),
            "process_pid": 1000 + ordinal,
            "start_utc": f"2026-09-27T12:{start_minute:02d}:00+00:00",
            "end_utc": f"2026-09-27T12:{end_minute:02d}:00+00:00",
            "wall_clock_secs": 60.0,
            "exit_code": exit_code,
            "git_head": self.head,
            "config_sha256": self.config_sha,
            "disposition": disposition,
            "boundary_checkpoint": None,
            "resume_checkpoint": None,
        }

    def record(self, invocations: list[dict]) -> dict:
        return {
            "run_name": self.run.name,
            "artifact_dir": self.run_rel,
            "config_path": self.config_rel,
            "config_sha256": self.config_sha,
            "git_head": self.head,
            "invocations": invocations,
        }

    def checkpoint(self, payload: dict) -> dict:
        path = self.run / "checkpoints" / "step-000031.pt"
        path.parent.mkdir(parents=True)
        torch.save(payload, path)
        return {
            "path": str(path.relative_to(self.root)),
            "sha256": verifier.sha256_file(path),
        }

    def launch_evidence(self, run_name: str, invocation: dict) -> None:
        """Write the launcher files one final-band invocation must be bound to."""
        directory = verifier.LAUNCH_ROOT_REL / run_name / f"invocation-{invocation['invocation_ordinal']}"
        launch_dir = self.root / directory
        launch_dir.mkdir(parents=True)
        documents = {
            "launch.json": {
                "mode": verifier.LAUNCH_MODE, "run_name": run_name,
                "invocation_ordinal": invocation["invocation_ordinal"],
                "launch_kind": invocation["launch_kind"],
                "command": invocation["command"], "git_head": invocation["git_head"],
            },
            "process.json": {
                "trainer_pid": invocation["process_pid"], "start_utc": invocation["start_utc"],
            },
            "exit.json": {
                "trainer_pid": invocation["process_pid"], "exit_code": invocation["exit_code"],
                "end_utc": invocation["end_utc"], "wall_clock_secs": invocation["wall_clock_secs"],
            },
        }
        for name, payload in documents.items():
            (launch_dir / name).write_text(json.dumps(payload))
        (launch_dir / "output.log").write_text("trainer output\n")
        invocation["launch"] = {
            "mode": verifier.LAUNCH_MODE,
            "directory": str(directory),
            "files": {
                name: verifier.sha256_file(launch_dir / name)
                for name in ("launch.json", "process.json", "output.log", "exit.json")
            },
        }

    def final_record(self, invocation: dict) -> dict:
        return dict(self.record([invocation]), band_generation=verifier.FINAL_GENERATION)

    def test_final_band_invocation_requires_detached_launch_evidence(self) -> None:
        fresh = self.invocation(1, kind="fresh")
        with self.assertRaisesRegex(verifier.VerifyError, "detached session"):
            verifier._assert_invocations(self.final_record(fresh), self.head)
        self.launch_evidence(self.run.name, fresh)
        self.assertIs(verifier._assert_invocations(self.final_record(fresh), self.head), fresh)

    def test_launch_evidence_rejects_edited_output_and_mismatched_ledger_fields(self) -> None:
        fresh = self.invocation(1, kind="fresh")
        self.launch_evidence(self.run.name, fresh)
        log = self.root / fresh["launch"]["directory"] / "output.log"
        log.write_text("edited\n")
        with self.assertRaisesRegex(verifier.VerifyError, "launch file bytes differ"):
            verifier._assert_invocations(self.final_record(fresh), self.head)
        log.write_text("trainer output\n")
        for changed, message in (
            (dict(fresh, exit_code=1), "exit record differs"),
            (dict(fresh, command=fresh["command"] + " "), "identity or command"),
            (dict(fresh, process_pid=4242), "PID or start time"),
        ):
            with self.subTest(message=message), self.assertRaisesRegex(verifier.VerifyError, message):
                verifier._assert_invocations(self.final_record(changed), self.head)

    def test_fresh_finished_invocation(self) -> None:
        fresh = self.invocation(1, kind="fresh")
        self.assertIs(
            verifier._assert_invocations(self.record([fresh]), self.head),
            fresh,
        )

    def test_verified_boundary_allows_same_head_resume(self) -> None:
        boundary = self.checkpoint({
            "invariant_b_state": {"front_high_water": 0, "last_advance_step": 0}
        })
        fresh = self.invocation(
            1, kind="fresh", disposition="interrupted", exit_code=130
        )
        fresh["boundary_checkpoint"] = boundary
        resumed = self.invocation(2, kind="resume", command_suffix=" --resume latest")
        resumed["resume_checkpoint"] = boundary
        self.assertIs(
            verifier._assert_invocations(self.record([fresh, resumed]), self.head),
            resumed,
        )

    def test_resume_rejects_wrong_checkpoint_hash(self) -> None:
        boundary = self.checkpoint({
            "invariant_b_state": {"front_high_water": 0, "last_advance_step": 0}
        })
        boundary["sha256"] = "b" * 64
        fresh = self.invocation(
            1, kind="fresh", disposition="interrupted", exit_code=130
        )
        fresh["boundary_checkpoint"] = boundary
        resumed = self.invocation(2, kind="resume", command_suffix=" --resume latest")
        resumed["resume_checkpoint"] = boundary
        with self.assertRaisesRegex(verifier.VerifyError, "bytes differ"):
            verifier._assert_invocations(self.record([fresh, resumed]), self.head)

    def test_resume_rejects_checkpoint_without_invariant_state(self) -> None:
        boundary = self.checkpoint({"model": {}})
        fresh = self.invocation(
            1, kind="fresh", disposition="interrupted", exit_code=130
        )
        fresh["boundary_checkpoint"] = boundary
        resumed = self.invocation(2, kind="resume", command_suffix=" --resume latest")
        resumed["resume_checkpoint"] = boundary
        with self.assertRaisesRegex(verifier.VerifyError, "invariant_b_state"):
            verifier._assert_invocations(self.record([fresh, resumed]), self.head)

    def test_resume_rejects_changed_head_or_config(self) -> None:
        boundary = self.checkpoint({
            "invariant_b_state": {"front_high_water": 0, "last_advance_step": 0}
        })
        fresh = self.invocation(
            1, kind="fresh", disposition="interrupted", exit_code=130
        )
        fresh["boundary_checkpoint"] = boundary
        resumed = self.invocation(2, kind="resume", command_suffix=" --resume latest")
        resumed["resume_checkpoint"] = boundary
        for field, altered in (("git_head", "b" * 40), ("config_sha256", "b" * 64)):
            with self.subTest(field=field):
                changed = dict(resumed, **{field: altered})
                with self.assertRaisesRegex(verifier.VerifyError, "HEAD or config"):
                    verifier._assert_invocations(
                        self.record([fresh, changed]), self.head
                    )

    def test_resume_rejects_missing_invocation_or_boundary(self) -> None:
        fresh = self.invocation(1, kind="fresh", command_suffix=" --resume latest")
        with self.assertRaisesRegex(verifier.VerifyError, "must not resume"):
            verifier._assert_invocations(self.record([fresh]), self.head)
        fresh = self.invocation(
            1, kind="fresh", disposition="interrupted", exit_code=130
        )
        resumed = self.invocation(2, kind="resume", command_suffix=" --resume latest")
        with self.assertRaisesRegex(verifier.VerifyError, "boundary checkpoint"):
            verifier._assert_invocations(self.record([fresh, resumed]), self.head)

    def test_old_blocked_state_does_not_block_new_terminal(self) -> None:
        terminal = {
            "status": "terminal",
            "authorized_terminal_reason": "invariant_b_halt_no_advance",
            "evaluation": "preserved-unspent",
        }
        with (
            mock.patch.object(verifier, "_gate_chain"),
            mock.patch.object(verifier, "assert_generation_two_retained"),
            mock.patch.object(verifier, "load_ledger", return_value={
                "records": [], "band_generations": [], "final_band_generation": None
            }),
            mock.patch.object(verifier, "_blocked_state", return_value=None),
            mock.patch.object(verifier, "_terminal_state", return_value=terminal),
            mock.patch.object(verifier, "_target_runs", return_value=()),
            contextlib.redirect_stdout(io.StringIO()) as output,
        ):
            verifier.cmd_run_window()
        self.assertIn("RUN-WINDOW-TERMINAL-OK", output.getvalue())

    def test_complete_generation_seven_band_accepts_verified_resume(self) -> None:
        boundary = self.checkpoint({
            "invariant_b_state": {"front_high_water": 0, "last_advance_step": 0}
        })
        first = self.invocation(
            1, kind="fresh", disposition="interrupted", exit_code=130
        )
        first["start_utc"] = "2026-09-27T12:02:00+00:00"
        first["end_utc"] = "2026-09-27T12:03:00+00:00"
        first["boundary_checkpoint"] = boundary
        resumed = self.invocation(2, kind="resume", command_suffix=" --resume latest")
        resumed["start_utc"] = "2026-09-27T12:04:00+00:00"
        resumed["end_utc"] = "2026-09-27T12:05:00+00:00"
        resumed["resume_checkpoint"] = boundary
        seed42 = self.record([first, resumed])
        seed42.update({
            "band_generation": 7, "seed": 42, "in_final_band": True,
            "final_process_disposition": "finished", "ledger_disposition": "finished",
        })
        self.launch_evidence(seed42["run_name"], first)
        self.launch_evidence(seed42["run_name"], resumed)
        records = [seed42]
        for name, seed, in_band in (
            ("smoke", 42, False), ("seed41", 41, True), ("seed43", 43, True)
        ):
            run_name = f"stage0-v23g7-{name}"
            config_rel = f"configs/{run_name}.yaml"
            config = self.root / config_rel
            config.write_text(f"run:\n  run_name: {run_name}\n")
            run_rel = f"runs/{run_name}"
            (self.root / run_rel).mkdir()
            config_sha = verifier.sha256_file(config)
            invocation = self.invocation(1, kind="fresh")
            minute = {"smoke": 0, "seed41": 6, "seed43": 8}[name]
            invocation["start_utc"] = f"2026-09-27T12:{minute:02d}:00+00:00"
            invocation["end_utc"] = f"2026-09-27T12:{minute + 1:02d}:00+00:00"
            invocation["command"] = (
                f"python -m pinn.train --config {config_rel} --stage-0-only"
            )
            invocation["config_sha256"] = config_sha
            self.launch_evidence(run_name, invocation)
            records.append({
                "band_generation": 7, "run_name": run_name, "seed": seed,
                "in_final_band": in_band, "git_head": self.head,
                "config_path": config_rel, "config_sha256": config_sha,
                "artifact_dir": run_rel, "invocations": [invocation],
                "final_process_disposition": "finished",
                "ledger_disposition": "finished",
            })
        ledger = {
            "records": records,
            "band_generations": [{
                "band_generation": 7, "git_head": self.head,
                "launch_order": list(verifier.FINAL_LAUNCH_ORDER),
            }],
            "final_band_generation": 7,
        }
        with (
            mock.patch.object(verifier, "_gate_chain"),
            mock.patch.object(verifier, "assert_generation_two_retained"),
            mock.patch.object(verifier, "load_ledger", return_value=ledger),
            mock.patch.object(verifier, "_blocked_state", return_value=None),
            mock.patch.object(verifier, "_terminal_state", return_value=None),
            contextlib.redirect_stdout(io.StringIO()) as output,
        ):
            verifier.cmd_run_window()
        self.assertIn("RUN-WINDOW-OK", output.getvalue())

    def test_band_rejects_seed41_before_seed42(self) -> None:
        records = [{
            "run_name": name,
            "invocations": [{
                "start_utc": f"2026-09-27T12:{ordinal * 2:02d}:00+00:00",
                "end_utc": f"2026-09-27T12:{ordinal * 2 + 1:02d}:00+00:00",
            }],
        } for ordinal, name in enumerate((
            "stage0-v23g7-smoke", "stage0-v23g7-seed41",
            "stage0-v23g7-seed42", "stage0-v23g7-seed43",
        ))]
        with self.assertRaisesRegex(verifier.VerifyError, "timestamps violate"):
            verifier._assert_launch_order(
                {"launch_order": list(verifier.FINAL_LAUNCH_ORDER)}, records
            )

    def test_current_generation_blocked_state_still_refuses_closeout(self) -> None:
        with (
            mock.patch.object(verifier, "_gate_chain"),
            mock.patch.object(verifier, "assert_generation_two_retained"),
            mock.patch.object(verifier, "load_ledger", return_value={
                "records": [], "band_generations": [], "final_band_generation": None
            }),
            mock.patch.object(verifier, "_blocked_state", return_value={
                "band_generation": 7,
                "run_name": "stage0-v23g7-smoke",
                "evaluation": "preserved-unspent",
                "terminal": False,
            }),
        ):
            with self.assertRaisesRegex(verifier.VerifyError, "blocked-state"):
                verifier.cmd_run_window()

    def test_band_rejects_seed_record_with_wrong_run_name(self) -> None:
        head = "a" * 40
        records = [
            {
                "band_generation": 7,
                "run_name": f"stage0-v23g7-{name}",
                "seed": seed,
                "in_final_band": in_band,
                "git_head": head,
                "final_process_disposition": "finished",
                "ledger_disposition": "finished",
            }
            for name, seed, in_band in (
                ("smoke", 42, False),
                ("seed41", 41, True),
                ("seed42", 42, True),
                ("seed99", 43, True),
            )
        ]
        ledger = {
            "records": records,
            "band_generations": [{"band_generation": 7, "git_head": head}],
            "final_band_generation": 7,
        }
        with (
            mock.patch.object(verifier, "_gate_chain"),
            mock.patch.object(verifier, "assert_generation_two_retained"),
            mock.patch.object(verifier, "load_ledger", return_value=ledger),
            mock.patch.object(verifier, "_assert_invocations", return_value={
                "disposition": "finished", "exit_code": 0
            }),
            mock.patch.object(verifier, "_blocked_state", return_value=None),
            mock.patch.object(verifier, "_terminal_state", return_value=None),
            mock.patch.object(verifier, "_target_runs", return_value=()),
            contextlib.redirect_stdout(io.StringIO()),
        ):
            with self.assertRaisesRegex(verifier.VerifyError, "run names"):
                verifier.cmd_run_window()

    def test_candidate_accepts_generation_seven_name(self) -> None:
        best = self.run / "checkpoints" / "best.pt"
        best.parent.mkdir(parents=True)
        best.write_bytes(b"model")
        facts = {
            key: True for key in verifier.REQUIRED_STRUCTURAL_FACTS
        }
        facts["eligible"] = True
        receipt = {
            "schema": "phase57-candidate-receipt/v1",
            "facts": {
                "41": {**facts, "eligible": False},
                "42": facts,
                "43": {**facts, "eligible": False},
            },
            "run_name": self.run.name,
            "seed": 42,
            "candidate_best_path": str(best.relative_to(self.root)),
            "candidate_best_sha256": hashlib.sha256(b"model").hexdigest(),
        }
        receipt_path = self.root / verifier.EVIDENCE_REL / "candidate-receipt.json"
        receipt_path.parent.mkdir(parents=True)
        receipt_path.write_text(json.dumps(receipt))
        with (
            mock.patch.object(verifier, "cmd_run_window"),
            mock.patch.object(verifier, "_terminal_state", return_value=None),
            contextlib.redirect_stdout(io.StringIO()) as output,
        ):
            verifier.cmd_candidate()
        self.assertIn("CANDIDATE-OK", output.getvalue())


if __name__ == "__main__":
    unittest.main()
