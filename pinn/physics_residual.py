"""Phase 38 / NET-03 — the PHYS-02 componentwise-AD physics residual.

Rebuilt from the authoritative framework spec ``pinn_architecture.md`` (§5.3.1
PHYS-02 and §3.2 softened force). CTX-17 bans the v1.3-era ``pinn/`` files as a
pattern source; nothing here is derived from them.

PHYS-02 contract (§5.3.1)
-------------------------
The canonical autograd leaf is ``u = t/T``. When the code path differentiates
with respect to ``u``::

    v' = dr'/du          (no chain-rule factor)
    a' = d^2 r'/du^2     (no chain-rule factor)

The factors 2 and 4 apply ONLY to a code path that differentiates directly with
respect to a ``tau = 2u - 1`` leaf. The network computes ``tau = 2u - 1`` INSIDE
its ``forward``, so autograd on the ``u`` leaf already propagates that relation
and produces those factors on its own. This module therefore differentiates on
the ``u`` leaf and applies NO manual 2x / 4x factor — applying one would double
count.

All nine derivatives ``dr'_{i,alpha}/du`` are required. The anti-pattern
``torch.autograd.grad(r.sum(), u, create_graph=True)`` is FORBIDDEN: it is a
vector-Jacobian product against an all-ones covector over the OUTPUT COMPONENTS,
not the nine individual derivatives. The two acceptable patterns are used here:
``torch.func.jacrev`` (+ ``vmap`` over the N_t axis) for a callable model, and
an explicit per-output-component ``torch.autograd.grad`` loop for a positions
tensor that is already graph-connected to the ``u`` leaf.

Softened Newtonian force (§3.2)
-------------------------------
::

    r_safe_ij = sqrt(||r'_j - r'_i||^2 + eps_soft^2)      eps_soft = 1e-5
    F_ij      = m_j (r'_j - r'_i) / r_safe_ij^3
    f_i(u_n)  = a'_i(u_n) - sum_{j != i} F_ij

The masses are the ordered RAW masses; ``G = 1`` is absorbed by the raw-mass
nondimensionalization (``D``), so no free gravitational coefficient appears.
``eps_soft`` comes from ``pinn.constants.EPS_SOFT`` — the single home for the
value. PHYS-03: the softening is additive on the SQUARED norm; the anti-pattern
``||d|| + eps`` on the distance is prohibited.

Batch-dimension contract (residual -> loss seam)
------------------------------------------------
The batch axis is ``N_t`` (number of collocation snapshots) and is the LEADING
dimension:

    * ``physics_residual``: ``(N_t, 3, 3)`` positions + ``(N_t,)`` u leaf
      -> ``(N_t, 3, 3)`` residuals.
    * ``componentwise_du``: ``(N_t,)`` u leaf -> ``(N_t, 9)`` first and second
      derivatives.
    * ``softened_acceleration``: ``(N_t, 3, 3)`` -> ``(N_t, 3, 3)``.

A scalar (0-dim) ``u`` leaf is also accepted and yields the unbatched shapes.

Typical caller: the trajectory callable closes over the model's ``forward``,
which returns COM-projected positions (``pinn.network`` /
``pinn.com_projection.project_com``), e.g.::

    traj = lambda u: model.forward(build_tau_ic13(u, ic13), masses).reshape(3, 3)
    residual = physics_residual(traj, u_points, masses, dtype=..., device=...)

Precision/device discipline (CTX-14 / ENV-04): ``dtype`` and ``device`` are
mandatory explicit arguments; scalar constants are wrapped as same-dtype/device
tensors (never Python-float x tensor, which the MPS dual-number path rejects).
The module never calls ``torch.set_default_dtype`` and never probes device
availability, so the identical code path passes fp64-CPU ``gradcheck`` and runs
under fp32-MPS.

Fail-loud (threat T-38-11): any non-finite leaf, position, or residual component
raises rather than emitting a passing result ("refusing to produce evidence",
the discipline of ``pinn/verification/componentwise_ad.py``).
"""

from __future__ import annotations

import torch

from pinn.constants import EPS_SOFT

__all__ = ["componentwise_du", "softened_acceleration", "physics_residual",
           "EPS_SOFT"]

_N_BODIES = 3
_N_DIMS = 3
_N_COMPONENTS = _N_BODIES * _N_DIMS  # the nine dr'_{i,alpha}/du


def _require_finite(tensor, what):
    """Raise unless every component of ``tensor`` is finite (fail-loud)."""
    if not bool(torch.isfinite(tensor).all()):
        raise ValueError(
            f"non-finite {what}; refusing to produce evidence "
            f"(PHYS-02 fail-loud contract)")


# ---------------------------------------------------------------------------
# §5.3.1 — componentwise derivatives on the canonical u leaf.
# ---------------------------------------------------------------------------

