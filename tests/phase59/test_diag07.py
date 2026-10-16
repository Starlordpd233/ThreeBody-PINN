"""Phase 59 DIAG-07 driver tests. The driver is loaded by path."""

from __future__ import annotations

import argparse
import dataclasses
import hashlib
import importlib.util
import json
import math
import subprocess
import sys
import tempfile
import textwrap
import unittest
from decimal import Decimal
from pathlib import Path
from unittest import mock

import torch


ROOT = Path(__file__).resolve().parents[2]
COMMON = (
    ROOT
    / ".planning/phases/59-read-only-baseline-scorecard/evidence/diag07/diag07_common.py"
)
DRIVER = (
    ROOT
    / ".planning/phases/59-read-only-baseline-scorecard/evidence/diag07/jx01_jx10.py"
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


def _require_function(test, name):
    module = _require_common(test)
    test.assertTrue(hasattr(module, name), f"diag07_common.{name} is required")
    return module


def load_driver():
    """Load the JX driver by path with its sibling library already bound."""
    common = load_common()
    with mock.patch.dict(sys.modules, {"diag07_common": common}):
        spec = importlib.util.spec_from_file_location("phase59_jx01_jx10", DRIVER)
        if spec is None or spec.loader is None:
            raise AssertionError(f"cannot load {DRIVER}")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
    return module


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


class RuntimePairTests(unittest.TestCase):
    def test_each_runtime_builds_with_a_pair_generation_7_permits(self) -> None:
        # Generation 7's resolve_runtime accepts only (float32, mps) and
        # (float64, cpu). The float64 run is promoted after a float32 restore;
        # it is never built as the refused (float32, cpu) pair.
        common = _require_common(self)
        driver = load_driver()
        from pinn.verification.feasibility_scorecard import load_scorecard

        class _Stop(Exception):
            pass

        seen = []

        def record(_code_root, _repo_root, _run, _sources, pair):
            seen.append(tuple(pair))
            raise _Stop

        for runtimes in ("mps", "cpu"):
            args = argparse.Namespace(code_root="unused", runtimes=runtimes)
            with mock.patch.object(common, "build_controller", record):
                with self.assertRaises(_Stop):
                    driver._run_jx10(
                        args, {}, {}, load_scorecard(), Path("."), Path("."),
                        ["jx01_jx10.py"],
                    )
        self.assertEqual(seen, [("float32", "mps"), ("float64", "cpu")])


class PacketDecimalBoundaryTests(unittest.TestCase):
    """GAP-59-11: a rounded packet field passes at exactly one fourth-decimal step.

    The frozen bound phase58_packet_rounded_abs stays 1e-4. The 4-decimal copies
    are compared in exact decimal units, so one step passes whichever way binary
    floating point rounds the difference, and two steps fail.
    """

    STEP = Decimal("0.0001")
    SCALARS = ("prefix_through_front", "prefix_to_cross_next", "rtilde_median_all_bins")

    @staticmethod
    def _scorecard():
        from pinn.verification.feasibility_scorecard import load_scorecard

        return load_scorecard()

    @staticmethod
    def _rows(scorecard, name=None, key=None, index=None, value=None):
        """Rows that equal the packet, with one rounded field replaced when asked."""
        packet = scorecard.section("diag07")["jx10"]["phase58_packet"]
        rows = {}
        for run_name, expected in packet.items():
            rows[run_name] = {
                "front_idx": expected["front_idx"],
                "raw_rbar_bin0": expected["raw_rbar_bin0"],
                "rounded": {
                    "prefix_through_front": expected["prefix_through_front"],
                    "prefix_to_cross_next": expected["prefix_to_cross_next"],
                    "rtilde_median_all_bins": expected["rtilde_median_all_bins"],
                    "rtilde_bins_0_5": list(expected["rtilde_bins_0_5"]),
                },
            }
        if name is not None:
            rounded = rows[name]["rounded"]
            if index is None:
                rounded[key] = value
            else:
                rounded[key][index] = value
        return rows

    @staticmethod
    def _passed(driver, scorecard, rows, check_name):
        checks = []
        supports = driver._compare_packet(rows, scorecard, checks)
        by_name = {item["name"]: item["passed"] for item in checks}
        return supports, by_name[check_name]

    def test_the_observed_one_step_pair_passes(self) -> None:
        # stage-0-init.pt bin 2: measured 2.0539 against the packet's 2.0538.
        # In doubles the gap is a hair over 1e-4; in decimal it is one step.
        self.assertGreater(2.0539 - 2.0538, 1e-4)
        driver = load_driver()
        scorecard = self._scorecard()
        rows = self._rows(scorecard, "stage-0-init.pt", "rtilde_bins_0_5", 2, 2.0539)
        supports, passed = self._passed(
            driver, scorecard, rows, "phase58.stage-0-init.pt.rtilde_bins_0_5",
        )
        self.assertTrue(passed)
        self.assertTrue(supports)

    def test_two_steps_fail(self) -> None:
        driver = load_driver()
        scorecard = self._scorecard()
        rows = self._rows(scorecard, "stage-0-init.pt", "rtilde_bins_0_5", 2, 2.0540)
        supports, passed = self._passed(
            driver, scorecard, rows, "phase58.stage-0-init.pt.rtilde_bins_0_5",
        )
        self.assertFalse(passed)
        self.assertFalse(supports)

    def test_a_pair_with_a_binary_gap_just_under_the_bound_passes(self) -> None:
        # best.pt bin 2: measured 0.6165 against the packet's 0.6166.
        self.assertEqual(0.6166 - 0.6165, 9.999999999998899e-05)
        driver = load_driver()
        scorecard = self._scorecard()
        rows = self._rows(scorecard, "best.pt", "rtilde_bins_0_5", 2, 0.6165)
        supports, passed = self._passed(
            driver, scorecard, rows, "phase58.best.pt.rtilde_bins_0_5",
        )
        self.assertTrue(passed)
        self.assertTrue(supports)

    def test_every_packet_value_passes_one_step_and_fails_two_either_way(self) -> None:
        driver = load_driver()
        scorecard = self._scorecard()
        packet = scorecard.section("diag07")["jx10"]["phase58_packet"]
        for name, expected in packet.items():
            sites = [(key, None, expected[key]) for key in self.SCALARS]
            sites += [
                ("rtilde_bins_0_5", index, value)
                for index, value in enumerate(expected["rtilde_bins_0_5"])
            ]
            for key, index, value in sites:
                for steps in (-2, -1, 1, 2):
                    with self.subTest(name=name, key=key, index=index, steps=steps):
                        moved = float(Decimal(repr(value)) + steps * self.STEP)
                        rows = self._rows(scorecard, name, key, index, moved)
                        _supports, passed = self._passed(
                            driver, scorecard, rows, f"phase58.{name}.{key}",
                        )
                        self.assertEqual(passed, abs(steps) == 1)

    def test_front_index_and_raw_rbar_checks_keep_their_own_rules(self) -> None:
        driver = load_driver()
        scorecard = self._scorecard()
        packet = scorecard.section("diag07")["jx10"]["phase58_packet"]
        base = self._rows(scorecard)
        base["best.pt"]["front_idx"] = packet["best.pt"]["front_idx"] + 1
        supports, passed = self._passed(
            driver, scorecard, base, "phase58.best.pt.front_idx",
        )
        self.assertFalse(passed)
        self.assertFalse(supports)
        for factor, wanted in ((1.00005, True), (1.00015, False)):
            with self.subTest(factor=factor):
                rows = self._rows(scorecard)
                rows["best.pt"]["raw_rbar_bin0"] = (
                    packet["best.pt"]["raw_rbar_bin0"] * factor
                )
                _supports, passed = self._passed(
                    driver, scorecard, rows, "phase58.best.pt.raw_rbar_bin0",
                )
                self.assertEqual(passed, wanted)


class ShareFormulaTests(unittest.TestCase):
    def test_shares_match_the_hand_computed_projections(self) -> None:
        # Toy two-parameter case. v_hat = exp_avg_sq / (1 - beta2**step) and
        # m_hat = exp_avg / (1 - beta1**step) with step 1; P = 1/(sqrt(v_hat)+eps).
        module = _require_function(self, "preconditioned_shares")
        beta1, beta2, eps, step = 0.9, 0.999, 1e-8, 1.0
        exp_avg, exp_avg_sq = [0.5, -0.25], [4.0, 1.0]
        weighted = {"phys": [1.0, 0.0], "ic": [0.0, 2.0]}
        total = [1.0, 2.0]
        got = module.preconditioned_shares(
            weighted, total, exp_avg, exp_avg_sq, step,
            beta1=beta1, beta2=beta2, eps=eps,
        )
        v_hat = [value / (1.0 - beta2 ** step) for value in exp_avg_sq]
        m_hat = [value / (1.0 - beta1 ** step) for value in exp_avg]
        precond = [1.0 / (math.sqrt(value) + eps) for value in v_hat]

        def project(vector, onto):
            left = [p * x for p, x in zip(precond, vector)]
            right = [p * x for p, x in zip(precond, onto)]
            return sum(a * b for a, b in zip(left, right)) / sum(b * b for b in right)

        for name, vector in weighted.items():
            self.assertAlmostEqual(got["primary"][name], project(vector, total), places=12)
            self.assertAlmostEqual(got["secondary"][name], project(vector, m_hat), places=12)
        self.assertAlmostEqual(got["primary_sum"], 1.0, places=12)
        self.assertGreater(got["primary"]["phys"], 0.0)

    def test_vectors_of_different_lengths_are_refused(self) -> None:
        module = _require_function(self, "preconditioned_shares")
        with self.assertRaises(ValueError):
            module.preconditioned_shares(
                {"phys": [1.0, 0.0, 0.0]}, [1.0, 2.0], [0.5, -0.25], [4.0, 1.0], 1.0,
                beta1=0.9, beta2=0.999, eps=1e-8,
            )


class FlattenTests(unittest.TestCase):
    @staticmethod
    def _model_and_payload():
        model = torch.nn.Linear(2, 1)
        state = {
            0: {
                "step": torch.tensor(7.0),
                "exp_avg": torch.tensor([[1.0, 2.0]]),
                "exp_avg_sq": torch.tensor([[3.0, 4.0]]),
            },
            1: {
                "step": torch.tensor(7.0),
                "exp_avg": torch.tensor([5.0]),
                "exp_avg_sq": torch.tensor([6.0]),
            },
        }
        return model, {"optimizer": {"state": state, "param_groups": [{"params": [0, 1]}]}}

    def test_state_follows_model_parameter_order(self) -> None:
        module = _require_function(self, "flatten_optimizer_state")
        model, payload = self._model_and_payload()
        exp_avg, exp_avg_sq, step = module.flatten_optimizer_state(payload, model)
        self.assertEqual(exp_avg.tolist(), [1.0, 2.0, 5.0])
        self.assertEqual(exp_avg_sq.tolist(), [3.0, 4.0, 6.0])
        self.assertEqual(exp_avg.dtype, torch.float64)
        self.assertEqual(step, 7.0)

    def test_a_missing_entry_a_different_shape_or_no_state_is_refused(self) -> None:
        module = _require_function(self, "flatten_optimizer_state")
        model, payload = self._model_and_payload()
        del payload["optimizer"]["state"][1]
        with self.assertRaises(ValueError):
            module.flatten_optimizer_state(payload, model)
        model, payload = self._model_and_payload()
        payload["optimizer"]["state"][1]["exp_avg"] = torch.tensor([5.0, 9.0])
        with self.assertRaises(ValueError):
            module.flatten_optimizer_state(payload, model)
        model, payload = self._model_and_payload()
        payload["optimizer"] = None
        with self.assertRaises(ValueError):
            module.flatten_optimizer_state(payload, model)


class _DecompositionFixture(unittest.TestCase):
    """A tiny CPU float64 controller with a refusing store and non-zero lambdas."""

    TERMS = ("data", "ic", "phys", "energy", "angmom")

    def setUp(self) -> None:
        self._tmpdir = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmpdir.cleanup)

    def build(self, module):
        from tests.phase40.test_optimizer_phase import _build_controller

        controller = _build_controller(
            self._tmpdir.name, max_epochs=1, n_adam=1, collocation_count=64,
        )
        store = module.RefusingCheckpointStore()
        controller._checkpoint_store = store
        parameters = tuple(p for p in controller.model.parameters() if p.requires_grad)
        batch = controller._stage_batch(
            controller._train_source, stage=0, collocation_count=64,
        )
        anchor_ctx = controller._build_anchor_context(
            controller._train_source, batch, None,
        )
        weights = dataclasses.replace(
            controller.scheduled_weights.current(0),
            lambda_phys=0.7, lambda_e=0.3, lambda_l=0.2,
        )
        return controller, store, parameters, batch, anchor_ctx, weights

    @staticmethod
    def norm(vector) -> float:
        return float(torch.linalg.vector_norm(vector))


