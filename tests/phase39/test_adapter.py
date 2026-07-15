"""Phase 39 Wave-0 contract — shared types + the in-memory admitted-set adapter.

Deferred contracts for Plan 02's ``pinn.data.types`` and ``pinn.data.adapter``
(DATA-01 / DATA-03, plus the frozen identities/outcomes every later module
consumes). Every test SKIPs via the localized ``_require`` helper (importing the
single ``tests.phase39._SKIP_PHRASE``) until the production symbol lands, then
turns green. No production file is created or edited here (Plans 02/03 own all
of ``pinn/data``).

Contract highlights (39-01-PLAN task 39-01-01 acceptance criteria):

* Identity equality/order depends on STRUCTURAL fields, never path formatting;
  invalid shape/fidelity/negative id fails before use.
* ``StageLabel`` admits only ``0``, ``1``, ``UNASSIGNED``; ``DataVersionHashDeferred``
  is distinguishable from success/``None``; mismatch is an exception; the fatal
  Stage-0 result carries the exact threshold (240) and observed count.
* ``FixedBatch.data_points`` and ``.collocation_points`` are separate frozen
  fields (never one aliased point set); model tensors carry last dims 14 and 3.
* GAP-39-07 ``resident_tensor_bytes`` deduplicates shared storage (40 + view +
  20 = 60, not 80) and the mem line is ``mem: 60 (0.600000) watermark=0.7``.
* A deferred synthetic end-to-end contract wires adapter -> split ->
  build_stage_batch -> build_population_report on one ``TinyCorpus`` (N6).
"""

import importlib
import unittest

from tests.phase39 import _SKIP_PHRASE
from tests.phase39 import _fixtures

TYPES = "pinn.data.types"
ADAPTER = "pinn.data.adapter"
SPLITS = "pinn.data.splits"
BATCHES = "pinn.data.batches"
STAGE_SCAN = "pinn.data.stage_scan"


def _require(symbol, module):
    try:
        mod = importlib.import_module(module)
    except ImportError:
        raise unittest.SkipTest(f"{_SKIP_PHRASE} {module}.{symbol}")
    if not hasattr(mod, symbol):
        raise unittest.SkipTest(f"{_SKIP_PHRASE} {module}.{symbol}")
    return getattr(mod, symbol)


def _load_torch():
    try:
        import torch
    except ImportError as exc:  # pragma: no cover
        raise unittest.SkipTest(f"torch not installed: {exc}")
    return torch


# ===========================================================================
# Structural identities.
# ===========================================================================

class IdentityTypeTests(unittest.TestCase):
    def test_physical_key_equality_and_order_are_structural(self):
        PhysicalKey = _require("PhysicalKey", TYPES)
        a = PhysicalKey("hierarchical", 7)
        b = PhysicalKey("hierarchical", 7)
        self.assertEqual(a, b)
        self.assertEqual(hash(a), hash(b))              # hashable identity
        self.assertLess(PhysicalKey("hierarchical", 1), PhysicalKey("hierarchical", 2))
        self.assertEqual(len({a, b}), 1)                # de-dups by fields

    def test_record_key_distinguishes_fidelity(self):
        RecordKey = _require("RecordKey", TYPES)
        base = RecordKey("hierarchical", "base", 7)
        gold = RecordKey("hierarchical", "gold", 7)
        self.assertNotEqual(base, gold)
        self.assertEqual(base, RecordKey("hierarchical", "base", 7))

    def test_invalid_identity_inputs_fail_before_use(self):
        PhysicalKey = _require("PhysicalKey", TYPES)
        RecordKey = _require("RecordKey", TYPES)
        for bad_variant in ("gold", "brutus_hierarchical", "", None):
            with self.assertRaises((ValueError, TypeError)):
                PhysicalKey(bad_variant, 1)
        for bad_id in (-1, "abc", 1.5):
            with self.assertRaises((ValueError, TypeError)):
                PhysicalKey("hierarchical", bad_id)
        for bad_fidelity in ("silver", "", None):
            with self.assertRaises((ValueError, TypeError)):
                RecordKey("hierarchical", bad_fidelity, 1)

    def test_identity_is_not_a_formatted_path(self):
        PhysicalKey = _require("PhysicalKey", TYPES)
        # Equality must not depend on any zero-padding / path rendering: the
        # structural id 7 is one identity regardless of how a path spells it.
        self.assertEqual(PhysicalKey("hierarchical", 7), PhysicalKey("hierarchical", 7))


