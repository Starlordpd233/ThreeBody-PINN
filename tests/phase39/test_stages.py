"""Phase 39 Wave-0 contract — the sole record-level Stage-0/1 classifier.

Deferred contract for ``pinn.data.stages.classify_stage_label(record,
interim_s0)`` (GAP-39-03 + GAP-39-08). Every test SKIPs via the localized
``_require`` helper (importing the single ``tests.phase39._SKIP_PHRASE``) until
the production classifier lands in Wave 1/2; it then turns green.

Authoritative membership (GAP-39-03; ``ctl_instruction.md:23-28,138-198``):

* Only ORIGINAL/BASE hierarchical Set 1a records may receive a numeric label.
* Stage 0 is evaluated BEFORE the collapsed Stage 1a/1b branch.
* Every gold record (including hierarchical Set 2a), every non-Set-1a record,
  and every degenerate-Lmax record is ``UNASSIGNED``.
* The Stage-1 criterion is strict ``s_min > s0``; equality is NOT Stage 0/1.
* Stage 2-6 are NEVER returned; the only outputs are ``0``, ``1``,
  ``UNASSIGNED``, and paired base/gold twins yield ``gold_numeric_stage_count == 0``.

Production ownership remains in Plans 02/03; this file takes no production
ownership and constructs only in-memory attribute-bearing stand-in records.
"""

import math
import unittest
from types import SimpleNamespace

from tests.phase39 import _SKIP_PHRASE

STAGES_MODULE = "pinn.data.stages"
TYPES_MODULE = "pinn.data.types"

INTERIM_S0 = 0.01


def _require(symbol, module):
    import importlib
    try:
        mod = importlib.import_module(module)
    except ImportError:
        raise unittest.SkipTest(f"{_SKIP_PHRASE} {module}.{symbol}")
    if not hasattr(mod, symbol):
        raise unittest.SkipTest(f"{_SKIP_PHRASE} {module}.{symbol}")
    return getattr(mod, symbol)


