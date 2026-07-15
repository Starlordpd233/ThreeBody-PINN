"""Phase 39 Wave-0 contract — the grouped stage-stratified split manifest (DATA-04).

Deferred contract for ``pinn.data.splits.build_split_manifest`` (GAP-39-06
complete-signature Hamilton split; GAP-39-08 base-label/gold-UNASSIGNED
signatures; GAP-39-11 split-only ``MISSING_BASE`` sentinel). Every test SKIPs
via the localized ``_require`` helper until production lands.

The splitter consumes an in-memory ``source`` exposing ``admitted_records()``
(objects with ``.physical_key``, ``.record_key``, ``.stage_label``) — no disk,
no adapter internals — and writes a canonical, byte-stable ``splits.json`` into
the injected run directory (never the corpus root).

Grounding: ``39-PATTERNS.md`` splits.py; ``ctl_instruction.md:515-530``; GAP-39-06
(signature ``(regime, base_stage, gold_stage_or_missing)``, seeded Hamilton
largest-remainder, fixed train->validation->test tie order); GAP-39-11
(``MISSING_BASE`` belongs only to the split signature/manifest, never a persisted
record label, never a numeric pool).
"""

import importlib
import inspect
import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from types import SimpleNamespace
from unittest import mock

import numpy as np

from tests.phase39 import _SKIP_PHRASE, _fixtures

SPLITS = "pinn.data.splits"
TYPES = "pinn.data.types"


def _require(symbol, module):
    try:
        mod = importlib.import_module(module)
    except ImportError:
        raise unittest.SkipTest(f"{_SKIP_PHRASE} {module}.{symbol}")
    if not hasattr(mod, symbol):
        raise unittest.SkipTest(f"{_SKIP_PHRASE} {module}.{symbol}")
    return getattr(mod, symbol)


class _Source:
    """Minimal admitted-set source consumed by the splitter."""

    def __init__(self, records):
        self._records = list(records)

    def admitted_records(self):
        return tuple(self._records)


class StageIndexContract(unittest.TestCase):
    """Task 39-04-01 — persisted-label, memory-only StageQuery behavior."""

    def test_numeric_queries_read_persisted_labels_and_exclude_gold(self):
        splits = importlib.import_module(SPLITS)
        types = importlib.import_module(TYPES)
        base = SimpleNamespace(
            physical_key=types.PhysicalKey("hierarchical", 7),
            record_key=types.RecordKey("hierarchical", "base", 7),
            stage_label=types.StageLabel.STAGE_0,
        )
        gold = SimpleNamespace(
            physical_key=types.PhysicalKey("hierarchical", 7),
            record_key=types.RecordKey("hierarchical", "gold", 7),
            stage_label=types.StageLabel.UNASSIGNED,
        )

        index = splits.StageIndex([gold, base])

        self.assertEqual(index.records_at(0), (base.record_key,))
        self.assertEqual(index.records_at_or_below(1), (base.record_key,))
        self.assertFalse(index.has_stage(1))
        self.assertEqual(index.gold_numeric_stage_count, 0)

    def test_stage_index_rejects_missing_invalid_and_gold_numeric_labels(self):
        splits = importlib.import_module(SPLITS)
        types = importlib.import_module(TYPES)

        def record(fidelity, label=...):
            fields = {
                "physical_key": types.PhysicalKey("hierarchical", 1),
                "record_key": types.RecordKey("hierarchical", fidelity, 1),
            }
            if label is not ...:
                fields["stage_label"] = label
            return SimpleNamespace(**fields)

        with self.assertRaises((TypeError, ValueError)):
            splits.StageIndex([record("base")])
        with self.assertRaises((TypeError, ValueError)):
            splits.StageIndex([record("base", 0)])
        with self.assertRaises((TypeError, ValueError)):
            splits.StageIndex([record("base", types.MISSING_BASE)])
        with self.assertRaises((TypeError, ValueError)):
            splits.StageIndex([record("gold", types.StageLabel.STAGE_0)])
        self.assertNotIn(types.MISSING_BASE, set(types.StageLabel))

    def test_numeric_labels_are_restricted_to_original_base_hierarchical(self):
        splits = importlib.import_module(SPLITS)
        types = importlib.import_module(TYPES)
        standard = SimpleNamespace(
            physical_key=types.PhysicalKey("standard", 2),
            record_key=types.RecordKey("standard", "base", 2),
            stage_label=types.StageLabel.STAGE_1,
        )
        with self.assertRaises((TypeError, ValueError)):
            splits.StageIndex([standard])

    def test_constructor_has_no_independent_stage_map_parameter(self):
        splits = importlib.import_module(SPLITS)
        self.assertEqual(list(inspect.signature(splits.StageIndex).parameters), ["records"])