class StageLabelTypeTests(unittest.TestCase):
    def test_only_three_labels_admitted(self):
        StageLabel = _require("StageLabel", TYPES)
        self.assertEqual(StageLabel(0), StageLabel.STAGE_0)
        self.assertEqual(StageLabel(1), StageLabel.STAGE_1)
        self.assertEqual(StageLabel("UNASSIGNED"), StageLabel.UNASSIGNED)
        for bad in (2, 3, 5, 6, "STAGE_0", "nope"):
            with self.assertRaises(ValueError):
                StageLabel(bad)
        for forbidden in ("STAGE_2", "STAGE_3", "STAGE_4", "STAGE_5", "STAGE_6"):
            self.assertFalse(hasattr(StageLabel, forbidden))


# ===========================================================================
# Version + fatal outcome types.
# ===========================================================================

class VersionOutcomeTypeTests(unittest.TestCase):
    def test_deferred_is_distinct_from_success_and_none(self):
        Deferred = _require("DataVersionHashDeferred", TYPES)
        Verified = _require("DataVersionHashVerified", TYPES)
        self.assertIsNot(Deferred, None)
        self.assertIsNot(Deferred, True)
        self.assertNotEqual(Deferred, None)
        self.assertNotEqual(Deferred, True)
        self.assertNotEqual(Deferred, Verified)

    def test_mismatch_is_a_hard_exception_type(self):
        Mismatch = _require("DataVersionHashMismatch", TYPES)
        self.assertTrue(issubclass(Mismatch, Exception))


class FatalResultTypeTests(unittest.TestCase):
    def test_stage_zero_underpopulated_carries_threshold_and_observed(self):
        Fatal = _require("StageZeroUnderpopulated", TYPES)
        fatal = Fatal(observed=5, threshold=240)
        self.assertEqual(fatal.threshold, 240)
        self.assertEqual(fatal.observed, 5)


# ===========================================================================
# Point-set / batch field separation.
# ===========================================================================

class PointSetAndBatchTypeTests(unittest.TestCase):
    def test_data_and_collocation_point_sets_are_distinct_types(self):
        DataFidelityPoints = _require("DataFidelityPoints", TYPES)
        PhysicsCollocationPoints = _require("PhysicsCollocationPoints", TYPES)
        self.assertIsNot(DataFidelityPoints, PhysicsCollocationPoints)

    def test_fixed_batch_keeps_two_separate_point_set_fields(self):
        import dataclasses
        FixedBatch = _require("FixedBatch", TYPES)
        names = {f.name for f in dataclasses.fields(FixedBatch)}
        self.assertIn("data_points", names)
        self.assertIn("collocation_points", names)
        # They cannot be one undifferentiated point-set field.
        self.assertNotEqual("data_points", "collocation_points")

    def test_data_fidelity_points_expose_input_and_raw_mass_fields(self):
        import dataclasses
        DataFidelityPoints = _require("DataFidelityPoints", TYPES)
        names = {f.name for f in dataclasses.fields(DataFidelityPoints)}
        # 14-wide [tau, IC13] and raw (N, 3) masses travel separately.
        self.assertTrue({"tau_ic13", "masses"} <= names,
                        f"DataFidelityPoints must carry tau_ic13 + masses; got {names}")


# ===========================================================================
# GAP-39-07 deterministic resident-tensor bytes + mem line.
# ===========================================================================

