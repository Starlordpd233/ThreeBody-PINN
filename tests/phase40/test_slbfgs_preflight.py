"""Phase 40 — sL-BFGS preflight typed-refusal contract (TRAIN-07).

Stages 0-2 pass the gate; stages >= 3 raise StochasticLBFGSNotImplemented
with a non-empty message and a .stage field. This is a typed stop, never a
silent skip — silently routing an unimplemented sL-BFGS stage would deviate
from the locked spec without any signal (SPEC Prohibition 2).

Grounding: ctl_instruction.md routes stages 3-6 to stochastic L-BFGS
(PLAT-02, deferred beyond the v2.0 slice).
"""
from __future__ import annotations

import unittest

from tests.phase40.test_prohibitions import _require

MODULE = "pinn.training.slbfgs_preflight"

StochasticLBFGSNotImplemented = _require("StochasticLBFGSNotImplemented", MODULE)
check_stage_preflight = _require("check_stage_preflight", MODULE)


class PreflightAcceptTests(unittest.TestCase):
    def test_stage_0_returns_none(self):
        self.assertIsNone(check_stage_preflight(0))

    def test_stage_1_returns_none(self):
        self.assertIsNone(check_stage_preflight(1))

    def test_stage_2_returns_none(self):
        self.assertIsNone(check_stage_preflight(2))


class PreflightRefusalTests(unittest.TestCase):
    def test_stage_3_raises_typed_refusal(self):
        with self.assertRaises(StochasticLBFGSNotImplemented) as ctx:
            check_stage_preflight(3)
        self.assertEqual(ctx.exception.stage, 3)
        self.assertTrue(str(ctx.exception), "exception message is empty")

    def test_stage_4_raises_with_stage_field(self):
        with self.assertRaises(StochasticLBFGSNotImplemented) as ctx:
            check_stage_preflight(4)
        self.assertEqual(ctx.exception.stage, 4)

    def test_stage_5_raises_with_stage_field(self):
        with self.assertRaises(StochasticLBFGSNotImplemented) as ctx:
            check_stage_preflight(5)
        self.assertEqual(ctx.exception.stage, 5)

    def test_stage_6_raises_with_stage_field(self):
        with self.assertRaises(StochasticLBFGSNotImplemented) as ctx:
            check_stage_preflight(6)
        self.assertEqual(ctx.exception.stage, 6)

    def test_refusal_message_is_non_empty(self):
        for stage in (3, 4, 5, 6):
            with self.subTest(stage=stage), self.assertRaises(StochasticLBFGSNotImplemented) as ctx:
                check_stage_preflight(stage)
            self.assertTrue(str(ctx.exception), f"stage {stage} refusal message is empty")


class ExceptionShapeTests(unittest.TestCase):
    def test_exception_subclasses_exception(self):
        self.assertTrue(issubclass(StochasticLBFGSNotImplemented, Exception))

    def test_exception_stores_stage_attribute(self):
        exc = StochasticLBFGSNotImplemented(5)
        self.assertEqual(exc.stage, 5)


if __name__ == "__main__":
    unittest.main()
