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

An arm with a physics term (Rung 2a, Rung 2b, probe Rung-2b) trains under the same
ratified schedule. Each Adam step redraws the 4,096 stratified collocation rows from
the arm's own seed-42 numpy ``Generator`` and calls the trainer's memory-bounded step
through ``learnability_losses.physics_adam_step``; the loss weights come from the
PHYS-05 ``ScheduledWeights`` warmup of the same budget (D-01). A single frozen monitor
set is drawn before step 1 and ``frozen_monitor_log`` is recorded at every budget-rule
reading; nothing halts on invariant B or reads a front index to decide anything (D-06).
At the Adam-to-L-BFGS handoff the collocation rows, pass-1 causal weights, bin counts
and loss weights are frozen for the whole polish (GAP-60-05, 57-RULING.md:112-124).

Both scored states of every arm are re-scored on the CPU in float64 (GAP-60-07): the
same weights are widened on the CPU, the same float32-rounded normalized IC13 is fed
in, and the CPU tier and counts boolean must equal the official ones. Any difference
writes ``owner-stop.json``, raises ``CrossCheckDisagreement`` and never takes the
better of the two scores. A counted arm compares its position error with the committed
two-Kepler formula through the frozen ``counts``; a probe arm never calls it and
records ``not applicable: no hierarchical split``.

A real arm admitted by ``learnability_protocol.admit_arm`` carries its admission and
the loaded run protocol into ``build_real_record``, which fills every hash and version
SPEC Requirement 4 names beside every result field SPEC Requirement 5 names, and
``validate_record`` must accept the record before it is written (D-10).
"""

from __future__ import annotations

# Capture before Torch import: the record states whether the fallback was set.
import os as _os

_PRE_IMPORT_FALLBACK = _os.environ.get("PYTORCH_ENABLE_MPS_FALLBACK") or None

import copy
import hashlib
import json
import math
import os
import platform
import signal
import subprocess
import sys
import time
from collections import OrderedDict
from collections.abc import Mapping
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import torch

from pinn.architecture_spec import ArchitectureSpec
from pinn.constants import (
    PHYS05_LAMBDA_E_MAX,
    PHYS05_LAMBDA_IC_ADVISORY,
    PHYS05_LAMBDA_L_MAX,
    PHYS05_LAMBDA_PHYS_MAX,
    SIREN_FIRST_OMEGA_0,
)
from pinn.loss_catalog import _angular_momentum, _matched_plummer_hamiltonian
from pinn.network import build_network
from pinn.training.atomic_io import atomic_write_torch
from pinn.training.config import R_REF_ARTIFACT_RELATIVE_PATH, OptConfig
from pinn.training.controllers import _tensor_hash
from pinn.training.determinism import capture_rng_state, restore_rng_state
from pinn.training.grad_clip import DEFAULT_C_STAGE_TABLE, DEFAULT_MEDIAN_FLOOR, GradClipper
from pinn.training.scheduled_weights import LossWeights, ScheduledWeights
from pinn.verification import evidence_io
from pinn.verification.learnability_protocol import (
    AdmissionRefused,
    admit_arm,
    load_protocol,
)
from pinn.verification.feasibility_scorecard import (
    OwnerRouted,
    better_state,
    budget_outcome,
    counts,
    load_scorecard,
    polish_should_stop,
    scoring_cadence_ok,
    steps_budget,
)
from pinn.verification.diagnostic_architecture import build_network_with_first_omega
from pinn.verification.feasibility_scorer import score_network
from pinn.verification.learnability_arms import (
    EVIDENCE_REL,
    EXIT_OK,
    EXIT_OWNER,
    EXIT_REFUSED,
    EXIT_SIGHUP,
    EXIT_SIGINT,
    EXIT_SIGTERM,
    FIXTURE_FORMULA_NOTE,
    FORMULA_NOT_APPLICABLE,
    LOSS_ARMS,
    REAL_RUNTIME,
    RUN_SCHEMA,
    RUNS_REL,
    SEED,
    TIMING_STEPS,
    FirstResultExists,
    UnknownArm,
    arm_evidence_dir,
    arm_run_dir,
    arm_spec,
    check_override,
    resolve_first_omega_0,
    write_record_exclusive,
)
from pinn.verification.learnability_data import HarnessHalt, load_arm_data, open_real_context
from pinn.verification.learnability_losses import (
    data_only_loss,
    data_polish_objective,
    draw_collocation_times,
    frozen_monitor_log,
    make_trajectory,
    physics_adam_step,
    physics_pass1,
    physics_polish_objective,
    release_chunk_memory,
)

__all__ = [
    "CLAIM_FILE",
    "ClaimExists",
    "CrossCheckDisagreement",
    "GovernedStop",
    "OWNER_STOP_FILE",
    "OWNER_STOP_SCHEMA",
    "PROCESS_FILE",
    "REQUIRED_REAL_FIELDS",
    "RESUME_FILE",
    "RESUME_SCHEMA",
    "R_REF_NOTE",
    "ResumeRefused",
    "budget_from_timing",
    "build_arm_network",
    "build_real_record",
    "cross_check_state",
    "drive_adam",
    "formula_reference",
    "install_stop_handlers",
    "load_resume_checkpoint",
    "main",
    "make_adam",
    "make_clipper",
    "make_cosine",
    "make_scheduled_weights",
    "reading_steps",
    "request_stop",
    "run_arm",
    "save_resume_checkpoint",
    "save_weights",
    "start_second_cosine",
    "stop_requested",
    "timing_run",
    "timing_steps_for",
    "validate_record",
    "weights_digest",
    "write_owner_stop",
]

OWNER_STOP_SCHEMA = "phase60-owner-stop/v1"
OWNER_STOP_FILE = "owner-stop.json"
_BUDGET_OUTCOME_STAGE = "budget_outcome"
_CROSS_CHECK_STAGE = "cross_check"
COUNTS_STAGE = "counts"
_DTYPES = {"float32": torch.float32, "float64": torch.float64}
R_REF_NOTE = "Stage-0 reference in force, applied unchanged"
_D04_NOTE = (
    "D-04: every data-only arm uses the Stage-0 cosine (k = 0), so the 75%-100% window "
    "of the frozen still-improving test is the low-rate tail of that cosine."
)
_D05_NOTE = (
    "D-05: probe Rung-2b starts from scratch while the 0.7 factor assumes weights "
    "carried forward from the previous stage."
)
# The committed Phase 59 two-Kepler singles row: E_formula for every counted panel system.
TWO_KEPLER_REL = Path(
    ".planning/phases/59-read-only-baseline-scorecard/evidence/baselines/two_kepler.json"
)
# The ratified stratified draw: 16 bins x 256 slots of the one system = 4,096 rows.
_SLOTS = 256
_HEX64 = frozenset("0123456789abcdef")
_MISSING = object()

# The ignored resume tree of one arm (SPEC Requirement 8, SCOPE-44).
RESUME_SCHEMA = "phase60-resume/v1"
RESUME_FILE = "resume.pt"
CLAIM_SCHEMA = "phase60-arm-claim/v1"
CLAIM_FILE = "claim.json"
STOP_SCHEMA = "phase60-arm-stop/v1"
STOP_PREFIX = "stop-"
PROCESS_FILE = "process.json"
_RESUME_PHASES = ("timing", "adam", "polish")
# SIGHUP, SIGINT and SIGTERM: the three signals a checkpointed stop may resume from.
_GOVERNED_CODES = {
    signal.SIGHUP: EXIT_SIGHUP,
    signal.SIGINT: EXIT_SIGINT,
    signal.SIGTERM: EXIT_SIGTERM,
}
# Module state a signal handler writes and the runner reads at its safe boundaries.
_STOP = {"requested": False, "signum": None, "exit_code": None}


class GovernedStop(BaseException):
    """A governed signal asked the arm to stop and its checkpoint is already on disk.

    A ``BaseException`` for the same reason the trainer's ``_StopRequested`` is: no
    ordinary ``except Exception`` inside a run may swallow a stop.
    """

    def __init__(self, exit_code, *, signal_name=None, phase=None, step=None):
        super().__init__(f"governed stop after {signal_name or 'a signal'}: exit {exit_code}")
        self.exit_code = int(exit_code)
        self.signal_name = signal_name
        self.phase = phase
        self.step = step


class _StopRequested(BaseException):
    """Abort an in-progress L-BFGS outer call at its next closure evaluation."""


class ResumeRefused(RuntimeError):
    """The run tree cannot be resumed exactly. The arm goes to the owner."""


class ClaimExists(RuntimeError):
    """The arm's run tree is already claimed by an earlier invocation."""


def request_stop(signum):
    """Record a governed stop request for SIGHUP, SIGINT or SIGTERM. The first one wins.

    A signal handler may only set this flag: ``run_arm`` checkpoints at its next safe
    boundary (an Adam step boundary, a reading, or between polish outer calls) and then
    raises ``GovernedStop``. Returns the exit code (129, 130 or 143).
    """
    code = _GOVERNED_CODES.get(signum if isinstance(signum, int) else None)
    if code is None:
        raise ValueError(f"{signum!r} is not one of the governed stop signals")
    if not _STOP["requested"]:
        _STOP.update(requested=True, signum=int(signum), exit_code=code)
    return int(_STOP["exit_code"])


def stop_requested():
    """True when a governed stop has been requested and not yet acted on."""
    return bool(_STOP["requested"])


def _reset_stop():
    """Forget a stop request. Tests and a fresh command-line invocation start clean."""
    _STOP.update(requested=False, signum=None, exit_code=None)


def _signal_name(signum):
    try:
        return signal.Signals(int(signum)).name
    except (TypeError, ValueError):
        return "UNKNOWN"


def install_stop_handlers():
    """Install SIGHUP, SIGINT and SIGTERM handlers that only request a governed stop.

    ``pinn/training/signals.py`` has no SIGHUP handler and escalates a second SIGINT, so
    the arm carries its own three handlers here; that module is not edited. Returns a
    callable that restores the previous handlers.
    """
    previous = {number: signal.getsignal(number) for number in _GOVERNED_CODES}

    def handler(signum, _frame):
        request_stop(signum)

    for number in _GOVERNED_CODES:
        signal.signal(number, handler)

    def restore():
        for number, old in previous.items():
            if old is not None:
                signal.signal(number, old)

    return restore


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


def _guarded_update(stepper, loss, outcome):
    """GAP-60-06: check before ``optimizer.step()``; return a skipped-step name or ``None``.

    A non-finite loss, clip outcome or (with clipping off) gradient leaves the optimizer
    untouched, so Adam ends at the last finite state and no non-finite weight is written.
    """
    if not math.isfinite(float(loss)):
        return "non_finite_loss"
    if outcome is None:
        if not _gradients_finite(stepper._parameters):
            return "non_finite_gradient"
    elif outcome.non_finite:
        return "non_finite_clip_outcome"
    elif float(outcome.total_norm) > outcome.clip_value:
        stepper.clipped_steps += 1
    stepper.optimizer.step()
    stepper.scheduler.step()
    return None


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
        return _guarded_update(self, loss, outcome)


@dataclass
class _PhysicsInputs:
    """Everything a physics Adam step reads besides the model, optimizer and schedule.

    ``r_ref`` is the Stage-0 reference in force (the admission's value for a real arm, the
    fixture's explicit value for a fixture). ``eps_h`` is the admission's ``1e-4 x S_H`` and
    stays ``None`` where the stage's energy weight is zero and the term is never evaluated.
    """

    rng: object
    train_key: object
    n_slots: int
    r_ref: float
    h0: object
    l0: object
    eps_h: object
    ic13_t: object
    masses_t: object
    true_r0: object
    true_v0: object
    weights: object
    data_points: object
    microbatch_size: int


