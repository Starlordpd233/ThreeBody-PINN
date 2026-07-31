"""CONF-09 frame-completion invariants (plan 47-01, task 2).

The residency swap itself is three lines. These are the assertions that prove it
was a PURE FRAME COMPLETION:

* ``test_ic13_invariance`` (D-04) — the INPUT side never moved.
* ``test_velocity_identity`` (D-02) — ``dr'/du = v_gauge`` exactly, so the
  autograd derivative and its target share one frame.
* ``test_ratified_frame_is_coherent`` (D-01/D-05) — the persisted frame constant
  describes what the adapter actually serves.
* ``test_gate_metric_near_invariance`` (D-08) — the observable relative-drift
  metric moved only within a bound DERIVED per trajectory from inputs.

Coordinate tuples (recorded explicitly, Phase 46 style — a numerically plausible
result assembled from incoherent units is the failure this milestone exists to
remove):

* OLD arm  — ``{position: r_com_ordered, time: t_native, velocity: v_com_ordered,
  masses: ordered_raw}``. The pre-CONF-09 pairing. Reconstructible from
  ``preprocess_trajectory`` output alone because D-03 keeps those fields.
* NEW arm  — ``{position: r_prime, time: u = t/T, velocity: dr_prime_du ==
  v_gauge, masses: ordered_raw}``. The locked canonical contract.

The two softenings are kept visually distinct throughout and are NEVER crossed:
the loss-side training softening is ``pinn.constants.EPS_SOFT = 1e-5``; the
validation-side invariants softening is
``pinn.verification.gate_metrics.EPS_INV = 1e-10``. Each reading below consumes
its own module's default (the full dual-epsilon defence belongs to the CONF-02
plan; see 47-CONTEXT.md D-09).

Train-free and dataset-free (SCOPE-27/28): every number here comes from stored
preprocessing output over fixture corpora.
"""

from __future__ import annotations

import math
from pathlib import Path

import numpy as np
import torch

from pinn.constants import (
    D_CHARACTERISTIC_LENGTH,
    EPS_SOFT,
    T_CHARACTERISTIC_TIME,
)
from pinn.data.adapter import (
    BRUTUS_FOLDER_TABLE,
    AdmittedSetAdapter,
    parse_brutus_file,
    record_key_from_brutus,
)
from pinn.data.preprocessing import (
    build_raw_ic13,
    compute_invariants,
    preprocess_trajectory,
)
from pinn.loss_catalog import _matched_plummer_hamiltonian
from pinn.training.validation_gate import (
    COHERENT_FRAME_PAIRS,
    MASS_CONVENTION_ORDERED_RAW,
    POSITION_FRAME_SCALED,
    RATIFIED_VALIDATION_FRAME,
    TIME_COORD_NORMALIZED,
    _validate_frame,
)
from pinn.verification.gate_metrics import (
    EPS_INV,
    finite_difference_velocity,
    matched_plummer_hamiltonian_series,
    trajectory_eps_h,
)
from tests.phase39._fixtures import TinyCorpus
from tests.phase46._fixtures import make_com_offset_trajectory

_PAIRS = ((0, 1), (0, 2), (1, 2))

# A fixed, enumerated sample of tiny-corpus records: both variants, both
# fidelities. Enumerated rather than discovered so the population never drifts.
_SAMPLED_RECORDS = (
    ("brutus_hierarchical", "hierarchical", 0),
    ("brutus_hierarchical_gold_standard", "hierarchical", 0),
    ("brutus_standard_quasi_random", "standard", 0),
)


# ---------------------------------------------------------------------------
# Fixture plumbing
# ---------------------------------------------------------------------------


def _adapter(corpus):
    return AdmittedSetAdapter(
        root=corpus.data_root,
        blacklist_path=corpus.blacklist_path,
        precision="float32",
        device="cpu",
        run_dir=corpus.run_dir,
        version_metadata_path=corpus.version_metadata_path,
    )


def _parsed(corpus, folder, variant, ident):
    path = corpus._brutus_path(folder, variant, ident)
    return parse_brutus_file(path, root=corpus.data_root)


def _corpus_records(corpus):
    """Every ``(record_key, parsed)`` pair on the tiny corpus, folder-ordered."""
    for folder, (variant, _fidelity) in sorted(BRUTUS_FOLDER_TABLE.items()):
        folder_dir = corpus.data_root / "brutus_output" / folder
        if not folder_dir.is_dir():
            continue
        for path in sorted(folder_dir.glob("*.txt")):
            key = record_key_from_brutus(folder, path.name)
            yield key, parse_brutus_file(path, root=corpus.data_root)


# ---------------------------------------------------------------------------
# The D-08 derived bound
# ---------------------------------------------------------------------------


