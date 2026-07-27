"""Phase 46 dataset-free fixtures — no ``simulation_data/`` access.

Two fixture families back the whole Phase 46 suite:

- A duck-typed ``StubStageSource`` mirroring the
  ``pinn.data.splits.StageIndex`` method surface, plus
  ``make_stub_split_sources`` returning a disjoint ``(train_source,
  validation_source)`` pair (two independent sources over non-overlapping
  ``RecordKey`` sets — the shape ``StageIndex.from_split`` materializes for the
  ``"train"`` and ``"validation"`` split names). No constructor for any
  third/withheld split view exists in this module (D-16); plan 46-05's isolation
  suite re-asserts that absence.
- A closed-form dual-frame trajectory generator ``make_dual_frame_trajectory``
  (D-21) that emits the SAME physical trajectory in two locked encodings — raw
  ``(r, v, t)`` and scaled ``(r/D, v*T/D, t/T)`` — using ``pinn.constants``
  ``D_CHARACTERISTIC_LENGTH`` / ``T_CHARACTERISTIC_TIME`` so the fixture and the
  production probe share exactly one source of ``D``/``T``. Degenerate,
  empty-population, pairing-confound, and COM-offset builders feed the
  fail-closed and discriminator paths of plans 46-02..46-07.

Two ``StubStageSource`` contract details are load-bearing and are honored, not
smoothed over:

(a) ``record_keys()`` and ``records_at_or_below(stage)`` return keys in the
    caller-supplied INSERTION order, never sorted — the real ``StageIndex``
    returns ``tuple(self._records)`` (``splits.py:200``) and a filtered walk over
    that same dict (``splits.py:254-261``), so a stub that quietly sorted would
    make every downstream ``sorted(...)`` assertion vacuous.
(b) ``records_at_or_below(stage)`` accepts a PLAIN INT (the ``StageIndex``
    contract via ``_numeric_stage``), never an object that must carry a
    ``.value`` attribute.

RNG discipline: any RNG accepted by these fixtures would be an explicit
``numpy.random.Generator``; these builders are deterministic and use no global
RNG state.
"""

from __future__ import annotations

from dataclasses import dataclass
from types import SimpleNamespace

import numpy as np

from pinn.constants import D_CHARACTERISTIC_LENGTH, T_CHARACTERISTIC_TIME

__all__ = [
    "StubStageSource",
    "make_stub_split_sources",
    "StubModel",
    "DualFrameTrajectory",
    "make_dual_frame_trajectory",
    "make_degenerate_trajectory",
    "make_empty_source",
    "make_pairing_confound_trajectory",
    "make_com_offset_trajectory",
]


# ---------------------------------------------------------------------------
# StageIndex-shaped stub source
# ---------------------------------------------------------------------------


def _numeric_stage(stage) -> int:
    """Coerce a stage argument to a plain int (accepts an int or a label)."""
    return int(getattr(stage, "value", stage))


