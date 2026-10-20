"""Phase 60 (INST-05): the trainer's own loss functions, composed for the harness arms.

The harness never re-implements a loss. Every term is a function the production
trainer already calls: the Huber data term, the initial-condition anchor, the
causal physics term, the soft-energy and angular-momentum terms and the
total composition come from ``pinn.loss_catalog``; the componentwise derivatives and
the softened acceleration come from ``pinn.physics_residual``; the chunked data term, the
bin count and the bin-index rule come from ``pinn.training.controllers``; the
stratified collocation draw comes from ``pinn.data.batches``. All of them are
imported by bare name at module scope, so ``mock.patch.object`` on this module
moves the output and a mutation test can prove the harness really calls them.

The physics step takes every tensor and constant as an explicit argument (the
trainer reads them from controller state). Its order is the trainer's
memory-bounded step: pass 1 freezes the causal weights, then the data and
initial-condition terms are back-propagated, then pass 2 back-propagates each
chunk of collocation rows with a constant row weight. Every residual evaluation
uses chunks of at most ``microbatch_size`` rows (256 in production) and
releases each chunk before the next, so no 4,096-row graph is ever built.

The frozen monitor is a log (D-06): ``frozen_monitor_log`` evaluates a fixed set of
collocation rows through pass 1 when the runner asks and returns the causal-weight
statistics; it has no threshold and no halt. The physics polish objective uses the
rows, causal weights, bin counts and loss weights frozen at the Adam-to-L-BFGS
handoff (GAP-60-05) and the same chunked pass 2, never a full-batch evaluation.

``r_ref`` is an explicit argument everywhere. The runner passes the Stage-0
reference in force; these functions never read the governed artifact.
"""

from __future__ import annotations

import gc

import numpy as np
import torch

from pinn.constants import T_CHARACTERISTIC_TIME
from pinn.data.batches import _stratified_full_slot_rows
from pinn.loss_catalog import (
    LossWeights,
    angular_momentum_loss,
    causal_physics_loss,
    compose_total,
    data_huber_loss,
    ic_anchor_loss,
    soft_energy_loss,
)
from pinn.physics_residual import componentwise_du, softened_acceleration
from pinn.training.controllers import (
    _RATIFIED_N_BINS,
    _bin_index_for_times,
    accumulate_chunked_data_term,
)

__all__ = [
    "make_trajectory",
    "draw_collocation_times",
    "collocation_chunk_raw",
    "physics_pass1",
    "ic_term",
    "physics_pass2_backward",
    "physics_adam_step",
    "physics_polish_objective",
    "frozen_monitor_log",
    "release_chunk_memory",
    "data_only_loss",
    "data_polish_objective",
]


def release_chunk_memory(device):
    """Free a just-finished chunk's autograd graph (generation 0 only).

    A chunk's graph holds reference cycles that only the cyclic collector can
    break. On an MPS device the cached blocks are also returned to the driver.
    An error from the cache call alone is ignored.
    """
    gc.collect(0)
    if device.type == "mps" and hasattr(torch, "mps"):
        try:
            torch.mps.empty_cache()
        except Exception:
            pass


def _require_weights(weights):
    if not isinstance(weights, LossWeights):
        raise TypeError(f"weights must be a LossWeights; got {type(weights)!r}")


def _require_positive_microbatch(microbatch_size):
    if microbatch_size <= 0:
        raise ValueError(f"microbatch_size must be positive; got {microbatch_size!r}")


def make_trajectory(model, ic13_t, masses_t):
    """The trainer's trajectory closure: scalar ``u`` to the ``(3, 3)`` positions.

    The network input is ``[tau, IC13]`` with ``tau = 2u - 1``; ``u`` stays the
    autograd leaf. ``ic13_t`` has shape ``(13,)`` and ``masses_t`` shape ``(3,)``.
    """

    def traj(u_scalar):
        tau = (2.0 * u_scalar - 1.0).reshape(1)
        tau_ic13 = torch.cat([tau, ic13_t], dim=0).unsqueeze(0)
        pos = model(tau_ic13, masses_t.unsqueeze(0))
        return pos.reshape(3, 3)

    return traj


def draw_collocation_times(record_key, rng, *, n_slots=256):
    """Ascending collocation times: one row per slot inside each of the 16 bins.

    One system repeated in every slot is the single-system case of the ratified
    stratified draw, so 256 slots give 4,096 rows with 256 in each bin.
    """
    if isinstance(n_slots, bool) or not isinstance(n_slots, int) or n_slots <= 0:
        raise ValueError(f"n_slots must be a positive int; got {n_slots!r}")
    rows = _stratified_full_slot_rows([record_key] * n_slots, rng=rng)
    return np.sort(np.asarray([time for _key, time in rows], dtype=np.float64))


