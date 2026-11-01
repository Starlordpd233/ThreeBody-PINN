"""Plan 66-02 (EXP-01): the reading rule, improvement check and run readers.

One test per behavior bullet of task 66-02-02, on synthetic dicts and temporary
directories only (no Phase 66 evidence file exists yet, so none is read):
:class:`ReadingRuleTests` pins the reading rule at its edges (the frozen
scorecard's inclusive Tier-1 line, the constant-predictor band, the unsettled
label, the confirmation and routing tables), :class:`ImprovementTests` pins the
output-movement improvement check (the DIAG-09 signal, never the loss),
:class:`RecordReaderTests` pins the record and run-directory readers with every
mechanical and setting problem from the plan, and :class:`RunIdentityTests`
pins the (orbit_key, seed, registration_sha256) run identity and the
three-run review. The synthetic records copy the committed Phase 65 smoke
record's shape (scores.network, comparisons, similarity entries with input and
h1 rows, access, registration, variant) so the readers are exercised against
the real field paths.
"""

from __future__ import annotations

import contextlib
import hashlib
import io
import json
import math
import tempfile
import unittest
from datetime import datetime
from pathlib import Path

from pinn.verification import diagnostic_phase66 as p66
from pinn.verification.diagnostic_phase66 import classify_exp01, tier1_e_max
from pinn.verification.feasibility_scorecard import load_scorecard

#: The full EXP-01 similarity cadence for a 268,000-step run (task 66-02-03
#: pins the generator; here it is the synthetic record's fixed cadence).
CADENCE = [
    0, 100, 300, 1000, 3000, 10000, 30000, 100000,
    128000, 156000, 184000, 212000, 240000, 268000,
]

RECEIPT_SCHEMA = "phase66-power-gate/v1"


def _synthetic_record(
    *,
    orbit_key="hierarchical/gold/1632",
    seed=42,
    registration="a" * 64,
    run_id=None,
    e=None,
    e_const=None,
    movements=None,
    step0_frequency_max=22.7,
    tier=None,
    **overrides,
):
    """An EXP-01-shaped record dict built from the smoke record's shape.

    The default network E sits in the near band (about 1.02 times the orbit's
    own constant-predictor E) and the output movement is flat, so a clean
    record reads clean. ``movements`` replaces the per-cadence output-movement
    values (a shorter list drops the final-step entry); ``tier`` overrides the
    consistent default tier computed from E.
    """
    if e_const is None:
        e_const = p66.E_CONST_PREDICTED[orbit_key]
    if e is None:
        e = e_const * 1.02
    if tier is None:
        tier = 1 if e <= 0.1 else 0
    if movements is None:
        movements = [0.5] * len(CADENCE)
    if run_id is None:
        run_id = "exp01-d1-w384-o1000-1632"
    entries = [
        {
            "step": step,
            "layers": [
                {"name": "input", "order": 0, "adjacent_cosine_mean": 0.99},
                {"name": "h1", "order": 1, "adjacent_cosine_mean": 0.98},
            ],
            "first_layer_frequency": {
                "median": 12.0,
                "max": step0_frequency_max if step == 0 else 22.73,
            },
            "output_movement": {"value": value},
        }
        for step, value in zip(CADENCE, movements)
    ]
    record = {
        "status": "complete",
        "run_id": run_id,
        "variant": {
            **p66.EXP01_VARIANT.to_json_dict(),
            "registered": True,
            "registry": "phase66",
        },
        "seed": int(seed),
        "orbit": {
            "train": {"record_key": orbit_key, "split": "train", "n_within_window": 1001},
            "score": {"record_key": orbit_key, "split": "score"},
            "beside": {"record_key": orbit_key, "split": "beside"},
        },
        "steps": {
            "requested": 268000, "warmup": 200,
            "measured": 267800, "completed": 268000,
        },
        "similarity": {"cadence": list(CADENCE), "entries": entries},
        "loss": {"final": 0.001, "trace": [0.5, 0.05, 0.001]},
        "timing": {"seconds_per_step": 0.008, "warmup_seconds": 0.5},
        "scores": {"network": {"E": e, "tier": tier, "eps_h": 14.493981514909423}},
        "comparisons": [
            {
                "comparison": "window_mean_constant",
                "predictor": {"kind": "window_mean_constant"},
                "score": {"E": e_const},
            },
            {
                "comparison": "two_kepler",
                "applicable": True,
                "score": {"E": 0.9168487091299374},
            },
        ],
        "registration": {
            "path": "reg/smoke-registration.json",
            "sha256": registration,
        },
        "access": {
            "reads": {"train": 1, "validation": 0, "refusals": 0},
            "attestation": {
                "opened": {"train": 1, "validation": 0},
                "test_split_opened": 0,
                "refused_before_open": 0,
            },
            "stage0": {"actual_opens": 1, "refused_before_open": 0},
        },
    }
    record.update(overrides)
    return record


