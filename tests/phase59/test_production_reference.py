"""Phase 59 production-reference contracts on a synthetic corpus only."""

from __future__ import annotations

import unittest

import numpy as np
import torch

from pinn.data.adapter import (
    BRUTUS_FOLDER_TABLE,
    BRUTUS_SUBDIR,
    load_blacklist_file,
    measure_dt_out,
    parse_brutus_file,
    parse_footer,
    to_parsed_trajectory,
)
from pinn.data.admission import evaluate_admission
from pinn.data.preprocessing import (
    NormalizationStats,
    build_raw_ic13,
    compute_invariants,
    normalize_ic13,
    preprocess_trajectory,
)
from pinn.data.splits import StageIndex
from pinn.data.types import RecordKey
from pinn.loss_catalog import _matched_plummer_components
from pinn.verification.split_allowlist import NotAdmitted
from tests.phase46._fixtures import make_com_offset_trajectory
from tests.phase59._corpus_fixtures import tiny_split_fixture
from tests.phase59.test_split_allowlist import _reader


def _production():
    try:
        import pinn.verification.production_reference as module
    except ImportError as exc:
        if getattr(exc, "name", None) == "pinn.verification.production_reference":
            return None
        raise
    return module


def _brutus_path(data_root, key):
    folder = next(
        name for name, pair in BRUTUS_FOLDER_TABLE.items()
        if pair == (key.variant, key.fidelity)
    )
    return data_root / BRUTUS_SUBDIR / folder / f"brutus_{key.variant}_{key.id:04d}.txt"


def _acceleration_magnitudes(times, velocities):
    """Test-local transcription of adapter.py:1071-1086."""
    n = int(times.shape[0])
    acceleration = torch.empty_like(velocities)
    acceleration[0] = (velocities[1] - velocities[0]) / (times[1] - times[0])
    acceleration[-1] = (velocities[-1] - velocities[-2]) / (times[-1] - times[-2])
    if n > 2:
        denominator = (times[2:] - times[:-2]).reshape(-1, 1, 1)
        acceleration[1:-1] = (velocities[2:] - velocities[:-2]) / denominator
    return torch.linalg.vector_norm(acceleration.reshape(n, -1), dim=1)


def _cast(array):
    return torch.tensor(np.asarray(array, dtype=np.float64), dtype=torch.float32)


def _seam_oracle(path, key, data_root, blacklist, stats):
    """Per-file adapter seams in adapter.py:814-860 order, then the fp32 cast."""
    parsed_brutus = parse_brutus_file(path, root=data_root)
    parsed = to_parsed_trajectory(key, parsed_brutus)
    reference, _provenance, _anomalous, _missing = parse_footer(
        parsed_brutus.footer_raw, variant=key.variant, fidelity=key.fidelity
    )
    measured = measure_dt_out(parsed_brutus.times)
    outcome = evaluate_admission(
        parsed,
        blacklist=blacklist,
        remediation_quarantine=frozenset(),
        dt_out=reference.get("dt_out"),
    )
    if outcome.disposition != "admit":
        raise AssertionError(f"oracle did not admit {key!r}: {outcome.disposition}")
    pre = preprocess_trajectory(
        parsed_brutus.times, parsed_brutus.positions,
        parsed_brutus.velocities, parsed_brutus.masses,
    )
    invariants = compute_invariants(pre.masses_ordered, pre.r0_gauge, pre.v0_gauge)
    raw_ic13 = build_raw_ic13(
        pre.masses_ordered, pre.r0_gauge, pre.v0_gauge, invariants.E
    )
    kinetic0, potential0 = _matched_plummer_components(
        pre.r_gauge[0], pre.v_gauge[0], pre.masses_ordered,
        dtype=torch.float64, device=torch.device("cpu"),
    )
    times = _cast(parsed_brutus.times)
    velocities = _cast(pre.v_gauge)
    return {
        "ic13": _cast(normalize_ic13(raw_ic13, stats)),
        "masses": _cast(pre.masses_ordered),
        "raw_ic13": _cast(raw_ic13),
        "n_snapshots": int(pre.r_gauge.shape[0]),
        "dt_out_measured": float(measured),
        "k0": float(kinetic0[0]),
        "uabs0": float(abs(potential0[0])),
        "snapshot_times": times,
        "snapshot_positions": _cast(pre.r_gauge),
        "snapshot_velocities": velocities,
        "acceleration_magnitudes": _acceleration_magnitudes(times, velocities),
    }


