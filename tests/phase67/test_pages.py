"""Plan 67-06 task 67-06-01: the design, page and matrix contracts (pure).

The Phase 67 execution adapter freezes one scientific design per experiment
before any real operation: every declared arm and case, the prospective
hypothesis prediction with the flat, opposite, unsettled and mechanical
alternatives recorded equally, the registered schedule numbers, the scope
branch table, and the exact case-major Cartesian matrices with their orbit
aware variant names. These tests drive the pure builders directly — no
fixture repo, no corpus, no launch — so a broken contract fails as an
assertion on the planned behavior, never as a harness side effect.
"""

from __future__ import annotations

import copy
import importlib
import json
import tempfile
import unittest
from pathlib import Path

MODULE_NAME = "diagnostic_phase67_execution"


def _module(case):
    try:
        return importlib.import_module(f"pinn.verification.{MODULE_NAME}")
    except ImportError as exc:
        case.fail(f"pinn.verification.{MODULE_NAME} is missing: {exc}")


def _refusal(case):
    return _module(case).Phase67CommandRefused


def _symbol(case, module, name):
    value = getattr(module, name, None)
    case.assertIsNotNone(value, f"{module.__name__}.{name} is missing")
    return value


#: The exact per-experiment products (the plan's declared arm orders).
EXPECTED_ROWS = {"exp02": 15, "exp03": 15, "exp04": 18, "exp05": 12}
EXPECTED_ARMS = {
    "exp02": ("d2", "d4", "d6", "d8", "d12"),
    "exp03": ("lr1e-3", "lr3e-4", "lr1e-4", "lr3e-5", "lr1e-5"),
    "exp04": (
        "locked-raw", "locked-f1", "locked-f12",
        "exp01-raw", "exp01-f1", "exp01-f12",
    ),
    "exp05": ("lap1", "lap2", "lap5", "lap10"),
}
EXPECTED_CASES = (
    ("main-1632-s42", "hierarchical/gold/1632", 42),
    ("repeat-851-s42", "hierarchical/gold/851", 42),
    ("repeat-1632-s41", "hierarchical/gold/1632", 41),
)

#: The synthetic grid evidence the matrix builder consumes: two orbits, a
#: full [0, 10] window and (for exp05) exact first-crossing lap endpoints.
_TIMES = [round(index * 10.0 / 41, 12) for index in range(42)]
_GRID_SHA = "a" * 64


def _window(endpoint, laps=None):
    window = {
        "t_end": float(endpoint),
        "first_time": _TIMES[0],
        "last_time": _TIMES[-1],
        "sample_count": len(_TIMES),
        "physical_times_sha256": _GRID_SHA,
        "normalized_tau_sha256": _GRID_SHA,
        "baselines": {
            "window_mean_constant": {"E": 1.25},
            "two_kepler": {"applicable": False, "failure": "not_applicable",
                           "reason": "synthetic"},
        },
    }
    if laps is not None:
        window["requested_laps"] = laps
    return window


def _metadata_record(experiment, *, digest="b" * 64):
    orbits = {}
    for orbit in ("hierarchical/gold/1632", "hierarchical/gold/851"):
        windows = {"full": _window(10.0)}
        if experiment == "exp05":
            for arm, laps in (("lap1", 1), ("lap2", 2), ("lap5", 5), ("lap10", 10)):
                windows[arm] = _window(2.5 + 0.1 * laps, laps=laps)
        orbits[orbit] = {
            "census": {"N_in": 10.471994061054543 if orbit.endswith("1632") else 18.612048388702},
            "max_adjacent_phase_increment_rad": {"harmonic_1": 0.4, "harmonic_2": 0.8},
            "windows": windows,
        }
    return {"schema": "phase67-metadata/v1", "experiment": experiment,
            "orbits": orbits, "sha256": digest}


class ModuleContractTests(unittest.TestCase):
    """The plan's declared helper symbols exist on the execution adapter."""

    def test_the_execution_adapter_exposes_the_declared_helpers(self):
        execution = _module(self)
        for name in (
            "phase67_design", "phase67_run_matrix",
            "admit_phase67_metadata_registration", "capture_phase67_metadata",
            "launch_phase67_row", "audit_phase67",
        ):
            _symbol(self, execution, name)

    def test_the_cli_entry_point_exists_on_the_pure_module(self):
        phase67 = importlib.import_module("pinn.verification.diagnostic_phase67")
        self.assertTrue(callable(getattr(phase67, "main", None)),
                        "diagnostic_phase67.main is missing")

    def test_the_registered_case_bindings_match_the_d09_roles(self):
        execution = _module(self)
        from pinn.verification.diagnostic_phase67 import PHASE67_CASES

        cases = _symbol(self, execution, "CASES")
        self.assertEqual(tuple(tuple(row) for row in cases), EXPECTED_CASES)
        by_role = {
            "main": {"orbit_key": "hierarchical/gold/1632", "seed": 42},
            "repeat-system": {"orbit_key": "hierarchical/gold/851", "seed": 42},
            "repeat-seed": {"orbit_key": "hierarchical/gold/1632", "seed": 41},
        }
        self.assertEqual(dict(PHASE67_CASES), by_role)


