"""Phase 39 Wave-0 contract — the seven-clause Step-1A admission gate (DATA-02).

Deferred contract for ``pinn.data.admission`` (+ the ``pinn.data.types``
parsed-record type). Every test SKIPs via the localized ``_require`` helper
(importing the single ``tests.phase39._SKIP_PHRASE``) until production lands.

The conservation boundary (clause 5) and the GAP-39-04 near-zero-``H(0)``
predicate are expressed against PURE helpers so their exact boundaries are
testable dataset-free without crafting a full trajectory with a target energy
drift; structural/completeness/non-finite clauses (3, 4, GAP-39-05) are tested
through the full ``evaluate_admission`` over controllable float64 arrays.

Grounding: ``ctl_instruction.md:539-607``; GAP-39-04 (scale-aware 64-eps
quarantine, no denominator floor); GAP-39-05 (whole-trajectory quarantine after
dropping any non-finite block, sample/trajectory accounting kept separate).
The footer ``dE/E`` and metrics JSON must never gate — mechanically enforced in
``test_prohibitions.py``; here we assert the admission API takes no such input.
"""

import importlib
import inspect
import math
import unittest

from tests.phase39 import _SKIP_PHRASE

ADMISSION = "pinn.data.admission"
TYPES = "pinn.data.types"


def _require(symbol, module):
    try:
        mod = importlib.import_module(module)
    except ImportError:
        raise unittest.SkipTest(f"{_SKIP_PHRASE} {module}.{symbol}")
    if not hasattr(mod, symbol):
        raise unittest.SkipTest(f"{_SKIP_PHRASE} {module}.{symbol}")
    return getattr(mod, symbol)


def _np():
    try:
        import numpy as np
    except ImportError as exc:  # pragma: no cover
        raise unittest.SkipTest(f"numpy not installed: {exc}")
    return np


class ConservationBoundaryTests(unittest.TestCase):
    """Clause 5 disposition as a function of the recomputed ``eps_H``.

    SCS = log10(eps_H): reject only ``SCS > -5`` (eps_H > 1e-5); ``SCS == -5``
    (eps_H == 1e-5) is admitted-and-flagged Marginal; ``eps_H == 0`` is Excellent
    (SCS = -inf)."""

    def setUp(self):
        self.evaluate = _require("evaluate_conservation", ADMISSION)

    def test_reject_above_minus_five(self):
        out = self.evaluate(1e-4)              # SCS = -4 > -5
        self.assertTrue(out.rejected)

    def test_marginal_exactly_minus_five(self):
        out = self.evaluate(1e-5)              # SCS = -5 -> admit + Marginal
        self.assertFalse(out.rejected)
        self.assertTrue(out.marginal)

    def test_admit_below_minus_five(self):
        out = self.evaluate(1e-6)              # SCS = -6 -> admit
        self.assertFalse(out.rejected)
        self.assertFalse(out.marginal)

    def test_zero_drift_is_excellent(self):
        out = self.evaluate(0.0)
        self.assertFalse(out.rejected)
        self.assertEqual(out.grade, "Excellent")
        self.assertEqual(out.scs, -math.inf)


class NearZeroEnergyTests(unittest.TestCase):
    """GAP-39-04 scale-aware quarantine predicate (no denominator floor)."""

    def setUp(self):
        self.near_zero = _require("is_near_zero_initial_energy", ADMISSION)

    def _boundary(self, k0, v0):
        np = _np()
        return 64 * np.finfo(np.float64).eps * (abs(k0) + abs(v0))

    def test_exact_zero_quarantines(self):
        self.assertTrue(self.near_zero(0.0, 1.0, -1.0))

    def test_boundary_quarantines(self):
        k0, v0 = 2.0, -1.0
        h0 = self._boundary(k0, v0)            # |H0| == 64*eps*scale
        self.assertTrue(self.near_zero(h0, k0, v0))

    def test_nextafter_above_boundary_is_resolved(self):
        np = _np()
        k0, v0 = 2.0, -1.0
        h0 = np.nextafter(self._boundary(k0, v0), np.inf)
        self.assertFalse(self.near_zero(h0, k0, v0))

    def test_small_but_resolved_energy_is_not_near_zero(self):
        self.assertFalse(self.near_zero(0.5, 1.0, -0.5))


