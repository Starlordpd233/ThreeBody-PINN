"""Plan 67-05 task 67-05-02: the prospective contrast and confirmation rules.

D-08/D-09/D-10/D-11 (through 67-RESEARCH's interpretation recommendation),
committed before any registration exists: the final-quarter improvement rule
at its exact boundary, the matched-contrast rule (each noncontrol arm against
its registered control — d12, lr1e-4, its own backbone's raw input, or
lap10), the direction/relative-effect/tier-qualification arithmetic at the
exact 20 percent line, the three-case confirmation requiring the same
direction on main and both repeats with no unsettled endpoint, and the
experiment-level confirmation over every declared noncontrol contrast.
Adjacent-time hidden-state similarity stays associated descriptive evidence
(no cosine threshold, no causal claim), an observed fit is preserved
separately from cause confirmation, loss stays context and GAP-59-08 stays
explicit. Pure synthetic dicts only; no run directory, corpus or timing is
touched.
"""

from __future__ import annotations

import math
import unittest

CASES = {
    "main": ("hierarchical/gold/1632", 42),
    "repeat-system": ("hierarchical/gold/851", 42),
    "repeat-seed": ("hierarchical/gold/1632", 41),
}


def _p67():
    """The pure rule module, imported lazily so a missing symbol fails per test."""
    from pinn.verification import diagnostic_phase67

    return diagnostic_phase67


def _reading(
    *,
    e=1.0,
    tier=0,
    unsettled=False,
    arm="d2",
    orbit_key="hierarchical/gold/1632",
    seed=42,
    experiment="exp02",
    problems=(),
    setting_problems=(),
    layer_trace=None,
):
    """One mechanically clean Phase 67 endpoint reading, as the reader emits."""
    return {
        "identity": {
            "experiment": experiment,
            "arm": arm,
            "case": "main",
            "orbit_key": orbit_key,
            "seed": seed,
        },
        "mechanical_problems": list(problems),
        "setting_problems": list(setting_problems),
        "unsettled": unsettled,
        "scores": {"network": {"E": e, "tier": tier}},
        "layer_trace": [
            {"step": 0, "layers": [{"name": "input", "order": 0,
                                    "adjacent_cosine_mean": 0.99}]}
        ] if layer_trace is None else layer_trace,
    }


def _checkpoints(mid, end, first=4.0):
    """Three score checkpoints at N/2, 3N/4 and N."""
    return [
        {"step": 50, "score": {"E": first, "tier": 0}},
        {"step": 75, "score": {"E": mid, "tier": 0}},
        {"step": 100, "score": {"E": end, "tier": 0}},
    ]


def _three_cases(arm_e, control_e, *, arm_tier=0, control_tier=0,
                 arm="d2", control="d12", unsettled=False, problems=()):
    """The three registered cases of one contrast, arm and control paired."""
    return {
        role: {
            "arm": _reading(
                e=arm_e, tier=arm_tier, unsettled=unsettled, arm=arm,
                orbit_key=orbit, seed=seed, problems=problems,
            ),
            "control": _reading(
                e=control_e, tier=control_tier, arm=control,
                orbit_key=orbit, seed=seed,
            ),
        }
        for role, (orbit, seed) in CASES.items()
    }