class SignaturePartitionContract(unittest.TestCase):
    """Task 39-04-01 — complete-signature Hamilton group allocation."""

    def setUp(self):
        self.splits = importlib.import_module(SPLITS)
        self.types = importlib.import_module(TYPES)

    def _rec(self, fidelity, id_, label, variant="hierarchical"):
        return SimpleNamespace(
            physical_key=self.types.PhysicalKey(variant, id_),
            record_key=self.types.RecordKey(variant, fidelity, id_),
            stage_label=label,
        )

    def _pair(self, id_, label, variant="hierarchical"):
        return [
            self._rec("base", id_, label, variant),
            self._rec("gold", id_, self.types.StageLabel.UNASSIGNED, variant),
        ]

    def _partition(self, records, seed=17):
        return self.splits._partition_by_signature(
            records, seed=seed, ratios=self.splits.SplitRatios()
        )

    def test_complete_signatures_preserve_missing_sentinels_and_group_integrity(self):
        records = self._pair(1, self.types.StageLabel.STAGE_0)
        records.append(self._rec("base", 2, self.types.StageLabel.STAGE_1))
        records.append(self._rec("gold", 3, self.types.StageLabel.UNASSIGNED))

        manifest = self._partition(records)

        self.assertIn(
            ("hierarchical", 0, "UNASSIGNED"), manifest.signatures
        )
        self.assertIn(
            ("hierarchical", 1, self.types.MISSING_GOLD), manifest.signatures
        )
        self.assertIn(
            ("hierarchical", self.types.MISSING_BASE, "UNASSIGNED"),
            manifest.signatures,
        )
        placements = {}
        for split_name, keys in manifest.splits.items():
            for key in keys:
                placements.setdefault(key.physical_key, set()).add(split_name)
        self.assertEqual(set(placements), {
            self.types.PhysicalKey("hierarchical", 1),
            self.types.PhysicalKey("hierarchical", 2),
            self.types.PhysicalKey("hierarchical", 3),
        })
        self.assertTrue(all(len(names) == 1 for names in placements.values()))

    def test_hamilton_uses_fixed_tie_order_and_emits_rare_deviations(self):
        records = [
            rec
            for id_ in range(5)
            for rec in self._pair(id_, self.types.StageLabel.STAGE_0)
        ]

        manifest = self._partition(records)
        summary = manifest.signature_summaries[0]

        self.assertEqual(summary.counts, {"train": 4, "validation": 1, "test": 0})
        self.assertEqual(sum(summary.counts.values()), 5)
        self.assertTrue(summary.deviations)
        self.assertEqual(
            summary.deviations,
            self._partition(list(reversed(records))).signature_summaries[0].deviations,
        )

    def test_every_hamilton_allocation_sums_exactly_to_signature_size(self):
        for size in range(1, 21):
            with self.subTest(size=size):
                records = [
                    rec
                    for id_ in range(size)
                    for rec in self._pair(id_, self.types.StageLabel.STAGE_0)
                ]
                summary = self._partition(records).signature_summaries[0]
                self.assertEqual(sum(summary.counts.values()), size)

    def test_partition_uses_only_local_rng_state(self):
        records = [
            rec
            for id_ in range(10)
            for rec in self._pair(id_, self.types.StageLabel.STAGE_0)
        ]
        np.random.seed(12345)
        expected = np.random.random()
        np.random.seed(12345)
        self._partition(records)
        self.assertEqual(np.random.random(), expected)

    def test_input_order_is_irrelevant_and_seed_changes_only_identities(self):
        records = [
            rec
            for id_ in range(30)
            for rec in self._pair(id_, self.types.StageLabel.STAGE_0)
        ]
        first = self._partition(records, seed=1)
        reversed_input = self._partition(list(reversed(records)), seed=1)
        second_seed = self._partition(records, seed=2)

        self.assertEqual(first.to_dict(), reversed_input.to_dict())
        self.assertEqual(
            {name: len(keys) for name, keys in first.splits.items()},
            {name: len(keys) for name, keys in second_seed.splits.items()},
        )
        self.assertNotEqual(
            {key.physical_key for key in first.splits["train"]},
            {key.physical_key for key in second_seed.splits["train"]},
        )

    def test_partition_rejects_empty_input_and_invalid_ratios(self):
        with self.assertRaises(ValueError):
            self._partition([])
        with self.assertRaises(ValueError):
            self.splits.SplitRatios(train=0.7, validation=0.2, test=0.2)

    def test_from_split_materializes_adapter_once_and_excludes_other_splits(self):
        records = [
            rec
            for id_ in range(20)
            for rec in self._pair(id_, self.types.StageLabel.STAGE_0)
        ]
        manifest = self._partition(records)

        class AdapterLike:
            def __init__(self, admitted):
                self._by_key = {record.record_key: record for record in admitted}
                self.record_keys_calls = 0
                self.blacklisted_physical_keys = frozenset()

            def record_keys(self):
                self.record_keys_calls += 1
                return tuple(reversed(sorted(self._by_key)))

            def get(self, key):
                return self._by_key[key]

        source = AdapterLike(records)
        train = self.splits.StageIndex.from_split(source, manifest, "train")
        self.assertEqual(source.record_keys_calls, 1)
        train_physical = {key.physical_key for key in train.records_at_or_below(1)}
        expected_train = {
            key.physical_key for key in manifest.splits["train"]
        }
        held_out = {
            key.physical_key
            for name in ("validation", "test")
            for key in manifest.splits[name]
        }
        self.assertEqual(train_physical, expected_train)
        self.assertTrue(train_physical.isdisjoint(held_out))

        validation = self.splits.StageIndex.from_split(source, manifest, "validation")
        self.assertEqual(
            {key.physical_key for key in validation.records_at_or_below(1)},
            {key.physical_key for key in manifest.splits["validation"]},
        )


