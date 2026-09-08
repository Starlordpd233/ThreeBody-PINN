"""Phase 38 / NET-04 — locked five-term loss catalog with supplied-weights composer.

Rebuilt from ``pinn_architecture.md`` §3.1–§3.5 and ``ctl_instruction.md``
Phase 2 total loss. The catalog is the loss the overfit rung (38-06) drives and
the object Phase 40's scheduler and Phase 42's logging later consume unchanged.

Terms (exactly five; no linear-momentum term — linear momentum is structural
via the COM projection head, §4.1)::

    L_data        §3.1  Huber(delta_r=1) on COM-projected scaled positions r'
    L_IC          §3.3  squared-error anchors at u=0 (tau=-1), beta_v=1
    L_phys_causal §3.2  causally-weighted residual energy, eta_c=1, stopgrad
    L_E           §3.4  soft-energy Huber on relative Hamiltonian drift
    L_L           §3.5  componentwise angular-momentum Huber

Composer: pure function of a SUPPLIED five-field ``LossWeights`` vector —
no scheduling/warmup (Phase 40 / TRAIN-03). ``lambda_data`` is fixed at 1.0
(§3.1 unweighted data term) and enforced at construction.

Precision/device discipline (CTX-14 / ENV-04): every callable takes explicit
``dtype``/``device``; scalar constants are wrapped as same-dtype/device tensors.
No ``torch.set_default_dtype``, no availability probe, no v1.3-era import.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Mapping

import torch

from pinn.constants import (
    CAUSAL_ETA_C,
    CAUSAL_W1,
    D_CHARACTERISTIC_LENGTH,
    EPS_L,
    EPS_SOFT,
    HUBER_DELTA_ANGMOM,
    HUBER_DELTA_DATA,
    HUBER_DELTA_ENERGY,
)

__all__ = [
    "CAUSAL_CLIP_FIELD_NAMES",
    "CAUSAL_CLIP_FORMULA",
    "CAUSAL_CLIP_PROVENANCE",
    "LossWeights",
    "LossTerms",
    "data_huber_loss",
    "ic_anchor_loss",
    "causal_physics_loss",
    "resolve_causal_clip_facts",
    "soft_energy_loss",
    "angular_momentum_loss",
    "compose_total",
    "D_CHARACTERISTIC_LENGTH",
]

_N_BODIES = 3
_N_DIMS = 3

# These identifiers are part of the strict run-record contract.  Keep their
# spelling and provenance in this module so loss execution, setup, and the
# metadata validator cannot silently publish different meanings.
CAUSAL_CLIP_FIELD_NAMES = (
    "causal_clip_precision",
    "causal_clip_exponent_floor",
    "causal_clip_min_weight",
    "causal_clip_formula",
    "causal_clip_provenance",
)
CAUSAL_CLIP_FORMULA = "exp(clamp_min(x_n, causal_clip_exponent_floor))"
CAUSAL_CLIP_PROVENANCE = "log_smallest_normal:directed_up"

# Phase 56 contract (SPEC-01/SPEC-06; 54-RULING.md "Batch allocation and bin
# policy"): the ratified M=16 fixed-bin structure. A length check against
# this fires only when a caller EXPLICITLY supplies ``r_ref`` (see
# ``_R_REF_UNSET`` below) -- a caller relying on the identity default keeps
# operating on whatever length it always has (e.g. Phase 55's
# architecture_characterization_probe.measure_case, whose n_col is a
# configurable sweep parameter, not fixed at 16).
_RATIFIED_M_BINS = 16

# Sentinel distinguishing "caller did not pass r_ref" from "caller passed
# r_ref=1.0" -- both must reach a defined, finite-positive r_ref_value, but
# only the former is exempt from the M=16 length check below.
_R_REF_UNSET = object()


def resolve_causal_clip_facts(dtype, device) -> dict[str, object]:
    """Derive the causal exponent floor for one active dtype/backend.

    ``log(torch.finfo(dtype).tiny)`` is a mathematical bound.  It is first
    represented in the active dtype/device and, if that rounding is below the
    mathematical value, advanced exactly once with ``nextafter`` toward
    positive infinity.  The returned Python scalars are the same facts used by
    :func:`causal_physics_loss` and persisted in ``training_metadata.json``.
    """
    if dtype is torch.float32:
        precision = "float32"
    elif dtype is torch.float64:
        precision = "float64"
    else:
        raise ValueError(
            "causal clip facts require torch.float32 or torch.float64; "
            f"got {dtype!r}"
        )

    active_device = torch.device(device)
    mathematical_floor = math.log(torch.finfo(dtype).tiny)
    floor_tensor = torch.as_tensor(
        mathematical_floor, dtype=dtype, device=active_device,
    )
    floor_value = float(floor_tensor.detach().cpu())
    if floor_value < mathematical_floor:
        floor_tensor = torch.nextafter(
            floor_tensor,
            torch.as_tensor(math.inf, dtype=dtype, device=active_device),
        )
        floor_value = float(floor_tensor.detach().cpu())
    min_weight = float(torch.exp(floor_tensor).detach().cpu())
    return {
        "causal_clip_precision": precision,
        "causal_clip_exponent_floor": floor_value,
        "causal_clip_min_weight": min_weight,
        "causal_clip_formula": CAUSAL_CLIP_FORMULA,
        "causal_clip_provenance": CAUSAL_CLIP_PROVENANCE,
    }


# ---------------------------------------------------------------------------
# Supplied weights + result container
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class LossWeights:
    """Five-field named λ container matching Phase 40's PHYS-05 weight vector.

    ``lambda_data`` is FIXED at 1.0 by §3.1 (data term unweighted). Construction
    rejects any negative/NaN weight and any ``lambda_data != 1.0``.
    """

    lambda_data: float = 1.0
    lambda_ic: float = 1.0
    lambda_phys: float = 1.0
    lambda_e: float = 1.0
    lambda_l: float = 1.0

    def __post_init__(self) -> None:
        fields = (
            ("lambda_data", self.lambda_data),
            ("lambda_ic", self.lambda_ic),
            ("lambda_phys", self.lambda_phys),
            ("lambda_e", self.lambda_e),
            ("lambda_l", self.lambda_l),
        )
        for name, value in fields:
            try:
                finite = math.isfinite(float(value))
            except (TypeError, ValueError):
                finite = False
            if not finite or float(value) < 0.0:
                raise ValueError(
                    f"LossWeights.{name} must be finite and non-negative; "
                    f"got {value!r} (a negative lambda silently flips the term "
                    f"into gradient ascent)"
                )
        if float(self.lambda_data) != 1.0:
            raise ValueError(
                f"LossWeights.lambda_data must be 1.0 (pinn_architecture.md §3.1 "
                f"unweighted data term); got {self.lambda_data!r}"
            )


@dataclass(frozen=True)
class LossTerms:
    """Per-term scalars + weighted total — Phase 42 OPS-03 logging surface."""

    data: torch.Tensor
    ic: torch.Tensor
    phys: torch.Tensor
    energy: torch.Tensor
    angmom: torch.Tensor
    total: torch.Tensor


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _huber(diff: torch.Tensor, delta: float, *, dtype, device) -> torch.Tensor:
    """Elementwise Huber (smooth L1) matching torch.nn.functional.huber_loss."""
    delta_t = torch.as_tensor(delta, dtype=dtype, device=device)
    abs_diff = diff.abs()
    quadratic = torch.as_tensor(0.5, dtype=dtype, device=device) * diff * diff
    linear = delta_t * (abs_diff - torch.as_tensor(0.5, dtype=dtype, device=device) * delta_t)
    return torch.where(abs_diff <= delta_t, quadratic, linear)


def _as_positions(positions, *, dtype, device) -> torch.Tensor:
    p = torch.as_tensor(positions, dtype=dtype, device=device)
    if p.dim() == 2 and p.shape == (_N_BODIES, _N_DIMS):
        p = p.unsqueeze(0)
    if p.shape[-2:] != (_N_BODIES, _N_DIMS):
        raise ValueError(
            f"positions must be (N_t, 3, 3) or (3, 3); got shape {tuple(p.shape)}"
        )
    return p


def _matched_plummer_components(positions, velocities, masses, *, dtype, device,
                                eps_soft=EPS_SOFT) -> tuple[torch.Tensor, torch.Tensor]:
    """Matched-Plummer (T', V_eps) component pair per snapshot; returns ((N_t,), (N_t,)).

    The ONE home of the softened pairwise sum (CONF-02 / D-11): the §3.4 S_H
    admission capture and the L_E Hamiltonian both read their components from
    here, so the two consumers can never drift apart on the softening.
    ``potential`` is the signed Plummer potential (strictly negative); callers
    needing ``Uabs = -V_eps`` take ``abs`` themselves.
    """
    p = _as_positions(positions, dtype=dtype, device=device)
    v = _as_positions(velocities, dtype=dtype, device=device)
    m = torch.as_tensor(masses, dtype=dtype, device=device)
    # Kinetic: T' = (1/2) sum_i m_i ||v'_i||^2
    speed_sq = (v * v).sum(dim=-1)  # (N_t, 3)
    kinetic = torch.as_tensor(0.5, dtype=dtype, device=device) * (m * speed_sq).sum(dim=-1)
    # Potential: V_eps = -sum_{i<j} m_i m_j / r_safe
    eps = torch.as_tensor(eps_soft, dtype=dtype, device=device)
    potential = torch.zeros(p.shape[0], dtype=dtype, device=device)
    for i in range(_N_BODIES):
        for j in range(i + 1, _N_BODIES):
            delta = p[:, j] - p[:, i]
            r_safe = torch.sqrt((delta * delta).sum(dim=-1) + eps * eps)
            potential = potential - (m[i] * m[j] / r_safe)
    return kinetic, potential


def _matched_plummer_hamiltonian(positions, velocities, masses, *, dtype, device,
                                 eps_soft=EPS_SOFT) -> torch.Tensor:
    """Matched-Plummer H_eps = T' + V_eps per snapshot; returns (N_t,)."""
    kinetic, potential = _matched_plummer_components(
        positions, velocities, masses, dtype=dtype, device=device, eps_soft=eps_soft)
    return kinetic + potential


def _angular_momentum(positions, velocities, masses, *, dtype, device) -> torch.Tensor:
    """L' = sum_i m_i (r'_i × v'_i); returns (N_t, 3)."""
    p = _as_positions(positions, dtype=dtype, device=device)
    v = _as_positions(velocities, dtype=dtype, device=device)
    m = torch.as_tensor(masses, dtype=dtype, device=device)
    cross = torch.cross(p, v, dim=-1)  # (N_t, 3, 3)
    return (m.unsqueeze(-1) * cross).sum(dim=-2)


# ---------------------------------------------------------------------------
# Term callables
# ---------------------------------------------------------------------------

def data_huber_loss(pred_positions, true_positions, *, dtype, device):
    """§3.1 data Huber on COM-projected scaled positions r' = r/D.

    Inputs are already in the dimensionless system (r'). The catalog documents
    D via ``D_CHARACTERISTIC_LENGTH`` so callers convert raw Brutus positions
    with ``r' = r / D`` before calling.  GAP-45-01 / D-01 ratifies the scalar
    reduction as ``sum(Huber) / (9 * N_t)`` for the resident ``(N_t, 3, 3)``
    tensor.  The mean below is intentionally retained unchanged (D-03): it
    is exactly that reduction, with no compensating factor of nine.
    """
    # Touch D so the dimensionless conversion is load-bearing in this module
    # (tests assert the constant is referenced; callers use it to form r').
    _ = D_CHARACTERISTIC_LENGTH
    pred = _as_positions(pred_positions, dtype=dtype, device=device)
    true = _as_positions(true_positions, dtype=dtype, device=device)
    residual = pred - true
    return _huber(residual, HUBER_DELTA_DATA, dtype=dtype, device=device).mean()


def ic_anchor_loss(pred_r0, true_r0, pred_v0, true_v0, *, beta_v=1.0, dtype, device):
    """§3.3 IC squared-error anchors at u=0 / tau=-1.

    ``L_IC = L_IC,r + beta_v * L_IC,v`` with
    ``L_IC,r = (1/3) sum_i ||pred_r_i - true_r_i||^2`` (same for velocity).
    Default ``beta_v = 1``.
    """
    pr = torch.as_tensor(pred_r0, dtype=dtype, device=device).reshape(_N_BODIES, _N_DIMS)
    tr = torch.as_tensor(true_r0, dtype=dtype, device=device).reshape(_N_BODIES, _N_DIMS)
    pv = torch.as_tensor(pred_v0, dtype=dtype, device=device).reshape(_N_BODIES, _N_DIMS)
    tv = torch.as_tensor(true_v0, dtype=dtype, device=device).reshape(_N_BODIES, _N_DIMS)
    three = torch.as_tensor(float(_N_BODIES), dtype=dtype, device=device)
    l_r = ((pr - tr) ** 2).sum() / three
    l_v = ((pv - tv) ** 2).sum() / three
    beta = torch.as_tensor(beta_v, dtype=dtype, device=device)
    return l_r + beta * l_v


def causal_physics_loss(residuals_per_time, *, r_ref=_R_REF_UNSET, eta_c=CAUSAL_ETA_C,
                        times=None, frozen_weights=None, dtype, device,
                        return_details: bool = False):
    """§3.2 causally-weighted physics residual energy.

    Preconditions
    -------------
    ``residuals_per_time`` (``Rbar_n``, shape ``(N_t,)``) MUST be ordered in
    ascending collocation time. The prefix-cumsum weight

        w_1 = 1
        w_n = exp(-eta_c * sum_{m<n} stopgrad(Rtilde_m))

    is only meaningful on a time-sorted sequence. When the optional ``times``
    (or collocation ``u``) argument is supplied, this function asserts
    ``all(times[1:] >= times[:-1])`` and raises ``ValueError`` on unordered
    input BEFORE any weight is computed — a shuffled input is rejected, not
    silently mis-weighted.

    ``R_ref`` normalization (Phase 56 contract: causal-exponent argument
    amended; SPEC-01/SPEC-06; 54-RULING.md checkpoint ② Block 1)
    -----------------------------------------------------------------------
    When the caller supplies ``r_ref`` (a finite positive scalar), every
    ``Rbar_n`` is normalized to ``Rtilde_n = Rbar_n / r_ref`` BEFORE both the
    exclusive-prefix exponent AND the outer mean reduction consume it — the
    residual-wide application 54-RULING.md ratifies. ``r_ref`` is frozen: it
    is never recomputed inside this call, only accepted. Supplying ``r_ref``
    ALSO activates the ratified ``M = 16``-bin length check (a length other
    than 16 is refused) since the amended recipe fixes the bin count exactly.
    Omitting ``r_ref`` (the default) is equivalent to ``r_ref = 1`` — an
    identity normalization preserving every pre-amendment caller's exact
    byte-for-byte behavior, with no length restriction.

    Returns ``(1/N_t) sum_n w_n Rtilde_n``. The cumulative residual used for
    the weight is ``stopgrad``'d (``.detach()``) so the weight cannot become
    an adversarial training term; the OUTER reduction is NOT detached, so
    gradients flow to the raw ``residuals_per_time`` input. The exponent is
    clamped at the active dtype/device's upward-directed representable
    ``log(finfo.tiny)`` floor before exponentiation, so every finite
    non-negative normalized residual sequence has strictly positive causal
    weights.

    ``return_details=True`` additionally exposes ``raw_rbar`` (the
    UN-normalized input) and ``r_ref`` (the value actually used) alongside
    the existing ``w_n``/``rbar`` (now the NORMALIZED ``Rtilde``) keys, so a
    caller can publish both raw and normalized diagnostics from one
    computation and never silently apply a raw-unit threshold to a
    normalized value (or vice versa).
    """
    raw_rbar = torch.as_tensor(residuals_per_time, dtype=dtype, device=device).reshape(-1)
    r_ref_explicit = r_ref is not _R_REF_UNSET
    if r_ref_explicit:
        try:
            r_ref_value = float(r_ref)
        except (TypeError, ValueError) as exc:
            raise ValueError(
                f"causal_physics_loss requires a finite positive r_ref; got {r_ref!r}"
            ) from exc
        if not math.isfinite(r_ref_value) or r_ref_value <= 0.0:
            raise ValueError(
                f"causal_physics_loss requires a finite positive r_ref; got {r_ref!r}"
            )
    else:
        r_ref_value = 1.0

    if times is not None:
        t = torch.as_tensor(times, dtype=dtype, device=device).reshape(-1)
        if t.numel() != raw_rbar.numel():
            raise ValueError(
                f"causal_physics_loss: times length {t.numel()} != "
                f"residuals_per_time length {raw_rbar.numel()}"
            )
        if t.numel() > 1 and bool((t[1:] < t[:-1]).any()):
            raise ValueError(
                "causal_physics_loss requires ascending collocation times; "
                "got unordered times (the causal prefix weight is only "
                "meaningful on a time-sorted sequence)"
            )
    n_t = raw_rbar.numel()
    if n_t == 0:
        raise ValueError("causal_physics_loss: empty residuals_per_time")
    if r_ref_explicit and n_t != _RATIFIED_M_BINS:
        raise ValueError(
            f"causal_physics_loss requires exactly {_RATIFIED_M_BINS} bin "
            f"means (the ratified §3.2 M={_RATIFIED_M_BINS} fixed-bin "
            f"structure) when r_ref is supplied; got length {n_t}"
        )

    r_tilde = raw_rbar / r_ref_value

    if frozen_weights is None:
        eta = torch.as_tensor(eta_c, dtype=dtype, device=device)
        # Prefix sum of stopgrad(Rtilde) for the STRICTLY preceding points.
        # cumsum_excl[0] = 0; cumsum_excl[n] = sum_{m<n} Rtilde_m.detach()
        detached = r_tilde.detach()
        cumsum = torch.cumsum(detached, dim=0)
        # Shift right by one: exclusive prefix.
        zeros = torch.zeros(1, dtype=dtype, device=device)
        cumsum_excl = torch.cat([zeros, cumsum[:-1]], dim=0)
        clip_facts = resolve_causal_clip_facts(dtype, device)
        exponent = -eta * cumsum_excl
        floor = torch.as_tensor(
            clip_facts["causal_clip_exponent_floor"], dtype=dtype, device=device,
        )
        weights = torch.exp(torch.clamp_min(exponent, floor))
        # w_1 is identically 1 by construction (cumsum_excl[0] = 0); pin via constant.
        _ = CAUSAL_W1
    else:
        # GAP-54-06: an L-BFGS segment supplies one detached causal vector;
        # trial residuals must not trigger a new prefix/exponential pass.
        weights = torch.as_tensor(
            frozen_weights, dtype=dtype, device=device,
        ).reshape(-1).detach().clone()
        if weights.numel() != n_t:
            raise ValueError(
                "causal_physics_loss frozen_weights length must equal the "
                f"residual vector length {n_t}; got {weights.numel()}"
            )
        if not bool(torch.isfinite(weights).all()) or not bool((weights > 0.0).all()):
            raise ValueError(
                "causal_physics_loss frozen_weights must be finite and positive"
            )
    loss = (weights * r_tilde).mean()
    if return_details:
        # CTX-70: detach so the autograd graph is NOT retained across steps
        # (retaining it would be a self-inflicted per-step memory DoS).
        return loss, {
            "w_n": weights.detach(),
            "rbar": r_tilde.detach(),
            "raw_rbar": raw_rbar.detach(),
            "r_ref": r_ref_value,
        }
    return loss


def soft_energy_loss(pred_positions, pred_velocities, h0, eps_h, *,
                     masses, dtype, device, eps_soft=EPS_SOFT):
    """§3.4 soft-energy Huber on relative Hamiltonian drift.

    ``Delta H_n = (H(u_n) - H_0) / (|H_0| + eps_h)`` with matched-Plummer
    ``H_eps = T' + V_eps``. ``eps_h`` is the SUPPLIED metadata scalar equal to
    ``1e-4 * S_H`` computed UPSTREAM (Phase 39/40) — this term consumes it
    directly and does NOT recompute ``S_H`` or re-apply the ``1e-4`` factor.
    """
    h = _matched_plummer_hamiltonian(
        pred_positions, pred_velocities, masses,
        dtype=dtype, device=device, eps_soft=eps_soft,
    )
    h0_t = torch.as_tensor(h0, dtype=dtype, device=device)
    eps_h_t = torch.as_tensor(eps_h, dtype=dtype, device=device)
    denom = h0_t.abs() + eps_h_t
    delta_h = (h - h0_t) / denom
    return _huber(delta_h, HUBER_DELTA_ENERGY, dtype=dtype, device=device).mean()


def angular_momentum_loss(pred_positions, pred_velocities, l0, *,
                          masses, dtype, device):
    """§3.5 componentwise angular-momentum Huber.

    ``L_L = (1/(3 N_t)) sum_n sum_alpha Huber((L'_alpha - L'_0,alpha)/L_scale,
    delta=1.0)`` with ``L_scale = ||L_0'|| + eps_L`` (eps_L = 1e-8).
    """
    l_t = _angular_momentum(pred_positions, pred_velocities, masses,
                            dtype=dtype, device=device)  # (N_t, 3)
    l0_t = torch.as_tensor(l0, dtype=dtype, device=device).reshape(3)
    scale = torch.linalg.vector_norm(l0_t) + torch.as_tensor(EPS_L, dtype=dtype, device=device)
    relative = (l_t - l0_t) / scale
    return _huber(relative, HUBER_DELTA_ANGMOM, dtype=dtype, device=device).mean()


def compose_total(terms: Mapping[str, torch.Tensor], weights: LossWeights) -> LossTerms:
    """Weighted sum of the five per-term scalars under a SUPPLIED λ vector.

    Pure function of the supplied weights — does NOT schedule or warm up.
    Returns a ``LossTerms`` container with each per-term scalar plus the total
    for Phase 42 OPS-03 logging.
    """
    if not isinstance(weights, LossWeights):
        raise TypeError(f"compose_total expects LossWeights; got {type(weights)!r}")
    required = ("data", "ic", "phys", "energy", "angmom")
    for key in required:
        if key not in terms:
            raise KeyError(f"compose_total missing term {key!r}")
    data = terms["data"]
    ic = terms["ic"]
    phys = terms["phys"]
    energy = terms["energy"]
    angmom = terms["angmom"]
    total = (
        weights.lambda_data * data
        + weights.lambda_ic * ic
        + weights.lambda_phys * phys
        + weights.lambda_e * energy
        + weights.lambda_l * angmom
    )
    return LossTerms(
        data=data, ic=ic, phys=phys, energy=energy, angmom=angmom, total=total,
    )
