"""Boundary tables for the pre-registered scorecard rules (FEAS-01)."""

from __future__ import annotations

import math
import unittest

from pinn.verification import feasibility_scorecard as rules
from pinn.verification.feasibility_scorecard import OwnerRouted, load_scorecard


def _fn(test: unittest.TestCase, name: str):
    function = getattr(rules, name, None)
    test.assertIsNotNone(function, name)
    return function


class CountsTests(unittest.TestCase):
    def test_true_when_tier_counts_and_error_is_strictly_below_formula(self):
        counts = _fn(self, "counts")
        card = load_scorecard()
        self.assertTrue(counts(1, 0.09, 0.0900001, scorecard=card))
        self.assertTrue(counts(1, math.nextafter(0.09, 0.0), 0.09, scorecard=card))

    def test_false_when_error_equals_formula(self):
        counts = _fn(self, "counts")
        card = load_scorecard()
        self.assertFalse(counts(1, 0.09, 0.09, scorecard=card))
        self.assertFalse(counts(1, math.nextafter(0.09, 1.0), 0.09, scorecard=card))

    def test_false_when_tier_is_below_minimum(self):
        counts = _fn(self, "counts")
        self.assertFalse(counts(0, 0.05, 0.9, scorecard=load_scorecard()))

    def test_false_when_error_or_formula_is_non_finite(self):
        counts = _fn(self, "counts")
        card = load_scorecard()
        self.assertFalse(counts(1, float("nan"), 0.1, scorecard=card))
        self.assertFalse(counts(1, 0.05, float("nan"), scorecard=card))

    def test_owner_routed_when_formula_is_not_applicable(self):
        counts = _fn(self, "counts")
        with self.assertRaises(OwnerRouted) as caught:
            counts(1, 0.05, None, scorecard=load_scorecard())
        self.assertIn("not applicable", str(caught.exception))


class G2FiresTests(unittest.TestCase):
    def test_fires_when_two_of_three_are_below_tier_1(self):
        g2_fires = _fn(self, "g2_fires")
        self.assertTrue(g2_fires([0, 0, 1], scorecard=load_scorecard()))

    def test_does_not_fire_when_only_one_is_below_tier_1(self):
        g2_fires = _fn(self, "g2_fires")
        self.assertFalse(g2_fires([0, 1, 1], scorecard=load_scorecard()))

    def test_wrong_panel_size_raises(self):
        g2_fires = _fn(self, "g2_fires")
        with self.assertRaises(ValueError):
            g2_fires([0, 0], scorecard=load_scorecard())


class DecisionVerdictTests(unittest.TestCase):
    def _call(self, **overrides):
        decision_verdict = _fn(self, "decision_verdict")
        kwargs = {
            "g2_fired": False,
            "sweep_rescued": False,
            "rung2b_counts": [True, True, False],
            "rung3_counts": [True] * 12 + [False] * 4,
            "control_branch": "a",
            "rung1_beats_formula": [True, True, False],
            "scorecard": load_scorecard(),
        }
        kwargs.update(overrides)
        return decision_verdict(**kwargs)

    def test_rethink_when_g2_fired_and_sweep_rescued_nothing(self):
        verdict = self._call(
            g2_fired=True,
            sweep_rescued=False,
            rung2b_counts=None,
            rung3_counts=None,
            control_branch=None,
            rung1_beats_formula=None,
        )
        self.assertEqual(verdict["verdict"], "RETHINK-REPRESENTATION")
        self.assertFalse(verdict["representation_limit_qualifier"])

    def test_rescue_is_owner_routed(self):
        with self.assertRaises(OwnerRouted) as caught:
            self._call(g2_fired=True, sweep_rescued=True)
        self.assertIn("owner checkpoint 4", str(caught.exception))

    def test_go_when_rung2b_rung3_and_control_all_pass(self):
        verdict = self._call()
        self.assertEqual(verdict["verdict"], "GO")
        self.assertFalse(verdict["representation_limit_qualifier"])
        self.assertEqual(verdict["reasons"], [])

    def test_pivot_names_the_rung3_clause(self):
        verdict = self._call(rung3_counts=[True] * 11 + [False] * 5)
        self.assertEqual(verdict["verdict"], "PIVOT-TRAINING")
        self.assertTrue(any("Rung 3" in reason for reason in verdict["reasons"]))

    def test_pivot_names_the_control_clause(self):
        verdict = self._call(control_branch="b")
        self.assertEqual(verdict["verdict"], "PIVOT-TRAINING")
        self.assertTrue(any("control" in reason for reason in verdict["reasons"]))

    def test_representation_qualifier_when_rung1_beats_formula_once(self):
        verdict = self._call(rung1_beats_formula=[True, False, False])
        self.assertTrue(verdict["representation_limit_qualifier"])

    def test_wrong_rung3_length_raises(self):
        with self.assertRaises(ValueError):
            self._call(rung3_counts=[True] * 15)


