"""Phase 68: Yardstick audit unit and synthetic tracer tests.

Tests the guarded audit_pair function and pre-open admission rules using a
controlled TinyCorpus fixture. Proves that:
1. One temporary hierarchical pair is admitted before opening its two files.
2. Four prediction/grid groups traverse the actual functions and retain separate identities.
3. Reference-to-reference position errors are exactly zero.
4. The constant has its own finite nonzero H(0), zero energy drift and SCS -infinity despite nonzero position error.
5. The fixture tests show no validation/test open and pre-path refusal for other keys.
"""

from __future__ import annotations

import hashlib
import json
import math
import tempfile
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from types import SimpleNamespace

import numpy as np
import torch

import pinn.data.splits as splits_module
from pinn.data.splits import SplitManifest, SplitRatios
from pinn.data.types import RecordKey
from pinn.training.validation_gate import json_safe_float
from pinn.verification import split_allowlist
from pinn.verification.diagnostic_data import (
    Stage0TrainingReader,
    Stage0TrainingRefused,
)
from pinn.verification.evidence_io import canonical_json_bytes
from pinn.verification.feasibility_scorecard import load_scorecard
from pinn.verification.gate_metrics import (
    EPS_INV,
    aggregate_gate_verdict,
    scs_from_eps_h,
)
from pinn.verification.split_allowlist import (
    SplitAllowlist,
    SplitRefused,
    install_open_attestation,
)
from pinn.verification.yardstick_audit import (
    FIXED_PANEL_SYSTEM_IDS,
    SCHEMA_VERSION,
    YardstickAuditError,
    array_digest,
    audit_pair,
    compute_fd_metrics,
    compute_fd_metrics_float32_input,
)
from tests.phase39._fixtures import HIER_MASSES, TinyCorpus, write_brutus


def _manifest_group(variant, identifier, split, base_stage, *, with_gold=True):
    records = [
        {"variant": variant, "fidelity": "base", "id": identifier, "stage": base_stage}
    ]
    signature = {
        "variant": variant,
        "base_stage": base_stage,
        "gold_stage": "UNASSIGNED" if with_gold else "MISSING_GOLD",
    }
    if with_gold:
        records.append(
            {"variant": variant, "fidelity": "gold", "id": identifier, "stage": "UNASSIGNED"}
        )
    return {
        "physical_key": {"variant": variant, "id": identifier},
        "signature": signature,
        "split": split,
        "records": records,
    }


def _summary_for(signature, groups, ratios):
    from collections import Counter

    names = ("train", "validation", "test")
    counts = Counter(group["split"] for group in groups
                     if group["signature"] == signature)
    size = sum(counts.values())
    quotas, expected = splits_module._hamilton_counts(size, ratios)
    quota = {name: float(value) for name, value in zip(names, quotas)}
    deviations = tuple(
        {
            "split": name,
            "quota": quota[name],
            "count": int(expected[index]),
            "delta": float(splits_module.Decimal(expected[index]) - quotas[index]),
        }
        for index, name in enumerate(names)
        if splits_module.Decimal(expected[index]) != quotas[index]
    )
    return {
        "signature": signature,
        "quota": quota,
        "counts": {name: int(expected[index]) for index, name in enumerate(names)},
        "deviations": list(deviations),
    }