def componentwise_du(fn, u_leaf):
    """Componentwise ``dr'/du`` and ``d^2 r'/du^2`` on the canonical ``u`` leaf.

    Args:
        fn: a trajectory callable mapping a SCALAR ``u`` tensor to the positions
            (any shape whose flattened size is the number of output components;
            the 3-body model gives ``(3, 3)`` or a 9-vector). Any ``tau = 2u - 1``
            map inside ``fn`` is propagated by autograd — do NOT pre-scale.
        u_leaf: the ``u`` leaf. Either a scalar (0-dim) tensor or a ``(N_t,)``
            tensor of collocation times.

    Returns:
        ``(first, second)``: the componentwise first and second derivatives with
        respect to ``u``. For a ``(N_t,)`` leaf both have shape ``(N_t, C)``
        (``C = 9`` for the 3-body model); for a scalar leaf both have shape
        ``(C,)``. NO manual 2x / 4x chain factor is applied (§5.3.1).

    Implementation: ``torch.func.jacrev`` composed with itself, mapped over the
    leading N_t axis with ``torch.func.vmap`` — an acceptable §5.3.1 pattern.
    The forbidden summed-output VJP (``grad(r.sum(), u)``) is never used, and
    the result stays differentiable w.r.t. the model parameters ``fn`` closes
    over (the training gradient path).
    """
    u = u_leaf if torch.is_tensor(u_leaf) else torch.as_tensor(u_leaf)
    _require_finite(u, "u leaf")

    def _flat(u_scalar):
        return fn(u_scalar).reshape(-1)

    first_fn = torch.func.jacrev(_flat)
    second_fn = torch.func.jacrev(first_fn)

    if u.dim() == 0:
        first = first_fn(u)
        second = second_fn(u)
    elif u.dim() == 1:
        first = torch.func.vmap(first_fn)(u)
        second = torch.func.vmap(second_fn)(u)
    else:
        raise ValueError(
            f"componentwise_du expects a scalar or (N_t,) u leaf; got shape "
            f"{tuple(u.shape)}")

    _require_finite(first, "first derivative dr'/du")
    _require_finite(second, "second derivative d^2r'/du^2")
    return first, second


def _componentwise_du_from_graph(positions, u_leaf):
    """Componentwise derivatives from a positions tensor already tied to ``u``.

    ``positions`` must be graph-connected to ``u_leaf`` (i.e. produced by
    evaluating the trajectory at that leaf, which must require grad). The
    derivative of EACH of the nine output components is taken separately — the
    forbidden ``r.sum()`` VJP sums over the OUTPUT COMPONENTS and is never used.

    ``grad_outputs`` is a vector of ones over the N_t axis ONLY. That is exact,
    not an approximation: ``u[n]`` influences only snapshot ``n``, so the
    Jacobian over the batch axis is diagonal and the ones-covector reduction
    returns precisely ``d positions[n, k] / d u[n]`` per element.
    """
    flat = positions.reshape(-1, _N_COMPONENTS)
    batched = u_leaf.dim() == 1
    if not u_leaf.requires_grad:
        raise ValueError(
            "the positions-tensor path requires a u leaf with requires_grad=True "
            "(the positions must be graph-connected to the u leaf); pass a "
            "trajectory callable instead if you do not have one")
    ones = torch.ones(flat.shape[0], dtype=flat.dtype, device=flat.device)
    firsts, seconds = [], []
    for k in range(_N_COMPONENTS):
        g1 = torch.autograd.grad(flat[:, k], u_leaf, grad_outputs=ones,
                                 create_graph=True)[0]
        g2 = torch.autograd.grad(g1, u_leaf, grad_outputs=ones,
                                 create_graph=True)[0]
        firsts.append(g1.reshape(-1))
        seconds.append(g2.reshape(-1))
    first = torch.stack(firsts, dim=-1)   # (N_t, 9)
    second = torch.stack(seconds, dim=-1)  # (N_t, 9)
    if not batched:
        first = first.reshape(_N_COMPONENTS)
        second = second.reshape(_N_COMPONENTS)
    _require_finite(first, "first derivative dr'/du")
    _require_finite(second, "second derivative d^2r'/du^2")
    return first, second


# ---------------------------------------------------------------------------
# §3.2 — softened Newtonian force sum (raw masses, G = 1 absorbed into D).
# ---------------------------------------------------------------------------

