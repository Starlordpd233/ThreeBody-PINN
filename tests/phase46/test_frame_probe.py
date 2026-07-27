"""Dataset-free CONF-01 target-frame probe suite (plan 46-02, Tasks 1-2).

Drives ``pinn/verification/target_frame_probe.py`` against the 46-01 dual-frame
fixtures and the REAL ``pinn.data.preprocessing.preprocess_trajectory`` (the
positive control is the genuine locked transform, not a re-implementation;
D-21). No real-corpus file is read anywhere in this module (D-24); every
control is built from a synthetic closed-form trajectory.

The production module is present, so every test RUNS — none use the deferred
``_SKIP_PHRASE`` convention. The suite is green only when the probe genuinely
identifies arms, pins boundary semantics, fail-closes on degeneracy, attributes
confounds, sorts its population, and routes exactly one of four verdicts.
"""

from __future__ import annotations

import unittest

import numpy as np

from pinn.constants import D_CHARACTERISTIC_LENGTH, T_CHARACTERISTIC_TIME
from pinn.data.preprocessing import preprocess_trajectory
from pinn.data.types import RecordKey
from pinn.verification import target_frame_probe as tfp
from pinn.verification.target_frame_probe import (
    ARM_RAW,
    ARM_SCALED,
    VERDICT_AMBIGUOUS,
    VERDICT_NON_FRAME_DIVERGENCE,
    VERDICT_TARGETS_ARE_RAW,
    VERDICT_TARGETS_ARE_SCALED,
    FrameProbeUnavailable,
)

from tests.phase46._fixtures import (
    make_com_offset_trajectory,
    make_degenerate_trajectory,
    make_dual_frame_trajectory,
)

_D = float(D_CHARACTERISTIC_LENGTH)
_T = float(T_CHARACTERISTIC_TIME)


# ---------------------------------------------------------------------------
# Builders shared across the suite
# ---------------------------------------------------------------------------


def _preprocess(trajectory):
    return preprocess_trajectory(
        trajectory.times_raw,
        trajectory.positions_raw,
        trajectory.velocities_raw,
        trajectory.masses,
    )


def _controls(trajectory, pre):
    return (
        trajectory.times_raw,
        trajectory.positions_raw,
        trajectory.velocities_raw,
        trajectory.masses,
        pre,
    )


def _resident(trajectory, *, positions, velocities, masses=None):
    if masses is None:
        masses = trajectory.masses
    return (
        trajectory.times_raw,
        np.asarray(positions, dtype=np.float64),
        np.asarray(velocities, dtype=np.float64),
        np.asarray(masses, dtype=np.float64),
    )


def _fp32(array):
    return np.asarray(array, dtype=np.float64).astype(np.float32).astype(np.float64)


def _key(i=0):
    return RecordKey("hierarchical", "base", int(i))


# ---------------------------------------------------------------------------
# Task 1: arm primitives, residual, tolerance, measure_trajectory
# ---------------------------------------------------------------------------


class ArmPrimitivesTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.traj = make_dual_frame_trajectory()
        cls.pre = _preprocess(cls.traj)
        cls.controls = _controls(cls.traj, cls.pre)

    def test_1_scaled_frame_identifies_scaled_arm(self):
        # Resident == r' (scaled targets): scaled arm coherent, raw arm separated.
        resident = _resident(
            self.traj,
            positions=self.traj.positions_scaled,
            velocities=self.traj.velocities_scaled,
        )
        m = tfp.measure_trajectory(_key(), resident, self.controls)
        self.assertTrue(np.isfinite(m.numerical_tolerance))
        self.assertLessEqual(m.arms[ARM_SCALED].median, m.numerical_tolerance)
        self.assertGreater(m.arms[ARM_RAW].median, m.numerical_tolerance)
        # separation[X] = arm X's own residual strictly above tolerance.
        self.assertFalse(m.separation[ARM_SCALED])
        self.assertTrue(m.separation[ARM_RAW])

    def test_2_raw_frame_identifies_raw_arm(self):
        # Resident == r (raw targets): raw arm coherent, scaled arm separated.
        # Structurally symmetric to test_1 (same helper, the other encoding).
        resident = _resident(
            self.traj,
            positions=self.traj.positions_raw,
            velocities=self.traj.velocities_raw,
        )
        m = tfp.measure_trajectory(_key(), resident, self.controls)
        self.assertTrue(np.isfinite(m.numerical_tolerance))
        self.assertLessEqual(m.arms[ARM_RAW].median, m.numerical_tolerance)
        self.assertGreater(m.arms[ARM_SCALED].median, m.numerical_tolerance)
        self.assertTrue(m.separation[ARM_SCALED])
        self.assertFalse(m.separation[ARM_RAW])

    def test_3_boundary_direction_is_le_consistent_strict_separated(self):
        tol = 0.5
        # residual == tolerance -> consistent, NOT separated (boundary pinned).
        self.assertTrue(tfp._consistent(tol, tol))
        self.assertFalse(tfp._separated(tol, tol))
        self.assertTrue(tfp._consistent(tol - 1e-9, tol))
        self.assertTrue(tfp._separated(tol + 1e-9, tol))
        # Non-finite fails closed in both directions.
        self.assertFalse(tfp._consistent(float("nan"), tol))
        self.assertFalse(tfp._separated(float("nan"), tol))
        self.assertFalse(tfp._consistent(0.1, float("nan")))

    def test_4a_single_snapshot_is_recorded_not_raised(self):
        traj = make_degenerate_trajectory("single_snapshot")
        self.assertEqual(traj.positions_raw.shape[0], 1)
        try:
            pre = _preprocess(traj)
            controls = _controls(traj, pre)
        except Exception:
            controls = None
        resident = _resident(
            traj, positions=traj.positions_raw, velocities=traj.velocities_raw
        )
        m = tfp.measure_trajectory(_key(), resident, controls)
        # No unhandled exception; the trajectory fails closed (no verdict from it).
        self.assertFalse(m.finite)
        reasons = {reason for _, reason in m.exclusions}
        self.assertIn("too_few_snapshots", reasons)

    def test_4b_non_finite_snapshot_is_ledgered_not_silently_skipped(self):
        traj = make_degenerate_trajectory("non_finite")
        self.assertTrue(np.isnan(traj.positions_raw).any())
        resident = _resident(
            traj, positions=traj.positions_raw, velocities=traj.velocities_raw
        )
        # controls=None isolates the probe's own fail-closed path (preprocessing a
        # NaN-laden trajectory is not the property under test here).
        m = tfp.measure_trajectory(_key(), resident, None)
        self.assertFalse(m.finite)
        reasons = {reason for _, reason in m.exclusions}
        self.assertIn("non_finite", reasons)

    def test_5_qualifying_mask_is_symmetric_and_exclusions_identical(self):
        resident = _resident(
            self.traj,
            positions=self.traj.positions_scaled,
            velocities=self.traj.velocities_scaled,
        )
        m = tfp.measure_trajectory(_key(), resident, self.controls)
        # Same qualifying count across all four arms (D-03 mask symmetry).
        lengths = {len(arm.relative_residual) for arm in m.arms.values()}
        self.assertEqual(len(lengths), 1)
        # Every ArmResidual carries the shared ledger; non-empty (endpoints exist),
        # and identical exclusion indices across all four arms.
        self.assertGreater(len(m.exclusions), 0)
        for arm in m.arms.values():
            self.assertGreater(len(arm.exclusions), 0)
        idx_tuples = {tuple(i for i, _ in arm.exclusions) for arm in m.arms.values()}
        self.assertEqual(len(idx_tuples), 1)

    def test_6_tolerance_two_term_provenance_no_physics_constant(self):
        # GAP-46-03 Option A: floor = max(control medians); fp32 = measured,
        # nonnegative increment; tolerance = floor + increment; no multiplier.
        pos = tfp.ArmResidual(
            arm="positive_control", median=1e-3, maximum=1e-3,
            relative_residual=np.array([1e-3]), exclusions=(), finite=True,
        )
        prov = tfp.ArmResidual(
            arm="provenance_control", median=2e-3, maximum=2e-3,
            relative_residual=np.array([2e-3]), exclusions=(), finite=True,
        )
        floor, inc, tol = tfp.numerical_tolerance_for([pos, prov], lambda: 5e-4)
        self.assertAlmostEqual(floor, 2e-3)            # max of control medians
        self.assertAlmostEqual(inc, 5e-4)              # measured round-trip term
        self.assertAlmostEqual(tol, 2e-3 + 5e-4)       # sum, NO safety multiplier
        self.assertGreater(tol, 0.0)
        # The fp32 term is genuinely measured: changing it changes the tolerance.
        _, _, tol_larger = tfp.numerical_tolerance_for([pos, prov], lambda: 1e-2)
        self.assertGreater(tol_larger, tol)
        # A negative measured increment is clamped to zero (guardrail 2), not nan.
        floor_n, inc_n, tol_n = tfp.numerical_tolerance_for([pos, prov], lambda: -1.0)
        self.assertEqual(inc_n, 0.0)
        self.assertAlmostEqual(tol_n, floor_n)
        # Non-finite control median OR non-finite increment fails closed (guardrail 5).
        nan_arm = tfp.ArmResidual(
            arm="positive_control", median=float("nan"), maximum=float("nan"),
            relative_residual=np.array([]), exclusions=(), finite=False,
        )
        _, _, tol_nan_ctrl = tfp.numerical_tolerance_for([nan_arm, prov], lambda: 1e-3)
        self.assertTrue(np.isnan(tol_nan_ctrl))
        _, _, tol_nan_inc = tfp.numerical_tolerance_for([pos, prov], lambda: float("nan"))
        self.assertTrue(np.isnan(tol_nan_inc))
        # No module-level physics-threshold constant participates.
        for forbidden in ("DEFAULT_RESIDUAL_THRESHOLD", "DEFAULT_NEWTONIAN_RESIDUAL_THRESHOLD"):
            self.assertFalse(hasattr(tfp, forbidden))


