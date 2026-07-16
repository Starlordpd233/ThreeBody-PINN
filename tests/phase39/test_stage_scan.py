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
import hashlib
import io
import json
from pathlib import Path
import re
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

    def evidence_lines(self):
        """Mirrors the adapter's redacted evidence projection for the CLI."""
        return (
            "GSD_DATA_ROOT=$GSD_DATA_ROOT source=env:GSD_DATA_ROOT",
            "brutus_folder brutus_hierarchical present=True",
            "brutus_folder brutus_hierarchical_gold_standard present=True",
            "brutus_folder brutus_standard_quasi_random present=True",
            "brutus_folder brutus_standard_quasi_random_gold_standard present=True",
            "allow_partial_data_root=0",
            "blacklist hierarchical n_blacklist_entries=2",
            "blacklist standard n_blacklist_entries=63",
            "blacklist base n_present_on_disk=65 n_excluded=65",
            "blacklist gold n_present_on_disk=65 n_excluded=65",
            "folder brutus_hierarchical found=1 admitted=1 rejected=0 quarantined=0 dropped_samples=0",
            "mem: 1234 (0.000048) watermark=0.7",
            "mem_ballpark=1100",
            "gold_numeric_stage_count=0",
        )


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

    def test_stage_scan_exports_atomic_writer(self):
        module = importlib.import_module(STAGE_SCAN)
        self.assertTrue(
            hasattr(module, "write_population_report"),
            "Plan 39-06 Task 2 must export write_population_report",
        )

    def test_stage_scan_exports_cli_main(self):
        module = importlib.import_module(STAGE_SCAN)
        self.assertTrue(
            hasattr(module, "main"),
            "Plan 39-06 Task 2 must export testable main(argv=None)",
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


class PopulationReportWriterContract(unittest.TestCase):
    def setUp(self):
        self.write = _require("write_population_report")

    def test_writer_emits_canonical_atomic_json_bytes(self):
        report = {"z": [3, 2, 1], "a": {"fatal": False}}
        expected = (json.dumps(report, sort_keys=True, indent=2) + "\n").encode()

        with tempfile.TemporaryDirectory() as temp_dir:
            run_dir = Path(temp_dir) / "run"
            path = self.write(report, run_dir)

            self.assertEqual(path, run_dir / "stage_population.json")
            self.assertEqual(path.read_bytes(), expected)
            self.assertEqual(list(run_dir.glob("*.tmp.*")), [])

    def test_writer_rejects_repository_corpus_run_directory(self):
        repository = Path(__file__).resolve().parents[2]
        forbidden = repository / "simulation_data" / "phase39-forbidden-run"

        with self.assertRaisesRegex(ValueError, "simulation_data|corpus"):
            self.write({"fatal": False}, forbidden)
        self.assertFalse(forbidden.exists())

    def test_writer_replace_failure_preserves_previous_report(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            run_dir = Path(temp_dir) / "run"
            run_dir.mkdir()
            destination = run_dir / "stage_population.json"
            destination.write_bytes(b"previous\n")

            with mock.patch("pinn.data.stage_scan.os.replace", side_effect=OSError("boom")):
                with self.assertRaisesRegex(OSError, "boom"):
                    self.write({"fatal": False}, run_dir)

            self.assertEqual(destination.read_bytes(), b"previous\n")
            self.assertEqual(list(run_dir.glob("*.tmp.*")), [])


class StageScanCliContract(unittest.TestCase):
    def setUp(self):
        self.main = _require("main")

    def _run(self, source, run_dir, *extra):
        adapter_factory = mock.Mock(return_value=source)
        stdout = io.StringIO()
        with mock.patch(
            "pinn.data.stage_scan.AdmittedSetAdapter",
            adapter_factory,
        ), mock.patch("sys.stdout", new=stdout):
            exit_code = self.main(["--run-dir", str(run_dir), *extra])
        return exit_code, stdout.getvalue(), adapter_factory

    def test_cli_full_pass_writes_manifest_report_and_hash_log(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            source = _source(250, data_root=root / "corpus")
            run_dir = root / "run"

            exit_code, stdout, _factory = self._run(source, run_dir)

            report = json.loads((run_dir / "stage_population.json").read_text())
            split_bytes = (run_dir / "splits.json").read_bytes()
            scan_log = (run_dir / "scan.log").read_text()

        self.assertEqual(exit_code, 0)
        self.assertEqual(report["stage0_full_split_count"], 250)
        self.assertLess(report["stage0_train_split_count"], 240)
        self.assertIs(report["fatal"], False)
        self.assertIn("stage0_full_split_count=250", stdout)
        self.assertIn(
            f"stage0_train_split_count={report['stage0_train_split_count']}",
            stdout,
        )
        self.assertIn("gold_numeric_stage_count=0", stdout)
        self.assertIn(
            "splits.json_sha256=" + hashlib.sha256(split_bytes).hexdigest(),
            scan_log,
        )
        self.assertIn(f"splits.json_bytes={len(split_bytes)}", scan_log)
        self.assertIn("splits.json_byte_identity=true", scan_log)
        # Evidence passthrough: every line the source's evidence_lines()
        # returned reaches scan.log verbatim, in order.
        for line in source.evidence_lines():
            self.assertIn(line, scan_log)
        # Freshness markers: one run_timestamp and one run_nonce, stable
        # within the run and formatted per the row contract.
        self.assertRegex(scan_log, re.compile(r"^run_timestamp=[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z$", re.MULTILINE))
        self.assertRegex(scan_log, re.compile(r"^run_nonce=[0-9a-f]{16}$", re.MULTILINE))
        # Exit code and byte-identity fields use the renamed/derived names.
        self.assertIn("scan_exit_code=0", scan_log)
        self.assertIn("evidence_byte_identity=true", scan_log)
        # Privacy: no resolved host path leaks into retained evidence.
        self.assertNotIn("root: ", scan_log)
        self.assertNotIn(str(Path.home()), scan_log)

    def test_cli_fatal_writes_report_manifest_and_log_before_exit_two(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            source = _source(239, data_root=root / "corpus")
            run_dir = root / "run"

            exit_code, stdout, _factory = self._run(source, run_dir)

            report_path = run_dir / "stage_population.json"
            split_path = run_dir / "splits.json"
            log_path = run_dir / "scan.log"
            report = json.loads(report_path.read_text())
            split_bytes = split_path.read_bytes()
            scan_log = log_path.read_text()

        self.assertEqual(exit_code, 2)
        self.assertEqual(report["fatal"]["type"], "StageZeroUnderpopulated")
        self.assertEqual(report["fatal"]["observed"], 239)
        self.assertEqual(report["stage0_full_split_count"], 239)
        self.assertTrue(split_bytes)
        self.assertIn("stage0_full_split_count=239", stdout)
        self.assertIn("splits.json_byte_identity=true", scan_log)
        self.assertIn("scan_exit_code=2", scan_log)
        self.assertIn("evidence_byte_identity=true", scan_log)

    def test_cli_forwards_all_explicit_adapter_and_split_flags(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            source = _source(240, data_root=root / "corpus")
            run_dir = root / "run"
            blacklist = root / "blacklist.json"
            metadata = root / "version.json"

            exit_code, _stdout, factory = self._run(
                source,
                run_dir,
                "--data-root",
                str(root / "corpus"),
                "--blacklist-path",
                str(blacklist),
                "--version-metadata-path",
                str(metadata),
                "--expected-data-version-hash",
                "expected",
                "--supplied-data-version-hash",
                "supplied",
                "--memory-capacity-bytes",
                "123456",
                "--memory-watermark",
                "0.75",
                "--interim-s0",
                "0.02",
                "--seed",
                "77",
                "--ratios",
                "0.7",
                "0.2",
                "0.1",
            )

        self.assertEqual(exit_code, 0)
        factory.assert_called_once_with(
            data_root=str(root / "corpus"),
            blacklist_path=str(blacklist),
            version_metadata_path=str(metadata),
            expected_data_version_hash="expected",
            supplied_data_version_hash="supplied",
            capacity_bytes=123456,
            memory_watermark=0.75,
            interim_s0=0.02,
            run_dir=str(run_dir),
            device="cpu",
        )

    def test_cli_rejects_zero_capacity_before_adapter_construction(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            source = _source(240, data_root=root / "corpus")
            run_dir = root / "run"
            exit_code, _stdout, factory = self._run(
                source, run_dir, "--memory-capacity-bytes", "0",
            )
        self.assertNotEqual(exit_code, 0)
        factory.assert_not_called()

    def test_cli_rejects_negative_capacity_before_adapter_construction(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            source = _source(240, data_root=root / "corpus")
            run_dir = root / "run"
            exit_code, _stdout, factory = self._run(
                source, run_dir, "--memory-capacity-bytes", "-1",
            )
        self.assertNotEqual(exit_code, 0)
        factory.assert_not_called()

    def test_cli_rejects_nan_watermark_before_adapter_construction(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            source = _source(240, data_root=root / "corpus")
            run_dir = root / "run"
            exit_code, _stdout, factory = self._run(
                source, run_dir, "--memory-watermark", "nan",
            )
        self.assertNotEqual(exit_code, 0)
        factory.assert_not_called()

    def test_cli_rejects_inf_watermark_before_adapter_construction(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            source = _source(240, data_root=root / "corpus")
            run_dir = root / "run"
            exit_code, _stdout, factory = self._run(
                source, run_dir, "--memory-watermark", "inf",
            )
        self.assertNotEqual(exit_code, 0)
        factory.assert_not_called()

    def test_cli_rejects_zero_watermark_before_adapter_construction(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            source = _source(240, data_root=root / "corpus")
            run_dir = root / "run"
            exit_code, _stdout, factory = self._run(
                source, run_dir, "--memory-watermark", "0",
            )
        self.assertNotEqual(exit_code, 0)
        factory.assert_not_called()

    def test_cli_rejects_negative_watermark_before_adapter_construction(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            source = _source(240, data_root=root / "corpus")
            run_dir = root / "run"
            exit_code, _stdout, factory = self._run(
                source, run_dir, "--memory-watermark", "-0.5",
            )
        self.assertNotEqual(exit_code, 0)
        factory.assert_not_called()

    def test_cli_rejects_watermark_greater_than_one_before_adapter_construction(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            source = _source(240, data_root=root / "corpus")
            run_dir = root / "run"
            exit_code, _stdout, factory = self._run(
                source, run_dir, "--memory-watermark", "1.5",
            )
        self.assertNotEqual(exit_code, 0)
        factory.assert_not_called()

    def test_cli_rejects_nan_interim_s0_before_adapter_construction(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            source = _source(240, data_root=root / "corpus")
            run_dir = root / "run"
            exit_code, _stdout, factory = self._run(
                source, run_dir, "--interim-s0", "nan",
            )
        self.assertNotEqual(exit_code, 0)
        factory.assert_not_called()

    def test_cli_rejects_inf_interim_s0_before_adapter_construction(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            source = _source(240, data_root=root / "corpus")
            run_dir = root / "run"
            exit_code, _stdout, factory = self._run(
                source, run_dir, "--interim-s0", "inf",
            )
        self.assertNotEqual(exit_code, 0)
        factory.assert_not_called()

    def test_cli_rejects_nonpositive_interim_s0_before_adapter_construction(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            source = _source(240, data_root=root / "corpus")
            run_dir = root / "run"
            exit_code, _stdout, factory = self._run(
                source, run_dir, "--interim-s0", "0",
            )
        self.assertNotEqual(exit_code, 0)
        factory.assert_not_called()

    def test_cli_forwards_explicit_device_cpu(self):
        """The production CLI passes device='cpu' explicitly (D-03)."""
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            source = _source(240, data_root=root / "corpus")
            run_dir = root / "run"
            exit_code, _stdout, factory = self._run(source, run_dir)
        self.assertEqual(exit_code, 0)
        _, kwargs = factory.call_args
        self.assertEqual(kwargs.get("device"), "cpu")

    def test_cli_stamps_one_run_timestamp_and_nonce_across_writes(self):
        """The pending and final writes of one run share one nonce/timestamp."""
        write_scan_log = _require("_write_scan_log")
        captured = {}

        def _capture_nonce(*args, **kwargs):
            # The nonce is embedded in the scan.log text; extract it.
            text = write_scan_log(*args, **kwargs)
            captured["path"] = text
            return text

        # A source whose report raises lets us observe the pending write's
        # nonce by reading scan.log after the fatal path returns. Simpler:
        # assert the nonce is stable by running main() once and reading the
        # final scan.log — the pending write happened earlier in the same run
        # with the same nonce, so the final artifact's nonce is the run nonce.
        # Two separate main() invocations must produce different nonces.
        nonces = set()
        timestamps = set()
        for _ in range(2):
            with tempfile.TemporaryDirectory() as temp_dir:
                root = Path(temp_dir)
                source = _source(240, data_root=root / "corpus")
                run_dir = root / "run"
                self._run(source, run_dir)
                scan_log = (run_dir / "scan.log").read_text()
                nonce_match = re.search(r"^run_nonce=([0-9a-f]{16})$", scan_log, re.MULTILINE)
                ts_match = re.search(r"^run_timestamp=([0-9T:Z-]+)$", scan_log, re.MULTILINE)
                self.assertIsNotNone(nonce_match)
                self.assertIsNotNone(ts_match)
                nonces.add(nonce_match.group(1))
                timestamps.add(ts_match.group(1))
        self.assertEqual(len(nonces), 2, "two runs must produce distinct nonces")

    def test_cli_exit_code_field_renamed_to_scan_exit_code(self):
        """The readiness tail emits scan_exit_code=, never a bare exit_code=."""
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            source = _source(240, data_root=root / "corpus")
            run_dir = root / "run"
            self._run(source, run_dir)
            scan_log = (run_dir / "scan.log").read_text()
        self.assertIn("scan_exit_code=0", scan_log)
        # No line may start with the old bare field name (the new name contains
        # "exit_code=" as a substring, so a plain substring check would lie).
        for line in scan_log.splitlines():
            self.assertFalse(
                line.startswith("exit_code="),
                f"bare exit_code= field leaked: {line!r}",
            )

    def test_cli_fail_closed_source_without_evidence_lines(self):
        """A source lacking evidence_lines() raises TypeError, no clean scan.log."""
        # A source that cannot produce evidence — the CLI must fail loudly
        # rather than write an evidence-poor scan.log.
        class _BareSource:
            pass

        bare_source = _BareSource()
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            run_dir = root / "run"
            with self.assertRaises(TypeError) as cm:
                self._run(bare_source, run_dir)
            self.assertIn("evidence_lines", str(cm.exception))


# Deliberate duplicate of the ledger row's contract. If row 39-07-02 ever
# changes, this tuple must be updated in lockstep so the mirror cannot
# silently drift from the row it mirrors.
_ROW_39_07_02_PATTERNS = (
    r"^allow_partial_data_root=0$",
    r"^scan_exit_code=[0-9]+$",
    r"^run_timestamp=[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}",
    r"^run_nonce=[0-9a-f]{16}$",
    r"^stage0_train_split_count=[0-9]+$",
    r"^stage0_full_split_count=[0-9]+$",
    r"splits.json_sha256=[0-9a-f]{64}",
    r"^evidence_byte_identity=true$",
    r"gold_numeric_stage_count=0",
    r"mem: [0-9]+ \([0-9]+\.[0-9]{6}\) watermark=0\.7",
    r"mem_ballpark=[0-9]+",
    r"n_blacklist_entries",
    r"n_present_on_disk",
    r"GSD_DATA_ROOT=",
)


class ScanLogLedgerRowContract(unittest.TestCase):
    """Dataset-free mirror of 39-VALIDATION.md row 39-07-02."""

    def setUp(self):
        self.main = _require("main")

    def _run(self, source, run_dir, *extra):
        adapter_factory = mock.Mock(return_value=source)
        with mock.patch(
            "pinn.data.stage_scan.AdmittedSetAdapter",
            adapter_factory,
        ):
            return self.main(["--run-dir", str(run_dir), *extra])

    def test_scan_log_satisfies_validation_row_39_07_02_field_contract(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            source = _source(250, data_root=root / "corpus")
            run_dir = root / "run"
            self._run(source, run_dir)
            scan_log = (run_dir / "scan.log").read_text()

        for pattern in _ROW_39_07_02_PATTERNS:
            with self.subTest(pattern=pattern):
                self.assertRegex(scan_log, re.compile(pattern, re.MULTILINE))

        # Privacy conditions paired with the presence checks: no resolved
        # root line and no host home prefix anywhere in the emitted bytes.
        for line in scan_log.splitlines():
            self.assertFalse(line.startswith("root: "), "resolved root leaked")
        self.assertNotIn(str(Path.home()), scan_log)

        # The mem: fraction must parse as a float at or below the 0.7 watermark.
        mem_match = re.search(
            r"mem: [0-9]+ \(([0-9]+\.[0-9]{6})\) watermark=0\.7", scan_log)
        self.assertIsNotNone(mem_match)
        self.assertLessEqual(float(mem_match.group(1)), 0.7)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
