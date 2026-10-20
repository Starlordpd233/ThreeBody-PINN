"""Phase 60 (SPEC Requirement 3, GAP-59-13): the shared scorer on MPS float32.

``feasibility_scorer.network_trajectory`` used to widen each chunk with one
``.to(device="cpu", dtype=torch.float64)`` call, which the MPS framework refuses.
These tests prove the three-site fix: a network that lives on the MPS device is
scored end to end, the arrays come back as float64 on the CPU, and a static
guard keeps the one-call widen from returning. ``SuccessorRecordTests`` pins the
committed D-09 successor digest to the scorer file on disk, so a later scorer
edit without a new record fails.

The MPS classes need this Mac's MPS device. A missing device fails the test, so
the proof cannot pass by skipping, unless ``PHASE60_ALLOW_NO_MPS`` is "1".
``PlatformProbeTests`` probes the platform defect itself and runs only when
``PHASE60_PLATFORM_PROBES`` is "1", so a future torch release cannot break the
suite.
"""

from __future__ import annotations

import ast
import hashlib
import json
import os
import unittest
from pathlib import Path

import numpy as np
import torch

from pinn.architecture_spec import ArchitectureSpec
from pinn.constants import T_CHARACTERISTIC_TIME
from pinn.network import build_network
from pinn.physics_residual import componentwise_du
from pinn.verification import feasibility_scorer as scorer
from pinn.verification.feasibility_scorecard import load_scorecard, tier_of
from tests.phase59._fixtures import lagrange_rotation
from tests.phase59.test_scorer_network import _IC13, _MASSES, _TIMES, _closure, _model

ROOT = Path(__file__).resolve().parents[2]
SCORER_PATH = ROOT / "pinn" / "verification" / "feasibility_scorer.py"
SUCCESSOR_RECORD_PATH = (
    ROOT / ".planning" / "phases" / "60-single-system-learnability" / "evidence"
    / "scorer-successor.json"
)
SUCCESSOR_SCHEMA = "phase60-scorer-successor/v1"
SUCCESSOR_KEYS = (
    "schema", "path", "predecessor_sha256", "successor_sha256", "reason", "note",
)
# The scorer's SHA-256 before the GAP-59-13 fix: the digest the committed Phase 59
# results pin as producer_sha256.
PHASE_59_SCORER_SHA256 = "cd5019a2ba5604f39d5c6e01763ff3f0e53547920a57bbf174ebc3bb0a73870b"
ALLOW_NO_MPS_ENV = "PHASE60_ALLOW_NO_MPS"
PLATFORM_PROBES_ENV = "PHASE60_PLATFORM_PROBES"
HELPER_NAME = "_to_cpu_float64"
CPU = torch.device("cpu")
ARRAY_NAMES = ("positions", "velocities", "accelerations")

# Largest allowed difference between the MPS float32 array and the CPU float64
# array of the same weights, as a fraction of the CPU array's largest magnitude.
# This is a float32 test tolerance, not a scorecard value. The first SIREN layer
# runs at frequency 30, so the production network's velocities reach about 480
# and its accelerations about 5e5, and float32 rounding is amplified with them.
# Measured for the seed-7 network over the 41 test times: 4.7e-5 (positions),
# 8.7e-5 (velocities) and 9.5e-5 (accelerations) of the largest magnitude, at
# most 1.6e-4 across seeds 0 to 3. An element-wise rtol 1e-4 / atol 1e-5 check
# leaves 17%, 41% and 42% of the elements outside, so it cannot be used. The
# bound keeps a ten-fold margin and still fails by orders of magnitude if an
# array is swapped, transposed or dropped.
FLOAT32_SCALE_BOUND = 1e-3


def mps_device_or_stop(testcase):
    """The MPS device, proved by allocating on it.

    A machine without a working MPS device fails the test, so the GAP-59-13
    proof never passes by skipping. ``PHASE60_ALLOW_NO_MPS=1`` turns that
    failure into a skip.
    """
    try:
        torch.zeros(1, device="mps")
    except Exception as exc:
        if os.environ.get(ALLOW_NO_MPS_ENV) == "1":
            testcase.skipTest(f"no usable MPS device ({ALLOW_NO_MPS_ENV}=1): {exc}")
        testcase.fail(
            f"this test needs the MPS device (set {ALLOW_NO_MPS_ENV}=1 to skip): {exc}"
        )
    return torch.device("mps")


def _mps_network_with_weights_of(reference, device):
    """A float32 network on ``device`` that carries the reference network's weights."""
    network = build_network(ArchitectureSpec(), dtype=torch.float32, device=device)
    network.load_state_dict(reference.state_dict())
    return network


