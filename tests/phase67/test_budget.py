"""Plan 67-04 task 67-04-02: the common update budget from every timing row.

D-07/D-08/D-09/D-10 (through 67-RESEARCH's budget recommendation): every arm
and repeat within an experiment receives the same update count, derived only
from measured cost. ``phase67_budget(cost_rows, *, expected_identities)``
takes the validated cost-only rows of one experiment's registered timing runs
— keyed by the complete experiment/arm/orbit/seed/window identity, at the
registered timing scale 1200/200/1000 with all actual checkpoint costs and
the full-launch wall — and returns the largest multiple of the 100-step
quantum at or above the 300-step floor whose every-row projected whole-run
wall (the launch residual ``F`` plus the measured warmup, the measured steps
at the timing rate with the 25 percent margin, five maximum logger events,
three maximum scorer events and the byte-scaled publication I/O) stays within
75 percent of the 3,540-second cap. Row permutation and changed scientific
scores leave the budget unchanged; a slow repeat constrains it; missing,
duplicate, malformed, non-finite or boolean rows refuse; a negative launch
residual beyond 1e-9 seconds refuses; equality at the target is admitted and
the next 100-step candidate exceeds it; an unsafe record size refuses rather
than shortening science; and no score, loss, tier or cosine value enters the
projection or the output (T-67-10/T-67-11).
"""

from __future__ import annotations

import json
import math
import unittest

from pinn.verification.diagnostic_fit import HOUR_SECONDS  # noqa: F401  (cap sanity)
from pinn.verification import diagnostic_phase67 as p67


def _p67():
    """The module under test (already imported above; kept for symmetry)."""
    return p67


RULE = p67.PHASE67_BUDGET_RULE
TARGET = float(RULE["time_fraction"]) * float(RULE["cap_seconds"])
QUANTUM = int(RULE["step_quantum"])


def _identity(experiment="exp02", arm="d2", orbit="hierarchical/gold/1632",
              seed=42, window=10.0):
    return {
        "experiment": experiment,
        "arm": arm,
        "orbit_key": orbit,
        "seed": seed,
        "window": window,
    }


def _identity_key(identity):
    """The canonical identity key the budget output uses (test-side copy)."""
    return "|".join((
        str(identity["experiment"]),
        str(identity["arm"]),
        str(identity["orbit_key"]),
        str(int(identity["seed"])),
        repr(float(identity["window"])),
    ))


def _cost_row(identity=None, **overrides):
    """One validated synthetic cost row at the registered timing scale."""
    row = {
        "identity": dict(_identity() if identity is None else identity),
        "timing": {
            "optimizer_steps": int(RULE["timing_steps"]),
            "warmup_steps": int(RULE["timing_warmup"]),
            "measured_steps": int(RULE["timing_measured"]),
            "seconds_per_step": 0.004,
            "warmup_seconds": 0.8,
            "measured_seconds": 4.0,
        },
        "logger_event_seconds": [0.05, 0.06, 0.05, 0.07, 0.06],
        "scorer_event_seconds": [0.6, 0.6, 0.6],
        "publication_io_seconds": 0.05,
        "launch_wall_seconds": 30.0,
        "record_bytes": 400000,
        "weights_bytes": 1100000,
    }
    row.update(overrides)
    return row


def _three_cases():
    """The declared main and repeat identities (D-09), main + 851 + seed41."""
    return [
        _identity(arm="d2", orbit="hierarchical/gold/1632", seed=42),
        _identity(arm="d2", orbit="hierarchical/gold/851", seed=42),
        _identity(arm="d2", orbit="hierarchical/gold/1632", seed=41),
    ]


def _rows_for(identities, **per_row):
    rows = []
    for index, identity in enumerate(identities):
        overrides = per_row.get(index, {})
        rows.append(_cost_row(identity=identity, **overrides))
    return rows