def frame_drift_tolerance(masses_ordered, r_old, k_old_series, v_old_series,
                          h_old_series, eps, *, D, times=None,
                          fd_velocities=None):
    """Upper bound on ``|eps_h_new - eps_h_old|`` for ONE trajectory and ONE
    reading, DERIVED from inputs only.

    Every term below is an input — ``pinn.constants``, the trajectory's own
    masses and geometry, or ``numpy.finfo``. Nothing is fitted to an observed
    metric value, so SCOPE-29 / 47-CONTEXT.md D-26 are satisfied: this is a
    formula, not a threshold, and it may not be widened after observing a
    difference.

    Args:
        masses_ordered: ``(3,)`` raw ordered masses.
        r_old: ``(Nt, 3, 3)`` OLD-frame positions (COM/boost-gauged, canonically
            ordered, UNROTATED and UNSCALED) — the geometry the per-pair closest
            approach is read from.
        k_old_series: ``(Nt,)`` old-frame kinetic term ``K_old(t)``.
        v_old_series: ``(Nt,)`` old-frame softened potential ``V_old_at_eps(t)``.
        h_old_series: ``(Nt,)`` old-frame Hamiltonian ``H_old(t) = K + V``.
        eps: the READING's own softening — validation-side ``EPS_INV`` or
            loss-side ``EPS_SOFT``. The bound tightens or loosens automatically;
            no per-arm constant is ever chosen.
        D: the characteristic length, which must be the locked
            ``D_CHARACTERISTIC_LENGTH`` (Step 1 depends on it).
        times: the reading's own ``(Nt,)`` snapshot times, in the SAME units the
            divided difference used, or ``None``. Supplied ONLY by a reading that
            reconstructs velocity by finite differences (Step 5). The actual
            per-node spacings are read from this array; no uniform step is ever
            assumed.
        fd_velocities: that reading's ``(Nt, 3, 3)`` reconstructed velocity
            series, or ``None``. Supplied together with ``times``.

    Returns:
        The bound, as a float.

    Raises:
        ValueError: if the derivation's own validity precondition
            ``delta_total < abs(H_old(0))`` fails. That condition means the
            softening floor dominates the trajectory's energy and the comparison
            is meaningless — a finding to surface, never a tolerance to relax.
        ValueError: if exactly one of ``times``/``fd_velocities`` is supplied.
            Half a Step-5 input is ambiguous — it cannot be told apart from a
            stored-velocity reading, and defaulting it to zero would silently
            drop the term for a reading that needs it.

    Derivation
    ----------
    **Step 1 — the exact frame identity.** ``preprocess_trajectory``
    (``preprocessing.py:196-205``) applies an ORTHOGONAL rotation ``R0`` (so
    pairwise distances and speeds are preserved exactly), then divides positions
    by ``D`` and velocities by ``V = D/T``. ``pinn/constants.py:24,31`` locks
    ``D = cbrt(G*T**2)`` with ``G = 1``, ``T = 10`` — the PIPE-09 identity
    ``D**3 == T**2``. Therefore ``T**2/D**2 == D**3/D**2 == D``, and per
    snapshot the kinetic term satisfies ``K_new == D * K_old`` while the softened
    potential satisfies ``V_new_at_eps == -sum_ij m_i*m_j /
    sqrt((s_ij/D)**2 + eps**2) == -D * sum_ij m_i*m_j /
    sqrt(s_ij**2 + (D*eps)**2) == D * V_old_at_D_times_eps``. Hence
    ``H_new(t) == D * (K_old(t) + V_old_at_D_times_eps(t))`` EXACTLY. The uniform
    factor ``D`` cancels identically in the relative drift
    ``eps_H = max_t |(H(t)-H(0))/H(0)|``, so the two arms can differ ONLY because
    the same numeric ``eps`` behaves as an effective ``D*eps`` in old-frame
    units — exactly the softening-floor asymmetry D-08 names, now quantified.
    The identity also holds for the validation-side reading, whose velocity is a
    divided difference of positions with respect to the supplied times
    (``gate_metrics.py:84-123``): that operator is linear in positions with
    coefficients ``1/(t[k+1]-t[k-1])``, so scaling positions by ``1/D`` and times
    by ``1/T`` scales its output by ``T/D == 1/V``, exactly as the stored
    velocities scale.

    **Step 2 — the softening residual (exact inequality).** Let
    ``delta(t) = V_old_at_D_times_eps(t) - V_old_at_eps(t) >= 0``, so
    ``H_new(t)/D == H_old(t) + delta(t)``. With ``f(a) = (s**2 + a**2) ** -0.5``,
    the difference of two square roots gives ``f(eps) - f(D*eps) ==
    (D**2 - 1) * eps**2 / ( (sqrt(s**2 + D**2*eps**2) + sqrt(s**2 + eps**2)) *
    sqrt(s**2 + eps**2) * sqrt(s**2 + D**2*eps**2) )``, bounded above by
    ``(D**2 - 1) * eps**2 / (2 * s**3)``. Summing the three pairs and maximizing
    over the compared snapshots, ``delta_max = 0.5 * (D**2 - 1) * eps**2 *
    sum_over_pairs( m_i * m_j / s_ij_min**3 )``, where ``s_ij_min = min_t
    norm(r_old_i(t) - r_old_j(t))`` is that PAIR's closest approach in OLD-frame
    units — read from the trajectory's own geometry, an input, never a metric
    output.

    **Step 3 — propagation into the ratio (exact inequality).** Write
    ``a = H_old(0)``, ``e = delta(0)``, ``Delta(t) = H_old(t) - H_old(0)``,
    ``d(t) = delta(t) - delta(0)``. Then ``g_new(t) - g_old(t) ==
    (a*d(t) - Delta(t)*e) / (a * (a + e))``, and since ``|d| <= delta_total``,
    ``|e| <= delta_total`` and ``max_t |Delta|/|a| == eps_h_old``,
    ``abs(eps_h_new - eps_h_old) <= delta_total * (1 + eps_h_old) /
    (abs(a) - delta_total)``. ``eps_h_old`` enters as the propagation
    amplification factor produced by this algebra — the measured baseline whose
    error bar is being computed, exactly as a measurement uncertainty depends on
    the measurement. It is NOT a fitted quantity and does not make the bound
    output-tuned. The bound is valid only while ``delta_total < abs(a)``.

    **Step 4 — the float64 allowance, folded into ``delta_total``.** Two
    cancellations that are exact in real arithmetic are only near-exact in
    float64: (1) ``T**2/D**2 == D`` holds to a few ULP because ``D`` is formed by
    ``100.0 ** (1.0/3.0)``; (2) each ``H`` evaluation accumulates a handful of
    float64 terms. Both act as an extra ABSOLUTE perturbation of ``H_old``, so
    ``delta_round = 4*u*K_max + 8*u*(K_max + absV_max)`` with
    ``u = numpy.finfo(numpy.float64).eps / 2``, ``K_max = max_t K_old(t)``,
    ``absV_max = max_t abs(V_old_at_eps(t))``, and ``delta_round`` enters
    ``delta_total`` (whose full composition Step 5 completes) throughout Step 3.
    The literals ``4`` and ``8`` are OPERATION COUNTS (one pow, one square, one
    divide for the ``D`` identity; three pairwise potential terms, three kinetic
    terms, one sum and one ratio for the assembly) — not fudge factors, and not
    to be raised.

    **Step 5 — the finite-difference velocity cancellation allowance
    (validation-side reading ONLY).** The validation-side reading does not
    consume stored velocities; it reconstructs them as a central divided
    difference ``v[k] = (pos[k+1] - pos[k-1]) / (t[k+1] - t[k-1])``
    (``gate_metrics.py:84-123``).

    In EXACT arithmetic that operator is linear in positions and scales exactly
    as stored velocities do — which is what Step 1 already argues, and Step 1 is
    correct and unchanged. In float64 the stored position components each carry
    an ABSOLUTE representation error of order ``u * abs(r)``, and those errors do
    NOT cancel in the numerator. The reconstructed velocity therefore carries
    absolute error

        dv_i[k] <= 2*u*R_max/dt_k + 2*u*abs(v_i[k])

    with ``u = numpy.finfo(numpy.float64).eps / 2`` (the same unit round-off Step
    4 uses); ``R_max`` the maximum over snapshots, bodies and components of
    ``abs(position)``, read from the trajectory's own geometry (the same
    OLD-frame array Step 2 reads); and ``dt_k = t[k+1] - t[k-1]`` computed from
    the ACTUAL supplied times at each interior node. A single assumed uniform
    step is a DEFECT, not a simplification — Brutus sampling is not uniform —
    which is the same constraint ``test_velocity_identity`` already imposes on
    itself. The second term is the round-off of the division itself.

    The first term is the cancellation amplification: since
    ``abs(v) ~ abs(dr)/dt``, the ratio of that term to ``abs(v)`` is
    ``~ 2*u*abs(r)/abs(dr)``, i.e. the CONDITION NUMBER of the subtraction —
    exactly the quantity Step 4 omits.

    This propagates into the kinetic term ``K = 0.5 * sum_i m_i * norm(v_i)**2``
    as ``dK_k = sum_i m_i * norm(v_i[k]) * dv_i[k]``
    (``d(0.5*m*norm(v)**2) = m * dot(v, dv) <= m * norm(v) * dv``), and, being an
    absolute perturbation of ``H_old``, enters exactly where ``delta_round``
    does:

        delta_fd    = max over interior k of ( sum_i m_i*norm(v_i[k])*dv_i[k] )
        delta_total = delta_max + delta_round + delta_fd

    Every quantity is an INPUT — masses, positions, the supplied times, the
    reading's own reconstructed velocity series, and ``numpy.finfo``. No observed
    metric value enters, and the term evaluates identically regardless of what
    the comparison shows; that is why it is admissible under SCOPE-29 /
    47-CONTEXT.md D-26 and is an EXTENSION of the derivation rather than a
    widening of it (Step 4's counts ``4`` and ``8`` are untouched).

    ``delta_fd`` is ZERO for the loss-side reading, which consumes stored
    velocities and performs no differencing.
    """
    masses = np.asarray(masses_ordered, dtype=np.float64).reshape(3)
    positions = np.asarray(r_old, dtype=np.float64)
    kinetic = np.asarray(k_old_series, dtype=np.float64).reshape(-1)
    potential = np.asarray(v_old_series, dtype=np.float64).reshape(-1)
    hamiltonian = np.asarray(h_old_series, dtype=np.float64).reshape(-1)
    eps = float(eps)
    D = float(D)

    # Step 1's identity T**2/D**2 == D is the locked PIPE-09 relation; it is not
    # true for an arbitrary D, so an unlocked D invalidates the whole bound.
    if D != float(D_CHARACTERISTIC_LENGTH):
        raise ValueError(
            "the Step-1 frame identity T**2/D**2 == D rests on the locked PIPE-09 "
            f"relation D**3 == T**2; got D={D!r}, locked "
            f"D_CHARACTERISTIC_LENGTH={float(D_CHARACTERISTIC_LENGTH)!r}"
        )

    # Step 2: per-pair closest approach in OLD-frame (raw, COM-gauged, unscaled)
    # units, read from the trajectory's own geometry.
    pair_sum = 0.0
    for i, j in _PAIRS:
        separation = np.linalg.norm(positions[:, i, :] - positions[:, j, :], axis=-1)
        s_min = float(np.min(separation))
        if not math.isfinite(s_min) or s_min <= 0.0:
            raise ValueError(
                f"pair ({i},{j}) closest approach is {s_min!r}; the softening "
                "residual bound needs a finite positive separation"
            )
        pair_sum += float(masses[i]) * float(masses[j]) / s_min ** 3
    delta_max = 0.5 * (D ** 2 - 1.0) * eps ** 2 * pair_sum

    # Step 4: the float64 allowance (unit round-off u, operation counts 4 and 8).
    unit_roundoff = float(np.finfo(np.float64).eps) / 2.0
    k_max = float(np.max(np.abs(kinetic)))
    abs_v_max = float(np.max(np.abs(potential)))
    delta_round = 4.0 * unit_roundoff * k_max + 8.0 * unit_roundoff * (k_max + abs_v_max)

    # Step 5: the finite-difference cancellation allowance. BOTH inputs or
    # NEITHER — half of them cannot be distinguished from a stored-velocity
    # reading, and silently pricing the term at zero for a differencing reading
    # is the exact failure this remediation exists to remove.
    if (times is None) != (fd_velocities is None):
        raise ValueError(
            "Step 5 needs BOTH `times` and `fd_velocities` or NEITHER; got "
            f"times={'None' if times is None else 'supplied'}, "
            f"fd_velocities={'None' if fd_velocities is None else 'supplied'}. "
            "A reading that reconstructs velocity by divided differences must "
            "supply both; a reading that consumes stored velocities supplies "
            "neither"
        )
    if times is None:
        delta_fd = 0.0
    else:
        delta_fd = _finite_difference_energy_allowance(
            masses, positions, times, fd_velocities, unit_roundoff
        )

    delta_total = delta_max + delta_round + delta_fd

    # Step 3: propagation into the relative-drift ratio.
    a = float(hamiltonian[0])
    if not math.isfinite(a) or a == 0.0:
        raise ValueError(f"H_old(0) must be finite and non-zero; got {a!r}")
    eps_h_old = float(np.max(np.abs((hamiltonian - a) / a)))
    if not delta_total < abs(a):
        raise ValueError(
            "frame-drift bound precondition violated: the softening floor "
            f"dominates the trajectory energy (delta_total={delta_total!r} >= "
            f"|H_old(0)|={abs(a)!r}); the before/after comparison is meaningless "
            "for this trajectory and this is a finding to surface, not a "
            "tolerance to relax"
        )
    return delta_total * (1.0 + eps_h_old) / (abs(a) - delta_total)


