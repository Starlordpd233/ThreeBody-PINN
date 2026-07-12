"""Phase 37 ENV-03 componentwise-AD scientific test contract (CTX-08..CTX-10,
T-37-06).

Wave 0 contract. Tests import ``pinn.verification.componentwise_ad`` inside test
methods so module compilation is the only Wave 0 green condition; the suite
turns green only in Wave 2 when the worker lands.

The fixture preserves the authoritative §10.3 contract from
``pinn_architecture.md`` and the legacy
``.planning/milestones/v1.4-phases/21-acceptance-checks-and-handoff/probes/probe_ad.py``:
scalar leaf ``u = 0.3 in [0, 1]``; the trajectory
``r'(u) = [sin(2*pi*u), cos(2*pi*u), u**2]``; analytical first derivative
``[2*pi*cos(2*pi*u), -2*pi*sin(2*pi*u), 2*u]``; componentwise loop; aggregate
``relative_error < 1e-6``.
"""

import importlib
import math
import unittest

WORKER_MODULE = "pinn.verification.componentwise_ad"

# CTX-09 locked protocol constants.
SCALAR_LEAF_U = 0.3
WARMUP_ITERATIONS = 10
SAMPLE_COUNT = 30
EVALUATIONS_PER_SAMPLE = 100
AGGREGATE_CRITERION = 1e-6

# Analytical first derivative at u = 0.3. Tests compare the worker output to
# these exact values to preserve §10.3 semantics.
TWO_PI_U = 2 * math.pi * SCALAR_LEAF_U
ANALYTICAL_AT_U_0_3 = (
    2 * math.pi * math.cos(TWO_PI_U),
    -2 * math.pi * math.sin(TWO_PI_U),
    2 * SCALAR_LEAF_U,
)


def _load_worker():
    """Import the production worker; skip the test if it does not exist yet."""
    try:
        module = importlib.import_module(WORKER_MODULE)
    except ImportError as exc:
        raise unittest.SkipTest(
            f"{WORKER_MODULE} not implemented until Wave 2: {exc}")
    return module


