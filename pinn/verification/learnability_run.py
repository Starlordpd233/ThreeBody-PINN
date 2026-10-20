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

A real arm sizes itself (D-02, GAP-60-04): a separate timing run of the exact arm
configuration measures seconds per step, ``steps_budget`` turns that into the arm's
step budget B at the frozen 3-hour cap, and the cosine runs over exactly B. The
timing network is discarded and the arm starts from its own seed-42 initialization.
``drive_adam`` reads the scorer at the frozen cadence and branches only on what
``budget_outcome`` returns (complete, one extension, or inconclusive with a rate)
and on divergence (GAP-60-06). An improvement rate that cannot be determined raises
``OwnerRouted``: the runner writes ``owner-stop.json`` and the Adam weights and then
re-raises it, and nothing catches it and retries (T-60-11).
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
from pinn.constants import (
    PHYS05_LAMBDA_E_MAX,
    PHYS05_LAMBDA_IC_ADVISORY,
    PHYS05_LAMBDA_L_MAX,
    PHYS05_LAMBDA_PHYS_MAX,
    SIREN_FIRST_OMEGA_0,
)
from pinn.network import build_network
from pinn.training.atomic_io import atomic_write_torch
from pinn.training.config import OptConfig
from pinn.training.controllers import _tensor_hash
from pinn.training.grad_clip import DEFAULT_C_STAGE_TABLE, DEFAULT_MEDIAN_FLOOR, GradClipper
from pinn.training.scheduled_weights import ScheduledWeights
from pinn.verification.feasibility_scorecard import (
    OwnerRouted,
    better_state,
    budget_outcome,
    polish_should_stop,
    scoring_cadence_ok,
    steps_budget,
)
from pinn.verification.diagnostic_architecture import build_network_with_first_omega
from pinn.verification.feasibility_scorer import score_network
from pinn.verification.learnability_arms import (
    FIXTURE_FORMULA_NOTE,
    RUN_SCHEMA,
    SEED,
    TIMING_STEPS,
    FirstResultExists,
    arm_evidence_dir,
    check_override,
    resolve_first_omega_0,
    write_record_exclusive,
)
from pinn.verification.learnability_data import HarnessHalt, load_arm_data
from pinn.verification.learnability_losses import (
    data_only_loss,
    data_polish_objective,
    release_chunk_memory,
)

__all__ = [
    "OWNER_STOP_FILE",
    "OWNER_STOP_SCHEMA",
    "budget_from_timing",
    "build_arm_network",
    "drive_adam",
    "make_adam",
    "make_clipper",
    "make_cosine",
    "make_scheduled_weights",
    "reading_steps",
    "run_arm",
    "save_weights",
    "start_second_cosine",
    "timing_run",
    "timing_steps_for",
    "weights_digest",
    "write_owner_stop",
]

OWNER_STOP_SCHEMA = "phase60-owner-stop/v1"
OWNER_STOP_FILE = "owner-stop.json"
_BUDGET_OUTCOME_STAGE = "budget_outcome"
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
    """The production network, seed 42, at the requested first-layer frequency.

    The locked value is built by the production ``build_network``. Any other value
    comes from ``build_network_with_first_omega``, which leaves ``ArchitectureSpec``
    omega-locked. Whether an arm may use a non-locked value is decided earlier, by
    ``check_override`` in ``run_arm``; this function only builds.
    """
    if first_omega_0 == SIREN_FIRST_OMEGA_0:
        return build_network(ArchitectureSpec(seed=SEED), dtype=dtype, device=device)
    return build_network_with_first_omega(first_omega_0, seed=SEED, dtype=dtype, device=device)


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


def _timing_minimum(scorecard):
    """The frozen minimum number of timing-run steps."""
    return int(scorecard.section("budget_rule")["timing_run_min_steps"])


def timing_steps_for(spec, *, scorecard):
    """GAP-60-04: 500 timing steps for a data-only arm, 50 for an arm with a physics term.

    Both counts must be at least the frozen minimum. A count below it is a
    harness error, not a value to clamp.
    """
    minimum = _timing_minimum(scorecard)
    for name, count in TIMING_STEPS.items():
        if count < minimum:
            raise HarnessHalt(
                f"the {name} timing run is {count} steps; the frozen minimum is {minimum}"
            )
    return TIMING_STEPS["data_only" if spec.loss_arm == "data_only" else "physics"]