def _write_directory(path, record, *, receipt=None, attempt=None):
    """A synthetic run directory: record.json, attempt.json, power-gate.json."""
    path = Path(path)
    path.mkdir(parents=True)
    raw = json.dumps(record, indent=2, sort_keys=True).encode("utf-8") + b"\n"
    (path / "record.json").write_bytes(raw)
    if attempt is None:
        attempt = {
            "schema": "phase65-fit-attempt/v1",
            "status": "published",
            "pid": 1,
            "started_utc": "2026-10-31T15:00:00+00:00",
            "ended_utc": "2026-10-31T15:30:00+00:00",
            "registration": {
                "path": "reg/smoke-registration.json",
                "sha256": record["registration"]["sha256"],
            },
            "output": "record.json",
            "whole_run_cap_seconds": 3300.0,
            "record_sha256": hashlib.sha256(raw).hexdigest(),
        }
    (path / "attempt.json").write_bytes(
        json.dumps(attempt, indent=2, sort_keys=True).encode("utf-8") + b"\n"
    )
    if receipt is None:
        receipt = {
            "schema": RECEIPT_SCHEMA,
            "checked_utc": "2026-10-31T14:59:00+00:00",
            "power_source": "AC Power",
            "pmset_first_line": "Now drawing from 'AC Power'",
            "registration": "reg/smoke-registration.json",
            "output": "runs/example/record.json",
            "load_average": [1.0, 1.0, 1.0],
            "launched": {
                "module": "pinn.verification.diagnostic_fit", "subcommand": "run"
            },
            "window": {
                "timezone": "America/Chicago",
                "local_time": "2026-10-31T09:59:00-05:00",
                "isoweekday": 6,
            },
        }
    (path / "power-gate.json").write_bytes(
        json.dumps(receipt, indent=2, sort_keys=True).encode("utf-8") + b"\n"
    )
    return path