class DesignTests(unittest.TestCase):
    """One frozen design per experiment: arms, cases, predictions, scope."""

    @classmethod
    def setUpClass(cls):
        cls.execution = _module(cls)

    def _design(self, experiment):
        return self.execution.phase67_design(experiment)

    def test_the_design_freezes_every_arm_case_and_branch_equally(self):
        from pinn.verification.diagnostic_phase67 import (
            CONFIRMATION_LABELS,
            PHASE67_BUDGET_RULE,
        )

        for experiment in EXPECTED_ARMS:
            with self.subTest(experiment=experiment):
                design = self._design(experiment)
                self.assertEqual(design["schema"], "phase67-design/v1")
                self.assertEqual(design["experiment"], experiment)
                self.assertEqual(
                    [entry["arm"] for entry in design["variants"]],
                    list(EXPECTED_ARMS[experiment]),
                )
                self.assertEqual(
                    tuple((row["case"], row["orbit_key"], row["seed"])
                          for row in design["cases"]),
                    EXPECTED_CASES,
                )
                table = design["prediction_table"]
                self.assertEqual(tuple(table), EXPECTED_ARMS[experiment])
                for arm, branches in table.items():
                    for branch in ("hypothesis", "flat", "opposite", "unsettled",
                                   "mechanical"):
                        self.assertIsInstance(branches[branch], str)
                        self.assertTrue(
                            branches[branch].strip(),
                            f"{experiment}/{arm} names no {branch} branch text",
                        )
                scope = design["scope_branches"]
                self.assertEqual(tuple(sorted(scope)), tuple(sorted(CONFIRMATION_LABELS)))
                timing = design["schedule"]["timing"]
                self.assertEqual(timing["optimizer_steps"],
                                 PHASE67_BUDGET_RULE["timing_steps"])
                self.assertEqual(timing["warmup_steps"],
                                 PHASE67_BUDGET_RULE["timing_warmup"])
                self.assertEqual(timing["similarity_cadence"], [0, 300, 600, 900, 1200])
                self.assertEqual(timing["score_cadence"], [600, 900, 1200])
                self.assertEqual(timing["cap_seconds"], 900.0)
                self.assertEqual(design["schedule"]["science"]["cap_seconds"], 3540.0)
                self.assertTrue(design["no_continuation"].strip())
                self.assertIn("multi-setting positive control",
                              design["positive_control_note"])

    def test_every_hypothesis_prediction_matches_the_plan_direction(self):
        directions = {
            "exp02": "shallower depth",
            "exp03": "learning-rate sensitivity",
            "exp04": "encoded harmonic",
            "exp05": "shorter window",
        }
        for experiment, phrase in directions.items():
            with self.subTest(experiment=experiment):
                design = self._design(experiment)
                self.assertIn(phrase, design["hypothesis"]["prediction"])
                for arm in EXPECTED_ARMS[experiment]:
                    if arm == design["control_arm"]:
                        continue
                    self.assertIn(
                        phrase,
                        design["prediction_table"][arm]["hypothesis"],
                        f"{arm} hypothesis branch does not name the direction",
                    )

    def test_the_registered_control_of_every_arm_is_the_declared_one(self):
        from pinn.verification.diagnostic_phase67 import phase67_control_arm

        for experiment, arms in EXPECTED_ARMS.items():
            design = self._design(experiment)
            for arm in arms:
                self.assertEqual(
                    design["controls"][arm], phase67_control_arm(experiment, arm)
                )
            self.assertEqual(design["control_arm"], arms[-1])

    def test_the_design_records_depth_sizes_and_encoded_confounds(self):
        exp02 = self._design("exp02")
        self.assertEqual(
            exp02["confounds"]["depth_parameter_counts"],
            {"d2": 137737, "d4": 269321, "d6": 400905, "d8": 532489, "d12": 795657},
        )
        exp04 = self._design("exp04")
        self.assertIn("fan_in", exp04["confounds"]["encoded"])
        self.assertIn("frequency", exp04["confounds"]["encoded"])

    def test_exp04_variants_are_orbit_aware_and_exp05_names_the_algorithm(self):
        from pinn.verification.diagnostic_phase67_catalog import (
            FEATURE_FREQUENCY_851,
        )

        exp04 = self._design("exp04")
        variants = {
            entry["arm"]: entry["declarations"] for entry in exp04["variants"]
        }
        locked_f1 = variants["locked-f1"]
        self.assertEqual(
            set(locked_f1),
            {"hierarchical/gold/1632", "hierarchical/gold/851"},
        )
        self.assertEqual(
            locked_f1["hierarchical/gold/851"]["feature_frequency"],
            FEATURE_FREQUENCY_851,
        )
        raw = variants["exp01-raw"]
        self.assertEqual(raw["hierarchical/gold/1632"], raw["hierarchical/gold/851"])
        exp05 = self._design("exp05")
        self.assertEqual(exp05["window_selection"]["algorithm"], "first_lap_prefixes")
        self.assertEqual(exp05["window_selection"]["lap_counts"], [1, 2, 5, 10])