class StubStageSource:
    """Duck-typed ``StageIndex`` over an explicit ordered record population.

    Constructed from an ordered mapping ``RecordKey -> record`` (a ``dict`` or an
    iterable of pairs); the caller controls insertion order, and every key-returning
    method preserves that order rather than sorting it (mirrors the real
    ``StageIndex`` — see module docstring (a)). Records are lightweight namespaces
    exposing the ``AdmittedRecord``-shaped fields downstream suites dereference.
    """

    def __init__(self, records_by_key, *, blacklisted_physical_keys=(),
                 gold_numeric_stage_count=0, dt_out=1.0):
        if isinstance(records_by_key, dict):
            items = list(records_by_key.items())
        else:
            items = list(records_by_key)
        # Plain dict preserves insertion order (Py3.7+); ``_order`` records it
        # explicitly so the key-returning methods never depend on sort order.
        self._records = dict(items)
        self._order = [key for key, _ in items]
        self._blacklisted_physical_keys = frozenset(blacklisted_physical_keys)
        self._gold_numeric_stage_count = int(gold_numeric_stage_count)
        self._dt_out = float(dt_out)

    # -- population surface -------------------------------------------------

    @property
    def blacklisted_physical_keys(self):
        return self._blacklisted_physical_keys

    @property
    def gold_numeric_stage_count(self):
        return self._gold_numeric_stage_count

    def record_keys(self):
        # Insertion order, never sorted (mirrors StageIndex.record_keys).
        return tuple(self._order)

    def get(self, key):
        return self._records[key]

    def has_stage(self, stage):
        numeric = _numeric_stage(stage)
        return any(self._stage_value(key) == numeric for key in self._order)

    def records_at(self, stage):
        numeric = _numeric_stage(stage)
        return tuple(key for key in self._order if self._stage_value(key) == numeric)

    def records_at_or_below(self, stage):
        # Insertion order over the same dict, plain-int threshold (mirrors
        # StageIndex.records_at_or_below, splits.py:254-261).
        numeric = _numeric_stage(stage)
        return tuple(
            key for key in self._order if self._stage_value(key) <= numeric
        )

    def is_blacklisted(self, physical_key):
        return physical_key in self._blacklisted_physical_keys

    # -- per-record snapshot surface ---------------------------------------

    def n_snapshots(self, key):
        return int(self._records[key].n_snapshots)

    def snapshot_times(self, key):
        # Deliberately ends at 9.5 so a per-record times[-1] normalizer is caught.
        return np.linspace(0.0, 9.5, self.n_snapshots(key), dtype=np.float64)

    def snapshot_positions(self, key):
        times = self.snapshot_times(key)
        positions = np.zeros((len(times), 3, 3), dtype=np.float64)
        positions[:, 0, 0] = times + key.id / 1000.0
        positions[:, 1, 1] = 2.0 * times
        positions[:, 2, 2] = -times
        return positions

    def snapshot_velocities(self, key):
        times = self.snapshot_times(key)
        velocities = np.zeros((len(times), 3, 3), dtype=np.float64)
        velocities[:, 0, 0] = times ** 2
        velocities[:, 1, 1] = times
        return velocities

    def acceleration_magnitudes(self, key):
        return np.arange(1, self.n_snapshots(key) + 1, dtype=np.float64)

    def dt_out(self, key):
        record = self._records[key]
        if hasattr(record, "dt_out_measured"):
            return float(record.dt_out_measured)
        return self._dt_out

    def stage_label(self, key):
        return self._records[key].stage_label

    # -- internals ----------------------------------------------------------

    def _stage_value(self, key):
        label = self._records[key].stage_label
        return _numeric_stage(label)


def _build_stub_record(key, *, stage_label, n_snapshots):
    """Build one ``AdmittedRecord``-shaped namespace for the stub source."""
    masses = np.array([1.0 + key.id / 10000.0, 2.0, 3.0], dtype=np.float64)
    ic13 = np.linspace(0.0, 1.2, 13, dtype=np.float64) + key.id / 10000.0
    return SimpleNamespace(
        record_key=key,
        physical_key=key.physical_key,
        variant=key.variant,
        fidelity=key.fidelity,
        ic13=ic13,
        masses=masses,
        raw_ic13=ic13.copy(),
        n_snapshots=int(n_snapshots),
        E=float(-0.5 - key.id / 10000.0),
        stage_label=stage_label,
        dt_out_measured=1.0,
    )


def _make_ordered_records(ids, *, stage0_value, n_snapshots):
    """Return an insertion-ordered ``RecordKey -> record`` dict.

    Keys are inserted in the order of ``ids`` (so a caller supplying ids in
    deliberately non-ascending order produces a non-sorted ``record_keys()``).
    """
    from pinn.data.types import RecordKey, StageLabel

    label = StageLabel.STAGE_0 if stage0_value == 0 else StageLabel.STAGE_1
    ordered = {}
    for ident in ids:
        key = RecordKey("hierarchical", "base", int(ident))
        ordered[key] = _build_stub_record(key, stage_label=label, n_snapshots=n_snapshots)
    return ordered