class DecompositionTests(_DecompositionFixture):
    def test_norms_and_weighted_sum_match_the_trainer_and_nothing_changes(self) -> None:
        module = _require_function(self, "per_term_gradients")
        controller, store, parameters, batch, anchor_ctx, weights = self.build(module)
        before = [parameter.detach().clone() for parameter in parameters]
        vectors = module.per_term_gradients(
            controller, batch, anchor_ctx, weights, microbatch_size=20,
        )
        self.assertTrue(all(parameter.grad is None for parameter in parameters))
        _terms, stats = controller._run_adam_step_microbatched(
            batch, anchor_ctx, weights, parameters,
            microbatch_size=20, want_diagnostics=True,
        )
        trainer_grad = torch.cat([
            (p.grad if p.grad is not None else torch.zeros_like(p))
            .detach().reshape(-1).to(torch.float64)
            for p in parameters
        ])
        for parameter in parameters:
            parameter.grad = None
        for name in self.TERMS:
            with self.subTest(term=name):
                trainer = float(stats[f"grad_norm_raw_{name}"])
                self.assertGreater(trainer, 0.0)
                self.assertLessEqual(
                    abs(self.norm(vectors[name]) - trainer), 1e-10 * trainer,
                )
        difference = self.norm(trainer_grad - vectors["total_weighted"])
        self.assertLessEqual(difference, 1e-10 * self.norm(trainer_grad))
        self.assertEqual(vectors["total_weighted"].dtype, torch.float64)
        for parameter, original in zip(parameters, before):
            self.assertTrue(torch.equal(parameter.detach(), original))
        self.assertEqual(store.write_attempts, 0)
        self.assertIsNone(controller._optimizer)


