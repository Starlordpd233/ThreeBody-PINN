"""Phase 59 DIAG-07 driver tests. The driver is loaded by path."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import subprocess
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path
from unittest import mock

import torch


ROOT = Path(__file__).resolve().parents[2]
COMMON = (
    ROOT
    / ".planning/phases/59-read-only-baseline-scorecard/evidence/diag07/diag07_common.py"
)
GEN7 = "629b1a6ca4462915b6340a59b8d4e3ad8df75d8b"
SEED42 = "stage0-v23g7-seed42"
_MODULE = None


def load_common():
    """Load the driver library by path under a stable test name."""
    global _MODULE
    if _MODULE is not None:
        return _MODULE
    spec = importlib.util.spec_from_file_location("phase59_diag07_common", COMMON)
    if spec is None or spec.loader is None:
        raise AssertionError(f"cannot load {COMMON}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    _MODULE = module
    return module


def _require_common(test):
    test.assertTrue(COMMON.is_file(), "diag07_common.py is required")
    return load_common()


class SnapshotIdentityTests(unittest.TestCase):
    def test_archive_matches_commit_and_bootstrap_is_first(self) -> None:
        _require_common(self)
        with tempfile.TemporaryDirectory() as temporary:
            snap = Path(temporary) / "gen7"
            snap.mkdir()
            archived = subprocess.run(
                ["git", "archive", GEN7, "pinn", "configs"],
                cwd=ROOT,
                check=True,
                capture_output=True,
            )
            extracted = subprocess.run(
                ["tar", "-x", "-C", str(snap)],
                input=archived.stdout,
                check=True,
            )
            self.assertEqual(extracted.returncode, 0)
            probe = textwrap.dedent(
                """
                import hashlib, importlib.util, sys
                from pathlib import Path
                repo, common, snap = map(Path, sys.argv[1:4])
                spec = importlib.util.spec_from_file_location(
                    "phase59_diag07_common_snapshot", common
                )
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                identity = module.verify_snapshot(snap, repo)
                if len(identity["snapshot_digest"]) != 64:
                    raise SystemExit("digest is not 64 hex")
                if int(identity["snapshot_files"]) <= 0:
                    raise SystemExit("file count is empty")
                target = snap / "pinn" / "__init__.py"
                original = target.read_bytes()
                mutated = bytearray(original)
                mutated[0] ^= 1
                target.write_bytes(mutated)
                try:
                    module.verify_snapshot(snap, repo)
                except Exception:
                    print("CORRUPT-RAISED")
                else:
                    raise SystemExit("corrupt snapshot was accepted")
                target.write_bytes(original)
                booted = module.bootstrap(snap, repo)
                import pinn
                if not Path(pinn.__file__).resolve().is_relative_to(snap.resolve()):
                    raise SystemExit("pinn.__file__ is outside the snapshot")
                if booted.get("pinn_module_root") != "code_root":
                    raise SystemExit("pinn_module_root is not code_root")
                if sys.path[0] != str(snap.resolve()):
                    raise SystemExit("snapshot was not inserted first")
                if str(repo.resolve()) in sys.path:
                    raise SystemExit("repository root was added to sys.path")
                for name, digest in booted["overlay_modules"].items():
                    leaf = name.rsplit(".", 1)[1]
                    path = (repo / "pinn" / "verification" / f"{leaf}.py").resolve()
                    loaded = Path(sys.modules[name].__file__).resolve()
                    if loaded != path:
                        raise SystemExit(f"{name} did not load from the repository")
                    if hashlib.sha256(path.read_bytes()).hexdigest() != digest:
                        raise SystemExit(f"{name} digest mismatch")
                print("SNAPSHOT-OK")
                """
            ).strip()
            first = subprocess.run(
                [sys.executable, "-B", "-c", probe, str(ROOT), str(COMMON), str(snap)],
                cwd=ROOT,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(first.returncode, 0, first.stderr + first.stdout)
            self.assertIn("CORRUPT-RAISED", first.stdout)
            self.assertIn("SNAPSHOT-OK", first.stdout)
            second = subprocess.run(
                [
                    sys.executable, "-B", "-c",
                    "import pinn\n"
                    "import importlib.util, sys\n"
                    "from pathlib import Path\n"
                    "repo, common, snap = map(Path, sys.argv[1:4])\n"
                    "spec = importlib.util.spec_from_file_location('phase59_diag07_late', common)\n"
                    "module = importlib.util.module_from_spec(spec)\n"
                    "spec.loader.exec_module(module)\n"
                    "try:\n"
                    "    module.bootstrap(snap, repo)\n"
                    "except Exception:\n"
                    "    print('LATE-RAISED')\n"
                    "else:\n"
                    "    raise SystemExit('bootstrap accepted an imported pinn')\n",
                    str(ROOT), str(COMMON), str(snap),
                ],
                cwd=ROOT,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(second.returncode, 0, second.stderr + second.stdout)
            self.assertIn("LATE-RAISED", second.stdout)


class RegistryTests(unittest.TestCase):
    def test_retention_sha_and_adam_step_are_refused_before_a_bad_load(self) -> None:
        module = _require_common(self)
        from pinn.verification.feasibility_scorecard import load_scorecard
        from pinn.verification import production_reference

        scorecard = load_scorecard()
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            relative = Path("runs") / SEED42 / "checkpoints" / "best.pt"
            target = root / relative
            target.parent.mkdir(parents=True)
            raw = b"arbitrary-bytes"
            target.write_bytes(raw)
            retention_path = (
                root
                / ".planning/phases/57-corrected-re-run-the-preserved-evaluation"
                / "evidence/generation-7-retention.json"
            )
            retention_path.parent.mkdir(parents=True)
            retention_path.write_text(
                json.dumps({"files": [{"path": relative.as_posix(), "sha256": "0" * 64}]}),
                encoding="utf-8",
            )

            def refuse_load(*_args, **_kwargs):
                raise AssertionError("torch.load reached")

            with mock.patch.object(production_reference.torch, "load", refuse_load):
                with self.assertRaises(ValueError):
                    module.load_registry_checkpoint(
                        root, SEED42, "best.pt", scorecard=scorecard
                    )
            digest = hashlib.sha256(raw).hexdigest()
            retention_path.write_text(
                json.dumps({"files": [{"path": relative.as_posix(), "sha256": digest}]}),
                encoding="utf-8",
            )
            with mock.patch.object(
                production_reference.torch,
                "load",
                return_value={"counters": {"global_step": 899}, "optimizer": None},
            ):
                with self.assertRaises(ValueError):
                    module.load_registry_checkpoint(
                        root, SEED42, "best.pt", scorecard=scorecard
                    )
            early = {
                "counters": {"global_step": 900},
                "optimizer": {"state": {0: {"step": 899.0}}, "param_groups": []},
            }
            with mock.patch.object(production_reference.torch, "load", return_value=early):
                with self.assertRaises(ValueError):
                    module.load_registry_checkpoint(
                        root, SEED42, "best.pt", scorecard=scorecard
                    )
            accepted = {
                "counters": {"global_step": 900},
                "optimizer": {
                    "state": {0: {"step": 900.0}, 1: {"step": 900.0}},
                    "param_groups": [],
                },
            }
            with mock.patch.object(production_reference.torch, "load", return_value=accepted):
                payload, provenance = module.load_registry_checkpoint(
                    root, SEED42, "best.pt", scorecard=scorecard
                )
            self.assertEqual(int(payload["counters"]["global_step"]), 900)
            self.assertEqual(provenance["adam_step"], 900.0)
        real_payload, real_provenance = module.load_registry_checkpoint(
            ROOT, SEED42, "best.pt", scorecard=scorecard
        )
        self.assertEqual(int(real_payload["counters"]["global_step"]), 900)
        self.assertEqual(real_provenance["adam_step"], 900.0)


class RunBookkeepingTests(unittest.TestCase):
    def _patches(self, repo: Path):
        from pinn.verification import evidence_io

        def repo_root(explicit=None):
            if explicit is None:
                return Path(repo)
            return Path(explicit)

        return evidence_io, mock.patch.object(evidence_io, "_repo_root", repo_root)

    def test_freeze_and_preflight_failures_propagate(self) -> None:
        module = _require_common(self)
        from pinn.verification import evidence_io

        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            with mock.patch.object(
                evidence_io,
                "require_frozen_scorecard",
                side_effect=evidence_io.FreezeNotEstablished("absent"),
            ):
                with self.assertRaises(evidence_io.FreezeNotEstablished):
                    module.start_run(
                        root, ["jx10.json"], label="jx10",
                        command=["python", "driver"], required_bytes=1024,
                    )
            self.assertFalse((root / "logs" / "launch.lock.log").exists())
            preflight = mock.Mock(
                side_effect=evidence_io.MemoryPreflightError("short")
            )
            with self._patches(root)[1], mock.patch.object(
                evidence_io, "require_frozen_scorecard", return_value={"head": "x"}
            ), mock.patch.object(evidence_io, "memory_preflight", preflight):
                with self.assertRaises(evidence_io.MemoryPreflightError):
                    module.start_run(
                        root / "area", ["jx10.json"], label="jx10",
                        command=["python", "driver"], required_bytes=1024,
                    )
            failure = root / ".planning/phases/59-read-only-baseline-scorecard/evidence/logs/launch-failures.log"
            self.assertTrue(failure.is_file())
            self.assertIn("short", failure.read_text(encoding="utf-8"))
            lock = root / ".planning/phases/59-read-only-baseline-scorecard/evidence/logs/launch.lock.log"
            self.assertFalse(lock.exists())

    def test_launch_lock_orders_preflight_markers_and_release(self) -> None:
        module = _require_common(self)
        evidence_io, repo_patch = self._patches(Path("."))
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            area = root / "area"
            area.mkdir()
            kept = area / "jx02.done.json"
            kept.write_text(
                json.dumps({"result_files": {"jx02.json": "abc"}}) + "\n",
                encoding="utf-8",
            )
            stale = area / "jx10.done.json"
            stale.write_text(
                json.dumps({"result_files": {"jx10.json": "old"}}) + "\n",
                encoding="utf-8",
            )
            calls = []

            def preflight(required_bytes, **_kwargs):
                calls.append(required_bytes)
                return {
                    "available_bytes": 10,
                    "required_bytes": int(required_bytes),
                    "source": "vm_stat",
                }

            with mock.patch.object(evidence_io, "_repo_root", lambda explicit=None: root), mock.patch.object(
                evidence_io, "require_frozen_scorecard", return_value={"head": "x"}
            ):
                evidence_io.begin_long_step("survey", "survey", command=["survey"])
                with mock.patch.object(evidence_io, "memory_preflight", preflight):
                    with self.assertRaises(evidence_io.LaunchRefused) as caught:
                        module.start_run(
                            area, ["jx10.json"], label="jx10",
                            command=["python", "driver"], required_bytes=64,
                        )
                self.assertIn("survey/survey", str(caught.exception))
                self.assertEqual(calls, [])
                self.assertTrue(stale.is_file())
                holder = json.loads(
                    (
                        root
                        / ".planning/phases/59-read-only-baseline-scorecard/evidence/logs/launch.lock.log"
                    ).read_text(encoding="utf-8")
                )
                evidence_io.record_long_step_failure("holder-finished", run_id=holder["run_id"])
                with mock.patch.object(evidence_io, "memory_preflight", preflight):
                    info = module.start_run(
                        area, ["jx10.json"], label="jx10",
                        command=["python", "driver"], required_bytes=64,
                    )
                self.assertEqual(calls, [64])
                self.assertTrue(info["run_id"])
                self.assertFalse(stale.exists())
                self.assertTrue(kept.is_file())
                (area / "jx10.json").write_text("{}\n", encoding="utf-8")
                real_end = evidence_io.end_long_step

                def end_after_marker(run_id, **kwargs):
                    self.assertTrue((area / "jx10.done.json").is_file())
                    return real_end(run_id, **kwargs)

                with mock.patch.object(evidence_io, "end_long_step", end_after_marker):
                    marker = module.finish_run(
                        area, "jx10", ["jx10.json"],
                        command=["python", "driver"], run_info=info,
                    )
                self.assertTrue(marker.is_file())
                payload = json.loads(marker.read_text(encoding="utf-8"))
                self.assertEqual(set(payload["result_files"]), {"jx10.json"})
                lock = (
                    root
                    / ".planning/phases/59-read-only-baseline-scorecard/evidence/logs/launch.lock.log"
                )
                self.assertFalse(lock.exists())
                info = module.start_run(
                    area, ["jx01.json"], label="jx01",
                    command=["python", "driver"], required_bytes=64,
                )
                module.fail_run(info, "tolerance")
                self.assertFalse(lock.exists())
                text = (
                    root
                    / ".planning/phases/59-read-only-baseline-scorecard/evidence/logs/launch-failures.log"
                ).read_text(encoding="utf-8")
                self.assertIn("tolerance", text)

    def test_producer_hashes_cover_the_driver_and_overlays(self) -> None:
        module = _require_common(self)
        driver = (
            ROOT
            / ".planning/phases/59-read-only-baseline-scorecard/evidence/diag07/jx01_jx10.py"
        )
        self.assertTrue(driver.is_file(), "jx01_jx10.py is required")
        hashes = module.producer_hashes(driver)
        expected = [
            COMMON.relative_to(ROOT).as_posix(),
            driver.relative_to(ROOT).as_posix(),
            "pinn/verification/feasibility_scorecard.py",
            "pinn/verification/evidence_io.py",
            "pinn/verification/split_allowlist.py",
            "pinn/verification/production_reference.py",
            "pinn/verification/feasibility_scorer.py",
        ]
        self.assertEqual(list(hashes), expected)
        for relative, digest in hashes.items():
            self.assertEqual(
                digest, hashlib.sha256((ROOT / relative).read_bytes()).hexdigest()
            )


class RefusingStoreTests(unittest.TestCase):
    def test_every_write_method_refuses_and_should_checkpoint_is_false(self) -> None:
        module = _require_common(self)
        store = module.RefusingCheckpointStore()
        names = (
            "save", "save_rolling", "save_best", "save_anchor", "promote",
            "record_disposition", "load_latest", "load_checkpoint", "rollback",
            "fallback_scan",
        )
        for name in names:
            with self.subTest(name=name):
                with self.assertRaises(module.CheckpointWriteRefused):
                    getattr(store, name)()
        self.assertFalse(store.should_checkpoint(1, 0.0))
        self.assertEqual(store.write_attempts, len(names))


class MonitorFieldsTests(unittest.TestCase):
    def test_prefix_fields_follow_the_phase58_formulas(self) -> None:
        module = _require_common(self)
        rtilde = [0.3, 0.4, 0.6] + [0.0] * 13

        class _Controller:
            def _evaluate_front_monitor(self):
                return {
                    "w_n_stats": {
                        "w_min": 0.1, "w_mean": 0.2, "w_max": 0.9, "front_idx": 1,
                    },
                    "residuals_per_bin": list(rtilde),
                    "raw_residuals_per_bin": [5.0] * 16,
                }

        fields = module.monitor_fields(_Controller())
        self.assertEqual(fields["front_idx"], 1)
        self.assertAlmostEqual(fields["prefix_through_front"], 0.7)
        self.assertAlmostEqual(fields["prefix_to_cross_next"], 1.3)
        self.assertEqual(fields["rtilde_bins_0_5"], rtilde[:6])
        self.assertAlmostEqual(fields["rtilde_median_all_bins"], 0.0)
        self.assertEqual(len(fields["prefix"]), 17)
        self.assertEqual(fields["rounded"]["prefix_through_front"], 0.7)


class ModuleProvenanceTests(unittest.TestCase):
    def test_a_module_outside_the_snapshot_and_overlays_is_refused(self) -> None:
        module = _require_common(self)
        import types

        bogus = types.ModuleType("pinn.diag07_outside")
        bogus.__file__ = str(Path(tempfile.gettempdir()) / "diag07_outside.py")
        sys.modules[bogus.__name__] = bogus
        try:
            with self.assertRaises(RuntimeError):
                module.assert_module_provenance(ROOT, ROOT, {})
        finally:
            sys.modules.pop(bogus.__name__, None)
        module.assert_module_provenance(ROOT, ROOT, {})


if __name__ == "__main__":
    unittest.main()
