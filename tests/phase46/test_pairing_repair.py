"""Phase 46 Plan 08 — minimal resident pairing repair contract.

The repair exposes the COM-recentered, zero-momentum, canonically ordered
trajectory before rotation or global scaling.  Expected arrays below are
derived directly from the raw fixture equations; production preprocessing
helpers are deliberately not reused to construct the oracle.
"""

from __future__ import annotations

import hashlib
import unittest

import numpy as np

from pinn.data.adapter import AdmittedSetAdapter, parse_brutus_file
from pinn.data.preprocessing import preprocess_trajectory
from pinn.data.types import RecordKey
from tests.phase39._fixtures import TinyCorpus
from tests.phase46._fixtures import make_com_offset_trajectory


_MASSES = (0.8, 0.6, 1.0)
_EXPECTED_PERMUTATION = np.array([2, 0, 1], dtype=np.int64)
_OLD_ARRAY_FINGERPRINTS = {
    "masses_ordered": "b8770265dc5210ea5db7013c5b2e4e5a97cb2ecc3d602b8189be3e61207868a4",
    "permutation": "53afea624a503a0bf39e469e8979f67fcb1890ea0392adf9e155124f5ede9ebb",
    "r0_gauge": "bc2692dc23954896578bc113bf77d6de5af607f0f45c2702526ac45a669cd3b2",
    "v0_gauge": "cd6d62ee6ab8495edd815669767adcce51513b693afccaa9b6a1131f245200b9",
    "r_gauge": "edb1749dc6280e87d624e7b217588c62cd0b4f33b5470bc820383bac88d2dd22",
    "v_gauge": "191213351dc1e5f349db02d45a6bb7a76815cbf05b85521dd4b0871b8e88b59e",
    "R0": "40565c1e592d6397b65ba53fa36ab5b66f0c80c4df500dae2780ae1511900b1b",
    "R_COM0": "f9739ffbe7acfe4fa92b772de5b4c9113415ba8cf62d4b6a2ad71d565c190c06",
    "V_COM": "d80d8dbff2422107e96032e992bd2d329fab2948c1ab82667bec980f113429d7",
}
_OLD_SCALAR_HEX = {
    "D": "0x1.290fca9c761f7p+2",
    "T": "0x1.4000000000000p+3",
    "V": "0x1.db4c7760bcff2p-2",
}


def _fixture_and_preprocessed():
    trajectory, _offset, _drift = make_com_offset_trajectory(
        masses=_MASSES, n_snapshots=8
    )
    preprocessed = preprocess_trajectory(
        trajectory.times_raw,
        trajectory.positions_raw,
        trajectory.velocities_raw,
        trajectory.masses,
    )
    return trajectory, preprocessed


def _independent_com_ordered(trajectory):
    masses = np.asarray(trajectory.masses, dtype=np.float64)
    positions = np.asarray(trajectory.positions_raw, dtype=np.float64)
    velocities = np.asarray(trajectory.velocities_raw, dtype=np.float64)
    times = np.asarray(trajectory.times_raw, dtype=np.float64)
    total_mass = float(np.sum(masses))
    initial_com = np.sum(masses[:, None] * positions[0], axis=0) / total_mass
    com_velocity = np.sum(masses[:, None] * velocities[0], axis=0) / total_mass
    positions_com = (
        positions
        - initial_com[None, None, :]
        - com_velocity[None, None, :] * times[:, None, None]
    )
    velocities_com = velocities - com_velocity[None, None, :]
    return (
        positions_com[:, _EXPECTED_PERMUTATION, :],
        velocities_com[:, _EXPECTED_PERMUTATION, :],
    )


def _fingerprint(array):
    return hashlib.sha256(np.asarray(array).tobytes(order="C")).hexdigest()