class StructuralAndCompletenessClauseTests(unittest.TestCase):
    """Clauses 3-4 over full parsed float64 arrays (disposition before clause 5)."""

    def setUp(self):
        self.evaluate_admission = _require("evaluate_admission", ADMISSION)
        self.ParsedTrajectory = _require("ParsedTrajectory", TYPES)
        self.RecordKey = _require("RecordKey", TYPES)

    def _parsed(self, times, corrupt=None):
        np = _np()
        n = len(times)
        # Deterministic finite bodies; ``corrupt(i_snapshot)`` may inject a
        # non-finite value into one snapshot's positions.
        positions = np.zeros((n, 3, 3), dtype=np.float64)
        velocities = np.zeros((n, 3, 3), dtype=np.float64)
        for s in range(n):
            for b in range(3):
                positions[s, b] = [1.0 + b + 0.1 * times[s], -0.5 * (b + 1), 0.05 * (b + 1)]
                velocities[s, b] = [0.3 * (b + 1), -0.2 * (b + 1), 0.01 * (b + 1)]
            if corrupt is not None:
                corrupt(positions, s)
        masses = np.array([1.349, 0.307, 1.344], dtype=np.float64)
        return self.ParsedTrajectory(
            record_key=self.RecordKey("hierarchical", "base", 0),
            times=np.asarray(times, dtype=np.float64),
            positions=positions, velocities=velocities, masses=masses)

    def test_fewer_than_two_snapshots_is_not_admitted(self):
        out = self.evaluate_admission(self._parsed([0.0]))
        self.assertNotEqual(out.disposition, "admit")

    def test_non_monotone_times_is_not_admitted(self):
        out = self.evaluate_admission(self._parsed([0.0, 5.0, 3.0, 9.6]))
        self.assertNotEqual(out.disposition, "admit")

    def test_incomplete_final_time_is_rejected(self):
        out = self.evaluate_admission(self._parsed([0.0, 2.0, 4.0]))  # final < 9.5
        self.assertEqual(out.disposition, "reject")

    def test_admission_api_takes_no_footer_or_metrics_input(self):
        # The gate recomputes eps_H from raw arrays: no footer / metrics param.
        params = set(inspect.signature(self.evaluate_admission).parameters)
        self.assertNotIn("footer", params)
        self.assertNotIn("metrics", params)
        self.assertNotIn("dE_over_E", params)


