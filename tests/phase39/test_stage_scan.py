"""Phase 39 Wave-0 contract — the Thrust-A Stage-0 population scan (DATA-06).

GAP-39-03 / GAP-39-08: the scan CONSUMES persisted ``stage_label`` values (it
never reclassifies), only original/base hierarchical Set 1a carries a numeric
label, and every gold record is ``UNASSIGNED`` so ``gold_numeric_stage_count``
is exactly zero. The Stage-0 membership predicate is the authoritative CTL
conjunction with strict ``s_min > s0`` (``ctl_instruction.md:23-28,138-198``);
equality is excluded. This module takes no production ownership.

Deferred contract for ``pinn.data.stage_scan`` (every test SKIPs via the
localized ``_require`` helper until production lands).

DATA-06 fatal mechanics (VALIDATION 39-06-01/02): the fatal-class signal binds
EXCLUSIVELY to the admitted/full Stage-0 count — 239 is fatal, 240 is nonfatal,
and full >= 240 stays nonfatal even when a retained train-split diagnostic is
below 240. ``stage0_train_split_count`` is Phase-40 seam evidence only and never
drives ``StageZeroUnderpopulated`` or the CLI exit.
"""

import importlib
import unittest
from types import SimpleNamespace

from tests.phase39 import _SKIP_PHRASE

STAGE_SCAN = "pinn.data.stage_scan"
TYPES = "pinn.data.types"


def _require(symbol, module):
    try:
        mod = importlib.import_module(module)
    except ImportError:
        raise unittest.SkipTest(f"{_SKIP_PHRASE} {module}.{symbol}")
    if not hasattr(mod, symbol):
        raise unittest.SkipTest(f"{_SKIP_PHRASE} {module}.{symbol}")
    return getattr(mod, symbol)


class _ReportSource:
    def __init__(self, records):
        self._records = list(records)

    def admitted_records(self):
        return tuple(self._records)


class PopulationReportContract(unittest.TestCase):
    def setUp(self):
        self.build = _require("build_population_report", STAGE_SCAN)
        self.RecordKey = _require("RecordKey", TYPES)
        self.StageLabel = _require("StageLabel", TYPES)

    # -- record helpers ------------------------------------------------------
    def _base0(self, id_, s_min):
        return SimpleNamespace(record_key=self.RecordKey("hierarchical", "base", id_),
                               stage_label=self.StageLabel.STAGE_0, s_min=s_min)

    def _base1(self, id_):
        return SimpleNamespace(record_key=self.RecordKey("hierarchical", "base", id_),
                               stage_label=self.StageLabel.STAGE_1, s_min=0.5)

    def _gold(self, id_):
        return SimpleNamespace(record_key=self.RecordKey("hierarchical", "gold", id_),
                               stage_label=self.StageLabel.UNASSIGNED, s_min=0.5)

    def _std(self, id_):
        return SimpleNamespace(record_key=self.RecordKey("standard", "base", id_),
                               stage_label=self.StageLabel.UNASSIGNED, s_min=0.5)

    def _source(self, n_stage0, n_stage1=5, n_gold=10, n_standard=5):
        recs = [self._base0(i, 0.02 + i * 1e-4) for i in range(n_stage0)]
        recs += [self._base1(10_000 + i) for i in range(n_stage1)]
        recs += [self._gold(20_000 + i) for i in range(n_gold)]
        recs += [self._std(30_000 + i) for i in range(n_standard)]
        return _ReportSource(recs)

    # -- base-only labels + zero-gold invariant -----------------------------
    def test_counts_are_base_only_and_gold_numeric_count_is_zero(self):
        report = self.build(self._source(240, n_stage1=5, n_gold=10), interim_s0=0.01)
        self.assertEqual(report.stages["0"].record_count, 240)
        self.assertEqual(report.stages["1"].record_count, 5)
        self.assertEqual(report.gold_numeric_stage_count, 0)
        self.assertEqual(report.unassigned_by_fidelity["gold"], 10)

    def test_s_min_distribution_is_stage0_only_and_sorted(self):
        report = self.build(self._source(240), interim_s0=0.01)
        dist = report.s_min.values
        self.assertEqual(len(dist), 240)                 # Stage-0 records only
        self.assertEqual(list(dist), sorted(dist))       # auditable sorted order

    def test_interim_s0_is_an_input_seam_not_mutated(self):
        report = self.build(self._source(240), interim_s0=0.01)
        self.assertEqual(report.interim_s0, 0.01)

    def test_adding_gold_does_not_change_stage_counts_or_fatal(self):
        few_gold = self.build(self._source(240, n_gold=2), interim_s0=0.01)
        many_gold = self.build(self._source(240, n_gold=500), interim_s0=0.01)
        self.assertEqual(few_gold.stages["0"].record_count,
                         many_gold.stages["0"].record_count)
        self.assertEqual(few_gold.gold_numeric_stage_count,
                         many_gold.gold_numeric_stage_count)
        self.assertFalse(bool(few_gold.fatal))
        self.assertFalse(bool(many_gold.fatal))

    # -- DATA-06 fatal boundary (full/admitted count is the sole operand) ----
    def test_full_count_239_is_fatal(self):
        report = self.build(self._source(239), interim_s0=0.01)
        self.assertTrue(bool(report.fatal))
        self.assertEqual(report.fatal.threshold, 240)
        self.assertEqual(report.fatal.observed, 239)

    def test_full_count_240_is_nonfatal(self):
        report = self.build(self._source(240), interim_s0=0.01)
        self.assertFalse(bool(report.fatal))

    def test_full_ge_240_with_low_train_split_is_nonfatal(self):
        # stage0_train_split_count is diagnostic Phase-40 evidence only; a train
        # count below 240 must NOT make a full>=240 set fatal.
        report = self.build(self._source(250), interim_s0=0.01,
                            stage0_train_split_count=100)
        self.assertFalse(bool(report.fatal))
        self.assertEqual(report.stage0_train_split_count, 100)


class ScanCliContract(unittest.TestCase):
    def test_main_is_a_callable_cli_seam(self):
        main = _require("main", STAGE_SCAN)
        self.assertTrue(callable(main))


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
