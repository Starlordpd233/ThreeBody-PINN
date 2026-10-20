"""Phase 60 (INST-05): the data-only loss, composed from the trainer's own functions.

The harness never re-implements a loss. The Huber data term is
``pinn.loss_catalog.data_huber_loss`` and the polish objective is
``pinn.training.controllers.accumulate_chunked_data_term``. Both are imported
by bare name at module scope, so ``mock.patch.object`` on this module moves the
output and a mutation test can prove the harness really calls them. Plan 60-05
adds the physics terms to this module.
"""

from __future__ import annotations

from pinn.loss_catalog import data_huber_loss
from pinn.training.controllers import accumulate_chunked_data_term

__all__ = ["data_only_loss", "data_polish_objective"]


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