def _finite_difference_energy_allowance(masses, positions, times, fd_velocities,
                                        unit_roundoff):
    """Step 5's ``delta_fd`` — the divided difference's cancellation allowance.

    ``delta_fd = max over interior k of ( sum_i m_i*norm(v_i[k])*dv_i[k] )`` with
    ``dv_i[k] = 2*u*R_max/dt_k + 2*u*norm(v_i[k])``. Interior nodes only: those
    are the nodes ``gate_metrics.finite_difference_velocity`` fills with the
    CENTRED stencil, and ``dt_k = t[k+1] - t[k-1]`` is that stencil's own
    denominator (``gate_metrics.py:120-121``), read per node from the ACTUAL
    supplied times.

    ``abs(v_i[k])`` is read as the body-``i`` speed ``norm(v_i[k])``, the same
    per-body magnitude the ``dK`` expression uses — the larger of the two
    readings the notation admits, so the allowance is never understated.

    All arguments are already-coerced float64 inputs from
    :func:`frame_drift_tolerance`; nothing here is fitted to an observed metric.
    """
    t = np.asarray(times, dtype=np.float64).reshape(-1)
    velocities = np.asarray(fd_velocities, dtype=np.float64)
    n_snapshots = int(positions.shape[0])
    if t.shape[0] != n_snapshots:
        raise ValueError(
            f"times has {t.shape[0]} entries but the trajectory has "
            f"{n_snapshots} snapshots"
        )
    if velocities.shape != positions.shape:
        raise ValueError(
            f"fd_velocities shape {velocities.shape} must match the position "
            f"array shape {positions.shape}"
        )
    if n_snapshots < 3:
        raise ValueError(
            "the Step-5 allowance is defined on the CENTRED stencil's interior "
            f"nodes, and a {n_snapshots}-snapshot series has none; every "
            "velocity would then be a one-sided difference this term does not "
            "cover — a finding to surface, not a term to zero out"
        )

    # dt_k = t[k+1] - t[k-1], per interior node. No uniform step is assumed.
    dt = t[2:] - t[:-2]
    if not np.all(np.isfinite(dt)) or not np.all(dt > 0.0):
        raise ValueError(
            "the centred-stencil denominators t[k+1]-t[k-1] must be finite and "
            "positive; times must be strictly increasing"
        )

    r_max = float(np.max(np.abs(positions)))
    if not math.isfinite(r_max):
        raise ValueError(f"R_max must be finite; got {r_max!r}")

    speed = np.linalg.norm(velocities[1:-1], axis=-1)          # (Ni, 3)
    dv = 2.0 * unit_roundoff * r_max / dt[:, None] + 2.0 * unit_roundoff * speed
    d_kinetic = (masses.reshape(1, 3) * speed * dv).sum(axis=-1)
    return float(np.max(d_kinetic))


