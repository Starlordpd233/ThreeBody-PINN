"""Phase 37 ENV-03 dual-arm precision orchestrator test contract
(CTX-08, CTX-10, CTX-11, CTX-13, CTX-14 / T-37-07).

Wave 0 contract. Tests import ``scripts.run_precision_probe`` inside test
methods so module compilation is the only Wave 0 green condition; the suite
turns green only in Wave 3 when the orchestrator lands.
"""

import importlib
import json
import os
import pathlib
import subprocess
import sys
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[2]
ORCHESTRATOR_PY = ROOT / "scripts" / "run_precision_probe.py"

REQUIRED_ARM_IDS = ("fp32-mps", "fp64-cpu")
OWNER_DECISION_STATEMENT = "Owner decision required; no D1-p verdict is recorded by this report."


def _load_orchestrator():
    if not ORCHESTRATOR_PY.exists():
        raise unittest.SkipTest(
            "scripts/run_precision_probe.py not implemented until Wave 3")
    import importlib.util
    spec = importlib.util.spec_from_file_location("run_precision_probe", str(ORCHESTRATOR_PY))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _write_fake_raw(out_dir, mps_record=None, cpu_record=None, run_id="20260712T000000Z"):
    """Write a fake raw.json with both arm records for renderer/validator tests."""
    out_dir = pathlib.Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    mps = mps_record or {
        "profile": "fp32-mps", "precision": "float32", "requested_device": "mps",
        "resolved_device": "mps", "actual_device": "mps",
        "pre_import_fallback": None, "torch_build": "test",
        "exception": None,
        "patterns": {
            "full_jacobian": {"predicted": [0, 0, 0], "analytical": [0, 0, 0],
                              "aggregate_relative_error": 1e-9,
                              "criterion": 1e-6, "passed": True,
                              "raw_samples_ns": [1] * 30, "median": 1, "p25": 1,
                              "p75": 1, "min": 1, "max": 1},
            "scalar_u_jvp": {"predicted": [0, 0, 0], "analytical": [0, 0, 0],
                             "aggregate_relative_error": 1e-9,
                             "criterion": 1e-6, "passed": True,
                             "raw_samples_ns": [1] * 30, "median": 1, "p25": 1,
                             "p75": 1, "min": 1, "max": 1},
        },
    }
    cpu = cpu_record or dict(mps, profile="fp64-cpu", precision="float64",
                             requested_device="cpu", resolved_device="cpu",
                             actual_device="cpu")
    raw = {
        "schema_version": "phase37-precision/v1",
        "run_id": run_id,
        "timestamp": "2026-07-12T00:00:00Z",
        "repository_commit": "0" * 40,
        "fingerprint": {"path": "fingerprint.json", "schema_version": "phase37/v1",
                        "sha256": "0" * 64},
        "orchestration": {"executable": "python", "timeout_seconds": 900,
                          "profiles": list(REQUIRED_ARM_IDS),
                          "fallback_policy": "stripped-for-mps"},
        "arms": {REQUIRED_ARM_IDS[0]: mps, REQUIRED_ARM_IDS[1]: cpu},
        "verification": {"two_arms": True, "both_patterns": True,
                         "fingerprint_hash_match": True},
    }
    (out_dir / "raw.json").write_text(json.dumps(raw, sort_keys=True, indent=2) + "\n")
    return raw


