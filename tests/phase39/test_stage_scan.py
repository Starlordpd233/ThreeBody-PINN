"""Phase 39 Plan 06 contract for the read-only Thrust-A population scan.

GAP-39-03 / GAP-39-08 and the authoritative CTL contract at lines 23-28 and
138-198 require one shared pre-residency classifier seam.  The report consumes
each admitted record's persisted ``stage_label``; only original/base
hierarchical Set 1a may be numeric, every gold record is ``UNASSIGNED``, and
strict ``s_min > s0`` excludes equality from Stage 0.

DATA-06 readiness is bound exclusively to the admitted/full Stage-0 count:
0 and 239 are fatal, 240 is nonfatal, and a diagnostic train-split count below
240 cannot create a second gate.
"""

from __future__ import annotations

import importlib
import importlib.util
import json
from pathlib import Path
from types import SimpleNamespace
import tempfile
import unittest
from unittest import mock

from pinn.data.stages import classify_stage_label
from pinn.data.types import (
    Fidelity,
    PhysicalKey,
    RecordKey,
    StageLabel,
    StageZeroUnderpopulated,
    Variant,
)
from tests.phase39 import _SKIP_PHRASE


STAGE_SCAN = "pinn.data.stage_scan"


def _require(symbol):
    try:
        module = importlib.import_module(STAGE_SCAN)
    except ImportError:
        raise unittest.SkipTest(f"{_SKIP_PHRASE} {STAGE_SCAN}.{symbol}")
    if not hasattr(module, symbol):
        raise unittest.SkipTest(f"{_SKIP_PHRASE} {STAGE_SCAN}.{symbol}")
    return getattr(module, symbol)


class _ReportSource:
    def __init__(self, records, *, interim_s0=0.01, data_root=None):
        self._records = tuple(records)
        self.classifier_interim_s0 = interim_s0
        self.data_root = data_root
        self.blacklisted_physical_keys = frozenset()
        self.gold_numeric_stage_count = 0
        self.folder_counts = {
            "brutus_hierarchical": {
                "found": len(self._records),
                "admitted": len(self._records),
                "rejected": 0,
                "quarantined": 0,
                "dropped_samples": 0,
            }
        }
        self._canonical_hash = "a" * 64

    def admitted_records(self):
        return self._records


class _Manifest:
    def __init__(self, records, train_physical_keys):
        self._train = frozenset(train_physical_keys)
        physical_keys = sorted({record.physical_key for record in records})
        self.groups = tuple(
            SimpleNamespace(
                physical_key=physical_key,
                split="train" if physical_key in self._train else "validation",
            )
            for physical_key in physical_keys
        )

    def physical_keys(self, split_name):
        if split_name == "train":
            return self._train
        return frozenset(
            group.physical_key
            for group in self.groups
            if group.split == split_name
        )


def _record(
    id_,
    *,
    variant="hierarchical",
    fidelity="base",
    label=StageLabel.STAGE_0,
    energy=-1.0,
    l_ratio=0.8,
    q=1.0,
    s_min=0.02,
    resident_bytes=64,
):
    key = RecordKey(variant, fidelity, id_)
    return SimpleNamespace(
        record_key=key,
        physical_key=key.physical_key,
        variant=Variant(variant),
        fidelity=Fidelity(fidelity),
        stage_label=label,
        E=energy,
        l_ratio=l_ratio,
        Q=q,
        min_separation=float(s_min),
        resident_bytes=resident_bytes,
    )


def _source(n_stage0, *, n_stage1=0, n_gold=0, n_standard=0, data_root=None):
    records = [
        _record(index, s_min=0.02 + index * 1e-6)
        for index in range(n_stage0)
    ]
    records.extend(
        _record(
            10_000 + index,
            label=StageLabel.STAGE_1,
            energy=-0.3,
            s_min=0.03 + index * 1e-6,
        )
        for index in range(n_stage1)
    )
    records.extend(
        _record(
            20_000 + index,
            fidelity="gold",
            label=StageLabel.UNASSIGNED,
            s_min=0.04 + index * 1e-6,
        )
        for index in range(n_gold)
    )
    records.extend(
        _record(
            30_000 + index,
            variant="standard",
            label=StageLabel.UNASSIGNED,
            s_min=0.05 + index * 1e-6,
        )
        for index in range(n_standard)
    )
    return _ReportSource(records, data_root=data_root)


class ProductionPresenceContract(unittest.TestCase):
    def test_stage_scan_module_exists(self):
        self.assertIsNotNone(
            importlib.util.find_spec(STAGE_SCAN),
            "Plan 39-06 must provide pinn.data.stage_scan",
        )