class MatrixTests(unittest.TestCase):
    """The exact case-major Cartesian products with orbit-aware variants."""

    @classmethod
    def setUpClass(cls):
        cls.execution = _module(cls)

    def _matrix(self, experiment, kind="timing"):
        return self.execution.phase67_run_matrix(
            experiment, kind, metadata=_metadata_record(experiment)
        )

    def test_each_matrix_is_the_exact_case_major_cartesian_product(self):
        for experiment, count in EXPECTED_ROWS.items():
            for kind in ("timing", "science"):
                with self.subTest(experiment=experiment, kind=kind):
                    rows = self._matrix(experiment, kind)
                    self.assertEqual(len(rows), count)
                    expected_order = [
                        (case, arm)
                        for case, _orbit, _seed in EXPECTED_CASES
                        for arm in EXPECTED_ARMS[experiment]
                    ]
                    self.assertEqual(
                        [(row["case"], row["arm"]) for row in rows], expected_order
                    )
                    for row in rows:
                        self.assertEqual(row["experiment"], experiment)
                        self.assertEqual(row["kind"], kind)
                        orbit = next(
                            orbit for case, orbit, _seed in EXPECTED_CASES
                            if case == row["case"]
                        )
                        self.assertEqual(row["orbit_key"], orbit)
                        self.assertEqual(
                            row["seed"],
                            next(seed for case, _o, seed in EXPECTED_CASES
                                 if case == row["case"]),
                        )
                        self.assertIsInstance(row["variant_name"], str)
                        self.assertTrue(row["variant_name"])
                        self.assertEqual(row["metadata_sha256"], "b" * 64)
                        self.assertEqual(row["physical_window"], {"t_start": 0.0,
                                                                  "t_end": row["t_end"]})
                        self.assertEqual(
                            row["registration_path"],
                            f"evidence/{experiment}/{kind}/{row['case']}/"
                            f"{row['arm']}/registration.json",
                        )
                        self.assertEqual(
                            row["output_path"],
                            f"evidence/{experiment}/{kind}/{row['case']}/"
                            f"{row['arm']}/record.json",
                        )

    def test_the_variant_names_are_orbit_aware_for_exp04_and_per_window_for_exp05(self):
        exp04 = self._matrix("exp04")
        by_case = {row["case"]: row for row in exp04 if row["arm"] == "locked-f1"}
        self.assertEqual(by_case["main-1632-s42"]["variant_name"],
                         "exp04-locked-f1")
        self.assertEqual(by_case["main-1632-s42"]["t_end"], 10.0)
        self.assertEqual(by_case["repeat-851-s42"]["variant_name"],
                         "exp04-locked-f1-851")
        exp05 = self._matrix("exp05")
        ends = {row["arm"]: row["t_end"] for row in exp05
                if row["case"] == "main-1632-s42"}
        self.assertEqual(set(ends), {"lap1", "lap2", "lap5", "lap10"})
        self.assertTrue(all(0.0 < end < 10.0 for end in ends.values()))

    def test_the_declared_window_is_the_variant_length_not_the_grid_endpoint(self):
        # The real gold grid ends at 9.999999999999831 (the committed capture
        # attests it), while every full-window variant declares the locked
        # 10.0 window; the rows declare the variant's window length (Phase
        # 66's committed real registrations declare 10.0), never the
        # observed float64 grid endpoint.
        metadata = _metadata_record("exp02")
        for orbit in metadata["orbits"].values():
            orbit["windows"]["full"] = _window(9.999999999999831)
        rows = self.execution.phase67_run_matrix(
            "exp02", "timing", metadata=metadata
        )
        self.assertTrue(rows)
        for row in rows:
            self.assertEqual(row["t_end"], 10.0)
            self.assertEqual(
                row["physical_window"], {"t_start": 0.0, "t_end": 10.0}
            )

    def test_the_timing_and_science_schedules_come_from_the_registered_rule(self):
        from pinn.verification.diagnostic_phase67 import (
            PHASE67_BUDGET_RULE,
            phase67_cadence,
            phase67_score_cadence,
        )

        rows = self._matrix("exp02")
        timing_steps = int(PHASE67_BUDGET_RULE["timing_steps"])
        for row in rows:
            self.assertEqual(row["schedule"]["optimizer_steps"], timing_steps)
            self.assertEqual(row["schedule"]["similarity_cadence"],
                             phase67_cadence(timing_steps))
            self.assertEqual(row["schedule"]["score_cadence"],
                             phase67_score_cadence(timing_steps))
            self.assertEqual(row["schedule"]["cap_seconds"], 900.0)

    def test_an_incomplete_or_foreign_metadata_record_refuses(self):
        for bad_name, mutate in (
            ("missing orbit", lambda doc: doc["orbits"].pop("hierarchical/gold/851")),
            ("missing window", lambda doc: doc["orbits"][
                "hierarchical/gold/1632"]["windows"].pop("full")),
            ("wrong experiment", lambda doc: doc.update(experiment="exp99")),
        ):
            with self.subTest(bad=bad_name):
                doc = _metadata_record("exp02")
                mutate(doc)
                with self.assertRaises(_refusal(self)):
                    self.execution.phase67_run_matrix(
                        "exp02", "timing", metadata=doc
                    )
        with self.assertRaises(_refusal(self)):
            self.execution.phase67_run_matrix("exp99", "timing",
                                              metadata=_metadata_record("exp02"))
        with self.assertRaises(_refusal(self)):
            self.execution.phase67_run_matrix("exp02", "other",
                                              metadata=_metadata_record("exp02"))
        # A non-mapping metadata record refuses too.
        with self.assertRaises(_refusal(self)):
            self.execution.phase67_run_matrix("exp02", "timing", metadata=[])