class _PhysicsStepper:
    """One Adam step of an arm with a physics term (D-01, D-06, GAP-60-05).

    Each step redraws the arm's stratified collocation rows from its own numpy
    ``Generator`` and runs the trainer's memory-bounded physics step through
    ``physics_adam_step``: pass 1 freezes the causal weights, the data and IC terms are
    back-propagated, then pass 2 walks the rows in chunks of at most 256. The loss weights
    are ``ScheduledWeights.current(step)``, the PHYS-05 warmup of the same budget. The
    same guard as the data-only step checks the returned total before ``optimizer.step()``.
    """

    def __init__(self, model, data, optimizer, scheduler, clipper, clip_stage, *, physics,
                 dtype, device):
        self.model = model
        self.data = data
        self.optimizer = optimizer
        self.scheduler = scheduler
        self.clipper = clipper
        self.clip_stage = clip_stage
        self.physics = physics
        self.dtype = dtype
        self.device = device
        self.clipped_steps = 0
        self._parameters = list(model.parameters())

    def step(self, index):
        """Take one step. Returns ``None``, or the name of a non-finite quantity that skipped it."""
        physics = self.physics
        self.optimizer.zero_grad(set_to_none=True)
        collocation_times = draw_collocation_times(
            physics.train_key, physics.rng, n_slots=physics.n_slots
        )
        terms = physics_adam_step(
            self.model,
            data_points=physics.data_points,
            ic13_t=physics.ic13_t,
            masses_t=physics.masses_t,
            true_r0=physics.true_r0,
            true_v0=physics.true_v0,
            collocation_times=collocation_times,
            weights=physics.weights.current(index),
            r_ref=physics.r_ref,
            h0=physics.h0,
            eps_h=physics.eps_h,
            l0=physics.l0,
            microbatch_size=physics.microbatch_size,
            dtype=self.dtype,
            device=self.device,
        )
        outcome = None
        if self.clipper is not None:
            outcome = self.clipper.clip(self._parameters, stage=self.clip_stage)
        return _guarded_update(self, terms["total"], outcome)


def _build_stepper(spec, model, data, optimizer, scheduler, clipper, *, physics, dtype, device):
    """The step object the timing run and the arm share, chosen by the arm's loss."""
    if physics is None:
        return _AdamStepper(
            model, data, optimizer, scheduler, clipper, spec.clip_stage,
            dtype=dtype, device=device,
        )
    return _PhysicsStepper(
        model, data, optimizer, scheduler, clipper, spec.clip_stage, physics=physics,
        dtype=dtype, device=device,
    )


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
    physics=None,
    clock=time.monotonic,
    stop_fn=None,
):
    """GAP-60-04: time ``steps`` Adam steps of the exact arm configuration, then discard everything.

    A fresh network, optimizer, cosine and clipper are built for the arm's record, loss,
    first-layer frequency, stage and clipping setting. Every step is timed, the first one
    included. MPS work is synchronized before the clock is first read and again after the
    last step, before it is read for the second time. The network, optimizer and clipper are
    dropped on return and the arm starts from its own seed-42 initialization. ``data`` may
    be passed to reuse the arm's already-loaded record. An arm with a physics term passes a
    ``_PhysicsInputs`` whose ``rng`` is the timing run's own throwaway generator and whose
    ``weights`` schedule covers ``steps``. Returns ``{steps, wall_seconds, seconds_per_step}``,
    or ``None`` when ``stop_fn`` asked for a governed stop at a step boundary: an
    interrupted timing run has no budget and is repeated from its start on resume.
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
    stepper = _build_stepper(
        spec, model, data, optimizer, scheduler, clipper,
        physics=physics, dtype=dtype, device=device,
    )
    _synchronize(device)
    started = clock()
    stopped = False
    for index in range(1, steps + 1):
        if stop_fn is not None and stop_fn():
            stopped = True
            break
        stepper.step(index)
    _synchronize(device)
    wall = clock() - started
    del stepper, clipper, scheduler, optimizer, model
    release_chunk_memory(device)
    if stopped:
        return None
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
    stop_fn=None,
    resume_state=None,
):
    """The budget driver. It branches only on ``budget_outcome``, divergence and a stop.

    ``step_fn(step)`` takes Adam step number ``step`` and returns ``None``, or a short name
    for the non-finite quantity that made it skip the optimizer step (GAP-60-06).
    ``read_fn(step)`` scores the current network and returns ``E``. ``on_extend()`` is called
    once, when the frozen rule grants the extension. At the end of the budget the frozen
    ``budget_outcome`` decides: complete, extend once to its ``new_budget_steps``, or (after
    the extension) inconclusive with a rate. An ``OwnerRouted`` it raises propagates
    unchanged. A skipped step ends Adam at the last finite state: ``budget_outcome`` is not
    called and no reading is invented. Adam's wall time is the sum of every step and every
    reading (GAP-60-05).

    ``resume_state`` continues a stopped driver: its step, readings, extension flag and
    summed wall seconds, with the budget unchanged (SPEC Requirement 8). ``stop_fn`` is
    consulted at every step boundary a checkpoint may be taken at; when it fires the driver
    returns with ``stopped`` true and the next step to take, and no budget outcome is
    decided.
    """
    if isinstance(budget, bool) or not isinstance(budget, int) or budget < 1:
        raise HarnessHalt(f"the Adam budget must be a positive integer; got {budget!r}")
    horizon = budget
    readings = []
    adam_seconds = 0.0
    step = 0
    extended = False
    new_budget_steps = None
    if resume_state is not None:
        step = int(resume_state["step"])
        readings = [list(item) for item in resume_state["readings"]]
        adam_seconds = float(resume_state["adam_seconds"])
        extended = bool(resume_state["extended"])
        new_budget_steps = resume_state["new_budget_steps"]
        if new_budget_steps is not None:
            horizon = int(new_budget_steps)
        if step > horizon:
            raise HarnessHalt(
                f"the resume checkpoint stopped at step {step}, past the horizon {horizon}"
            )
    planned = frozenset(
        reading_steps(budget, scorecard=scorecard, through=horizon, enforce_cadence=enforce_cadence)
    )
    rate_per_step = None
    diverged_at_step = None
    diverged_by = None
    outcome = None
    stopped = False
    if resume_state is None:
        started = clock()
        readings.append([step, read_fn(step)])
        adam_seconds += clock() - started
    while outcome is None:
        if stop_fn is not None and stop_fn():
            stopped = True
            break
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
        "stopped": stopped,
        "stopped_at_step": step if stopped else None,
        "step": step,
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


# ---------------------------------------------------------------------------
# The resume tree: one claim, one checkpoint, one marker per governed stop.
# ---------------------------------------------------------------------------


def _stop_markers(run_dir):
    """The governed stop markers of one run tree."""
    return sorted(Path(run_dir).glob(f"{STOP_PREFIX}*.json"))


def _stop_entry(*, phase, step):
    """The record's entry for one governed stop: signal, exit code, phase and step."""
    return {
        "signal": _signal_name(_STOP["signum"]),
        "exit_code": int(_STOP["exit_code"]),
        "phase": str(phase),
        "step": int(step),
    }


def _write_stop_marker(run_dir, spec, entry):
    """Write ``stop-<n>.json`` for one governed stop and return its path.

    Every stop is kept: a resumed arm that stops again writes the next number, so the
    ``launch.stops`` history in the record has one marker per entry (T-60-07).
    """
    number = len(_stop_markers(run_dir)) + 1
    path = Path(run_dir) / f"{STOP_PREFIX}{number}.json"
    payload = {
        "schema": STOP_SCHEMA,
        "diagnostic": True,
        "arm_id": spec.arm_id,
        "utc": datetime.now(timezone.utc).isoformat(),
        **entry,
    }
    write_record_exclusive(path, payload)
    return path


def _claim_run(run_dir, spec):
    """Claim an arm's run tree exactly once. A claimed tree refuses a fresh start."""
    directory = Path(run_dir)
    if (directory / CLAIM_FILE).exists():
        raise ClaimExists(
            f"arm {spec.arm_id} already claims {directory.name}; a stopped arm resumes with "
            "--resume and a fresh start needs an unclaimed tree"
        )
    payload = {
        "schema": CLAIM_SCHEMA,
        "arm_id": spec.arm_id,
        "pid": os.getpid(),
        "utc_started": datetime.now(timezone.utc).isoformat(),
        "resume": False,
    }
    return write_record_exclusive(directory / CLAIM_FILE, payload)


def _cpu_state_dict(model):
    """A model's state dict on the CPU, so a checkpoint restores on any device."""
    return OrderedDict(
        (name, tensor.detach().cpu().clone()) for name, tensor in model.state_dict().items()
    )


@dataclass
class _SavedScore:
    """A scored state restored from a checkpoint: its JSON block and the fields read."""

    payload: dict
    E: float
    eps_h: float
    tier: int

    def to_json_dict(self):
        return dict(self.payload)


_JSON_SENTINELS = {"NaN": math.nan, "Infinity": math.inf, "-Infinity": -math.inf}


def _number(value):
    """A recorded JSON number, with the three non-finite sentinels widened back to floats."""
    if isinstance(value, str):
        return _JSON_SENTINELS.get(value, math.nan)
    return float(value)


def _saved_score(payload):
    """Rebuild one scored state from the JSON block a checkpoint holds."""
    if not isinstance(payload, Mapping) or "E" not in payload:
        raise ResumeRefused("the resume checkpoint holds no scored state")
    return _SavedScore(
        payload=dict(payload),
        E=_number(payload["E"]),
        eps_h=_number(payload["eps_h"]),
        tier=int(payload["tier"]),
    )


def _resume_payload(
    *,
    spec,
    phase,
    invocations,
    stops,
    timing_runs,
    timing=None,
    budget=None,
    frozen_budget=None,
    driver=None,
    adam_complete=False,
    adam=None,
    trace=None,
    monitor_log=None,
    model=None,
    optimizer=None,
    scheduler=None,
    clipper=None,
    scheduled=None,
    rng_state=None,
    frozen_monitor_times=None,
    clipped_steps=0,
    adam_seconds=0.0,
    polish_seconds=0.0,
    total_seconds=0.0,
    segment=None,
    lbfgs=None,
    polish=None,
    first_omega_0=None,
    runtime=None,
    protocol_sha256=None,
    module_sha256=None,
):
    """One resume checkpoint: every component the arm needs to continue exactly.

    Tensors, numbers, strings, lists and dicts only, so ``torch.load`` can read it with
    ``weights_only=True`` (T-60-02). ``segment`` is the frozen L-BFGS segment: the
    collocation rows, causal weights and bin counts of a physics arm, or a data-only
    marker, and its absence makes a polish checkpoint un-resumable.
    """
    return {
        "arm_id": spec.arm_id,
        "loss_arm": spec.loss_arm,
        "run_kind": spec.run_kind,
        "phase": phase,
        "invocations": int(invocations),
        "stops": [dict(item) for item in stops],
        "timing_runs": int(timing_runs),
        "timing": None if timing is None else dict(timing),
        "budget_steps": None if budget is None else int(budget),
        "frozen_budget_steps": None if frozen_budget is None else int(frozen_budget),
        "driver": None if driver is None else copy.deepcopy(driver),
        "adam_complete": bool(adam_complete),
        "adam": None if adam is None else copy.deepcopy(adam),
        "trace": copy.deepcopy(trace or []),
        "monitor_log": copy.deepcopy(monitor_log or []),
        "model": None if model is None else _cpu_state_dict(model),
        "optimizer": None if optimizer is None else copy.deepcopy(optimizer.state_dict()),
        "scheduler": None if scheduler is None else copy.deepcopy(scheduler.state_dict()),
        "clipper": None if clipper is None else copy.deepcopy(clipper.state_dict()),
        "scheduled_weights": None if scheduled is None else copy.deepcopy(scheduled.state_dict()),
        "rng": None if rng_state is None else copy.deepcopy(rng_state),
        "clipped_steps": int(clipped_steps),
        "frozen_monitor_times": (
            None
            if frozen_monitor_times is None
            else torch.as_tensor(
                np.ascontiguousarray(frozen_monitor_times, dtype=np.float64)
            ).clone()
        ),
        "adam_seconds": float(adam_seconds),
        "polish_seconds": float(polish_seconds),
        "total_seconds": float(total_seconds),
        "segment": segment,
        "lbfgs": lbfgs,
        "polish": None if polish is None else copy.deepcopy(polish),
        "first_omega_0": None if first_omega_0 is None else float(first_omega_0),
        "runtime": None if runtime is None else [runtime[0], runtime[1]],
        "protocol_sha256": protocol_sha256,
        "module_sha256": None if module_sha256 is None else dict(module_sha256),
    }