class PopulationReportContract(unittest.TestCase):
    def setUp(self):
        self.build = _require("build_population_report")

    def test_classifier_parity_includes_all_conjunct_near_miss_equality_and_gold(self):
        all_conjunct = _record(1, s_min=0.0100001)
        near_miss = _record(2, label=StageLabel.UNASSIGNED, q=1.300001)
        equality = _record(3, label=StageLabel.UNASSIGNED, s_min=0.01)
        gold = _record(1, fidelity="gold", label=StageLabel.UNASSIGNED)

        for record in (all_conjunct, near_miss, equality, gold):
            classifier_record = SimpleNamespace(
                variant=record.variant,
                fidelity=record.fidelity,
                E=record.E,
                l_ratio=record.l_ratio,
                Q=record.Q,
                s_min=record.min_separation,
            )
            self.assertIs(
                record.stage_label,
                classify_stage_label(classifier_record, interim_s0=0.01),
            )

    def test_report_membership_is_persisted_field_driven_and_sweep_uses_sole_seam(self):
        source = _source(240, n_stage1=3, n_gold=2, n_standard=2)
        source._records[0].E = 0.0  # persisted label intentionally disagrees
        before = tuple(record.stage_label for record in source.admitted_records())
        real_classifier = classify_stage_label

        with mock.patch(
            "pinn.data.stage_scan.classify_stage_label",
            wraps=real_classifier,
        ) as classifier:
            report = self.build(source)

        self.assertEqual(report["stages"]["0"]["record_count"], 240)
        self.assertEqual(classifier.call_count, 3 * 243)
        self.assertTrue(
            all(
                call.kwargs.keys() == {"interim_s0"}
                for call in classifier.call_args_list
            )
        )
        self.assertEqual(
            tuple(record.stage_label for record in source.admitted_records()),
            before,
        )
        self.assertEqual(source.classifier_interim_s0, 0.01)

    def test_report_is_deterministic_complete_and_portable(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir).resolve() / "absolute-corpus"
            source = _source(
                240,
                n_stage1=5,
                n_gold=10,
                n_standard=5,
                data_root=root,
            )
            for record in source.admitted_records():
                record.source_path = root / f"{record.record_key.id}.txt"

            first = self.build(source)
            second = self.build(source)
            first_bytes = json.dumps(first, sort_keys=True, indent=2) + "\n"
            second_bytes = json.dumps(second, sort_keys=True, indent=2) + "\n"

        self.assertEqual(first_bytes, second_bytes)
        self.assertEqual(first["schema_version"], "phase39-stage-population/v1")
        self.assertEqual(first["gold_numeric_stage_count"], 0)
        self.assertEqual(first["stages"]["0"]["resident_bytes"], 240 * 64)
        self.assertEqual(first["stages"]["1"]["resident_bytes"], 5 * 64)
        self.assertEqual(first["stages"]["UNASSIGNED"]["resident_bytes"], 15 * 64)
        self.assertEqual(
            sum(stage["resident_bytes"] for stage in first["stages"].values()),
            260 * 64,
        )
        self.assertEqual(first["s_min"]["count"], 260)
        self.assertEqual(first["s_min"]["values"], sorted(first["s_min"]["values"]))
        self.assertEqual(
            sum(
                summary["count"]
                for fidelity_map in first["s_min_by_variant_fidelity"].values()
                for summary in fidelity_map.values()
            ),
            first["s_min"]["count"],
        )
        self.assertEqual(len(first["s0_sensitivity_sweep"]["entries"]), 3)
        self.assertNotIn(str(root), first_bytes)
        self.assertNotIn("/Users/", first_bytes)

    def test_gold_numeric_label_fails_closed(self):
        source = _source(240)
        source._records += (
            _record(999, fidelity="gold", label=StageLabel.STAGE_0),
        )
        with self.assertRaisesRegex(ValueError, "gold_numeric_stage_count"):
            self.build(source)

    def test_full_count_zero_and_239_raise_with_complete_report_attached(self):
        for observed in (0, 239):
            with self.subTest(observed=observed):
                with self.assertRaises(StageZeroUnderpopulated) as caught:
                    self.build(_source(observed, n_stage1=2, n_gold=1))
                error = caught.exception
                self.assertEqual(error.threshold, 240)
                self.assertEqual(error.observed, observed)
                self.assertEqual(error.report["stage0_full_split_count"], observed)
                self.assertEqual(error.report["fatal"]["observed"], observed)
                self.assertIn("s_min", error.report)

    def test_full_count_240_is_nonfatal(self):
        report = self.build(_source(240))
        self.assertEqual(report["stage0_full_split_count"], 240)
        self.assertIs(report["fatal"], False)
        self.assertIsNone(report["stage0_train_split_count"])

    def test_full_ge_240_with_low_train_split_is_nonfatal(self):
        source = _source(250)
        train_keys = {
            record.physical_key
            for record in source.admitted_records()[:100]
        }
        manifest = _Manifest(source.admitted_records(), train_keys)

        report = self.build(source, manifest=manifest)

        self.assertEqual(report["stage0_full_split_count"], 250)
        self.assertEqual(report["stage0_train_split_count"], 100)
        self.assertIs(report["fatal"], False)
        self.assertEqual(report["readiness_operand"], "stage0_full_split_count")


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