class YardstickAuditTracerTests(unittest.TestCase):
    """Test audit_pair with a synthetic TinyCorpus fixture."""

    def setUp(self):
        self.tmp_dir = TemporaryDirectory(prefix="phase68-test-")
        self.corpus = TinyCorpus()
        tmp_path = Path(self.tmp_dir.name)

        # Build nested schedules for id 7:
        # Base: 11 snapshots t = 0..10 in steps of 1.0
        # Gold: 101 snapshots t = 0..10 in steps of 0.1
        # Every base time is an exact gold time!
        base_times = [round(i * 1.0, 6) for i in range(11)]
        gold_times = [round(i * 0.1, 6) for i in range(101)]

        base_brutus_path = self.corpus._brutus_path("brutus_hierarchical", "hierarchical", 7)
        gold_brutus_path = self.corpus._brutus_path("brutus_hierarchical_gold_standard", "hierarchical", 7)

        write_brutus(base_brutus_path, base_times, HIER_MASSES)
        write_brutus(gold_brutus_path, gold_times, HIER_MASSES)

        # Build custom split manifest
        groups = [
            _manifest_group("hierarchical", 7, "train", 0, with_gold=True),
            _manifest_group("hierarchical", 200, "validation", 0, with_gold=True),
            _manifest_group("hierarchical", 201, "test", 0, with_gold=True),
            _manifest_group("hierarchical", 42, "train", 1, with_gold=True),
            _manifest_group("standard", 0, "train", "UNASSIGNED", with_gold=True),
        ]
        ratios = SplitRatios()
        signatures = [
            _summary_for(
                {"variant": "hierarchical", "base_stage": 0, "gold_stage": "UNASSIGNED"},
                groups, ratios
            ),
            _summary_for(
                {"variant": "hierarchical", "base_stage": 1, "gold_stage": "UNASSIGNED"},
                groups, ratios
            ),
            _summary_for(
                {"variant": "standard", "base_stage": "UNASSIGNED", "gold_stage": "UNASSIGNED"},
                groups, ratios
            ),
        ]
        payload = {
            "schema_version": 1,
            "algorithm": "group-signature-hamilton-v1",
            "tie_order": ["train", "validation", "test"],
            "seed": 42,
            "ratios": ratios.as_dict(),
            "signatures": signatures,
            "groups": groups,
        }
        manifest_raw = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
        manifest_path = tmp_path / "splits.json"
        manifest_path.write_bytes(manifest_raw)

        self.allowlist = SplitAllowlist.from_manifest(
            manifest_path,
            expected_sha256=hashlib.sha256(manifest_raw).hexdigest(),
        )

        split_allowlist._ATTESTATION = None
        split_allowlist._ATTESTATION_ROOT = None
        self.attestation = install_open_attestation(
            data_root=self.corpus.data_root,
            data_root_source="fixture",
            withheld_basenames=self.allowlist.withheld_basenames(),
            split_by_basename=self.allowlist.split_by_basename(),
        )
        self.reader = Stage0TrainingReader(
            allowlist=self.allowlist,
            data_root=self.corpus.data_root,
            data_root_source="fixture",
            blacklist_path=self.corpus.blacklist_path,
        )
        self.scorecard = load_scorecard()

    def tearDown(self):
        split_allowlist._ATTESTATION = None
        split_allowlist._ATTESTATION_ROOT = None
        self.corpus._tmp.cleanup()
        self.tmp_dir.cleanup()

    def test_refusals_before_path_resolution(self):
        """Non-Stage-0 TRAIN keys refuse before path resolution, with no files opened."""
        val_key = RecordKey("hierarchical", "base", 200)
        test_key = RecordKey("hierarchical", "base", 201)
        stage1_key = RecordKey("hierarchical", "base", 42)
        std_key = RecordKey("standard", "base", 0)
        unknown_key = RecordKey("hierarchical", "base", 9999)

        initial_opens = len(self.reader._stage0_opened)
        self.assertEqual(initial_opens, 0)

        # Validation and stage-1 keys pass allowlist.require() then raise Stage0TrainingRefused
        with self.assertRaises(Stage0TrainingRefused):
            self.reader.read(val_key)
        with self.assertRaises(Stage0TrainingRefused):
            self.reader.read(stage1_key)

        # Withheld, standard, and unknown keys raise SplitRefused before path
        with self.assertRaises(SplitRefused):
            self.reader.read(test_key)
        with self.assertRaises(SplitRefused):
            self.reader.read(std_key)
        with self.assertRaises(SplitRefused):
            self.reader.read(unknown_key)

        # Confirm zero actual opens occurred during refused calls
        self.assertEqual(len(self.reader._stage0_opened), 0)
        self.assertEqual(self.reader._stage0_refusals, 5)

    def test_synthetic_pair_tracer(self):
        """Synthetic hierarchical pair executes end-to-end and satisfies all acceptance criteria."""
        base_key = RecordKey("hierarchical", "base", 7)
        gold_key = RecordKey("hierarchical", "gold", 7)

        result = audit_pair(self.reader, base_key, gold_key, scorecard=self.scorecard)
        self.assertIn("record_info", result)
        self.assertIn("rows", result)

        rec_info = result["record_info"]
        self.assertEqual(rec_info["system_id"], 7)
        self.assertEqual(rec_info["split"], "train")
        self.assertEqual(rec_info["physical_stage"], 0)
        self.assertTrue(rec_info["gold_base_agreement"]["passed"])
        self.assertLessEqual(
            rec_info["gold_base_agreement"]["deviation"],
            rec_info["gold_base_agreement"]["tolerance"],
        )

        rows = result["rows"]
        # Exactly 4 rows: base brutus, base constant, gold brutus, gold constant
        self.assertEqual(len(rows), 4)

        base_brutus = rows[0]
        base_constant = rows[1]
        gold_brutus = rows[2]
        gold_constant = rows[3]

        # 1. Distinct identity
        self.assertEqual(base_brutus["grid"], "base")
        self.assertEqual(base_brutus["prediction"], "brutus")
        self.assertEqual(base_constant["grid"], "base")
        self.assertEqual(base_constant["prediction"], "window_mean_constant")
        self.assertEqual(gold_brutus["grid"], "gold")
        self.assertEqual(gold_brutus["prediction"], "brutus")
        self.assertEqual(gold_constant["grid"], "gold")
        self.assertEqual(gold_constant["prediction"], "window_mean_constant")

        # 2. Reference-to-reference position errors are exactly zero
        self.assertEqual(base_brutus["feas01"]["E"], 0.0)
        self.assertEqual(base_brutus["feas01"]["e_sys_max"], 0.0)
        self.assertEqual(base_brutus["feas01"]["e_in_max"], 0.0)

        self.assertEqual(gold_brutus["feas01"]["E"], 0.0)
        self.assertEqual(gold_brutus["feas01"]["e_sys_max"], 0.0)
        self.assertEqual(gold_brutus["feas01"]["e_in_max"], 0.0)

        # 3. Constant predictor has finite nonzero H(0), zero energy drift, and SCS -infinity despite E > 0
        for const_row in (base_constant, gold_constant):
            with self.subTest(grid=const_row["grid"]):
                self.assertGreater(const_row["feas01"]["E"], 0.0)
                # Check gate_fd_native
                native_fd = const_row["gate_fd_native"]
                self.assertEqual(native_fd["eps_h"], 0.0)
                self.assertEqual(native_fd["scs"], "-Infinity")
                self.assertEqual(native_fd["verdict"], "PASS")
                self.assertNotEqual(native_fd["h0"], 0.0)
                self.assertTrue(math.isfinite(float(native_fd["h0"])))
                self.assertEqual(native_fd["peak_abs_change"], 0.0)

                # Check gate_fd_float32_input
                f32_fd = const_row["gate_fd_float32_input"]
                self.assertEqual(f32_fd["eps_h"], 0.0)
                self.assertEqual(f32_fd["scs"], "-Infinity")
                self.assertEqual(f32_fd["verdict"], "PASS")

        # 4. Reader access checks: exactly 2 files opened (base and gold for id 7)
        access = self.reader.access_summary()
        self.assertEqual(access["actual_opens"], 2)
        opened_keys = [entry["record_key"] for entry in access["opened"]]
        self.assertIn("hierarchical/base/7", opened_keys)
        self.assertIn("hierarchical/gold/7", opened_keys)

        # Attestation check: exactly 2 train opens, 0 validation opens, 0 test opens
        attest_summary = self.attestation.summary()
        self.assertEqual(attest_summary["opened"]["train"], 2)
        self.assertEqual(attest_summary["opened"]["validation"], 0)
        self.assertEqual(attest_summary["test_split_opened"], 0)
        self.assertEqual(attest_summary["blocked_attempts"], 0)


