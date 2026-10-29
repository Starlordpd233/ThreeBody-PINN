"""Phase 65 (INST-08): the minute-scale diagnostic fit, score and record path.

``fit_diagnostic`` fits one named diagnostic variant on one already-loaded
Stage-0 training orbit with a constant-rate Adam policy — ``OptConfig``'s betas
and epsilon, the variant's learning rate, no physics term, no scheduler and no
polish — taking the existing data-only loss (INST-05's ``data_only_loss``)
directly, guarding the loss and gradients before every update, measuring the
shared time-signal similarity at initialization and at the final step once
each (hooks and logging kept outside the optimizer timing), scoring the fitted
network with the frozen FEAS-01 ``score_network``, recording the window-mean
constant predictor (zero velocities) and the two-Kepler comparison through the
frozen ``score_trajectory`` on the same times and body order, and publishing
one canonical, exclusive record plus an intrinsically marked tensor payload.

The record and payload carry the ``inst08-diagnostic/v1`` identity
(``artifact_kind``/``diagnostic``/``counted``), variant identity and
configuration, seed, runtime, orbit/window identity, requested and completed
steps, similarity cadence, timing basis, the full frozen scorer output,
comparison rows, the 33 pinned source hashes and the reader's access counts. A
bare state dict is never published as an INST-08 artifact. This module never
calls the sealed Phase 60 entry points (``run_arm``, ``admit_arm``) or the
real-corpus resolver; Plan 65-03 wires the shared refusal into production.
"""

from __future__ import annotations

import hashlib
import math
import re
import time
from collections import OrderedDict
from pathlib import Path

import numpy as np
import torch

from pinn.constants import T_CHARACTERISTIC_TIME
from pinn.training.atomic_io import atomic_write_torch
from pinn.training.config import OptConfig
from pinn.verification import evidence_io
from pinn.verification.diagnostic_guard import (
    WEIGHTS_SCHEMA,
    diagnostic_marker,
)
from pinn.verification.diagnostic_similarity import measure_time_signal
from pinn.verification.diagnostic_variants import (
    REGISTRY,
    DiagnosticVariant,
    build_variant,
    resolve_variant,
)
from pinn.verification.feasibility_scorer import score_network, score_trajectory
from pinn.verification.learnability_arms import SEED, FirstResultExists, write_record_exclusive
from pinn.verification.learnability_losses import data_only_loss
from pinn.verification.learnability_protocol import PINNED_MODULES
from pinn.verification.learnability_run import weights_digest
from pinn.verification.two_kepler import NotApplicable, two_kepler_prediction

__all__ = [
    "DIAGNOSTIC_SCHEMA",
    "TIMING_BASIS",
    "DiagnosticFitRefused",
    "diagnostic_evidence_dir",
    "diagnostic_run_id",
    "fit_diagnostic",
    "log_similarity",
    "pinned_source_hashes",
    "save_diagnostic_weights",
]

DIAGNOSTIC_SCHEMA = "inst08-diagnostic/v1"
RECORD_NAME = "record.json"
WEIGHTS_NAME = "weights.pt"
_RUN_ID_RE = re.compile(r"[a-z0-9][a-z0-9-]*")

#: The measured wall time covers the constant-rate Adam steps only. Similarity
#: logging (hooks), frozen scoring, comparison predictors and artifact writes
#: are outside the measured window (D-11's timing basis).
TIMING_BASIS = (
    "optimizer steps only (constant-rate Adam); similarity logging, frozen "
    "scoring, comparisons and artifact writes excluded; monotonic clock"
)

_DTYPES = {"float64": torch.float64, "float32": torch.float32}


class DiagnosticFitRefused(RuntimeError):
    """A diagnostic fit precondition does not hold; nothing runs or is published."""


def _resolve_runtime(runtime):
    """Map a named ``(dtype, device)`` pair to torch objects. No availability probe."""
    try:
        dtype_name, device_name = runtime
    except (TypeError, ValueError) as exc:
        raise DiagnosticFitRefused(
            f"runtime must be a (dtype, device) pair such as ('float64', 'cpu'); "
            f"got {runtime!r}"
        ) from exc
    if dtype_name not in _DTYPES:
        raise DiagnosticFitRefused(
            f"runtime dtype must be one of {sorted(_DTYPES)}; got {dtype_name!r}"
        )
    return _DTYPES[dtype_name], torch.device(device_name)