def save_resume_checkpoint(run_dir, payload):
    """Write one resume checkpoint atomically under ``run_dir`` and return its path."""
    if not isinstance(payload, Mapping):
        raise ResumeRefused("a resume checkpoint must be a mapping")
    body = dict(payload)
    body["schema"] = RESUME_SCHEMA
    path = Path(run_dir) / RESUME_FILE
    atomic_write_torch(path, body)
    return path


def load_resume_checkpoint(run_dir, *, arm_id, protocol_sha256, module_sha256):
    """Load and vet the checkpoint of an interrupted arm; refuse anything not restorable.

    Refused (``ResumeRefused``): no checkpoint or no governed stop marker; another arm;
    another run protocol or a changed pinned module digest (T-60-12); an unknown phase;
    and a polish-phase checkpoint without its frozen segment state, in the trainer's own
    wording (``controllers.py`` lines 845-850 and 2213-2218).
    """
    directory = Path(run_dir)
    path = directory / RESUME_FILE
    if not path.is_file():
        raise ResumeRefused(
            f"a resume needs {RESUME_FILE} in {directory.name} and there is none; the arm "
            "goes to the owner"
        )
    if not _stop_markers(directory):
        raise ResumeRefused(
            f"a resume needs a {STOP_PREFIX}<n>.json marker in {directory.name} and there is "
            "none; only a governed stop is resumed"
        )
    payload = torch.load(path, map_location="cpu", weights_only=True)
    if not isinstance(payload, Mapping) or payload.get("schema") != RESUME_SCHEMA:
        raise ResumeRefused(
            f"the resume checkpoint in {directory.name} is not a {RESUME_SCHEMA} record"
        )
    if payload.get("arm_id") != arm_id:
        raise ResumeRefused(
            f"the resume checkpoint names arm {payload.get('arm_id')!r}, not {arm_id!r}"
        )
    if payload.get("protocol_sha256") != protocol_sha256:
        raise ResumeRefused(
            "the run protocol changed since this arm stopped; the arm cannot resume and "
            "goes to the owner"
        )
    if dict(payload.get("module_sha256") or {}) != dict(module_sha256 or {}):
        raise ResumeRefused(
            "a pinned module changed since this arm stopped; the arm cannot resume and goes "
            "to the owner"
        )
    if payload.get("phase") not in _RESUME_PHASES:
        raise ResumeRefused(
            f"the resume checkpoint has the unknown phase {payload.get('phase')!r}"
        )
    if payload.get("phase") == "polish" and payload.get("segment") is None:
        raise ResumeRefused(
            "resume checkpoint is missing active L-BFGS segment state; refusing to redraw "
            "samples or causal weights"
        )
    if payload.get("phase") == "polish" and payload.get("lbfgs") is None:
        raise ResumeRefused("the resume checkpoint is missing the L-BFGS state of the polish")
    for name in ("invocations", "stops", "timing_runs"):
        if name not in payload:
            raise ResumeRefused(f"the resume checkpoint is missing {name}")
    return payload


def _pin_facts(protocol):
    """``(protocol SHA-256, pinned module digests)``. A fixture arm has no protocol."""
    if protocol is None:
        return None, {}
    facts = _protocol_facts(protocol)
    return facts["protocol_sha256"], dict(facts["module_sha256"])


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


def _data_objective(model, data, *, dtype, device):
    """The data-only polish closure: the trainer's chunked full-batch data term."""
    chunk_size = OptConfig().lbfgs_chunk_size

    def closure():
        return data_polish_objective(
            model, data.data_points, chunk_size=chunk_size, dtype=dtype, device=device
        )

    return closure


def _physics_objective(model, run, *, dtype, device):
    """The physics polish closure on the rows, weights and bin counts frozen at the handoff."""
    chunk_size = OptConfig().lbfgs_chunk_size
    physics = run

    def closure():
        return physics_polish_objective(
            model,
            frozen_times=physics.handoff_times,
            frozen_w_n=physics.frozen_w_n,
            frozen_bin_counts=physics.frozen_bin_counts,
            frozen_weights=physics.frozen_weights,
            data_points=physics.data_points,
            ic13_t=physics.ic13_t,
            masses_t=physics.masses_t,
            true_r0=physics.true_r0,
            true_v0=physics.true_v0,
            r_ref=physics.r_ref,
            h0=physics.h0,
            eps_h=physics.eps_h,
            l0=physics.l0,
            data_chunk_size=chunk_size,
            microbatch_size=physics.microbatch_size,
            dtype=dtype,
            device=device,
        )

    return closure