# ---------------------------------------------------------------------------
# Dual-arm gate-metric computation (shared with the plan's task-3 D-23 record)
# ---------------------------------------------------------------------------


def _kinetic_series(masses_ordered, velocities):
    """``K(t) = 0.5 * sum_i m_i * ||v_i||^2`` in float64.

    No softening enters the kinetic term, so this is not a second
    implementation of the softened-potential loop (which stays single-homed in
    ``loss_catalog`` / ``gate_metrics``). The potential series is then recovered
    as ``H - K`` rather than re-summed here.
    """
    m = np.asarray(masses_ordered, dtype=np.float64).reshape(3)
    v = np.asarray(velocities, dtype=np.float64)
    return 0.5 * (m.reshape(1, 3) * (v ** 2).sum(axis=-1)).sum(axis=-1)


def _loss_side_hamiltonian(positions, velocities, masses_ordered):
    """Loss-side ``H(t)`` at the TRAINING softening ``EPS_SOFT = 1e-5``.

    Coordinate tuple is the caller's; this helper never mixes frames. Uses the
    loss module's own default softening and never the validation-side
    ``EPS_INV``.
    """
    series = _matched_plummer_hamiltonian(
        np.asarray(positions, dtype=np.float64),
        np.asarray(velocities, dtype=np.float64),
        np.asarray(masses_ordered, dtype=np.float64),
        dtype=torch.float64,
        device=torch.device("cpu"),
    )
    return series.detach().cpu().numpy().astype(np.float64)