def _independent_cpu_float64_arrays(model):
    """Positions, velocities and accelerations of a CPU float64 network.

    Computed from the trainer's closure and ``componentwise_du`` without calling
    ``network_trajectory``, so a wiring mistake inside ``network_trajectory``
    cannot hide by appearing on both sides of a comparison.
    """
    model.eval()
    trajectory = _closure(model)
    u = torch.as_tensor(_TIMES / T_CHARACTERISTIC_TIME, dtype=torch.float64, device=CPU)
    positions = torch.func.vmap(lambda s: trajectory(s).reshape(-1))(u)
    velocities, accelerations = componentwise_du(trajectory, u)
    return tuple(
        array.detach().numpy().reshape(-1, 3, 3)
        for array in (positions, velocities, accelerations)
    )


# ---------------------------------------------------------------------------
# Static detectors: pure functions of source text, each with an injected-
# violation self-test below.
# ---------------------------------------------------------------------------

def one_call_widen_lines(source):
    """Lines of ``.to(...)`` calls that pass both a ``device`` and a ``dtype`` keyword."""
    lines = []
    for node in ast.walk(ast.parse(source)):
        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Attribute)
            and node.func.attr == "to"
            and {"device", "dtype"} <= {keyword.arg for keyword in node.keywords}
        ):
            lines.append(node.lineno)
    return sorted(lines)


def module_function(source, name):
    """The module-level ``FunctionDef`` called ``name``, or ``None``."""
    for node in ast.parse(source).body:
        if isinstance(node, ast.FunctionDef) and node.name == name:
            return node
    return None


def helper_call_count(source, function_name, helper_name):
    """Calls to the bare name ``helper_name`` inside the module-level ``function_name``."""
    function = module_function(source, function_name)
    if function is None:
        return 0
    return sum(
        1
        for node in ast.walk(function)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == helper_name
    )


# ---------------------------------------------------------------------------
# MPS behavior.
# ---------------------------------------------------------------------------

class MpsPresenceTests(unittest.TestCase):
    def test_a_tensor_can_be_allocated_on_the_mps_device(self):
        device = mps_device_or_stop(self)
        tensor = torch.zeros(1, device=device)
        self.assertEqual(tensor.device.type, "mps")


class MpsTrajectoryTests(unittest.TestCase):
    def setUp(self):
        self.device = mps_device_or_stop(self)

    def test_arrays_are_float64_on_the_cpu_and_follow_the_cpu_float64_network(self):
        reference = _model()
        expected = _independent_cpu_float64_arrays(reference)
        network = _mps_network_with_weights_of(reference, self.device)
        got = scorer.network_trajectory(
            network, _IC13, _MASSES, _TIMES,
            dtype=torch.float32, device=self.device, want_acceleration=True,
        )
        self.assertEqual(len(got), 3)
        for name, array, truth in zip(ARRAY_NAMES, got, expected):
            with self.subTest(array=name):
                self.assertIsInstance(array, np.ndarray)
                self.assertEqual(array.dtype, np.float64)
                self.assertEqual(array.shape, (len(_TIMES), 3, 3))
                self.assertTrue(np.isfinite(array).all())
                difference = float(np.max(np.abs(array - truth)))
                scale = float(np.max(np.abs(truth)))
                self.assertLessEqual(
                    difference,
                    FLOAT32_SCALE_BOUND * scale,
                    f"{name}: largest difference {difference:.3e} against scale {scale:.3e}",
                )


class MpsScoreTests(unittest.TestCase):
    def setUp(self):
        self.device = mps_device_or_stop(self)

    def test_score_network_returns_a_score_result_for_a_network_on_mps(self):
        network = _mps_network_with_weights_of(_model(), self.device)
        orbit, _velocities, _omega = lagrange_rotation(_TIMES, masses=_MASSES)
        result = scorer.score_network(
            network, _IC13, _MASSES, orbit, (0, 1), _TIMES,
            scorecard=load_scorecard(), dtype=torch.float32, device=self.device, grid="gold",
        )
        self.assertIsInstance(result, scorer.ScoreResult)
        self.assertEqual(result.velocity_source, "autograd")
        self.assertIs(type(result.tier), int)
        self.assertIn(result.tier, range(4))


# ---------------------------------------------------------------------------
# Static guard on the scorer source, with detector self-tests.
# ---------------------------------------------------------------------------