def collocation_chunk_raw(traj, masses_t, times_chunk, *, dtype, device):
    """Positions, velocities and the per-row residual energy for one chunk of rows.

    The same ``componentwise_du``, ``vmap`` and ``softened_acceleration`` calls
    the trainer makes; only the size of the ``u`` batch differs from a
    full-batch evaluation.
    """
    u_leaf = torch.as_tensor(
        times_chunk / T_CHARACTERISTIC_TIME, dtype=dtype, device=device
    )
    first, second = componentwise_du(traj, u_leaf)
    positions = torch.func.vmap(lambda s: traj(s).reshape(-1))(u_leaf)
    positions = positions.reshape(-1, 3, 3)
    velocities = first.reshape(-1, 3, 3)
    accel = second.reshape(-1, 3, 3)
    force = softened_acceleration(positions, masses_t, dtype=dtype, device=device)
    residual = accel - force
    rbar = (residual**2).sum(dim=(-2, -1)) / 3.0
    return positions, velocities, rbar


def physics_pass1(traj, masses_t, times, *, r_ref, microbatch_size, dtype, device):
    """Pass 1: the frozen causal weights, with no parameter graph kept past a chunk.

    Returns ``(details, bin_counts)``. ``details`` is the trainer's
    ``causal_physics_loss`` detail mapping (``w_n``, the normalized and raw
    per-bin residuals and ``r_ref``); ``bin_counts`` holds the rows per bin.
    ``times`` is the ascending array of collocation times.
    """
    _require_positive_microbatch(microbatch_size)
    n_total = int(times.shape[0])
    bin_sums = torch.zeros(_RATIFIED_N_BINS, dtype=dtype, device=device)
    bin_counts = torch.zeros(_RATIFIED_N_BINS, dtype=dtype, device=device)
    start = 0
    while start < n_total:
        end = min(start + microbatch_size, n_total)
        chunk_times = times[start:end]
        positions_chunk, velocities_chunk, rbar_chunk = collocation_chunk_raw(
            traj, masses_t, chunk_times, dtype=dtype, device=device
        )
        rbar_chunk = rbar_chunk.detach().clone()
        times_tensor_chunk = torch.as_tensor(chunk_times, dtype=dtype, device=device)
        bin_idx_chunk = _bin_index_for_times(
            times_tensor_chunk, n_bins=_RATIFIED_N_BINS, t_max=T_CHARACTERISTIC_TIME
        )
        bin_sums = bin_sums.index_add(0, bin_idx_chunk, rbar_chunk)
        bin_counts = bin_counts.index_add(0, bin_idx_chunk, torch.ones_like(rbar_chunk))
        del positions_chunk, velocities_chunk, rbar_chunk, bin_idx_chunk, times_tensor_chunk
        release_chunk_memory(device)
        start = end
    raw_bin_means = bin_sums / bin_counts.clamp(min=1.0)
    bin_centres = (
        torch.arange(_RATIFIED_N_BINS, dtype=dtype, device=device)
        + torch.as_tensor(0.5, dtype=dtype, device=device)
    ) / _RATIFIED_N_BINS * T_CHARACTERISTIC_TIME
    _discard_loss, details = causal_physics_loss(
        raw_bin_means,
        r_ref=r_ref,
        times=bin_centres,
        dtype=dtype,
        device=device,
        return_details=True,
    )
    return details, bin_counts.detach()


def ic_term(traj, true_r0, true_v0, *, dtype, device):
    """The initial-condition anchor: position and velocity at ``u = 0``."""
    zero_u = torch.zeros((), dtype=dtype, device=device)
    pred_r0 = traj(zero_u)
    first0, _second0 = componentwise_du(traj, zero_u)
    pred_v0 = first0.reshape(3, 3)
    return ic_anchor_loss(pred_r0, true_r0, pred_v0, true_v0, dtype=dtype, device=device)