def _synchronize(device):
    """Wait for queued MPS work. It acts only on an MPS device and probes nothing."""
    if device.type == "mps" and hasattr(torch, "mps") and hasattr(torch.mps, "synchronize"):
        torch.mps.synchronize()


def make_adam(model, lr_stage):
    """D-01: Adam on ``LR_k = 1e-3 x 0.7^k`` with the trainer's betas and epsilon.

    Every constant comes from the trainer's ``OptConfig``; there is no literal rate here.
    """
    opt = OptConfig()
    return torch.optim.Adam(
        model.parameters(), lr=opt.lr_for_stage(lr_stage), betas=opt.adam_betas, eps=opt.adam_eps
    )


def make_cosine(optimizer, t_max, *, last_epoch=-1):
    """D-01, D-02: cosine annealing to zero over ``t_max`` steps, as the trainer builds it."""
    return torch.optim.lr_scheduler.CosineAnnealingLR(
        optimizer, T_max=max(t_max, 1), last_epoch=last_epoch
    )


def start_second_cosine(optimizer, t_max):
    """D-03: the one extension, a second cosine of length ``t_max`` on the same optimizer.

    Every parameter group's rate goes back to its initial rate and a new cosine starts
    from there, so the rate trace over ``[B, 2B)`` equals the trace over ``[0, B)``. The
    optimizer is not rebuilt, so Adam's moments and step count carry on. Continuing the
    first scheduler would climb back up, and a new scheduler without the reset would stay
    at zero.
    """
    for group in optimizer.param_groups:
        group["lr"] = group["initial_lr"]
    return torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=max(t_max, 1))


def make_scheduled_weights(budget, lr_stage):
    """D-01: the PHYS-05 warmup for an arm with a physics term, over the arm's budget.

    The warmup length is ``min(2000, floor(0.1 B))``. The stage maxima are the PHYS-05
    table entries. The extension never calls ``rewarm()``, so the ramp is not repeated.
    """
    return ScheduledWeights(
        budget,
        lambda_phys_max=PHYS05_LAMBDA_PHYS_MAX[lr_stage],
        lambda_e_max=PHYS05_LAMBDA_E_MAX[lr_stage],
        lambda_l_max=PHYS05_LAMBDA_L_MAX[lr_stage],
        lambda_ic=PHYS05_LAMBDA_IC_ADVISORY,
    )


def make_clipper():
    """GAP-60-03: the trainer's median-based Adam clipper with its stage table and median floor."""
    return GradClipper(c_stage_table=dict(DEFAULT_C_STAGE_TABLE), median_floor=DEFAULT_MEDIAN_FLOOR)


def _gradients_finite(parameters):
    return all(
        parameter.grad is None or bool(torch.isfinite(parameter.grad).all())
        for parameter in parameters
    )


class _AdamStepper:
    """One Adam step of a data-only arm. The timing run and the arm take the same step.

    Every step zeroes the gradients, computes the loss and clips with the trainer's clipper
    at the arm's clip stage when clipping is on (GAP-60-03). It then checks the loss and the
    clip outcome before ``optimizer.step()`` (GAP-60-06): on a non-finite value the step is
    skipped and its name is returned, so Adam ends at the last finite state. With clipping
    off there is no clip outcome, so the gradients themselves are checked.
    """

    def __init__(self, model, data, optimizer, scheduler, clipper, clip_stage, *, dtype, device):
        self.model = model
        self.data = data
        self.optimizer = optimizer
        self.scheduler = scheduler
        self.clipper = clipper
        self.clip_stage = clip_stage
        self.dtype = dtype
        self.device = device
        self.clipped_steps = 0
        self._parameters = list(model.parameters())

    def step(self, _index):
        """Take one step. Returns ``None``, or the name of a non-finite quantity that skipped it."""
        self.optimizer.zero_grad(set_to_none=True)
        loss = data_only_loss(
            self.model, self.data.data_points, dtype=self.dtype, device=self.device
        )
        loss.backward()
        outcome = None
        if self.clipper is not None:
            outcome = self.clipper.clip(self._parameters, stage=self.clip_stage)
        if not math.isfinite(float(loss)):
            return "non_finite_loss"
        if outcome is None:
            if not _gradients_finite(self._parameters):
                return "non_finite_gradient"
        elif outcome.non_finite:
            return "non_finite_clip_outcome"
        elif float(outcome.total_norm) > outcome.clip_value:
            self.clipped_steps += 1
        self.optimizer.step()
        self.scheduler.step()
        return None


