"""Phase 60 (INST-05): the arm runner of the learnability harness.

One arm trains the production network on one named record with the trainer's
own data loss, runs Adam on the Stage-0 cosine, then the frozen full-batch
L-BFGS polish, scores both states on the scored grid and on the grid beside it,
and writes one record and two weights files. The record is created exactly
once: a second run of the same arm raises ``FirstResultExists`` before any
optimizer step. A harness weights file is a plain state dict. It is not a
production checkpoint, no run directory is created for it, and the evaluator
refuses it. The frozen rules (cadence, polish stop, better state) are called
from the scorecard module and never re-implemented.
"""

from __future__ import annotations

# Capture before Torch import: the record states whether the fallback was set.
import os as _os

_PRE_IMPORT_FALLBACK = _os.environ.get("PYTORCH_ENABLE_MPS_FALLBACK") or None

import hashlib
import math
import time
from collections import OrderedDict
from pathlib import Path

import torch

from pinn.architecture_spec import ArchitectureSpec
from pinn.constants import SIREN_FIRST_OMEGA_0
from pinn.network import build_network
from pinn.training.atomic_io import atomic_write_torch
from pinn.training.config import OptConfig
from pinn.training.controllers import _tensor_hash
from pinn.verification.feasibility_scorecard import (
    better_state,
    polish_should_stop,
    scoring_cadence_ok,
)
from pinn.verification.feasibility_scorer import score_network
from pinn.verification.learnability_arms import (
    FIXTURE_FORMULA_NOTE,
    RUN_SCHEMA,
    SEED,
    FirstResultExists,
    arm_evidence_dir,
    write_record_exclusive,
)
from pinn.verification.learnability_data import HarnessHalt, load_arm_data
from pinn.verification.learnability_losses import data_only_loss, data_polish_objective

__all__ = [
    "build_arm_network",
    "run_arm",
    "save_weights",
    "weights_digest",
]

_DTYPES = {"float32": torch.float32, "float64": torch.float64}
_D04_NOTE = (
    "D-04: every data-only arm uses the Stage-0 cosine (k = 0), so the 75%-100% window "
    "of the frozen still-improving test is the low-rate tail of that cosine."
)


def _resolve_runtime(runtime):
    """Map a ``(dtype name, device name)`` pair to torch objects. No availability probe."""
    try:
        dtype_name, device_name = runtime
        return _DTYPES[dtype_name], torch.device(device_name)
    except (KeyError, TypeError, ValueError, RuntimeError) as exc:
        raise HarnessHalt(
            f"runtime must be a (dtype, device) pair such as ('float32', 'mps'); got {runtime!r}"
        ) from exc


def build_arm_network(first_omega_0, *, dtype, device):
    """The production network, seed 42. Only the locked first-layer frequency is built here."""
    if float(first_omega_0) != float(SIREN_FIRST_OMEGA_0):
        raise HarnessHalt(
            f"first_omega_0 {first_omega_0!r} is not the locked {SIREN_FIRST_OMEGA_0}; "
            "this builder constructs only the locked network"
        )
    return build_network(ArchitectureSpec(seed=SEED), dtype=dtype, device=device)


def weights_digest(state_dict):
    """One SHA-256 over every tensor's name and canonical digest, in sorted-name order.

    A tensor's canonical digest is ``controllers._tensor_hash``: dtype, shape
    and bytes of the CPU-contiguous tensor.
    """
    digest = hashlib.sha256()
    for name in sorted(state_dict):
        digest.update(name.encode("utf-8"))
        digest.update(b"\0")
        digest.update(_tensor_hash(state_dict[name]).encode("ascii"))
        digest.update(b"\n")
    return digest.hexdigest()