def physics_pass2_backward(
    traj,
    masses_t,
    times,
    *,
    w_n,
    bin_counts,
    r_ref,
    weights,
    h0,
    eps_h,
    l0,
    microbatch_size,
    dtype,
    device,
):
    """Pass 2: back-propagate the weighted physics terms one chunk at a time.

    Each row carries the constant weight ``w_n[bin] / (16 * r_ref * count[bin])``,
    so the sum over every chunk reproduces the full-batch causal loss. The
    energy and angular-momentum terms are evaluated only when their own weight
    is above zero; a skipped term reports zero. Returns the detached
    ``(phys, energy, angmom)`` totals; the gradients are left in ``.grad``.
    """
    _require_weights(weights)
    _require_positive_microbatch(microbatch_size)
    n_total = int(times.shape[0])
    n_bins = _RATIFIED_N_BINS
    r_ref = float(r_ref)
    with_energy = weights.lambda_e > 0.0
    with_angmom = weights.lambda_l > 0.0
    phys_total = torch.zeros((), dtype=dtype, device=device)
    energy_total = torch.zeros((), dtype=dtype, device=device)
    angmom_total = torch.zeros((), dtype=dtype, device=device)
    start = 0
    while start < n_total:
        end = min(start + microbatch_size, n_total)
        chunk_times = times[start:end]
        positions_chunk, velocities_chunk, rbar_chunk = collocation_chunk_raw(
            traj, masses_t, chunk_times, dtype=dtype, device=device
        )
        times_tensor_chunk = torch.as_tensor(chunk_times, dtype=dtype, device=device)
        bin_idx_chunk = _bin_index_for_times(
            times_tensor_chunk, n_bins=n_bins, t_max=T_CHARACTERISTIC_TIME
        )
        row_weight_chunk = w_n[bin_idx_chunk] / (
            float(n_bins) * r_ref * bin_counts[bin_idx_chunk]
        )
        phys_chunk = (row_weight_chunk * rbar_chunk).sum()
        chunk_frac = float(end - start) / float(n_total)
        weighted_chunk = weights.lambda_phys * phys_chunk
        if with_energy:
            energy_chunk = chunk_frac * soft_energy_loss(
                positions_chunk,
                velocities_chunk,
                h0,
                eps_h,
                masses=masses_t,
                dtype=dtype,
                device=device,
            )
            weighted_chunk = weighted_chunk + weights.lambda_e * energy_chunk
            energy_total = energy_total + energy_chunk.detach()
        if with_angmom:
            angmom_chunk = chunk_frac * angular_momentum_loss(
                positions_chunk,
                velocities_chunk,
                l0,
                masses=masses_t,
                dtype=dtype,
                device=device,
            )
            weighted_chunk = weighted_chunk + weights.lambda_l * angmom_chunk
            angmom_total = angmom_total + angmom_chunk.detach()
        weighted_chunk.backward()
        phys_total = phys_total + phys_chunk.detach()
        del (
            positions_chunk,
            velocities_chunk,
            rbar_chunk,
            times_tensor_chunk,
            bin_idx_chunk,
            row_weight_chunk,
            phys_chunk,
            weighted_chunk,
        )
        release_chunk_memory(device)
        start = end
    return phys_total, energy_total, angmom_total


def physics_adam_step(
    model,
    *,
    data_points,
    ic13_t,
    masses_t,
    true_r0,
    true_v0,
    collocation_times,
    weights,
    r_ref,
    h0,
    eps_h,
    l0,
    microbatch_size,
    dtype,
    device,
):
    """One memory-bounded physics Adam step: gradients land in ``.grad``.

    Pass 1 freezes the causal weights, ``(data + IC).backward()`` follows, then
    pass 2 runs the chunk loop. The caller clears the gradients first and owns
    the optimizer. ``data_points=None`` is Rung 2a: the data term is never
    evaluated, ``compose_total`` receives a zero tensor for it, and
    ``LossWeights`` keeps ``lambda_data`` at 1.0. Returns the detached terms
    ``data``, ``ic``, ``phys``, ``energy``, ``angmom`` and ``total``.
    """
    _require_weights(weights)
    traj = make_trajectory(model, ic13_t, masses_t)
    details, bin_counts = physics_pass1(
        traj,
        masses_t,
        collocation_times,
        r_ref=r_ref,
        microbatch_size=microbatch_size,
        dtype=dtype,
        device=device,
    )
    ic = ic_term(traj, true_r0, true_v0, dtype=dtype, device=device)
    if data_points is None:
        data = torch.zeros((), dtype=dtype, device=device)
    else:
        data = data_only_loss(model, data_points, dtype=dtype, device=device)
    (weights.lambda_data * data + weights.lambda_ic * ic).backward()
    release_chunk_memory(device)
    phys, energy, angmom = physics_pass2_backward(
        traj,
        masses_t,
        collocation_times,
        w_n=details["w_n"],
        bin_counts=bin_counts,
        r_ref=details["r_ref"],
        weights=weights,
        h0=h0,
        eps_h=eps_h,
        l0=l0,
        microbatch_size=microbatch_size,
        dtype=dtype,
        device=device,
    )
    terms = compose_total(
        {
            "data": data.detach(),
            "ic": ic.detach(),
            "phys": phys,
            "energy": energy,
            "angmom": angmom,
        },
        weights,
    )
    return {
        "data": terms.data,
        "ic": terms.ic,
        "phys": terms.phys,
        "energy": terms.energy,
        "angmom": terms.angmom,
        "total": terms.total,
    }