class StepsBudgetTests(unittest.TestCase):
    def test_three_hour_cap_at_twelve_seconds_per_step(self):
        steps_budget = _fn(self, "steps_budget")
        self.assertEqual(steps_budget(3.0, 600.0, 50, scorecard=load_scorecard()), 900)

    def test_timing_run_shorter_than_minimum_raises(self):
        steps_budget = _fn(self, "steps_budget")
        with self.assertRaises(ValueError):
            steps_budget(3.0, 600.0, 49, scorecard=load_scorecard())

    def test_non_integer_timing_steps_raise(self):
        steps_budget = _fn(self, "steps_budget")
        with self.assertRaises(ValueError):
            steps_budget(3.0, 600.0, 50.5, scorecard=load_scorecard())


class StillImprovingTests(unittest.TestCase):
    def test_exact_ten_percent_drop_is_improving(self):
        still_improving = _fn(self, "still_improving")
        readings = [(750, 0.20), (1000, 0.18)]
        self.assertTrue(still_improving(readings, 1000, scorecard=load_scorecard()))

    def test_drop_just_under_ten_percent_is_not_improving(self):
        still_improving = _fn(self, "still_improving")
        readings = [(750, 0.20), (1000, 0.1801)]
        self.assertFalse(still_improving(readings, 1000, scorecard=load_scorecard()))

    def test_no_finite_final_reading_is_not_improving(self):
        still_improving = _fn(self, "still_improving")
        readings = [(750, 0.20), (1000, float("nan"))]
        self.assertFalse(still_improving(readings, 1000, scorecard=load_scorecard()))

    def test_finite_final_without_reference_is_improving(self):
        still_improving = _fn(self, "still_improving")
        self.assertTrue(still_improving([(1000, 0.5)], 1000, scorecard=load_scorecard()))

    def test_one_step_above_the_drop_bound_is_not_improving(self):
        still_improving = _fn(self, "still_improving")
        bound = (1.0 - 0.1) * 0.20
        readings = [(750, 0.20), (1000, math.nextafter(bound, 1.0))]
        self.assertFalse(still_improving(readings, 1000, scorecard=load_scorecard()))


class BudgetOutcomeTests(unittest.TestCase):
    def test_first_pass_while_improving_extends(self):
        budget_outcome = _fn(self, "budget_outcome")
        result = budget_outcome(
            [(750, 0.20), (1000, 0.18)],
            1000,
            extended=False,
            scorecard=load_scorecard(),
        )
        self.assertEqual(result["outcome"], "extend")
        self.assertEqual(result["new_budget_steps"], 2000)

    def test_extended_pass_while_improving_is_inconclusive_with_rate(self):
        budget_outcome = _fn(self, "budget_outcome")
        best_ref = 0.20
        best_final = 0.18
        result = budget_outcome(
            [(750, best_ref), (1000, best_final)],
            1000,
            extended=True,
            scorecard=load_scorecard(),
        )
        expected = (best_ref - best_final) / (best_ref * 0.25 * 1000)
        self.assertEqual(result["outcome"], "inconclusive")
        self.assertEqual(result["rate_per_step"], expected)

    def test_not_improving_is_complete(self):
        budget_outcome = _fn(self, "budget_outcome")
        result = budget_outcome(
            [(750, 0.20), (1000, 0.19)],
            1000,
            extended=False,
            scorecard=load_scorecard(),
        )
        self.assertEqual(result, {"outcome": "complete"})


class ScoringCadenceTests(unittest.TestCase):
    def test_gap_equal_to_the_fraction_is_ok(self):
        scoring_cadence_ok = _fn(self, "scoring_cadence_ok")
        steps = list(range(0, 1001, 50))
        self.assertTrue(scoring_cadence_ok(steps, 1000, scorecard=load_scorecard()))

    def test_gap_one_past_the_fraction_is_not_ok(self):
        scoring_cadence_ok = _fn(self, "scoring_cadence_ok")
        self.assertFalse(
            scoring_cadence_ok([0, 51, 1000], 1000, scorecard=load_scorecard())
        )

    def test_missing_endpoint_is_not_ok(self):
        scoring_cadence_ok = _fn(self, "scoring_cadence_ok")
        card = load_scorecard()
        self.assertFalse(scoring_cadence_ok([50, 1000], 1000, scorecard=card))
        self.assertFalse(scoring_cadence_ok([0, 50], 1000, scorecard=card))