class MicrobatchEquivalenceTests(_DecompositionFixture):
    def test_per_term_vectors_do_not_depend_on_the_microbatch_size(self) -> None:
        module = _require_function(self, "per_term_gradients")
        controller, _store, _parameters, batch, anchor_ctx, weights = self.build(module)
        reference = module.per_term_gradients(
            controller, batch, anchor_ctx, weights, microbatch_size=1000,
        )
        for size in (3, 64):
            other = module.per_term_gradients(
                controller, batch, anchor_ctx, weights, microbatch_size=size,
            )
            for name, vector in reference.items():
                with self.subTest(size=size, term=name):
                    self.assertLessEqual(
                        self.norm(other[name] - vector), 1e-6 * self.norm(vector),
                    )


class IcSplitTests(_DecompositionFixture):
    def test_the_ic_gradient_is_the_position_half_plus_the_velocity_half(self) -> None:
        module = _require_function(self, "per_term_gradients")
        controller, _store, _parameters, batch, anchor_ctx, weights = self.build(module)
        vectors = module.per_term_gradients(
            controller, batch, anchor_ctx, weights, microbatch_size=20,
        )
        self.assertGreater(self.norm(vectors["ic_position"]), 0.0)
        self.assertGreater(self.norm(vectors["ic_velocity"]), 0.0)
        residual = vectors["ic"] - vectors["ic_position"] - vectors["ic_velocity"]
        self.assertLessEqual(self.norm(residual), 1e-10 * self.norm(vectors["ic"]))