def timing_run(
    spec,
    *,
    context,
    scorecard,
    runtime,
    first_omega_0,
    steps,
    clip_enabled=True,
    data=None,
    clock=time.monotonic,
):
    """GAP-60-04: time ``steps`` Adam steps of the exact arm configuration, then discard everything.

    A fresh network, optimizer, cosine and clipper are built for the arm's record, loss,
    first-layer frequency, stage and clipping setting. Every step is timed, the first one
    included. MPS work is synchronized before the clock is first read and again after the
    last step, before it is read for the second time. The network, optimizer and clipper are
    dropped on return and the arm starts from its own seed-42 initialization. ``data`` may
    be passed to reuse the arm's already-loaded record. Returns
    ``{steps, wall_seconds, seconds_per_step}``.
    """
    dtype, device = _resolve_runtime(runtime)
    minimum = _timing_minimum(scorecard)
    if isinstance(steps, bool) or not isinstance(steps, int) or steps < minimum:
        raise HarnessHalt(f"a timing run takes an integer of at least {minimum} steps; got {steps!r}")
    if data is None:
        data = load_arm_data(spec, context, scorecard=scorecard, dtype=dtype, device=device)
    model = build_arm_network(first_omega_0, dtype=dtype, device=device)
    optimizer = make_adam(model, spec.lr_stage)
    scheduler = make_cosine(optimizer, steps)
    clipper = make_clipper() if clip_enabled else None
    stepper = _AdamStepper(
        model, data, optimizer, scheduler, clipper, spec.clip_stage, dtype=dtype, device=device
    )
    _synchronize(device)
    started = clock()
    for index in range(1, steps + 1):
        stepper.step(index)
    _synchronize(device)
    wall = clock() - started
    del stepper, clipper, scheduler, optimizer, model
    release_chunk_memory(device)
    return {"steps": steps, "wall_seconds": wall, "seconds_per_step": wall / steps}


def budget_from_timing(timing, *, scorecard):
    """D-02: the arm's step budget B, the frozen 3-hour cap over the timing run's seconds per step."""
    cap_hours = float(scorecard.section("budget_rule")["cap_hours_single_system"])
    return steps_budget(
        cap_hours, timing["wall_seconds"], timing["steps"], scorecard=scorecard
    )


def reading_steps(budget, *, scorecard, through=None, enforce_cadence=True):
    """Steps 0, every ``max(1, floor(f * B))`` steps, and ``B``; the same interval on to ``through``.

    ``through`` is ``B`` until the frozen rule grants the one extension, and then its
    ``new_budget_steps``. With ``enforce_cadence`` the readings must meet
    ``scoring_cadence_ok`` for ``B`` and for ``through``, else ``HarnessHalt``. A fixture
    budget below 20 steps cannot meet a 5% gap with whole steps, so a fixture passes False.
    """
    horizon = budget if through is None else through
    for name, value in (("budget", budget), ("through", horizon)):
        if isinstance(value, bool) or not isinstance(value, int) or value < 1:
            raise HarnessHalt(f"{name} must be a positive integer; got {value!r}")
    if horizon < budget:
        raise HarnessHalt(f"through ({horizon}) must not be below the budget ({budget})")
    fraction = float(scorecard.section("budget_rule")["scoring_cadence_max_fraction"])
    stride = max(1, math.floor(fraction * budget))
    steps = sorted(set(range(0, horizon, stride)) | {budget, horizon})
    if enforce_cadence:
        first = [step for step in steps if step <= budget]
        if not (
            scoring_cadence_ok(first, budget, scorecard=scorecard)
            and scoring_cadence_ok(steps, horizon, scorecard=scorecard)
        ):
            raise HarnessHalt(
                f"readings every {stride} steps cannot meet the frozen scoring cadence at a "
                f"budget of {budget} (through {horizon})"
            )
    return steps