class PreprocessingPairingSeamTests(unittest.TestCase):
    def test_exposes_independently_derived_ordered_com_arrays_as_float64(self):
        trajectory, preprocessed = _fixture_and_preprocessed()
        expected_positions, expected_velocities = _independent_com_ordered(trajectory)

        self.assertEqual(preprocessed.r_com_ordered.dtype, np.float64)
        self.assertEqual(preprocessed.v_com_ordered.dtype, np.float64)
        np.testing.assert_array_equal(
            preprocessed.permutation, _EXPECTED_PERMUTATION
        )
        np.testing.assert_array_equal(
            preprocessed.r_com_ordered, expected_positions
        )
        np.testing.assert_array_equal(
            preprocessed.v_com_ordered, expected_velocities
        )

    def test_exposed_arrays_satisfy_mass_weighted_com_and_momentum_gauge(self):
        _trajectory, preprocessed = _fixture_and_preprocessed()

        initial_com = np.sum(
            preprocessed.masses_ordered[:, None]
            * preprocessed.r_com_ordered[0],
            axis=0,
        )
        initial_momentum = np.sum(
            preprocessed.masses_ordered[:, None]
            * preprocessed.v_com_ordered[0],
            axis=0,
        )
        self.assertLess(float(np.linalg.norm(initial_com)), 1e-12)
        self.assertLess(float(np.linalg.norm(initial_momentum)), 1e-12)

    def test_exposed_arrays_are_neither_rotated_nor_globally_scaled(self):
        _trajectory, preprocessed = _fixture_and_preprocessed()

        self.assertFalse(
            np.allclose(preprocessed.r_com_ordered, preprocessed.r_gauge)
        )
        self.assertFalse(
            np.allclose(
                preprocessed.r_com_ordered,
                preprocessed.r_gauge * preprocessed.D,
            )
        )
        self.assertFalse(
            np.allclose(
                preprocessed.v_com_ordered,
                preprocessed.v_gauge * preprocessed.V,
            )
        )
        self.assertAlmostEqual(
            float(np.linalg.norm(preprocessed.r_com_ordered)),
            float(np.linalg.norm(preprocessed.r_gauge)) * preprocessed.D,
            places=12,
        )
        self.assertAlmostEqual(
            float(np.linalg.norm(preprocessed.v_com_ordered)),
            float(np.linalg.norm(preprocessed.v_gauge)) * preprocessed.V,
            places=12,
        )

    def test_additive_fields_leave_every_preexisting_output_bit_identical(self):
        _trajectory, preprocessed = _fixture_and_preprocessed()

        for field, expected in _OLD_ARRAY_FINGERPRINTS.items():
            self.assertEqual(
                _fingerprint(getattr(preprocessed, field)),
                expected,
                field,
            )
        for field, expected in _OLD_SCALAR_HEX.items():
            self.assertEqual(float(getattr(preprocessed, field)).hex(), expected, field)


def _adapter(corpus):
    return AdmittedSetAdapter(
        root=corpus.data_root,
        blacklist_path=corpus.blacklist_path,
        precision="float32",
        device="cpu",
        run_dir=corpus.run_dir,
        version_metadata_path=corpus.version_metadata_path,
    )


def _resident_fixture(corpus):
    adapter = _adapter(corpus)
    key = RecordKey("hierarchical", "base", 0)
    path = corpus._brutus_path(
        "brutus_hierarchical", "hierarchical", 0
    )
    parsed = parse_brutus_file(path, root=corpus.data_root)
    masses = np.asarray(parsed.masses, dtype=np.float64)
    total_mass = float(np.sum(masses))
    initial_com = (
        np.sum(masses[:, None] * parsed.positions[0], axis=0) / total_mass
    )
    com_velocity = (
        np.sum(masses[:, None] * parsed.velocities[0], axis=0) / total_mass
    )
    positions_com = (
        parsed.positions
        - initial_com[None, None, :]
        - com_velocity[None, None, :] * parsed.times[:, None, None]
    )
    velocities_com = parsed.velocities - com_velocity[None, None, :]
    permutation = np.array([0, 2, 1], dtype=np.int64)
    return (
        adapter,
        key,
        parsed,
        positions_com[:, permutation, :],
        velocities_com[:, permutation, :],
        masses[permutation],
    )