def _project(row, n):
    """The registered per-row projection at ``n`` steps (independent copy)."""
    timing = row["timing"]
    fixed = float(row["launch_wall_seconds"]) - (
        float(timing["warmup_seconds"])
        + float(timing["measured_seconds"])
        + sum(float(v) for v in row["logger_event_seconds"])
        + sum(float(v) for v in row["scorer_event_seconds"])
        + float(row["publication_io_seconds"])
    )
    published = int(row["record_bytes"]) + int(row["weights_bytes"])
    stride = p67.phase67_loss_trace_stride(n)
    entries = p67.phase67_loss_trace_entries(n, stride)
    timing_entries = p67.phase67_loss_trace_entries(
        int(RULE["timing_steps"]), p67.phase67_loss_trace_stride(int(RULE["timing_steps"]))
    )
    growth = max(0, len(str(n)) - len(str(int(RULE["timing_steps"]))))
    bound = (
        published
        + int(RULE["loss_entry_bytes"]) * max(0, entries - timing_entries)
        + growth * (int(RULE["similarity_events"]) + int(RULE["score_events"]) + entries)
    )
    ratio = max(1.0, bound / published)
    return (
        fixed
        + float(timing["warmup_seconds"])
        + (n - int(RULE["warmup_steps"]))
        * float(timing["seconds_per_step"])
        * (1.0 + float(RULE["rate_margin"]))
        + int(RULE["similarity_events"]) * max(float(v) for v in row["logger_event_seconds"])
        + int(RULE["score_events"]) * max(float(v) for v in row["scorer_event_seconds"])
        + float(row["publication_io_seconds"]) * ratio
    )


class BudgetRuleTests(unittest.TestCase):
    """The budget rule's own numbers stay the registered ones."""

    def test_the_rule_bounds_the_science_cap_under_the_hour_refusal(self):
        self.assertLess(float(RULE["cap_seconds"]), HOUR_SECONDS)
        self.assertEqual(RULE["min_steps"] % QUANTUM, 0)
        self.assertGreater(RULE["min_steps"], int(RULE["warmup_steps"]))
        self.assertEqual(
            int(RULE["timing_steps"]) - int(RULE["timing_warmup"]),
            int(RULE["timing_measured"]),
        )
        self.assertLess(float(RULE["timing_cap_seconds"]), float(RULE["cap_seconds"]))