def dual_arm_frame_comparison(pre, times):
    """The D-08 before/after comparison for ONE trajectory, BOTH readings.

    ``pre`` is a ``PreprocessedTrajectory``; ``times`` the native snapshot times.
    Returns ``{reading: {...}}`` for ``"validation"`` (``gate_metrics`` at
    ``EPS_INV``) and ``"loss"`` (``_matched_plummer_hamiltonian`` at
    ``EPS_SOFT``), each carrying ``eps_h_old``, ``eps_h_new``, ``difference`` and
    the per-trajectory ``bound`` that ``frame_drift_tolerance`` returns.

    OLD arm ``{position: r_com_ordered, time: t_native, velocity: v_com_ordered,
    masses: ordered_raw}``; NEW arm ``{position: r_prime, time: u = t/T,
    velocity: dr_prime_du, masses: ordered_raw}``.
    """
    times_native = np.asarray(times, dtype=np.float64)
    times_normalized = times_native / float(pre.T)
    positions_old = np.asarray(pre.r_com_ordered, dtype=np.float64)
    positions_new = np.asarray(pre.r_gauge, dtype=np.float64)
    masses = np.asarray(pre.masses_ordered, dtype=np.float64)

    results = {}

    # -- validation-side reading: gate_metrics at EPS_INV (1e-10) --------------
    fd_velocity_old = finite_difference_velocity(
        positions_old, times_native
    ).cpu().numpy()
    h_old = matched_plummer_hamiltonian_series(
        positions_old, fd_velocity_old, masses
    ).cpu().numpy()
    fd_velocity_new = finite_difference_velocity(
        positions_new, times_normalized
    ).cpu().numpy()
    h_new = matched_plummer_hamiltonian_series(
        positions_new, fd_velocity_new, masses
    ).cpu().numpy()
    k_old = _kinetic_series(masses, fd_velocity_old)
    # This reading RECONSTRUCTS velocity by divided differences, so it carries
    # Step 5's cancellation allowance and supplies both of its inputs: the OLD
    # arm's own native times and its own reconstructed series.
    results["validation"] = _arm_record(
        masses, positions_old, k_old, h_old, h_new, EPS_INV, pre.D,
        times=times_native, fd_velocities=fd_velocity_old,
    )

    # -- loss-side reading: _matched_plummer_hamiltonian at EPS_SOFT (1e-5) ----
    velocities_old = np.asarray(pre.v_com_ordered, dtype=np.float64)
    velocities_new = np.asarray(pre.v_gauge, dtype=np.float64)
    h_old_loss = _loss_side_hamiltonian(positions_old, velocities_old, masses)
    h_new_loss = _loss_side_hamiltonian(positions_new, velocities_new, masses)
    k_old_loss = _kinetic_series(masses, velocities_old)
    # This reading CONSUMES stored velocities — no differencing, so Step 5's
    # allowance is zero and NEITHER of its inputs is supplied.
    results["loss"] = _arm_record(
        masses, positions_old, k_old_loss, h_old_loss, h_new_loss, EPS_SOFT, pre.D
    )
    return results


def _arm_record(masses, positions_old, k_old, h_old, h_new, eps, D, *,
                times=None, fd_velocities=None):
    """Assemble one reading's before/after record plus its derived bound.

    ``times``/``fd_velocities`` are forwarded verbatim to
    :func:`frame_drift_tolerance`: both for a divided-difference reading, neither
    for a stored-velocity reading (Step 5).
    """
    # V_old_at_eps == H_old - K_old: recovered by subtraction so the softened
    # pairwise sum keeps exactly one home (47-CONTEXT.md D-09/D-11).
    v_old = h_old - k_old
    eps_h_old = trajectory_eps_h(torch.as_tensor(h_old))
    eps_h_new = trajectory_eps_h(torch.as_tensor(h_new))
    bound = frame_drift_tolerance(
        masses, positions_old, k_old, v_old, h_old, eps, D=float(D),
        times=times, fd_velocities=fd_velocities,
    )
    return {
        "eps_h_old": float(eps_h_old),
        "eps_h_new": float(eps_h_new),
        "difference": abs(float(eps_h_new) - float(eps_h_old)),
        "bound": float(bound),
        "eps": float(eps),
    }