class OrchestrationClauseTests(unittest.TestCase):
    """Clauses 1, 2, 6, 7 plus the aggregate parsed-count identity. Every
    fixture body's inter-body separation is invariant under the shared
    ``+0.1*t`` offset applied to all three bodies, so H(t) is exactly
    conserved (eps_H == 0, Excellent) and the record cleanly reaches clause
    5/6/7 when not blocked earlier -- isolating each clause under test."""

    def setUp(self):
        self.evaluate_admission = _require("evaluate_admission", ADMISSION)
        self.ParsedTrajectory = _require("ParsedTrajectory", TYPES)
        self.RecordKey = _require("RecordKey", TYPES)
        self.PhysicalKey = _require("PhysicalKey", TYPES)

    def _times(self, n=12):
        return [round(i * (10.0 / (n - 1)), 6) for i in range(n)]

    def _parsed(self, record_key=None):
        np = _np()
        times = self._times()
        n = len(times)
        positions = np.zeros((n, 3, 3), dtype=np.float64)
        velocities = np.zeros((n, 3, 3), dtype=np.float64)
        for s in range(n):
            for b in range(3):
                positions[s, b] = [1.0 + b + 0.1 * times[s], -0.5 * (b + 1), 0.05 * (b + 1)]
                velocities[s, b] = [0.3 * (b + 1), -0.2 * (b + 1), 0.01 * (b + 1)]
        masses = np.array([1.349, 0.307, 1.344], dtype=np.float64)
        key = record_key or self.RecordKey("hierarchical", "base", 0)
        return self.ParsedTrajectory(record_key=key, times=np.asarray(times, dtype=np.float64),
                                      positions=positions, velocities=velocities, masses=masses)

    def test_control_record_admits_with_excellent_grade(self):
        # Exact-conservation-by-construction (all bodies share the +0.1*t
        # offset, so pairwise separations -- and hence H(t) -- are invariant
        # up to float64 rounding, not bit-exact zero).
        out = self.evaluate_admission(self._parsed())
        self.assertEqual(out.disposition, "admit")
        self.assertEqual(out.grade, "Excellent")
        self.assertLess(out.eps_H, 1e-10)

    # -- clause 1: identity/blacklist -----------------------------------
    def test_blacklisted_physical_key_is_excluded(self):
        key = self.RecordKey("hierarchical", "base", 3)
        blacklist = {self.PhysicalKey("hierarchical", 3)}
        out = self.evaluate_admission(self._parsed(key), blacklist=blacklist)
        self.assertNotEqual(out.disposition, "admit")
        self.assertIn("blacklisted", out.reasons)

    def test_non_blacklisted_key_is_unaffected_by_a_nonempty_blacklist(self):
        key = self.RecordKey("hierarchical", "base", 3)
        blacklist = {self.PhysicalKey("hierarchical", 999)}
        out = self.evaluate_admission(self._parsed(key), blacklist=blacklist)
        self.assertEqual(out.disposition, "admit")

    # -- clause 2: remediation quarantine ---------------------------------
    def test_remediation_quarantine_present_key_quarantines(self):
        key = self.RecordKey("hierarchical", "base", 5)
        remediation = {self.PhysicalKey("hierarchical", 5)}
        out = self.evaluate_admission(self._parsed(key), remediation_quarantine=remediation)
        self.assertEqual(out.disposition, "quarantine")
        self.assertIn("remediation_quarantine", out.reasons)

    def test_default_empty_remediation_quarantine_matches_explicit_empty_set(self):
        # Proves clause 2's fail-closed source is SPECIFIED (empty set), not
        # merely unspecified/omitted.
        default_out = self.evaluate_admission(self._parsed())
        explicit_out = self.evaluate_admission(self._parsed(), remediation_quarantine=frozenset())
        self.assertEqual(default_out.disposition, explicit_out.disposition)
        self.assertEqual(default_out.reasons, explicit_out.reasons)

    # -- clause 6: physical invariant gates (optional post-preprocessing) --
    def test_com_postcondition_failure_quarantines_when_supplied(self):
        out = self.evaluate_admission(self._parsed(), com_norm=1e-6)
        self.assertEqual(out.disposition, "quarantine")
        self.assertIn("com_postcondition_failed", out.reasons)

    def test_momentum_postcondition_failure_quarantines_when_supplied(self):
        out = self.evaluate_admission(self._parsed(), momentum_norm=1e-6)
        self.assertEqual(out.disposition, "quarantine")
        self.assertIn("momentum_postcondition_failed", out.reasons)

    def test_com_momentum_absent_by_default_does_not_block_admission(self):
        out = self.evaluate_admission(self._parsed())
        self.assertEqual(out.disposition, "admit")

    # -- clause 7: grid-consistency (WARN only, never reject) --------------
    def test_grid_consistency_warns_but_does_not_reject(self):
        # dt_out far smaller than the actual ~0.909 spacing -> max_gap warning.
        out = self.evaluate_admission(self._parsed(), dt_out=0.1)
        self.assertEqual(out.disposition, "admit")
        self.assertTrue(any("grid" in w for w in out.warnings))

    def test_grid_consistency_matching_dt_out_does_not_warn(self):
        out = self.evaluate_admission(self._parsed(), dt_out=10.0 / 11.0)
        self.assertEqual(out.disposition, "admit")
        self.assertEqual(out.warnings, ())

    # -- aggregate identity -------------------------------------------------
    def test_parsed_equals_admitted_plus_rejected_plus_quarantined(self):
        admit_key = self.RecordKey("hierarchical", "base", 0)
        reject_key = self.RecordKey("hierarchical", "base", 1)
        quarantine_key = self.RecordKey("hierarchical", "base", 2)
        blacklist = {self.PhysicalKey("hierarchical", 1)}
        remediation = {self.PhysicalKey("hierarchical", 2)}

        outcomes = [
            self.evaluate_admission(self._parsed(admit_key), blacklist=blacklist,
                                    remediation_quarantine=remediation),
            self.evaluate_admission(self._parsed(reject_key), blacklist=blacklist,
                                    remediation_quarantine=remediation),
            self.evaluate_admission(self._parsed(quarantine_key), blacklist=blacklist,
                                    remediation_quarantine=remediation),
        ]
        counts = {"admit": 0, "reject": 0, "quarantine": 0}
        for out in outcomes:
            counts[out.disposition] += 1
        self.assertEqual(sum(counts.values()), len(outcomes))
        self.assertEqual(counts, {"admit": 1, "reject": 1, "quarantine": 1})
        # dropped_samples is a fully independent counter from disposition.
        self.assertTrue(all(isinstance(o.dropped_samples, int) for o in outcomes))