class ReadingRuleTests(unittest.TestCase):
    """The reading rule at its edges, the confirmation rule and the routes."""

    def test_the_tier1_limit_is_the_scorecards_inclusive_0_1(self):
        card = load_scorecard()
        self.assertEqual(tier1_e_max(card), 0.1)
        self.assertEqual(card.section("tiers")["comparison"], "inclusive_le")

    def test_the_predicted_constants_carry_the_phase_64_values(self):
        self.assertEqual(
            p66.E_CONST_PREDICTED["hierarchical/gold/1632"], 1.1538408194255343
        )
        self.assertEqual(
            p66.E_CONST_PREDICTED["hierarchical/gold/851"], 1.233696866477104
        )
        self.assertEqual(p66.E_CONST_TOLERANCE, 1e-9)
        self.assertEqual(
            dict(p66.IMPROVEMENT_RULE),
            {
                "signal": "similarity.entries[*].output_movement.value",
                "reference_fraction": 0.75,
                "min_growth": 0.01,
            },
        )
        self.assertEqual(p66.FIRST_LAYER_INPUTS, 14)
        self.assertEqual(p66.FREQUENCY_CHECK, (0.95, 1.00001))
        self.assertEqual(
            p66.BRANCHES, ("tier1", "near", "between", "other", "unsettled")
        )
        self.assertEqual(
            p66.ROUTES, ("phase67-as-planned", "propose-66.1", "owner")
        )
        self.assertEqual(
            [(spec["role"], spec["orbit_key"], spec["seed"]) for spec in p66.EXP01_RUNS],
            [
                ("main", "hierarchical/gold/1632", 42),
                ("repeat-system", "hierarchical/gold/851", 42),
                ("repeat-seed", "hierarchical/gold/1632", 41),
            ],
        )

    def test_the_edges_of_the_reading_rule_are_inclusive_at_the_lines(self):
        for orbit_key, e_const in dict(p66.E_CONST_PREDICTED).items():
            with self.subTest(orbit_key=orbit_key):
                self.assertEqual(classify_exp01(0.1, e_const, tier1_max=0.1), "tier1")
                self.assertEqual(
                    classify_exp01(math.nextafter(0.1, math.inf), e_const, tier1_max=0.1),
                    "between",
                )
                self.assertEqual(classify_exp01(0.95 * e_const, e_const, tier1_max=0.1), "near")
                self.assertEqual(classify_exp01(1.05 * e_const, e_const, tier1_max=0.1), "near")
                self.assertEqual(
                    classify_exp01(math.nextafter(0.95 * e_const, -math.inf), e_const, tier1_max=0.1),
                    "between",
                )
                self.assertEqual(
                    classify_exp01(math.nextafter(1.05 * e_const, math.inf), e_const, tier1_max=0.1),
                    "other",
                )
                self.assertEqual(classify_exp01(e_const, e_const, tier1_max=0.1), "near")
                self.assertEqual(classify_exp01(0.5, e_const, tier1_max=0.1), "between")
                self.assertEqual(classify_exp01(2.0, e_const, tier1_max=0.1), "other")
                for bad in (math.nan, math.inf, -math.inf):
                    self.assertEqual(classify_exp01(bad, e_const, tier1_max=0.1), "other")

    def test_a_still_improving_run_is_unsettled_above_the_tier1_line(self):
        e_const = p66.E_CONST_PREDICTED["hierarchical/gold/1632"]
        # Tier 1 stays Tier 1 even while still improving.
        self.assertEqual(
            classify_exp01(0.1, e_const, tier1_max=0.1, still_improving=True), "tier1"
        )
        for e in (
            math.nextafter(0.1, math.inf),
            0.5,
            e_const,          # inside the band
            0.95 * e_const,   # the lower band edge
            1.05 * e_const,   # the upper band edge
            2.0,
        ):
            with self.subTest(e=e):
                self.assertEqual(
                    classify_exp01(e, e_const, tier1_max=0.1, still_improving=True),
                    "unsettled",
                )
        for bad in (math.nan, math.inf, -math.inf):
            self.assertEqual(
                classify_exp01(bad, e_const, tier1_max=0.1, still_improving=True),
                "other",
            )

    def test_confirm_returns_confirmed_only_for_tier1_or_near_tripled(self):
        self.assertEqual(p66.confirm("tier1", "tier1", "tier1"), "confirmed")
        self.assertEqual(p66.confirm("near", "near", "near"), "confirmed")
        for branch in ("between", "other", "unsettled"):
            with self.subTest(branch=branch):
                self.assertEqual(p66.confirm(branch, branch, branch), "unconfirmed")
        for main in ("tier1", "near", "between", "other", "unsettled"):
            for repeat_system in ("tier1", "near", "between", "other", "unsettled"):
                for repeat_seed in ("tier1", "near", "between", "other", "unsettled"):
                    values = (main, repeat_system, repeat_seed)
                    agrees = main == repeat_system == repeat_seed
                    expected = "confirmed" if agrees and main in ("tier1", "near") else "unconfirmed"
                    with self.subTest(values=values):
                        self.assertEqual(p66.confirm(*values), expected)
        for out_of_branch in ("out-of-branch", None):
            with self.subTest(out_of_branch=out_of_branch):
                self.assertEqual(p66.confirm(out_of_branch, "tier1", "tier1"), "unconfirmed")
                self.assertEqual(p66.confirm("near", out_of_branch, "near"), "unconfirmed")

    def test_route_sends_confirmed_tier1_and_near_and_everything_else_to_the_owner(self):
        self.assertEqual(p66.route("tier1", "confirmed"), "phase67-as-planned")
        self.assertEqual(p66.route("near", "confirmed"), "propose-66.1")
        for main in ("tier1", "near", "between", "other", "unsettled", "out-of-branch"):
            for confirmation in ("confirmed", "unconfirmed"):
                expected = {
                    ("tier1", "confirmed"): "phase67-as-planned",
                    ("near", "confirmed"): "propose-66.1",
                }.get((main, confirmation), "owner")
                with self.subTest(main=main, confirmation=confirmation):
                    self.assertEqual(p66.route(main, confirmation), expected)
        for branch in ("tier1", "near", "between", "other", "unsettled"):
            with self.subTest(branch=branch):
                self.assertEqual(p66.route(branch, "unconfirmed"), "owner")