def pinned_source_hashes(*, repo_root=None):
    """The 33 pinned INST-05 module hashes, as the frozen protocol pins them.

    A pinned artifact that is missing is a refusal, not a regenerated baseline.
    """
    try:
        return dict(
            evidence_io.module_hashes(list(PINNED_MODULES), repo_root=repo_root)
        )
    except FileNotFoundError as exc:
        raise DiagnosticFitRefused(f"a pinned source artifact is missing: {exc}") from exc


def diagnostic_run_id(variant, data):
    """``<variant name>-<train record slug>``, a plain lowercase token."""
    key = data.records["train"]["record_key"]
    run_id = f"{variant.name}-{str(key).replace('/', '-')}"
    if _RUN_ID_RE.fullmatch(run_id) is None:
        raise DiagnosticFitRefused(
            f"the diagnostic run id must match [a-z0-9][a-z0-9-]*; got {run_id!r}"
        )
    return run_id


def diagnostic_evidence_dir(run_id, *, evidence_root):
    """``<evidence_root>/diagnostics/<run_id>``, refusing an id that could escape."""
    if not isinstance(run_id, str) or _RUN_ID_RE.fullmatch(run_id) is None:
        raise DiagnosticFitRefused(
            f"the diagnostic run id must match [a-z0-9][a-z0-9-]*; got {run_id!r}"
        )
    return Path(evidence_root) / "diagnostics" / run_id


def save_diagnostic_weights(path, model, *, variant, seed, runtime):
    """Save the CPU state dict inside the intrinsic diagnostic envelope.

    The payload is the marker block beside the plain ``state_dict``, so it
    loads with ``weights_only=True`` and can never be mistaken for a bare
    production state dict. Returns the file and tensor digests.
    """
    state = OrderedDict(
        (name, tensor.detach().cpu().clone())
        for name, tensor in model.state_dict().items()
    )
    payload = {
        **diagnostic_marker(schema=WEIGHTS_SCHEMA),
        "variant": variant.to_json_dict(),
        "seed": int(seed),
        "runtime": {"dtype": str(runtime[0]), "device": str(runtime[1])},
        "state_dict": state,
    }
    atomic_write_torch(path, payload)
    digest = hashlib.sha256(Path(path).read_bytes()).hexdigest()
    return {
        "file": Path(path).name,
        "sha256": digest,
        "tensor_digest": weights_digest(state),
        "schema": WEIGHTS_SCHEMA,
    }


def log_similarity(model, data_points, times_physical, *, step, point):
    """The fit logger's callable similarity entry.

    ``measure_time_signal`` is the sole measurement implementation: probe and
    logger share this one function (D-05), so the logger's trace is comparable
    with the DIAG-09 reproduction by construction.
    """
    measurement = measure_time_signal(
        model,
        data_points.tau_ic13,
        data_points.masses,
        data_points.targets,
        times_physical,
    )
    return {
        "step": int(step),
        "point": str(point),
        **measurement.to_json_dict(),
    }


def _validate_data_points(data_points):
    if data_points is None:
        raise DiagnosticFitRefused("the fit needs data points; got None")
    tau = getattr(data_points, "tau_ic13", None)
    masses = getattr(data_points, "masses", None)
    targets = getattr(data_points, "targets", None)
    if tau is None or masses is None or targets is None:
        raise DiagnosticFitRefused(
            "the fit needs tau_ic13, masses and targets; a field is None"
        )
    if not isinstance(tau, torch.Tensor) or tau.dim() != 2:
        raise DiagnosticFitRefused(
            f"tau_ic13 must be a 2-D tensor (N, 14); got {type(tau).__name__} "
            f"{tuple(getattr(tau, 'shape', ()))}"
        )
    count = int(tau.shape[0])
    if count < 2:
        raise DiagnosticFitRefused(
            f"at least two samples are needed for a diagnostic fit; got {count}"
        )