def make_stub_split_sources(n_train=6, n_validation=6, n_snapshots=16):
    """Return a disjoint ``(train_source, validation_source)`` pair.

    Mirrors production's ``StageIndex.from_split(source, manifest, "train")`` and
    ``StageIndex.from_split(source, manifest, "validation")`` — two independent
    ``StageIndex``-shaped sources over non-overlapping ``RecordKey`` sets. The two
    id ranges are disjoint, so the physical-key populations never overlap.

    The validation source is inserted in DESCENDING id order on purpose: its
    ``records_at_or_below(0)`` then returns keys in a non-ascending order that
    differs from ``sorted(...)``, so downstream ``sorted(...)`` requirements are
    genuinely exercised rather than passing vacuously (module docstring (a)).
    """
    train_ids = tuple(range(0, n_train))
    # Disjoint range, inserted descending so insertion order != sorted order.
    validation_ids = tuple(range(1000 + n_validation - 1, 1000 - 1, -1))
    train_records = _make_ordered_records(train_ids, stage0_value=0, n_snapshots=n_snapshots)
    validation_records = _make_ordered_records(
        validation_ids, stage0_value=0, n_snapshots=n_snapshots
    )
    train_source = StubStageSource(train_records)
    validation_source = StubStageSource(validation_records)
    return train_source, validation_source


def make_empty_source():
    """Return a ``StubStageSource`` with zero records (fail-closed empty path)."""
    return StubStageSource({})


# ---------------------------------------------------------------------------
# Stub model
# ---------------------------------------------------------------------------


class StubModel:
    """Callable stub with the production model call signature.

    ``model(tau_ic13, masses)`` returns an ``(N, 9)`` float64 tensor (3 bodies x
    3 coordinates). Exposes ``.eval()`` / ``.train()`` / ``.training`` so a
    caller's ``model.eval()`` / ``try/finally: model.train()`` bracket is
    observable, a ``.calls`` list recording the input shapes received, and an
    injectable ``fail_hook`` invoked per call so a test can raise mid-pass and
    assert mode restoration.
    """

    def __init__(self, *, fail_hook=None, n_out=9):
        self.training = True
        self.calls = []
        self._fail_hook = fail_hook
        self._n_out = int(n_out)

    def eval(self):
        self.training = False
        return self

    def train(self, mode=True):
        self.training = bool(mode)
        return self

    def __call__(self, tau_ic13, masses):
        import torch

        self.calls.append((tuple(tau_ic13.shape), tuple(masses.shape)))
        if self._fail_hook is not None:
            self._fail_hook(self)
        n = int(tau_ic13.shape[0])
        return torch.zeros((n, self._n_out), dtype=torch.float64)


# ---------------------------------------------------------------------------
# Dual-frame synthetic trajectory (D-21)
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class DualFrameTrajectory:
    """One physical trajectory in two locked encodings (raw and scaled).

    Fields:
        masses: ``(3,)`` ordered raw masses shared by both encodings.
        times_raw / positions_raw / velocities_raw: the raw ``(r, v, t)``
            encoding — ``positions_raw`` is ``(Nt, 3, 3)``, ``velocities_raw`` the
            same, ``times_raw`` ``(Nt,)``.
        times_scaled / positions_scaled / velocities_scaled: the locked
            ``(r/D, v*T/D, t/T)`` encoding, derived from the raw arrays via the
            single shared ``D`` / ``T``.
        D: ``pinn.constants.D_CHARACTERISTIC_LENGTH``.
        T: ``pinn.constants.T_CHARACTERISTIC_TIME``.
        finite_difference_tolerance: a FINITE-DIFFERENCE / dtype NUMERICAL
            tolerance — the central-second-difference truncation bound of the
            scaled (larger-error) frame plus an fp64 round-off floor. It is NOT a
            physics acceptance threshold: it states only the resolution at which
            the matched-frame force-consistency identity can be checked, never a
            target-quality / Hamiltonian / training threshold (D-06).
    """

    masses: np.ndarray
    times_raw: np.ndarray
    positions_raw: np.ndarray
    velocities_raw: np.ndarray
    times_scaled: np.ndarray
    positions_scaled: np.ndarray
    velocities_scaled: np.ndarray
    D: float
    T: float
    finite_difference_tolerance: float