class ImprovementTests(unittest.TestCase):
    """The improvement check over synthetic similarity entries."""

    def _entries(self, movements, steps=None):
        steps = CADENCE if steps is None else steps
        return [
            {"step": step, "output_movement": {"value": value}}
            for step, value in zip(steps, movements)
        ]

    def test_the_reference_is_the_last_cadence_entry_at_or_before_three_quarters(self):
        flat = [0.5] * len(CADENCE)
        result = p66.improvement_check(self._entries(flat), final_step=268000)
        self.assertEqual(result["reference_step"], 184000)
        self.assertEqual(0.75 * 268000, 201000)
        short = p66.improvement_check(
            self._entries([0.5, 0.5], steps=[0, 5200]), final_step=5200
        )
        self.assertEqual(short["reference_step"], 0)
        self.assertEqual(short["final_step"], 5200)

    def test_the_growth_threshold_is_strict_at_min_growth(self):
        flat = [0.0] * len(CADENCE)
        exactly = list(flat)
        exactly[-1] = 0.01
        result = p66.improvement_check(self._entries(exactly), final_step=268000)
        self.assertIs(result["still_improving"], False)
        self.assertEqual(result["growth"], 0.01)
        grown = list(flat)
        grown[-1] = math.nextafter(0.01, math.inf)
        self.assertIs(
            p66.improvement_check(self._entries(grown), final_step=268000)["still_improving"],
            True,
        )
        falling = [0.5] * len(CADENCE)
        falling[-1] = 0.005
        result = p66.improvement_check(self._entries(falling), final_step=268000)
        self.assertIs(result["still_improving"], False)
        self.assertEqual(
            set(result),
            {
                "reference_step", "reference_output_movement", "final_step",
                "final_output_movement", "growth", "min_growth", "still_improving",
            },
        )
        self.assertEqual(result["min_growth"], 0.01)
        self.assertEqual(result["reference_output_movement"], 0.5)
        self.assertEqual(result["final_output_movement"], 0.005)

    def test_an_unevaluable_improvement_check_raises(self):
        without_final = self._entries([0.5] * (len(CADENCE) - 1))
        with self.assertRaises(ValueError):
            p66.improvement_check(without_final, final_step=268000)
        missing_at_reference = [
            {"step": step, "output_movement": {"value": 0.5}}
            for step in CADENCE
        ]
        reference_index = CADENCE.index(184000)  # the reference entry
        del missing_at_reference[reference_index]["output_movement"]
        with self.assertRaises(ValueError):
            p66.improvement_check(missing_at_reference, final_step=268000)
        non_finite_final = self._entries([0.5] * (len(CADENCE) - 1) + [math.nan])
        with self.assertRaises(ValueError):
            p66.improvement_check(non_finite_final, final_step=268000)