class CommonBudgetTests(unittest.TestCase):
    """The largest common update count over every registered timing row."""

    def test_the_budget_picks_the_largest_common_n_for_every_row(self):
        identities = _three_cases()
        rows = _rows_for(identities)
        budget = p67.phase67_budget(rows, expected_identities=identities)
        n = budget["common_optimizer_steps"]
        self.assertIsInstance(n, int)
        self.assertEqual(n % QUANTUM, 0)
        self.assertGreaterEqual(n, int(RULE["min_steps"]))
        self.assertEqual(budget["warmup_steps"], int(RULE["warmup_steps"]))
        self.assertEqual(budget["measured_steps"], n - int(RULE["warmup_steps"]))
        self.assertEqual(budget["similarity_cadence"], p67.phase67_cadence(n))
        self.assertEqual(budget["score_cadence"], p67.phase67_score_cadence(n))
        self.assertEqual(budget["loss_trace_stride"], p67.phase67_loss_trace_stride(n))
        projections = budget["per_row_projection_seconds"]
        self.assertEqual(
            set(projections), {_identity_key(identity) for identity in identities}
        )
        for row in rows:
            expected = _project(row, n)
            self.assertAlmostEqual(
                projections[_identity_key(row["identity"])], expected, places=9
            )
            self.assertLessEqual(projections[_identity_key(row["identity"])], TARGET)
        # Maximality: the next 100-step candidate exceeds the target for the
        # binding row, so N + 100 cannot fit.
        self.assertGreater(max(_project(row, n + QUANTUM) for row in rows), TARGET)
        self.assertLessEqual(max(_project(row, n) for row in rows), TARGET)
        # Every required output field is present.
        for field in (
            "common_optimizer_steps", "warmup_steps", "measured_steps",
            "similarity_cadence", "score_cadence", "loss_trace_stride",
            "per_row_projection_seconds", "timing_evidence_digests",
            "experiment_projected_seconds", "phase_cost_ledger",
        ):
            self.assertIn(field, budget)

    def test_a_slow_repeat_constrains_the_common_budget(self):
        identities = _three_cases()
        fast = p67.phase67_budget(
            _rows_for(identities), expected_identities=identities
        )
        slow_rows = _rows_for(identities)
        slow_rows[2]["timing"]["seconds_per_step"] = 0.008
        slow = p67.phase67_budget(slow_rows, expected_identities=identities)
        self.assertLess(slow["common_optimizer_steps"], fast["common_optimizer_steps"])
        self.assertLessEqual(
            max(_project(row, slow["common_optimizer_steps"]) for row in slow_rows),
            TARGET,
        )

    def test_row_permutation_and_changed_scientific_scores_change_nothing(self):
        identities = _three_cases()
        plain = p67.phase67_budget(
            _rows_for(identities), expected_identities=identities
        )
        permuted = list(reversed(_rows_for(identities)))
        for row in permuted:
            # Scientific values the cost row must never read: changed scores,
            # losses and cosines leave the budget unchanged.
            row["E"] = 0.987654321
            row["tier"] = 1
            row["loss_final"] = 0.0321
            row["h1_cosine"] = 0.99
        shuffled = p67.phase67_budget(permuted, expected_identities=identities)
        self.assertEqual(
            json.dumps(shuffled, sort_keys=True), json.dumps(plain, sort_keys=True)
        )

    def test_target_equality_is_admitted_and_the_next_quantum_exceeds_it(self):
        # Exact-arithmetic row: every constant is a dyadic rational, so the
        # projection at N = 17100 equals 0.75 * 3540 exactly (2655.0), and
        # N + 100 exceeds it by a full quantum's cost.
        identity = _identity(orbit="hierarchical/gold/1632", seed=42)
        row = _cost_row(
            identity=identity,
            timing={
                "optimizer_steps": 1200, "warmup_steps": 200, "measured_steps": 1000,
                "seconds_per_step": 0.125, "warmup_seconds": 0.0,
                "measured_seconds": 4.0,
            },
            logger_event_seconds=[0.0] * 5,
            scorer_event_seconds=[0.0] * 3,
            publication_io_seconds=0.0,
            launch_wall_seconds=18.375,
        )
        budget = p67.phase67_budget([row], expected_identities=[identity])
        self.assertEqual(budget["common_optimizer_steps"], 17100)
        self.assertEqual(
            budget["per_row_projection_seconds"][_identity_key(identity)], 2655.0
        )
        self.assertEqual(_project(row, 17100), 2655.0)
        self.assertGreater(_project(row, 17100 + QUANTUM), TARGET)

    def test_measured_checkpoint_costs_are_included_in_the_projection(self):
        identity = _identity()
        bare = _cost_row(
            identity=identity,
            timing={
                "optimizer_steps": 1200, "warmup_steps": 200, "measured_steps": 1000,
                "seconds_per_step": 0.0125, "warmup_seconds": 0.0,
                "measured_seconds": 4.0,
            },
            logger_event_seconds=[0.0] * 5,
            scorer_event_seconds=[0.0] * 3,
            publication_io_seconds=0.0,
            launch_wall_seconds=18.375,
        )
        # One slow logger event (max 2.0 s over a 0-sum... non-uniform) and
        # one slow scorer event: the projection re-adds 5*max logger and
        # 3*max scorer seconds for the science run's own events, so the net
        # inclusion beyond the timing run's own itemized sums is
        # (5*2 - 2) + (3*6 - 6) = 20 seconds at every N.
        loaded = json.loads(json.dumps(bare))
        loaded["logger_event_seconds"] = [0.0, 0.0, 0.0, 0.0, 2.0]
        loaded["scorer_event_seconds"] = [0.0, 0.0, 6.0]
        budget_bare = p67.phase67_budget([bare], expected_identities=[identity])
        budget_loaded = p67.phase67_budget([loaded], expected_identities=[identity])
        self.assertLess(
            budget_loaded["common_optimizer_steps"],
            budget_bare["common_optimizer_steps"],
        )
        for n in (300, 1700, 169200):
            with self.subTest(n=n):
                self.assertAlmostEqual(
                    _project(loaded, n) - _project(bare, n), 20.0, places=9
                )
        n_loaded = budget_loaded["common_optimizer_steps"]
        self.assertAlmostEqual(
            budget_loaded["per_row_projection_seconds"][_identity_key(identity)],
            _project(loaded, n_loaded),
            places=9,
        )

    def test_the_publication_io_scales_with_the_predicted_byte_bound(self):
        identity = _identity()
        row = _cost_row(
            identity=identity,
            timing={
                "optimizer_steps": 1200, "warmup_steps": 200, "measured_steps": 1000,
                "seconds_per_step": 0.125, "warmup_seconds": 0.0,
                "measured_seconds": 4.0,
            },
            logger_event_seconds=[0.0] * 5,
            scorer_event_seconds=[0.0] * 3,
            publication_io_seconds=2.0,
            launch_wall_seconds=18.375,
            record_bytes=400000,
            weights_bytes=1100000,
        )
        budget = p67.phase67_budget([row], expected_identities=[identity])
        n = budget["common_optimizer_steps"]
        published = 400000 + 1100000
        stride = p67.phase67_loss_trace_stride(n)
        entries = p67.phase67_loss_trace_entries(n, stride)
        timing_entries = 600
        growth = max(0, len(str(n)) - 4)
        bound = (
            published + 32 * max(0, entries - timing_entries)
            + growth * (5 + 3 + entries)
        )
        self.assertGreater(bound, published)  # science writes more than timing
        # F = 18.375 - (0 + 4 + 0 + 0 + 2.0) = 12.375; the publication term
        # carries the byte-bound ratio, not the bare measured seconds.
        self.assertAlmostEqual(
            budget["per_row_projection_seconds"][_identity_key(identity)],
            12.375 + (n - 200) * 0.15625 + 2.0 * (bound / published),
            places=9,
        )

    def test_an_unsafe_record_size_refuses_rather_than_shortening_science(self):
        identity = _identity()
        row = _cost_row(identity=identity, weights_bytes=9800000)
        with self.assertRaises(ValueError) as raised:
            p67.phase67_budget([row], expected_identities=[identity])
        self.assertIn("size", str(raised.exception))

    def test_no_admissible_n_yields_an_explicit_resource_refusal(self):
        identity = _identity()
        row = _cost_row(identity=identity)
        row["timing"]["seconds_per_step"] = 30.0
        with self.assertRaises(ValueError) as raised:
            p67.phase67_budget([row], expected_identities=[identity])
        self.assertIn("no admissible", str(raised.exception))


