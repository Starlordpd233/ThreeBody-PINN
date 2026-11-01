"""Plan 66-02 (EXP-01): the time-bound budget, cadence and design block.

One test per behavior bullet of task 66-02-03, on synthetic timing records
only: :class:`Phase66BudgetTests` pins the bounded similarity cadence (at most
14 entries), the ceil-to-10,000 loss-trace stride and its Site F trace-length
equivalence, the launch-wall margin, the budget whose N is set by time alone
(the 0.75-of-cap bound with the 25 percent rate margin, maximality at the step
quantum, the N-independent record-size ceiling guard, the fast-rate case, and
every refusal), and the frozen JSON-normal design block. The budget CLI test
proves the timing directory's score never reaches the output.
"""

from __future__ import annotations

import contextlib
import hashlib
import io
import json
import tempfile
import unittest
from pathlib import Path

from pinn.verification import diagnostic_phase66 as p66

#: The timing run's registered cadence (BUDGET_RULE.timing_cadence).
TIMING_CADENCE = [0, 1300, 2600, 3900, 5200]


def _timing_record(**overrides):
    """A synthetic 5,200-step timing record in the smoke record's shape."""
    entries = [
        {
            "step": step,
            "layers": [
                {"name": "input", "order": 0, "adjacent_cosine_mean": 0.99},
                {"name": "h1", "order": 1, "adjacent_cosine_mean": 0.98},
            ],
            "first_layer_frequency": {"median": 12.0, "max": 22.73},
            "output_movement": {"value": 0.6},
            "tau_values": [0.001 * index for index in range(64)],
        }
        for step in TIMING_CADENCE
    ]
    record = {
        "status": "complete",
        "run_id": "exp01-d1-w384-o1000-1632",
        "steps": {
            "requested": 5200, "warmup": 200, "measured": 5000, "completed": 5200,
        },
        "similarity": {"cadence": list(TIMING_CADENCE), "entries": entries},
        "loss": {"final": 0.0321, "trace": [0.0321] * 5200},
        "timing": {
            "seconds_per_step": 0.004,
            "warmup_seconds": 0.2,
            "measured_seconds": 20.0,
            "phases": {"logging_seconds": 2.5, "scoring_seconds": 1.0},
        },
        "scores": {"network": {"E": 0.123456789, "tier": 0}},
    }
    record.update(overrides)
    return record