class StaticWidenTests(unittest.TestCase):
    def setUp(self):
        self.source = SCORER_PATH.read_text(encoding="utf-8")

    def test_the_scorer_has_no_one_call_device_and_dtype_widen(self):
        self.assertEqual(one_call_widen_lines(self.source), [])

    def test_the_cpu_then_float64_helper_exists_at_module_level(self):
        self.assertIsNotNone(module_function(self.source, HELPER_NAME))

    def test_network_trajectory_calls_the_helper_at_exactly_three_sites(self):
        self.assertEqual(helper_call_count(self.source, "network_trajectory", HELPER_NAME), 3)

    def test_the_widen_detector_fires_on_the_old_idiom(self):
        old = "def f(x):\n    return x.detach().to(device='cpu', dtype=torch.float64)\n"
        self.assertEqual(one_call_widen_lines(old), [2])
        reordered = "def f(x):\n    return x.to(dtype=torch.float64, device=cpu)\n"
        self.assertEqual(one_call_widen_lines(reordered), [2])

    def test_the_widen_detector_is_quiet_on_two_single_purpose_moves(self):
        safe = (
            "def f(x):\n"
            "    return x.detach().to('cpu').to(torch.float64)\n"
            "def g(x):\n"
            "    return x.to(device=cpu)\n"
            "def h(x):\n"
            "    return x.to(dtype=torch.float64)\n"
        )
        self.assertEqual(one_call_widen_lines(safe), [])

    def test_the_helper_counter_counts_only_named_calls_in_the_named_function(self):
        source = (
            "def _to_cpu_float64(t):\n"
            "    return t\n"
            "def network_trajectory(a, b):\n"
            "    x = _to_cpu_float64(a)\n"
            "    y = _to_cpu_float64(b)\n"
            "    z = other(a)\n"
            "    return x, y, z\n"
            "def elsewhere(a):\n"
            "    return _to_cpu_float64(a)\n"
        )
        self.assertEqual(helper_call_count(source, "network_trajectory", HELPER_NAME), 2)
        self.assertEqual(helper_call_count(source, "missing", HELPER_NAME), 0)
        self.assertIsNone(module_function(source, "missing"))
        nested = "class C:\n    def _to_cpu_float64(self, t):\n        return t\n"
        self.assertIsNone(module_function(nested, HELPER_NAME))


# ---------------------------------------------------------------------------
# The frozen tier rule for a non-finite E (SPEC edge boundary / R2).
# ---------------------------------------------------------------------------

class NonFiniteTierTests(unittest.TestCase):
    def test_a_non_finite_position_error_is_tier_zero(self):
        scorecard = load_scorecard()
        for label, value in (("nan", float("nan")), ("inf", float("inf"))):
            with self.subTest(E=label):
                self.assertEqual(tier_of(value, 0.0, scorecard=scorecard), 0)


# ---------------------------------------------------------------------------
# D-09: the single committed successor digest of the scorer.
# ---------------------------------------------------------------------------

class SuccessorRecordTests(unittest.TestCase):
    """Any later scorer edit without a new owner-visible record fails these."""

    def setUp(self):
        self.record = json.loads(SUCCESSOR_RECORD_PATH.read_text(encoding="utf-8"))

    def test_the_record_has_exactly_the_six_keys_and_the_schema(self):
        self.assertEqual(sorted(self.record), sorted(SUCCESSOR_KEYS))
        self.assertEqual(self.record["schema"], SUCCESSOR_SCHEMA)

    def test_the_record_names_one_path_as_a_string(self):
        self.assertIsInstance(self.record["path"], str)
        self.assertEqual(self.record["path"], SCORER_PATH.relative_to(ROOT).as_posix())

    def test_the_predecessor_is_the_phase_59_digest(self):
        self.assertEqual(self.record["predecessor_sha256"], PHASE_59_SCORER_SHA256)

    def test_the_successor_is_the_digest_of_the_current_scorer(self):
        current = hashlib.sha256(SCORER_PATH.read_bytes()).hexdigest()
        self.assertEqual(self.record["successor_sha256"], current)
        self.assertNotEqual(self.record["successor_sha256"], self.record["predecessor_sha256"])


# ---------------------------------------------------------------------------
# Non-gating platform probe.
# ---------------------------------------------------------------------------

@unittest.skipUnless(
    os.environ.get(PLATFORM_PROBES_ENV) == "1",
    f"platform probe: set {PLATFORM_PROBES_ENV}=1 to run it",
)
class PlatformProbeTests(unittest.TestCase):
    def test_the_old_one_call_widen_of_an_mps_tensor_is_refused_by_the_platform(self):
        device = mps_device_or_stop(self)
        tensor = torch.ones(4, dtype=torch.float32, device=device)
        with self.assertRaises(TypeError):
            tensor.to(device="cpu", dtype=torch.float64)


if __name__ == "__main__":
    unittest.main()