class PolishShouldStopTests(unittest.TestCase):
    def test_stops_at_five_calls_or_a_quarter_of_adam_time(self):
        polish_should_stop = _fn(self, "polish_should_stop")
        card = load_scorecard()
        self.assertTrue(polish_should_stop(5, 1.0, 100.0, scorecard=card))
        self.assertTrue(polish_should_stop(0, 25.0, 100.0, scorecard=card))
        self.assertFalse(polish_should_stop(4, 24.9, 100.0, scorecard=card))
        self.assertFalse(
            polish_should_stop(4, math.nextafter(25.0, 0.0), 100.0, scorecard=card)
        )


class BetterStateTests(unittest.TestCase):
    def test_exact_tie_keeps_adam(self):
        better_state = _fn(self, "better_state")
        state = {"E": 0.05, "eps_h": 1e-3}
        self.assertEqual(better_state(state, dict(state), scorecard=load_scorecard()), "adam")

    def test_lower_energy_error_at_equal_position_error_wins(self):
        better_state = _fn(self, "better_state")
        adam = {"E": 0.05, "eps_h": 1e-3}
        polish = {"E": 0.05, "eps_h": math.nextafter(1e-3, 0.0)}
        self.assertEqual(better_state(adam, polish, scorecard=load_scorecard()), "polish")

    def test_non_finite_polish_position_error_loses(self):
        better_state = _fn(self, "better_state")
        adam = {"E": 0.05, "eps_h": 1e-3}
        polish = {"E": float("nan"), "eps_h": 0.0}
        self.assertEqual(better_state(adam, polish, scorecard=load_scorecard()), "adam")


class G1FiresTests(unittest.TestCase):
    def test_fires_at_the_threshold(self):
        g1_fires = _fn(self, "g1_fires")
        result = g1_fires({900: 0.01, 951: 0.0}, scorecard=load_scorecard())
        self.assertTrue(result["fires"])
        self.assertIn("Phase 61", result["outcome"])
        self.assertEqual(list(result["checked_checkpoints"]), [900, 951])

    def test_does_not_fire_just_below_the_threshold(self):
        g1_fires = _fn(self, "g1_fires")
        result = g1_fires(
            {900: math.nextafter(0.01, 0.0), 951: 0.0},
            scorecard=load_scorecard(),
        )
        self.assertFalse(result["fires"])
        self.assertEqual(result["outcome"], "proceed")

    def test_non_finite_share_is_not_determinable(self):
        g1_fires = _fn(self, "g1_fires")
        result = g1_fires({900: float("nan"), 951: 0.0}, scorecard=load_scorecard())
        self.assertIsNone(result["fires"])
        self.assertEqual(result["outcome"], "not determinable (owner-routed)")

    def test_missing_checkpoint_raises(self):
        g1_fires = _fn(self, "g1_fires")
        with self.assertRaises(ValueError):
            g1_fires({900: 0.0}, scorecard=load_scorecard())


class Jx1ReadingTests(unittest.TestCase):
    def test_named_readings_at_the_two_thresholds_and_between(self):
        jx1_reading = _fn(self, "jx1_reading")
        card = load_scorecard()
        self.assertIn("supports", jx1_reading(1e-4, scorecard=card))
        self.assertIn("falsifies", jx1_reading(1e-2, scorecard=card))
        self.assertIn("neither", jx1_reading(5e-3, scorecard=card))

    def test_one_step_off_each_bound(self):
        jx1_reading = _fn(self, "jx1_reading")
        card = load_scorecard()
        self.assertIn("supports", jx1_reading(math.nextafter(1e-4, 0.0), scorecard=card))
        self.assertIn("neither", jx1_reading(math.nextafter(1e-4, 1.0), scorecard=card))
        self.assertIn("neither", jx1_reading(math.nextafter(1e-2, 0.0), scorecard=card))
        self.assertIn("falsifies", jx1_reading(math.nextafter(1e-2, 1.0), scorecard=card))

    def test_non_finite_is_not_determinable(self):
        jx1_reading = _fn(self, "jx1_reading")
        self.assertIn("not determinable", jx1_reading(float("nan"), scorecard=load_scorecard()))


if __name__ == "__main__":
    unittest.main()