class ManifestWriterContract(unittest.TestCase):
    """Task 39-04-02 — canonical atomic split-manifest persistence."""

    def test_writer_partitions_source_internally_and_returns_typed_manifest(self):
        splits = importlib.import_module(SPLITS)
        types = importlib.import_module(TYPES)
        records = []
        for id_ in range(10):
            physical_key = types.PhysicalKey("hierarchical", id_)
            records.extend((
                SimpleNamespace(
                    physical_key=physical_key,
                    record_key=types.RecordKey("hierarchical", "base", id_),
                    stage_label=types.StageLabel.STAGE_0,
                ),
                SimpleNamespace(
                    physical_key=physical_key,
                    record_key=types.RecordKey("hierarchical", "gold", id_),
                    stage_label=types.StageLabel.UNASSIGNED,
                ),
            ))

        with TemporaryDirectory() as tmp:
            run_dir = Path(tmp) / "run"
            manifest = splits.write_split_manifest(
                _Source(records),
                run_dir=run_dir,
                seed=11,
                ratios=splits.SplitRatios(),
            )

            self.assertIsInstance(manifest, splits.SplitManifest)
            self.assertEqual(Path(manifest.path), run_dir / "splits.json")
            self.assertTrue(Path(manifest.path).is_file())

    def _records(self, count=30):
        types = importlib.import_module(TYPES)
        records = []
        for id_ in range(count):
            physical_key = types.PhysicalKey("hierarchical", id_)
            records.extend((
                SimpleNamespace(
                    physical_key=physical_key,
                    record_key=types.RecordKey("hierarchical", "base", id_),
                    stage_label=types.StageLabel.STAGE_0,
                ),
                SimpleNamespace(
                    physical_key=physical_key,
                    record_key=types.RecordKey("hierarchical", "gold", id_),
                    stage_label=types.StageLabel.UNASSIGNED,
                ),
            ))
        return records

    def test_writer_is_single_canonical_signature_and_materializes_once(self):
        splits = importlib.import_module(SPLITS)
        records = self._records(10)

        class AdapterLike:
            def __init__(self, admitted):
                self._records = {record.record_key: record for record in admitted}
                self.calls = 0

            def record_keys(self):
                self.calls += 1
                return tuple(self._records)

            def get(self, key):
                return self._records[key]

        source = AdapterLike(records)
        with TemporaryDirectory() as tmp:
            splits.write_split_manifest(
                source, run_dir=Path(tmp) / "run", seed=9,
                ratios=splits.SplitRatios())
        self.assertEqual(source.calls, 1)
        self.assertIs(splits.build_split_manifest, splits.write_split_manifest)
        self.assertEqual(
            list(inspect.signature(splits.write_split_manifest).parameters),
            ["source", "run_dir", "seed", "ratios"],
        )

    def test_independent_writes_are_byte_identical_and_round_trip_typed(self):
        splits = importlib.import_module(SPLITS)
        records = self._records()
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            first = splits.write_split_manifest(
                _Source(records), root / "one", 41, splits.SplitRatios())
            second = splits.write_split_manifest(
                _Source(reversed(records)), root / "two", 41,
                splits.SplitRatios())
            first_bytes = Path(first.path).read_bytes()
            second_bytes = Path(second.path).read_bytes()
            parsed = splits.SplitManifest.from_path(first.path)

        self.assertEqual(first_bytes, second_bytes)
        self.assertEqual(parsed.to_dict(), first.to_dict())
        payload = json.loads(first_bytes)
        self.assertEqual(payload["schema_version"], 1)
        self.assertEqual(payload["algorithm"], "group-signature-hamilton-v1")
        self.assertEqual(payload["tie_order"], ["train", "validation", "test"])
        self.assertIn("signatures", payload)
        self.assertIn("groups", payload)
        serialized = first_bytes.decode("utf-8")
        self.assertNotIn("timestamp", serialized.lower())
        self.assertNotIn(".tmp.", serialized)
        self.assertNotIn(str(Path(tmp).resolve()), serialized)

    def test_replace_failure_preserves_destination_and_removes_temporary(self):
        splits = importlib.import_module(SPLITS)
        with TemporaryDirectory() as tmp:
            run_dir = Path(tmp) / "run"
            run_dir.mkdir()
            destination = run_dir / "splits.json"
            destination.write_bytes(b"previous-manifest\n")
            with mock.patch("pinn.data.splits.os.replace", side_effect=OSError("injected")):
                with self.assertRaisesRegex(OSError, "injected"):
                    splits.write_split_manifest(
                        _Source(self._records(10)), run_dir, 1,
                        splits.SplitRatios())
            self.assertEqual(destination.read_bytes(), b"previous-manifest\n")
            self.assertEqual(list(run_dir.glob("splits.json.tmp.*")), [])

    def test_run_directory_beneath_source_corpus_is_rejected_before_write(self):
        splits = importlib.import_module(SPLITS)

        class CorpusSource(_Source):
            def __init__(self, records, data_root):
                super().__init__(records)
                self.data_root = data_root

        with TemporaryDirectory() as tmp:
            corpus = Path(tmp) / "simulation_data" / "Data"
            run_dir = corpus / "run"
            source = CorpusSource(self._records(10), corpus)
            with self.assertRaisesRegex(ValueError, "read-only corpus root"):
                splits.write_split_manifest(
                    source, run_dir, 1, splits.SplitRatios())
            self.assertFalse(run_dir.exists())

    def test_train_epoch_order_is_seeded_while_validation_and_test_are_fixed(self):
        splits = importlib.import_module(SPLITS)
        with TemporaryDirectory() as tmp:
            manifest = splits.write_split_manifest(
                _Source(self._records()), Path(tmp) / "run", 7,
                splits.SplitRatios())

        epoch_a = manifest.train_epoch_order(100)
        epoch_a_repeat = manifest.train_epoch_order(100)
        epoch_b = manifest.train_epoch_order(101)
        self.assertEqual(epoch_a, epoch_a_repeat)
        self.assertNotEqual(epoch_a, epoch_b)
        self.assertEqual(set(epoch_a), set(manifest.splits["train"]))
        for split_name in ("validation", "test"):
            fixed = manifest.fixed_order(split_name)
            self.assertEqual(fixed, tuple(sorted(fixed)))
            self.assertEqual(tuple(manifest.iter_split(split_name)), fixed)
        self.assertEqual(tuple(manifest.iter_split("train", epoch_seed=100)), epoch_a)

    def test_gold_only_group_round_trip_keeps_missing_base_out_of_record_label(self):
        splits = importlib.import_module(SPLITS)
        types = importlib.import_module(TYPES)
        records = self._records(9)
        records.append(SimpleNamespace(
            physical_key=types.PhysicalKey("hierarchical", 42),
            record_key=types.RecordKey("hierarchical", "gold", 42),
            stage_label=types.StageLabel.UNASSIGNED,
        ))
        with TemporaryDirectory() as tmp:
            manifest = splits.write_split_manifest(
                _Source(records), Path(tmp) / "run", 3, splits.SplitRatios())
            parsed = splits.SplitManifest.from_path(manifest.path)

        signature = ("hierarchical", types.MISSING_BASE, "UNASSIGNED")
        self.assertIn(signature, parsed.signatures)
        group = next(group for group in parsed.groups if group.physical_key.id == 42)
        self.assertEqual(group.signature, signature)
        self.assertEqual(group.records[0].stage_label, types.StageLabel.UNASSIGNED)
        self.assertNotEqual(group.records[0].stage_label, types.MISSING_BASE)

    def test_production_adapter_is_the_direct_writer_and_from_split_source(self):
        splits = importlib.import_module(SPLITS)
        adapter_module = importlib.import_module("pinn.data.adapter")
        with _fixtures.TinyCorpus() as corpus:
            adapter = adapter_module.AdmittedSetAdapter(
                root=corpus.data_root,
                blacklist_path=corpus.blacklist_path,
                precision="float32",
                device="cpu",
                run_dir=corpus.run_dir,
                version_metadata_path=corpus.version_metadata_path,
            )
            manifest = splits.write_split_manifest(
                adapter,
                run_dir=corpus.run_dir,
                seed=23,
                ratios=splits.SplitRatios(),
            )
            train = splits.StageIndex.from_split(adapter, manifest, "train")

        self.assertEqual(
            {group.physical_key for group in manifest.groups},
            {key.physical_key for key in adapter.record_keys()},
        )
        self.assertTrue(
            {key.physical_key for key in train.record_keys()}.issubset(
                manifest.physical_keys("train")
            )
        )
        self.assertEqual(train.gold_numeric_stage_count, 0)

    def test_tampered_manifest_counts_and_duplicate_groups_fail_to_parse(self):
        splits = importlib.import_module(SPLITS)
        with TemporaryDirectory() as tmp:
            manifest = splits.write_split_manifest(
                _Source(self._records(10)), Path(tmp) / "run", 5,
                splits.SplitRatios())
            payload = manifest.to_dict()

        bad_counts = json.loads(json.dumps(payload))
        bad_counts["signatures"][0]["counts"]["train"] += 1
        with self.assertRaisesRegex(ValueError, "Hamilton allocation"):
            splits.SplitManifest.from_dict(bad_counts)

        duplicate = json.loads(json.dumps(payload))
        duplicate["groups"].append(duplicate["groups"][0])
        with self.assertRaisesRegex(ValueError, "more than once"):
            splits.SplitManifest.from_dict(duplicate)