# ---------------------------------------------------------------------------
# Analytic scaled-frame acceleration / jerk (velocity-identity tolerance)
# ---------------------------------------------------------------------------


def _softened_accel_and_jerk(positions, velocities, masses_ordered, eps):
    """Closed-form softened-Newtonian acceleration and jerk in the SCALED frame.

    ``accel_i = sum_{j != i} m_j (r_j - r_i) / r_safe_ij**3`` and
    ``jerk_i = sum_{j != i} m_j ( (v_j - v_i)/r_safe_ij**3 - 3 (r_j - r_i) *
    dot(r_j - r_i, v_j - v_i) / r_safe_ij**5 )`` with
    ``r_safe_ij = sqrt(norm(r_j - r_i)**2 + eps**2)``. Coordinate tuple:
    ``{position: r_prime, time: u, velocity: dr_prime_du, masses: ordered_raw}``
    — the scaled frame keeps the same equation of motion because ``G = 1`` and
    ``D**3 == T**2``.

    ``eps`` is the TRAINING softening ``EPS_SOFT``, never the validation-side
    ``EPS_INV``.
    """
    r = np.asarray(positions, dtype=np.float64)
    v = np.asarray(velocities, dtype=np.float64)
    m = np.asarray(masses_ordered, dtype=np.float64).reshape(3)
    eps_sq = float(eps) ** 2
    accel = np.zeros_like(r)
    jerk = np.zeros_like(r)
    for i in range(3):
        for j in range(3):
            if i == j:
                continue
            dr = r[:, j, :] - r[:, i, :]
            dv = v[:, j, :] - v[:, i, :]
            r_safe = np.sqrt((dr ** 2).sum(axis=-1) + eps_sq)
            inv3 = 1.0 / r_safe ** 3
            inv5 = 1.0 / r_safe ** 5
            dot = (dr * dv).sum(axis=-1)
            accel[:, i, :] += m[j] * dr * inv3[:, None]
            jerk[:, i, :] += m[j] * (
                dv * inv3[:, None] - 3.0 * dr * (dot * inv5)[:, None]
            )
    return accel, jerk


# ---------------------------------------------------------------------------
# D-04: IC13 / E invariance
# ---------------------------------------------------------------------------


def test_ic13_invariance():
    """The swap left the INPUT side untouched (47-CONTEXT.md D-04).

    ``preprocessing.py:217-219`` sets ``r0_gauge = r_scaled[0]`` alongside
    ``r_gauge = r_scaled``, so ``pre.r_gauge[0]`` IS ``pre.r0_gauge``
    elementwise — the identity that makes IC₁₃ invariance a checkable assertion
    rather than a hope. ``adapter.py`` builds ``raw_ic13``/``E`` from
    ``r0_gauge``/``v0_gauge``, which the swap never touched, so recomputing both
    independently from the preprocessing output must reproduce what the adapter
    stored.

    Coordinate tuple: ``{position: r_prime[0] == r0_gauge, time: n/a,
    velocity: v_gauge[0] == v0_gauge, masses: ordered_raw}``.
    """
    with TinyCorpus() as corpus:
        adapter = _adapter(corpus)
        admitted = set(adapter.record_keys())
        assert admitted, "tiny corpus admitted nothing; fixture is broken"

        checked = 0
        for key, parsed in _corpus_records(corpus):
            if key not in admitted:
                continue
            pre = preprocess_trajectory(
                parsed.times, parsed.positions, parsed.velocities, parsed.masses
            )

            # The identity the whole invariance argument rests on: exact, because
            # one array assignment produces both sides.
            np.testing.assert_array_equal(pre.r_gauge[0], pre.r0_gauge)
            np.testing.assert_array_equal(pre.v_gauge[0], pre.v0_gauge)

            # Independent recomputation of the stored inputs from r0/v0_gauge.
            invariants = compute_invariants(
                pre.masses_ordered, pre.r0_gauge, pre.v0_gauge
            )
            raw_ic13 = build_raw_ic13(
                pre.masses_ordered, pre.r0_gauge, pre.v0_gauge, invariants.E
            )

            record = adapter.get(key)
            np.testing.assert_array_equal(
                record.raw_ic13.cpu().numpy(),
                np.asarray(raw_ic13, dtype=np.float64).astype(np.float32),
            )
            assert float(record.E) == float(invariants.E), key
            checked += 1

        assert checked == len(admitted), (
            f"checked {checked} of {len(admitted)} admitted records"
        )


# ---------------------------------------------------------------------------
# D-02: the velocity identity dr'/du = v_gauge
# ---------------------------------------------------------------------------