class RecordReaderTests(unittest.TestCase):
    """The record and run-directory readers, and the score-free check-run."""

    def test_a_clean_record_reads_clean_with_branch_equal_to_e_band(self):
        reading = p66.read_exp01_record(_synthetic_record(), tier1_max=0.1)
        self.assertEqual(reading["mechanical_problems"], [])
        self.assertEqual(reading["setting_problems"], [])
        self.assertIs(reading["improvement"]["still_improving"], False)
        self.assertEqual(reading["e_band"], "near")
        self.assertEqual(reading["branch"], reading["e_band"])
        self.assertEqual(reading["orbit_key"], "hierarchical/gold/1632")
        self.assertEqual(reading["seed"], 42)
        self.assertEqual(reading["registration_sha256"], "a" * 64)
        self.assertEqual(reading["E_const"], p66.E_CONST_PREDICTED["hierarchical/gold/1632"])
        self.assertEqual(reading["two_kepler"], 0.9168487091299374)
        self.assertEqual(reading["steps_completed"], 268000)
        self.assertEqual(reading["output_movement_final"], 0.5)
        self.assertEqual(reading["first_layer_frequency"]["step_0"], 22.7)

    def test_a_still_improving_non_tier1_run_reads_unsettled(self):
        movements = [0.5] * 11 + [0.5, 0.51, 0.52]
        reading = p66.read_exp01_record(
            _synthetic_record(movements=movements, e=1.18), tier1_max=0.1
        )
        self.assertEqual(reading["mechanical_problems"], [])
        self.assertIs(reading["improvement"]["still_improving"], True)
        self.assertEqual(reading["e_band"], "near")
        self.assertEqual(reading["branch"], "unsettled")
        tier1_reading = p66.read_exp01_record(
            _synthetic_record(movements=movements, e=0.1), tier1_max=0.1
        )
        self.assertEqual(tier1_reading["branch"], "tier1")
        self.assertEqual(tier1_reading["e_band"], "tier1")

    def test_each_mechanical_problem_reads_out_of_branch(self):
        tier1_disagree = _synthetic_record(tier=1)  # E sits in the near band
        extra_row = _synthetic_record()
        extra_row["similarity"]["entries"][0]["layers"].append(
            {"name": "h2", "order": 2, "adjacent_cosine_mean": 0.9}
        )
        drifted = _synthetic_record(
            e_const=p66.E_CONST_PREDICTED["hierarchical/gold/1632"] + 1e-6
        )
        no_final = _synthetic_record(movements=[0.5] * (len(CADENCE) - 1))
        non_finite = _synthetic_record(
            movements=[0.5] * (len(CADENCE) - 1) + [math.inf]
        )
        unregistered = _synthetic_record()
        unregistered["variant"]["registered"] = False
        wrong_registry = _synthetic_record()
        wrong_registry["variant"]["registry"] = "phase65"
        validation_open = _synthetic_record()
        validation_open["access"]["reads"]["validation"] = 1
        test_open = _synthetic_record()
        test_open["access"]["attestation"]["test_split_opened"] = 2

        cases = [
            ("status not complete", _synthetic_record(status="incomplete"),
             "the run status is not complete"),
            ("tier disagreeing with E", tier1_disagree,
             "the recorded scorecard grade disagrees with the network error"),
            ("E_const off its prediction", drifted,
             "the record's constant-predictor score disagrees with its predicted value"),
            ("similarity rows other than input and h1", extra_row,
             "the similarity log carries rows other than input and h1"),
            ("improvement not evaluable: no final entry", no_final,
             "the improvement check cannot be evaluated"),
            ("improvement not evaluable: non-finite final", non_finite,
             "the improvement check cannot be evaluated"),
            ("registered is false", unregistered,
             "the record's variant registry fields are wrong"),
            ("registry is not phase66", wrong_registry,
             "the record's variant registry fields are wrong"),
            ("a validation open", validation_open,
             "a validation or test split was opened"),
            ("a test-split open", test_open,
             "a validation or test split was opened"),
        ]
        for name, record, problem in cases:
            with self.subTest(problem=name):
                reading = p66.read_exp01_record(record, tier1_max=0.1)
                self.assertIn(problem, reading["mechanical_problems"])
                self.assertEqual(reading["branch"], "out-of-branch")
                # The label band is still computed from E alone.
                self.assertIn(reading["e_band"], p66.BRANCHES)

    def test_the_step_0_bandwidth_check_is_a_setting_problem(self):
        wide_open = _synthetic_record(step0_frequency_max=0.68)
        reading = p66.read_exp01_record(wide_open, tier1_max=0.1)
        self.assertEqual(reading["setting_problems"],
                         ["the step-0 first-layer bandwidth check failed"])
        self.assertEqual(reading["mechanical_problems"], [])
        self.assertEqual(reading["branch"], "unsettled")  # E in the near band
        between = p66.read_exp01_record(
            _synthetic_record(step0_frequency_max=0.68, e=0.9), tier1_max=0.1
        )
        self.assertEqual(between["e_band"], "between")
        self.assertEqual(between["branch"], "unsettled")
        tier1_fit = p66.read_exp01_record(
            _synthetic_record(step0_frequency_max=0.68, e=0.1), tier1_max=0.1
        )
        self.assertEqual(tier1_fit["branch"], "out-of-branch")
        # A step-0 maximum inside the band is no setting problem.
        good = p66.read_exp01_record(
            _synthetic_record(step0_frequency_max=22.73), tier1_max=0.1
        )
        self.assertEqual(good["setting_problems"], [])

    def test_read_run_directory_adds_the_receipt_window_and_attempt_checks(self):
        tmp = Path(self.enterContext(
            tempfile.TemporaryDirectory(prefix="phase66-reader-")
        ))

        def directory(name, record=None, receipt="default", attempt=None):
            record = _synthetic_record() if record is None else record
            return _write_directory(
                tmp / name, record,
                receipt=None if receipt == "default" else receipt,
                attempt=attempt,
            )

        clean = p66.read_run_directory(directory("clean"), tier1_max=0.1)
        self.assertEqual(clean["mechanical_problems"], [])
        self.assertEqual(clean["setting_problems"], [])
        self.assertNotEqual(clean["branch"], "out-of-branch")

        missing_receipt = directory("missing-receipt")
        (missing_receipt / "power-gate.json").unlink()
        reading = p66.read_run_directory(missing_receipt, tier1_max=0.1)
        self.assertIn("the power-gate receipt is missing", reading["mechanical_problems"])
        self.assertEqual(reading["branch"], "out-of-branch")

        battery = directory(
            "battery",
            receipt={"schema": RECEIPT_SCHEMA, "checked_utc": "2026-10-31T14:59:00+00:00",
                     "power_source": "Battery Power",
                     "window": {"timezone": "America/Chicago",
                                "local_time": "2026-10-31T09:59:00-05:00",
                                "isoweekday": 6}},
        )
        reading = p66.read_run_directory(battery, tier1_max=0.1)
        self.assertIn("the receipt does not record AC Power", reading["mechanical_problems"])

        weekday_window = directory(
            "weekday",
            receipt={"schema": RECEIPT_SCHEMA, "checked_utc": "2026-10-28T14:59:00+00:00",
                     "power_source": "AC Power",
                     "window": {"timezone": "America/Chicago",
                                "local_time": "2026-10-28T09:59:00-05:00",
                                "isoweekday": 3}},
        )
        reading = p66.read_run_directory(weekday_window, tier1_max=0.1)
        self.assertIn("the receipt window is outside the weekend window",
                      reading["mechanical_problems"])

        late_receipt = directory(
            "late",
            receipt={"schema": RECEIPT_SCHEMA, "checked_utc": "2026-10-31T15:01:00+00:00",
                     "power_source": "AC Power",
                     "window": {"timezone": "America/Chicago",
                                "local_time": "2026-10-31T10:01:00-05:00",
                                "isoweekday": 6}},
        )
        reading = p66.read_run_directory(late_receipt, tier1_max=0.1)
        self.assertIn("the receipt was written after the attempt started",
                      reading["mechanical_problems"])

        running = directory(
            "running",
            attempt={"schema": "phase65-fit-attempt/v1", "status": "running",
                     "pid": 1, "started_utc": "2026-10-31T15:00:00+00:00",
                     "record_sha256": "0" * 64},
        )
        reading = p66.read_run_directory(running, tier1_max=0.1)
        self.assertIn("the attempt is not published", reading["mechanical_problems"])

        wrong_digest = directory("wrong-digest")
        payload = json.loads((wrong_digest / "attempt.json").read_bytes())
        payload["record_sha256"] = "f" * 64
        (wrong_digest / "attempt.json").write_bytes(
            json.dumps(payload, indent=2, sort_keys=True).encode("utf-8") + b"\n"
        )
        reading = p66.read_run_directory(wrong_digest, tier1_max=0.1)
        self.assertIn("the attempt's record digest disagrees with the record bytes",
                      reading["mechanical_problems"])
        self.assertEqual(reading["branch"], "out-of-branch")

    def test_check_run_prints_only_the_directory_and_value_free_problems(self):
        tmp = Path(self.enterContext(
            tempfile.TemporaryDirectory(prefix="phase66-check-")
        ))
        record = _synthetic_record(e=0.123456789, movements=[0.777] * len(CADENCE))
        clean_dir = _write_directory(tmp / "clean", record)
        stdout = io.StringIO()
        stderr = io.StringIO()
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            code = p66.main(["check-run", "--dir", str(clean_dir)])
        self.assertEqual(code, 0)
        combined = stdout.getvalue() + stderr.getvalue()
        self.assertIn("EXP01-CHECK-OK", combined)
        payload = json.loads(stdout.getvalue().split("EXP01-CHECK-OK")[0])
        self.assertEqual(
            set(payload), {"dir", "mechanical_problems", "setting_problems"}
        )
        self.assertEqual(payload["mechanical_problems"], [])
        for secret in ("0.123456789", "1.1538408194255343", "14.493981514909423",
                       "0.777", "branch", "tier", "improvement"):
            self.assertNotIn(secret, combined)

        spent = _synthetic_record(e=0.123456789, status="incomplete")
        problem_dir = _write_directory(tmp / "spent", spent)
        stdout = io.StringIO()
        stderr = io.StringIO()
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            code = p66.main(["check-run", "--dir", str(problem_dir)])
        self.assertEqual(code, 2)
        combined = stdout.getvalue() + stderr.getvalue()
        self.assertIn("EXP01-CHECK-PROBLEMS", combined)
        payload = json.loads(stdout.getvalue().split("EXP01-CHECK-PROBLEMS")[0])
        self.assertIn("the run status is not complete", payload["mechanical_problems"])
        for secret in ("0.123456789", "1.1538408194255343", "14.493981514909423",
                       "0.777"):
            self.assertNotIn(secret, combined)