class CostRowTests(unittest.TestCase):
    """The budget consumes only cost fields: scores change nothing."""

    TIMING_RECORD = {
        "status": "complete",
        "steps": {"requested": 1200, "warmup": 200, "measured": 1000,
                  "completed": 1200},
        "timing": {
            "seconds_per_step": 0.01,
            "warmup_seconds": 2.0,
            "measured_seconds": 10.0,
            "events": {
                "logging": [{"step": 0, "seconds": 0.4}] * 5,
                "scoring": [{"step": 600, "seconds": 0.6}] * 3,
                "publication_io": [{"phase": "publish", "seconds": 0.2}],
            },
        },
        "scores": {"network": {"E": 1.5, "tier": 0}},
        "similarity": {"entries": [{"step": 0}] * 5},
    }

    def test_cost_rows_ignore_every_scientific_value(self):
        execution = _module(self)
        extractor = _symbol(self, execution, "phase67_cost_rows")
        identity = {"experiment": "exp02", "arm": "d2",
                    "orbit_key": "hierarchical/gold/1632", "seed": 42,
                    "window": 10.0}
        raw = json.dumps(self.TIMING_RECORD, indent=2).encode("utf-8")
        record = dict(self.TIMING_RECORD)
        receipt = {"checked_utc": "2026-11-07T18:00:00+00:00"}
        attempt = {"ended_utc": "2026-11-07T18:00:20+00:00",
                   "completed_steps": 1200}
        first = extractor([(identity, record, receipt, attempt, len(raw))])
        tampered = copy.deepcopy(record)
        tampered["scores"]["network"] = {"E": 0.011, "tier": 1}
        tampered["similarity"]["entries"] = [
            {"step": 0, "adjacent_cosine_mean": 0.13}] * 5
        second = extractor([(identity, tampered, receipt, attempt, len(raw))])
        self.assertEqual(first, second)
        self.assertNotIn("scores", json.dumps(first))

    def test_an_incomplete_or_mismatched_timing_record_refuses(self):
        execution = _module(self)
        extractor = _symbol(self, execution, "phase67_cost_rows")
        identity = {"experiment": "exp02", "arm": "d2",
                    "orbit_key": "hierarchical/gold/1632", "seed": 42,
                    "window": 10.0}
        record = dict(self.TIMING_RECORD)
        receipt = {"checked_utc": "2026-11-07T18:00:00+00:00"}
        attempt = {"ended_utc": "2026-11-07T18:00:20+00:00"}
        incomplete = dict(record, status="incomplete")
        with self.assertRaises(_refusal(self)):
            extractor([(identity, incomplete, receipt, attempt, 10)])
        wrong_steps = dict(record)
        wrong_steps["steps"] = {"completed": 100}
        with self.assertRaises(_refusal(self)):
            extractor([(identity, wrong_steps, receipt, attempt, 10)])