class BudgetValidationTests(unittest.TestCase):
    """Every declared row must be present, unique, well-formed and finite."""

    def test_a_missing_declared_row_refuses_including_seed41(self):
        identities = _three_cases()
        rows = _rows_for(identities)
        for missing_index in range(3):
            with self.subTest(missing=identities[missing_index]):
                incomplete = [row for i, row in enumerate(rows) if i != missing_index]
                with self.assertRaises(ValueError) as raised:
                    p67.phase67_budget(incomplete, expected_identities=identities)
                self.assertIn("missing", str(raised.exception))
                self.assertIn(str(identities[missing_index]["seed"]), str(raised.exception))

    def test_a_duplicate_or_unknown_row_refuses(self):
        identities = _three_cases()
        rows = _rows_for(identities)
        duplicated = rows + [json.loads(json.dumps(rows[0]))]
        with self.assertRaises(ValueError) as raised:
            p67.phase67_budget(duplicated, expected_identities=identities)
        self.assertIn("duplicate", str(raised.exception))
        unknown = _cost_row(identity=_identity(arm="d12"))
        with self.assertRaises(ValueError) as raised:
            p67.phase67_budget(rows + [unknown], expected_identities=identities)
        self.assertIn("not a declared identity", str(raised.exception))

    def test_malformed_nonfinite_and_boolean_rows_refuse(self):
        identity = _identity()
        bad_rows = []
        row = _cost_row(identity=identity)
        nonfinite = json.loads(json.dumps(row))
        nonfinite["timing"]["seconds_per_step"] = float("nan")
        bad_rows.append(("nonfinite rate", nonfinite))
        boolean = json.loads(json.dumps(row))
        boolean["launch_wall_seconds"] = True
        bad_rows.append(("boolean wall", boolean))
        negative = json.loads(json.dumps(row))
        negative["logger_event_seconds"] = [-0.1, 0.0, 0.0, 0.0, 0.0]
        bad_rows.append(("negative event", negative))
        short_events = json.loads(json.dumps(row))
        short_events["logger_event_seconds"] = [0.05] * 4
        bad_rows.append(("four logger events", short_events))
        short_scorer = json.loads(json.dumps(row))
        short_scorer["scorer_event_seconds"] = [0.6, 0.6]
        bad_rows.append(("two scorer events", short_scorer))
        wrong_steps = json.loads(json.dumps(row))
        wrong_steps["timing"]["optimizer_steps"] = 1100
        wrong_steps["timing"]["measured_steps"] = 900
        bad_rows.append(("wrong timing steps", wrong_steps))
        wrong_warmup = json.loads(json.dumps(row))
        wrong_warmup["timing"]["warmup_steps"] = 100
        bad_rows.append(("wrong timing warmup", wrong_warmup))
        zero_rate = json.loads(json.dumps(row))
        zero_rate["timing"]["seconds_per_step"] = 0.0
        bad_rows.append(("zero rate", zero_rate))
        fractional_bytes = json.loads(json.dumps(row))
        fractional_bytes["record_bytes"] = 400000.5
        bad_rows.append(("fractional bytes", fractional_bytes))
        boolean_seed = json.loads(json.dumps(row))
        boolean_seed["identity"]["seed"] = True
        bad_rows.append(("boolean seed", boolean_seed))
        missing_field = json.loads(json.dumps(row))
        missing_field["identity"].pop("window")
        bad_rows.append(("incomplete identity", missing_field))
        string_window = json.loads(json.dumps(row))
        string_window["identity"]["window"] = "10.0"
        bad_rows.append(("string window", string_window))
        infinite_wall = json.loads(json.dumps(row))
        infinite_wall["launch_wall_seconds"] = float("inf")
        bad_rows.append(("infinite wall", infinite_wall))
        for name, bad in bad_rows:
            with self.subTest(case=name):
                with self.assertRaises(ValueError):
                    p67.phase67_budget([bad], expected_identities=[identity])

    def test_a_negative_residual_beyond_the_tolerance_refuses(self):
        identity = _identity()
        within = _cost_row(identity=identity)
        # launch wall 1e-10 s shorter than its own itemized costs: inside the
        # 1e-9 s tolerance, so the row still admits.
        within["launch_wall_seconds"] = (
            within["timing"]["warmup_seconds"]
            + within["timing"]["measured_seconds"]
            + sum(within["logger_event_seconds"])
            + sum(within["scorer_event_seconds"])
            + within["publication_io_seconds"]
            - 1e-10
        )
        budget = p67.phase67_budget([within], expected_identities=[identity])
        self.assertGreaterEqual(budget["common_optimizer_steps"], int(RULE["min_steps"]))
        beyond = _cost_row(identity=identity)
        beyond["launch_wall_seconds"] = (
            beyond["timing"]["warmup_seconds"]
            + beyond["timing"]["measured_seconds"]
            + sum(beyond["logger_event_seconds"])
            + sum(beyond["scorer_event_seconds"])
            + beyond["publication_io_seconds"]
            - 1e-6
        )
        with self.assertRaises(ValueError) as raised:
            p67.phase67_budget([beyond], expected_identities=[identity])
        self.assertIn("residual", str(raised.exception))

    def test_a_bad_timing_evidence_digest_refuses(self):
        identity = _identity()
        row = _cost_row(identity=identity, timing_evidence_sha256="not-a-digest")
        with self.assertRaises(ValueError):
            p67.phase67_budget([row], expected_identities=[identity])


