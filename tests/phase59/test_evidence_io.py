"""Phase 59 evidence writer: canonical JSON, redaction, freeze guard, launch lock."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path

import numpy as np

from pinn.data.types import PhysicalKey, RecordKey


ROOT = Path(__file__).resolve().parents[2]


def _io():
    try:
        import pinn.verification.evidence_io as module
    except ImportError as exc:
        if getattr(exc, "name", None) == "pinn.verification.evidence_io":
            return None
        raise
    return module


def _git(root: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    proc = subprocess.run(
        ["git", *args],
        cwd=root,
        capture_output=True,
        text=True,
        check=False,
    )
    if check and proc.returncode != 0:
        raise AssertionError(f"git {args[0]} failed: {proc.stderr}")
    return proc


def _init_repo(root: Path) -> None:
    _git(root, "init")
    _git(root, "config", "user.email", "phase59@example.com")
    _git(root, "config", "user.name", "phase59")


class CanonicalJsonTests(unittest.TestCase):
    def test_canonical_json_uses_sorted_keys_and_sentinels(self) -> None:
        module = _io()
        self.assertIsNotNone(module)
        payload = {"b": float("nan"), "a": [1.0, float("inf")]}
        expected = b'{\n  "a": [\n    1.0,\n    "Infinity"\n  ],\n  "b": "NaN"\n}\n'
        self.assertEqual(module.canonical_json_bytes(payload), expected)

    def test_numpy_values_and_record_keys_become_plain_json(self) -> None:
        module = _io()
        self.assertIsNotNone(module)
        key = RecordKey("hierarchical", "gold", 3)
        physical = PhysicalKey("standard", 4)
        payload = {
            "key": key,
            "physical": physical,
            "row": np.array([1.0, np.inf]),
            "flag": np.bool_(True),
            "count": np.int64(2),
        }
        parsed = json.loads(module.canonical_json_bytes(payload))
        self.assertEqual(parsed["key"], "hierarchical/gold/3")
        self.assertEqual(parsed["physical"], "standard/4")
        self.assertEqual(parsed["row"], [1.0, "Infinity"])
        self.assertIs(parsed["flag"], True)
        self.assertEqual(parsed["count"], 2)
        self.assertEqual(module.record_key_str(key), "hierarchical/gold/3")
        self.assertEqual(module.record_key_str(physical), "standard/4")


class RedactionTests(unittest.TestCase):
    def test_write_json_refuses_home_and_data_root(self) -> None:
        module = _io()
        self.assertIsNotNone(module)
        from pinn.data.adapter import EvidenceRedactionError

        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            target = root / "out.json"
            home = str(Path.home())
            with self.assertRaises(EvidenceRedactionError):
                module.write_json(target, {"path": home})
            data_root = root / "corpus"
            data_root.mkdir()
            with self.assertRaises(EvidenceRedactionError):
                module.write_json(
                    target,
                    {"path": str(data_root.resolve())},
                    data_root=data_root,
                )
            self.assertFalse(target.exists())


class RootGuardTests(unittest.TestCase):
    def test_reject_evidence_root_refuses_simulation_data_and_data_root(self) -> None:
        module = _io()
        self.assertIsNotNone(module)
        dataset = ROOT / "simulation_data" / "phase59-evidence-guard"
        data_root = Path(tempfile.mkdtemp())
        self.addCleanup(lambda: __import__("shutil").rmtree(data_root, ignore_errors=True))
        with self.assertRaises(ValueError):
            module.reject_evidence_root(dataset)
        with self.assertRaises(ValueError):
            module.reject_evidence_root(data_root / "nested", data_root=data_root)
        main_sim = data_root / "simulation_data"
        main_sim.mkdir()
        corpus = main_sim / "Data"
        corpus.mkdir()
        with self.assertRaises(ValueError):
            module.reject_evidence_root(main_sim / "other.txt", data_root=corpus)


class AtomicWriteTests(unittest.TestCase):
    def test_write_json_is_atomic_and_returns_sha256(self) -> None:
        module = _io()
        self.assertIsNotNone(module)
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / "area" / "result.json"
            digest = module.write_json(target, {"b": 1, "a": [1.0]})
            raw = target.read_bytes()
            self.assertEqual(digest, hashlib.sha256(raw).hexdigest())
            self.assertEqual(json.loads(raw), {"a": [1.0], "b": 1})
            self.assertEqual(list(Path(temporary).rglob("*.tmp.*")), [])


class ManifestTests(unittest.TestCase):
    def test_area_manifest_hashes_regular_files_and_skips_logs(self) -> None:
        module = _io()
        self.assertIsNotNone(module)
        with tempfile.TemporaryDirectory() as temporary:
            area = Path(temporary) / "census"
            area.mkdir()
            (area / "census.json").write_text('{"a": 1}\n', encoding="utf-8")
            (area / "MANIFEST.json").write_text("{}\n", encoding="utf-8")
            cache = area / "__pycache__"
            cache.mkdir()
            (cache / "x.pyc").write_bytes(b"pyc")
            logs = area / "logs"
            logs.mkdir()
            (logs / "step.log").write_text("log\n", encoding="utf-8")
            manifest = module.area_manifest(area)
            self.assertEqual(manifest["schema"], "phase59-area-manifest/v1")
            self.assertEqual(manifest["area"], "census")
            self.assertEqual(set(manifest["files"]), {"census.json"})
            entry = manifest["files"]["census.json"]
            raw = (area / "census.json").read_bytes()
            self.assertEqual(entry["size_bytes"], len(raw))
            self.assertEqual(entry["sha256"], hashlib.sha256(raw).hexdigest())
            written = module.write_area_manifest(area)
            self.assertEqual(written["files"], manifest["files"])
            self.assertTrue((area / "MANIFEST.json").is_file())


class CommandRedactionTests(unittest.TestCase):
    def test_redacted_command_replaces_data_root_and_home(self) -> None:
        module = _io()
        self.assertIsNotNone(module)
        data_root = Path("/Users/me/simulation_data/Data")
        rendered = module.redacted_command(
            ["python", "-m", "x", "--data-root", str(data_root)],
            data_root=data_root,
        )
        self.assertIn("<DATA_ROOT>", rendered)
        self.assertNotIn("/Users/", rendered)
        home = str(Path.home())
        rendered_home = module.redacted_command(
            ["python", str(Path.home() / "notes.txt")],
            data_root=None,
        )
        self.assertNotIn(home, rendered_home)
        self.assertIn("~", rendered_home)


class _FreezeFixture(unittest.TestCase):
    def setUp(self) -> None:
        module = _io()
        self.module = module
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        if module is None:
            return
        _init_repo(self.root)
        self._write_sources()
        self.sources = _git(self.root, "rev-parse", "HEAD").stdout.strip()
        self._write_freeze(self.sources)
        self.freeze = _git(self.root, "rev-parse", "HEAD").stdout.strip()

    def _write_sources(self) -> None:
        scorecard = ROOT / "pinn/verification/artifacts/feasibility_scorecard_v1.json"
        module_path = ROOT / "pinn/verification/feasibility_scorecard.py"
        for source, relative in (
            (scorecard, "pinn/verification/artifacts/feasibility_scorecard_v1.json"),
            (module_path, "pinn/verification/feasibility_scorecard.py"),
        ):
            dest = self.root / relative
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(source.read_bytes())
        plain = self.root / ".planning/phases/59-read-only-baseline-scorecard/59-SCORECARD.md"
        plain.parent.mkdir(parents=True, exist_ok=True)
        plain.write_text("plain scorecard\n", encoding="utf-8")
        for name in ("59-CONTEXT.md", "59-GAPS.md", "59-RESEARCH.md", "59-VALIDATION.md"):
            path = self.root / ".planning/phases/59-read-only-baseline-scorecard" / name
            path.write_text(f"{name} stand-in\n", encoding="utf-8")
        _git(self.root, "add", "-A")
        _git(self.root, "commit", "-m", "sources")

    def _write_freeze(self, head: str) -> None:
        phase = self.root / ".planning/phases/59-read-only-baseline-scorecard"
        evidence = phase / "evidence"
        evidence.mkdir(parents=True, exist_ok=True)
        paths = {
            "scorecard_path": "pinn/verification/artifacts/feasibility_scorecard_v1.json",
            "scorecard_module_path": "pinn/verification/feasibility_scorecard.py",
            "plain_doc_path": ".planning/phases/59-read-only-baseline-scorecard/59-SCORECARD.md",
        }
        record = {
            "schema": "phase59-scorecard-freeze/v1",
            "scorecard_schema_version": "phase59-feasibility-scorecard/v1",
            "decisions_frozen": ["D-11"],
            "note": "test freeze",
            "phase_start_head": head,
            "head_at_freeze": head,
        }
        for key, relative in paths.items():
            raw = (self.root / relative).read_bytes()
            prefix = key.removesuffix("_path")
            record[key] = relative
            record[f"{prefix}_sha256"] = hashlib.sha256(raw).hexdigest()
            record[f"{prefix}_size_bytes"] = len(raw)
        record["decision_sources"] = self._pins(head)
        self.assertEqual(len(record), 16)
        (evidence / "scorecard-freeze.json").write_text(
            json.dumps(record, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        _git(self.root, "add", "-A")
        _git(self.root, "commit", "-m", "freeze")

    def _pins(self, commit: str) -> dict:
        modes = {
            "59-CONTEXT.md": "unchanged",
            "59-GAPS.md": "ancestor_state",
            "59-RESEARCH.md": "unchanged",
            "59-VALIDATION.md": "ancestor_state",
        }
        pins = {}
        for name, mode in modes.items():
            relative = f".planning/phases/59-read-only-baseline-scorecard/{name}"
            blob = _git(self.root, "rev-parse", f"{commit}:{relative}").stdout.strip()
            raw = subprocess.check_output(["git", "show", f"{commit}:{relative}"], cwd=self.root)
            last = _git(
                self.root, "log", "-1", "--format=%H", commit, "--", relative
            ).stdout.strip()
            pins[relative] = {
                "git_blob": blob,
                "sha256": hashlib.sha256(raw).hexdigest(),
                "last_commit": last,
                "verify": mode,
            }
        return pins


class FreezeGuardTests(_FreezeFixture):
    def test_require_frozen_scorecard_returns_the_freeze_commit(self) -> None:
        self.assertIsNotNone(self.module)
        found = self.module.require_frozen_scorecard(repo_root=self.root)
        self.assertEqual(found["freeze_commit"], self.freeze)
        self.assertEqual(found["head"], self.freeze)

    def test_missing_freeze_record_raises(self) -> None:
        self.assertIsNotNone(self.module)
        path = (
            self.root
            / ".planning/phases/59-read-only-baseline-scorecard/evidence/scorecard-freeze.json"
        )
        path.unlink()
        with self.assertRaises(self.module.FreezeNotEstablished):
            self.module.require_frozen_scorecard(repo_root=self.root)

    def test_edited_frozen_bytes_raise(self) -> None:
        self.assertIsNotNone(self.module)
        scorecard = self.root / "pinn/verification/artifacts/feasibility_scorecard_v1.json"
        scorecard.write_bytes(scorecard.read_bytes() + b" ")
        _git(self.root, "add", "-A")
        _git(self.root, "commit", "-m", "edit scorecard")
        with self.assertRaises(self.module.FreezeNotEstablished):
            self.module.require_frozen_scorecard(repo_root=self.root)

    def test_dirty_scorecard_raises(self) -> None:
        self.assertIsNotNone(self.module)
        scorecard = self.root / "pinn/verification/artifacts/feasibility_scorecard_v1.json"
        scorecard.write_bytes(scorecard.read_bytes() + b" ")
        with self.assertRaises(self.module.FreezeNotEstablished) as caught:
            self.module.require_frozen_scorecard(repo_root=self.root)
        self.assertIn("dirty", str(caught.exception))

    def test_decision_source_pin_failures_raise(self) -> None:
        self.assertIsNotNone(self.module)
        path = (
            self.root
            / ".planning/phases/59-read-only-baseline-scorecard/evidence/scorecard-freeze.json"
        )
        record = json.loads(path.read_text(encoding="utf-8"))
        record.pop("decision_sources")
        path.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        _git(self.root, "add", "-A")
        _git(self.root, "commit", "-m", "drop pins")
        with self.assertRaises(self.module.FreezeNotEstablished):
            self.module.require_frozen_scorecard(repo_root=self.root)

    def test_context_edit_after_freeze_raises_and_gaps_edit_does_not(self) -> None:
        self.assertIsNotNone(self.module)
        phase = self.root / ".planning/phases/59-read-only-baseline-scorecard"
        gaps = phase / "59-GAPS.md"
        gaps.write_text(gaps.read_text(encoding="utf-8") + "new gap\n", encoding="utf-8")
        _git(self.root, "add", "-A")
        _git(self.root, "commit", "-m", "gaps")
        self.module.require_frozen_scorecard(repo_root=self.root)
        context = phase / "59-CONTEXT.md"
        context.write_text(context.read_text(encoding="utf-8") + "edit\n", encoding="utf-8")
        _git(self.root, "add", "-A")
        _git(self.root, "commit", "-m", "context")
        with self.assertRaises(self.module.FreezeNotEstablished):
            self.module.require_frozen_scorecard(repo_root=self.root)


class ModuleHashTests(unittest.TestCase):
    def test_module_hashes_pins_current_bytes(self) -> None:
        module = _io()
        self.assertIsNotNone(module)
        relative = "pinn/verification/evidence_io.py"
        digest = hashlib.sha256((ROOT / relative).read_bytes()).hexdigest()
        self.assertEqual(module.module_hashes([relative]), {relative: digest})


class MemoryPreflightTests(unittest.TestCase):
    SAMPLE = textwrap.dedent(
        """\
        Mach Virtual Memory Statistics: (page size of 16384 bytes)
        Pages free:                               10.
        Pages inactive:                           20.
        Pages speculative:                        30.
        """
    )

    def test_available_memory_parses_vm_stat_sample(self) -> None:
        module = _io()
        self.assertIsNotNone(module)
        self.assertEqual(module.available_memory_bytes(self.SAMPLE), (10 + 20 + 30) * 16384)

    def test_memory_preflight_raises_below_the_requirement(self) -> None:
        module = _io()
        self.assertIsNotNone(module)
        available = (10 + 20 + 30) * 16384
        found = module.memory_preflight(available, sample=self.SAMPLE)
        self.assertEqual(found["source"], "vm_stat")
        self.assertEqual(found["available_bytes"], available)
        with self.assertRaises(module.MemoryPreflightError):
            module.memory_preflight(available + 1, sample=self.SAMPLE)


class CompletionMarkerTests(unittest.TestCase):
    def test_marker_matches_until_a_result_byte_changes(self) -> None:
        module = _io()
        self.assertIsNotNone(module)
        with tempfile.TemporaryDirectory() as temporary:
            area = Path(temporary) / "survey"
            area.mkdir()
            result = area / "survey.json"
            result.write_text('{"ok": true}\n', encoding="utf-8")
            module.write_completion_marker(
                area,
                "survey",
                command="python -m survey",
                utc_started="2026-10-14T00:00:00+00:00",
                utc_finished="2026-10-14T00:00:01+00:00",
                elapsed_seconds=1.0,
                result_paths=[result],
                preflight={
                    "available_bytes": 10,
                    "required_bytes": 1,
                    "source": "vm_stat",
                },
            )
            marker = json.loads((area / "survey.done.json").read_text(encoding="utf-8"))
            self.assertEqual(marker["schema"], "phase59-completion-marker/v1")
            self.assertEqual(marker["status"], "complete")
            self.assertTrue(module.completion_marker_ok(area, "survey"))
            result.write_text('{"ok": false}\n', encoding="utf-8")
            self.assertFalse(module.completion_marker_ok(area, "survey"))


class LaunchLockTests(unittest.TestCase):
    def test_one_launch_at_a_time_and_gitignore(self) -> None:
        module = _io()
        self.assertIsNotNone(module)
        self.assertTrue(str(module.LAUNCH_LOCK_REL).endswith(".log"))
        self.assertTrue(str(module.LAUNCH_FAILURES_REL).endswith(".log"))
        for relative in (module.LAUNCH_LOCK_REL, module.LAUNCH_FAILURES_REL):
            proc = subprocess.run(
                ["git", "check-ignore", "-q", "--", str(relative)],
                cwd=ROOT,
                check=False,
            )
            self.assertEqual(proc.returncode, 0, relative)
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            command = ["python", "-m", "survey"]
            run_id = module.begin_long_step(
                "survey", "survey", command=command, evidence_root=root
            )
            lock = root / "logs" / "launch.lock.log"
            self.assertTrue(lock.is_file())
            with self.assertRaises(module.LaunchRefused) as caught:
                module.begin_long_step(
                    "diag07", "jx02_jx05", command=command, evidence_root=root
                )
            message = str(caught.exception)
            self.assertIn("survey/survey", message)
            self.assertIn(run_id, message)
            self.assertIn(str(os.getpid()), message)
            self.assertIn("alive true", message)
            module.end_long_step(run_id, evidence_root=root)
            self.assertFalse(lock.exists())
            again = module.begin_long_step(
                "survey", "survey", command=command, evidence_root=root
            )
            with self.assertRaises(module.LaunchRefused):
                module.end_long_step(run_id, evidence_root=root)
            module.record_long_step_failure(
                "halted", run_id=again, evidence_root=root
            )
            failure = (root / "logs" / "launch-failures.log").read_text(encoding="utf-8")
            line = json.loads(failure.strip().splitlines()[-1])
            self.assertEqual(line["schema"], "phase59-launch-failure/v1")
            self.assertEqual(line["reason"], "halted")
            self.assertFalse(lock.exists())

    def test_stale_lock_recovery_refuses_a_live_foreign_pid(self) -> None:
        module = _io()
        self.assertIsNotNone(module)
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            logs = root / "logs"
            logs.mkdir()
            holder = subprocess.Popen(
                [sys.executable, "-c", "import time; time.sleep(30)"]
            )
            self.addCleanup(lambda: holder.poll() is not None or holder.kill())
            payload = {
                "schema": "phase59-launch-lock/v1",
                "area": "diag07",
                "step": "jx01",
                "run_id": "foreign",
                "pid": holder.pid,
                "command": "python -m diag07",
                "utc_started": "2026-10-14T00:00:00+00:00",
            }
            (logs / "launch.lock.log").write_text(
                json.dumps(payload) + "\n", encoding="utf-8"
            )
            with self.assertRaises(module.LaunchRefused):
                module.record_long_step_failure("recover", evidence_root=root)
            self.assertTrue((logs / "launch.lock.log").is_file())
            holder.kill()
            holder.wait(timeout=5)
            finished = subprocess.Popen([sys.executable, "-c", "import sys"])
            finished.wait(timeout=5)
            payload["pid"] = finished.pid
            payload["run_id"] = "finished"
            (logs / "launch.lock.log").write_text(
                json.dumps(payload) + "\n", encoding="utf-8"
            )
            module.record_long_step_failure("stale", evidence_root=root)
            self.assertFalse((logs / "launch.lock.log").exists())
            text = (logs / "launch-failures.log").read_text(encoding="utf-8")
            self.assertEqual(json.loads(text.strip().splitlines()[-1])["reason"], "stale")


class RuntimeGateTests(unittest.TestCase):
    def test_runtime_gate_budget_boundary(self) -> None:
        module = _io()
        self.assertIsNotNone(module)
        for elapsed in (599.0, 600.0):
            with self.subTest(elapsed=elapsed):
                with _stderr() as err:
                    code = module.runtime_gate(elapsed, label="CENSUS")
                self.assertEqual(code, 0)
                self.assertIn("WALL-SECONDS", err.getvalue())
                self.assertIn("budget 600", err.getvalue())
        with _stderr() as err:
            code = module.runtime_gate(600.01, label="CENSUS")
        self.assertEqual(code, 5)
        self.assertIn("CENSUS-RUNTIME-OVER-BUDGET", err.getvalue())


class _stderr:
    def __enter__(self):
        import io
        from contextlib import redirect_stderr

        self.buffer = io.StringIO()
        self._redirect = redirect_stderr(self.buffer)
        self._redirect.__enter__()
        return self.buffer

    def __exit__(self, exc_type, exc, tb):
        return self._redirect.__exit__(exc_type, exc, tb)


if __name__ == "__main__":
    unittest.main()