def _lagrange_equilateral(masses, side, n_snapshots, n_periods):
    """Closed-form Lagrange equilateral three-body solution (G = 1).

    Three bodies at the vertices of an equilateral triangle of side ``side``
    rotate rigidly about the mass-weighted centre of mass at angular velocity
    ``omega`` with ``omega**2 = (m1 + m2 + m3) / side**3``. This is an EXACT
    Newtonian solution for arbitrary masses: the net gravitational acceleration
    on body i reduces to ``omega**2 * (r_COM - r_i)``, i.e. exactly the centripetal
    acceleration of rigid rotation about the COM (the two-line derivation:
    ``a_i = sum_{j!=i} m_j (r_j - r_i)/|r_j - r_i|^3`` with all pair separations
    equal to ``side`` ``= (G/a^3)[M r_COM - M r_i] = omega**2 (r_COM - r_i)``). No
    integrator is needed, so the trajectory is deterministic, snapshot-parametric,
    and exactly force-consistent by construction.

    Returns ``(times, positions, velocities, omega, amplitude)`` in the raw frame,
    with the COM at the origin; ``amplitude`` is the largest body-to-COM distance.
    """
    masses = np.asarray(masses, dtype=np.float64)
    total_mass = float(masses.sum())
    omega = float(np.sqrt(total_mass / side ** 3))  # G = 1
    circumradius = side / np.sqrt(3.0)
    phi = np.array([0.0, 2.0 * np.pi / 3.0, 4.0 * np.pi / 3.0])
    # Equilateral vertices centered on the geometric centroid (the origin).
    vertices = np.stack(
        [circumradius * np.cos(phi), circumradius * np.sin(phi), np.zeros(3)],
        axis=-1,
    )  # (3, 3): (body, coord)
    # Shift so the mass-weighted COM sits at the origin (the rotation centre).
    com = (masses.reshape(3, 1) * vertices).sum(axis=0) / total_mass
    q = vertices - com  # initial body positions relative to the COM

    period = 2.0 * np.pi / omega
    t_end = n_periods * period
    times = np.linspace(0.0, t_end, int(n_snapshots), dtype=np.float64)
    theta = omega * times
    c = np.cos(theta)
    s = np.sin(theta)
    positions = np.empty((len(times), 3, 3), dtype=np.float64)
    velocities = np.empty((len(times), 3, 3), dtype=np.float64)
    for n in range(len(times)):
        rotation = np.array(
            [[c[n], -s[n], 0.0], [s[n], c[n], 0.0], [0.0, 0.0, 1.0]]
        )
        positions[n] = q @ rotation.T
        # v = omega * (z-hat cross r): exact time derivative of rigid rotation.
        velocities[n, :, 0] = -omega * positions[n, :, 1]
        velocities[n, :, 1] = omega * positions[n, :, 0]
        velocities[n, :, 2] = 0.0
    amplitude = float(np.linalg.norm(q, axis=-1).max())
    return times, positions, velocities, omega, amplitude