class BudgetOutputTests(unittest.TestCase):
    """The output is cost-only, digested and ledgered."""

    def test_the_output_carries_no_score_loss_or_cosine_value(self):
        identities = _three_cases()
        rows = _rows_for(identities)
        for row in rows:
            row["E"] = 0.123456789
            row["loss_final"] = 0.0321
            row["h1_cosine_mean"] = 0.987
            row["tier"] = 0
        budget = p67.phase67_budget(rows, expected_identities=identities)
        rendered = json.dumps(budget, sort_keys=True)
        for secret in ("0.123456789", "0.0321", "0.987"):
            self.assertNotIn(secret, rendered)

    def test_timing_evidence_digests_pass_through(self):
        identities = _three_cases()
        rows = _rows_for(identities)
        digest = "a" * 64
        rows[0]["timing_evidence_sha256"] = digest
        budget = p67.phase67_budget(rows, expected_identities=identities)
        digests = budget["timing_evidence_digests"]
        self.assertEqual(len(digests), 3)
        self.assertEqual(digests[_identity_key(identities[0])], digest)
        for identity in identities[1:]:
            self.assertIsNone(digests[_identity_key(identity)])

    def test_the_ledger_separates_measured_projections_from_cap_reservations(self):
        identities = _three_cases()
        rows = _rows_for(identities)
        budget = p67.phase67_budget(
            rows, expected_identities=identities, unmeasured={"exp05": 12}
        )
        ledger = budget["phase_cost_ledger"]
        self.assertEqual(ledger["cap_seconds"], float(RULE["cap_seconds"]))
        entries = {
            entry["experiment"]: entry for entry in ledger["experiments"]
        }
        self.assertIn("exp02", entries)
        measured = entries["exp02"]
        self.assertEqual(measured["basis"], "measured_projection")
        self.assertEqual(measured["declared_runs"], 3)
        self.assertAlmostEqual(
            measured["planned_seconds"],
            sum(budget["per_row_projection_seconds"].values()),
            places=9,
        )
        self.assertEqual(
            budget["experiment_projected_seconds"]["exp02"],
            measured["planned_seconds"],
        )
        reserved = entries["exp05"]
        self.assertEqual(reserved["basis"], "cap_reservation_unmeasured")
        self.assertEqual(reserved["declared_runs"], 12)
        self.assertEqual(
            reserved["reserved_upper_bound_seconds"],
            12 * float(RULE["cap_seconds"]),
        )
        rendered = json.dumps(reserved, sort_keys=True)
        self.assertIn("no measured timing rows", rendered)
        # The reservation is cap-based, never a borrowed historical rate.
        for field in ("seconds_per_step", "rate", "phase66", "exp01"):
            self.assertNotIn(field, rendered)

    def test_all_arithmetic_is_validated_finite(self):
        identity = _identity()
        row = _cost_row(identity=identity)
        row["timing"]["seconds_per_step"] = 1e308
        with self.assertRaises(ValueError) as raised:
            p67.phase67_budget([row], expected_identities=[identity])
        self.assertIn("finite", str(raised.exception))


if __name__ == "__main__":
    unittest.main()