class SplitManifestContract(unittest.TestCase):
    def setUp(self):
        self.build = _require("build_split_manifest", SPLITS)
        self.PhysicalKey = _require("PhysicalKey", TYPES)
        self.RecordKey = _require("RecordKey", TYPES)
        self.StageLabel = _require("StageLabel", TYPES)

    # -- record helpers ------------------------------------------------------
    def _rec(self, fidelity, id_, label, variant="hierarchical"):
        return SimpleNamespace(
            physical_key=self.PhysicalKey(variant, id_),
            record_key=self.RecordKey(variant, fidelity, id_),
            stage_label=label)

    def _pair(self, id_, base_label):
        """A base/gold twin sharing one PhysicalKey (gold always UNASSIGNED)."""
        return [self._rec("base", id_, base_label),
                self._rec("gold", id_, self.StageLabel.UNASSIGNED)]

    def _run_dir(self, tmp):
        d = Path(tmp) / "run"
        d.mkdir(parents=True, exist_ok=True)
        return d

    # -- no leakage + persistence -------------------------------------------
    def test_base_gold_twins_share_one_split_and_no_key_spans(self):
        records = []
        for i in range(10):
            records.extend(self._pair(i, self.StageLabel.STAGE_0))
        with TemporaryDirectory() as tmp:
            manifest = self.build(_Source(records), seed=7, run_dir=self._run_dir(tmp))
        # Every physical key is assigned to exactly one split.
        assignment = {}
        for split_name, keys in manifest.splits.items():
            for rk in keys:
                pk = (rk.variant, rk.id)
                assignment.setdefault(pk, set()).add(split_name)
        for pk, splits in assignment.items():
            self.assertEqual(len(splits), 1, f"{pk} spans splits {splits}")

    def test_manifest_records_seed_ratios_and_algorithm(self):
        records = [r for i in range(20) for r in self._pair(i, self.StageLabel.STAGE_0)]
        with TemporaryDirectory() as tmp:
            manifest = self.build(_Source(records), seed=99, run_dir=self._run_dir(tmp))
        self.assertEqual(manifest.seed, 99)
        self.assertEqual(manifest.algorithm, "group-signature-hamilton-v1")
        self.assertEqual(set(manifest.ratios), {"train", "validation", "test"})
        self.assertAlmostEqual(manifest.ratios["train"], 0.8)

    # -- determinism ---------------------------------------------------------
    def test_same_seed_reproduces_bytes_and_input_order_is_irrelevant(self):
        base = [r for i in range(30) for r in self._pair(i, self.StageLabel.STAGE_0)]
        shuffled = list(reversed(base))
        with TemporaryDirectory() as t1, TemporaryDirectory() as t2:
            m1 = self.build(_Source(base), seed=5, run_dir=self._run_dir(t1))
            m2 = self.build(_Source(shuffled), seed=5, run_dir=self._run_dir(t2))
            b1 = Path(m1.path).read_bytes()
            b2 = Path(m2.path).read_bytes()
        self.assertEqual(b1, b2)

    def test_manifest_is_written_into_the_injected_run_dir(self):
        records = [r for i in range(10) for r in self._pair(i, self.StageLabel.STAGE_0)]
        with TemporaryDirectory() as tmp:
            run_dir = self._run_dir(tmp)
            manifest = self.build(_Source(records), seed=1, run_dir=run_dir)
            self.assertTrue(Path(manifest.path).is_file())
            self.assertEqual(Path(manifest.path).parent.resolve(), run_dir.resolve())

    # -- Hamilton apportionment ---------------------------------------------
    def test_single_signature_hamilton_counts_and_tie_order(self):
        # 10 identical-signature groups -> 8 train / 1 val / 1 test.
        records = [r for i in range(10) for r in self._pair(i, self.StageLabel.STAGE_0)]
        with TemporaryDirectory() as tmp:
            manifest = self.build(_Source(records), seed=3, run_dir=self._run_dir(tmp))
        counts = {name: len({(rk.variant, rk.id) for rk in keys})
                  for name, keys in manifest.splits.items()}
        self.assertEqual(counts["train"], 8)
        self.assertEqual(counts["validation"], 1)
        self.assertEqual(counts["test"], 1)

    def test_seed_changes_identities_not_counts(self):
        records = [r for i in range(30) for r in self._pair(i, self.StageLabel.STAGE_0)]
        with TemporaryDirectory() as t1, TemporaryDirectory() as t2:
            m_a = self.build(_Source(records), seed=1, run_dir=self._run_dir(t1))
            m_b = self.build(_Source(records), seed=2, run_dir=self._run_dir(t2))
        counts_a = {n: len(v) for n, v in m_a.splits.items()}
        counts_b = {n: len(v) for n, v in m_b.splits.items()}
        self.assertEqual(counts_a, counts_b)
        train_a = {(rk.variant, rk.id) for rk in m_a.splits["train"]}
        train_b = {(rk.variant, rk.id) for rk in m_b.splits["train"]}
        self.assertNotEqual(train_a, train_b)

    # -- GAP-39-08 signature invariant --------------------------------------
    def test_present_gold_signature_value_is_never_numeric(self):
        # A gold record carrying a numeric label is a hard invariant failure.
        bad = [self._rec("base", 0, self.StageLabel.STAGE_0),
               self._rec("gold", 0, self.StageLabel.STAGE_0)]
        with TemporaryDirectory() as tmp:
            with self.assertRaises((ValueError, AssertionError)):
                self.build(_Source(bad), seed=1, run_dir=self._run_dir(tmp))

    def test_missing_gold_uses_the_explicit_sentinel(self):
        MISSING_GOLD = _require("MISSING_GOLD", TYPES)
        records = [self._rec("base", i, self.StageLabel.STAGE_0) for i in range(5)]  # no gold
        with TemporaryDirectory() as tmp:
            manifest = self.build(_Source(records), seed=1, run_dir=self._run_dir(tmp))
        signatures = {sig for sig in manifest.signatures}
        self.assertTrue(any(MISSING_GOLD in sig for sig in signatures),
                        f"missing-gold sentinel absent from signatures: {signatures}")

    # -- GAP-39-11 MISSING_BASE (split-only) --------------------------------
    def test_gold_only_group_uses_missing_base_and_is_assigned_once(self):
        MISSING_BASE = _require("MISSING_BASE", TYPES)
        # A physical key whose base was admission-rejected: gold only.
        records = [self._rec("gold", 42, self.StageLabel.UNASSIGNED)]
        for i in range(9):  # padding groups so the split has members
            records.extend(self._pair(i, self.StageLabel.STAGE_0))
        with TemporaryDirectory() as tmp:
            manifest = self.build(_Source(records), seed=1, run_dir=self._run_dir(tmp))
        # The gold-only group carries a distinct (variant, MISSING_BASE, UNASSIGNED)
        # signature and is assigned to exactly one split.
        self.assertTrue(any(MISSING_BASE in sig for sig in manifest.signatures))
        placements = [name for name, keys in manifest.splits.items()
                      if any(rk.id == 42 for rk in keys)]
        self.assertEqual(len(placements), 1)

    def test_missing_base_never_enters_a_numeric_pool(self):
        # MISSING_BASE is a split-signature sentinel, not a persisted label, so
        # it must not be a StageLabel value.
        StageLabel = self.StageLabel
        MISSING_BASE = _require("MISSING_BASE", TYPES)
        self.assertNotIn(MISSING_BASE, set(StageLabel))


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