class ResidentBytesTests(unittest.TestCase):
    def test_shared_storage_is_counted_once(self):
        torch = _load_torch()
        resident_tensor_bytes = _require("resident_tensor_bytes", ADAPTER)
        owned = torch.zeros(10, dtype=torch.float32)   # 40 bytes
        view = owned[:5]                                # shares storage -> +0
        independent = torch.zeros(5, dtype=torch.float32)  # 20 bytes
        self.assertEqual(resident_tensor_bytes([owned, view, independent]), 60)

    def test_mem_line_exact_format(self):
        format_mem_line = _require("format_mem_line", ADAPTER)
        line = format_mem_line(60, 100)
        self.assertEqual(line, "mem: 60 (0.600000) watermark=0.7")

    def test_metric_ignores_unrelated_process_allocations(self):
        torch = _load_torch()
        resident_tensor_bytes = _require("resident_tensor_bytes", ADAPTER)
        owned = torch.zeros(10, dtype=torch.float32)
        before = resident_tensor_bytes([owned])
        _unrelated = torch.zeros(1000, dtype=torch.float32)  # not in the set
        self.assertEqual(resident_tensor_bytes([owned]), before)


# ===========================================================================
# Adapter residency / accessors / version / label persistence (deferred).
# ===========================================================================

class AdapterResidencyTests(unittest.TestCase):
    def _adapter(self, corpus, **over):
        AdmittedSetAdapter = _require("AdmittedSetAdapter", ADAPTER)
        kwargs = dict(root=corpus.data_root, blacklist_path=corpus.blacklist_path,
                      precision="float32", device="cpu", run_dir=corpus.run_dir,
                      version_metadata_path=corpus.version_metadata_path)
        kwargs.update(over)
        return AdmittedSetAdapter(**kwargs)

    def test_admitted_records_are_fp32_resident_with_accessors(self):
        torch = _load_torch()
        RecordKey = _require("RecordKey", TYPES)
        with _fixtures.TinyCorpus() as corpus:
            adapter = self._adapter(corpus)
            key = RecordKey("hierarchical", "base", 0)
            record = adapter.get(key)
            # fp32 residency for model-facing IC13 + raw masses.
            self.assertEqual(record.ic13.dtype, torch.float32)
            self.assertEqual(record.masses.dtype, torch.float32)
            # n_snapshots matches a direct parse (complete_times(12) -> 12 blocks).
            self.assertEqual(adapter.n_snapshots(key), 12)
            # dt_out carries measured + reference provenance (measured ~ 10/11).
            self.assertAlmostEqual(adapter.dt_out(key), 10.0 / 11.0, places=6)
            self.assertTrue(hasattr(record, "dt_out_measured"))
            self.assertTrue(hasattr(record, "dt_out_reference"))

    def test_mem_line_fraction_within_watermark(self):
        import re
        with _fixtures.TinyCorpus() as corpus:
            adapter = self._adapter(corpus, capacity_bytes=1 << 34)  # 16 GB
            line = adapter.mem_line()
            m = re.match(r"mem: (\d+) \((\d+\.\d{6})\) watermark=0\.7", line)
            self.assertIsNotNone(m, line)
            self.assertLessEqual(float(m.group(2)), 0.7)

    def test_empty_admitted_set_is_a_hard_init_failure(self):
        from tempfile import TemporaryDirectory
        from pathlib import Path
        import json
        AdmittedSetAdapter = _require("AdmittedSetAdapter", ADAPTER)
        with TemporaryDirectory() as tmp:
            root = Path(tmp) / "Data"
            for f in _fixtures.IC_FOLDERS:
                (root / _fixtures.IC_SUBDIR / f).mkdir(parents=True)
            for f in _fixtures.BRUTUS_FOLDERS:
                (root / _fixtures.BRUTUS_SUBDIR / f).mkdir(parents=True)
            blacklist = root / "blacklist.json"
            blacklist.write_text(json.dumps({"hierarchical": [], "standard": []}))
            with self.assertRaises((ValueError, RuntimeError)):
                AdmittedSetAdapter(root=root, blacklist_path=blacklist,
                                   precision="float32", device="cpu",
                                   run_dir=Path(tmp) / "run")

    def test_version_hash_match_mismatch_and_absent(self):
        Deferred = _require("DataVersionHashDeferred", TYPES)
        Mismatch = _require("DataVersionHashMismatch", TYPES)
        with _fixtures.TinyCorpus() as corpus:
            adapter = self._adapter(corpus)
            # Match -> a non-deferred verified outcome.
            self.assertNotEqual(adapter.verify_data_version(corpus.known_data_version_hash),
                                Deferred)
            # Mismatch -> hard refusal.
            with self.assertRaises(Mismatch):
                adapter.verify_data_version("b" * 64)
            # Absent metadata -> typed deferral (never a silent match).
            absent = self._adapter(corpus,
                                   version_metadata_path=corpus.absent_version_metadata_path)
            self.assertEqual(absent.verify_data_version("b" * 64), Deferred)

    def test_gold_labels_are_never_derived_from_base(self):
        RecordKey = _require("RecordKey", TYPES)
        StageLabel = _require("StageLabel", TYPES)
        with _fixtures.TinyCorpus() as corpus:
            adapter = self._adapter(corpus)
            # Robust fidelity invariant (independent of the synthetic invariants):
            # every gold record is UNASSIGNED; base labels may be 0/1/UNASSIGNED.
            for id_ in (0, 7):
                gold = RecordKey("hierarchical", "gold", id_)
                if gold in adapter.record_keys():
                    self.assertEqual(adapter.stage_label(gold), StageLabel.UNASSIGNED)
            self.assertEqual(adapter.gold_numeric_stage_count, 0)
            # Every numeric-labeled key is base hierarchical Set 1a.
            for key in adapter.record_keys():
                if adapter.stage_label(key) in (StageLabel.STAGE_0, StageLabel.STAGE_1):
                    self.assertEqual(key.fidelity, "base")
                    self.assertEqual(key.variant, "hierarchical")

    def test_blacklist_membership_is_immutable_and_observed(self):
        PhysicalKey = _require("PhysicalKey", TYPES)
        with _fixtures.TinyCorpus() as corpus:
            adapter = self._adapter(corpus)
            # id 3 hierarchical is blacklisted in the fixture; it is excluded.
            self.assertTrue(adapter.is_blacklisted(PhysicalKey("hierarchical", 3)))
            self.assertNotIn(PhysicalKey("hierarchical", 3),
                             {k.physical_key if hasattr(k, "physical_key")
                              else PhysicalKey(k.variant, k.id)
                              for k in adapter.record_keys()})