class RuleConstantsTests(unittest.TestCase):
    """The registered rule constants, controls and notes."""

    def test_the_three_registered_cases_are_the_d09_identities(self):
        cases = _p67().PHASE67_CASES
        self.assertEqual(
            {role: (case["orbit_key"], case["seed"]) for role, case in cases.items()},
            CASES,
        )

    def test_the_control_arms_are_the_registered_controls(self):
        p67 = _p67()
        self.assertEqual(p67.phase67_control_arm("exp02", "d2"), "d12")
        self.assertEqual(p67.phase67_control_arm("exp02", "d12"), "d12")
        self.assertEqual(p67.phase67_control_arm("exp03", "lr1e-5"), "lr1e-4")
        self.assertEqual(p67.phase67_control_arm("exp04", "locked-f1"), "locked-raw")
        self.assertEqual(p67.phase67_control_arm("exp04", "locked-f12"), "locked-raw")
        self.assertEqual(p67.phase67_control_arm("exp04", "exp01-f1"), "exp01-raw")
        self.assertEqual(p67.phase67_control_arm("exp04", "exp01-f12"), "exp01-raw")
        self.assertEqual(p67.phase67_control_arm("exp05", "lap1"), "lap10")
        self.assertEqual(p67.phase67_control_arm("exp05", "lap5"), "lap10")
        for experiment, arm in (("exp99", "d2"), ("exp02", "nope"), ("exp04", "mid"),
                                ("exp05", "lap3")):
            with self.subTest(experiment=experiment, arm=arm):
                with self.assertRaises(ValueError):
                    p67.phase67_control_arm(experiment, arm)

    def test_the_rule_numbers_and_labels_are_the_registered_ones(self):
        p67 = _p67()
        rule = p67.PHASE67_IMPROVEMENT_RULE
        self.assertEqual(rule["threshold"], 0.05)
        self.assertIn("strictly_greater", rule["comparison"])
        effect = p67.PHASE67_EFFECT_RULE
        self.assertEqual(effect["threshold"], 0.20)
        self.assertIn("greater_or_equal", effect["comparison"])
        self.assertEqual(
            p67.CONFIRMATION_LABELS,
            ("confirmed-improvement", "confirmed-worsening", "ambiguous",
             "unsettled", "inconclusive-mechanical"),
        )
        self.assertIn("GAP-59-08", p67.GAP_59_08_NOTE)
        self.assertIn("no causal claim", p67.SIMILARITY_NOTE)


class ImprovementTests(unittest.TestCase):
    """The final-quarter improvement rule at its exact boundary."""

    def test_exact_five_percent_is_settled_and_the_next_instant_is_not(self):
        check = _p67().phase67_improvement_check
        settled = check(_checkpoints(20.0, 19.0))
        self.assertIs(settled["settled"], True)
        self.assertEqual(settled["improvement"], 0.05)
        unsettled = check(_checkpoints(20.0, math.nextafter(19.0, -math.inf)))
        self.assertIs(unsettled["settled"], False)
        self.assertGreater(unsettled["improvement"], 0.05)
        self.assertIs(check(_checkpoints(20.0, 10.0))["settled"], False)

    def test_a_smaller_improvement_and_a_worsening_are_settled(self):
        check = _p67().phase67_improvement_check
        self.assertIs(check(_checkpoints(20.0, math.nextafter(19.0, math.inf)))["settled"], True)
        self.assertIs(check(_checkpoints(2.0, 4.0))["settled"], True)

    def test_a_zero_reference_is_settled_either_way(self):
        check = _p67().phase67_improvement_check
        zero_final = check(_checkpoints(0.0, 0.0))
        self.assertIs(zero_final["settled"], True)
        self.assertIsNone(zero_final["improvement"])
        positive_final = check(_checkpoints(0.0, 0.5))
        self.assertIs(positive_final["settled"], True)
        self.assertIsNone(positive_final["improvement"])

    def test_malformed_checkpoints_refuse(self):
        check = _p67().phase67_improvement_check
        for bad in (
            [],
            _checkpoints(2.0, 1.0)[:2],
            _checkpoints(2.0, 1.0) + [{"step": 101, "score": {"E": 0.5}}],
            [{"step": 75, "score": {"E": -1.0}},
             {"step": 75, "score": {"E": 1.0}}, {"step": 100, "score": {"E": 0.5}}],
            _checkpoints(float("nan"), 0.5),
            _checkpoints(2.0, float("inf")),
            [
                {"step": 75, "score": {"E": True}},
                {"step": 75, "score": {"E": 1.0}},
                {"step": 100, "score": {"E": 0.5}},
            ],
            [
                {"step": 100, "score": {"E": 1.0}},
                {"step": 75, "score": {"E": 1.0}},
                {"step": 50, "score": {"E": 0.5}},
            ],
            "not-a-list",
        ):
            with self.subTest(bad=bad):
                with self.assertRaises(ValueError):
                    check(bad)


