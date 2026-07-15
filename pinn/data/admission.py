"""Phase 39 — the seven-clause Step-1A trajectory admission gate (DATA-02).

Implements ``ctl_instruction.md`` Step 1A (``:539-607``) in exact clause
order. Consumes ONLY a parsed float64 :class:`~pinn.data.types.ParsedTrajectory`
plus a pre-validated blacklist/remediation set -- no path, file handle,
footer-derived energy, or metrics JSON is ever accepted here (mechanically
enforced by ``tests/phase39/test_prohibitions.py``). Every disposition/reason
is returned as typed, assertable state; the caller (Plan 39-03's adapter)
aggregates and logs.

GAP-39-04 (scale-aware near-zero H(0), no denominator floor) and GAP-39-05
(a non-finite complete block quarantines the WHOLE trajectory, with
sample-drop and trajectory-disposition kept as separate counters) are
resolved autonomy rulings, not new CTL authority -- see ``39-GAPS.md``.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Any

import numpy as np

# Plummer softening used ONLY in the admission-gate Hamiltonian (distinct from
# the static-invariant softening in ``pinn.data.preprocessing`` and the
# training-time ``pinn.constants.EPS_SOFT``; all three are numerically equal
# by convention but semantically independent per-module constants).
EPS_H_SOFTENING = 1e-10

# GAP-39-04: scale-aware near-zero H(0) safety factor (reversible default).
NEAR_ZERO_EPS_FACTOR = 64

# Clause 4 completeness floor.
COMPLETENESS_MIN_FINAL_TIME = 9.5

# Clause 7 grid-consistency (warn-only) reversible defaults.
GRID_MAX_GAP_FACTOR = 1.5
GRID_MIN_SNAPSHOT_FRACTION = 0.9


# ---------------------------------------------------------------------------
# Clause 5 — pure conservation-boundary helpers (dataset-free boundary tests).
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class ConservationOutcome:
    rejected: bool
    marginal: bool
    grade: str
    scs: float
    eps_H: float


def evaluate_conservation(eps_H: float) -> ConservationOutcome:
    """SCS = log10(eps_H). Reject only ``SCS > -5``; ``SCS == -5`` is
    admitted-and-flagged Marginal; ``eps_H == 0`` is Excellent (SCS = -inf)."""
    if eps_H == 0.0:
        return ConservationOutcome(rejected=False, marginal=False, grade="Excellent",
                                    scs=-math.inf, eps_H=0.0)
    scs = math.log10(eps_H)
    rejected = scs > -5.0
    marginal = scs == -5.0
    if scs <= -10.0:
        grade = "Excellent"
    elif scs <= -6.0:
        grade = "Acceptable"
    elif scs <= -5.0:
        grade = "Marginal"
    else:
        grade = "Reject"
    return ConservationOutcome(rejected=rejected, marginal=marginal, grade=grade,
                                scs=scs, eps_H=eps_H)


def is_near_zero_initial_energy(h0: float, k0: float, v0: float) -> bool:
    """GAP-39-04: quarantine when ``H0 == 0.0`` or, for
    ``scale = |K0| + |V0| > 0``, ``|H0| <= 64 * finfo(float64).eps * scale``.
    NEVER a denominator floor -- this predicate only gates whether ``eps_H``'s
    division by ``H0`` is numerically meaningful; it never adds to ``H0``."""
    if h0 == 0.0:
        return True
    scale = abs(k0) + abs(v0)
    if scale > 0.0 and abs(h0) <= NEAR_ZERO_EPS_FACTOR * np.finfo(np.float64).eps * scale:
        return True
    return False


def _hamiltonian(masses, positions, velocities):
    """``H(t) = K(t) + V(t)`` in float64 with Plummer softening ``eps=1e-10``
    (one snapshot: ``masses`` (3,), ``positions``/``velocities`` (3, 3))."""
    K = 0.5 * float(np.sum(masses * np.sum(velocities * velocities, axis=1)))
    V = 0.0
    n = masses.shape[0]
    for i in range(n):
        for j in range(i + 1, n):
            r_safe = math.sqrt(float(np.sum((positions[i] - positions[j]) ** 2)) + EPS_H_SOFTENING ** 2)
            V -= masses[i] * masses[j] / r_safe
    return K + V, K, V


# ---------------------------------------------------------------------------
# Full seven-clause evaluator.
# ---------------------------------------------------------------------------

@dataclass
class AdmissionOutcome:
    disposition: str          # "admit" | "reject" | "quarantine"
    reasons: tuple = field(default_factory=tuple)
    warnings: tuple = field(default_factory=tuple)
    dropped_samples: int = 0
    eps_H: Any = None
    scs: Any = None
    grade: Any = None
    marginal: bool = False


def _reject(reasons, dropped_samples=0):
    return AdmissionOutcome(disposition="reject", reasons=tuple(reasons),
                             dropped_samples=dropped_samples)


def _quarantine(reasons, dropped_samples=0):
    return AdmissionOutcome(disposition="quarantine", reasons=tuple(reasons),
                             dropped_samples=dropped_samples)


def evaluate_admission(parsed, *, blacklist=frozenset(), remediation_quarantine=frozenset(),
                        com_norm=None, momentum_norm=None, dt_out=None):
    """Evaluate all seven Step-1A clauses over one parsed float64 trajectory.

    ``blacklist`` defaults to an empty ``frozenset()`` (frozen Wave-0 contract:
    ``tests/phase39/test_admission.py`` calls ``evaluate_admission(parsed)``
    with no blacklist argument). Clause 1's "missing blacklist file = hard
    init failure" is enforced upstream, at the ADAPTER boundary that loads and
    schema-validates ``problematic_ics_blacklist.json`` before calling this
    pure evaluator (Plan 39-03) -- never by this function silently treating an
    unsupplied blacklist as a fail-closed configuration error, since the
    frozen per-clause tests call this function directly with no blacklist at
    all and must still exercise clauses 3-7.

    ``remediation_quarantine`` defaults to an EMPTY ``frozenset()`` because
    clause 2 is "empty in the verified baseline" (``ctl_instruction.md:552-559``);
    passing an explicit empty set is identical to the default.

    ``com_norm``/``momentum_norm`` (optional) let the caller supply the
    Step-2.6 POST-preprocessing COM/momentum postcondition norms once
    preprocessing has run (Plan 39-03 orchestration); when absent, this clause
    is a documented no-op (mass invariance across the trajectory is already
    enforced upstream at parse time -- ``ParsedTrajectory.masses`` is a single
    ``(3,)`` vector by contract, so there is nothing further to compare here).

    ``dt_out`` (optional) is the record's resolved output interval for the
    WARN-only clause-7 grid-consistency check; absent, clause 7 is skipped.
    """
    # Clause 1: identity & blacklist (fail-closed exclusion).
    physical_key = parsed.record_key.physical_key
    if physical_key in blacklist:
        return _reject(("blacklisted",))

    # Clause 2: data-remediation quarantine (config, empty in the verified
    # baseline; a present physical key is quarantined).
    if physical_key in remediation_quarantine:
        return _quarantine(("remediation_quarantine",))

    times = np.asarray(parsed.times, dtype=np.float64)
    positions = np.asarray(parsed.positions, dtype=np.float64)
    velocities = np.asarray(parsed.velocities, dtype=np.float64)
    masses = np.asarray(parsed.masses, dtype=np.float64)

    # GAP-39-05: detect + count non-finite COMPLETE blocks; retain only finite
    # blocks for every downstream clause. ANY drop unconditionally quarantines
    # the whole trajectory -- no partial salvage, even when >= 2 finite
    # monotone blocks remain.
    finite_mask = np.array([
        bool(np.isfinite(t) and np.all(np.isfinite(positions[i])) and np.all(np.isfinite(velocities[i])))
        for i, t in enumerate(times)
    ])
    n_dropped = int(np.size(finite_mask) - np.count_nonzero(finite_mask))
    retained_times = times[finite_mask]
    retained_positions = positions[finite_mask]
    retained_velocities = velocities[finite_mask]

    if n_dropped > 0:
        reasons = ["non_finite_snapshot"]
        structural_ok, structural_reason = _structural_check(retained_times)
        if not structural_ok:
            reasons.append(structural_reason)
        return _quarantine(reasons, dropped_samples=n_dropped)

    # Clause 3: structural integrity (>= 2 finite blocks, strict monotone
    # timestamps -- no corruption was involved on this path).
    structural_ok, structural_reason = _structural_check(retained_times)
    if not structural_ok:
        return _reject((structural_reason,))

    # Clause 4: completeness. Footer presence/line counts/snapshot-count
    # constants MUST NOT be used (enforced by construction: only parsed
    # snapshot-block times are consulted).
    if float(retained_times[-1]) < COMPLETENESS_MIN_FINAL_TIME:
        return _reject(("incomplete_trajectory",))

    # Clause 5: conservation gate (locked post-v1.3; SI-DQA-003).
    H0, K0, V0 = _hamiltonian(masses, retained_positions[0], retained_velocities[0])
    if is_near_zero_initial_energy(H0, K0, V0):
        return _quarantine(("near_zero_initial_energy",))

    H_all = np.array([_hamiltonian(masses, retained_positions[i], retained_velocities[i])[0]
                       for i in range(retained_positions.shape[0])])
    eps_H = float(np.max(np.abs((H_all - H0) / H0)))
    cons = evaluate_conservation(eps_H)
    if cons.rejected:
        return AdmissionOutcome(disposition="reject", reasons=("conservation_scs_reject",),
                                 eps_H=eps_H, scs=cons.scs, grade=cons.grade, marginal=False)

    # Clause 6: physical invariant gates. Mass invariance across the
    # trajectory is already enforced upstream at parse time (see docstring);
    # the COM/momentum Step-2.6 postconditions apply to the SCALED,
    # preprocessed state and are checked here ONLY when the caller supplies
    # them (Plan 39-03 wires preprocessing before this call in the full
    # adapter orchestration).
    if com_norm is not None and com_norm >= 1e-12:
        return _quarantine(("com_postcondition_failed",))
    if momentum_norm is not None and momentum_norm >= 1e-12:
        return _quarantine(("momentum_postcondition_failed",))

    # Clause 7: grid-consistency (WARN level, never reject).
    warnings = []
    if dt_out is not None and dt_out > 0:
        diffs = np.diff(retained_times)
        max_gap = float(np.max(diffs)) if diffs.size else 0.0
        if max_gap > GRID_MAX_GAP_FACTOR * dt_out:
            warnings.append("grid_gap_exceeds_1.5x_dt_out")
        expected_n = float(retained_times[-1]) / dt_out + 1.0
        if retained_positions.shape[0] < GRID_MIN_SNAPSHOT_FRACTION * expected_n:
            warnings.append("grid_snapshot_count_below_0.9x_expected")

    return AdmissionOutcome(disposition="admit", reasons=(), warnings=tuple(warnings),
                             dropped_samples=0, eps_H=eps_H, scs=cons.scs, grade=cons.grade,
                             marginal=cons.marginal)


def _structural_check(times):
    """Clause 3: ``>= 2`` retained blocks, strictly monotone increasing
    timestamps. Returns ``(ok, reason)``."""
    if times.size < 2:
        return False, "insufficient_snapshots"
    if not bool(np.all(np.diff(times) > 0)):
        return False, "non_monotone_times"
    return True, None