def _scaled_frame_tolerance(h_raw, omega, amplitude, D, T):
    """Derive the finite-difference/dtype numerical tolerance (NOT a physics
    threshold) from the sampling, ``omega``, and the shared ``D`` / ``T``.

    The central second difference has truncation error
    ``(h**2 / 12) * max|r''''|``; for rigid rotation ``|r''''| ~ omega**4 *
    amplitude``. The SCALED frame ``(r/D, u = t/T)`` carries the larger error
    because ``d2/du2`` amplifies the raw truncation by ``T**2 / D`` (== ``D**2``
    under the locked identity ``D**3 == T**2``). We bound the per-snapshot vector
    norm by ``sqrt(9) = 3`` times the worst per-component error of the scaled
    frame, plus an fp64 round-off floor at the acceleration scale. The result is a
    rigorous upper bound on any matched-frame residual, named so it can never be
    mistaken for a physics acceptance threshold.
    """
    if h_raw <= 0.0:
        # Fewer than two snapshots: no finite-difference resolution exists, so the
        # numerical tolerance is 0.0 (which downstream reads as fail-closed).
        return 0.0
    omega_u = omega * T
    h_u = h_raw / T
    amplitude_u = amplitude / D
    wh = omega_u * h_u
    # Exact per-unit-amplitude central-second-difference error factor for a
    # sinusoid: omega_u**2 * |1 - 2(1 - cos(wh)) / wh**2| (== omega_u**2*wh**2/12
    # to leading order). Using the closed form keeps the bound rigorous, not a
    # bare constant.
    exact_factor = omega_u ** 2 * abs(1.0 - 2.0 * (1.0 - np.cos(wh)) / (wh ** 2))
    truncation_bound = 3.0 * amplitude_u * exact_factor  # sqrt(9) vector factor
    roundoff_floor = 1e-12 * omega_u ** 2 * amplitude_u
    return float(truncation_bound + roundoff_floor)


def make_dual_frame_trajectory(*, masses=(1.0, 0.8, 0.6), side=1.0,
                               n_snapshots=64, n_periods=0.5):
    """Build one physical trajectory in both locked encodings from one ``D``/``T``.

    The raw encoding satisfies ``d2r/dt2 == a_newton(r, m)`` to finite-difference
    accuracy by construction (closed-form Lagrange solution); the scaled encoding
    satisfies ``d2r'/du2 == a_newton(r', m)`` to the same accuracy because
    ``D**3 == T**2`` with ``G = 1``. Treating the raw arrays as if they were ``r'``
    leaves a residual larger than the tolerance by a factor of ``T**2 - 1``, so the
    two frames are separable rather than degenerate.
    """
    masses = np.asarray(masses, dtype=np.float64)
    D = float(D_CHARACTERISTIC_LENGTH)
    T = float(T_CHARACTERISTIC_TIME)
    times_raw, positions_raw, velocities_raw, omega, amplitude = _lagrange_equilateral(
        masses, float(side), int(n_snapshots), float(n_periods)
    )
    h_raw = float(times_raw[1] - times_raw[0]) if len(times_raw) > 1 else 0.0
    tolerance = _scaled_frame_tolerance(h_raw, omega, amplitude, D, T)
    return DualFrameTrajectory(
        masses=masses,
        times_raw=times_raw,
        positions_raw=positions_raw,
        velocities_raw=velocities_raw,
        times_scaled=times_raw / T,
        positions_scaled=positions_raw / D,
        velocities_scaled=velocities_raw * T / D,
        D=D,
        T=T,
        finite_difference_tolerance=tolerance,
    )


def make_degenerate_trajectory(kind, *, masses=(1.0, 0.8, 0.6), side=1.0,
                               n_snapshots=8, n_periods=0.25):
    """Build a degenerate trajectory for the fail-closed paths.

    ``kind``:
        ``"non_finite"`` — positions contain a NaN at an interior snapshot.
        ``"coincident"`` — two bodies share identical positions at every snapshot
            (zero pairwise separation).
        ``"single_snapshot"`` — exactly one time sample.
    """
    if kind == "single_snapshot":
        n_snapshots = 1
    trajectory = make_dual_frame_trajectory(
        masses=masses, side=side, n_snapshots=n_snapshots, n_periods=n_periods
    )
    positions_raw = trajectory.positions_raw.copy()
    velocities_raw = trajectory.velocities_raw.copy()
    if kind == "non_finite":
        if len(positions_raw) < 2:
            raise ValueError("non_finite degenerate fixture needs >= 2 snapshots")
        positions_raw[1, 0, 0] = np.nan
    elif kind == "coincident":
        positions_raw[:, 1, :] = positions_raw[:, 0, :]
        velocities_raw[:, 1, :] = velocities_raw[:, 0, :]
    elif kind != "single_snapshot":
        raise ValueError(f"unknown degenerate kind: {kind!r}")
    D = trajectory.D
    T = trajectory.T
    return DualFrameTrajectory(
        masses=trajectory.masses,
        times_raw=trajectory.times_raw,
        positions_raw=positions_raw,
        velocities_raw=velocities_raw,
        times_scaled=trajectory.times_raw / T,
        positions_scaled=positions_raw / D,
        velocities_scaled=velocities_raw * T / D,
        D=D,
        T=T,
        finite_difference_tolerance=trajectory.finite_difference_tolerance,
    )