class RunIdentityTests(unittest.TestCase):
    """The run-identity triple and the three-run review."""

    def test_two_records_sharing_a_run_id_are_distinct_runs_by_the_triple(self):
        first = p66.read_exp01_record(
            _synthetic_record(seed=42, registration="a" * 64), tier1_max=0.1
        )
        second = p66.read_exp01_record(
            _synthetic_record(seed=41, registration="b" * 64, run_id=first["run_id"]),
            tier1_max=0.1,
        )
        first_key = (first["orbit_key"], first["seed"], first["registration_sha256"])
        second_key = (second["orbit_key"], second["seed"], second["registration_sha256"])
        self.assertNotEqual(first_key, second_key)
        self.assertEqual(first["run_id"], second["run_id"])

    def _three_directories(self, tmp, *, seed_repeat=41, repeat_registration="c" * 64,
                           main_movements=None, repeat_movements=None):
        flat = [0.5] * len(CADENCE)
        main_record = _synthetic_record(
            e=1.18, movements=main_movements if main_movements is not None else flat,
        )
        system_record = _synthetic_record(
            orbit_key="hierarchical/gold/851", e=1.26, run_id="exp01-d1-w384-o1000-851",
            registration="b" * 64,
            movements=repeat_movements if repeat_movements is not None else flat,
        )
        seed_record = _synthetic_record(
            seed=seed_repeat, run_id="exp01-d1-w384-o1000-1632",
            registration=repeat_registration,
            movements=repeat_movements if repeat_movements is not None else flat,
        )
        return (
            _write_directory(tmp / "main", main_record),
            _write_directory(tmp / "repeat-system", system_record),
            _write_directory(tmp / "repeat-seed", seed_record),
        )

    def test_review_refuses_two_role_directories_that_are_the_same_run(self):
        tmp = Path(self.enterContext(
            tempfile.TemporaryDirectory(prefix="phase66-identity-")
        ))
        main_dir, system_dir, seed_dir = self._three_directories(tmp)
        duplicate = _write_directory(
            tmp / "duplicate",
            _synthetic_record(e=1.18, movements=[0.5] * len(CADENCE)),
        )
        stderr = io.StringIO()
        with contextlib.redirect_stderr(stderr):
            code = p66.main([
                "review", "--main", str(main_dir),
                "--repeat-system", str(duplicate), "--repeat-seed", str(seed_dir),
            ])
        self.assertEqual(code, 2)
        self.assertIn("EXP01-REFUSED", stderr.getvalue())
        # The clean trio is not refused: the duplicate is the only difference.
        with contextlib.redirect_stderr(io.StringIO()):
            with contextlib.redirect_stdout(io.StringIO()):
                code = p66.main([
                    "review", "--main", str(main_dir),
                    "--repeat-system", str(system_dir), "--repeat-seed", str(seed_dir),
                ])
        self.assertEqual(code, 0)

    def test_review_refuses_a_role_whose_orbit_or_seed_differs(self):
        tmp = Path(self.enterContext(
            tempfile.TemporaryDirectory(prefix="phase66-roles-")
        ))
        main_dir, system_dir, _seed_dir = self._three_directories(tmp)
        wrong_seed = _write_directory(
            tmp / "wrong-seed",
            _synthetic_record(seed=42, registration="d" * 64,
                              run_id="exp01-d1-w384-o1000-1632"),
        )
        stderr = io.StringIO()
        with contextlib.redirect_stderr(stderr):
            code = p66.main([
                "review", "--main", str(main_dir),
                "--repeat-system", str(system_dir), "--repeat-seed", str(wrong_seed),
            ])
        self.assertEqual(code, 2)
        self.assertIn("EXP01-REFUSED", stderr.getvalue())
        wrong_orbit = _write_directory(
            tmp / "wrong-orbit",
            _synthetic_record(orbit_key="hierarchical/gold/4658", seed=41,
                              registration="e" * 64, e_const=1.1396,
                              run_id="exp01-d1-w384-o1000-4658"),
        )
        stderr = io.StringIO()
        with contextlib.redirect_stderr(stderr):
            code = p66.main([
                "review", "--main", str(main_dir),
                "--repeat-system", str(system_dir), "--repeat-seed", str(wrong_orbit),
            ])
        self.assertEqual(code, 2)
        self.assertIn("EXP01-REFUSED", stderr.getvalue())

    def test_review_confirms_three_settled_near_runs_and_routes_to_66_1(self):
        tmp = Path(self.enterContext(
            tempfile.TemporaryDirectory(prefix="phase66-review-")
        ))
        main_dir, system_dir, seed_dir = self._three_directories(tmp)
        stdout = io.StringIO()
        stderr = io.StringIO()
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            code = p66.main([
                "review", "--main", str(main_dir),
                "--repeat-system", str(system_dir), "--repeat-seed", str(seed_dir),
            ])
        self.assertEqual(code, 0)
        payload = json.loads(stdout.getvalue().split("EXP01-REVIEW")[0])
        self.assertEqual(set(payload), {"runs", "confirmation", "route"})
        self.assertEqual(sorted(payload["runs"]), ["main", "repeat-seed", "repeat-system"])
        self.assertEqual(payload["confirmation"], "confirmed")
        self.assertEqual(payload["route"], "propose-66.1")
        self.assertIn("EXP01-REVIEW confirmation=confirmed route=propose-66.1",
                      stdout.getvalue())

    def test_one_still_improving_run_refuses_confirmation_and_routes_to_owner(self):
        tmp = Path(self.enterContext(
            tempfile.TemporaryDirectory(prefix="phase66-review-improving-")
        ))
        growing = [0.5] * 11 + [0.5, 0.51, 0.52]
        main_dir, system_dir, seed_dir = self._three_directories(
            tmp, main_movements=growing, repeat_movements=growing,
        )
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            code = p66.main([
                "review", "--main", str(main_dir),
                "--repeat-system", str(system_dir), "--repeat-seed", str(seed_dir),
            ])
        self.assertEqual(code, 0)
        payload = json.loads(stdout.getvalue().split("EXP01-REVIEW")[0])
        self.assertEqual(payload["confirmation"], "unconfirmed")
        self.assertEqual(payload["route"], "owner")
        self.assertIn("EXP01-REVIEW confirmation=unconfirmed route=owner",
                      stdout.getvalue())


if __name__ == "__main__":
    unittest.main()