class Jx1FlowTests(_DecompositionFixture):
    """The driver's JX-1 measurement on the tiny controller, with a synthetic payload."""

    def test_one_measurement_records_norms_cosines_and_shares_without_side_effects(self) -> None:
        common = _require_function(self, "per_term_gradients")
        driver = load_driver()
        self.assertTrue(hasattr(driver, "_measure_jx1"), "_measure_jx1 is required")
        from pinn.verification.feasibility_scorecard import load_scorecard

        scorecard = load_scorecard()
        controller, store, parameters, batch, _anchor_ctx, _weights = self.build(common)
        controller._front_monitor_batch = batch
        generator = torch.Generator().manual_seed(0)
        state = {
            index: {
                "step": torch.tensor(900.0),
                "exp_avg": torch.randn(parameter.shape, generator=generator) * 1e-3,
                "exp_avg_sq": torch.rand(parameter.shape, generator=generator) * 1e-6 + 1e-9,
            }
            for index, parameter in enumerate(parameters)
        }
        payload = {
            "counters": {"global_step": 900},
            "optimizer": {
                "state": state,
                "param_groups": [{
                    "params": list(range(len(parameters))),
                    "betas": (0.9, 0.999),
                    "eps": 1e-8,
                }],
            },
        }
        before = [parameter.detach().clone() for parameter in parameters]
        checks, flags = [], {"parameters": True, "grads": True, "files": True, "optimizer": True}
        with mock.patch.object(
            common, "load_registry_checkpoint", return_value=(payload, {"file": "best.pt"}),
        ), mock.patch.object(common, "file_hashes", return_value={}), mock.patch.object(
            driver, "_load_into",
        ):
            records, provenance = driver._measure_jx1(
                controller, ROOT, [900], {900: "best.pt"}, scorecard,
                ("float64", "cpu"), 20, 1e-5, "cpu", checks, flags,
            )
        record = records[900]
        json.dumps(record)
        self.assertEqual(provenance, [{"file": "best.pt"}])
        self.assertTrue(all(item["passed"] for item in checks), checks)
        self.assertTrue(all(flags.values()), flags)
        self.assertEqual(set(record["grad_norm_raw"]), set(driver._TERMS))
        self.assertEqual(
            set(record["cosines"]), {"ic_phys", "ic_data", "phys_data"},
        )
        self.assertGreater(record["ic_split"]["position_norm"], 0.0)
        shares = record["shares"]
        self.assertAlmostEqual(shares["primary_sum"], 1.0, places=6)
        self.assertEqual(shares["adam_step"], 900.0)
        self.assertIn("physics", shares["reading"])
        self.assertTrue(all(parameter.grad is None for parameter in parameters))
        for parameter, original in zip(parameters, before):
            self.assertTrue(torch.equal(parameter.detach(), original))
        self.assertEqual(store.write_attempts, 0)
        self.assertIsNone(controller._optimizer)

    def test_a_checkpoint_without_moments_records_that_no_share_is_computable(self) -> None:
        common = _require_function(self, "per_term_gradients")
        driver = load_driver()
        self.assertTrue(hasattr(driver, "_measure_jx1"), "_measure_jx1 is required")
        from pinn.verification.feasibility_scorecard import load_scorecard

        scorecard = load_scorecard()
        controller, _store, _parameters, batch, _anchor_ctx, _weights = self.build(common)
        controller._front_monitor_batch = batch
        payload = {"counters": {"global_step": 0}, "optimizer": None}
        checks, flags = [], {"parameters": True, "grads": True, "files": True, "optimizer": True}
        with mock.patch.object(
            common, "load_registry_checkpoint", return_value=(payload, {"file": "init.pt"}),
        ), mock.patch.object(common, "file_hashes", return_value={}), mock.patch.object(
            driver, "_load_into",
        ):
            records, _provenance = driver._measure_jx1(
                controller, ROOT, [0], {0: "init.pt"}, scorecard,
                ("float64", "cpu"), 20, 1e-5, "cpu", checks, flags,
            )
        self.assertEqual(records[0]["shares"], "not computable: no stored moments")
        self.assertTrue(all(item["passed"] for item in checks), checks)

    def test_cpu_against_mps_uses_the_frozen_relative_and_absolute_floor_rules(self) -> None:
        driver = load_driver()
        self.assertTrue(hasattr(driver, "_compare_jx1_cpu"), "_compare_jx1_cpu is required")
        from pinn.verification.feasibility_scorecard import load_scorecard

        scorecard = load_scorecard()
        terms = driver._TERMS

        def record(norm, share):
            kinds = {kind: {term: share for term in terms} for kind in ("primary", "secondary")}
            return {"grad_norm_raw": {term: norm for term in terms}, "shares": kinds}

        def outcome(cpu_norm, cpu_share):
            checks = []
            driver._compare_jx1_cpu(
                {900: record(1.0, 0.0)}, {900: record(cpu_norm, cpu_share)}, scorecard, checks,
            )
            return {item["name"]: item["passed"] for item in checks}

        inside = outcome(1.0009, 9e-8)
        self.assertTrue(all(inside.values()), inside)
        norm_out = outcome(1.0011, 0.0)
        self.assertFalse(norm_out["jx1.cpu_vs_mps.900.grad_norms"])
        share_out = outcome(1.0, 2e-7)
        self.assertFalse(share_out["jx1.cpu_vs_mps.900.shares"])


class CosineTests(unittest.TestCase):
    def test_cosine_of_parallel_orthogonal_and_zero_vectors(self) -> None:
        module = _require_function(self, "cosine")
        self.assertAlmostEqual(module.cosine([1.0, 2.0], [2.0, 4.0]), 1.0, places=12)
        self.assertAlmostEqual(module.cosine([1.0, 0.0], [0.0, 3.0]), 0.0, places=12)
        self.assertAlmostEqual(module.cosine([1.0, 0.0], [-2.0, 0.0]), -1.0, places=12)
        self.assertIsNone(module.cosine([0.0, 0.0], [1.0, 1.0]))


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