def make_pairing_confound_trajectory(*, masses=(1.0, 0.8, 0.6), side=1.0,
                                     n_snapshots=64, n_periods=0.5, shift=1):
    """Build a trajectory whose mass vector is misaligned with its positions.

    Returns ``(trajectory, permutation)``: the SAME Lagrange positions, but with
    the mass vector cyclically rolled by ``shift`` relative to the position array,
    plus the applied index permutation ``permutation`` such that
    ``masses_confounded = masses[list(permutation)]``. Plan 46-02's permutation
    discriminator asserts the probe both DETECTS the misalignment and reports which
    permutation restores coherence (D-04).
    """
    trajectory = make_dual_frame_trajectory(
        masses=masses, side=side, n_snapshots=n_snapshots, n_periods=n_periods
    )
    permutation = tuple(int((i - shift) % 3) for i in range(3))
    confounded_masses = trajectory.masses[list(permutation)].copy()
    confounded = DualFrameTrajectory(
        masses=confounded_masses,
        times_raw=trajectory.times_raw,
        positions_raw=trajectory.positions_raw,
        velocities_raw=trajectory.velocities_raw,
        times_scaled=trajectory.times_scaled,
        positions_scaled=trajectory.positions_scaled,
        velocities_scaled=trajectory.velocities_scaled,
        D=trajectory.D,
        T=trajectory.T,
        finite_difference_tolerance=trajectory.finite_difference_tolerance,
    )
    return confounded, permutation


def make_com_offset_trajectory(*, masses=(1.0, 0.8, 0.6), side=1.0,
                               n_snapshots=64, n_periods=0.5,
                               offset=(0.5, -0.25, 0.1),
                               drift=(0.05, 0.02, -0.03)):
    """Build a trajectory with a constant COM offset and uniform COM drift.

    Returns ``(trajectory, offset_vec, drift_vec)``: the same Lagrange trajectory
    with ``offset + drift * t`` added to every body in the raw encoding (and
    ``drift`` added to the raw velocities), so the mass-weighted COM at the first
    snapshot equals ``offset`` (within dtype round-off) and drifts at ``drift``.
    The scaled encoding is derived from the augmented raw arrays. Plan 46-02's
    COM/boost discriminator uses this as its positive case (D-04).
    """
    trajectory = make_dual_frame_trajectory(
        masses=masses, side=side, n_snapshots=n_snapshots, n_periods=n_periods
    )
    offset_vec = np.asarray(offset, dtype=np.float64)
    drift_vec = np.asarray(drift, dtype=np.float64)
    t = trajectory.times_raw
    positions_raw = trajectory.positions_raw + offset_vec.reshape(1, 1, 3) + (
        drift_vec.reshape(1, 1, 3) * t.reshape(-1, 1, 1)
    )
    velocities_raw = trajectory.velocities_raw + drift_vec.reshape(1, 1, 3)
    D = trajectory.D
    T = trajectory.T
    offset_trajectory = DualFrameTrajectory(
        masses=trajectory.masses,
        times_raw=trajectory.times_raw,
        positions_raw=positions_raw,
        velocities_raw=velocities_raw,
        times_scaled=trajectory.times_raw / T,
        positions_scaled=positions_raw / D,
        velocities_scaled=velocities_raw * T / D,
        D=D,
        T=T,
        finite_difference_tolerance=trajectory.finite_difference_tolerance,
    )
    return offset_trajectory, offset_vec, drift_vec
