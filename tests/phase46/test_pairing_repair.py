"""Phase 46 Plan 08 seam contract + Phase 47 Plan 01 (CONF-09) resident contract.

Two distinct surfaces live in this one file, and the distinction is the point.

``PreprocessingPairingSeamTests`` covers the ``PreprocessedTrajectory``
INTERMEDIATE that Phase 46 added: the COM-recentered, zero-momentum,
canonically ordered arrays before rotation or global scaling. That seam is
unchanged by Phase 47 (47-CONTEXT.md D-03 keeps the fields in place), so every
method in that class is byte-identical to the Phase 46 original.

``AdapterPairingRepairTests`` covers the RESIDENT surface the adapter serves.
Phase 47 CONF-09 completed the residency transform (GAP-46-07 owner ruling
2026-07-28, option A): residents now carry the FULL canonical pipeline —
COM/boost gauge, canonical body order, rotation gauge, and ``D``/``V`` scaling.
This file is corrected in place rather than superseded by a parallel Phase 47
oracle (47-CONTEXT.md D-06): two competing oracles for one property is the
failure ``46-CONTEXT.md`` warns against.

Oracle discipline. Expected arrays are derived directly from the raw fixture
equations; production preprocessing helpers are deliberately not reused to
construct the oracle. Because the rotation gauge is built by SELECTING and
orthonormalizing direction vectors (``preprocessing.py:140-171``), a second
implementation of that selection does not reproduce bit-for-bit — so the
independent oracle asserts body ORDER and STRUCTURE with a scale-relative
closeness, never bit-exactness. The one bit-exact resident claim lives in
``test_resident_trajectory_is_rotation_gauged_and_globally_scaled``, where a
single shared ``preprocess_trajectory`` call produces both sides.
"""

from __future__ import annotations

import hashlib
import itertools
import unittest

import numpy as np

from pinn.constants import D_CHARACTERISTIC_LENGTH, T_CHARACTERISTIC_TIME
from pinn.data.adapter import AdmittedSetAdapter, parse_brutus_file
from pinn.data.preprocessing import ETA_GAUGE, preprocess_trajectory
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


def _independent_rotation_gauge(masses_ordered, r0_ordered, v0_ordered, D, T):
    """Rebuild the §2.4 Jacobi rotation gauge INLINE for the oracle.

    Deliberately does not call ``preprocess_trajectory`` or
    ``pinn.data.preprocessing._rotation_gauge`` — reusing either would collapse
    the oracle into the thing it checks (47-01-PLAN.md task 1(d)(i)).

    All three §2.4 branches are written out, because the tiny-corpus fixture is
    genuinely lambda-degenerate: its bodies are collinear at ``t = 0``
    (``tests/phase39/_fixtures.py::_body_line`` places body ``i`` at
    ``(1+i) * (1, -0.5, 0.05)``), so ``lambda_perp`` vanishes to round-off and
    the gauge is fixed by the velocity-candidate fallback. An oracle that
    implemented only the primary branch would be measuring a different gauge
    than production and would report a spurious O(1) failure.
    """
    m1 = float(masses_ordered[0])
    m2 = float(masses_ordered[1])
    V = D / T
    rho = r0_ordered[1] - r0_ordered[0]
    lam = r0_ordered[2] - (m1 * r0_ordered[0] + m2 * r0_ordered[1]) / (m1 + m2)

    rho_norm = float(np.linalg.norm(rho))
    if rho_norm <= ETA_GAUGE * D:
        raise AssertionError(
            "oracle fixture is rho-degenerate; a rho-degenerate record is "
            "quarantined by production and cannot reach the resident surface"
        )
    e_x = rho / rho_norm

    lam_perp = lam - np.dot(lam, e_x) * e_x
    lam_perp_norm = float(np.linalg.norm(lam_perp))
    if lam_perp_norm > ETA_GAUGE * D:
        e_y = lam_perp / lam_perp_norm
    else:
        rho_dot = v0_ordered[1] - v0_ordered[0]
        lambda_dot = v0_ordered[2] - (
            m1 * v0_ordered[0] + m2 * v0_ordered[1]
        ) / (m1 + m2)
        e_y = None
        for candidate in (
            rho_dot, lambda_dot, v0_ordered[0], v0_ordered[1], v0_ordered[2]
        ):
            candidate_perp = candidate - np.dot(candidate, e_x) * e_x
            if float(np.linalg.norm(candidate_perp)) > ETA_GAUGE * V:
                e_y = candidate_perp / float(np.linalg.norm(candidate_perp))
                break
        if e_y is None:
            basis = np.eye(3)
            fallback = basis[int(np.argmin(np.abs(basis @ e_x)))]
            fallback_perp = fallback - np.dot(fallback, e_x) * e_x
            e_y = fallback_perp / float(np.linalg.norm(fallback_perp))
        # Deterministic sign: keep lambda_y >= 0 whenever numerically meaningful.
        if np.dot(lam_perp, e_y) < 0:
            e_y = -e_y

    e_z = np.cross(e_x, e_y)
    return np.stack([e_x, e_y, e_z], axis=0)