def frozen_monitor_log(traj, masses_t, frozen_times, *, r_ref, microbatch_size, dtype, device):
    """The frozen monitor's statistics at the current parameters (D-06).

    Runs the chunked pass 1 on the frozen collocation rows and returns plain
    floats and lists: the minimum, mean and maximum causal weight, the front
    index (the largest bin whose weight exceeds one half, else -1), the
    normalized and raw residual of each of the 16 bins, and ``r_ref``. The runner
    calls it only at the budget-rule readings. It is a log: it has no threshold,
    no halt and no return code, and nothing here decides anything from a front
    value.
    """
    details, _bin_counts = physics_pass1(
        traj,
        masses_t,
        frozen_times,
        r_ref=r_ref,
        microbatch_size=microbatch_size,
        dtype=dtype,
        device=device,
    )
    w_n = details["w_n"]
    w_n_list = w_n.tolist()
    return {
        "w_min": float(w_n.min()),
        "w_mean": float(w_n.mean()),
        "w_max": float(w_n.max()),
        "front_idx": max([n for n, w in enumerate(w_n_list) if w > 0.5], default=-1),
        "residuals_per_bin": [float(r) for r in details["rbar"].tolist()],
        "raw_residuals_per_bin": [float(r) for r in details["raw_rbar"].tolist()],
        "r_ref": float(details["r_ref"]),
    }


def physics_polish_objective(
    model,
    *,
    frozen_times,
    frozen_w_n,
    frozen_bin_counts,
    frozen_weights,
    data_points,
    ic13_t,
    masses_t,
    true_r0,
    true_v0,
    r_ref,
    h0,
    eps_h,
    l0,
    data_chunk_size,
    microbatch_size,
    dtype,
    device,
):
    """The physics polish objective: one L-BFGS closure evaluation on frozen inputs.

    The collocation rows, the causal weights, the bin counts and the loss weights
    are the ones frozen at the Adam-to-L-BFGS handoff. They are never redrawn or
    recomputed between closure evaluations (GAP-60-05, 57-RULING.md). Gradients
    are cleared, the data term (when the arm has one) is accumulated by the
    trainer's chunked function, the initial-condition term is back-propagated,
    and the chunked pass 2 adds the physics, energy and angular-momentum
    gradients. The trainer's own closure builds all 4,096 rows at once, so the
    harness never calls it. Returns the detached weighted total.
    """
    _require_weights(frozen_weights)
    model.zero_grad(set_to_none=True)
    if data_points is None:
        weighted_data = torch.zeros((), dtype=dtype, device=device)
    else:
        weighted_data = accumulate_chunked_data_term(
            model,
            data_points,
            weight=frozen_weights.lambda_data,
            chunk_size=data_chunk_size,
            dtype=dtype,
            device=device,
        )
    traj = make_trajectory(model, ic13_t, masses_t)
    weighted_ic = frozen_weights.lambda_ic * ic_term(
        traj, true_r0, true_v0, dtype=dtype, device=device
    )
    weighted_ic.backward()
    release_chunk_memory(device)
    phys, energy, angmom = physics_pass2_backward(
        traj,
        masses_t,
        frozen_times,
        w_n=frozen_w_n,
        bin_counts=frozen_bin_counts,
        r_ref=r_ref,
        weights=frozen_weights,
        h0=h0,
        eps_h=eps_h,
        l0=l0,
        microbatch_size=microbatch_size,
        dtype=dtype,
        device=device,
    )
    other_total = (
        weighted_ic.detach()
        + frozen_weights.lambda_phys * phys
        + frozen_weights.lambda_e * energy
        + frozen_weights.lambda_l * angmom
    )
    return (weighted_data + other_total).detach()


def data_only_loss(model, data_points, *, dtype, device):
    """The Adam objective of a data-only arm: the Huber data term over every point.

    ``data_points`` carries ``tau_ic13`` (N, 14), ``masses`` (N, 3) and
    ``targets`` (N, 3, 3). The result keeps its autograd graph.
    """
    pred = model(data_points.tau_ic13, data_points.masses)
    return data_huber_loss(
        pred.reshape(-1, 3, 3),
        data_points.targets.reshape(-1, 3, 3),
        dtype=dtype,
        device=device,
    )


def data_polish_objective(model, data_points, *, chunk_size, dtype, device):
    """The full-batch polish objective: one closure evaluation for L-BFGS.

    Gradients are cleared, then ``accumulate_chunked_data_term`` accumulates the
    exact full-batch gradient chunk by chunk and returns the detached scalar.
    """
    model.zero_grad(set_to_none=True)
    return accumulate_chunked_data_term(
        model,
        data_points,
        weight=1.0,
        chunk_size=chunk_size,
        dtype=dtype,
        device=device,
    )