def test_velocity_identity():
    """``dr'/du == v_gauge``, so the AD derivative and its target share one frame.

    Two independent statements.

    (i) EXACT ALGEBRAIC IDENTITY. ``v_gauge`` is the rotation-gauged COM-frame
    velocity divided by ``V = D/T``, the value recorded on
    ``PreprocessedTrajectory``; and the resident velocity series is exactly the
    fp32 cast of ``v_gauge``. (The RESIDENT PAIRING ORACLE is not duplicated
    here — it lives corrected-in-place in
    ``tests/phase46/test_pairing_repair.py`` per D-06. This is the first link of
    the frame-identity chain, stated from a single shared
    ``preprocess_trajectory`` call, not a second oracle.)

    (ii) NUMERIC SANITY on a force-consistent trajectory. A finite difference of
    ``r_gauge`` with respect to ``u = t/T`` reproduces ``v_gauge`` at interior
    snapshots within a tolerance computed from the ACTUAL per-interval spacings
    and the analytic scaled-frame jerk. Brutus sampling is not guaranteed
    uniform, so no single ``Δu`` is ever assumed: ``h_minus``/``h_plus`` are read
    per interior node from the ``u`` array itself, and the check is run on a
    deliberately NON-UNIFORM subsample as well as the full grid.

    Fixture choice. (ii) uses the closed-form Lagrange fixture from
    ``tests/phase46/_fixtures.py`` rather than ``TinyCorpus``: the tiny corpus's
    synthetic body lines carry velocities that are NOT the time derivative of
    their positions (``tests/phase39/_fixtures.py::_body_line``), so a
    finite-difference identity there would measure the fixture's own kinematic
    inconsistency instead of the frame transform. The Lagrange trajectory is an
    exact Newtonian solution, so ``v == dr/dt`` holds to float64 round-off and
    the assertion measures what it claims to.

    Coordinate tuple: ``{position: r_prime, time: u = t/T,
    velocity: dr_prime_du, masses: ordered_raw}``.
    """
    trajectory, _offset, _drift = make_com_offset_trajectory(n_snapshots=64)

    # -- (i) exact algebraic identity -------------------------------------
    with TinyCorpus() as corpus:
        adapter = _adapter(corpus)
        folder, variant, ident = _SAMPLED_RECORDS[0]
        parsed = _parsed(corpus, folder, variant, ident)
        key = record_key_from_brutus(
            folder, corpus._brutus_path(folder, variant, ident).name
        )
        pre = preprocess_trajectory(
            parsed.times, parsed.positions, parsed.velocities, parsed.masses
        )
        np.testing.assert_array_equal(
            adapter.snapshot_velocities(key).cpu().numpy(),
            np.asarray(pre.v_gauge, dtype=np.float64).astype(np.float32),
        )

        # v_gauge * V reproduces the rotation-gauged COM-frame velocities.
        # DERIVED float64 tolerance: the two sides differ only by the rounding of
        # a rotate (one dot product per component), one divide by V and one
        # multiply back — bounded by a handful of unit round-offs at the array's
        # own scale.
        rotated = np.asarray(pre.v_com_ordered, dtype=np.float64) @ np.asarray(
            pre.R0, dtype=np.float64
        ).T
        scale = float(np.max(np.abs(rotated)))
        algebraic_tolerance = 16.0 * float(np.finfo(np.float64).eps) * scale
        assert np.max(
            np.abs(np.asarray(pre.v_gauge, dtype=np.float64) * float(pre.V) - rotated)
        ) <= algebraic_tolerance
        assert float(pre.V) == float(pre.D) / float(pre.T)
        assert float(pre.D) == float(D_CHARACTERISTIC_LENGTH)
        assert float(pre.T) == float(T_CHARACTERISTIC_TIME)

    # -- (ii) numeric sanity, uniform AND non-uniform sampling ------------
    # Deliberately irregular index stride: consecutive gaps of 1, 2, 3, 4 make
    # h_plus != h_minus at every interior node, so a tolerance that assumed a
    # single Δu would be caught here.
    non_uniform = np.array(
        sorted({0, 1, 3, 6, 10, 15, 21, 28, 36, 45, 55, 63}), dtype=np.int64
    )
    for label, index in (("uniform", np.arange(64)), ("non-uniform", non_uniform)):
        _assert_velocity_identity_on(trajectory, index, label)