def _guarded_step(model, optimizer, data_points, *, dtype, device, step):
    """One constant-rate Adam step behind finiteness guards.

    A non-finite loss or gradient refuses before ``optimizer.step()`` — the
    diagnostic never updates on, or publishes, a non-finite quantity.
    """
    optimizer.zero_grad(set_to_none=True)
    loss = data_only_loss(model, data_points, dtype=dtype, device=device)
    value = float(loss)
    if not math.isfinite(value):
        raise DiagnosticFitRefused(
            f"the data-only loss is not finite before step {step}: {value!r}"
        )
    loss.backward()
    for parameter in model.parameters():
        if parameter.grad is not None and not bool(
            torch.isfinite(parameter.grad).all()
        ):
            raise DiagnosticFitRefused(
                f"a parameter gradient is not finite before step {step}; "
                "refusing the optimizer update"
            )
    optimizer.step()
    return float(loss.detach())


def _comparison_rows(data, *, scorecard):
    """The matched-window comparison rows through the frozen score_trajectory.

    Same times, same body order, same window as the network score. A formula
    ``NotApplicable`` result carries its existing reason; it never becomes a
    successful score.
    """
    view = data.score
    positions = np.asarray(view.positions, dtype=np.float64)
    times = np.asarray(view.times, dtype=np.float64)
    masses = np.asarray(data.masses, dtype=np.float64).reshape(3)
    inner_pair = tuple(int(slot) for slot in view.inner_pair)

    constant = np.broadcast_to(
        positions.mean(axis=0, keepdims=True), positions.shape
    ).copy()
    constant_score = score_trajectory(
        constant,
        np.zeros_like(constant),
        positions,
        masses,
        inner_pair,
        times,
        velocity_source="analytic",
        scorecard=scorecard,
        grid=view.grid,
    )
    constant_row = {
        "comparison": "window_mean_constant",
        "predictor": {
            "kind": "window_mean_constant",
            "velocities": "zero",
            "definition": "each body held at its time-mean position over the window",
        },
        "score": constant_score.to_json_dict(),
    }

    elapsed = (times - times[0]) / T_CHARACTERISTIC_TIME
    r0 = data.true_r0.detach().cpu().numpy().astype(np.float64).reshape(3, 3)
    v0 = data.true_v0.detach().cpu().numpy().astype(np.float64).reshape(3, 3)
    try:
        predicted, predicted_v = two_kepler_prediction(r0, v0, masses, inner_pair, elapsed)
    except NotApplicable as exc:
        kepler_row = {
            "comparison": "two_kepler",
            "applicable": False,
            "failure": "not_applicable",
            "reason": exc.reason,
        }
    except RuntimeError as exc:
        # The frozen formula's own Newton solver failed on this window (its
        # message, verbatim). Like NotApplicable, it never becomes a score.
        kepler_row = {
            "comparison": "two_kepler",
            "applicable": False,
            "failure": "solver_did_not_converge",
            "reason": str(exc),
        }
    else:
        kepler_score = score_trajectory(
            predicted,
            predicted_v,
            positions,
            masses,
            inner_pair,
            times,
            velocity_source="analytic",
            scorecard=scorecard,
            grid=view.grid,
        )
        kepler_row = {
            "comparison": "two_kepler",
            "applicable": True,
            "initial_state": "the train record's first in-window snapshot (true_r0, true_v0)",
            "score": kepler_score.to_json_dict(),
        }
    return [constant_row, kepler_row]