class ReferenceTests(unittest.TestCase):
    def test_load_reference_matches_the_preprocessed_trajectory(self):
        production = _production()
        self.assertIsNotNone(production)
        with tiny_split_fixture() as fx:
            _allowlist, reader = _reader(fx)
            admitted = reader.read(fx.allowed_key)
            pre = preprocess_trajectory(
                admitted.parsed_brutus.times,
                admitted.parsed_brutus.positions,
                admitted.parsed_brutus.velocities,
                admitted.parsed_brutus.masses,
            )
            invariants = compute_invariants(pre.masses_ordered, pre.r0_gauge, pre.v0_gauge)
            reference = production.load_reference(reader, fx.allowed_key)
        self.assertEqual(reference.positions.dtype, np.float64)
        self.assertEqual(reference.velocities.dtype, np.float64)
        self.assertEqual(reference.times.dtype, np.float64)
        np.testing.assert_array_equal(reference.positions, pre.r_gauge)
        np.testing.assert_array_equal(reference.velocities, pre.v_gauge)
        np.testing.assert_array_equal(reference.times, admitted.parsed_brutus.times)
        np.testing.assert_array_equal(reference.masses, pre.masses_ordered)
        np.testing.assert_array_equal(reference.permutation, pre.permutation)
        np.testing.assert_array_equal(reference.positions_com_ordered, pre.r_com_ordered)
        self.assertEqual(reference.inner_pair, production.inner_pair_slots(pre.permutation))
        self.assertEqual(reference.raw_ic13.shape, (13,))
        self.assertEqual(reference.E, float(invariants.E))
        self.assertEqual(reference.Q, float(invariants.Q))
        self.assertEqual(reference.s_min, float(invariants.s_min))
        self.assertEqual(reference.l_ratio, invariants.l_ratio)
        self.assertEqual(reference.grid, "base")
        self.assertEqual(reference.n_snapshots, int(pre.r_gauge.shape[0]))
        self.assertGreater(reference.n_snapshots, 0)


class PairTrackingTests(unittest.TestCase):
    def test_inner_pair_follows_the_mass_permutation(self):
        production = _production()
        self.assertIsNotNone(production)
        cases = (
            ((0.8, 0.6, 1.0), np.array([2, 0, 1], dtype=np.int64), (1, 2)),
            ((1.0, 0.6, 0.8), np.array([0, 2, 1], dtype=np.int64), (0, 2)),
        )
        for masses, permutation, slots in cases:
            trajectory, _offset, _drift = make_com_offset_trajectory(
                masses=masses, n_snapshots=8
            )
            pre = preprocess_trajectory(
                trajectory.times_raw,
                trajectory.positions_raw,
                trajectory.velocities_raw,
                trajectory.masses,
            )
            np.testing.assert_array_equal(pre.permutation, permutation)
            self.assertEqual(production.inner_pair_slots(pre.permutation), slots)


class SeamEquivalenceTests(unittest.TestCase):
    def test_resident_record_matches_the_per_file_seam_oracle(self):
        production = _production()
        self.assertIsNotNone(production)
        stats = NormalizationStats(
            slot_means=np.zeros(12, dtype=np.float64),
            slot_stds=np.ones(12, dtype=np.float64),
            e_scale=1.0,
        )
        compared = 0
        with tiny_split_fixture() as fx:
            allowlist, reader = _reader(fx)
            blacklist, _entries = load_blacklist_file(fx.blacklist_path)
            for split in ("train", "validation"):
                for key in allowlist.records(split):
                    if not reader.exists(key):
                        continue
                    try:
                        reference = production.load_reference(reader, key)
                    except NotAdmitted:
                        continue
                    oracle = _seam_oracle(
                        _brutus_path(fx.data_root, key),
                        key,
                        fx.data_root,
                        blacklist,
                        stats,
                    )
                    resident = production.resident_record(reference, stats)
                    for name in (
                        "ic13", "masses", "raw_ic13", "snapshot_times",
                        "snapshot_positions", "snapshot_velocities",
                    ):
                        self.assertTrue(
                            torch.equal(getattr(resident, name), oracle[name]),
                            name,
                        )
                    self.assertTrue(torch.equal(
                        resident.acceleration_magnitudes(),
                        oracle["acceleration_magnitudes"],
                    ))
                    self.assertEqual(resident.n_snapshots, oracle["n_snapshots"])
                    self.assertEqual(resident.dt_out_measured, oracle["dt_out_measured"])
                    self.assertEqual(resident.k0, oracle["k0"])
                    self.assertEqual(resident.uabs0, oracle["uabs0"])
                    compared += 1
            allowed = production.load_reference(reader, fx.allowed_key)
            resident = production.resident_record(allowed, stats)
            index = StageIndex([resident])
            self.assertTrue(torch.equal(
                index.snapshot_positions(fx.allowed_key), resident.snapshot_positions
            ))
            self.assertTrue(torch.equal(
                index.acceleration_magnitudes(fx.allowed_key),
                resident.acceleration_magnitudes(),
            ))
        self.assertGreater(compared, 0)