def _oracle_scale(oracle):
    """Largest magnitude in the oracle array — the scale the resident bound is
    taken relative to."""
    return float(np.max(np.abs(np.asarray(oracle, dtype=np.float64))))


def _resident_closeness_bound(oracle):
    """Scale-relative bound for a float64 oracle vs. an fp32 RESIDENT array.

    DERIVED, not chosen. Two independent float64 implementations of the same
    orthonormalization agree to a few hundred float64 ULP, which is invisible
    next to the dominant term: residency is an fp32 contract
    (``adapter.py::_materialize``), so the resident value is the float64
    pipeline output rounded to float32 — an error of up to ``0.5 * eps32`` times
    the element magnitude. The bound therefore rides on ``numpy.finfo(float32).eps``
    at the array's own scale, reusing the ``32.0`` fp32 round-trip allowance this
    file already uses in
    ``test_resident_trajectory_preserves_com_and_zero_momentum_gauge``.

    The value is deliberately NOT load-bearing: every defect this oracle exists
    to catch — a wrong canonical body order, a missing rotation, a missing
    ``D``/``V`` scale (the scale factor alone is ``D ≈ 4.64``) — produces an O(1)
    RELATIVE difference, seven orders of magnitude above an fp32 round-trip. If
    an assertion against this bound fails, fix the transform chain; never widen
    the bound.
    """
    return 32.0 * float(np.finfo(np.float32).eps) * _oracle_scale(oracle)


def _pairing_residual(resident, oracle, body_order):
    """Max absolute deviation between the resident array and the oracle read
    under ``body_order``.

    The resident-surface analogue of the probe's
    ``stepwise_attribution.plus_permutation`` discriminator: it is zero (within
    the fp32 residency bound) under the IDENTITY body map and nonzero under
    every other, which is what "the permutation is applied exactly once" means
    at this surface.
    """
    resident64 = np.asarray(resident, dtype=np.float64)
    reordered = np.asarray(oracle, dtype=np.float64)[:, list(body_order), :]
    return float(np.max(np.abs(resident64 - reordered)))


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
    positions_ordered = positions_com[:, permutation, :]
    velocities_ordered = velocities_com[:, permutation, :]
    masses_ordered = masses[permutation]

    # CONF-09: the oracle now carries the COMPLETED canonical chain — the same
    # rotation gauge and D/V scaling the resident surface acquired in Phase 47 —
    # still reimplemented inline from the parsed arrays.
    D = float(D_CHARACTERISTIC_LENGTH)
    T = float(T_CHARACTERISTIC_TIME)
    V = D / T
    R0 = _independent_rotation_gauge(
        masses_ordered, positions_ordered[0], velocities_ordered[0], D, T
    )
    positions_gauge = (positions_ordered @ R0.T) / D
    velocities_gauge = (velocities_ordered @ R0.T) / V
    return (
        adapter,
        key,
        parsed,
        positions_gauge,
        velocities_gauge,
        masses_ordered,
    )