def drive_adam(
    *,
    budget,
    step_fn,
    read_fn,
    scorecard,
    on_extend,
    clock,
    enforce_cadence=True,
):
    """The budget driver. It branches only on ``budget_outcome`` and on divergence.

    ``step_fn(step)`` takes Adam step number ``step`` and returns ``None``, or a short name
    for the non-finite quantity that made it skip the optimizer step (GAP-60-06).
    ``read_fn(step)`` scores the current network and returns ``E``. ``on_extend()`` is called
    once, when the frozen rule grants the extension. At the end of the budget the frozen
    ``budget_outcome`` decides: complete, extend once to its ``new_budget_steps``, or (after
    the extension) inconclusive with a rate. An ``OwnerRouted`` it raises propagates
    unchanged. A skipped step ends Adam at the last finite state: ``budget_outcome`` is not
    called and no reading is invented. Adam's wall time is the sum of every step and every
    reading (GAP-60-05).
    """
    if isinstance(budget, bool) or not isinstance(budget, int) or budget < 1:
        raise HarnessHalt(f"the Adam budget must be a positive integer; got {budget!r}")
    horizon = budget
    planned = frozenset(
        reading_steps(budget, scorecard=scorecard, through=horizon, enforce_cadence=enforce_cadence)
    )
    readings = []
    adam_seconds = 0.0
    step = 0
    extended = False
    new_budget_steps = None
    rate_per_step = None
    diverged_at_step = None
    diverged_by = None
    outcome = None
    started = clock()
    readings.append([step, read_fn(step)])
    adam_seconds += clock() - started
    while outcome is None:
        if step == horizon:
            verdict = budget_outcome(readings, horizon, extended=extended, scorecard=scorecard)
            if verdict["outcome"] == "extend":
                new_budget_steps = verdict["new_budget_steps"]
                horizon = new_budget_steps
                extended = True
                on_extend()
                planned = frozenset(
                    reading_steps(
                        budget, scorecard=scorecard, through=horizon,
                        enforce_cadence=enforce_cadence,
                    )
                )
            else:
                outcome = verdict["outcome"]
                rate_per_step = verdict.get("rate_per_step")
            continue
        step += 1
        started = clock()
        skipped_for = step_fn(step)
        adam_seconds += clock() - started
        if skipped_for is not None:
            outcome = "diverged"
            diverged_at_step = step
            diverged_by = skipped_for
            continue
        if step in planned:
            started = clock()
            readings.append([step, read_fn(step)])
            adam_seconds += clock() - started
    return {
        "outcome": outcome,
        "budget_steps": budget,
        "extended": extended,
        "new_budget_steps": new_budget_steps,
        "rate_per_step": rate_per_step,
        "diverged_at_step": diverged_at_step,
        "diverged_by": diverged_by,
        "steps_taken": step if diverged_at_step is None else diverged_at_step - 1,
        "readings": readings,
        "reading_steps": [item[0] for item in readings],
        "adam_seconds": adam_seconds,
    }


def write_owner_stop(arm_dir, *, stage, reason, details, data_root=None):
    """Write ``owner-stop.json`` for an owner-routed stop. It is created once and never replaced.

    ``run_arm`` refuses to start an arm that has one, so the stop stays in front of the owner.
    Returns the SHA-256 of the bytes written.
    """
    if not isinstance(stage, str) or not stage:
        raise HarnessHalt(f"an owner stop names the stage it stopped in; got {stage!r}")
    payload = {
        "schema": OWNER_STOP_SCHEMA,
        "diagnostic": True,
        "stage": stage,
        "reason": str(reason),
        "details": details,
    }
    return write_record_exclusive(Path(arm_dir) / OWNER_STOP_FILE, payload, data_root=data_root)


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


def _checked_steps(value, name, minimum):
    if isinstance(value, bool) or not isinstance(value, int) or value < minimum:
        raise HarnessHalt(f"{name} must be an integer of at least {minimum}; got {value!r}")
    return value