class Phase66BudgetTests(unittest.TestCase):
    """The bounded cadence, the time-only budget and the frozen design."""

    def test_the_cadence_matches_the_registered_schedule(self):
        self.assertEqual(
            p66.exp01_cadence(268000),
            [0, 100, 300, 1000, 3000, 10000, 30000, 100000,
             128000, 156000, 184000, 212000, 240000, 268000],
        )
        self.assertEqual(
            p66.exp01_cadence(637000),
            [0, 100, 300, 1000, 3000, 10000, 30000, 100000,
             189500, 279000, 368500, 458000, 547500, 637000],
        )
        self.assertEqual(
            p66.exp01_cadence(100000),
            [0, 100, 300, 1000, 3000, 10000, 30000, 100000],
        )
        self.assertEqual(
            p66.exp01_cadence(50000),
            [0, 100, 300, 1000, 3000, 10000, 30000, 50000],
        )
        self.assertEqual(p66.exp01_cadence(100), [0, 100])
        for n in (5000, 50000, 268000, 637000, 5000000, 20000000):
            with self.subTest(n=n):
                cadence = p66.exp01_cadence(n)
                self.assertEqual(cadence, sorted(set(cadence)))
                self.assertEqual(cadence[0], 0)
                self.assertEqual(cadence[-1], n)
                self.assertLessEqual(len(cadence), 14)

    def test_the_loss_trace_stride_is_ceil_n_over_10000(self):
        self.assertEqual(p66.exp01_loss_trace_stride(5200), 1)
        self.assertEqual(p66.exp01_loss_trace_stride(10000), 1)
        self.assertEqual(p66.exp01_loss_trace_stride(10001), 2)
        self.assertEqual(p66.exp01_loss_trace_stride(637000), 64)
        self.assertEqual(p66.exp01_loss_trace_stride(5000000), 500)

    def test_loss_trace_entries_matches_the_site_f_trace_length(self):
        self.assertEqual(p66.loss_trace_entries(5200, 1), 5200)
        self.assertEqual(p66.loss_trace_entries(10001, 2), 5001)
        for n, stride in ((20, 3), (5200, 1), (10001, 2), (637000, 64)):
            with self.subTest(n=n, stride=stride):
                losses = list(range(1, n + 1))
                trace = losses[stride - 1::stride]
                if len(losses) % stride:
                    trace = trace + [losses[-1]]
                self.assertEqual(len(trace), p66.loss_trace_entries(n, stride))
        # The rule's stride never exceeds the 10,001-entry record bound at any
        # n: the small range in full, the k*10000 boundary families to 20M,
        # and the extremes.
        for n in range(1, 20002):
            self.assertLessEqual(
                p66.loss_trace_entries(n, p66.exp01_loss_trace_stride(n)), 10001,
                f"n={n}",
            )
        for k in range(1, 2001):
            for n in (k * 10000 - 1, k * 10000, k * 10000 + 1):
                self.assertLessEqual(
                    p66.loss_trace_entries(n, p66.exp01_loss_trace_stride(n)),
                    10001, f"n={n}",
                )
        for n in (5000000, 20000000):
            self.assertLessEqual(
                p66.loss_trace_entries(n, p66.exp01_loss_trace_stride(n)), 10001
            )

    def test_launch_wall_seconds_adds_the_resolution_margin(self):
        receipt = {"checked_utc": "2026-10-31T14:59:00+00:00"}
        attempt = {"ended_utc": "2026-10-31T15:30:00+00:00"}
        self.assertEqual(p66.launch_wall_seconds(receipt, attempt), 1862.0)
        with self.assertRaises(ValueError):
            p66.launch_wall_seconds({}, attempt)
        with self.assertRaises(ValueError):
            p66.launch_wall_seconds(receipt, {})
        with self.assertRaises(ValueError):
            p66.launch_wall_seconds(
                {"checked_utc": "2026-10-31T14:59:00+00:00"},
                {"ended_utc": "2026-10-31T14:58:00+00:00"},
            )

    def test_the_budget_sets_the_step_count_by_time_alone(self):
        record = _timing_record()
        budget = p66.exp01_budget(
            record, record_bytes=400000, launch_wall_seconds=60.0
        )
        n = budget["optimizer_steps"]
        self.assertEqual(n % 1000, 0)
        self.assertGreater(n, 200)
        self.assertEqual(budget["warmup_steps"], 200)
        self.assertEqual(budget["measured_steps"], n - 200)
        self.assertEqual(budget["similarity_cadence"], p66.exp01_cadence(n))
        self.assertEqual(
            budget["loss_trace_stride"], p66.exp01_loss_trace_stride(n)
        )
        self.assertEqual(budget["whole_run_cap_seconds"], 3300.0)
        # Maximality: the bound holds at N, and the remaining headroom is
        # smaller than one more quantum's measured cost (at least
        # 1000 * s_m * (1 + margin), before the cadence term), so N + the
        # quantum exceeds the bound.
        limit = 0.75 * 3300.0
        self.assertLessEqual(budget["projected_wall_seconds"], limit)
        self.assertLess(
            limit - budget["projected_wall_seconds"],
            0.004 * 1.25 * 1000,
        )
        # The record stays committable, the ceiling is reported, and no score,
        # similarity value or loss value is present.
        self.assertLess(budget["projected_record_bytes"], 0.9 * 10485760)
        self.assertLessEqual(budget["record_bytes_ceiling"], 0.9 * 10485760)
        self.assertEqual(budget["size_limit_bytes"], 10485760)
        self.assertEqual(
            budget["limit_source"], "scripts/git_policy/validate_staged_paths.py"
        )
        self.assertEqual(budget["inputs"]["seconds_per_step"], 0.004)
        self.assertEqual(budget["inputs"]["record_bytes"], 400000)
        self.assertEqual(budget["inputs"]["launch_wall_seconds"], 60.0)
        rendered = json.dumps(budget)
        for secret in ("0.123456789", "0.0321", "0.6"):
            self.assertNotIn(secret, rendered)

    def test_a_fast_rate_still_returns_the_time_bound(self):
        fast = _timing_record()
        fast["timing"]["seconds_per_step"] = 0.0002
        budget = p66.exp01_budget(
            fast, record_bytes=400000, launch_wall_seconds=60.0
        )
        self.assertGreater(budget["optimizer_steps"], 1000000)
        self.assertLess(budget["projected_record_bytes"], 0.9 * 10485760)
        # The run length depends on time alone: a bigger existing record does
        # not change N.
        bigger = p66.exp01_budget(
            fast, record_bytes=400000 + 1048576, launch_wall_seconds=60.0
        )
        self.assertEqual(bigger["optimizer_steps"], budget["optimizer_steps"])

    def test_the_budget_refuses_broken_inputs(self):
        incomplete = _timing_record(status="incomplete")
        with self.assertRaises(ValueError):
            p66.exp01_budget(incomplete, record_bytes=1, launch_wall_seconds=60.0)
        missing_field = _timing_record()
        del missing_field["timing"]["seconds_per_step"]
        with self.assertRaises(ValueError):
            p66.exp01_budget(missing_field, record_bytes=1, launch_wall_seconds=60.0)
        stopped = _timing_record()
        stopped["timing"]["seconds_per_step"] = 0.0
        with self.assertRaises(ValueError):
            p66.exp01_budget(stopped, record_bytes=1, launch_wall_seconds=60.0)
        negative_fixed = _timing_record()
        with self.assertRaises(ValueError):
            p66.exp01_budget(negative_fixed, record_bytes=1, launch_wall_seconds=1.0)
        infeasible = _timing_record()
        infeasible["timing"]["seconds_per_step"] = 10.0
        with self.assertRaises(ValueError):
            p66.exp01_budget(infeasible, record_bytes=1, launch_wall_seconds=60.0)
        absurd = _timing_record()
        absurd["similarity"]["entries"] = [
            {
                "step": step,
                "output_movement": {"value": 0.6},
                "tau_values": [0.001 * index for index in range(60000)],
            }
            for step in TIMING_CADENCE
        ]
        with self.assertRaises(ValueError):
            p66.exp01_budget(absurd, record_bytes=1, launch_wall_seconds=60.0)

    def test_the_design_block_is_the_frozen_json_normal_dict(self):
        design = p66.exp01_design()
        self.assertEqual(
            set(design),
            {
                "experiment", "variant", "variant_registry", "parameters",
                "locked_12_parameters", "first_layer_inputs",
                "first_layer_frequency_bound", "runtime", "optimizer", "loss",
                "physical_window", "runs", "reading_rule", "budget_rule",
            },
        )
        self.assertEqual(design["experiment"], "EXP-01")
        self.assertEqual(design["variant"], p66.EXP01_VARIANT.to_json_dict())
        self.assertEqual(design["variant_registry"], "phase66")
        self.assertEqual(design["parameters"], 157065)
        self.assertEqual(design["locked_12_parameters"], 795657)
        self.assertEqual(design["first_layer_inputs"], 14)
        self.assertEqual(
            design["first_layer_frequency_bound"],
            p66.first_layer_frequency_bound(1000.0),
        )
        self.assertEqual(design["runtime"], {"dtype": "float32", "device": "mps"})
        self.assertEqual(
            design["optimizer"], {"kind": "adam_constant_rate", "lr": 0.0001}
        )
        self.assertEqual(design["loss"], "data_only")
        self.assertEqual(design["physical_window"], [0.0, 10.0])
        self.assertEqual(design["runs"], [dict(spec) for spec in p66.EXP01_RUNS])
        reading = design["reading_rule"]
        self.assertEqual(reading["improvement"], dict(p66.IMPROVEMENT_RULE))
        self.assertEqual(reading["near_band"], p66.NEAR_BAND)
        self.assertEqual(
            reading["routes"],
            {
                "confirmed tier1": "phase67-as-planned",
                "confirmed near": "propose-66.1",
                "otherwise": "owner",
            },
        )
        budget_rule = design["budget_rule"]
        expected_rule = dict(p66.BUDGET_RULE)
        # The design block is JSON-normal: the rule's cadence sequences are
        # lists, never tuples.
        expected_rule["cadence_head"] = list(p66.BUDGET_RULE["cadence_head"])
        expected_rule["timing_cadence"] = list(p66.BUDGET_RULE["timing_cadence"])
        self.assertEqual(budget_rule, expected_rule)
        self.assertEqual(budget_rule["size_limit_bytes"], 10485760)
        self.assertEqual(budget_rule["loss_trace_entries_max"], 10000)
        self.assertEqual(budget_rule["cadence_tail_entries"], 6)
        self.assertNotIn("cadence_stride", budget_rule)
        self.assertEqual(reading["improvement"]["min_growth"], 0.01)
        # JSON-normal and stable: every sequence is a list, every key a string.
        self.assertEqual(json.loads(json.dumps(design)), design)
        first = json.dumps(design, indent=2, sort_keys=True)
        second = json.dumps(p66.exp01_design(), indent=2, sort_keys=True)
        self.assertEqual(first, second)

    def test_the_budget_cli_reports_the_time_bound_without_scores(self):
        tmp = Path(self.enterContext(
            tempfile.TemporaryDirectory(prefix="phase66-budget-")
        ))
        record = _timing_record()
        raw = json.dumps(record, indent=2, sort_keys=True).encode("utf-8") + b"\n"
        directory = tmp / "timing"
        directory.mkdir(parents=True)
        (directory / "record.json").write_bytes(raw)
        attempt = {
            "schema": "phase65-fit-attempt/v1", "status": "published",
            "pid": 1, "started_utc": "2026-10-31T15:00:00+00:00",
            "ended_utc": "2026-10-31T15:00:58+00:00",
            "record_sha256": hashlib.sha256(raw).hexdigest(),
        }
        receipt = {
            "schema": "phase66-power-gate/v1",
            "checked_utc": "2026-10-31T15:00:00+00:00",
            "power_source": "AC Power",
            "window": {"timezone": "America/Chicago",
                       "local_time": "2026-10-31T10:00:00-05:00",
                       "isoweekday": 6},
        }
        (directory / "attempt.json").write_bytes(
            json.dumps(attempt, indent=2, sort_keys=True).encode("utf-8") + b"\n"
        )
        (directory / "power-gate.json").write_bytes(
            json.dumps(receipt, indent=2, sort_keys=True).encode("utf-8") + b"\n"
        )
        stdout = io.StringIO()
        stderr = io.StringIO()
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            code = p66.main(["budget", "--timing-dir", str(directory)])
        self.assertEqual(code, 0)
        combined = stdout.getvalue() + stderr.getvalue()
        self.assertIn("EXP01-BUDGET steps=", combined)
        self.assertIn("loss_trace_stride=", combined)
        self.assertIn("cap=3300.0", combined)
        payload = json.loads(stdout.getvalue().split("EXP01-BUDGET")[0])
        self.assertEqual(payload["optimizer_steps"] % 1000, 0)
        self.assertLess(payload["projected_record_bytes"], 0.9 * 10485760)
        for secret in ("0.123456789", "0.0321", "0.6"):
            self.assertNotIn(secret, combined)


if __name__ == "__main__":
    unittest.main()