class AdapterPairingRepairTests(unittest.TestCase):
    def test_resident_positions_velocities_and_masses_share_one_body_order(self):
        with TinyCorpus() as corpus:
            (
                adapter,
                key,
                _parsed,
                expected_positions,
                expected_velocities,
                expected_masses,
            ) = _resident_fixture(corpus)

            np.testing.assert_array_equal(
                adapter.snapshot_positions(key).cpu().numpy(),
                expected_positions.astype(np.float32),
            )
            np.testing.assert_array_equal(
                adapter.snapshot_velocities(key).cpu().numpy(),
                expected_velocities.astype(np.float32),
            )
            np.testing.assert_array_equal(
                adapter.get(key).masses.cpu().numpy(),
                expected_masses.astype(np.float32),
            )

    def test_resident_trajectory_preserves_com_and_zero_momentum_gauge(self):
        with TinyCorpus() as corpus:
            (
                adapter,
                key,
                _parsed,
                expected_positions,
                expected_velocities,
                expected_masses,
            ) = _resident_fixture(corpus)
            upstream_com = np.sum(
                expected_masses[:, None] * expected_positions[0], axis=0
            )
            upstream_momentum = np.sum(
                expected_masses[:, None] * expected_velocities[0], axis=0
            )
            self.assertLess(float(np.linalg.norm(upstream_com)), 1e-12)
            self.assertLess(float(np.linalg.norm(upstream_momentum)), 1e-12)

            masses = adapter.get(key).masses.cpu().numpy().astype(np.float64)
            positions = (
                adapter.snapshot_positions(key).cpu().numpy().astype(np.float64)
            )
            velocities = (
                adapter.snapshot_velocities(key).cpu().numpy().astype(np.float64)
            )
            initial_com = np.sum(masses[:, None] * positions[0], axis=0)
            initial_momentum = np.sum(masses[:, None] * velocities[0], axis=0)
            # Materialization is an existing fp32 contract, so the resident
            # assertion uses a scale-derived fp32 round-trip bound after the
            # upstream float64 seam has met the preprocessing 1e-12 tolerance.
            eps32 = np.finfo(np.float32).eps
            com_roundoff_bound = (
                32.0
                * eps32
                * max(1.0, float(np.sum(np.abs(masses[:, None] * positions[0]))))
            )
            momentum_roundoff_bound = (
                32.0
                * eps32
                * max(1.0, float(np.sum(np.abs(masses[:, None] * velocities[0]))))
            )

            self.assertLess(float(np.linalg.norm(initial_com)), com_roundoff_bound)
            self.assertLess(
                float(np.linalg.norm(initial_momentum)),
                momentum_roundoff_bound,
            )

    def test_resident_trajectory_is_not_rotation_gauged_or_globally_scaled(self):
        with TinyCorpus() as corpus:
            adapter, key, parsed, *_expected = _resident_fixture(corpus)
            preprocessed = preprocess_trajectory(
                parsed.times,
                parsed.positions,
                parsed.velocities,
                parsed.masses,
            )
            resident_positions = adapter.snapshot_positions(key).cpu().numpy()
            resident_velocities = adapter.snapshot_velocities(key).cpu().numpy()

            self.assertFalse(
                np.allclose(resident_positions, preprocessed.r_gauge)
            )
            self.assertFalse(
                np.allclose(
                    resident_positions,
                    preprocessed.r_gauge * preprocessed.D,
                )
            )
            self.assertFalse(
                np.allclose(resident_velocities, preprocessed.v_gauge)
            )
            self.assertFalse(
                np.allclose(
                    resident_velocities,
                    preprocessed.v_gauge * preprocessed.V,
                )
            )

    def test_admission_keys_snapshot_counts_and_folder_accounting_are_unchanged(self):
        expected_folder_counts = {
            "brutus_hierarchical": {
                "found": 9,
                "admitted": 6,
                "rejected": 2,
                "quarantined": 1,
                "dropped_samples": 11,
            },
            "brutus_hierarchical_gold_standard": {
                "found": 3,
                "admitted": 2,
                "rejected": 1,
                "quarantined": 0,
                "dropped_samples": 0,
            },
            "brutus_standard_quasi_random": {
                "found": 3,
                "admitted": 2,
                "rejected": 1,
                "quarantined": 0,
                "dropped_samples": 0,
            },
            "brutus_standard_quasi_random_gold_standard": {
                "found": 2,
                "admitted": 1,
                "rejected": 1,
                "quarantined": 0,
                "dropped_samples": 0,
            },
        }
        expected_snapshots = {
            RecordKey("hierarchical", "base", ident): 12
            for ident in (0, 7, 42, 55, 200, 202)
        }
        expected_snapshots.update(
            {
                RecordKey("hierarchical", "gold", ident): 24
                for ident in (0, 7)
            }
        )
        expected_snapshots.update(
            {
                RecordKey("standard", "base", ident): 12
                for ident in (0, 9)
            }
        )
        expected_snapshots[RecordKey("standard", "gold", 0)] = 24

        with TinyCorpus() as corpus:
            adapter = _adapter(corpus)
            self.assertEqual(adapter.folder_counts, expected_folder_counts)
            self.assertEqual(
                {key: adapter.n_snapshots(key) for key in adapter.record_keys()},
                expected_snapshots,
            )
            self.assertEqual(
                sum(adapter.n_snapshots(key) for key in adapter.record_keys()),
                168,
            )


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