class NormalizerRecoveryTests(unittest.TestCase):
    def test_synthetic_float32_rows_recover_within_1e_6(self):
        production = _production()
        self.assertIsNotNone(production)
        rng = np.random.default_rng(59)
        means = rng.normal(scale=0.3, size=12)
        stds = rng.uniform(0.4, 1.5, size=12)
        e_scale = 1.7
        stats = NormalizationStats(slot_means=means, slot_stds=stds, e_scale=e_scale)
        latent = rng.normal(scale=0.4, size=(40, 12))
        energy = rng.uniform(-0.7, 0.7, size=40) * e_scale
        raws = np.column_stack([means + stds * latent, energy]).astype(np.float64)
        rows = []
        row_keys = []
        raw_by_key = {}
        for index, raw in enumerate(raws):
            key = RecordKey("hierarchical", "base", index)
            raw_by_key[key] = raw
            normalized = np.asarray(normalize_ic13(raw, stats), dtype=np.float32)
            for _repeat in range(32):
                rows.append(normalized.copy())
                row_keys.append(key)
        recovered, residual = production.recover_ic13_normalizer(
            np.stack(rows), row_keys, raw_by_key
        )
        self.assertLessEqual(residual, 1e-6)
        np.testing.assert_allclose(recovered.slot_means, means, rtol=1e-4, atol=1e-4)
        np.testing.assert_allclose(recovered.slot_stds, stds, rtol=1e-4, atol=1e-4)
        self.assertAlmostEqual(float(recovered.e_scale), e_scale, delta=1e-4)

    def test_corrupted_row_raises_normalizer_recovery_error(self):
        production = _production()
        self.assertIsNotNone(production)
        with tiny_split_fixture() as fx:
            _allowlist, reader = _reader(fx)
            reference = production.load_reference(reader, fx.allowed_key)
            stats = NormalizationStats(
                slot_means=np.zeros(12, dtype=np.float64),
                slot_stds=np.ones(12, dtype=np.float64),
                e_scale=max(abs(float(reference.E)), 1.0),
            )
            normalized = np.asarray(
                normalize_ic13(reference.raw_ic13, stats), dtype=np.float32
            )
            rows = np.repeat(normalized.reshape(1, -1), 32, axis=0)
            original = float(rows[0, 0])
            shifted = np.float32(original + 1e-3)
            if abs(float(shifted)) >= 0.99:
                shifted = np.float32(original - 1e-3)
            rows[0, 0] = shifted
            tau = torch.zeros((32, 14), dtype=torch.float32)
            tau[:, 1:] = torch.tensor(rows)
            key = reference.record_key
            payload = {
                "front_monitor": {
                    "batch": {
                        "data": {
                            "tau_ic13": tau,
                            "record_keys": [[key.variant, key.fidelity, key.id]] * 32,
                        }
                    }
                }
            }
            with self.assertRaises(production.NormalizerRecoveryError):
                production.recover_normalizer_from_checkpoint(
                    reader, payload, tolerance=1e-6
                )


class MonitorReproductionTests(unittest.TestCase):
    def test_synthetic_monitor_batch_reproduces_and_one_bit_flip_is_counted(self):
        production = _production()
        self.assertIsNotNone(production)
        stats = NormalizationStats(
            slot_means=np.zeros(12, dtype=np.float64),
            slot_stds=np.ones(12, dtype=np.float64),
            e_scale=1.0,
        )
        with tiny_split_fixture() as fx:
            _allowlist, reader = _reader(fx)
            reference = production.load_reference(reader, fx.allowed_key)
            payload = _monitor_payload(reference, stats)
            result = production.monitor_batch_reproduction(
                payload, {reference.record_key: reference}, stats, ic13_tolerance=0.0
            )
            self.assertEqual(result["mismatches_targets"], 0)
            self.assertEqual(result["mismatches_times"], 0)
            self.assertEqual(result["mismatches_masses"], 0)
            self.assertEqual(result["ic13_max_abs"], 0.0)
            self.assertTrue(result["passed"])
            self.assertEqual(result["rows"], 3)
            flipped = _monitor_payload(reference, stats)
            targets = flipped["front_monitor"]["batch"]["data"]["targets"]
            bits = targets.view(torch.int32)
            bits[0, 0] = bits[0, 0] ^ 1
            bad = production.monitor_batch_reproduction(
                flipped, {reference.record_key: reference}, stats, ic13_tolerance=0.0
            )
        self.assertEqual(bad["mismatches_targets"], 1)


def _monitor_payload(reference, stats):
    times = _cast(reference.times)
    positions = _cast(reference.positions)
    masses = _cast(reference.masses)
    ic13 = _cast(normalize_ic13(reference.raw_ic13, stats))
    indices = (0, 1, int(reference.n_snapshots) // 2)
    tau_rows = []
    mass_rows = []
    target_rows = []
    time_rows = []
    keys = []
    for index in indices:
        stamp = times[index]
        tau = 2.0 * (stamp / float(reference.T)) - 1.0
        tau_rows.append(torch.cat((tau.reshape(1), ic13)))
        mass_rows.append(masses)
        target_rows.append(positions[index].reshape(9))
        time_rows.append(stamp)
        key = reference.record_key
        keys.append([key.variant, key.fidelity, int(key.id)])
    return {
        "front_monitor": {
            "batch": {
                "data": {
                    "tau_ic13": torch.stack(tau_rows),
                    "masses": torch.stack(mass_rows),
                    "targets": torch.stack(target_rows),
                    "times": torch.stack(time_rows),
                    "record_keys": keys,
                }
            }
        }
    }


if __name__ == "__main__":
    unittest.main()