class ContrastTests(unittest.TestCase):
    """The matched contrast rule: direction, effect, tiers, confirmation."""

    def _contrast(self, readings, experiment="exp02", arm="d2"):
        return _p67().phase67_contrast(experiment, arm, readings)

    def test_an_exact_twenty_percent_effect_confirms_improvement(self):
        result = self._contrast(_three_cases(4.0, 5.0))
        self.assertEqual(result["confirmation"], "confirmed-improvement")
        self.assertEqual(result["control"], "d12")
        for case in result["cases"].values():
            self.assertEqual(case["direction"], "improvement")
            self.assertEqual(case["relative_E_effect"], 0.2)
            self.assertTrue(case["percentage_applicable"])
            self.assertEqual(case["tier_direction"], "unchanged")
            self.assertIs(case["qualifies_effect"], True)

    def test_the_instant_below_twenty_percent_without_a_tier_change_is_ambiguous(self):
        result = self._contrast(
            _three_cases(math.nextafter(4.0, math.inf), 5.0)
        )
        self.assertEqual(result["confirmation"], "ambiguous")
        for case in result["cases"].values():
            self.assertLess(case["relative_E_effect"], 0.2)
            self.assertIs(case["qualifies_effect"], False)

    def test_a_matching_tier_change_qualifies_a_small_effect(self):
        result = self._contrast(_three_cases(0.9, 1.0, arm_tier=1))
        self.assertEqual(result["confirmation"], "confirmed-improvement")
        for case in result["cases"].values():
            self.assertEqual(case["tier_direction"], "improved")
            self.assertIs(case["qualifies_effect"], True)
        worsening = self._contrast(_three_cases(1.0, 0.9, arm_tier=0, control_tier=1))
        self.assertEqual(worsening["confirmation"], "confirmed-worsening")
        for case in worsening["cases"].values():
            self.assertEqual(case["direction"], "worsening")
            self.assertEqual(case["tier_direction"], "worsened")

    def test_a_twenty_percent_effect_qualifies_even_against_an_opposing_tier(self):
        # The registered rule is an OR: a nonzero E direction qualifies
        # through a matching tier change OR a twenty-percent effect, so an
        # opposing tier change cannot veto the effect side of the rule.
        result = self._contrast(_three_cases(4.0, 5.0, arm_tier=0, control_tier=1))
        self.assertEqual(result["confirmation"], "confirmed-improvement")
        for case in result["cases"].values():
            self.assertEqual(case["tier_direction"], "worsened")
            self.assertIs(case["qualifies_effect"], True)

    def test_ties_small_effects_and_opposed_directions_are_ambiguous(self):
        tie = self._contrast(_three_cases(5.0, 5.0))
        self.assertEqual(tie["confirmation"], "ambiguous")
        self.assertEqual(tie["cases"]["main"]["direction"], "tie")
        opposed = _three_cases(4.0, 5.0)
        opposed["repeat-system"]["arm"] = _reading(
            e=6.0, arm="d2", orbit_key="hierarchical/gold/851", seed=42
        )
        result = self._contrast(opposed)
        self.assertEqual(result["confirmation"], "ambiguous")
        self.assertEqual(result["cases"]["main"]["direction"], "improvement")
        self.assertEqual(result["cases"]["repeat-system"]["direction"], "worsening")

    def test_one_unsettled_endpoint_blocks_confirmation(self):
        unsettled = self._contrast(
            _three_cases(4.0, 5.0, unsettled=True)
        )
        self.assertEqual(unsettled["confirmation"], "unsettled")
        control_only = _three_cases(4.0, 5.0)
        for role in control_only:
            control_only[role]["control"]["unsettled"] = True
        self.assertEqual(
            self._contrast(control_only)["confirmation"], "unsettled"
        )

    def test_one_problematic_endpoint_is_inconclusive_mechanical(self):
        with_problems = self._contrast(
            _three_cases(4.0, 5.0, problems=["the record is torn"])
        )
        self.assertEqual(with_problems["confirmation"], "inconclusive-mechanical")
        with_setting = _three_cases(4.0, 5.0)
        with_setting["main"]["arm"]["setting_problems"] = ["wrong row"]
        self.assertEqual(
            self._contrast(with_setting)["confirmation"], "inconclusive-mechanical"
        )

    def test_a_zero_control_e_retains_direction_without_dividing_by_zero(self):
        zero_control = self._contrast(
            _three_cases(0.5, 0.0, arm_tier=0, control_tier=1)
        )
        self.assertEqual(zero_control["confirmation"], "confirmed-worsening")
        case = zero_control["cases"]["main"]
        self.assertEqual(case["direction"], "worsening")
        self.assertIsNone(case["relative_E_effect"])
        self.assertFalse(case["percentage_applicable"])
        self.assertEqual(case["tier_direction"], "worsened")
        # Without a matching tier change the zero-control effect cannot
        # qualify: no percentage exists to carry it.
        flat = self._contrast(_three_cases(0.5, 0.0))
        self.assertEqual(flat["confirmation"], "ambiguous")

    def test_the_observed_fit_and_similarity_stay_descriptive(self):
        result = self._contrast(_three_cases(4.0, 5.0))
        for case in result["cases"].values():
            self.assertEqual(case["observed_fit"]["arm"]["E"], 4.0)
            self.assertEqual(case["observed_fit"]["control"]["E"], 5.0)
            self.assertEqual(case["observed_fit"]["control"]["tier"], 0)
        self.assertEqual(
            set(result["descriptive"]),
            {"adjacent_time_similarity", "note", "gap_59_08", "loss"},
        )
        self.assertIn("GAP-59-08", result["descriptive"]["gap_59_08"])
        self.assertIn("no causal claim", result["descriptive"]["note"])
        self.assertEqual(result["descriptive"]["loss"], "context only")
        self.assertIn(
            "input",
            result["descriptive"]["adjacent_time_similarity"]["main"]["arm"][0][
                "layers"
            ][0]["name"],
        )

    def test_missing_repeats_wrong_controls_and_mismatched_identities_refuse(self):
        p67 = _p67()
        complete = _three_cases(4.0, 5.0)
        missing = {k: v for k, v in complete.items() if k != "repeat-seed"}
        with self.assertRaises(ValueError):
            self._contrast(missing)
        extra = {**complete, "repeat-none": complete["main"]}
        with self.assertRaises(ValueError):
            self._contrast(extra)
        wrong_control = _three_cases(4.0, 5.0, control="d8")
        with self.assertRaises(ValueError):
            self._contrast(wrong_control)
        wrong_exp04_control = {
            role: {
                "arm": _reading(e=4.0, arm="exp01-f1", orbit_key=orbit, seed=seed),
                "control": _reading(e=5.0, arm="locked-raw", orbit_key=orbit, seed=seed),
            }
            for role, (orbit, seed) in CASES.items()
        }
        with self.assertRaises(ValueError):
            self._contrast(wrong_exp04_control, experiment="exp04", arm="exp01-f1")
        wrong_arm = _three_cases(4.0, 5.0)
        wrong_arm["main"]["arm"]["identity"]["arm"] = "d4"
        with self.assertRaises(ValueError):
            self._contrast(wrong_arm)
        wrong_orbit = _three_cases(4.0, 5.0)
        wrong_orbit["repeat-system"]["arm"]["identity"]["orbit_key"] = (
            "hierarchical/gold/1632"
        )
        with self.assertRaises(ValueError):
            self._contrast(wrong_orbit)
        wrong_seed = _three_cases(4.0, 5.0)
        wrong_seed["repeat-seed"]["control"]["identity"]["seed"] = 42
        with self.assertRaises(ValueError):
            self._contrast(wrong_seed)
        wrong_experiment = _three_cases(4.0, 5.0)
        wrong_experiment["main"]["arm"]["identity"]["experiment"] = "exp03"
        with self.assertRaises(ValueError):
            self._contrast(wrong_experiment)

    def test_duplicate_run_identities_and_malformed_values_refuse(self):
        p67 = _p67()
        duplicate = _three_cases(4.0, 5.0)
        duplicate["repeat-seed"]["arm"] = dict(duplicate["main"]["arm"])
        with self.assertRaises(ValueError):
            self._contrast(duplicate)
        for field, value in (
            ("E", "4.0"), ("E", True), ("E", -1.0), ("E", float("nan")),
            ("tier", True), ("tier", "0"), ("tier", 9),
        ):
            with self.subTest(field=field, value=value):
                readings = _three_cases(4.0, 5.0)
                readings["main"]["arm"]["scores"]["network"][field] = value
                with self.assertRaises(ValueError):
                    self._contrast(readings)
        readings = _three_cases(4.0, 5.0)
        readings["main"]["arm"]["unsettled"] = "no"
        with self.assertRaises(ValueError):
            self._contrast(readings)
        for experiment, arm in (("exp99", "d2"), ("exp02", "d12")):
            with self.subTest(experiment=experiment, arm=arm):
                with self.assertRaises(ValueError):
                    p67.phase67_contrast(
                        experiment, arm, _three_cases(4.0, 5.0)
                    )


