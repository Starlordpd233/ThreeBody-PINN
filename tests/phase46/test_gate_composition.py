"""Dataset-free INST-01 gate-composition suite (plan 46-03, Tasks 1-2).

Drives ``pinn/training/validation_gate.py`` against the 46-01 stub fixtures and
the REAL ``pinn.verification.gate_metrics`` (composed, never reopened — D-13).
``unittest.mock.patch.object`` on the module's ``gate_metrics`` reference
provides the call-spy and controlled-eps_h assertions. No real run directory or
corpus file is used (D-24); every run dir is a stdlib temp directory.

The production module is present, so every test RUNS — none use the deferred
``_SKIP_PHRASE`` convention.
"""

from __future__ import annotations

import json
import math
import os
import shutil
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import torch

from pinn.constants import T_CHARACTERISTIC_TIME
from pinn.training import validation_gate as vg
from pinn.verification import gate_metrics

from tests.phase46._fixtures import (
    StubModel,
    make_empty_source,
    make_stub_split_sources,
)

SCALED_FRAME = vg.FrameConvention(
    vg.POSITION_FRAME_SCALED, vg.TIME_COORD_NORMALIZED,
    vg.MASS_CONVENTION_ORDERED_RAW, "phase46-test-scaled",
)
RAW_FRAME = vg.FrameConvention(
    vg.POSITION_FRAME_RAW, vg.TIME_COORD_RAW,
    vg.MASS_CONVENTION_ORDERED_RAW, "phase46-test-raw",
)


class _MpsFloat32Model:
    """Callable stub that emits an actual MPS float32 prediction."""

    def __init__(self):
        self.training = True
        self.calls = []

    def eval(self):
        self.training = False
        return self

    def train(self, mode=True):
        self.training = bool(mode)
        return self

    def __call__(self, tau_ic13, masses):
        n = int(tau_ic13.shape[0])
        self.calls.append((tuple(tau_ic13.shape), tuple(masses.shape)))
        return torch.zeros((n, 9), dtype=torch.float32, device=torch.device("mps"))


class _NaNModel:
    """StubModel-shaped callable that emits NaN positions (genuinely non-finite)."""

    def __init__(self):
        self.training = True
        self.calls = []

    def eval(self):
        self.training = False
        return self

    def train(self, mode=True):
        self.training = bool(mode)
        return self

    def __call__(self, tau_ic13, masses):
        n = int(tau_ic13.shape[0])
        self.calls.append(n)
        return torch.full((n, 9), float("nan"), dtype=torch.float64)


def _boom(_model):
    raise RuntimeError("injected mid-pass")


class FrameCoherenceTest(unittest.TestCase):
    def test_incoherent_pairs_rejected_coherent_accepted(self):
        # Both incoherent pairs raise BEFORE any model call.
        with self.assertRaises(vg.IncoherentFrameError):
            vg.FrameConvention(vg.POSITION_FRAME_SCALED, vg.TIME_COORD_RAW,
                               vg.MASS_CONVENTION_ORDERED_RAW, "x")
        with self.assertRaises(vg.IncoherentFrameError):
            vg.FrameConvention(vg.POSITION_FRAME_RAW, vg.TIME_COORD_NORMALIZED,
                               vg.MASS_CONVENTION_ORDERED_RAW, "x")
        # Both coherent pairs construct cleanly.
        vg.FrameConvention(vg.POSITION_FRAME_SCALED, vg.TIME_COORD_NORMALIZED,
                           vg.MASS_CONVENTION_ORDERED_RAW, "scaled")
        vg.FrameConvention(vg.POSITION_FRAME_RAW, vg.TIME_COORD_RAW,
                           vg.MASS_CONVENTION_ORDERED_RAW, "raw")


class GateComputationTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = make_stub_split_sources()[1]  # validation source

    def test_normalized_time_handed_to_gate_under_scaled_frame(self):
        captured = []
        real = gate_metrics.compute_trajectory_gate_metrics

        def spy(positions, times, masses, **kw):
            captured.append(times.detach().clone())
            return real(positions, times, masses, **kw)

        with patch.object(vg.gate_metrics, "compute_trajectory_gate_metrics", side_effect=spy):
            vg.compute_validation_gate(
                StubModel(), self.source, stage=0, global_step=0, frame=SCALED_FRAME
            )
        first_key = sorted(self.source.records_at_or_below(0))[0]
        expected = (
            torch.as_tensor(self.source.snapshot_times(first_key), dtype=torch.float64)
            / float(T_CHARACTERISTIC_TIME)
        )
        self.assertTrue(torch.allclose(captured[0], expected))

    def test_raw_time_handed_to_gate_under_raw_frame(self):
        captured = []
        real = gate_metrics.compute_trajectory_gate_metrics

        def spy(positions, times, masses, **kw):
            captured.append(times.detach().clone())
            return real(positions, times, masses, **kw)

        with patch.object(vg.gate_metrics, "compute_trajectory_gate_metrics", side_effect=spy):
            vg.compute_validation_gate(
                StubModel(), self.source, stage=0, global_step=0, frame=RAW_FRAME
            )
        first_key = sorted(self.source.records_at_or_below(0))[0]
        expected = torch.as_tensor(
            self.source.snapshot_times(first_key), dtype=torch.float64
        )
        self.assertTrue(torch.allclose(captured[0], expected))

    def test_full_pool_sorted_once_per_key(self):
        obs = vg.compute_validation_gate(
            StubModel(), self.source, stage=0, global_step=0, frame=SCALED_FRAME
        )
        pool = sorted(self.source.records_at_or_below(0))
        self.assertEqual([row.record_key for row in obs.rows], pool)
        self.assertEqual(obs.n_trajectories, len(pool))

    def _fake_metrics(self, eps_h):
        def spy(positions, times, masses, **kw):
            return gate_metrics.TrajectoryGateMetrics(
                hamiltonian_series=torch.zeros(int(times.shape[0]), dtype=torch.float64),
                eps_h=eps_h,
            )
        return spy

    def test_aggregate_at_reject_threshold_passes(self):
        with patch.object(vg.gate_metrics, "compute_trajectory_gate_metrics",
                          side_effect=self._fake_metrics(gate_metrics.GATE_EPS_H_REJECT_THRESHOLD)):
            obs = vg.compute_validation_gate(
                StubModel(), self.source, stage=0, global_step=0, frame=SCALED_FRAME
            )
        self.assertEqual(obs.aggregate_eps_h, gate_metrics.GATE_EPS_H_REJECT_THRESHOLD)
        self.assertEqual(obs.verdict, "PASS")

    def test_aggregate_strictly_above_threshold_fails(self):
        above = gate_metrics.GATE_EPS_H_REJECT_THRESHOLD * (1.0 + 1e-6)
        with patch.object(vg.gate_metrics, "compute_trajectory_gate_metrics",
                          side_effect=self._fake_metrics(above)):
            obs = vg.compute_validation_gate(
                StubModel(), self.source, stage=0, global_step=0, frame=SCALED_FRAME
            )
        self.assertGreater(obs.aggregate_eps_h, gate_metrics.GATE_EPS_H_REJECT_THRESHOLD)
        self.assertEqual(obs.verdict, "FAIL")

    def test_non_finite_retained_counted_and_fails(self):
        obs = vg.compute_validation_gate(
            _NaNModel(), self.source, stage=0, global_step=0, frame=SCALED_FRAME
        )
        self.assertEqual(obs.n_nonfinite, obs.n_trajectories)
        self.assertTrue(all(math.isnan(row.eps_h) for row in obs.rows))
        self.assertEqual(obs.verdict, "FAIL")

    def test_empty_pool_raises_unavailable(self):
        with self.assertRaises(vg.ValidationGateUnavailable):
            vg.compute_validation_gate(
                StubModel(), make_empty_source(), stage=0, global_step=0, frame=SCALED_FRAME
            )

    def test_prior_train_mode_restored(self):
        model = StubModel()
        model.train()
        self.assertTrue(model.training)
        vg.compute_validation_gate(
            model, self.source, stage=0, global_step=0, frame=SCALED_FRAME
        )
        self.assertTrue(model.training)

    def test_prior_eval_mode_restored(self):
        model = StubModel()
        model.eval()
        self.assertFalse(model.training)
        vg.compute_validation_gate(
            model, self.source, stage=0, global_step=0, frame=SCALED_FRAME
        )
        self.assertFalse(model.training)

    def test_mode_restored_even_when_forward_raises(self):
        model = StubModel(fail_hook=_boom)
        model.train()
        with self.assertRaises(RuntimeError):
            vg.compute_validation_gate(
                model, self.source, stage=0, global_step=0, frame=SCALED_FRAME
            )
        self.assertTrue(model.training)  # prior mode restored despite the exception