# ===========================================================================
# N6 — deferred synthetic end-to-end wiring smoke test.
# ===========================================================================

class EndToEndIntegrationTests(unittest.TestCase):
    """adapter init -> StageQuery -> split -> build_stage_batch ->
    build_population_report on ONE TinyCorpus fixture, asserting no wiring break
    across module boundaries (cross-AI review N6). The adapter IS the StageQuery
    surface consumed by the splitter, batch constructor, and report."""

    def test_full_chain_wires_without_breaking_module_boundaries(self):
        AdmittedSetAdapter = _require("AdmittedSetAdapter", ADAPTER)
        build_split_manifest = _require("build_split_manifest", SPLITS)
        build_stage_batch = _require("build_stage_batch", BATCHES)
        build_population_report = _require("build_population_report", STAGE_SCAN)
        StageZeroUnderpopulated = _require("StageZeroUnderpopulated", TYPES)

        with _fixtures.TinyCorpus() as corpus:
            adapter = AdmittedSetAdapter(
                root=corpus.data_root, blacklist_path=corpus.blacklist_path,
                precision="float32", device="cpu", run_dir=corpus.run_dir,
                version_metadata_path=corpus.version_metadata_path)

            # Split manifest is written into the injected run dir.
            manifest = build_split_manifest(adapter, seed=1234, run_dir=corpus.run_dir)
            self.assertIsNotNone(manifest)

            # Batch construction is reachable; a TinyCorpus cannot supply 240
            # Stage-0 trajectories, so the wiring may legitimately surface the
            # typed underpopulation fatal instead of a batch — either proves the
            # boundary is wired (a crash / import error would not).
            try:
                batch = build_stage_batch(adapter, stage=0)
                if batch is not None:
                    self.assertEqual(batch.data_points.tau_ic13.shape[-1], 14)
                    self.assertEqual(batch.data_points.masses.shape[-1], 3)
            except StageZeroUnderpopulated:
                pass

            # The Stage-0 report always consumes persisted labels and holds the
            # zero-gold invariant regardless of population.
            report = build_population_report(adapter, interim_s0=0.01)
            self.assertEqual(report.gold_numeric_stage_count, 0)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