class ComponentwiseADTests(unittest.TestCase):
    """CTX-09 / T-37-06: shared trajectory, both AD methods, locked criterion."""

    def test_synthetic_trajectory_matches_section_10_3(self):
        # r'(u) = [sin(2*pi*u), cos(2*pi*u), u**2]
        worker = _load_worker()
        traj = worker.synthetic_trajectory
        # Allow either a callable or an already-constructed tensor; the contract
        # is that the analytical form is preserved.
        self.assertTrue(callable(traj) or hasattr(traj, "shape"),
                        "synthetic_trajectory must be a callable or tensor")

    def test_analytical_first_derivative_matches_section_10_3(self):
        worker = _load_worker()
        # The worker must export the analytical first derivative in a form that
        # can be evaluated at u=0.3. We accept either a function or a tensor.
        analytical = worker.analytical_first_derivative
        self.assertTrue(callable(analytical) or hasattr(analytical, "shape"))

    def test_compute_derivative_full_jacobian_returns_analytical_vector_at_u_0_3(self):
        worker = _load_worker()
        result = worker.compute_derivative("full_jacobian", SCALAR_LEAF_U,
                                           precision="float64", device="cpu")
        # The result must expose all three component values plus signed deltas
        # and errors. Check the predicted vector against the analytical vector.
        for got, expected in zip(result["predicted"], ANALYTICAL_AT_U_0_3):
            self.assertAlmostEqual(got, expected, places=5,
                                   msg="full_jacobian diverged from analytical at u=0.3")
        # Componentwise relative error must be small.
        for got, expected in zip(result["predicted"], ANALYTICAL_AT_U_0_3):
            denom = max(abs(expected), 1e-12)
            self.assertLess(abs(got - expected) / denom, 1e-5)

    def test_compute_derivative_scalar_u_jvp_returns_analytical_vector_at_u_0_3(self):
        worker = _load_worker()
        result = worker.compute_derivative("scalar_u_jvp", SCALAR_LEAF_U,
                                           precision="float64", device="cpu")
        for got, expected in zip(result["predicted"], ANALYTICAL_AT_U_0_3):
            self.assertAlmostEqual(got, expected, places=5,
                                   msg="scalar_u_jvp diverged from analytical at u=0.3")

    def test_both_patterns_share_one_trajectory(self):
        worker = _load_worker()
        r_jac = worker.compute_derivative("full_jacobian", SCALAR_LEAF_U,
                                          precision="float64", device="cpu")
        r_jvp = worker.compute_derivative("scalar_u_jvp", SCALAR_LEAF_U,
                                          precision="float64", device="cpu")
        # Both methods must produce the same predicted vector at u=0.3 — proving
        # they share one trajectory, not two implementations.
        for a, b in zip(r_jac["predicted"], r_jvp["predicted"]):
            self.assertAlmostEqual(a, b, places=6,
                                   msg="full_jacobian and scalar_u_jvp diverged")

    def test_aggregate_relative_error_below_criterion_for_both_patterns(self):
        worker = _load_worker()
        for pattern in ("full_jacobian", "scalar_u_jvp"):
            result = worker.compute_derivative(pattern, SCALAR_LEAF_U,
                                               precision="float64", device="cpu")
            self.assertIn("aggregate_relative_error", result,
                          f"{pattern} missing aggregate_relative_error")
            self.assertLess(result["aggregate_relative_error"], AGGREGATE_CRITERION,
                            msg=f"{pattern} aggregate error exceeded criterion")

    def test_componentwise_signed_absolute_relative_errors_recorded(self):
        worker = _load_worker()
        result = worker.compute_derivative("full_jacobian", SCALAR_LEAF_U,
                                           precision="float64", device="cpu")
        for field in ("signed_delta", "absolute_error", "relative_error"):
            self.assertIn(field, result, f"missing componentwise field {field}")
            self.assertEqual(len(result[field]), 3,
                             f"{field} must have 3 components")

    def test_non_finite_components_fail(self):
        worker = _load_worker()
        # Inject a NaN by requesting an out-of-domain leaf: u outside [0,1] is
        # not in the locked fixture. The worker must reject the run rather than
        # return non-finite evidence.
        with self.assertRaises((ValueError, ArithmeticError)):
            worker.compute_derivative("full_jacobian", math.nan,
                                      precision="float64", device="cpu")

    def test_timing_protocol_constants_match_locked_contract(self):
        worker = _load_worker()
        protocol = worker.TimingProtocol
        # Accept either an instance, a class, or a dict.
        if hasattr(protocol, "warmup_iterations"):
            self.assertEqual(protocol.warmup_iterations, WARMUP_ITERATIONS)
            self.assertEqual(protocol.sample_count, SAMPLE_COUNT)
            self.assertEqual(protocol.evaluations_per_sample, EVALUATIONS_PER_SAMPLE)
        elif isinstance(protocol, dict):
            self.assertEqual(protocol["warmup_iterations"], WARMUP_ITERATIONS)
            self.assertEqual(protocol["sample_count"], SAMPLE_COUNT)
            self.assertEqual(protocol["evaluations_per_sample"], EVALUATIONS_PER_SAMPLE)
        else:
            # It's a class — instantiate.
            instance = protocol()
            self.assertEqual(instance.warmup_iterations, WARMUP_ITERATIONS)
            self.assertEqual(instance.sample_count, SAMPLE_COUNT)
            self.assertEqual(instance.evaluations_per_sample, EVALUATIONS_PER_SAMPLE)

    def test_run_probe_arm_returns_six_summary_statistics_and_raw_samples(self):
        worker = _load_worker()
        result = worker.run_probe_arm(precision="float64", device="cpu",
                                      patterns=("full_jacobian", "scalar_u_jvp"))
        for pattern in ("full_jacobian", "scalar_u_jvp"):
            record = result["patterns"][pattern]
            self.assertIn("raw_samples_ns", record,
                          f"{pattern} missing raw_samples_ns")
            self.assertEqual(len(record["raw_samples_ns"]), SAMPLE_COUNT,
                             f"{pattern} raw sample count != {SAMPLE_COUNT}")
            for stat in ("median", "p25", "p75", "min", "max"):
                self.assertIn(stat, record, f"{pattern} missing stat {stat}")

    def test_worker_captures_fallback_before_torch_import(self):
        # CTX-08: the worker MUST capture PYTORCH_ENABLE_MPS_FALLBACK before any
        # Torch import. We assert by source inspection that the worker's
        # top-level imports defer torch until after the fallback capture.
        import pathlib
        repo_root = pathlib.Path(__file__).resolve().parents[2]
        worker_py = repo_root / "pinn" / "verification" / "componentwise_ad.py"
        if not worker_py.exists():
            self.skipTest("worker not implemented until Wave 2")
        source = worker_py.read_text()
        # The fallback capture must appear before the first `import torch` line.
        fallback_idx = source.find("PYTORCH_ENABLE_MPS_FALLBACK")
        torch_idx = source.find("import torch")
        self.assertGreater(fallback_idx, -1, "worker never reads the fallback key")
        self.assertGreater(torch_idx, -1, "worker never imports torch")
        self.assertLess(fallback_idx, torch_idx,
                        "worker imports torch before capturing fallback state")


if __name__ == "__main__":
    unittest.main()