def _polish(model, data, *, scorecard, adam_seconds, adam_gold, dtype, device, clock,
            objective=None, resume=None, stop_fn=None):
    """The frozen full-batch L-BFGS polish (GAP-60-05).

    One outer call is one ``LBFGS.step(closure)``. A call improves when the
    closure objective at the iterate it ends with is strictly below the best so
    far, starting from the objective at the Adam result. ``polish_should_stop``
    runs after every call. The polish state is the iterate after the last call,
    or the parameters from before a call that produced a non-finite objective
    or non-finite parameters. The scored ``E`` is logged and never steers it.
    ``objective`` is a zero-argument closure; it defaults to the data-only
    objective, and an arm with a physics term passes the frozen-handoff one.

    A ``stop_fn`` that fires is surfaced by raising ``_StopRequested`` from the
    closure, so a long outer call aborts at its next evaluation. The parameters
    are restored to the state from before that call, and the L-BFGS state copied
    before it is returned for the checkpoint: nothing is redrawn (SPEC
    Requirement 8). ``resume`` continues a stopped polish from its counters, its
    trace and its summed wall seconds.

    Returns a dict: ``stop_reason``, ``outer_calls``, ``trace``, ``gold``,
    ``stopped``, ``lbfgs``, ``best_objective``, ``without_improvement`` and
    ``elapsed_seconds``.
    """
    settings = scorecard.section("lbfgs_polish")
    parameters = list(model.parameters())
    optimizer = torch.optim.LBFGS(
        parameters,
        history_size=int(settings["lbfgs_history_size"]),
        max_iter=int(settings["lbfgs_max_iter"]),
        line_search_fn=str(settings["lbfgs_line_search"]),
    )
    if objective is None:
        objective = _data_objective(model, data, dtype=dtype, device=device)
    inner = objective

    def closure():
        if stop_fn is not None and stop_fn():
            raise _StopRequested()
        return inner()

    if resume is None:
        best = float(closure())
        state_result = adam_gold
        without_improvement = 0
        outer_calls = 0
        trace = []
        prior_seconds = 0.0
        started = clock()
    else:
        optimizer.load_state_dict(resume["lbfgs"])
        best = float(resume["best_objective"])
        saved_state = resume.get("state")
        state_result = adam_gold if saved_state is None else _saved_score(saved_state)
        without_improvement = int(resume["without_improvement"])
        outer_calls = int(resume["outer_calls"])
        trace = [dict(entry) for entry in resume["trace"]]
        prior_seconds = float(resume["elapsed_seconds"])
        started = clock() - prior_seconds
    while True:
        before = [parameter.detach().clone() for parameter in parameters]
        snapshot = copy.deepcopy(optimizer.state_dict())
        try:
            returned = float(optimizer.step(closure))
        except _StopRequested:
            # The aborted call is not part of the polish: restore the parameters from
            # before it and keep the state dict copied before it.
            with torch.no_grad():
                for parameter, saved in zip(parameters, before):
                    parameter.copy_(saved)
            return {
                "stop_reason": None,
                "outer_calls": outer_calls,
                "trace": trace,
                "gold": state_result,
                "stopped": True,
                "lbfgs": snapshot,
                "best_objective": best,
                "without_improvement": without_improvement,
                "elapsed_seconds": (
                    trace[-1]["elapsed_seconds"] if trace else prior_seconds
                ),
            }
        outer_calls += 1
        objective_value = float(closure())
        if not (math.isfinite(returned) and math.isfinite(objective_value) and _all_finite(parameters)):
            with torch.no_grad():
                for parameter, saved in zip(parameters, before):
                    parameter.copy_(saved)
            trace.append(
                {
                    "call": outer_calls,
                    "objective": objective_value,
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
            return {
                "stop_reason": reason,
                "outer_calls": outer_calls,
                "trace": trace,
                "gold": state_result,
                "stopped": False,
                "lbfgs": None,
                "best_objective": best,
                "without_improvement": without_improvement,
                "elapsed_seconds": trace[-1]["elapsed_seconds"],
            }
        improved = objective_value < best
        if improved:
            best = objective_value
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
                "objective": objective_value,
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
            return {
                "stop_reason": reason,
                "outer_calls": outer_calls,
                "trace": trace,
                "gold": state_result,
                "stopped": False,
                "lbfgs": None,
                "best_objective": best,
                "without_improvement": without_improvement,
                "elapsed_seconds": polish_seconds,
            }


def _checked_steps(value, name, minimum):
    if isinstance(value, bool) or not isinstance(value, int) or value < minimum:
        raise HarnessHalt(f"{name} must be an integer of at least {minimum}; got {value!r}")
    return value


def _repo_root(repo_root=None):
    return Path(__file__).resolve().parents[2] if repo_root is None else Path(repo_root)


def _finite_positive(value, what):
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise HarnessHalt(f"{what} must be a finite positive number; got {value!r}")
    number = float(value)
    if not math.isfinite(number) or number <= 0.0:
        raise HarnessHalt(f"{what} must be a finite positive number; got {value!r}")
    return number


@dataclass
class _PhysicsRun:
    """The frozen handoff and the constants a physics polish closure reads (GAP-60-05)."""

    handoff_times: object
    frozen_w_n: object
    frozen_bin_counts: object
    frozen_weights: object
    data_points: object
    ic13_t: object
    masses_t: object
    true_r0: object
    true_v0: object
    r_ref: float
    h0: object
    eps_h: object
    l0: object
    microbatch_size: int


def _stage_energy_weight(lr_stage):
    """The PHYS-05 ``lambda_E^max`` of the arm's stage: zero below stage 2."""
    return float(PHYS05_LAMBDA_E_MAX[lr_stage])


def _physics_reference(spec, *, admission, fixture_r_ref):
    """The Stage-0 reference in force and the record block that names it (D-08, GAP-60-10)."""
    if admission is not None:
        block = admission.get("r_ref_in_force")
        if not isinstance(block, Mapping) or "value" not in block:
            raise HarnessHalt(
                f"arm {spec.arm_id} has a physics term and its admission names no r_ref_in_force"
            )
        if block.get("note") != R_REF_NOTE:
            raise HarnessHalt(
                f"arm {spec.arm_id}: the admission's r_ref_in_force note is not "
                f"{R_REF_NOTE!r}"
            )
        value = _finite_positive(block["value"], "r_ref_in_force.value")
        return value, {
            "value": value,
            "path": block.get("path"),
            "sha256": block.get("sha256"),
            "note": R_REF_NOTE,
        }
    if fixture_r_ref is None:
        raise HarnessHalt(
            f"arm {spec.arm_id} has a physics term; a fixture arm passes fixture_r_ref explicitly "
            "and a real arm takes the reference in force from its admission"
        )
    value = _finite_positive(fixture_r_ref, "fixture_r_ref")
    return value, {
        "value": value,
        "path": None,
        "sha256": None,
        "note": "fixture reference: no governed artifact",
    }


def _physics_scale(spec, *, admission):
    """``(eps_h, s_h_block)``. ``eps_h`` is the admission's ``1e-4 x S_H`` (GAP-60-12).

    A stage whose energy weight is zero never evaluates the term, so no scale is invented
    for it; a stage whose weight is above zero refuses to run without the admission block.
    """
    block = None if admission is None else admission.get("s_h")
    if block is None:
        if _stage_energy_weight(spec.lr_stage) > 0.0:
            raise HarnessHalt(
                f"arm {spec.arm_id} has an active energy term at stage {spec.lr_stage} and its "
                "admission names no S_H"
            )
        return None, None
    eps_h = _finite_positive(block["eps_h"], "s_h.eps_h")
    return eps_h, {
        "value": float(block["value"]),
        "eps_h": eps_h,
        "source_sha256": str(block["source_sha256"]),
    }


def governed_context_reference(repo_root=None):
    """The governed ``R_ref`` artifact the scorer's context column always uses."""
    relative = Path(R_REF_ARTIFACT_RELATIVE_PATH)
    path = _repo_root(repo_root) / relative
    try:
        raw = path.read_bytes()
    except OSError as exc:
        raise HarnessHalt("the governed R_ref artifact is unreadable") from exc
    return {
        "path": relative.as_posix(),
        "sha256": hashlib.sha256(raw).hexdigest(),
    }


def formula_reference(repo_root=None):
    """``(E_formula by system id, SHA-256 of the file)`` from the committed Phase 59 baselines.

    The two-Kepler singles row of a counted panel system is the formula error ``counts``
    compares against (SPEC Requirement 7, FEAS-01 (v)). A row that is not applicable or
    not a finite positive error is left out, so ``counts`` raises ``OwnerRouted`` rather
    than treating a missing formula as zero.
    """
    path = _repo_root(repo_root) / TWO_KEPLER_REL
    try:
        raw = path.read_bytes()
        payload = json.loads(raw)
        rows = payload["rows"]["singles"]
    except (OSError, ValueError, KeyError, TypeError) as exc:
        raise HarnessHalt("the Phase 59 two-Kepler baselines are unreadable") from exc
    errors = {}
    for row in rows:
        if row.get("applicable") is not True:
            continue
        try:
            error = float(row["E"])
            identifier = int(row["id"])
        except (KeyError, TypeError, ValueError):
            continue
        if math.isfinite(error) and error > 0.0:
            errors[identifier] = error
    return errors, hashlib.sha256(raw).hexdigest()


def _float32_rounded(values):
    """The float32-rounded array an MPS arm used, widened back to float64 (GAP-60-07)."""
    array = np.asarray(values, dtype=np.float64)
    return np.asarray(array, dtype=np.float32).astype(np.float64)


class CrossCheckDisagreement(RuntimeError):
    """The CPU float64 re-score changed the tier or the counts boolean. The arm stops."""


def _cross_check_network(first_omega_0):
    """The cross-check's own network: float64 on the CPU, at the arm's ``first_omega_0``."""
    cpu = torch.device("cpu")
    if first_omega_0 == SIREN_FIRST_OMEGA_0:
        return build_network(ArchitectureSpec(seed=SEED), dtype=torch.float64, device=cpu)
    return build_network_with_first_omega(first_omega_0, seed=SEED, dtype=torch.float64, device=cpu)


def cross_check_state(state_dict, spec, arm_data, first_omega_0, *, scorecard, formula):
    """GAP-60-07: re-score one saved state on the CPU in float64, beside the official score.

    The network is built at the arm's own ``first_omega_0`` (the diagnostic builder for any
    value, the production builder at 30.0), each saved tensor is moved to the CPU and then
    widened to float64, and the same float32-rounded normalized IC13 the MPS arm fed in is
    widened back to float64. The official metric arithmetic is float64 on the CPU, so the
    two scores differ only by the storage precision of the weights. Returns
    ``(ScoreResult, counts boolean)``; the counts boolean is ``None`` for a probe arm, which
    never calls ``counts``.
    """
    if not isinstance(state_dict, Mapping):
        raise CrossCheckDisagreement("a cross-check needs the saved state dict")
    cpu = torch.device("cpu")
    model = _cross_check_network(first_omega_0)
    widened = OrderedDict(
        (name, tensor.detach().to("cpu").to(torch.float64))
        for name, tensor in state_dict.items()
    )
    model.load_state_dict(widened)
    result = score_network(
        model,
        _float32_rounded(arm_data.ic13),
        _float32_rounded(arm_data.masses),
        arm_data.score.positions,
        arm_data.score.inner_pair,
        arm_data.score.times,
        scorecard=scorecard,
        dtype=torch.float64,
        device=cpu,
        grid=arm_data.score.grid,
    )
    counted = counts(result.tier, result.E, formula, scorecard=scorecard) if spec.counted else None
    return result, counted


# ---------------------------------------------------------------------------
# The real-arm record (SPEC Requirements 4 and 5, D-10).
# ---------------------------------------------------------------------------

REQUIRED_REAL_FIELDS = (
    "schema",
    "diagnostic",
    "run_kind",
    "arm_id",
    "loss_arm",
    "counted",
    "seed",
    "runtime.dtype",
    "runtime.device",
    "versions.torch",
    "versions.numpy",
    "versions.python",
    "versions.macos",
    "code.git_head",
    "code.dirty_pinn_paths",
    "config_sha256",
    "scorecard_sha256",
    "scorer_sha256",
    "protocol_sha256",
    "module_sha256",
    "normalizer.stats_sha256",
    "attestation.test_split_opened",
    "attestation.blocked_attempts",
    "attestation.refused_before_open",
    "timing.seconds_per_step",
    "budget.rule",
    "budget.budget_steps",
    "budget.reading_steps",
    "budget.readings",
    "budget.outcome",
    "budget.extended",
    "trace",
    "states.adam.score_gold",
    "states.adam.score_base",
    "states.adam.cross_check",
    "states.adam.weights.file",
    "states.adam.weights.sha256",
    "states.adam.weights.tensor_digest",
    "states.polish.score_gold",
    "states.polish.score_base",
    "states.polish.cross_check",
    "states.polish.weights.file",
    "states.polish.weights.sha256",
    "states.polish.weights.tensor_digest",
    "better_state",
    "result.state",
    "result.tier",
    "result.E",
    "result.e_in_max",
    "result.h",
    "result.eps_h",
    "formula.E_formula",
    "formula.counts",
    "wall.hours",
)


def _lookup(payload, dotted):
    current = payload
    for part in dotted.split("."):
        if not isinstance(current, Mapping) or part not in current:
            return _MISSING
        current = current[part]
    return current


def _is_hex64(value):
    return (
        isinstance(value, str)
        and len(value) == 64
        and all(character in _HEX64 for character in value)
    )


def _is_number(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def _is_nonfinite_sentinel(value):
    return isinstance(value, str) and value in ("NaN", "Infinity", "-Infinity")


def _one_line(condition, message):
    if not condition:
        raise HarnessHalt(message)


def validate_record(payload):
    """SPEC Requirements 4 and 5: a real-arm record is complete, or it is not written.

    Presence is checked for every dotted path in ``REQUIRED_REAL_FIELDS``; then the literal
    and type rules: seed 42, MPS float32, the harness schema, ``diagnostic`` true,
    ``run_kind`` real, 64-character lowercase hex digests, ``adam.weights`` and
    ``polish.weights`` as the only file names, zero test-split attestation counters, a
    finite positive seconds per step and wall hours, a tier in 0..3, ``adam`` or ``polish``
    as the better state, an ``h`` list carrying both the 0.01 and 0.1 horizons, non-finite
    numbers only as the ScoreResult JSON sentinels, a formula comparison that is null only
    on a probe arm, the physics fields of an arm with a physics term, and the ruling block
    of a continue arm (its SHA-256, ``on_grid`` and ``equals_confirmed``). Returns
    ``payload``; anything else raises ``HarnessHalt`` naming the field.
    """
    _one_line(isinstance(payload, Mapping), "a real-arm record must be a mapping")
    for field in REQUIRED_REAL_FIELDS:
        _one_line(_lookup(payload, field) is not _MISSING, f"a real-arm record is missing {field}")

    _one_line(payload["schema"] == RUN_SCHEMA, "a real-arm record carries the harness schema")
    _one_line(payload["diagnostic"] is True, "a real-arm record is marked diagnostic")
    _one_line(payload["run_kind"] == "real", "run_kind must be real on a real-arm record")
    _one_line(
        isinstance(payload["arm_id"], str) and bool(payload["arm_id"]),
        "arm_id must be a non-empty string",
    )
    _one_line(payload["loss_arm"] in LOSS_ARMS, "loss_arm must be one of the harness loss arms")
    _one_line(isinstance(payload["counted"], bool), "counted must be a boolean")
    _one_line(payload["seed"] == SEED, f"seed must be {SEED}")
    _one_line(payload["runtime"]["dtype"] == REAL_RUNTIME[0], "runtime.dtype must be float32")
    _one_line(payload["runtime"]["device"] == REAL_RUNTIME[1], "runtime.device must be mps")

    for name in ("torch", "numpy", "python", "macos"):
        value = payload["versions"][name]
        _one_line(isinstance(value, str) and bool(value), f"versions.{name} must be a string")
    _one_line(
        isinstance(payload["code"]["git_head"], str) and bool(payload["code"]["git_head"]),
        "code.git_head must be a commit id",
    )
    dirt = payload["code"]["dirty_pinn_paths"]
    _one_line(
        isinstance(dirt, list) and all(isinstance(item, str) for item in dirt),
        "code.dirty_pinn_paths must be a list of paths",
    )
    for name in (
        "config_sha256",
        "scorecard_sha256",
        "scorer_sha256",
        "protocol_sha256",
    ):
        _one_line(_is_hex64(payload[name]), f"{name} must be a 64-character lowercase hex digest")
    modules = payload["module_sha256"]
    _one_line(
        isinstance(modules, Mapping) and bool(modules)
        and all(_is_hex64(value) for value in modules.values()),
        "module_sha256 must map each pinned module to a hex digest",
    )
    _one_line(
        _is_hex64(payload["normalizer"]["stats_sha256"]),
        "normalizer.stats_sha256 must be a 64-character lowercase hex digest",
    )
    for name in ("test_split_opened", "blocked_attempts", "refused_before_open"):
        value = payload["attestation"][name]
        _one_line(
            isinstance(value, int) and not isinstance(value, bool) and value == 0,
            f"attestation.{name} must be zero",
        )

    seconds = payload["timing"]["seconds_per_step"]
    _one_line(
        _is_number(seconds) and math.isfinite(float(seconds)) and float(seconds) > 0.0,
        "timing.seconds_per_step must be a finite positive number",
    )
    budget = payload["budget"]
    _one_line(budget["rule"] == "frozen", "budget.rule must be frozen on a real arm")
    _one_line(
        isinstance(budget["budget_steps"], int) and not isinstance(budget["budget_steps"], bool)
        and budget["budget_steps"] >= 1,
        "budget.budget_steps must be a positive integer",
    )
    steps = budget["reading_steps"]
    _one_line(
        isinstance(steps, list) and bool(steps)
        and all(isinstance(step, int) and not isinstance(step, bool) for step in steps)
        and steps[0] == 0,
        "budget.reading_steps must be a list of integer steps starting at 0",
    )
    readings = budget["readings"]
    _one_line(
        isinstance(readings, list) and bool(readings)
        and all(
            isinstance(item, list) and len(item) == 2 for item in readings
        ),
        "budget.readings must be a list of [step, E] pairs",
    )
    _one_line(isinstance(budget["outcome"], str), "budget.outcome must be a string")
    _one_line(isinstance(budget["extended"], bool), "budget.extended must be a boolean")
    _one_line(isinstance(payload["trace"], list) and bool(payload["trace"]), "trace must be a list")

    for state in ("adam", "polish"):
        block = payload["states"][state]
        for field in ("score_gold", "score_base", "cross_check"):
            _one_line(
                isinstance(block[field], Mapping), f"states.{state}.{field} must be a mapping"
            )
        check = block["cross_check"]
        for field in ("tier", "E", "eps_h", "counts"):
            _one_line(field in check, f"states.{state}.cross_check is missing {field}")
        _one_line(
            isinstance(check["tier"], int) and not isinstance(check["tier"], bool)
            and 0 <= check["tier"] <= 3,
            f"states.{state}.cross_check.tier must be an integer in 0..3",
        )
        weights = block["weights"]
        _one_line(
            weights["file"] == f"{state}.weights",
            f"states.{state}.weights.file must be {state}.weights",
        )
        _one_line(
            _is_hex64(weights["sha256"]),
            f"states.{state}.weights.sha256 must be a 64-character lowercase hex digest",
        )
        _one_line(
            _is_hex64(weights["tensor_digest"]),
            f"states.{state}.weights.tensor_digest must be a 64-character lowercase hex digest",
        )

    _one_line(payload["better_state"] in ("adam", "polish"), "better_state must be adam or polish")
    result = payload["result"]
    _one_line(result["state"] in ("adam", "polish"), "result.state must be adam or polish")
    _one_line(
        isinstance(result["tier"], int) and not isinstance(result["tier"], bool)
        and 0 <= result["tier"] <= 3,
        "result.tier must be an integer in 0..3",
    )
    for field in ("E", "e_in_max", "eps_h"):
        value = result[field]
        _one_line(
            (_is_number(value) and math.isfinite(float(value))) or _is_nonfinite_sentinel(value),
            f"result.{field} must be a finite number or the JSON sentinel of a non-finite score",
        )
    horizons = result["h"]
    _one_line(
        isinstance(horizons, list)
        and all(isinstance(item, (list, tuple)) and len(item) == 2 for item in horizons),
        "result.h must be a list of [delta, value] pairs",
    )
    deltas = [float(item[0]) for item in horizons]
    for required in (0.01, 0.1):
        _one_line(
            any(abs(delta - required) < 1e-12 for delta in deltas),
            f"result.h must carry the {required} horizon",
        )

    formula = payload["formula"]
    if formula["counts"] is None:
        _one_line(
            formula["E_formula"] == FORMULA_NOT_APPLICABLE,
            "formula.counts may be null only on a probe arm, whose E_formula is "
            f"{FORMULA_NOT_APPLICABLE!r}",
        )
    else:
        _one_line(isinstance(formula["counts"], bool), "formula.counts must be a boolean or null")
        _one_line(
            _is_number(formula["E_formula"]) and math.isfinite(float(formula["E_formula"])),
            "formula.E_formula must be the committed two-Kepler error on a counted arm",
        )

    hours = payload["wall"]["hours"]
    _one_line(
        _is_number(hours) and math.isfinite(float(hours)) and float(hours) >= 0.0,
        "wall.hours must be a finite non-negative number",
    )

    if payload["loss_arm"] != "data_only":
        reference = payload.get("r_ref")
        _one_line(isinstance(reference, Mapping), "a physics arm records r_ref")
        _one_line(
            reference.get("note") == R_REF_NOTE, f"r_ref.note must be {R_REF_NOTE!r}"
        )
        _one_line(
            _finite_check(reference.get("value")), "r_ref.value must be a finite positive number"
        )
        context_ref = payload.get("scorer_context_r_ref")
        _one_line(
            isinstance(context_ref, Mapping) and _is_hex64(context_ref.get("sha256")),
            "a physics arm records scorer_context_r_ref with its SHA-256",
        )
        _one_line(
            isinstance(payload.get("monitor_log"), list) and bool(payload.get("monitor_log")),
            "a physics arm records the frozen monitor log",
        )
        handoff = payload.get("handoff")
        _one_line(isinstance(handoff, Mapping), "a physics arm records its handoff")
        _one_line(
            _is_hex64(handoff.get("rows_sha256")), "handoff.rows_sha256 must be a hex digest"
        )
        _one_line(
            isinstance(handoff.get("w_n"), list) and len(handoff["w_n"]) == 16,
            "handoff.w_n must hold the 16 causal weights",
        )
        _one_line(isinstance(handoff.get("weights"), Mapping), "handoff.weights must be a mapping")
        _one_line(
            isinstance(payload.get("schedule", {}).get("warmup_steps"), int),
            "a physics arm records schedule.warmup_steps",
        )
        if payload.get("rung") == "probe-2b":
            scale = payload.get("s_h")
            _one_line(isinstance(scale, Mapping), "a probe Rung-2b arm records s_h")
            _one_line(
                _finite_check(scale.get("eps_h")), "s_h.eps_h must be a finite positive number"
            )
            _one_line(
                _is_hex64(scale.get("source_sha256")),
                "s_h.source_sha256 must be a hex digest",
            )

    if payload["arm_id"].startswith("c-"):
        ruling = payload.get("ruling")
        _one_line(isinstance(ruling, Mapping), "a continue arm records its ruling")
        _one_line(_is_hex64(ruling.get("sha256")), "ruling.sha256 must be a hex digest")
        _one_line(isinstance(ruling.get("on_grid"), bool), "ruling.on_grid must be a boolean")
        _one_line(
            isinstance(ruling.get("equals_confirmed"), bool),
            "ruling.equals_confirmed must be a boolean",
        )
    return payload


def _finite_check(value):
    return _is_number(value) and math.isfinite(float(value)) and float(value) > 0.0


def _versions():
    """The exact interpreter and library versions SPEC Requirement 4 records."""
    return {
        "torch": str(torch.__version__),
        "numpy": str(np.__version__),
        "python": platform.python_version(),
        "macos": platform.mac_ver()[0],
    }


def _code_state(repo_root=None):
    """The commit the arm ran at and the ``pinn`` paths that were dirty."""
    root = _repo_root(repo_root)
    head = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=str(root),
        capture_output=True, text=True, check=False,
    )
    if head.returncode != 0 or not head.stdout.strip():
        raise HarnessHalt("the arm's git commit cannot be read")
    status = subprocess.run(
        ["git", "status", "--porcelain", "--", "pinn"], cwd=str(root),
        capture_output=True, text=True, check=False,
    )
    dirty = sorted(
        line[3:] for line in status.stdout.splitlines() if len(line) > 3 and line.strip()
    )
    return {"git_head": head.stdout.strip(), "dirty_pinn_paths": dirty}


def _key_text(key):
    return f"{key.variant}/{key.fidelity}/{key.id}"


def _config_sha256(spec, *, first_omega_0, runtime, budget_steps, clip):
    """The SHA-256 of the canonical JSON of the arm configuration the run used."""
    payload = {
        "arm_id": spec.arm_id,
        "rung": spec.rung,
        "path": spec.path,
        "loss_arm": spec.loss_arm,
        "system_id": int(spec.system_id),
        "variant": spec.variant,
        "train": _key_text(spec.train_key),
        "score": _key_text(spec.score_key),
        "beside": _key_text(spec.beside_key),
        "lr_stage": int(spec.lr_stage),
        "clip_stage": int(spec.clip_stage),
        "omega_provenance": spec.omega_provenance,
        "grid_omega": spec.grid_omega,
        "counted": bool(spec.counted),
        "run_kind": spec.run_kind,
        "first_omega_0": float(first_omega_0),
        "runtime": {"dtype": runtime[0], "device": runtime[1]},
        "budget_steps": int(budget_steps),
        "clip": dict(clip),
    }
    return hashlib.sha256(evidence_io.canonical_json_bytes(payload)).hexdigest()


def _protocol_facts(protocol):
    """The four digests a real-arm record cites, from the loaded run protocol."""
    if protocol is None:
        raise HarnessHalt("a real-arm record cites the run protocol and none was supplied")
    if hasattr(protocol, "payload") and hasattr(protocol, "sha256"):
        payload, sha256 = protocol.payload, protocol.sha256
    elif isinstance(protocol, Mapping) and "payload" in protocol:
        payload, sha256 = protocol["payload"], protocol.get("sha256")
    elif isinstance(protocol, Mapping):
        payload, sha256 = protocol, protocol.get("protocol_sha256")
    else:
        raise HarnessHalt("the run protocol must be the loaded protocol or its payload")
    if not isinstance(payload, Mapping):
        raise HarnessHalt("the run protocol payload must be a mapping")
    facts = {"protocol_sha256": sha256}
    for name in ("module_sha256", "scorecard_sha256", "scorer_sha256"):
        if name not in payload:
            raise HarnessHalt(f"the run protocol is missing {name}")
        facts[name] = payload[name]
    return facts


def build_real_record(*, spec, run_parts, admission, protocol, data_context, repo_root=None):
    """Assemble a real arm's record: the run's own parts beside every provenance field.

    Pure: no corpus record is read and no optimizer runs. Every input is required; a
    missing part raises ``HarnessHalt`` rather than being left out. The reference in force
    and the S_H block come from the admission, never from the run's own mapping, so the
    record states what authorized the arm. The result is JSON-safe, so it is exactly what
    ``write_record_exclusive`` writes.
    """
    _one_line(isinstance(run_parts, Mapping), "run_parts must be a mapping")
    _one_line(isinstance(admission, Mapping), "a real arm needs the admission that let it run")
    _one_line(
        admission.get("arm_id") == spec.arm_id,
        f"the admission is for {admission.get('arm_id')!r}, not {spec.arm_id!r}",
    )
    _one_line(
        data_context is not None and getattr(data_context, "attestation", None) is not None,
        "a real-arm record carries the process attestation and the context has none",
    )
    facts = _protocol_facts(protocol)
    _one_line(
        admission.get("protocol_sha256") == facts["protocol_sha256"],
        "the admission and the loaded protocol name different protocols",
    )
    for field in ("budget", "timing", "wall", "states", "result", "formula", "first_omega_0",
                  "runtime", "clip"):
        _one_line(field in run_parts, f"the run produced no {field} to record")
    runtime = run_parts["runtime"]
    _one_line(
        (runtime.get("dtype"), runtime.get("device")) == REAL_RUNTIME,
        f"a real arm runs at {REAL_RUNTIME[0]} on {REAL_RUNTIME[1]}",
    )

    record = dict(run_parts)
    record["versions"] = _versions()
    record["code"] = _code_state(repo_root)
    record["config_sha256"] = _config_sha256(
        spec,
        first_omega_0=run_parts["first_omega_0"],
        runtime=(runtime["dtype"], runtime["device"]),
        budget_steps=run_parts["budget"]["budget_steps"],
        clip=run_parts["clip"],
    )
    record["protocol_sha256"] = facts["protocol_sha256"]
    record["module_sha256"] = facts["module_sha256"]
    record["scorecard_sha256"] = facts["scorecard_sha256"]
    record["scorer_sha256"] = facts["scorer_sha256"]
    record["preflight_sha256"] = admission.get("preflight_sha256")
    record["attestation"] = data_context.attestation.summary()
    record["normalizer"] = {
        "stats_sha256": data_context.stats_sha256,
        "source": data_context.normalizer_source,
    }
    wall = dict(run_parts["wall"])
    wall["hours"] = float(wall["total_seconds"]) / 3600.0
    record["wall"] = wall

    notes = list(run_parts.get("readout_notes") or [])
    if spec.rung == "probe-2b" and _D05_NOTE not in notes:
        notes.append(_D05_NOTE)
    record["readout_notes"] = notes

    if spec.loss_arm != "data_only":
        reference = admission.get("r_ref_in_force")
        _one_line(
            isinstance(reference, Mapping) and reference.get("note") == R_REF_NOTE,
            f"a physics arm's admission names no Stage-0 reference in force ({R_REF_NOTE!r})",
        )
        record["r_ref"] = {
            "value": _finite_positive(reference.get("value"), "r_ref_in_force.value"),
            "path": reference.get("path"),
            "sha256": reference.get("sha256"),
            "note": R_REF_NOTE,
        }
        context_reference = admission.get("scorer_context_r_ref")
        _one_line(
            isinstance(context_reference, Mapping)
            and isinstance(context_reference.get("sha256"), str),
            "a physics arm's admission names no governed reference for the scorer's context",
        )
        record["scorer_context_r_ref"] = {
            "path": context_reference.get("path"),
            "sha256": context_reference.get("sha256"),
        }
        scale = admission.get("s_h")
        if scale is not None:
            record["s_h"] = {
                "value": float(scale["value"]),
                "eps_h": float(scale["eps_h"]),
                "source_sha256": str(scale["source_sha256"]),
            }
        elif _stage_energy_weight(spec.lr_stage) > 0.0:
            raise HarnessHalt(
                f"arm {spec.arm_id} has an active energy term and its admission names no S_H"
            )

    ruling = admission.get("ruling")
    if ruling is not None:
        record["ruling"] = {
            "path": ruling.get("path"),
            "sha256": ruling.get("sha256"),
            "answer": ruling.get("answer"),
            "approved_first_omega_0": ruling.get("approved_first_omega_0"),
            "on_grid": ruling.get("on_grid"),
            "equals_confirmed": ruling.get("equals_confirmed"),
        }
    return evidence_io.json_safe(record)


def _official_counts(arm_dir, spec, result, *, state, e_formula, scorecard, data_root):
    """``counts`` for one scored state of a counted arm; a probe never reaches ``counts``.

    SPEC Requirement 7 and the frozen counting rule: a counted system whose formula row is
    absent raises ``OwnerRouted``. The clause that catches it writes ``owner-stop.json``
    (stage ``counts``) and then re-raises the same exception; nothing retries and nothing
    substitutes a formula (T-60-11).
    """
    if not spec.counted:
        return None
    try:
        return counts(result.tier, result.E, e_formula, scorecard=scorecard)
    except OwnerRouted as stop:
        write_owner_stop(
            arm_dir,
            stage=COUNTS_STAGE,
            reason=str(stop),
            details={
                "arm_id": spec.arm_id,
                "state": state,
                "tier": int(result.tier),
                "E": float(result.E),
                "E_formula": e_formula,
            },
            data_root=data_root,
        )
        raise


def run_arm(
    spec,
    *,
    context,
    scorecard,
    runtime,
    evidence_root,
    fixture_budget_steps=None,
    fixture_timing_steps=None,
    fixture_n_slots=None,
    fixture_r_ref=None,
    clip_enabled=True,
    ruling=None,
    admission=None,
    protocol=None,
    resume=False,
    run_dir=None,
    clock=time.monotonic,
):
    """Run one arm end to end and return the record it wrote.

    ``runtime`` is a ``(dtype name, device name)`` pair. A real arm sizes itself: its own
    timing run (``timing_steps_for`` steps) gives seconds per step, ``budget_from_timing``
    gives the budget B, and ``drive_adam`` runs the cosine over B under the frozen budget
    rule. A fixture arm (both the arm and the context are fixtures) names its own small
    ``fixture_budget_steps`` and may name ``fixture_timing_steps`` (default: the frozen
    minimum), ``fixture_n_slots`` (default: the ratified 256 slots, 4,096 rows) and
    ``fixture_r_ref`` (the Stage-0 reference it passes explicitly). The record then holds
    the budget the frozen rule would have given, beside the fixture's. A real arm refuses
    every fixture knob. ``clip_enabled`` turns the trainer's gradient clipper on for the
    timing run and the arm (GAP-60-03); the launcher passes the run protocol's
    ``clip_data_only_arms``. ``ruling`` is the committed D-11 ruling an ``owner_approved``
    arm needs (duck-typed: ``answer`` and ``approved_first_omega_0``); without one that arm
    is refused.

    An arm with a physics term (D-01, D-06) trains the trainer's memory-bounded step with
    fresh collocation rows each step, the PHYS-05 warmup of the same budget, the reference
    in force and the frozen monitor logged at every reading. At the handoff the rows, the
    pass-1 causal weights, the bin counts and the loss weights are frozen for the polish
    (GAP-60-05).

    Every scored state is re-scored on the CPU in float64 (GAP-60-07). A tier or counts
    disagreement, an ``OwnerRouted`` from the budget outcome or from a missing formula,
    writes ``owner-stop.json`` and propagates unchanged; nothing is retried (T-60-11).

    A real arm that carries the admission ``learnability_protocol.admit_arm`` returned and
    the loaded run protocol writes its record through ``build_real_record`` and
    ``validate_record`` (SPEC Requirements 4 and 5, D-10): an incomplete record is never
    written. The first-layer frequency is resolved and authorized before anything else
    (INST-05(e)): an arm that is not entitled to its setting raises ``OverrideRefused``
    before any data is read, any network is built or any file is written.

    ``resume=True`` continues the arm from ``runs/phase60/<arm-id>/resume.pt`` (SPEC
    Requirement 8). Every component is restored exactly - the model, Adam, the scheduler
    and its cosine index, the scheduled weights, the clipper, the four RNG streams, the
    readings, the trace, the monitor log, B, the extension flag and the summed wall
    seconds - and the step budget is never re-timed. A stop during the timing run is the
    one case that repeats it, recorded as a second timing run. A checkpoint that cannot
    be restored raises ``ResumeRefused`` and goes to the owner; nothing is restarted
    silently. ``run_dir`` is the ignored run tree; the command line passes the canonical
    ``runs/phase60/<arm-id>`` and a direct caller defaults to a tree beside its evidence
    root, so a test writes nothing into the repository.
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
    strict = admission is not None or protocol is not None
    if strict:
        if fixture:
            raise HarnessHalt(
                f"arm {spec.arm_id} is a fixture and takes no admission and no protocol"
            )
        if admission is None or protocol is None:
            raise HarnessHalt(
                f"a real arm takes both the admission it was granted and the loaded run "
                f"protocol; arm {spec.arm_id} was given only one"
            )
        if tuple(runtime) != REAL_RUNTIME:
            raise HarnessHalt(
                f"a real arm runs at {REAL_RUNTIME[0]} on {REAL_RUNTIME[1]}; arm "
                f"{spec.arm_id} was asked for {runtime!r}"
            )
        recorded = admission.get("first_omega_0")
        if recorded is None or float(recorded) != float(first_omega_0):
            raise HarnessHalt(
                f"the admission's first_omega_0 {recorded!r} is not the arm's resolved "
                f"{first_omega_0}"
            )
    if fixture:
        budget = _checked_steps(fixture_budget_steps, "fixture_budget_steps", 1)
        timing_steps = (
            _timing_minimum(scorecard)
            if fixture_timing_steps is None
            else _checked_steps(fixture_timing_steps, "fixture_timing_steps", _timing_minimum(scorecard))
        )
        n_slots = (
            _SLOTS if fixture_n_slots is None
            else _checked_steps(fixture_n_slots, "fixture_n_slots", 1)
        )
    else:
        if any(
            knob is not None
            for knob in (fixture_budget_steps, fixture_timing_steps, fixture_n_slots, fixture_r_ref)
        ):
            raise HarnessHalt(
                "fixture_budget_steps, fixture_timing_steps, fixture_n_slots and "
                "fixture_r_ref are legal only for a fixture arm on a fixture context"
            )
        budget = None
        timing_steps = timing_steps_for(spec, scorecard=scorecard)
        n_slots = _SLOTS
    physics_arm = spec.loss_arm != "data_only"
    r_ref, r_ref_block = (
        _physics_reference(spec, admission=admission, fixture_r_ref=fixture_r_ref)
        if physics_arm else (None, None)
    )
    eps_h, s_h_block = (
        _physics_scale(spec, admission=admission) if physics_arm else (None, None)
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

    # SPEC Requirement 8: one claim, one checkpoint, one marker per governed stop.
    if not isinstance(resume, bool):
        raise HarnessHalt(f"resume must be a boolean; got {resume!r}")
    run_root = (
        # The launcher passes the canonical ``runs/phase60/<arm-id>``. Any direct caller
        # gets a tree beside the evidence root it already isolated, so a fixture or a test
        # leaves nothing in the repository.
        Path(run_dir) if run_dir is not None else Path(evidence_root) / RUNS_REL / spec.arm_id
    )
    protocol_sha256, module_sha256 = _pin_facts(protocol)
    if resume:
        saved = load_resume_checkpoint(
            run_root,
            arm_id=spec.arm_id,
            protocol_sha256=protocol_sha256,
            module_sha256=module_sha256,
        )
        invocations = int(saved["invocations"]) + 1
        stops = [dict(item) for item in saved["stops"]]
        timing_runs = int(saved["timing_runs"])
        resumed_from = saved["phase"]
        prior_total = float(saved["total_seconds"])
        recorded_omega = saved.get("first_omega_0")
        if recorded_omega is not None and float(recorded_omega) != float(first_omega_0):
            raise ResumeRefused(
                f"the resume checkpoint ran at first_omega_0 {recorded_omega!r}, not the "
                f"arm's resolved {first_omega_0}"
            )
    else:
        saved = None
        invocations = 1
        stops = []
        timing_runs = 0
        resumed_from = None
        prior_total = 0.0
        _claim_run(run_root, spec)
    total_started = clock() - prior_total
    adam_resume = resumed_from in ("adam", "polish")
    polish_resume = resumed_from == "polish"
    data = load_arm_data(spec, context, scorecard=scorecard, dtype=dtype, device=device)
    microbatch_size = int(OptConfig().adam_microbatch_size)
    ic13_t = torch.as_tensor(data.ic13, dtype=dtype, device=device).reshape(-1)
    masses_t = torch.as_tensor(data.masses, dtype=dtype, device=device).reshape(-1)
    if physics_arm:
        h0 = float(
            _matched_plummer_hamiltonian(
                data.true_r0.unsqueeze(0), data.true_v0.unsqueeze(0), masses_t,
                dtype=dtype, device=device,
            )[0]
        )
        l0 = _angular_momentum(
            data.true_r0.unsqueeze(0), data.true_v0.unsqueeze(0), masses_t,
            dtype=dtype, device=device,
        )[0]

    def physics_inputs(weights, rng):
        """The per-step bundle. ``data_points`` is None on Rung 2a (FEAS-04 arm (a))."""
        return _PhysicsInputs(
            rng=rng,
            train_key=spec.train_key,
            n_slots=n_slots,
            r_ref=r_ref,
            h0=h0,
            l0=l0,
            eps_h=eps_h,
            ic13_t=ic13_t,
            masses_t=masses_t,
            true_r0=data.true_r0,
            true_v0=data.true_v0,
            weights=weights,
            data_points=None if spec.loss_arm == "physics_ic" else data.data_points,
            microbatch_size=microbatch_size,
        )

    # D-02, GAP-60-04: the budget comes from this arm's own timing run. The timing network
    # is gone by the time the arm builds its own, from the seed-42 initialization. A physics
    # timing run draws its rows from its own throwaway generator, never the arm's.
    if adam_resume:
        # SPEC Requirement 8: a resume is never re-timed. The checkpoint's budget is B.
        timing = dict(saved["timing"])
        budget = int(saved["budget_steps"])
        frozen_budget = int(saved["frozen_budget_steps"])
        if budget < 1:
            raise ResumeRefused(
                f"the resume checkpoint holds the budget {budget}; an arm cannot resume "
                "without a positive step budget"
            )
    else:
        # A timing run interrupted by a governed stop has no budget; the resume repeats it
        # from its start and the record counts the second attempt.
        timing_runs += 1
        timing_physics = (
            physics_inputs(
                make_scheduled_weights(timing_steps, spec.lr_stage), np.random.default_rng(SEED)
            )
            if physics_arm else None
        )
        timing = timing_run(
            spec,
            context=context,
            scorecard=scorecard,
            runtime=runtime,
            first_omega_0=first_omega_0,
            steps=timing_steps,
            clip_enabled=clip_enabled,
            data=data,
            physics=timing_physics,
            clock=clock,
            stop_fn=stop_requested,
        )
        if timing is None:
            entry = _stop_entry(phase="timing", step=0)
            stops.append(entry)
            save_resume_checkpoint(
                run_root,
                _resume_payload(
                    spec=spec,
                    phase="timing",
                    invocations=invocations,
                    stops=stops,
                    timing_runs=timing_runs,
                    budget=budget,
                    first_omega_0=first_omega_0,
                    runtime=runtime,
                    protocol_sha256=protocol_sha256,
                    module_sha256=module_sha256,
                    total_seconds=clock() - total_started,
                ),
            )
            _write_stop_marker(run_root, spec, entry)
            raise GovernedStop(
                entry["exit_code"], signal_name=entry["signal"], phase="timing", step=0
            )
        frozen_budget = budget_from_timing(timing, scorecard=scorecard)
        if budget is None:
            budget = frozen_budget
    if budget < 1:
        raise HarnessHalt(
            f"the frozen budget for arm {spec.arm_id} is {budget} steps; no arm can be run"
        )

    # D-06: the arm's own stream. The frozen monitor set is drawn first, before step 1.
    # A data-only arm carries the generator too, so one checkpoint format holds all four
    # RNG streams and exact continuation is the same code path for every arm.
    rng = np.random.default_rng(SEED)
    frozen_monitor_times = (
        draw_collocation_times(spec.train_key, rng, n_slots=n_slots) if physics_arm else None
    )
    scheduled = make_scheduled_weights(budget, spec.lr_stage) if physics_arm else None
    arm_physics = physics_inputs(scheduled, rng) if physics_arm else None

    torch.manual_seed(SEED)
    model = build_arm_network(first_omega_0, dtype=dtype, device=device)
    opt = OptConfig()
    learning_rate = opt.lr_for_stage(spec.lr_stage)
    optimizer = make_adam(model, spec.lr_stage)
    scheduler = make_cosine(optimizer, budget)
    clipper = make_clipper() if clip_enabled else None
    stepper = _build_stepper(
        spec, model, data, optimizer, scheduler, clipper,
        physics=arm_physics, dtype=dtype, device=device,
    )
    monitor_traj = make_trajectory(model, ic13_t, masses_t) if physics_arm else None

    # SPEC Requirement 8: restore every component of a stopped arm exactly. Every
    # optimizer and scheduler state is loaded after the objects are rebuilt, so the
    # cosine continues at its own index rather than at a fresh one.
    if adam_resume:
        model.load_state_dict(saved["model"])
        optimizer.load_state_dict(saved["optimizer"])
        scheduler.load_state_dict(saved["scheduler"])
        if clipper is not None and saved.get("clipper") is not None:
            clipper.load_state_dict(saved["clipper"])
        if scheduled is not None and saved.get("scheduled_weights") is not None:
            scheduled.load_state_dict(saved["scheduled_weights"])
        if saved.get("rng") is None:
            raise ResumeRefused("the resume checkpoint holds no RNG state")
        restore_rng_state(saved["rng"], rng)
        stepper.clipped_steps = int(saved["clipped_steps"])
        if physics_arm and saved.get("frozen_monitor_times") is not None:
            frozen_monitor_times = saved["frozen_monitor_times"].numpy()
        trace = [dict(entry) for entry in saved["trace"]]
        monitor_log = [dict(entry) for entry in saved["monitor_log"]]
        driver_state = None if saved.get("driver") is None else dict(saved["driver"])
        adam_complete = bool(saved["adam_complete"])
        driven = driver_state if adam_complete else None
    else:
        driver_state = None
        adam_complete = False
        driven = None
        trace = []
        monitor_log = []

    stopped = {
        "extended": bool(driver_state["extended"]) if driver_state is not None else False
    }

    def on_extend():
        # D-03: the second cosine, on the same optimizer so Adam's moments are kept.
        stopped["extended"] = True
        stepper.scheduler = start_second_cosine(optimizer, budget)

    # A fixture budget below 20 steps cannot meet the frozen 5% cadence with whole
    # steps, so it is recorded against the rule but not held to it. A real arm is.
    enforce_cadence = not fixture
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
        if physics_arm:
            # D-06: a log, never a decision. The monitor runs only at the budget readings.
            monitor_log.append(
                {
                    "step": step,
                    **frozen_monitor_log(
                        monitor_traj,
                        masses_t,
                        frozen_monitor_times,
                        r_ref=r_ref,
                        microbatch_size=microbatch_size,
                        dtype=dtype,
                        device=device,
                    ),
                }
            )
        latest["result"], latest["step"] = result, step
        return float(result.E)

    try:
        if driven is None:
            driven = drive_adam(
                budget=budget,
                step_fn=stepper.step,
                read_fn=take_reading,
                scorecard=scorecard,
                on_extend=on_extend,
                clock=clock,
                enforce_cadence=enforce_cadence,
                stop_fn=stop_requested,
                resume_state=driver_state,
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
    if not adam_complete and driven["stopped"]:
        # SPEC Requirement 8: an Adam step boundary, after the checkpoint, is where a
        # governed stop leaves the arm. Nothing else is scored and nothing is written.
        entry = _stop_entry(phase="adam", step=driven["stopped_at_step"])
        stops.append(entry)
        save_resume_checkpoint(
            run_root,
            _resume_payload(
                spec=spec,
                phase="adam",
                invocations=invocations,
                stops=stops,
                timing_runs=timing_runs,
                timing=timing,
                budget=budget,
                frozen_budget=frozen_budget,
                driver=driven,
                adam_complete=False,
                trace=trace,
                monitor_log=monitor_log,
                model=model,
                optimizer=optimizer,
                scheduler=scheduler,
                clipper=clipper,
                scheduled=scheduled,
                rng_state=capture_rng_state(rng),
                frozen_monitor_times=frozen_monitor_times,
                clipped_steps=stepper.clipped_steps,
                adam_seconds=driven["adam_seconds"],
                total_seconds=clock() - total_started,
                first_omega_0=first_omega_0,
                runtime=runtime,
                protocol_sha256=protocol_sha256,
                module_sha256=module_sha256,
            ),
        )
        _write_stop_marker(run_root, spec, entry)
        raise GovernedStop(
            entry["exit_code"],
            signal_name=entry["signal"],
            phase="adam",
            step=driven["stopped_at_step"],
        )
    if not _all_finite(model.parameters()):
        # GAP-60-06: Adam ends at the last finite state, so this should not happen. If the
        # weights are not finite there is no polish, and the scorer refuses a non-finite
        # network, so no result can be formed. The arm stops and nothing is written.
        raise HarnessHalt(
            f"the Adam weights of arm {spec.arm_id} are not finite after step "
            f"{driven['steps_taken']}; no result can be scored and no polish is run"
        )
    if adam_complete:
        adam_gold = _saved_score(saved["adam"]["score_gold"])
        adam_block = dict(saved["adam"])
        adam_seconds = float(saved["adam_seconds"])
    else:
        adam_gold = latest["result"]
        if latest["step"] != driven["steps_taken"]:
            # GAP-60-06: Adam ended in a state no reading covered (a step was skipped
            # between two readings). That last finite state is scored now. It is not a
            # budget reading.
            adam_gold = _score(
                model, data, data.score, scorecard=scorecard, dtype=dtype, device=device
            )
        adam_seconds = driven["adam_seconds"]
        adam_block = None
    diverged = driven["outcome"] == "diverged"
    final_budget = budget if driven["new_budget_steps"] is None else driven["new_budget_steps"]
    cadence_ok = (
        None if diverged
        else scoring_cadence_ok(driven["reading_steps"], final_budget, scorecard=scorecard)
    )

    clip_settings = (clipper if clipper is not None else make_clipper()).state_dict()

    # SPEC Requirement 7: a counted arm compares against the committed two-Kepler row;
    # a probe never calls counts and records the formula as not applicable.
    e_formula = None
    formula_sha256 = None
    if spec.counted:
        formula_values, formula_sha256 = formula_reference()
        e_formula = formula_values.get(int(spec.system_id))

    def official_counts(name, result):
        """``counts`` for one scored state. A missing formula stops for the owner."""
        return _official_counts(
            arm_dir, spec, result,
            state=name, e_formula=e_formula, scorecard=scorecard,
            data_root=context.reader.data_root,
        )

    def cross_check(name, gold, official):
        """GAP-60-07: re-score the saved state on the CPU in float64 and compare."""
        state_dict = torch.load(arm_dir / f"{name}.weights", map_location="cpu", weights_only=True)
        cpu_result, cpu_counts = cross_check_state(
            state_dict, spec, data, first_omega_0, scorecard=scorecard, formula=e_formula
        )
        block = {
            "tier": int(cpu_result.tier),
            "E": float(cpu_result.E),
            "eps_h": float(cpu_result.eps_h),
            "counts": cpu_counts,
        }
        if int(cpu_result.tier) != int(gold.tier) or cpu_counts != official:
            reason = (
                f"the CPU float64 re-score of the {name} state disagrees with the official "
                f"score: tier {cpu_result.tier} vs {gold.tier}, counts {cpu_counts!r} vs "
                f"{official!r}"
            )
            write_owner_stop(
                arm_dir,
                stage=_CROSS_CHECK_STAGE,
                reason=reason,
                details={
                    "arm_id": spec.arm_id,
                    "state": name,
                    "official": {
                        "tier": int(gold.tier),
                        "E": float(gold.E),
                        "eps_h": float(gold.eps_h),
                        "counts": official,
                    },
                    "cross_check": block,
                },
                data_root=context.reader.data_root,
            )
            raise CrossCheckDisagreement(reason)
        return block

    if adam_block is None:
        adam_base = _score(model, data, data.beside, scorecard=scorecard, dtype=dtype, device=device)
        adam_file_sha, adam_tensor_digest = save_weights(arm_dir / "adam.weights", model)
        adam_counts = official_counts("adam", adam_gold)
        adam_cross = cross_check("adam", adam_gold, adam_counts)
        adam_block = {
            "score_gold": adam_gold.to_json_dict(),
            "score_base": adam_base.to_json_dict(),
            "cross_check": adam_cross,
            "weights": {
                "file": "adam.weights",
                "sha256": adam_file_sha,
                "tensor_digest": adam_tensor_digest,
            },
        }
    if not adam_complete and stop_requested():
        # The Adam-to-polish boundary is an Adam boundary too. The checkpoint says Adam
        # finished, so a resume goes straight to the handoff without repeating a step.
        entry = _stop_entry(phase="adam", step=driven["steps_taken"])
        stops.append(entry)
        save_resume_checkpoint(
            run_root,
            _resume_payload(
                spec=spec,
                phase="adam",
                invocations=invocations,
                stops=stops,
                timing_runs=timing_runs,
                timing=timing,
                budget=budget,
                frozen_budget=frozen_budget,
                driver=driven,
                adam_complete=True,
                adam=adam_block,
                trace=trace,
                monitor_log=monitor_log,
                model=model,
                optimizer=optimizer,
                scheduler=scheduler,
                clipper=clipper,
                scheduled=scheduled,
                rng_state=capture_rng_state(rng),
                frozen_monitor_times=frozen_monitor_times,
                clipped_steps=stepper.clipped_steps,
                adam_seconds=adam_seconds,
                total_seconds=clock() - total_started,
                first_omega_0=first_omega_0,
                runtime=runtime,
                protocol_sha256=protocol_sha256,
                module_sha256=module_sha256,
            ),
        )
        _write_stop_marker(run_root, spec, entry)
        raise GovernedStop(
            entry["exit_code"],
            signal_name=entry["signal"],
            phase="adam",
            step=driven["steps_taken"],
        )

    # GAP-60-05, 57-RULING.md:112-124: the rows, the pass-1 causal weights, the bin counts
    # and the loss weights are frozen once, at the Adam-to-L-BFGS handoff. A resumed polish
    # restores that frozen segment instead of drawing anything again.
    handoff_block = None
    polish_objective = None
    segment_block = None
    if physics_arm:
        if polish_resume:
            segment_block = dict(saved["segment"])
            handoff_times = segment_block["times"].numpy()
            frozen_w_n = segment_block["w_n"].to(device=device, dtype=dtype)
            bin_counts = segment_block["bin_counts"].to(device=device, dtype=dtype)
            frozen_weights = LossWeights(**dict(segment_block["weights"]))
        else:
            scheduled.freeze()
            frozen_weights = scheduled.current(0)
            handoff_times = draw_collocation_times(spec.train_key, rng, n_slots=n_slots)
            details, bin_counts = physics_pass1(
                make_trajectory(model, ic13_t, masses_t),
                masses_t,
                handoff_times,
                r_ref=r_ref,
                microbatch_size=microbatch_size,
                dtype=dtype,
                device=device,
            )
            frozen_w_n = details["w_n"]
            segment_block = {
                "times": torch.as_tensor(
                    np.ascontiguousarray(handoff_times, dtype=np.float64)
                ).clone(),
                "w_n": frozen_w_n.detach().cpu().clone(),
                "bin_counts": bin_counts.detach().cpu().clone(),
                "weights": {
                    "lambda_data": frozen_weights.lambda_data,
                    "lambda_ic": frozen_weights.lambda_ic,
                    "lambda_phys": frozen_weights.lambda_phys,
                    "lambda_e": frozen_weights.lambda_e,
                    "lambda_l": frozen_weights.lambda_l,
                },
            }
        polish_objective = _physics_objective(
            model,
            _PhysicsRun(
                handoff_times=handoff_times,
                frozen_w_n=frozen_w_n,
                frozen_bin_counts=bin_counts,
                frozen_weights=frozen_weights,
                data_points=None if spec.loss_arm == "physics_ic" else data.data_points,
                ic13_t=ic13_t,
                masses_t=masses_t,
                true_r0=data.true_r0,
                true_v0=data.true_v0,
                r_ref=r_ref,
                h0=h0,
                eps_h=eps_h,
                l0=l0,
                microbatch_size=microbatch_size,
            ),
            dtype=dtype,
            device=device,
        )
        handoff_block = {
            "rows_sha256": hashlib.sha256(
                np.ascontiguousarray(handoff_times, dtype=np.float64).tobytes()
            ).hexdigest(),
            "w_n": [float(value) for value in frozen_w_n.detach().cpu().tolist()],
            "weights": {
                "lambda_data": frozen_weights.lambda_data,
                "lambda_ic": frozen_weights.lambda_ic,
                "lambda_phys": frozen_weights.lambda_phys,
                "lambda_e": frozen_weights.lambda_e,
                "lambda_l": frozen_weights.lambda_l,
            },
        }
    else:
        # A data-only polish has no drawn segment: the full-batch set is fixed. The marker
        # keeps a polish checkpoint's segment state present and checkable.
        segment_block = {"kind": "data_only"}

    polish_resume_state = None
    if polish_resume:
        polish_resume_state = dict(saved["polish"])
        polish_resume_state["lbfgs"] = saved["lbfgs"]
    polish_result = _polish(
        model,
        data,
        scorecard=scorecard,
        adam_seconds=adam_seconds,
        adam_gold=adam_gold,
        dtype=dtype,
        device=device,
        clock=clock,
        objective=polish_objective,
        resume=polish_resume_state,
        stop_fn=stop_requested,
    )
    if polish_result["stopped"]:
        # SPEC Requirement 8: between polish outer calls, after restoring the parameters
        # from before the aborted call and keeping its pre-call L-BFGS state.
        entry = _stop_entry(phase="polish", step=polish_result["outer_calls"])
        stops.append(entry)
        save_resume_checkpoint(
            run_root,
            _resume_payload(
                spec=spec,
                phase="polish",
                invocations=invocations,
                stops=stops,
                timing_runs=timing_runs,
                timing=timing,
                budget=budget,
                frozen_budget=frozen_budget,
                driver=driven,
                adam_complete=True,
                adam=adam_block,
                trace=trace,
                monitor_log=monitor_log,
                model=model,
                optimizer=optimizer,
                scheduler=scheduler,
                clipper=clipper,
                scheduled=scheduled,
                rng_state=capture_rng_state(rng),
                frozen_monitor_times=frozen_monitor_times,
                clipped_steps=stepper.clipped_steps,
                adam_seconds=adam_seconds,
                polish_seconds=polish_result["elapsed_seconds"],
                total_seconds=clock() - total_started,
                segment=segment_block,
                lbfgs=polish_result["lbfgs"],
                polish={
                    "outer_calls": polish_result["outer_calls"],
                    "trace": polish_result["trace"],
                    "state": (
                        None if polish_result["gold"] is None
                        else polish_result["gold"].to_json_dict()
                    ),
                    "best_objective": polish_result["best_objective"],
                    "without_improvement": polish_result["without_improvement"],
                    "elapsed_seconds": polish_result["elapsed_seconds"],
                },
                first_omega_0=first_omega_0,
                runtime=runtime,
                protocol_sha256=protocol_sha256,
                module_sha256=module_sha256,
            ),
        )
        _write_stop_marker(run_root, spec, entry)
        raise GovernedStop(
            entry["exit_code"],
            signal_name=entry["signal"],
            phase="polish",
            step=polish_result["outer_calls"],
        )
    stop_reason = polish_result["stop_reason"]
    outer_calls = polish_result["outer_calls"]
    polish_trace = polish_result["trace"]
    polish_gold = polish_result["gold"]
    polish_seconds = polish_result["elapsed_seconds"]
    polish_base = _score(model, data, data.beside, scorecard=scorecard, dtype=dtype, device=device)
    polish_file_sha, polish_tensor_digest = save_weights(arm_dir / "polish.weights", model)
    polish_counts = official_counts("polish", polish_gold)
    polish_cross = cross_check("polish", polish_gold, polish_counts)

    chosen = better_state(
        {"E": adam_gold.E, "eps_h": adam_gold.eps_h},
        {"E": polish_gold.E, "eps_h": polish_gold.eps_h},
        scorecard=scorecard,
    )
    chosen_result = adam_gold if chosen == "adam" else polish_gold
    selected = chosen_result.to_json_dict()
    probe = str(spec.rung).startswith("probe")
    if spec.counted:
        result_counts = counts(chosen_result.tier, chosen_result.E, e_formula, scorecard=scorecard)
        formula_block = {
            "E_formula": e_formula,
            "counts": result_counts,
            "source_sha256": formula_sha256,
        }
    elif probe or not fixture:
        # SPEC Requirement 7: a probe is never counted and never calls counts.
        formula_block = {"E_formula": FORMULA_NOT_APPLICABLE, "counts": None, "source_sha256": None}
    else:
        formula_block = {"E_formula": FIXTURE_FORMULA_NOTE, "counts": None}

    schedule_block = {
        "lr_stage": spec.lr_stage,
        "lr_k": learning_rate,
        "betas": list(opt.adam_betas),
        "eps": opt.adam_eps,
        "cosine_t_max": max(budget, 1),
        "cosines": 2 if driven["extended"] else 1,
    }
    if physics_arm:
        schedule_block["warmup_steps"] = scheduled.warmup_length
    readout_notes = [] if physics_arm else [_D04_NOTE]
    if spec.rung == "probe-2b":
        readout_notes.append(_D05_NOTE)

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
        "schedule": schedule_block,
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
            "adam": adam_block,
            "polish": {
                "score_gold": polish_gold.to_json_dict(),
                "score_base": polish_base.to_json_dict(),
                "cross_check": polish_cross,
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
        "formula": formula_block,
        "wall": {
            "adam_seconds": adam_seconds,
            "polish_seconds": polish_seconds,
            "total_seconds": clock() - total_started,
        },
        "launch": {
            "invocations": invocations,
            "stops": [dict(item) for item in stops],
        },
        "timing_runs": timing_runs,
        "attestation": None if context.attestation is None else context.attestation.summary(),
        "mps_fallback_env": _PRE_IMPORT_FALLBACK,
        "readout_notes": readout_notes,
    }
    if physics_arm:
        record["r_ref"] = r_ref_block
        record["scorer_context_r_ref"] = (
            dict(admission["scorer_context_r_ref"])
            if admission is not None and admission.get("scorer_context_r_ref") is not None
            else governed_context_reference()
        )
        record["monitor_log"] = monitor_log
        record["handoff"] = handoff_block
        if s_h_block is not None:
            record["s_h"] = s_h_block
    if strict:
        record = build_real_record(
            spec=spec,
            run_parts=record,
            admission=admission,
            protocol=protocol,
            data_context=context,
        )
        validate_record(record)
    write_record_exclusive(record_path, record, data_root=context.reader.data_root)
    return record


# ---------------------------------------------------------------------------
# The real-arm command line (SPEC Requirement 8, SCOPE-44).
# ---------------------------------------------------------------------------

_USAGE = (
    "usage: python -B -m pinn.verification.learnability_run <arm-id> "
    "[--resume | --admit-only]"
)


def _parse_argv(argv):
    """``(arm_id, resume, admit_only)`` from one positional id and the two flags.

    The runner takes no runtime, precision or path argument: a real arm is seed 42 at
    MPS float32, and its records and setting come from the catalog and the admission.
    """
    arm_id = None
    resume = False
    admit_only = False
    for token in argv:
        if token == "--resume":
            if resume or admit_only:
                raise ValueError(
                    "--resume and --admit-only are mutually exclusive and appear once"
                )
            resume = True
        elif token == "--admit-only":
            if resume or admit_only:
                raise ValueError(
                    "--resume and --admit-only are mutually exclusive and appear once"
                )
            admit_only = True
        elif not isinstance(token, str) or token.startswith("-"):
            raise ValueError(f"{token!r} is not a flag of this runner")
        elif arm_id is None:
            arm_id = token
        else:
            raise ValueError("the runner takes exactly one arm id")
    if arm_id is None:
        raise ValueError("the runner takes one catalog arm id")
    return arm_id, resume, admit_only


def _write_process(run_dir, payload):
    """Write the arm's process record. A resume replaces the previous invocation's file."""
    path = Path(run_dir) / PROCESS_FILE
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path


def _available_memory():
    """The advisory free-memory figure, or ``None`` when ``vm_stat`` cannot be read.

    It is logged for the audit and never gates a launch: the footprint preflight is
    unreliable on this macOS (CONTEXT, Claude's Discretion).
    """
    try:
        return int(evidence_io.available_memory_bytes())
    except (evidence_io.MemoryPreflightError, OSError):
        return None


def main(argv=None):
    """The real-arm command line: admission first, one launch lock, the governed exits.

    ``python -B -m pinn.verification.learnability_run <arm-id> [--resume | --admit-only]``.
    ``admit_arm`` runs before anything else; ``--admit-only`` prints ``ADMIT-OK <id>`` and
    exits 0, or ``ADMIT-REFUSED: <reason>`` and exits 2, and creates nothing. A run takes
    the one-launch lock, records its own PID in ``runs/phase60/<arm-id>/process.json``,
    installs the three stop handlers and calls ``run_arm`` at the real runtime with the
    admission and the loaded protocol. The single top-level handler maps ``OwnerRouted``
    and ``CrossCheckDisagreement`` to ``OWNER-ROUTED`` with exit 3, once and without a
    retry, and a ``GovernedStop`` to its own 129, 130 or 143.
    """
    argv = list(sys.argv[1:] if argv is None else argv)
    _reset_stop()
    try:
        arm_id, resume, admit_only = _parse_argv(argv)
    except ValueError as exc:
        print(f"USAGE-REFUSED: {exc}", file=sys.stderr)
        print(_USAGE, file=sys.stderr)
        return EXIT_REFUSED
    try:
        spec = arm_spec(arm_id)
    except UnknownArm as exc:
        print(f"ADMIT-REFUSED: {exc}")
        return EXIT_REFUSED
    root = _repo_root()
    evidence = root / EVIDENCE_REL
    try:
        admission = admit_arm(
            arm_id, repo_root=root, evidence_root=evidence, resume=bool(resume)
        )
    except AdmissionRefused as exc:
        print(f"ADMIT-REFUSED: {exc}")
        return EXIT_REFUSED
    print(f"ADMIT-OK {arm_id}")
    if admit_only:
        return EXIT_OK
    run_root = arm_run_dir(arm_id, repo_root=root)
    _write_process(
        run_root,
        {
            "pid": os.getpid(),
            "utc_started": datetime.now(timezone.utc).isoformat(),
            "arm_id": arm_id,
            "resume": bool(resume),
            # Advisory only: the footprint preflight is unreliable on this macOS and no
            # memory value ever gates a run (CONTEXT, Claude's Discretion).
            "available_memory_bytes": _available_memory(),
        },
    )
    restore = install_stop_handlers()
    run_id = None
    try:
        try:
            run_id = evidence_io.begin_long_step(
                "phase60",
                arm_id,
                command=[
                    sys.executable, "-B", "-m", "pinn.verification.learnability_run", *argv,
                ],
                evidence_root=evidence,
            )
        except evidence_io.LaunchRefused as exc:
            print(str(exc))
            return EXIT_REFUSED
        context = open_real_context(repo_root=root)
        protocol = load_protocol(repo_root=root, evidence_root=evidence)
        run_arm(
            spec,
            context=context,
            scorecard=load_scorecard(),
            runtime=REAL_RUNTIME,
            evidence_root=evidence,
            admission=admission,
            protocol=protocol,
            clip_enabled=bool(admission["clip_enabled"]),
            resume=bool(resume),
            run_dir=run_root,
        )
        return EXIT_OK
    except (OwnerRouted, CrossCheckDisagreement) as exc:
        print(f"OWNER-ROUTED: {exc}")
        return EXIT_OWNER
    except GovernedStop as stop:
        return int(stop.exit_code)
    finally:
        restore()
        if run_id is not None:
            try:
                evidence_io.end_long_step(run_id, evidence_root=evidence)
            except evidence_io.LaunchRefused as exc:
                print(f"LAUNCH-LOCK-NOT-RELEASED: {exc}", file=sys.stderr)


if __name__ == "__main__":
    raise SystemExit(main())