class MpsPredictionNormalizationTest(unittest.TestCase):
    """Target-host MPS conversion contract (Phase 50 plan 50-06 Task 1)."""

    @classmethod
    def setUpClass(cls):
        if not torch.backends.mps.is_available():
            raise AssertionError("canonical MPS host required")
        cls.source = make_stub_split_sources()[1]

    def test_mps_float32_prediction_is_detached_cpu_then_float64_before_metric(self):
        captured = []
        real = gate_metrics.compute_trajectory_gate_metrics

        def spy(positions, times, masses, **kw):
            captured.append(
                {
                    "positions": positions,
                    "times": times,
                    "masses": masses,
                }
            )
            return real(positions, times, masses, **kw)

        model = _MpsFloat32Model()
        model.train()
        with patch.object(
            vg.gate_metrics, "compute_trajectory_gate_metrics", side_effect=spy
        ):
            obs = vg.compute_validation_gate(
                model,
                self.source,
                stage=0,
                global_step=0,
                frame=vg.RATIFIED_VALIDATION_FRAME,
                dtype=torch.float32,
                device=torch.device("mps"),
            )
        self.assertTrue(model.training)
        pool = sorted(self.source.records_at_or_below(0))
        self.assertEqual([row.record_key for row in obs.rows], pool)
        self.assertEqual(len(captured), len(pool))
        self.assertEqual(obs.n_trajectories, len(pool))
        first_key = pool[0]
        expected_t = int(self.source.n_snapshots(first_key))
        positions = captured[0]["positions"]
        times = captured[0]["times"]
        masses = captured[0]["masses"]
        self.assertEqual(positions.device.type, "cpu")
        self.assertEqual(positions.dtype, torch.float64)
        self.assertFalse(positions.requires_grad)
        self.assertEqual(tuple(positions.shape), (expected_t, 3, 3))
        self.assertEqual(times.device.type, "cpu")
        self.assertEqual(times.dtype, torch.float64)
        self.assertFalse(times.requires_grad)
        self.assertEqual(tuple(times.shape), (expected_t,))
        self.assertEqual(masses.device.type, "cpu")
        self.assertEqual(masses.dtype, torch.float64)
        self.assertFalse(masses.requires_grad)
        self.assertEqual(tuple(masses.shape), (3,))


class SidecarTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.source = make_stub_split_sources()[1]
        self.obs = vg.compute_validation_gate(
            StubModel(), self.source, stage=0, global_step=42, frame=SCALED_FRAME
        )

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_publish_roundtrip_deterministic_and_valid(self):
        d1 = Path(self.tmp) / "site1" / "run"
        d2 = Path(self.tmp) / "site2" / "run"  # same basename -> identical payload
        d1.mkdir(parents=True)
        d2.mkdir(parents=True)
        rel1 = vg.publish_gate_sidecar(d1, self.obs)
        rel2 = vg.publish_gate_sidecar(d2, self.obs)
        self.assertEqual(rel1, rel2)
        self.assertEqual((d1 / rel1).read_bytes(), (d2 / rel2).read_bytes())
        payload = json.loads((d1 / rel1).read_text())
        vg.validate_sidecar_payload(payload)  # no raise
        # D-18 fields: frame + conf01_evidence_ref, both thresholds, sorted triples.
        self.assertIn("conf01_evidence_ref", payload["frame"])
        self.assertEqual(payload["eps_h_reject_threshold"], gate_metrics.GATE_EPS_H_REJECT_THRESHOLD)
        self.assertEqual(payload["scs_reject_threshold"], gate_metrics.GATE_SCS_REJECT_THRESHOLD)
        self.assertEqual(payload["global_step"], 42)

    def test_non_finite_serializes_as_string_sentinel(self):
        nan_obs = vg.compute_validation_gate(
            _NaNModel(), self.source, stage=0, global_step=7, frame=SCALED_FRAME
        )
        run = Path(self.tmp) / "run2"
        run.mkdir()
        rel = vg.publish_gate_sidecar(run, nan_obs)
        text = (run / rel).read_text()
        self.assertNotIn("null", text)  # no null-collapsing anywhere
        payload = json.loads(text)
        self.assertEqual(payload["aggregate_eps_h"], "NaN")
        self.assertTrue(all(row["eps_h"] == "NaN" for row in payload["rows"]))
        self.assertEqual(payload["verdict"], "FAIL")

    def test_sidecar_path_is_run_relative_and_contained(self):
        self.assertEqual(vg.sidecar_relative_path(0), "validation_gate/step-00000000.json")
        rel = vg.sidecar_relative_path(12345)
        self.assertFalse(os.path.isabs(rel))
        self.assertNotIn("..", rel)
        run = Path(self.tmp) / "run3"
        run.mkdir()
        published = vg.publish_gate_sidecar(run, self.obs)
        base = run.resolve()
        dest = (run / published).resolve()
        self.assertEqual(dest.relative_to(base).as_posix(), published)

    def test_compact_returns_fields_when_sidecar_valid(self):
        run = Path(self.tmp) / "run4"
        run.mkdir()
        vg.publish_gate_sidecar(run, self.obs)
        fields = vg.compact_validation_fields(self.obs, run)
        self.assertEqual(
            set(fields),
            {"gate_schema_version", "gate_eps_h", "gate_scs", "gate_verdict",
             "gate_status", "gate_n_trajectories", "gate_n_nonfinite", "gate_sidecar"},
        )
        self.assertEqual(fields["gate_verdict"], self.obs.verdict)
        self.assertEqual(fields["gate_sidecar"], vg.sidecar_relative_path(42))

    def test_compact_raises_when_sidecar_absent(self):
        run = Path(self.tmp) / "run5"
        run.mkdir()  # nothing published
        with self.assertRaises(vg.ValidationGateUnavailable):
            vg.compact_validation_fields(self.obs, run)

    def test_compact_raises_when_sidecar_truncated(self):
        run = Path(self.tmp) / "run6"
        run.mkdir()
        rel = vg.publish_gate_sidecar(run, self.obs)
        path = run / rel
        path.write_text(path.read_text()[:20])  # truncation -> invalid JSON
        with self.assertRaises(vg.ValidationGateUnavailable):
            vg.compact_validation_fields(self.obs, run)

    def test_compact_raises_when_sidecar_schema_invalid(self):
        run = Path(self.tmp) / "run7"
        run.mkdir()
        rel = vg.publish_gate_sidecar(run, self.obs)
        payload = json.loads((run / rel).read_text())
        payload["schema_version"] = "bogus"
        (run / rel).write_text(json.dumps(payload))
        with self.assertRaises(vg.ValidationGateUnavailable):
            vg.compact_validation_fields(self.obs, run)

    def test_validate_sidecar_payload_is_fail_closed(self):
        run = Path(self.tmp) / "run8"
        run.mkdir()
        rel = vg.publish_gate_sidecar(run, self.obs)
        base = json.loads((run / rel).read_text())

        def expect_value_error(mutated):
            with self.assertRaises(ValueError):
                vg.validate_sidecar_payload(mutated)

        bad = json.loads(json.dumps(base))
        bad["schema_version"] = "wrong"
        expect_value_error(bad)

        bad = json.loads(json.dumps(base))
        del bad["verdict"]
        expect_value_error(bad)

        bad = json.loads(json.dumps(base))
        bad["rows"] = list(reversed(bad["rows"]))
        expect_value_error(bad)

        bad = json.loads(json.dumps(base))
        del bad["rows"][0]["record_key"]
        expect_value_error(bad)

        # The unmutated payload passes.
        vg.validate_sidecar_payload(base)


if __name__ == "__main__":
    unittest.main()