class ClassifierContract(unittest.TestCase):
    """The classifier is attribute-based over ``variant``, ``fidelity``, ``E``,
    ``l_ratio`` (angular-momentum ratio), ``Q``, and ``s_min``."""

    def setUp(self):
        self.classify = _require("classify_stage_label", STAGES_MODULE)
        self.StageLabel = _require("StageLabel", TYPES_MODULE)
        self.Variant = _require("Variant", TYPES_MODULE)
        self.Fidelity = _require("Fidelity", TYPES_MODULE)

    # -- record builders -----------------------------------------------------
    def _rec(self, **over):
        """A base hierarchical record with Stage-0-valid invariants by default."""
        fields = dict(
            variant=self.Variant.HIERARCHICAL,
            fidelity=self.Fidelity.BASE,
            E=-0.8,           # < -0.5
            l_ratio=0.7,      # > 0.5
            Q=1.0,            # in [0.7, 1.3]
            s_min=0.5,        # > s0
        )
        fields.update(over)
        return SimpleNamespace(**fields)

    def _labels(self):
        return self.StageLabel.STAGE_0, self.StageLabel.STAGE_1, self.StageLabel.UNASSIGNED

    # -- Stage 0 -------------------------------------------------------------
    def test_base_set1a_stage0(self):
        self.assertEqual(self.classify(self._rec(), INTERIM_S0), self.StageLabel.STAGE_0)

    def test_gold_stage0_invariants_are_unassigned(self):
        rec = self._rec(fidelity=self.Fidelity.GOLD)
        self.assertEqual(self.classify(rec, INTERIM_S0), self.StageLabel.UNASSIGNED)

    # -- Stage 1a / 1b collapse ---------------------------------------------
    def test_base_stage1a_collapses_to_stage1(self):
        rec = self._rec(E=-0.3, l_ratio=0.7)   # -0.5 <= E < -0.1, l_ratio > 0.5
        self.assertEqual(self.classify(rec, INTERIM_S0), self.StageLabel.STAGE_1)

    def test_base_stage1b_collapses_to_stage1(self):
        rec = self._rec(E=-0.8, l_ratio=0.3)   # E < -0.5, 0.1 <= l_ratio < 0.5
        self.assertEqual(self.classify(rec, INTERIM_S0), self.StageLabel.STAGE_1)

    def test_gold_stage1a_and_stage1b_are_unassigned(self):
        for over in (dict(E=-0.3, l_ratio=0.7), dict(E=-0.8, l_ratio=0.3)):
            rec = self._rec(fidelity=self.Fidelity.GOLD, **over)
            self.assertEqual(self.classify(rec, INTERIM_S0), self.StageLabel.UNASSIGNED)

    # -- fidelity / variant guard -------------------------------------------
    def test_standard_records_are_unassigned(self):
        for fid in (self.Fidelity.BASE, self.Fidelity.GOLD):
            rec = self._rec(variant=self.Variant.STANDARD, fidelity=fid)
            self.assertEqual(self.classify(rec, INTERIM_S0), self.StageLabel.UNASSIGNED)

    def test_base_hierarchical_outside_conjunction_is_unassigned(self):
        # Q out of [0.7, 1.3] fails the common conjunction for both stages.
        rec = self._rec(Q=2.0)
        self.assertEqual(self.classify(rec, INTERIM_S0), self.StageLabel.UNASSIGNED)

    # -- strict s_min > s0 boundary -----------------------------------------
    def test_s_min_equal_s0_is_not_stage0(self):
        rec = self._rec(s_min=INTERIM_S0)   # equality excluded (strict >)
        self.assertEqual(self.classify(rec, INTERIM_S0), self.StageLabel.UNASSIGNED)

    def test_s_min_just_above_s0_is_stage0(self):
        rec = self._rec(s_min=math.nextafter(INTERIM_S0, math.inf))
        self.assertEqual(self.classify(rec, INTERIM_S0), self.StageLabel.STAGE_0)

    # -- degenerate Lmax -----------------------------------------------------
    def test_degenerate_lmax_is_unassigned(self):
        rec = self._rec(l_ratio=float("nan"))
        self.assertEqual(self.classify(rec, INTERIM_S0), self.StageLabel.UNASSIGNED)

    # -- ordering + closed output set ---------------------------------------
    def test_stage0_is_evaluated_before_stage1(self):
        # A Stage-0-valid record must return STAGE_0, never STAGE_1.
        self.assertEqual(self.classify(self._rec(), INTERIM_S0), self.StageLabel.STAGE_0)

    def test_output_is_always_one_of_three_labels_no_stage_2_to_6(self):
        allowed = set(self._labels())
        samples = [
            self._rec(),
            self._rec(E=-0.3, l_ratio=0.7),
            self._rec(E=-0.8, l_ratio=0.3),
            self._rec(fidelity=self.Fidelity.GOLD),
            self._rec(variant=self.Variant.STANDARD),
            self._rec(Q=5.0),
            self._rec(l_ratio=float("nan")),
        ]
        for rec in samples:
            self.assertIn(self.classify(rec, INTERIM_S0), allowed)
        # The closed enum exposes no Stage 2-6 member.
        for forbidden in ("STAGE_2", "STAGE_3", "STAGE_4", "STAGE_5", "STAGE_6"):
            self.assertFalse(hasattr(self.StageLabel, forbidden),
                             f"StageLabel must not expose {forbidden}")

    def test_paired_base_gold_yields_zero_gold_numeric_labels(self):
        StageLabel = self.StageLabel
        numeric = {StageLabel.STAGE_0, StageLabel.STAGE_1}
        pairs = [
            (self._rec(), self._rec(fidelity=self.Fidelity.GOLD)),
            (self._rec(E=-0.3, l_ratio=0.7),
             self._rec(fidelity=self.Fidelity.GOLD, E=-0.3, l_ratio=0.7)),
            (self._rec(E=-0.8, l_ratio=0.3),
             self._rec(fidelity=self.Fidelity.GOLD, E=-0.8, l_ratio=0.3)),
        ]
        gold_numeric_stage_count = 0
        for base, gold in pairs:
            self.assertIn(self.classify(base, INTERIM_S0), numeric)   # base IS numeric
            if self.classify(gold, INTERIM_S0) in numeric:
                gold_numeric_stage_count += 1
        self.assertEqual(gold_numeric_stage_count, 0)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