class AdapterPairingRepairTests(unittest.TestCase):
    def test_resident_positions_velocities_and_masses_share_one_body_order(self):
        """Independent oracle: BODY ORDER + STRUCTURE, scale-relatively.

        The oracle reimplements the whole canonical chain inline, including the
        rotation gauge. Two independent implementations of a
        selection-and-orthonormalization basis do not agree bit-for-bit, and the
        resident surface is fp32 besides, so this method deliberately uses NO
        exact-equality assertion on the transformed arrays (the bit-exact claim
        belongs to ``test_resident_trajectory_is_rotation_gauged_and_globally_scaled``,
        where one shared ``preprocess_trajectory`` call feeds both sides). Masses
        are untransformed, so they stay an exact comparison.
        """
        with TinyCorpus() as corpus:
            (
                adapter,
                key,
                _parsed,
                expected_positions,
                expected_velocities,
                expected_masses,
            ) = _resident_fixture(corpus)

            resident_positions = adapter.snapshot_positions(key).cpu().numpy()
            resident_velocities = adapter.snapshot_velocities(key).cpu().numpy()

            position_bound = _resident_closeness_bound(expected_positions)
            velocity_bound = _resident_closeness_bound(expected_velocities)

            self.assertTrue(
                np.allclose(
                    resident_positions,
                    expected_positions,
                    rtol=0.0,
                    atol=position_bound,
                ),
                "resident positions diverge from the independent canonical oracle",
            )
            self.assertTrue(
                np.allclose(
                    resident_velocities,
                    expected_velocities,
                    rtol=0.0,
                    atol=velocity_bound,
                ),
                "resident velocities diverge from the independent canonical oracle",
            )
            np.testing.assert_array_equal(
                adapter.get(key).masses.cpu().numpy(),
                expected_masses.astype(np.float32),
            )

            # The permutation is applied EXACTLY ONCE: the identity body map is
            # the only one under which the resident/oracle pairing residual
            # vanishes (the resident-surface reading of the probe's
            # ``plus_permutation = 0.0`` discriminator). Every other body map
            # leaves an O(scale) residual, so the separation is structural, not
            # a matter of where the bound sits.
            self.assertLessEqual(
                _pairing_residual(resident_positions, expected_positions, (0, 1, 2)),
                position_bound,
            )
            self.assertLessEqual(
                _pairing_residual(resident_velocities, expected_velocities, (0, 1, 2)),
                velocity_bound,
            )
            for order in itertools.permutations((0, 1, 2)):
                if order == (0, 1, 2):
                    continue
                self.assertGreater(
                    _pairing_residual(
                        resident_positions, expected_positions, order
                    ),
                    position_bound,
                    f"body map {order} also matches: resident body order is ambiguous",
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

    def test_resident_trajectory_is_rotation_gauged_and_globally_scaled(self):
        """CONF-09: residents ARE the canonical rotation-gauged, D/V-scaled series.

        Both sides come from one shared ``preprocess_trajectory`` call over the
        same parsed arrays — the adapter's internal call and this one are the
        same deterministic float64 computation — so the resident tensors are
        exactly the fp32 cast of ``r_gauge``/``v_gauge``. This is the one place
        in the file where exact equality is licensed; the independent oracle
        above is scale-relative by necessity.
        """
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

            np.testing.assert_array_equal(
                resident_positions,
                preprocessed.r_gauge.astype(np.float32),
            )
            np.testing.assert_array_equal(
                resident_velocities,
                preprocessed.v_gauge.astype(np.float32),
            )
            # The global scale really is applied: the unscaled series is a
            # factor of D (resp. V) away and must NOT match.
            self.assertFalse(
                np.allclose(
                    resident_positions,
                    preprocessed.r_gauge * preprocessed.D,
                )
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