def _assert_velocity_identity_on(trajectory, index, label):
    """Run the (ii) finite-difference identity over one snapshot selection."""
    times = np.asarray(trajectory.times_raw, dtype=np.float64)[index]
    positions = np.asarray(trajectory.positions_raw, dtype=np.float64)[index]
    velocities = np.asarray(trajectory.velocities_raw, dtype=np.float64)[index]
    pre = preprocess_trajectory(times, positions, velocities, trajectory.masses)

    u = times / float(pre.T)
    r_gauge = np.asarray(pre.r_gauge, dtype=np.float64)
    v_gauge = np.asarray(pre.v_gauge, dtype=np.float64)

    # numpy.gradient fits a quadratic through each interior triple and is
    # second-order accurate on UNEQUAL spacings; its interior truncation error is
    # -(1/6) * h_minus * h_plus * f'''(xi).
    derivative = np.gradient(r_gauge, u, axis=0)

    h_minus = u[1:-1] - u[:-2]
    h_plus = u[2:] - u[1:-1]
    assert np.all(h_minus > 0.0) and np.all(h_plus > 0.0)
    if label == "non-uniform":
        assert np.any(np.abs(h_plus - h_minus) > 0.0), (
            "the non-uniform selection collapsed to an equal-spacing grid"
        )

    # The truncation theorem evaluates f''' at an unknown point in the stencil,
    # so a node-k evaluation is only rigorous when |f'''| does not exceed its
    # node-k magnitude inside the stencil. That holds here by construction: the
    # fixture is a rigid rotation (plus a zero-jerk COM drift), so ||f'''|| is
    # constant along the trajectory, and the per-component error is bounded by
    # the VECTOR norm used below. Expect the ratio to approach — never exceed —
    # 1, because for a sinusoid the exact error is the leading term times
    # (1 - (omega*h)**2/20 + ...).
    _accel, jerk = _softened_accel_and_jerk(
        r_gauge, v_gauge, pre.masses_ordered, EPS_SOFT
    )
    jerk_norm = np.linalg.norm(jerk[1:-1], axis=-1).max(axis=-1)

    # Round-off floor: the divided difference divides an O(max|r'|) subtraction
    # by the local spacing, so absolute round-off scales as
    # (operation count) * u64 * max|r'| / min(h_minus, h_plus). The count 4 is
    # the three-term quadratic stencil plus its division.
    roundoff = (
        4.0
        * float(np.finfo(np.float64).eps)
        * float(np.max(np.abs(r_gauge)))
        / np.minimum(h_minus, h_plus)
    )
    tolerance = (1.0 / 6.0) * h_plus * h_minus * jerk_norm + roundoff

    residual = np.abs(derivative[1:-1] - v_gauge[1:-1]).max(axis=-1).max(axis=-1)
    assert np.all(residual <= tolerance), (
        f"{label}: interior dr'/du deviates from v_gauge beyond the derived "
        f"per-node bound; worst ratio={float(np.max(residual / tolerance))!r}"
    )
    # Endpoints use one-sided differences and are excluded by construction.


# ---------------------------------------------------------------------------
# D-01/D-05: the ratified frame describes what the adapter serves
# ---------------------------------------------------------------------------


def test_ratified_frame_is_coherent():
    """``RATIFIED_VALIDATION_FRAME`` is the scaled triple and is admitted.

    A constant that does not track residency makes ``COHERENT_FRAME_PAIRS`` lie,
    which is why the swap and this re-ratification are one commit (D-05).
    """
    frame = RATIFIED_VALIDATION_FRAME
    assert frame.position_frame == POSITION_FRAME_SCALED
    assert frame.time_coord == TIME_COORD_NORMALIZED
    assert frame.mass_convention == MASS_CONVENTION_ORDERED_RAW
    assert (frame.position_frame, frame.time_coord) in COHERENT_FRAME_PAIRS

    # The dict form the sidecar/gate path validates.
    _validate_frame(
        {
            "position_frame": frame.position_frame,
            "time_coord": frame.time_coord,
            "mass_convention": frame.mass_convention,
            "conf01_evidence_ref": frame.conf01_evidence_ref,
        }
    )

    evidence = Path(frame.conf01_evidence_ref)
    assert evidence.is_file(), frame.conf01_evidence_ref
    assert evidence.parts[:3] == (
        ".planning",
        "phases",
        "47-frame-completion-s-h-pipeline",
    ), frame.conf01_evidence_ref
    assert "GAP-46-07" in evidence.read_text(encoding="utf-8")


# ---------------------------------------------------------------------------
# D-08: approximate gate-metric invariance within the derived bound
# ---------------------------------------------------------------------------


def test_gate_metric_near_invariance():
    """The observable relative drift moved only within the DERIVED bound.

    ``eps_H = max_t |(H(t)-H(0))/H(0)|`` is computed under BOTH pairings — the
    old ``(r_com_ordered, v_com_ordered, t_native)`` (reconstructible because
    D-03 keeps those fields) and the new ``(r_gauge, v_gauge, u = t/T)`` — for
    BOTH readings: validation-side ``gate_metrics`` at ``EPS_INV`` and loss-side
    ``_matched_plummer_hamiltonian`` at ``EPS_SOFT``.

    EXACT equality is never asserted: the same numeric ``eps`` acts as an
    effective ``D*eps`` in old-frame units, so the ``r_safe`` floor contributes
    differently in the two frames and exact equality would FAIL for a correct
    implementation (D-08). The comparison bound is
    ``frame_drift_tolerance(...)``, computed per trajectory and per reading from
    inputs only — never a hand-chosen constant, never widened after observing a
    difference (SCOPE-29 / D-26).
    """
    with TinyCorpus() as corpus:
        for folder, variant, ident in _SAMPLED_RECORDS:
            parsed = _parsed(corpus, folder, variant, ident)
            pre = preprocess_trajectory(
                parsed.times, parsed.positions, parsed.velocities, parsed.masses
            )
            comparison = dual_arm_frame_comparison(pre, parsed.times)
            assert set(comparison) == {"validation", "loss"}
            for reading, record in comparison.items():
                assert math.isfinite(record["eps_h_old"]), (folder, ident, reading)
                assert math.isfinite(record["eps_h_new"]), (folder, ident, reading)
                assert record["bound"] > 0.0
                assert record["difference"] <= record["bound"], (
                    f"{folder}/{ident} {reading}: |eps_h_new - eps_h_old| = "
                    f"{record['difference']!r} exceeds the derived bound "
                    f"{record['bound']!r}"
                )