class ConfirmationTests(unittest.TestCase):
    """The experiment-level confirmation over every declared contrast."""

    @staticmethod
    def _contrast(experiment, arm, confirmation="ambiguous"):
        return {
            "experiment": experiment,
            "arm": arm,
            "confirmation": confirmation,
            "reasons": ["a reason"] if confirmation != "confirmed-improvement" else [],
        }

    def test_every_declared_noncontrol_contrast_is_persisted(self):
        p67 = _p67()
        contrasts = [
            self._contrast("exp02", "d2", "confirmed-improvement"),
            self._contrast("exp02", "d4"),
            self._contrast("exp02", "d6", "unsettled"),
            self._contrast("exp02", "d8", "inconclusive-mechanical"),
        ]
        result = p67.phase67_confirmation(
            "exp02", contrasts,
            declared_arms=["d2", "d4", "d6", "d8", "d12"],
        )
        self.assertEqual(
            result["confirmed"],
            [{"arm": "d2", "confirmation": "confirmed-improvement"}],
        )
        self.assertEqual(
            {row["arm"] for row in result["unconfirmed"]}, {"d4", "d6", "d8"}
        )
        self.assertEqual(len(result["contrasts"]), 4)
        self.assertIn("GAP-59-08", result["descriptive"]["gap_59_08"])
        self.assertIn("no causal claim", result["descriptive"]["note"])

    def test_the_exp04_and_exp05_control_arms_are_not_contrasted(self):
        p67 = _p67()
        result = p67.phase67_confirmation(
            "exp04",
            [self._contrast("exp04", arm) for arm in
             ("locked-f1", "locked-f12", "exp01-f1", "exp01-f12")],
            declared_arms=["locked-raw", "locked-f1", "locked-f12",
                           "exp01-raw", "exp01-f1", "exp01-f12"],
        )
        self.assertEqual(len(result["contrasts"]), 4)
        result = p67.phase67_confirmation(
            "exp05",
            [self._contrast("exp05", arm) for arm in ("lap1", "lap2", "lap5")],
            declared_arms=["lap1", "lap2", "lap5", "lap10"],
        )
        self.assertEqual(len(result["contrasts"]), 3)

    def test_missing_duplicate_undeclared_and_control_contrasts_refuse(self):
        p67 = _p67()
        declared = ["d2", "d4", "d6", "d8", "d12"]
        with self.assertRaises(ValueError):
            p67.phase67_confirmation(
                "exp02", [self._contrast("exp02", "d2")], declared_arms=declared
            )
        with self.assertRaises(ValueError):
            p67.phase67_confirmation(
                "exp02",
                [self._contrast("exp02", "d2"), self._contrast("exp02", "d2"),
                 self._contrast("exp02", "d4"), self._contrast("exp02", "d6"),
                 self._contrast("exp02", "d8")],
                declared_arms=declared,
            )
        with self.assertRaises(ValueError):
            p67.phase67_confirmation(
                "exp02",
                [self._contrast("exp02", "d2"), self._contrast("exp02", "d4"),
                 self._contrast("exp02", "d6"), self._contrast("exp02", "d8"),
                 self._contrast("exp02", "lr1e-3")],
                declared_arms=declared,
            )
        with self.assertRaises(ValueError):
            p67.phase67_confirmation(
                "exp02",
                [self._contrast("exp02", "d2"), self._contrast("exp02", "d4"),
                 self._contrast("exp02", "d6"), self._contrast("exp02", "d8"),
                 self._contrast("exp02", "d12")],
                declared_arms=declared,
            )
        with self.assertRaises(ValueError):
            p67.phase67_confirmation(
                "exp02",
                [self._contrast("exp03", "d2"), self._contrast("exp03", "d4"),
                 self._contrast("exp03", "d6"), self._contrast("exp03", "d8")],
                declared_arms=declared,
            )
        for bad in ((), "exp02", None):
            with self.subTest(bad=bad):
                with self.assertRaises(ValueError):
                    p67.phase67_confirmation("exp02", bad, declared_arms=declared)


if __name__ == "__main__":
    unittest.main()