def fit_diagnostic(
    variant,
    data,
    *,
    context,
    scorecard,
    runtime=("float64", "cpu"),
    evidence_root,
    steps,
    times_physical=None,
    seed=SEED,
    repo_root=None,
    clock=time.monotonic,
):
    """Fit, measure, score and record one diagnostic variant on one orbit.

    ``data`` is an already-loaded ``ArmData`` (the Phase 60 fixture seam here;
    the training-only Stage-0 reader in Plan 65-02 later). ``times_physical``
    are the physical times of the training samples, recorded beside their
    normalized tau; it defaults to the score view's times, which is exact when
    the train and score records share a grid. Returns the canonical record.
    """
    resolved = resolve_variant(variant)
    if isinstance(steps, bool) or not isinstance(steps, int) or steps < 1:
        raise DiagnosticFitRefused(f"steps must be a positive integer; got {steps!r}")
    dtype, device = _resolve_runtime(runtime)
    _validate_data_points(getattr(data, "data_points", None))
    if times_physical is None:
        times_physical = data.score.times
    run_id = diagnostic_run_id(resolved, data)
    out_dir = diagnostic_evidence_dir(run_id, evidence_root=evidence_root)
    record_path = out_dir / RECORD_NAME
    if record_path.exists():
        raise FirstResultExists(
            f"a diagnostic record already exists at {record_path.name}; the first "
            "completed run is the result and a second run never replaces it"
        )

    model = build_variant(resolved, seed=seed, dtype=dtype, device=device)
    options = OptConfig()
    optimizer = torch.optim.Adam(
        model.parameters(),
        lr=float(resolved.learning_rate),
        betas=options.adam_betas,
        eps=options.adam_eps,
    )

    # Initialization is logged once, before the timer starts and before any step.
    similarity = {"cadence": ["init", "final"]}
    similarity["init"] = log_similarity(
        model, data.data_points, times_physical, step=0, point="init"
    )

    losses = []
    started = clock()
    for step in range(1, int(steps) + 1):
        losses.append(
            _guarded_step(model, optimizer, data.data_points, dtype=dtype, device=device, step=step)
        )
    wall = clock() - started

    # The final step is logged once, outside the optimizer timing window.
    similarity["final"] = log_similarity(
        model, data.data_points, times_physical, step=int(steps), point="final"
    )

    view = data.score
    score = score_network(
        model,
        data.ic13,
        data.masses,
        view.positions,
        view.inner_pair,
        view.times,
        scorecard=scorecard,
        dtype=dtype,
        device=device,
        grid=view.grid,
    )
    comparisons = _comparison_rows(data, scorecard=scorecard)

    out_dir.mkdir(parents=True, exist_ok=True)
    weights_block = save_diagnostic_weights(
        out_dir / WEIGHTS_NAME, model, variant=resolved, seed=seed, runtime=runtime
    )
    times = np.asarray(times_physical, dtype=np.float64).reshape(-1)
    record = {
        **diagnostic_marker(schema=DIAGNOSTIC_SCHEMA),
        "variant": {
            **resolved.to_json_dict(),
            "registered": resolved.name in REGISTRY,
        },
        "seed": int(seed),
        "runtime": {"dtype": str(runtime[0]), "device": str(runtime[1])},
        "orbit": {
            "train": data.records["train"],
            "score": data.records["score"],
            "beside": data.records["beside"],
            "window": {
                "t_start": float(times[0]),
                "t_end": float(times[-1]),
                "n_points": int(times.shape[0]),
                "configured_length": float(resolved.window_length),
                "basis": "physical times of the training samples",
            },
            "two_kepler_initial_state": (
                "the train record's first in-window snapshot (true_r0, true_v0)"
            ),
        },
        "steps": {"requested": int(steps), "completed": len(losses)},
        "optimizer": {
            "kind": "adam_constant_rate",
            "lr": float(resolved.learning_rate),
            "betas": [float(beta) for beta in options.adam_betas],
            "eps": float(options.adam_eps),
            "scheduler": None,
            "physics_term": None,
            "polish": None,
        },
        "similarity": similarity,
        "loss": {"final": losses[-1], "trace": losses},
        "timing": {
            "basis": TIMING_BASIS,
            "wall_seconds": float(wall),
            "seconds_per_step": float(wall) / len(losses),
            "completed_steps": len(losses),
        },
        "scores": {"network": score.to_json_dict()},
        "comparisons": comparisons,
        "weights": weights_block,
        "source_sha256": pinned_source_hashes(repo_root=repo_root),
        "access": {
            "reads": dict(context.reader.read_counts()),
            "attestation": (
                context.attestation.summary() if context.attestation is not None else None
            ),
        },
    }
    write_record_exclusive(
        record_path, record,
        data_root=getattr(context.reader, "data_root", None),
    )
    return record