def softened_acceleration(positions, masses, *, eps_soft=EPS_SOFT, dtype, device):
    """Gravitational acceleration ``sum_{j != i} m_j (r'_j - r'_i) / r_safe^3``.

    Args:
        positions: ``(3, 3)`` (body, coord) or batched ``(N_t, 3, 3)`` positions
            in the dimensionless system (``r' = r / D``).
        masses: the 3 ordered RAW masses, shape ``(3,)`` (or ``(N_t, 3)``).
        eps_soft: the Plummer softening (default ``pinn.constants.EPS_SOFT`` =
            1e-5). PHYS-03: softening is additive on the SQUARED norm.
        dtype: the resolved Torch dtype (explicit).
        device: the resolved Torch device (explicit).

    Returns:
        The acceleration with the same shape as ``positions``.
    """
    p = torch.as_tensor(positions, dtype=dtype, device=device)
    m = torch.as_tensor(masses, dtype=dtype, device=device)
    if p.shape[-2:] != (_N_BODIES, _N_DIMS):
        raise ValueError(
            f"softened_acceleration expects (..., 3 bodies, 3 coords) positions; "
            f"got shape {tuple(p.shape)}")
    _require_finite(p, "position")
    _require_finite(m, "mass")

    eps = torch.as_tensor(eps_soft, dtype=dtype, device=device)
    # d[..., i, j, :] = r'_j - r'_i.
    diff = p.unsqueeze(-3) - p.unsqueeze(-2)
    sq = (diff * diff).sum(dim=-1)                       # (..., i, j)
    r_safe = torch.sqrt(sq + eps * eps)                  # PHYS-03 squared-norm form
    inv_cube = r_safe.pow(-3)
    # Zero the self-interaction (i == j) before weighting. The diagonal's
    # inv_cube is finite (r_safe -> eps), and its gradient contribution vanishes
    # because d(sq)/d(diff) = 2*diff = 0 there, so the mask introduces no NaN.
    eye = torch.eye(_N_BODIES, dtype=dtype, device=device)
    off_diagonal = torch.as_tensor(1.0, dtype=dtype, device=device) - eye
    weights = m.unsqueeze(-2) * inv_cube * off_diagonal  # m_j broadcast over i
    accel = (diff * weights.unsqueeze(-1)).sum(dim=-2)   # sum over j
    _require_finite(accel, "softened acceleration component")
    return accel


# ---------------------------------------------------------------------------
# The PHYS-02 residual.
# ---------------------------------------------------------------------------

def physics_residual(model_or_positions, u, masses, *, dtype, device,
                     eps_soft=EPS_SOFT):
    """``f_i(u_n) = a'_i(u_n) - sum_{j != i} m_j (r'_j - r'_i) / r_safe^3``.

    Args:
        model_or_positions: EITHER a trajectory callable mapping a scalar ``u``
            tensor to ``(3, 3)`` COM-projected positions (typically closing over
            the model's ``forward``), OR a positions tensor of shape
            ``(N_t, 3, 3)`` that is already graph-connected to the ``u`` leaf.
        u: the canonical ``u = t/T`` leaf — a scalar or ``(N_t,)`` tensor. For
            the positions-tensor form it must have ``requires_grad=True``.
        masses: the 3 ordered RAW masses, shape ``(3,)``.
        dtype: the resolved Torch dtype (explicit).
        device: the resolved Torch device (explicit).
        eps_soft: the Plummer softening (default ``EPS_SOFT``).

    Returns:
        The per-body residual: ``(N_t, 3, 3)`` for a ``(N_t,)`` leaf, ``(3, 3)``
        for a scalar leaf. Non-finite components raise instead of being returned.

    The acceleration ``a'`` is the componentwise SECOND derivative on the ``u``
    leaf with NO manual chain factor (§5.3.1); a ``tau = 2u - 1`` map inside the
    model is propagated by autograd.
    """
    u_t = u if torch.is_tensor(u) else torch.as_tensor(u, dtype=dtype, device=device)
    _require_finite(u_t, "u leaf")

    if callable(model_or_positions):
        traj = model_or_positions
        # The first derivative (v' = dr'/du) is not part of the residual; only
        # a' = d^2r'/du^2 is. It is computed alongside and discarded here.
        _velocity, second = componentwise_du(traj, u_t)
        if u_t.dim() == 1:
            positions = torch.func.vmap(lambda s: traj(s).reshape(-1))(u_t)
            positions = positions.reshape(-1, _N_BODIES, _N_DIMS)
            accel = second.reshape(-1, _N_BODIES, _N_DIMS)
        else:
            positions = traj(u_t).reshape(_N_BODIES, _N_DIMS)
            accel = second.reshape(_N_BODIES, _N_DIMS)
    else:
        positions = torch.as_tensor(model_or_positions, dtype=dtype, device=device)
        if positions.shape[-2:] != (_N_BODIES, _N_DIMS):
            raise ValueError(
                f"physics_residual expects (..., 3 bodies, 3 coords) positions; "
                f"got shape {tuple(positions.shape)}")
        _require_finite(positions, "position")
        _velocity, second = _componentwise_du_from_graph(positions, u_t)
        accel = second.reshape(positions.shape)

    _require_finite(positions, "position")
    force = softened_acceleration(positions, masses, eps_soft=eps_soft,
                                  dtype=dtype, device=device)
    residual = accel - force
    _require_finite(residual, "residual component")
    return residual