class YardstickHelperUnitTests(unittest.TestCase):
    """Unit tests for array digests, FD metrics, and edge cases."""

    def test_array_digest_deterministic(self):
        arr1 = np.array([1.0, 2.0, 3.0], dtype=np.float64)
        arr2 = np.array([1.0, 2.0, 3.0], dtype=np.float64)
        d1 = array_digest(arr1)
        d2 = array_digest(arr2)
        self.assertEqual(d1["sha256"], d2["sha256"])
        self.assertEqual(d1["shape"], [3])
        self.assertEqual(d1["dtype"], "<f8")

        arr3 = np.array([1.0, 2.0, 3.0000000001], dtype=np.float64)
        self.assertNotEqual(d1["sha256"], array_digest(arr3)["sha256"])

    def test_compute_fd_metrics_constant_motion(self):
        # A 3-body system held at fixed positions: velocity is 0, drift is 0
        times = np.array([0.0, 1.0, 2.0, 3.0], dtype=np.float64)
        positions = np.zeros((4, 3, 3), dtype=np.float64)
        positions[:, 0, :] = [1.0, 0.0, 0.0]
        positions[:, 1, :] = [-1.0, 0.0, 0.0]
        positions[:, 2, :] = [0.0, 1.0, 0.0]
        masses = np.array([1.0, 1.0, 1.0], dtype=np.float64)

        fd = compute_fd_metrics(positions, times, masses)
        self.assertEqual(fd["eps_h"], 0.0)
        self.assertEqual(fd["scs"], "-Infinity")
        self.assertEqual(fd["verdict"], "PASS")
        self.assertNotEqual(fd["h0"], 0.0)
        self.assertTrue(math.isfinite(float(fd["h0"])))
        self.assertEqual(fd["peak_abs_change"], 0.0)

    def test_scs_zero_drift_vs_nan(self):
        self.assertEqual(json_safe_float(scs_from_eps_h(0.0)), "-Infinity")
        self.assertEqual(json_safe_float(scs_from_eps_h(float("nan"))), "NaN")
        self.assertEqual(json_safe_float(scs_from_eps_h(1e-5)), -5.0)


if __name__ == "__main__":
    unittest.main()