def save_weights(path, model):
    """Write the model's CPU state dict, in its own dtype, atomically.

    Returns ``(file SHA-256, canonical tensor digest)``. The file is a plain
    ``OrderedDict`` of tensors, so ``torch.load(..., weights_only=True)`` reads it.
    """
    state = OrderedDict(
        (name, tensor.detach().cpu().clone()) for name, tensor in model.state_dict().items()
    )
    atomic_write_torch(path, state)
    return hashlib.sha256(Path(path).read_bytes()).hexdigest(), weights_digest(state)


def _reading_steps(budget, scorecard):
    """Steps 0, every ``max(1, floor(f * B))`` steps, and ``B``."""
    fraction = float(scorecard.section("budget_rule")["scoring_cadence_max_fraction"])
    stride = max(1, math.floor(fraction * budget))
    return sorted(set(range(0, budget, stride)) | {budget})


def _score(model, data, view, *, scorecard, dtype, device):
    return score_network(
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


def _all_finite(parameters):
    return all(bool(torch.isfinite(parameter).all()) for parameter in parameters)


def _polish(model, data, *, scorecard, adam_seconds, adam_gold, dtype, device, clock):
    """The frozen full-batch L-BFGS polish (GAP-60-05).

    One outer call is one ``LBFGS.step(closure)``. A call improves when the
    closure objective at the iterate it ends with is strictly below the best so
    far, starting from the objective at the Adam result. ``polish_should_stop``
    runs after every call. The polish state is the iterate after the last call,
    or the parameters from before a call that produced a non-finite objective
    or non-finite parameters. The scored ``E`` is logged and never steers it.

    Returns ``(stop_reason, outer_calls, trace, gold_result)`` where
    ``gold_result`` is the scored-grid result of the polish state.
    """
    settings = scorecard.section("lbfgs_polish")
    parameters = list(model.parameters())
    optimizer = torch.optim.LBFGS(
        parameters,
        history_size=int(settings["lbfgs_history_size"]),
        max_iter=int(settings["lbfgs_max_iter"]),
        line_search_fn=str(settings["lbfgs_line_search"]),
    )
    chunk_size = OptConfig().lbfgs_chunk_size

    def closure():
        return data_polish_objective(
            model, data.data_points, chunk_size=chunk_size, dtype=dtype, device=device
        )

    started = clock()
    best = float(closure())
    state_result = adam_gold
    without_improvement = 0
    outer_calls = 0
    trace = []
    while True:
        before = [parameter.detach().clone() for parameter in parameters]
        returned = float(optimizer.step(closure))
        outer_calls += 1
        objective = float(closure())
        if not (math.isfinite(returned) and math.isfinite(objective) and _all_finite(parameters)):
            with torch.no_grad():
                for parameter, saved in zip(parameters, before):
                    parameter.copy_(saved)
            trace.append(
                {
                    "call": outer_calls,
                    "objective": objective,
                    "best_objective": best,
                    "improved": False,
                    "calls_without_improvement": without_improvement,
                    "restored": True,
                    "E": None,
                    "eps_h": None,
                    "tier": None,
                    "elapsed_seconds": clock() - started,
                }
            )
            reason = (
                f"non_finite: outer call {outer_calls} gave a non-finite objective or "
                "parameters; the parameters from before that call are the polish state"
            )
            return reason, outer_calls, trace, state_result
        improved = objective < best
        if improved:
            best = objective
            without_improvement = 0
        else:
            without_improvement += 1
        state_result = _score(
            model, data, data.score, scorecard=scorecard, dtype=dtype, device=device
        )
        scored = state_result.to_json_dict()
        polish_seconds = clock() - started
        trace.append(
            {
                "call": outer_calls,
                "objective": objective,
                "best_objective": best,
                "improved": improved,
                "calls_without_improvement": without_improvement,
                "restored": False,
                "E": scored["E"],
                "eps_h": scored["eps_h"],
                "tier": scored["tier"],
                "elapsed_seconds": polish_seconds,
            }
        )
        if polish_should_stop(without_improvement, polish_seconds, adam_seconds, scorecard=scorecard):
            if polish_should_stop(without_improvement, 0.0, adam_seconds, scorecard=scorecard):
                reason = (
                    f"no_improvement_calls: {without_improvement} outer calls in a row "
                    "without a lower objective"
                )
            else:
                reason = (
                    f"adam_wall_fraction: polish wall {polish_seconds:.6f} s reached the "
                    f"frozen fraction of the summed Adam wall {adam_seconds:.6f} s"
                )
            return reason, outer_calls, trace, state_result


def run_arm(
    spec,
    *,
    context,
    scorecard,
    runtime,
    evidence_root,
    fixture_budget_steps=None,
    clock=time.monotonic,
):
    """Run one data-only arm end to end and return the record it wrote.

    ``runtime`` is a ``(dtype name, device name)`` pair. A ``fixture_budget_steps``
    value is legal only when both the context and the arm are fixtures; the
    frozen budget rule for real arms is added by the budget driver.
    """
    dtype, device = _resolve_runtime(runtime)
    fixture = spec.run_kind == "fixture" and context.run_kind == "fixture"
    if fixture_budget_steps is not None and not fixture:
        raise HarnessHalt("fixture_budget_steps is legal only for a fixture arm on a fixture context")
    if not fixture:
        raise HarnessHalt("a real arm needs the frozen budget rule, which is not available here")
    budget = fixture_budget_steps
    if isinstance(budget, bool) or not isinstance(budget, int) or budget < 1:
        raise HarnessHalt(f"fixture_budget_steps must be a positive integer; got {budget!r}")
    if spec.loss_arm != "data_only":
        raise HarnessHalt(
            f"this runner trains data-only arms; loss_arm {spec.loss_arm!r} has no physics step here"
        )
    if spec.grid_omega is not None or spec.omega_provenance != "locked":
        raise HarnessHalt("this runner builds only the locked first_omega_0; no override is routed")
    arm_dir = arm_evidence_dir(spec.arm_id, evidence_root=evidence_root)
    record_path = arm_dir / "record.json"
    if record_path.exists():
        raise FirstResultExists(
            f"a record already exists for arm {spec.arm_id}; the first completed run is the "
            "result and a second run never replaces it"
        )
    total_started = clock()
    torch.manual_seed(SEED)
    first_omega_0 = float(SIREN_FIRST_OMEGA_0)
    model = build_arm_network(first_omega_0, dtype=dtype, device=device)
    data = load_arm_data(spec, context, scorecard=scorecard, dtype=dtype, device=device)

    opt = OptConfig()
    learning_rate = opt.lr_for_stage(spec.lr_stage)
    optimizer = torch.optim.Adam(
        model.parameters(), lr=learning_rate, betas=opt.adam_betas, eps=opt.adam_eps
    )
    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=max(budget, 1))
    reading_steps = _reading_steps(budget, scorecard)
    # The frozen cadence allows a gap of 5% of the budget, which whole steps cannot
    # meet below 20 steps. A fixture budget is therefore recorded against the rule
    # but not held to it; the budget driver enforces it for real arms.
    cadence_ok = scoring_cadence_ok(reading_steps, budget, scorecard=scorecard)

    scheduled = frozenset(reading_steps)
    readings = []
    trace = []
    adam_started = clock()

    def take_reading(step):
        result = _score(model, data, data.score, scorecard=scorecard, dtype=dtype, device=device)
        scored = result.to_json_dict()
        trace.append(
            {
                "step": step,
                "E": scored["E"],
                "eps_h": scored["eps_h"],
                "tier": scored["tier"],
                "elapsed_seconds": clock() - adam_started,
            }
        )
        readings.append([step, float(result.E)])
        return result

    adam_gold = take_reading(0)
    for step in range(1, budget + 1):
        optimizer.zero_grad(set_to_none=True)
        loss = data_only_loss(model, data.data_points, dtype=dtype, device=device)
        loss.backward()
        optimizer.step()
        scheduler.step()
        if step in scheduled:
            adam_gold = take_reading(step)
    adam_seconds = clock() - adam_started

    adam_base = _score(model, data, data.beside, scorecard=scorecard, dtype=dtype, device=device)
    adam_file_sha, adam_tensor_digest = save_weights(arm_dir / "adam.weights", model)

    stop_reason, outer_calls, polish_trace, polish_gold = _polish(
        model,
        data,
        scorecard=scorecard,
        adam_seconds=adam_seconds,
        adam_gold=adam_gold,
        dtype=dtype,
        device=device,
        clock=clock,
    )
    polish_seconds = polish_trace[-1]["elapsed_seconds"]
    polish_base = _score(model, data, data.beside, scorecard=scorecard, dtype=dtype, device=device)
    polish_file_sha, polish_tensor_digest = save_weights(arm_dir / "polish.weights", model)

    chosen = better_state(
        {"E": adam_gold.E, "eps_h": adam_gold.eps_h},
        {"E": polish_gold.E, "eps_h": polish_gold.eps_h},
        scorecard=scorecard,
    )
    selected = (adam_gold if chosen == "adam" else polish_gold).to_json_dict()
    record = {
        "schema": RUN_SCHEMA,
        "diagnostic": True,
        "run_kind": spec.run_kind,
        "arm_id": spec.arm_id,
        "rung": spec.rung,
        "path": spec.path,
        "loss_arm": spec.loss_arm,
        "system_id": spec.system_id,
        "counted": spec.counted,
        "keys": {
            "train": data.records["train"]["record_key"],
            "score": data.records["score"]["record_key"],
            "beside": data.records["beside"]["record_key"],
        },
        "records": data.records,
        "first_omega_0": first_omega_0,
        "omega_provenance": spec.omega_provenance,
        "seed": SEED,
        "runtime": {"dtype": runtime[0], "device": runtime[1]},
        "normalizer": {
            "stats_sha256": context.stats_sha256,
            "source": context.normalizer_source,
        },
        "schedule": {
            "lr_stage": spec.lr_stage,
            "lr_k": learning_rate,
            "betas": list(opt.adam_betas),
            "eps": opt.adam_eps,
            "cosine_t_max": max(budget, 1),
        },
        "budget": {
            "rule": "fixture",
            "budget_steps": budget,
            "reading_steps": reading_steps,
            "readings": readings,
            "cadence_ok": cadence_ok,
            "cadence_enforced": False,
        },
        "trace": trace,
        "states": {
            "adam": {
                "score_gold": adam_gold.to_json_dict(),
                "score_base": adam_base.to_json_dict(),
                "weights": {
                    "file": "adam.weights",
                    "sha256": adam_file_sha,
                    "tensor_digest": adam_tensor_digest,
                },
            },
            "polish": {
                "score_gold": polish_gold.to_json_dict(),
                "score_base": polish_base.to_json_dict(),
                "weights": {
                    "file": "polish.weights",
                    "sha256": polish_file_sha,
                    "tensor_digest": polish_tensor_digest,
                },
                "outer_calls": outer_calls,
                "trace": polish_trace,
                "stop_reason": stop_reason,
            },
        },
        "better_state": chosen,
        "result": {
            "state": chosen,
            "tier": selected["tier"],
            "E": selected["E"],
            "e_in_max": selected["e_in_max"],
            "h": selected["h"],
            "eps_h": selected["eps_h"],
        },
        "formula": {"E_formula": FIXTURE_FORMULA_NOTE, "counts": None},
        "wall": {
            "adam_seconds": adam_seconds,
            "polish_seconds": polish_seconds,
            "total_seconds": clock() - total_started,
        },
        "attestation": None if context.attestation is None else context.attestation.summary(),
        "mps_fallback_env": _PRE_IMPORT_FALLBACK,
        "readout_notes": [_D04_NOTE],
    }
    write_record_exclusive(record_path, record, data_root=context.reader.data_root)
    return record