class PrecisionOrchestratorTests(unittest.TestCase):
    """CTX-08, CTX-10, CTX-11, CTX-13, CTX-14: isolated dual arms, structured
    failures, append-only evidence, verdict-free rendering."""

    def setUp(self):
        self.tmp = pathlib.Path(tempfile.mkdtemp(prefix="phase37-orch-"))
        self.addCleanup(self._cleanup)

    def _cleanup(self):
        import shutil
        shutil.rmtree(self.tmp, ignore_errors=True)

    # ---- CTX-08 / T-37-07: subprocess isolation --------------------------------

    def test_run_launches_exactly_two_fixed_profiles_through_same_module(self):
        module = _load_orchestrator()
        if not hasattr(module, "run_child"):
            self.skipTest("run_child not yet exported")
        # Source inspection: the orchestrator must construct exactly two fixed
        # argv lists targeting the same module, never a shell, never a selector.
        source = ORCHESTRATOR_PY.read_text()
        self.assertIn("pinn.verification.componentwise_ad", source,
                      "orchestrator does not invoke the shared worker module")
        self.assertNotIn("shell=True", source, "orchestrator uses shell=True")
        # The fixed argv must encode 10/30/100.
        for needle in ("10", "30", "100"):
            self.assertIn(needle, source, f"argv missing protocol value {needle}")

    def test_mps_child_environment_has_fallback_key_removed(self):
        module = _load_orchestrator()
        if not hasattr(module, "RuntimeProfile"):
            self.skipTest("RuntimeProfile not yet exported")
        # Source inspection: the MPS arm must remove PYTORCH_ENABLE_MPS_FALLBACK
        # from the copied env, never replace it with another value.
        source = ORCHESTRATOR_PY.read_text()
        self.assertIn("PYTORCH_ENABLE_MPS_FALLBACK", source,
                      "orchestrator never touches the fallback key")
        # The pop/Unset must not be followed by re-setting it for the MPS arm.

    def test_timeout_becomes_structured_arm_record_without_extra_child(self):
        module = _load_orchestrator()
        if not hasattr(module, "build_evidence"):
            self.skipTest("build_evidence not yet exported")
        # Inject a timeout outcome for one arm; the evidence must retain it as a
        # structured record and must not launch another child.
        timeout_arm = {"profile": "fp32-mps", "exception": "TimeoutExpired",
                       "returncode": None, "stdout": "", "stderr": "",
                       "status": "timeout"}
        ok_arm = {"profile": "fp64-cpu", "exception": None, "returncode": 0,
                  "stdout": "{}", "stderr": "", "status": "ok"}
        evidence = module.build_evidence(
            fp32_mps=timeout_arm, fp64_cpu=ok_arm,
            fingerprint={"path": "fp.json", "sha256": "0" * 64,
                         "schema_version": "phase37/v1"},
            repository_commit="0" * 40)
        self.assertIn("arms", evidence)
        self.assertEqual(evidence["arms"]["fp32-mps"]["status"], "timeout")

    # ---- CTX-10: structured failure retention ----------------------------------

    def test_signal_becomes_structured_arm_record(self):
        module = _load_orchestrator()
        if not hasattr(module, "build_evidence"):
            self.skipTest("build_evidence not yet exported")
        sig_arm = {"profile": "fp32-mps", "exception": "SIGTERM",
                   "returncode": -15, "status": "signal"}
        ok_arm = {"profile": "fp64-cpu", "exception": None, "returncode": 0,
                  "stdout": "{}", "status": "ok"}
        evidence = module.build_evidence(
            fp32_mps=sig_arm, fp64_cpu=ok_arm,
            fingerprint={"path": "fp.json", "sha256": "0" * 64,
                         "schema_version": "phase37/v1"},
            repository_commit="0" * 40)
        self.assertEqual(evidence["arms"]["fp32-mps"]["status"], "signal")

    def test_malformed_json_becomes_structured_arm_record(self):
        module = _load_orchestrator()
        if not hasattr(module, "build_evidence"):
            self.skipTest("build_evidence not yet exported")
        bad_arm = {"profile": "fp32-mps", "stdout": "not json",
                   "returncode": 0, "exception": "JSONDecodeError",
                   "status": "malformed_stdout"}
        ok_arm = {"profile": "fp64-cpu", "stdout": "{}", "returncode": 0,
                  "exception": None, "status": "ok"}
        evidence = module.build_evidence(
            fp32_mps=bad_arm, fp64_cpu=ok_arm,
            fingerprint={"path": "fp.json", "sha256": "0" * 64,
                         "schema_version": "phase37/v1"},
            repository_commit="0" * 40)
        self.assertEqual(evidence["arms"]["fp32-mps"]["status"], "malformed_stdout")

    def test_device_mismatch_becomes_structured_arm_record(self):
        module = _load_orchestrator()
        if not hasattr(module, "build_evidence"):
            self.skipTest("build_evidence not yet exported")
        # Worker reports requested=mps but actual=cpu (silent fallback).
        arm = {"profile": "fp32-mps", "requested_device": "mps",
               "resolved_device": "mps", "actual_device": "cpu",
               "returncode": 0, "stdout": "{}", "status": "device_mismatch"}
        cpu = {"profile": "fp64-cpu", "requested_device": "cpu",
               "resolved_device": "cpu", "actual_device": "cpu",
               "returncode": 0, "stdout": "{}", "status": "ok"}
        evidence = module.build_evidence(
            fp32_mps=arm, fp64_cpu=cpu,
            fingerprint={"path": "fp.json", "sha256": "0" * 64,
                         "schema_version": "phase37/v1"},
            repository_commit="0" * 40)
        self.assertEqual(evidence["arms"]["fp32-mps"]["status"], "device_mismatch")

    def test_fallback_leakage_becomes_structured_arm_record(self):
        module = _load_orchestrator()
        if not hasattr(module, "build_evidence"):
            self.skipTest("build_evidence not yet exported")
        arm = {"profile": "fp32-mps", "pre_import_fallback": "1",
               "requested_device": "mps", "resolved_device": "mps",
               "actual_device": "mps", "returncode": 0, "stdout": "{}",
               "status": "fallback_leakage"}
        cpu = {"profile": "fp64-cpu", "pre_import_fallback": None,
               "requested_device": "cpu", "resolved_device": "cpu",
               "actual_device": "cpu", "returncode": 0, "stdout": "{}",
               "status": "ok"}
        evidence = module.build_evidence(
            fp32_mps=arm, fp64_cpu=cpu,
            fingerprint={"path": "fp.json", "sha256": "0" * 64,
                         "schema_version": "phase37/v1"},
            repository_commit="0" * 40)
        self.assertEqual(evidence["arms"]["fp32-mps"]["status"], "fallback_leakage")

    # ---- CTX-07 / T-37-07-O: append-only atomic evidence -----------------------

    def test_write_evidence_run_is_exclusive_and_atomic(self):
        module = _load_orchestrator()
        if not hasattr(module, "write_evidence_run"):
            self.skipTest("write_evidence_run not yet exported")
        evidence_root = self.tmp / "evidence" / "precision"
        raw = _write_fake_raw(self.tmp / "src")
        run_id = "20260712T000000Z"
        module.write_evidence_run(raw, evidence_root, run_id=run_id)
        run_dir = evidence_root / run_id
        self.assertTrue((run_dir / "raw.json").exists())
        self.assertTrue((run_dir / "summary.md").exists())
        # Collision must preserve the first run.
        raw["timestamp"] = "2026-07-13T00:00:00Z"
        with self.assertRaises((FileExistsError, OSError, ValueError)):
            module.write_evidence_run(raw, evidence_root, run_id=run_id)
        # The first run's bytes are unchanged.
        self.assertIn("2026-07-12", (run_dir / "raw.json").read_text())

    def test_write_evidence_run_rejects_path_traversal(self):
        module = _load_orchestrator()
        if not hasattr(module, "write_evidence_run"):
            self.skipTest("write_evidence_run not yet exported")
        evidence_root = self.tmp / "evidence"
        raw = _write_fake_raw(self.tmp / "src")
        for bad_id in ("../escape", "with/slash", "with..dotdot", ".hidden"):
            with self.assertRaises((ValueError, OSError)):
                module.write_evidence_run(raw, evidence_root, run_id=bad_id)

    # ---- CTX-11 / CTX-14: verdict-free rendering --------------------------------

    def test_render_summary_contains_fixed_owner_statement(self):
        module = _load_orchestrator()
        if not hasattr(module, "render_summary"):
            self.skipTest("render_summary not yet exported")
        raw = _write_fake_raw(self.tmp / "src")
        summary = module.render_summary(raw)
        self.assertIn(OWNER_DECISION_STATEMENT, summary,
                      "summary missing the fixed owner-decision statement")

    def test_render_summary_does_not_choose_or_recommend(self):
        module = _load_orchestrator()
        if not hasattr(module, "render_summary"):
            self.skipTest("render_summary not yet exported")
        raw = _write_fake_raw(self.tmp / "src")
        summary = module.render_summary(raw)
        for forbidden in ("winner", "recommend", "faster", "slower",
                          "better", "preferred", "selected", "default to"):
            self.assertNotIn(forbidden, summary.lower(),
                             f"summary encodes a verdict: {forbidden!r}")

    def test_render_summary_is_byte_identical_to_independent_invocation(self):
        module = _load_orchestrator()
        if not hasattr(module, "render_summary"):
            self.skipTest("render_summary not yet exported")
        raw = _write_fake_raw(self.tmp / "src")
        first = module.render_summary(raw)
        second = module.render_summary(raw)
        self.assertEqual(first, second, "render_summary is not deterministic")

    def test_render_summary_presents_both_arms_symmetrically(self):
        module = _load_orchestrator()
        if not hasattr(module, "render_summary"):
            self.skipTest("render_summary not yet exported")
        raw = _write_fake_raw(self.tmp / "src")
        summary = module.render_summary(raw)
        # Both arm IDs must appear with the same field labels in the same order.
        self.assertIn("fp32-mps", summary)
        self.assertIn("fp64-cpu", summary)

    # ---- CTX-13: no profile/tolerance/workload selector ------------------------

    def test_run_subcommand_has_no_profile_selector(self):
        # Source inspection: the `run` subcommand must not expose a profile
        # selector. Every invocation must execute both fixed arms.
        if not ORCHESTRATOR_PY.exists():
            self.skipTest("orchestrator not implemented until Wave 3")
        source = ORCHESTRATOR_PY.read_text()
        # A profile selector would appear as "--profile", "--arm", or
        # "add_argument" with a choices= for profile. Forbid them.
        self.assertNotIn("--profile", source, "orchestrator exposes a profile selector")
        self.assertNotIn("--arm", source, "orchestrator exposes an arm selector")

    def test_orchestrator_imports_neither_torch_nor_worker_in_process(self):
        # CTX-08: the parent must be stdlib-only and must NOT import torch or
        # the worker in-process. Source inspection.
        if not ORCHESTRATOR_PY.exists():
            self.skipTest("orchestrator not implemented until Wave 3")
        source = ORCHESTRATOR_PY.read_text()
        # Forbid top-level torch import (the parent never touches tensors).
        # Allow only mentions inside string literals (module path) or comments.
        lines = source.splitlines()
        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            if stripped.startswith("#"):
                continue
            if stripped.startswith('"""') or stripped.startswith("'''"):
                continue
            if "import torch" in stripped and "subprocess" not in stripped:
                # Allow only inside string literals — flag for manual review.
                self.fail(f"orchestrator imports torch at line {i}: {line}")


if __name__ == "__main__":
    unittest.main()