def run_arm(
    spec,
    *,
    context,
    scorecard,
    runtime,
    evidence_root,
    fixture_budget_steps=None,
    fixture_timing_steps=None,
    clip_enabled=True,
    ruling=None,
    clock=time.monotonic,
):
    """Run one data-only arm end to end and return the record it wrote.

    ``runtime`` is a ``(dtype name, device name)`` pair. A real arm sizes itself: its own
    timing run (``timing_steps_for`` steps) gives seconds per step, ``budget_from_timing``
    gives the budget B, and ``drive_adam`` runs the cosine over B under the frozen budget
    rule. A fixture arm (both the arm and the context are fixtures) names its own small
    ``fixture_budget_steps`` and may name ``fixture_timing_steps`` (default: the frozen
    minimum). The record then holds the budget the frozen rule would have given, beside
    the fixture's. A real arm refuses both fixture knobs. ``clip_enabled`` turns the
    trainer's gradient clipper on for the timing run and the arm (GAP-60-03); the launcher
    passes the run protocol's ``clip_data_only_arms``. ``ruling`` is the committed D-11
    ruling an ``owner_approved`` arm needs (duck-typed: ``answer`` and
    ``approved_first_omega_0``); without one that arm is refused.

    The first-layer frequency is resolved and authorized before anything else
    (INST-05(e)): an arm that is not entitled to its setting raises
    ``OverrideRefused`` before any data is read, any network is built or any file
    is written. An ``OwnerRouted`` from the budget outcome writes ``owner-stop.json`` and
    the Adam weights, then propagates unchanged (T-60-11).
    """
    first_omega_0 = resolve_first_omega_0(spec, scorecard=scorecard, ruling=ruling)
    check_override(spec, first_omega_0, scorecard=scorecard, ruling=ruling)
    dtype, device = _resolve_runtime(runtime)
    if spec.run_kind != context.run_kind:
        raise HarnessHalt(
            f"arm {spec.arm_id} is a {spec.run_kind} arm but its data context is a "
            f"{context.run_kind} context"
        )
    fixture = spec.run_kind == "fixture"
    if fixture:
        budget = _checked_steps(fixture_budget_steps, "fixture_budget_steps", 1)
        timing_steps = (
            _timing_minimum(scorecard)
            if fixture_timing_steps is None
            else _checked_steps(fixture_timing_steps, "fixture_timing_steps", _timing_minimum(scorecard))
        )
    else:
        if fixture_budget_steps is not None or fixture_timing_steps is not None:
            raise HarnessHalt(
                "fixture_budget_steps and fixture_timing_steps are legal only for a fixture "
                "arm on a fixture context"
            )
        budget = None
        timing_steps = timing_steps_for(spec, scorecard=scorecard)
    if spec.loss_arm != "data_only":
        raise HarnessHalt(
            f"this runner trains data-only arms; loss_arm {spec.loss_arm!r} has no physics step here"
        )
    arm_dir = arm_evidence_dir(spec.arm_id, evidence_root=evidence_root)
    record_path = arm_dir / "record.json"
    if record_path.exists():
        raise FirstResultExists(
            f"a record already exists for arm {spec.arm_id}; the first completed run is the "
            "result and a second run never replaces it"
        )
    if (arm_dir / OWNER_STOP_FILE).exists():
        raise FirstResultExists(
            f"arm {spec.arm_id} stopped for the owner and has {OWNER_STOP_FILE}; the owner "
            "decides what happens next, and a second run never replaces that stop"
        )
    total_started = clock()
    data = load_arm_data(spec, context, scorecard=scorecard, dtype=dtype, device=device)

    # D-02, GAP-60-04: the budget comes from this arm's own timing run. The timing network
    # is gone by the time the arm builds its own, from the seed-42 initialization.
    timing = timing_run(
        spec,
        context=context,
        scorecard=scorecard,
        runtime=runtime,
        first_omega_0=first_omega_0,
        steps=timing_steps,
        clip_enabled=clip_enabled,
        data=data,
        clock=clock,
    )
    frozen_budget = budget_from_timing(timing, scorecard=scorecard)
    if budget is None:
        budget = frozen_budget
    if budget < 1:
        raise HarnessHalt(
            f"the frozen budget for arm {spec.arm_id} is {budget} steps; no arm can be run"
        )

    torch.manual_seed(SEED)
    model = build_arm_network(first_omega_0, dtype=dtype, device=device)
    opt = OptConfig()
    learning_rate = opt.lr_for_stage(spec.lr_stage)
    optimizer = make_adam(model, spec.lr_stage)
    scheduler = make_cosine(optimizer, budget)
    clipper = make_clipper() if clip_enabled else None
    stepper = _AdamStepper(
        model, data, optimizer, scheduler, clipper, spec.clip_stage, dtype=dtype, device=device
    )

    stopped = {"extended": False}

    def on_extend():
        # D-03: the second cosine, on the same optimizer so Adam's moments are kept.
        stopped["extended"] = True
        stepper.scheduler = start_second_cosine(optimizer, budget)

    # A fixture budget below 20 steps cannot meet the frozen 5% cadence with whole
    # steps, so it is recorded against the rule but not held to it. A real arm is.
    enforce_cadence = not fixture
    trace = []
    adam_started = clock()
    latest = {}

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
        latest["result"], latest["step"] = result, step
        return float(result.E)

    try:
        driven = drive_adam(
            budget=budget,
            step_fn=stepper.step,
            read_fn=take_reading,
            scorecard=scorecard,
            on_extend=on_extend,
            clock=clock,
            enforce_cadence=enforce_cadence,
        )
    except OwnerRouted as stop:
        weights_file_sha, weights_tensor_digest = save_weights(arm_dir / "adam.weights", model)
        write_owner_stop(
            arm_dir,
            stage=_BUDGET_OUTCOME_STAGE,
            reason=str(stop),
            details={
                "arm_id": spec.arm_id,
                "budget_steps": budget,
                "extended": stopped["extended"],
                "readings": [[entry["step"], entry["E"]] for entry in trace],
                "timing": timing,
                "weights": {
                    "file": "adam.weights",
                    "sha256": weights_file_sha,
                    "tensor_digest": weights_tensor_digest,
                },
            },
            data_root=context.reader.data_root,
        )
        raise
    if not _all_finite(model.parameters()):
        # GAP-60-06: Adam ends at the last finite state, so this should not happen. If the
        # weights are not finite there is no polish, and the scorer refuses a non-finite
        # network, so no result can be formed. The arm stops and nothing is written.
        raise HarnessHalt(
            f"the Adam weights of arm {spec.arm_id} are not finite after step "
            f"{driven['steps_taken']}; no result can be scored and no polish is run"
        )
    adam_gold = latest["result"]
    if latest["step"] != driven["steps_taken"]:
        # GAP-60-06: Adam ended in a state no reading covered (a step was skipped between
        # two readings). That last finite state is scored now. It is not a budget reading.
        adam_gold = _score(model, data, data.score, scorecard=scorecard, dtype=dtype, device=device)
    adam_seconds = driven["adam_seconds"]
    diverged = driven["outcome"] == "diverged"
    final_budget = budget if driven["new_budget_steps"] is None else driven["new_budget_steps"]
    cadence_ok = (
        None if diverged
        else scoring_cadence_ok(driven["reading_steps"], final_budget, scorecard=scorecard)
    )

    clip_settings = (clipper if clipper is not None else make_clipper()).state_dict()

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
        "grid_omega": spec.grid_omega,
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
            "cosines": 2 if driven["extended"] else 1,
        },
        "timing": timing,
        "budget": {
            "rule": "fixture" if fixture else "frozen",
            "budget_steps": budget,
            "frozen_budget_steps": frozen_budget,
            "reading_steps": driven["reading_steps"],
            "readings": driven["readings"],
            "outcome": driven["outcome"],
            "extended": driven["extended"],
            "new_budget_steps": driven["new_budget_steps"],
            "rate_per_step": driven["rate_per_step"],
            "diverged_at_step": driven["diverged_at_step"],
            "diverged_by": driven["diverged_by"],
            "cadence_ok": cadence_ok,
            "cadence_enforced": enforce_cadence,
        },
        "clip": {
            "stage": spec.clip_stage,
            "multiplier": clip_settings["c_stage_table"][spec.clip_stage],
            "median_floor": clip_settings["median_floor"],
            "enabled": clip_enabled,
            "clipped_steps": stepper.clipped_steps,
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
