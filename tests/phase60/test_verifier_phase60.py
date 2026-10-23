"""Phase 60: tests for the independent evidence verifier (SPEC R4, R8).

Unit tests on synthetic repositories and evidence trees verifying fail-closed
behavior of all subcommands (protocol, preflight, records, g2, rescore, final).
"""

from __future__ import annotations

import contextlib
import importlib.util
import io
import json
import os
import shutil
import subprocess
import tempfile
import unittest
from collections import OrderedDict
from pathlib import Path
from types import SimpleNamespace
from unittest import mock

import torch

from pinn.network import ArchitectureSpec, build_network
from pinn.training.atomic_io import atomic_write_torch
from pinn.training.controllers import _tensor_hash
from pinn.verification import learnability_run
from pinn.verification.feasibility_scorecard import SCORECARD_SHA256
from pinn.verification.learnability_arms import SEED

VERIFIER_PATH = (
    Path(__file__).resolve().parents[2]
    / ".planning/phases/60-single-system-learnability/evidence/verify_phase60_evidence.py"
)


def load_verifier():
    spec = importlib.util.spec_from_file_location("verify_phase60_evidence", VERIFIER_PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _git(root: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    proc = subprocess.run(
        ["git", *args], cwd=root, capture_output=True, text=True, check=False
    )
    if check and proc.returncode != 0:
        raise AssertionError(f"git {' '.join(args)} failed: {proc.stderr}")
    return proc


def init_repo(root: Path) -> None:
    _git(root, "init")
    _git(root, "config", "user.email", "phase60@example.com")
    _git(root, "config", "user.name", "phase60")


def commit_all(root: Path, message: str) -> str:
    _git(root, "add", "-A")
    _git(root, "commit", "-m", message)
    return _git(root, "rev-parse", "HEAD").stdout.strip()


def run_main(module, argv: list[str]) -> tuple[int, str, str]:
    stdout = io.StringIO()
    stderr = io.StringIO()
    with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
        code = module.main(argv)
    return code, stdout.getvalue(), stderr.getvalue()


class VerifierStructureTests(unittest.TestCase):
    def setUp(self):
        self.module = load_verifier()

    def test_required_real_fields_equals_runner_list(self):
        self.assertEqual(
            self.module.REQUIRED_REAL_FIELDS,
            learnability_run.REQUIRED_REAL_FIELDS,
        )

    def test_g2_tokens_equals_five_pairs(self):
        expected = {
            "outcome": "g2-outcome.json",
            "sweep-curve": "sweep-curve.json",
            "rescue": "rescue.json",
            "skip-records": "skip-records.json",
            "stop-handoff": "stop-handoff.json",
        }
        self.assertEqual(self.module.G2_TOKENS, expected)


class ProtocolCheckTests(unittest.TestCase):
    def setUp(self):
        self.module = load_verifier()
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        self.root = Path(self.temp_dir.name)
        init_repo(self.root)

        # 1. Amendment commit
        req_file = self.root / ".planning/REQUIREMENTS.md"
        req_file.parent.mkdir(parents=True, exist_ok=True)
        req_file.write_text("# Requirements\n", encoding="utf-8")
        self.amendment_commit = commit_all(self.root, "spec(60-03): apply the phase 60 scope amendment text")

        # 2. Scorecard
        card_file = self.root / self.module.SCORECARD_REL
        card_file.parent.mkdir(parents=True, exist_ok=True)
        real_card = Path(__file__).resolve().parents[2] / self.module.SCORECARD_REL
        card_file.write_bytes(real_card.read_bytes())

        # 3. Scorer successor
        scorer_file = self.root / self.module.SCORER_REL
        scorer_file.parent.mkdir(parents=True, exist_ok=True)
        real_scorer = Path(__file__).resolve().parents[2] / self.module.SCORER_REL
        scorer_file.write_bytes(real_scorer.read_bytes())
        scorer_sha = self.module.sha256_file(scorer_file)

        succ_file = self.root / self.module.SCORER_SUCCESSOR_REL
        succ_file.parent.mkdir(parents=True, exist_ok=True)
        succ_payload = {
            "schema": "phase60-scorer-successor/v1",
            "path": self.module.SCORER_REL,
            "predecessor_sha256": "0" * 64,
            "successor_sha256": scorer_sha,
            "reason": "fix MPS widening",
            "note": "test",
        }
        succ_file.write_text(json.dumps(succ_payload) + "\n", encoding="utf-8")

        # 4. Pinned modules
        module_shas = {}
        for mod_rel in self.module.PINNED_MODULES:
            dest = self.root / mod_rel
            dest.parent.mkdir(parents=True, exist_ok=True)
            if not dest.is_file():
                real_mod = Path(__file__).resolve().parents[2] / mod_rel
                dest.write_bytes(real_mod.read_bytes() if real_mod.is_file() else b"# stub\n")
            module_shas[mod_rel] = self.module.sha256_file(dest)

        # 5. Preflight records
        preflight_file = self.root / self.module.PREFLIGHT_REL
        preflight_file.parent.mkdir(parents=True, exist_ok=True)
        preflight_file.write_text('{"schema": "phase60-preflight/v1"}\n', encoding="utf-8")
        preflight_sha = self.module.sha256_file(preflight_file)

        # 6. Run protocol
        proto_file = self.root / self.module.PROTOCOL_REL
        proto_file.parent.mkdir(parents=True, exist_ok=True)
        proto_payload = {
            "schema": self.module.PROTOCOL_SCHEMA,
            "scorecard_sha256": SCORECARD_SHA256,
            "scorer_sha256": scorer_sha,
            "amendment_commit": self.amendment_commit,
            "preflight_sha256": preflight_sha,
            "module_sha256": module_shas,
            "g2": {"failed_confirmation_pre_answer": None},
        }
        proto_file.write_text(json.dumps(proto_payload) + "\n", encoding="utf-8")
        proto_sha = self.module.sha256_file(proto_file)

        # 7. Protocol doc
        doc_file = self.root / self.module.PROTOCOL_DOC_REL
        doc_file.parent.mkdir(parents=True, exist_ok=True)
        doc_file.write_text(
            f"Audience: project owner\n\n## In plain language\nProtocol {proto_sha}\n",
            encoding="utf-8",
        )

        commit_all(self.root, "setup protocol test")

        patcher = mock.patch.object(self.module, "REPO_ROOT", self.root)
        patcher.start()
        self.addCleanup(patcher.stop)

    def test_committed_protocol_with_current_digests_passes(self):
        code, out, err = run_main(self.module, ["protocol"])
        self.assertEqual(code, 0, f"stderr: {err}")
        self.assertIn("PROTOCOL-OK", out)

    def test_changed_pinned_file_fails(self):
        pinned = self.root / self.module.PINNED_MODULES[0]
        pinned.write_bytes(b"# modified\n")
        commit_all(self.root, "modify pinned")
        code, out, err = run_main(self.module, ["protocol"])
        self.assertEqual(code, 1)
        self.assertIn("FAIL-CLOSED", err)

    def test_untracked_or_dirty_protocol_fails(self):
        proto_file = self.root / self.module.PROTOCOL_REL
        proto_file.write_text('{"dirty": true}\n', encoding="utf-8")
        code, out, err = run_main(self.module, ["protocol"])
        self.assertEqual(code, 1)
        self.assertIn("FAIL-CLOSED", err)

    def test_scorer_digest_unequal_to_successor_fails(self):
        scorer_file = self.root / self.module.SCORER_REL
        scorer_file.write_bytes(b"# modified scorer\n")
        commit_all(self.root, "modify scorer")
        code, out, err = run_main(self.module, ["protocol"])
        self.assertEqual(code, 1)
        self.assertIn("FAIL-CLOSED", err)

    def test_amendment_commit_not_an_ancestor_fails(self):
        proto_file = self.root / self.module.PROTOCOL_REL
        data = json.loads(proto_file.read_text(encoding="utf-8"))
        data["amendment_commit"] = "a" * 40
        proto_file.write_text(json.dumps(data) + "\n", encoding="utf-8")
        commit_all(self.root, "bad amendment commit")
        code, out, err = run_main(self.module, ["protocol"])
        self.assertEqual(code, 1)
        self.assertIn("FAIL-CLOSED", err)

    def test_protocol_doc_missing_sha_fails(self):
        doc_file = self.root / self.module.PROTOCOL_DOC_REL
        doc_file.write_text("Audience: owner\n\n## In plain language\nNo sha here\n", encoding="utf-8")
        commit_all(self.root, "strip sha from doc")
        code, out, err = run_main(self.module, ["protocol"])
        self.assertEqual(code, 1)
        self.assertIn("FAIL-CLOSED", err)


class PreflightCheckTests(unittest.TestCase):
    def setUp(self):
        self.module = load_verifier()
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        self.root = Path(self.temp_dir.name)
        init_repo(self.root)

        self.expected_keys = {
            "hierarchical/gold/1632": 1001,
            "hierarchical/gold/851": 1001,
            "hierarchical/gold/4658": 1001,
            "hierarchical/base/1632": 126,
            "hierarchical/base/851": 126,
            "hierarchical/base/4658": 126,
            "standard/gold/2279": 1001,
            "standard/gold/3418": 1001,
            "standard/base/2279": 59,
            "standard/base/3418": 59,
        }
        self.preflight_file = self.root / self.module.PREFLIGHT_REL
        self.preflight_file.parent.mkdir(parents=True, exist_ok=True)
        self._write_valid_preflight()
        commit_all(self.root, "setup preflight test")

        patcher = mock.patch.object(self.module, "REPO_ROOT", self.root)
        patcher.start()
        self.addCleanup(patcher.stop)

    def _write_valid_preflight(self, **updates):
        records = {}
        for k, count in self.expected_keys.items():
            records[k] = {
                "status": "ok",
                "n_within_t": count,
                "expected_within_t": count,
                "count_ok": True,
            }
        payload = {
            "schema": self.module.PREFLIGHT_SCHEMA,
            "records": records,
            "attestation": {
                "test_split_opened": 0,
                "blocked_attempts": 0,
                "refused_before_open": 0,
            },
        }
        payload.update(updates)
        self.preflight_file.write_text(json.dumps(payload) + "\n", encoding="utf-8")

    def test_valid_preflight_passes(self):
        code, out, err = run_main(self.module, ["preflight"])
        self.assertEqual(code, 0, f"stderr: {err}")
        self.assertIn("PREFLIGHT-OK", out)

    def test_nonzero_attestation_counter_fails(self):
        self._write_valid_preflight(attestation={"test_split_opened": 1, "blocked_attempts": 0, "refused_before_open": 0})
        commit_all(self.root, "bad counter")
        code, out, err = run_main(self.module, ["preflight"])
        self.assertEqual(code, 1)
        self.assertIn("FAIL-CLOSED", err)

    def test_missing_key_fails(self):
        records = {k: {"status": "ok", "n_within_t": c, "count_ok": True} for k, c in list(self.expected_keys.items())[:-1]}
        self._write_valid_preflight(records=records)
        commit_all(self.root, "missing key")
        code, out, err = run_main(self.module, ["preflight"])
        self.assertEqual(code, 1)
        self.assertIn("FAIL-CLOSED", err)

    def test_count_mismatch_fails(self):
        records = {}
        for k, count in self.expected_keys.items():
            records[k] = {"status": "ok", "n_within_t": count if "gold" not in k else count - 1, "count_ok": True}
        self._write_valid_preflight(records=records)
        commit_all(self.root, "count mismatch")
        code, out, err = run_main(self.module, ["preflight"])
        self.assertEqual(code, 1)
        self.assertIn("FAIL-CLOSED", err)

    def test_unredacted_home_directory_fails(self):
        payload = json.loads(self.preflight_file.read_text(encoding="utf-8"))
        payload["leaked_path"] = str(Path.home()) + "/data"
        self.preflight_file.write_text(json.dumps(payload) + "\n", encoding="utf-8")
        commit_all(self.root, "unredacted home")
        code, out, err = run_main(self.module, ["preflight"])
        self.assertEqual(code, 1)
        self.assertIn("FAIL-CLOSED", err)


class RecordsCheckTests(unittest.TestCase):
    def setUp(self):
        self.module = load_verifier()
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        self.root = Path(self.temp_dir.name)
        init_repo(self.root)

        # Protocol file
        proto_file = self.root / self.module.PROTOCOL_REL
        proto_file.parent.mkdir(parents=True, exist_ok=True)
        proto_file.write_text('{"schema": "phase60-run-protocol/v1"}\n', encoding="utf-8")
        self.protocol_sha = self.module.sha256_file(proto_file)

        # Scorer successor
        succ_file = self.root / self.module.SCORER_SUCCESSOR_REL
        succ_file.parent.mkdir(parents=True, exist_ok=True)
        self.scorer_sha = "1" * 64
        succ_file.write_text(json.dumps({"successor_sha256": self.scorer_sha}) + "\n", encoding="utf-8")

        # Create one valid real arm record
        self.arm_dir = self.root / self.module.EVIDENCE_REL / "arms" / "r1-1632"
        self.arm_dir.mkdir(parents=True, exist_ok=True)

        model = build_network(ArchitectureSpec(seed=SEED), dtype=torch.float32, device="cpu")
        state_dict = OrderedDict((k, v.detach().clone()) for k, v in model.state_dict().items())
        adam_path = self.arm_dir / "adam.weights"
        polish_path = self.arm_dir / "polish.weights"
        atomic_write_torch(adam_path, state_dict)
        atomic_write_torch(polish_path, state_dict)

        self.adam_sha = self.module.sha256_file(adam_path)
        self.polish_sha = self.module.sha256_file(polish_path)
        self.adam_digest = self.module.weights_digest(state_dict)
        self.polish_digest = self.module.weights_digest(state_dict)

        self.valid_record = {
            "schema": "phase60-run-record/v1",
            "diagnostic": True,
            "run_kind": "real",
            "arm_id": "r1-1632",
            "loss_arm": "data_only",
            "counted": True,
            "seed": 42,
            "first_omega_0": 30.0,
            "runtime": {"dtype": "float32", "device": "mps"},
            "versions": {"torch": "2.12.1", "numpy": "1.26.4", "python": "3.11.9", "macos": "14.5"},
            "code": {"git_head": "0" * 40, "dirty_pinn_paths": []},
            "config_sha256": "0" * 64,
            "scorecard_sha256": SCORECARD_SHA256,
            "scorer_sha256": self.scorer_sha,
            "protocol_sha256": self.protocol_sha,
            "module_sha256": {},
            "normalizer": {"stats_sha256": "0" * 64},
            "attestation": {"test_split_opened": 0, "blocked_attempts": 0, "refused_before_open": 0},
            "timing": {"seconds_per_step": 0.01},
            "budget": {
                "rule": "frozen",
                "budget_steps": 1000,
                "reading_steps": [50, 100],
                "readings": [],
                "outcome": "complete",
                "extended": False,
            },
            "trace": [],
            "states": {
                "adam": {
                    "score_gold": {"tier": 1, "E": 0.05, "eps_h": 1e-4},
                    "score_base": {"tier": 1, "E": 0.05, "eps_h": 1e-4},
                    "cross_check": {"tier": 1, "E": 0.05, "eps_h": 1e-4},
                    "weights": {"file": "adam.weights", "sha256": self.adam_sha, "tensor_digest": self.adam_digest},
                },
                "polish": {
                    "score_gold": {"tier": 1, "E": 0.04, "eps_h": 1e-4},
                    "score_base": {"tier": 1, "E": 0.04, "eps_h": 1e-4},
                    "cross_check": {"tier": 1, "E": 0.04, "eps_h": 1e-4},
                    "weights": {"file": "polish.weights", "sha256": self.polish_sha, "tensor_digest": self.polish_digest},
                },
            },
            "better_state": "polish",
            "result": {"state": "polish", "tier": 1, "E": 0.04, "e_in_max": 0.02, "h": 1e-4, "eps_h": 1e-4},
            "formula": {"E_formula": 0.1, "counts": True},
            "wall": {"hours": 0.5},
        }
        (self.arm_dir / "record.json").write_text(json.dumps(self.valid_record) + "\n", encoding="utf-8")
        commit_all(self.root, "setup arm records")

        patcher = mock.patch.object(self.module, "REPO_ROOT", self.root)
        patcher.start()
        self.addCleanup(patcher.stop)

    def test_valid_record_passes(self):
        code, out, err = run_main(self.module, ["records"])
        self.assertEqual(code, 0, f"stderr: {err}")
        self.assertIn("RECORDS-OK", out)

    def test_seed_mismatch_fails(self):
        rec = dict(self.valid_record)
        rec["seed"] = 41
        (self.arm_dir / "record.json").write_text(json.dumps(rec) + "\n", encoding="utf-8")
        commit_all(self.root, "bad seed")
        code, out, err = run_main(self.module, ["records"])
        self.assertEqual(code, 1)
        self.assertIn("FAIL-CLOSED", err)

    def test_runtime_cpu_fails(self):
        rec = dict(self.valid_record)
        rec["runtime"] = {"dtype": "float32", "device": "cpu"}
        (self.arm_dir / "record.json").write_text(json.dumps(rec) + "\n", encoding="utf-8")
        commit_all(self.root, "bad device")
        code, out, err = run_main(self.module, ["records"])
        self.assertEqual(code, 1)
        self.assertIn("FAIL-CLOSED", err)

    def test_weights_sha_mismatch_fails(self):
        (self.arm_dir / "adam.weights").write_bytes(b"corrupted\n")
        commit_all(self.root, "corrupt weights")
        code, out, err = run_main(self.module, ["records"])
        self.assertEqual(code, 1)
        self.assertIn("FAIL-CLOSED", err)

    def test_owner_stop_without_record_reports_owner_stop(self):
        stop_arm = self.root / self.module.EVIDENCE_REL / "arms" / "r1-851"
        stop_arm.mkdir(parents=True, exist_ok=True)
        (stop_arm / "owner-stop.json").write_text('{"reason": "halt"}\n', encoding="utf-8")
        code, out, err = run_main(self.module, ["records"])
        self.assertEqual(code, 1)
        self.assertIn("OWNER-STOP r1-851", out)


class G2CheckTests(unittest.TestCase):
    def setUp(self):
        self.module = load_verifier()
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        self.root = Path(self.temp_dir.name)
        init_repo(self.root)

        # Arms for 1632, 851, 4658
        self.arms_dir = self.root / self.module.EVIDENCE_REL / "arms"
        self.g2_dir = self.root / self.module.EVIDENCE_REL / "g2"
        self.g2_dir.mkdir(parents=True, exist_ok=True)

        for s, tier in [(1632, 0), (851, 0), (4658, 1)]:
            d = self.arms_dir / f"r1-{s}"
            d.mkdir(parents=True, exist_ok=True)
            rec = {"arm_id": f"r1-{s}", "result": {"tier": tier, "E": 0.2 if tier == 0 else 0.05}}
            (d / "record.json").write_text(json.dumps(rec) + "\n", encoding="utf-8")

        self.outcome_payload = {
            "schema": self.module.OUTCOME_SCHEMA,
            "g2_fired": True,
            "sweep_system": 1632,
            "confirmation_system": 851,
            "uncovered_system": 4658,
        }
        (self.g2_dir / "g2-outcome.json").write_text(json.dumps(self.outcome_payload) + "\n", encoding="utf-8")
        commit_all(self.root, "setup g2 tests")

        patcher = mock.patch.object(self.module, "REPO_ROOT", self.root)
        patcher.start()
        self.addCleanup(patcher.stop)

    def test_g2_outcome_matches_recomputed_tiers(self):
        code, out, err = run_main(self.module, ["g2", "--require", "outcome"])
        self.assertEqual(code, 0, f"stderr: {err}")
        self.assertIn("G2-OK", out)

    def test_g2_outcome_mismatch_fails(self):
        # Change tier of 851 to 1 so tiers are (0, 1, 1) -> g2_fired should be False
        d = self.arms_dir / "r1-851"
        rec = {"arm_id": "r1-851", "result": {"tier": 1, "E": 0.05}}
        (d / "record.json").write_text(json.dumps(rec) + "\n", encoding="utf-8")
        commit_all(self.root, "update tier")
        code, out, err = run_main(self.module, ["g2", "--require", "outcome"])
        self.assertEqual(code, 1)
        self.assertIn("FAIL-CLOSED", err)

    def test_skip_records_with_invalid_reason_fails(self):
        skip_file = self.g2_dir / "skip-records.json"
        skip_file.write_text(json.dumps({"schema": self.module.SKIP_SCHEMA, "reason": "unauthorized reason"}) + "\n", encoding="utf-8")
        commit_all(self.root, "bad skip reason")
        code, out, err = run_main(self.module, ["g2", "--require", "outcome,skip-records"])
        self.assertEqual(code, 1)
        self.assertIn("FAIL-CLOSED", err)

    def test_skip_records_beside_rung2_arm_fails(self):
        skip_file = self.g2_dir / "skip-records.json"
        skip_file.write_text(json.dumps({"schema": self.module.SKIP_SCHEMA, "reason": "no rescue"}) + "\n", encoding="utf-8")
        r2b_dir = self.arms_dir / "r2b-1632"
        r2b_dir.mkdir(parents=True, exist_ok=True)
        commit_all(self.root, "add r2b arm beside skip")
        code, out, err = run_main(self.module, ["g2", "--require", "outcome,skip-records"])
        self.assertEqual(code, 1)
        self.assertIn("FAIL-CLOSED", err)

    def commit_sweep(self, tiers, confirmed):
        # Four committed sweep arms of system 1632 (first_omega_0 60, 120, 240, 480) and a curve naming `confirmed`.
        for omega, tier in zip((60, 120, 240, 480), tiers):
            d = self.arms_dir / f"g2s-1632-w{omega:03d}"
            d.mkdir(parents=True, exist_ok=True)
            rec = {"arm_id": d.name, "result": {"tier": tier, "E": 0.2 if tier == 0 else 0.05}}
            (d / "record.json").write_text(json.dumps(rec) + "\n", encoding="utf-8")
        curve = {
            "schema": self.module.CURVE_SCHEMA,
            "sweep_system": 1632,
            "confirmed_first_omega_0": confirmed,
        }
        (self.g2_dir / "sweep-curve.json").write_text(json.dumps(curve) + "\n", encoding="utf-8")
        commit_all(self.root, "add the sweep arms and the sweep curve")

    # The curve check recomputes the confirmed setting from the four sweep records. It only runs
    # when all four are committed, which no test built before these three.
    def test_sweep_curve_with_no_tier_one_setting_confirms_none(self):
        self.commit_sweep((0, 0, 0, 0), None)
        code, out, err = run_main(self.module, ["g2", "--require", "outcome,sweep-curve"])
        self.assertEqual(code, 0, f"stderr: {err}")
        self.assertIn("G2-OK", out)

    def test_sweep_curve_confirmed_setting_mismatch_fails(self):
        # Negative control: no setting reached Tier 1, so a curve that confirms 240.0 is wrong.
        self.commit_sweep((0, 0, 0, 0), 240.0)
        code, out, err = run_main(self.module, ["g2", "--require", "outcome,sweep-curve"])
        self.assertEqual(code, 1)
        self.assertIn("confirmed_first_omega_0 mismatch", err)
        self.assertNotIn("G2-OK", out)

    def test_sweep_curve_confirms_the_highest_tier_one_setting(self):
        # Tiers 0 1 1 0: the highest setting at Tier 1 or better is 240.0 (neither the lowest, 120.0, nor the top of the grid, 480.0).
        self.commit_sweep((0, 1, 1, 0), 240.0)
        code, out, err = run_main(self.module, ["g2", "--require", "outcome,sweep-curve"])
        self.assertEqual(code, 0, f"stderr: {err}")
        self.assertIn("G2-OK", out)


class G2TokenTests(unittest.TestCase):
    def setUp(self):
        self.module = load_verifier()
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        self.root = Path(self.temp_dir.name)
        init_repo(self.root)

        self.arms_dir = self.root / self.module.EVIDENCE_REL / "arms"
        self.g2_dir = self.root / self.module.EVIDENCE_REL / "g2"
        self.g2_dir.mkdir(parents=True, exist_ok=True)

        for s, tier in [(1632, 0), (851, 0), (4658, 1)]:
            d = self.arms_dir / f"r1-{s}"
            d.mkdir(parents=True, exist_ok=True)
            rec = {"arm_id": f"r1-{s}", "result": {"tier": tier, "E": 0.2 if tier == 0 else 0.05}}
            (d / "record.json").write_text(json.dumps(rec) + "\n", encoding="utf-8")

        self.outcome_payload = {
            "schema": self.module.OUTCOME_SCHEMA,
            "g2_fired": True,
            "sweep_system": 1632,
            "confirmation_system": 851,
            "uncovered_system": 4658,
        }
        (self.g2_dir / "g2-outcome.json").write_text(json.dumps(self.outcome_payload) + "\n", encoding="utf-8")
        commit_all(self.root, "setup tokens test")

        patcher = mock.patch.object(self.module, "REPO_ROOT", self.root)
        patcher.start()
        self.addCleanup(patcher.stop)

    def test_fired_tree_token_behavior(self):
        code, out, err = run_main(self.module, ["g2", "--require", "outcome"])
        self.assertEqual(code, 0)
        self.assertIn("G2-OK", out)

        code, out, err = run_main(self.module, ["g2", "--require", "outcome,sweep-curve"])
        self.assertEqual(code, 1)
        self.assertIn("sweep-curve.json", err)

        code, out, err = run_main(self.module, ["g2"])
        self.assertEqual(code, 1)
        self.assertIn("sweep-curve.json", err)

    def test_not_fired_tree_no_require_default(self):
        # Update tiers to (1, 1, 1) and g2_fired: False
        for s in (1632, 851, 4658):
            d = self.arms_dir / f"r1-{s}"
            rec = {"arm_id": f"r1-{s}", "result": {"tier": 1, "E": 0.05}}
            (d / "record.json").write_text(json.dumps(rec) + "\n", encoding="utf-8")
        (self.g2_dir / "g2-outcome.json").write_text(
            json.dumps({"schema": self.module.OUTCOME_SCHEMA, "g2_fired": False}) + "\n",
            encoding="utf-8",
        )
        commit_all(self.root, "g2 not fired")
        code, out, err = run_main(self.module, ["g2"])
        self.assertEqual(code, 0)
        self.assertIn("G2-OK", out)

        # Adding sweep-curve.json to not-fired tree makes default g2 fail
        (self.g2_dir / "sweep-curve.json").write_text('{"schema": "phase60-sweep-curve/v1"}\n', encoding="utf-8")
        commit_all(self.root, "unexpected sweep-curve")
        code, out, err = run_main(self.module, ["g2"])
        self.assertEqual(code, 1)
        self.assertIn("unexpected g2 file sweep-curve.json", err)

    def test_invalid_tokens_fail_closed(self):
        for bad_req in ("sweepcurve", "outcome,outcome", "", "outcome,,rescue"):
            code, out, err = run_main(self.module, ["g2", "--require", bad_req])
            self.assertEqual(code, 1, f"bad require {bad_req!r} did not exit 1")
            self.assertIn("FAIL-CLOSED", err)
            self.assertNotIn("G2-OK", out)


class RescoreTests(unittest.TestCase):
    def setUp(self):
        self.module = load_verifier()
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        self.root = Path(self.temp_dir.name)
        init_repo(self.root)

        self.arm_dir = self.root / self.module.EVIDENCE_REL / "arms" / "r1-1632"
        self.arm_dir.mkdir(parents=True, exist_ok=True)

        model = build_network(ArchitectureSpec(seed=SEED), dtype=torch.float32, device="cpu")
        state_dict = OrderedDict((k, v.detach().clone()) for k, v in model.state_dict().items())
        adam_path = self.arm_dir / "adam.weights"
        polish_path = self.arm_dir / "polish.weights"
        atomic_write_torch(adam_path, state_dict)
        atomic_write_torch(polish_path, state_dict)

        adam_sha = self.module.sha256_file(adam_path)
        polish_sha = self.module.sha256_file(polish_path)
        adam_digest = self.module.weights_digest(state_dict)
        polish_digest = self.module.weights_digest(state_dict)

        self.record = {
            "schema": "phase60-run-record/v1",
            "arm_id": "r1-1632",
            "first_omega_0": 30.0,
            "better_state": "polish",
            "states": {
                "adam": {
                    "score_gold": {"tier": 1, "E": 0.05, "eps_h": 1e-4},
                    "cross_check": {"tier": 1, "E": 0.05, "eps_h": 1e-4},
                    "weights": {"file": "adam.weights", "sha256": adam_sha, "tensor_digest": adam_digest},
                },
                "polish": {
                    "score_gold": {"tier": 1, "E": 0.05, "eps_h": 1e-4},
                    "cross_check": {"tier": 1, "E": 0.05, "eps_h": 1e-4},
                    "weights": {"file": "polish.weights", "sha256": polish_sha, "tensor_digest": polish_digest},
                },
            },
            "formula": {"E_formula": 0.1, "counts": True},
        }
        (self.arm_dir / "record.json").write_text(json.dumps(self.record) + "\n", encoding="utf-8")
        commit_all(self.root, "setup rescore test")

        patcher = mock.patch.object(self.module, "REPO_ROOT", self.root)
        patcher.start()
        self.addCleanup(patcher.stop)

    def test_rescore_cpu_only_passes_and_fails_on_weight_tampering(self):
        with mock.patch.object(self.module, "open_real_context") as mock_ctx, \
             mock.patch.object(self.module, "load_arm_data") as mock_load_data, \
             mock.patch.object(self.module, "score_network") as mock_score:
            mock_ctx.return_value.__enter__.return_value = SimpleNamespace(
                opened=SimpleNamespace(test_split_opened=0)
            )
            mock_load_data.return_value = SimpleNamespace(
                ic13=torch.zeros((1, 13)),
                masses=torch.ones((1, 3)),
                score=SimpleNamespace(
                    positions=torch.zeros((10, 9)),
                    inner_pair=torch.zeros((10, 3)),
                    times=torch.zeros((10, 1)),
                    grid="gold",
                ),
            )
            mock_score.return_value = SimpleNamespace(tier=1, E=0.05, eps_h=1e-4)

            code, out, err = run_main(self.module, ["rescore", "--cpu-only"])
            self.assertEqual(code, 0, f"stderr: {err}")
            self.assertIn("RESCORE-OK", out)

            # Corrupt one byte of weights file
            (self.arm_dir / "adam.weights").write_bytes(b"tampered weights\n")
            commit_all(self.root, "tamper weights")
            code, out, err = run_main(self.module, ["rescore", "--cpu-only"])
            self.assertEqual(code, 1)
            self.assertIn("FAIL-CLOSED", err)


if __name__ == "__main__":
    unittest.main()
