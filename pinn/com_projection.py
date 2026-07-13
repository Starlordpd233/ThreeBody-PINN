"""Phase 38 / NET-02 — hard mass-weighted COM projection head.

Pure, idempotent, dtype/device-explicit subtraction of the mass-weighted
center of mass from the 9-dim (3 bodies x 3D) predicted positions, per
``pinn_architecture.md`` §5.3 (Output Frame) and the §10.2 COM invariance
criterion ``abs(COM) < 1e-10``.

Spec contract (§5.3)::

    R_COM = sum_j m_j r~_j / sum_j m_j
    r_i   = r~_i - R_COM,   i in {1,2,3}

``m_j`` are the ordered RAW pre-tanh masses supplied explicitly by the caller
(NET-02 / CTX-21). They are NOT recovered from the tanh-normalized IC13 mass
slots, so ``forward`` must hand them in explicitly (see ``pinn.network``).

Pattern: ``pinn/verification/componentwise_ad.py:62-76`` — pure transform,
constants/masses wrapped as same-dtype/device tensors via
``torch.as_tensor(..., dtype=, device=)``; NEVER Python-float x tensor (MPS
discipline). No module-level dtype assumption; no global-state mutation; no
``.to()`` afterthought. Idempotent by construction: subtracting an
already-zero COM is a no-op.

Does NOT import or copy the v1.3-era ``pinn/`` files (CTX-17).
"""

from __future__ import annotations

import torch

# Number of bodies and spatial dims — the 9-dim output is always 3 bodies x 3D
# (pinn_architecture.md §2.4 / §5.3). Encoding these as named constants rather
# than magic numbers keeps the reshape self-documenting.
_N_BODIES = 3
_N_DIMS = 3


def project_com(positions, masses, *, dtype, device):
    """Subtract the mass-weighted center of mass from 9-dim positions.

    Args:
        positions: 9-dim positions as a length-9 vector (3 bodies x 3D) or a
            batched ``(N, 9)`` tensor. May be a tensor, list, or anything
            ``torch.as_tensor`` accepts.
        masses: the 3 ordered RAW masses (shape ``(3,)``) broadcastable over
            the batch, OR per-sample masses of shape ``(N, 3)``.
        dtype: the resolved Torch dtype (explicit; no default per CTX-14/20).
        device: the resolved Torch device (explicit; no availability probe).

    Returns:
        The flattened 9-dim (or ``(N, 9)``) mass-weighted-COM-subtracted
        positions, on ``(dtype, device)``. Idempotent: re-projecting the
        output is a no-op within tolerance.

    The mass-weighted center of mass is

        R_COM = (sum_i m_i r_i) / (sum_i m_i)

    computed entirely with tensors on ``(dtype, device)`` (no Python-float x
    tensor), so the same code path runs under fp64-CPU and fp32-MPS.
    """
    m = torch.as_tensor(masses, dtype=dtype, device=device)
    p = torch.as_tensor(positions, dtype=dtype, device=device)
    if p.shape[-1] != _N_BODIES * _N_DIMS:
        raise ValueError(
            f"project_com: positions last dim must be "
            f"{_N_BODIES * _N_DIMS} (3 bodies x 3D); got shape {tuple(p.shape)}"
        )
    # Reshape the trailing 9 into (3 bodies, 3 dims); leading dims are batch.
    # positions (..., 9) -> (..., 3 bodies, 3 dims): row b is body b's vector.
    p3 = p.reshape(*p.shape[:-1], _N_BODIES, _N_DIMS)

    # masses (3,) or (..., 3). Expand over the spatial-dim axis so each body's
    # 3-vector is scaled by its mass: m broadcast to (..., 3 bodies, 1).
    m_expanded = m.unsqueeze(-1)
    # Weighted sum over bodies -> (..., 3 dims). Total mass -> (..., 1) so it
    # broadcasts cleanly against weighted_sum for both shared (3,) and
    # per-sample (..., 3) mass shapes.
    weighted_sum = (p3 * m_expanded).sum(dim=-2)
    total_mass = m.sum(dim=-1, keepdim=True)
    com = weighted_sum / total_mass  # (..., 3 dims)
    # Broadcast the per-sample COM over the body axis and subtract.
    projected = p3 - com.unsqueeze(-2)
    # Flatten the trailing (bodies, dims) back to 9, preserving any batch dims.
    return projected.reshape(*p.shape[:-1], _N_BODIES * _N_DIMS)


__all__ = ["project_com"]
