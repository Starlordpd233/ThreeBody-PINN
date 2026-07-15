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
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from types import SimpleNamespace

from tests.phase39 import _SKIP_PHRASE

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