class ScopeGateTests(unittest.TestCase):
    """Pending owner proposals block only the dependent experiment."""

    def _scope(self, confirmation):
        execution = _module(self)
        return _symbol(self, execution, "phase67_scope_disposition")(confirmation)

    def test_every_confirmation_label_maps_to_a_registered_disposition(self):
        within = ("confirmed-improvement", "ambiguous", "unsettled")
        blocking = ("confirmed-worsening", "inconclusive-mechanical")
        for label in within:
            disposition = self._scope(label)
            self.assertEqual(disposition["scope49_disposition"], "none", label)
            self.assertIs(disposition["dependent_launch_allowed"], True, label)
        for label in blocking:
            disposition = self._scope(label)
            self.assertEqual(
                disposition["scope49_disposition"], "proposal-pending", label
            )
            self.assertIs(disposition["dependent_launch_allowed"], False, label)
        with self.assertRaises(_refusal(self)):
            self._scope("confirmed-maybe")

    def test_a_pending_proposal_blocks_only_later_experiments(self):
        execution = _module(self)
        gate = _symbol(self, execution, "phase67_prior_experiment_allowed")
        with tempfile.TemporaryDirectory(prefix="phase67-scope-") as raw:
            root = Path(raw)
            evidence = root / "evidence"
            evidence.mkdir(parents=True)
            # No prior review at all: the first experiment owes nothing.
            self.assertTrue(gate("exp02", phase_dir=root, repo_root=root))
            # A pending proposal in exp02 blocks exp03..05 but not exp02.
            for experiment, allowed in (
                ("exp02", True), ("exp03", False), ("exp04", False), ("exp05", False),
            ):
                review = {
                    "schema": "phase67-review/v1", "experiment": "exp02",
                    "scope49_disposition": "proposal-pending",
                    "dependent_launch_allowed": False,
                }
                directory = evidence / "exp02"
                directory.mkdir(parents=True, exist_ok=True)
                (directory / "review.json").write_text(json.dumps(review))
                self.assertIs(
                    gate(experiment, phase_dir=root, repo_root=root),
                    allowed, experiment,
                )


class PageBuilderTests(unittest.TestCase):
    """The page text builders embed the design and never a score."""

    def test_the_timing_prediction_page_carries_the_design_and_predictions(self):
        execution = _module(self)
        builder = _symbol(self, execution, "timing_prediction_page")
        design = execution.phase67_design("exp02")
        page = builder(design)
        self.assertIn("```json phase67-design", page)
        embedded = page.split("```json phase67-design\n", 1)[1].split("\n```", 1)[0]
        self.assertEqual(json.loads(embedded), design)
        for arm in EXPECTED_ARMS["exp02"]:
            self.assertIn(arm, page)
        for branch in ("flat", "opposite", "unsettled", "mechanical"):
            self.assertIn(branch, page)
        self.assertIn("No rule is re-set after a result is seen.", page)

    def test_the_budget_page_and_prediction_page_are_cost_only(self):
        execution = _module(self)
        budget = {
            "schema": "phase67-budget/v1",
            "whole_run_cap_seconds": 3540.0,
            "common_optimizer_steps": 300,
            "warmup_steps": 200,
            "loss_trace_stride": 1,
            "per_row_projection_seconds": {},
            "phase_cost_ledger": {"cap_seconds": 3540.0, "experiments": []},
        }
        budget_page = _symbol(self, execution, "budget_page")(
            execution.phase67_design("exp02"), budget
        )
        prediction_page = _symbol(self, execution, "prediction_page")(
            execution.phase67_design("exp02"), budget
        )
        for page in (budget_page, prediction_page):
            self.assertIn("300", page)
            self.assertNotIn('"E"', page)
            self.assertNotIn("scores", page)
        self.assertIn("frozen before science", prediction_page)


if __name__ == "__main__":
    unittest.main()