class NonFiniteQuarantineTests(unittest.TestCase):
    """GAP-39-05 — a non-finite block quarantines the WHOLE trajectory; sample
    drops and trajectory disposition are kept as separate counters."""

    def setUp(self):
        self.evaluate_admission = _require("evaluate_admission", ADMISSION)
        self.ParsedTrajectory = _require("ParsedTrajectory", TYPES)
        self.RecordKey = _require("RecordKey", TYPES)

    def _times(self, n=12):
        return [round(i * (10.0 / (n - 1)), 6) for i in range(n)]

    def _parsed(self, times, corrupt=None):
        np = _np()
        n = len(times)
        positions = np.zeros((n, 3, 3), dtype=np.float64)
        velocities = np.zeros((n, 3, 3), dtype=np.float64)
        for s in range(n):
            for b in range(3):
                positions[s, b] = [1.0 + b + 0.1 * times[s], -0.5 * (b + 1), 0.05 * (b + 1)]
                velocities[s, b] = [0.3 * (b + 1), -0.2 * (b + 1), 0.01 * (b + 1)]
        if corrupt is not None:
            corrupt(positions)
        masses = np.array([1.349, 0.307, 1.344], dtype=np.float64)
        return self.ParsedTrajectory(
            record_key=self.RecordKey("hierarchical", "base", 0),
            times=np.asarray(times, dtype=np.float64),
            positions=positions, velocities=velocities, masses=masses)

    def test_interior_nonfinite_block_quarantines_and_counts_one_drop(self):
        def corrupt(pos):
            pos[6, 1, 0] = float("inf")     # interior snapshot 6, body 1
        out = self.evaluate_admission(self._parsed(self._times(), corrupt))
        self.assertEqual(out.disposition, "quarantine")
        self.assertIn("non_finite_snapshot", out.reasons)
        self.assertEqual(out.dropped_samples, 1)

    def test_all_finite_control_is_not_nonfinite_quarantined(self):
        out = self.evaluate_admission(self._parsed(self._times()))
        self.assertNotIn("non_finite_snapshot", out.reasons)
        self.assertEqual(out.dropped_samples, 0)

    def test_fewer_than_two_finite_blocks_records_both_reasons(self):
        def corrupt(pos):
            pos[1:, 0, 0] = float("nan")    # all but the first snapshot
        out = self.evaluate_admission(self._parsed(self._times(), corrupt))
        self.assertEqual(out.disposition, "quarantine")
        self.assertIn("non_finite_snapshot", out.reasons)
        # Structural insufficiency is also recorded (dual-reason case).
        self.assertTrue(any("structural" in r or "insufficient" in r for r in out.reasons))

    def test_disposition_counts_partition_and_drops_are_separate(self):
        # A record contributes to exactly one of admit/reject/quarantine; a
        # dropped sample is an independent count, never a disposition.
        out = self.evaluate_admission(self._parsed(self._times()))
        self.assertIn(out.disposition, {"admit", "reject", "quarantine"})
        self.assertIsInstance(out.dropped_samples, int)


class RemediationSupplierContractTests(unittest.TestCase):
    """N3: the clause-2 remediation set has a SPECIFIED empty-``frozenset``
    default (not an unspecified/omitted source), and the production
    ``AdmittedSetAdapter`` additionally passes it EXPLICITLY from its constructor
    (that explicit-supplier behaviour is verified end-to-end in
    ``tests/phase39/test_adapter.py::ProductionRootAndBlacklistTests``)."""

    def test_evaluate_admission_remediation_default_is_specified_empty_frozenset(self):
        evaluate_admission = _require("evaluate_admission", ADMISSION)
        sig = inspect.signature(evaluate_admission)
        param = sig.parameters["remediation_quarantine"]
        self.assertIsInstance(param.default, frozenset)
        self.assertEqual(param.default, frozenset())


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