# ---------------------------------------------------------------------------
# Task 2: confounds, population traversal, fail-closed verdict
# ---------------------------------------------------------------------------


class ConfoundAndPopulationTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.traj = make_dual_frame_trajectory()
        cls.pre = _preprocess(cls.traj)
        cls.controls = _controls(cls.traj, cls.pre)

    # -- Test 1: identity discrimination ----------------------------------

    def test_7a_identity_raw_when_resident_is_fp32_of_parsed(self):
        resident = _resident(
            self.traj,
            positions=_fp32(self.traj.positions_raw),
            velocities=_fp32(self.traj.velocities_raw),
        )
        conf = tfp.measure_confounds(_key(), resident, self.controls)
        self.assertTrue(conf.identity_raw)
        self.assertFalse(conf.identity_scaled)
        self.assertFalse(conf.identity_neither)

    def test_7b_identity_scaled_when_resident_is_fp32_of_positive_control(self):
        resident = _resident(
            self.traj,
            positions=_fp32(self.pre.r_gauge),
            velocities=_fp32(self.pre.v_gauge),
            masses=self.pre.masses_ordered,
        )
        conf = tfp.measure_confounds(_key(), resident, self.controls)
        self.assertTrue(conf.identity_scaled)
        self.assertFalse(conf.identity_raw)
        self.assertFalse(conf.identity_neither)

    def test_7c_identity_neither_for_an_ungauged_scaled_resident(self):
        # r' in the fixture's own orientation matches neither raw parsed nor the
        # canonically-gauged positive control.
        resident = _resident(
            self.traj,
            positions=self.traj.positions_scaled,
            velocities=self.traj.velocities_scaled,
        )
        conf = tfp.measure_confounds(_key(), resident, self.controls)
        self.assertTrue(conf.identity_neither)

    # -- Test 2: permutation confound + corrected re-evaluation -----------

    def test_8_permutation_correction_restores_coherence(self):
        # A non-identity canonical permutation (masses supplied non-descending).
        base = make_dual_frame_trajectory(masses=(0.6, 1.0, 0.8))
        pre = _preprocess(base)
        perm = tuple(int(i) for i in pre.permutation)
        self.assertNotEqual(perm, (0, 1, 2), "fixture must force a non-identity gauge")
        controls = _controls(base, pre)
        # Resident: FILE-order positions paired with CANONICAL-order masses (the
        # mass-pairing confound the plan's corrected re-evaluation targets).
        resident = _resident(
            base,
            positions=base.positions_raw,
            velocities=base.velocities_raw,
            masses=pre.masses_ordered,
        )
        measures = tfp.measure_trajectory(_key(), resident, controls)
        conf = tfp.measure_confounds(_key(), resident, controls)
        self.assertEqual(len(conf.restoring_permutation), 3)
        # Uncorrected raw arm (mismatched masses) separates; corrected re-aligns.
        self.assertGreater(conf.raw_residual_uncorrected, measures.numerical_tolerance)
        self.assertLessEqual(conf.raw_residual_corrected, measures.numerical_tolerance)
        self.assertLess(conf.raw_residual_corrected, conf.raw_residual_uncorrected)

    # -- Test 3: COM/boost confound ---------------------------------------

    def test_9_com_offset_confound_attributes_com_step(self):
        traj, offset, drift = make_com_offset_trajectory()
        pre = _preprocess(traj)
        controls = _controls(traj, pre)
        resident = _resident(
            traj, positions=traj.positions_raw, velocities=traj.velocities_raw
        )
        conf = tfp.measure_confounds(_key(), resident, controls)
        # The stored resident still carries the injected COM offset at t=0.
        np.testing.assert_allclose(conf.com_offset_stored, offset, atol=1e-8)
        # The COM-recenter step is the first diverging transform (D-04 attribution).
        self.assertEqual(conf.first_diverging_step, "com_recenter_boost")

    # -- Test 4: population ordering --------------------------------------

    def test_10_population_traversal_sorts_by_record_key(self):
        inserted = [RecordKey("hierarchical", "base", 1002),
                    RecordKey("hierarchical", "base", 1000),
                    RecordKey("hierarchical", "base", 1001)]
        population = [(k, {"seed42": "train"}) for k in inserted]
        resident = _resident(
            self.traj,
            positions=self.traj.positions_scaled,
            velocities=self.traj.velocities_scaled,
        )
        res_book = {k: resident for k in inserted}
        ctrl_book = {k: self.controls for k in inserted}
        _, accounting = tfp.probe_population(
            population,
            lambda k: res_book[k],
            lambda k: ctrl_book[k],
        )
        self.assertEqual(accounting["sorted_keys"], sorted(inserted))

    # -- Test 5: four-way verdict routing ---------------------------------

    def _two_member_population(self, build):
        """Build a 2-member (train, validation) population from per-index builder."""
        res_book, ctrl_book, population = {}, {}, []
        for i, split in enumerate(("train", "validation")):
            key = RecordKey("hierarchical", "base", 2000 + i)
            resident, controls = build(i)
            res_book[key] = resident
            ctrl_book[key] = controls
            population.append((key, {"seed42": split}))
        return population, res_book, ctrl_book

    def _verdict(self, population, res_book, ctrl_book):
        results, accounting = tfp.probe_population(
            population, lambda k: res_book[k], lambda k: ctrl_book[k]
        )
        return tfp.decide_verdict(results, accounting)

    def test_11a_conformant_scaled_population_yields_targets_are_scaled(self):
        def build(_i):
            resident = _resident(
                self.traj,
                positions=_fp32(self.pre.r_gauge),
                velocities=_fp32(self.pre.v_gauge),
                masses=self.pre.masses_ordered,
            )
            return resident, self.controls
        pop, res, ctrl = self._two_member_population(build)
        outcome = self._verdict(pop, res, ctrl)
        self.assertEqual(outcome.verdict, VERDICT_TARGETS_ARE_SCALED)

    def test_11b_raw_population_yields_targets_are_raw(self):
        def build(_i):
            resident = _resident(
                self.traj,
                positions=_fp32(self.traj.positions_raw),
                velocities=_fp32(self.traj.velocities_raw),
            )
            return resident, self.controls
        pop, res, ctrl = self._two_member_population(build)
        outcome = self._verdict(pop, res, ctrl)
        self.assertEqual(outcome.verdict, VERDICT_TARGETS_ARE_RAW)

    def test_11c_ungauged_scaled_population_yields_non_frame_divergence(self):
        # r' in the fixture orientation (scaled, no canonical gauge): identity to
        # neither control, but a transform divergence is attributable.
        def build(_i):
            resident = _resident(
                self.traj,
                positions=self.traj.positions_scaled,
                velocities=self.traj.velocities_scaled,
            )
            return resident, self.controls
        pop, res, ctrl = self._two_member_population(build)
        outcome = self._verdict(pop, res, ctrl)
        self.assertEqual(outcome.verdict, VERDICT_NON_FRAME_DIVERGENCE)

    def test_11d_train_validation_disagreement_yields_ambiguous(self):
        # train member is scaled-conformant, validation member is raw -> disagree.
        def scaled_resident():
            return _resident(
                self.traj,
                positions=_fp32(self.pre.r_gauge),
                velocities=_fp32(self.pre.v_gauge),
                masses=self.pre.masses_ordered,
            )
        def raw_resident():
            return _resident(
                self.traj,
                positions=_fp32(self.traj.positions_raw),
                velocities=_fp32(self.traj.velocities_raw),
            )
        k_train = RecordKey("hierarchical", "base", 3000)
        k_val = RecordKey("hierarchical", "base", 3001)
        population = [(k_train, {"seed42": "train"}), (k_val, {"seed42": "validation"})]
        res_book = {k_train: scaled_resident(), k_val: raw_resident()}
        ctrl_book = {k_train: self.controls, k_val: self.controls}
        outcome = self._verdict(population, res_book, ctrl_book)
        self.assertEqual(outcome.verdict, VERDICT_AMBIGUOUS)

    def test_11e_non_finite_measure_yields_ambiguous(self):
        nan_pos = np.full_like(self.traj.positions_raw, np.nan)
        nan_vel = np.full_like(self.traj.velocities_raw, np.nan)

        def build(i):
            if i == 0:
                # All-non-finite resident -> every arm NaN, trajectory fail-closed.
                # (measure_confounds indexes controls[4]; pass clean controls.)
                resident = _resident(self.traj, positions=nan_pos, velocities=nan_vel)
            else:
                resident = _resident(
                    self.traj,
                    positions=_fp32(self.traj.positions_raw),
                    velocities=_fp32(self.traj.velocities_raw),
                )
            return resident, self.controls

        pop, res, ctrl = self._two_member_population(build)
        outcome = self._verdict(pop, res, ctrl)
        self.assertEqual(outcome.verdict, VERDICT_AMBIGUOUS)

    # -- Test 6: empty population -----------------------------------------

    def test_12_empty_population_raises_unavailable(self):
        results, accounting = tfp.probe_population(
            [], lambda k: None, lambda k: None
        )
        with self.assertRaises(FrameProbeUnavailable):
            tfp.decide_verdict(results, accounting)


if __name__ == "__main__":
    unittest.main()
