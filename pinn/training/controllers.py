"""Phase 40 / TRAIN-02 + TRAIN-06 wiring -- RunController + PlateauDetector.

Implements the inner two-phase Adam->L-BFGS optimization loop
(``ctl_instruction.md`` Phase-2a/2b) as a correct sequencing of torch's own
primitives: fresh-optimizer-per-stage-boundary, per-epoch resampled Adam with
merged gradient clipping (40-02), the CTX-46 within-stage handoff detector
(``PlateauDetector``, distinct from the CURR-03 stage-exit plateau in
``stage_exit.py``), a frozen-lambda no-clip fixed-batch L-BFGS phase with
accumulate-in-closure chunking, and the ADVANCE/RECOVER/HALT stage-exit gate
(40-04) polled every L-BFGS epoch. ``CurriculumController`` (added in 40-06)
wraps ``run_stage(k)`` into the outer curriculum loop.

GAP-40-01 / GAP-40-02 ruling (RESOLVED-WITH-INSTRUCTION 2026-07-17, see
40-04's ``<open_decision>``): ``StageExitMachine.evaluate`` returns
``disposition: StageDisposition | None`` (``None`` == keep training).
``run_stage`` polls until the first non-None disposition and its own return
type stays the non-Optional ``StageDisposition`` -- ``MAX_EPOCHS`` bounds the
WHOLE stage (``n_adam <= max_epochs``), and Adam-budget exhaustion without a
plateau hands off to L-BFGS via the ``trigger="budget-exhausted"`` variant of
the CTX-45 handoff event (vs ``trigger="plateau"`` for the detector path).

Loss-term wiring (engineering choice, documented -- ``ctl_instruction.md`` /
``pinn_architecture.md`` do not specify a multi-identity batching contract for
the L_IC/L_E/L_L terms, and ``pinn.loss_catalog``'s ``ic_anchor_loss`` /
``soft_energy_loss`` / ``angular_momentum_loss`` are single-trajectory-scoped
by signature, matching the ONLY existing reference Adam loop
(``pinn/verification/overfit_probe.py``)): ``L_data`` uses the FULL
multi-identity ``FixedBatch.data_points`` (direct forward, no AD); ``L_IC``,
``L_E``, and ``L_L`` anchor on a single deterministic representative identity
per fixed batch (the first replay key, falling back to the first data-point
identity), with ``h0``/``l0`` computed from that identity's ground-truth
snapshot-0 position/velocity via the same matched-Plummer / angular-momentum
formulas ``pinn.loss_catalog`` uses internally (reusing the module's private
helpers rather than duplicating the formula, to avoid a divergent second
copy). ``eps_h`` is the dataset-wide scale ``energy_floor_factor * S_H``
(``ε_H = 1e-4 · S_H``), threaded in as the required keyword-only
``RunController(s_h=…)`` constructor parameter from the validated
``training_metadata.json`` pipeline (CONF-03 / D-19); the per-anchor ``abs(h0)``
survives only in the loss denominator (``soft_energy_loss``), not as the scale.
``L_phys`` draws its interior collocation TIMES from ``CollocationSampler``
only (TRAIN-04) -- ``FixedBatch.collocation_points`` is never touched for the
physics/energy/angular-momentum terms (single collocation-point source, no
double-count).

Validation-pass grad discipline: the pass never calls ``.backward()`` /
``optimizer.step()`` (no parameter UPDATE occurs), but the physics/IC/energy/
angular-momentum terms need live autograd (second-order ``componentwise_du``)
to evaluate at all -- wrapping the whole pass in ``torch.no_grad()`` would
make that computation raise (no graph to differentiate), exactly why
``pinn/verification/overfit_probe.py``'s own diagnostics ("Diagnostics need AD
for physics/velocity; enable grad") skip ``no_grad`` around the AD-needing
call. This module follows that established precedent: ``model.eval()`` /
``model.train()`` bracket the pass in a ``try/finally`` (so the model returns
to train mode even if the forward raises); the absence of a training step is
what makes it "no-grad" in the sense that matters (no descent step), not a
literal ``torch.no_grad()`` context.
"""

from __future__ import annotations

import logging
import math
import time
from dataclasses import dataclass, replace
from typing import Any, Callable, Mapping, Optional, Sequence

import numpy as np
import torch

import pinn.loss_catalog as loss_catalog
from pinn.constants import T_CHARACTERISTIC_TIME
from pinn.data.batches import (
    build_stage_batch,
    sample_collocation_points,
    sample_data_points,
    select_stage_records,
    select_validation_records,
)
from pinn.data.types import FixedBatch
from pinn.loss_catalog import (
    LossTerms,
    angular_momentum_loss,
    causal_physics_loss,
    compose_total,
    data_huber_loss,
    ic_anchor_loss,
    soft_energy_loss,
)
from pinn.physics_residual import componentwise_du, softened_acceleration
from pinn.training import determinism
from pinn.training.checkpoint import (
    CHECKPOINT_SCHEMA_VERSION,
    EmptyCheckpointStore,
    PromotionRefused,
)
from pinn.training.run_metadata import validate_s_h
from pinn.training.slbfgs_preflight import check_stage_preflight
from pinn.training.stage_exit import StageDisposition


class _StopRequested(BaseException):
    """Abort an in-progress L-BFGS step at the next closure evaluation."""


__all__ = [
    "PlateauDetector",
    "HandoffEvent",
    "RunController",
    "accumulate_chunked_data_term",
    "build_checkpoint_payload",
    "CurriculumController",
    "ForcedDispositionOnLiveRun",
    "StageFactoryModelMismatch",
    "CHECKPOINT_SCHEMA_VERSION",
]

# ---------------------------------------------------------------------------
# CTX-46 Adam -> L-BFGS handoff detector (TRAIN-02 part a).
# ---------------------------------------------------------------------------

_HANDOFF_SLOPE_THRESHOLD = -5e-3
_HANDOFF_FIRE_COUNT = 50
# Floor used only to keep log10 defined for a non-positive loss reading; the
# physics loss is a mean of non-negative Huber-like terms and should never be
# exactly zero or negative in practice, but a floor avoids a math-domain crash
# instead of silently corrupting the detector's state.
_TINY_POSITIVE_LOSS = 1e-300

_GRAD_STAT_TERMS: tuple[tuple[str, str], ...] = (
    ("data", "lambda_data"),
    ("ic", "lambda_ic"),
    ("phys", "lambda_phys"),
    ("energy", "lambda_e"),
    ("angmom", "lambda_l"),
)


def _global_parameter_grad_norm(
    term: Optional[torch.Tensor],
    parameters: tuple[torch.nn.Parameter, ...],
    *,
    retain_graph: bool,
) -> Optional[float]:
    """Return a term's global parameter-gradient L2 norm without side effects.

    ``autograd.grad`` returns gradients as values and therefore does not write
    to ``parameter.grad``. Parameters unused by a connected term return
    ``None`` and contribute zero. A graphless scalar is a legitimate
    disconnected term and is recorded as exact zero without calling
    ``autograd.grad`` (``allow_unused`` does not cover graphless outputs).
    """
    if term is None:
        return None
    if not isinstance(term, torch.Tensor):
        return None
    if not term.requires_grad or term.grad_fn is None or not parameters:
        return 0.0
    try:
        gradients = torch.autograd.grad(
            term,
            parameters,
            create_graph=False,
            retain_graph=retain_graph,
            allow_unused=True,
            materialize_grads=False,
        )
    except (RuntimeError, TypeError):
        # Diagnostics are observation-only. A released or otherwise
        # unavailable graph is represented as missing telemetry so the sink
        # can fail closed without changing optimizer behavior.
        return None
    squared = [g.detach().reshape(-1).square().sum() for g in gradients if g is not None]
    if not squared:
        return 0.0
    total_squared = squared[0]
    for value in squared[1:]:
        total_squared = total_squared + value
    return float(torch.sqrt(total_squared).detach())


def _global_parameter_grad_norm_from_grads(
    parameters: tuple[torch.nn.Parameter, ...],
) -> float:
    """Return the global L2 norm of gradients already accumulated on params."""
    squared = [
        parameter.grad.detach().reshape(-1).square().sum()
        for parameter in parameters
        if parameter.grad is not None
    ]
    if not squared:
        return 0.0
    total_squared = squared[0]
    for value in squared[1:]:
        total_squared = total_squared + value
    return float(torch.sqrt(total_squared).detach())


def _build_gradient_stats(
    terms: Mapping[str, torch.Tensor],
    weights: Any,
    parameters: tuple[torch.nn.Parameter, ...],
    *,
    provenance: str,
    raw_overrides: Optional[Mapping[str, Optional[float]]] = None,
) -> dict[str, Any]:
    """Build the canonical raw/applied five-term gradient telemetry mapping."""
    stats: dict[str, Any] = {"grad_stats_provenance": provenance}
    complete = True
    for name, weight_name in _GRAD_STAT_TERMS:
        if raw_overrides is not None and name in raw_overrides:
            raw = raw_overrides[name]
        else:
            raw = _global_parameter_grad_norm(
                terms.get(name), parameters, retain_graph=True,
            )
        try:
            weight = float(getattr(weights, weight_name))
        except (AttributeError, TypeError, ValueError):
            weight = float("nan")
        applied = None if raw is None else weight * raw
        stats[f"grad_norm_raw_{name}"] = raw
        stats[f"grad_norm_applied_{name}"] = applied
        try:
            complete = complete and raw is not None and math.isfinite(float(raw))
            complete = complete and applied is not None and math.isfinite(float(applied))
            complete = complete and math.isfinite(weight) and weight >= 0.0
        except (TypeError, ValueError):
            complete = False
    stats["grad_stats_complete"] = bool(complete)
    return stats


class PlateauDetector:
    """CTX-46 within-stage Adam->L-BFGS handoff detector.

    ``update(l_phys)`` ingests one epoch's RAW (non-log) physics-loss scalar
    and tracks the per-epoch finite difference of ``log10(L_phys)``. The
    consecutive-qualifying-epoch counter increments while
    ``slope > -5e-3`` and RESETS to 0 on any violating epoch -- including the
    unavoidable first call, which has no prior value and therefore no slope
    (not a qualifying epoch). ``fires()`` is True once the counter reaches 50
    consecutive qualifying epochs.

    Distinct from ``TotalLossPlateauSmoother`` (``stage_exit.py`` CURR-03
    criterion 1, the stage-exit total-loss plateau) -- separate object,
    separate state, no shared smoothing (RESEARCH Pitfall 4).
    """

    def __init__(self) -> None:
        self._prev_log10: Optional[float] = None
        self._consecutive: int = 0

    @property
    def consecutive_qualifying_epochs(self) -> int:
        return self._consecutive

    def reset(self) -> None:
        self._prev_log10 = None
        self._consecutive = 0

    def update(self, l_phys: Any) -> bool:
        """Ingest one epoch's raw physics-loss scalar; return ``fires()``."""
        x = float(l_phys)
        log10_val = math.log10(x) if x > 0.0 else math.log10(_TINY_POSITIVE_LOSS)
        if self._prev_log10 is None:
            self._consecutive = 0
        else:
            slope = log10_val - self._prev_log10
            if slope > _HANDOFF_SLOPE_THRESHOLD:
                self._consecutive += 1
            else:
                self._consecutive = 0
        self._prev_log10 = log10_val
        return self.fires()

    def fires(self) -> bool:
        return self._consecutive >= _HANDOFF_FIRE_COUNT


@dataclass(frozen=True)
class HandoffEvent:
    """CTX-45 Adam->L-BFGS handoff record -- distinguishes the two triggers."""

    trigger: str  # "plateau" | "budget-exhausted"
    adam_epochs_used: int


# ---------------------------------------------------------------------------
# Chunked-accumulation data term (RESEARCH Pitfall 2 / Open Question 2).
# ---------------------------------------------------------------------------

def accumulate_chunked_data_term(
    model,
    data_points,
    *,
    weight: float,
    chunk_size: int,
    dtype,
    device,
) -> torch.Tensor:
    """Gradient-accumulating, weighted, chunked ``L_data`` backward.

    Splits ``data_points`` into fixed-size sub-chunks (the last chunk may be
    smaller), computes ``data_huber_loss`` per chunk, weights each chunk's
    contribution by ``weight * len(chunk) / N_total``, and calls
    ``.backward()`` per chunk so gradients ACCUMULATE in ``model``'s
    parameters -- by linearity of the gradient of a mean, this is
    mathematically identical to a single full-batch mean-reduction backward
    at the same ``weight``. Returns the accumulated (already-detached)
    weighted scalar loss as a 0-d tensor (for closure-return / logging).

    Callers MUST call ``optimizer.zero_grad()`` before invoking this and MUST
    NOT call ``.backward()`` again on the returned tensor (it carries no
    graph). An UNWEIGHTED chunk sum would scale the gradient by the chunk
    count and distort the L-BFGS objective -- the ``len(chunk)/N_total``
    weighting is a correctness requirement, not a style choice.
    """
    n_total = data_points.tau_ic13.shape[0]
    if n_total == 0:
        raise ValueError("accumulate_chunked_data_term requires a non-empty batch")
    if chunk_size <= 0:
        raise ValueError(f"chunk_size must be positive; got {chunk_size!r}")
    total = torch.zeros((), dtype=dtype, device=device)
    start = 0
    while start < n_total:
        end = min(start + chunk_size, n_total)
        pred = model(data_points.tau_ic13[start:end], data_points.masses[start:end])
        pred_pos = pred.reshape(-1, 3, 3)
        true_pos = data_points.targets[start:end].reshape(-1, 3, 3)
        chunk_loss = data_huber_loss(pred_pos, true_pos, dtype=dtype, device=device)
        chunk_weight = float(weight) * (end - start) / n_total
        weighted_chunk = chunk_weight * chunk_loss
        weighted_chunk.backward()
        total = total + weighted_chunk.detach()
        start = end
    return total


# ---------------------------------------------------------------------------
# CTX-53 checkpoint payload composer (HIGH 1 — single owned composition site).
# ---------------------------------------------------------------------------

def build_checkpoint_payload(
    controller: "RunController",
    curriculum_state: Any,
    config_identity: Any,
    schema_version: Any,
    invariant_b_state: Optional[Mapping[str, Any]] = None,
) -> dict[str, Any]:
    """Assemble the FULL CTX-53 envelope from a live RunController + live inputs.

    Single owned composition site for every save path (boundary anchors,
    mid-stage rolling, guard-trip failure, best/latest). ``schema_version``
    must be ``CHECKPOINT_SCHEMA_VERSION`` imported from ``checkpoint.py`` —
    this module never redefines it. ``curriculum_state`` and
    ``config_identity`` are handed in LIVE by the checkpoint_hook closure
    (or CurriculumController boundary path) so mid-stage fires never see
    None/stale stage metadata.
    """
    sd = controller.state_dict()
    return {
        "model": sd["model"],
        "optimizer": sd.get("optimizer"),
        "scheduled_weights": sd["scheduled_weights"],
        # state_dict keeps the Phase-40 key name ``clipper``; CTX-53 surface
        # uses ``grad_clip``.
        "grad_clip": sd["clipper"],
        "curriculum": curriculum_state,
        "rng": sd.get("rng"),
        "counters": sd.get("counters"),
        "config_identity": config_identity,
        "schema_version": schema_version,
        "invariant_b_state": invariant_b_state,
    }


# ---------------------------------------------------------------------------
# Per-fixed-batch anchor context (single-identity IC/energy/angmom evaluation).
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class _AnchorContext:
    """Everything needed to evaluate L_IC / L_phys / L_E / L_L for one batch."""

    traj: Any  # Callable[[torch.Tensor], torch.Tensor] -- scalar u -> (3,3) positions
    masses: torch.Tensor
    true_r0: torch.Tensor
    true_v0: torch.Tensor
    h0: float
    l0: torch.Tensor
    eps_h: float
    collocation_times: np.ndarray  # ascending-sorted, shape (N,)


class RunController:
    """The inner Adam->L-BFGS two-phase optimization loop for one stage.

    Constructed once per stage (mirroring ``TrainingConfig``'s single-stage
    ``StageConfig`` and ``ScheduledWeights``'s per-stage lambda^max caps);
    ``run_stage(k)`` runs the full Adam->L-BFGS closure for that stage and
    returns a non-Optional ``StageDisposition``.
    """

    def __init__(
        self,
        model,
        train_source,
        validation_source,
        config,
        scheduled_weights,
        grad_clipper,
        collocation_sampler,
        stage_exit_machine,
        checkpoint_store,
        runtime,
        *,
        s_h: float,
        rng: Optional[np.random.Generator] = None,
        checkpoint_hook: Optional[Callable[..., Any]] = None,
        guard_hook: Optional[Callable[..., Any]] = None,
        should_stop: Optional[Callable[[], bool]] = None,
        replay_count: Optional[int] = None,
    ) -> None:
        if validation_source is None:
            raise ValueError(
                "RunController requires a validation_source: ADVANCE criterion 2 "
                "is defined on a held-out set (ctl_instruction.md CURR-03), so a "
                "RunController built without one could not evaluate the gate"
            )
        # CONF-03 / D-18: the run-level S_H crosses the trust boundary here as a
        # REQUIRED keyword-only scalar (no default can mask a missing validated
        # value). Re-apply the single-home fail-closed predicate (validate_s_h)
        # at the consumption boundary -- finite AND strictly positive.
        self._s_h = validate_s_h(s_h)
        self._model = model
        self._train_source = train_source
        self._validation_source = validation_source
        self._config = config
        self._scheduled_weights = scheduled_weights
        self._grad_clipper = grad_clipper
        self._collocation_sampler = collocation_sampler
        self._stage_exit_machine = stage_exit_machine
        self._checkpoint_store = checkpoint_store
        self._runtime = runtime
        self._dtype = runtime.dtype
        self._device = runtime.torch_device
        self._rng = rng if rng is not None else np.random.default_rng(config.run.seed)

        # Phase-41 CTRL-08 / CTRL-02 / CTRL-07 additive surface (hooks default
        # None so a hook-less controller is byte-for-byte Phase 40).
        self._optimizer: Any = None
        self._global_step: int = 0
        self._global_epoch: int = 0
        self._pending_optimizer_state: Any = None
        self._last_val_total: Optional[float] = None
        self._wall_clock_baseline: float = float(time.monotonic())
        self._checkpoint_hook = checkpoint_hook
        self._guard_hook = guard_hook
        self._should_stop = should_stop
        # 43-03 ACC-02 DATA-05 replay-budget override. None preserves the
        # ``select_stage_records`` default (240) byte-for-byte; a positive int
        # (the smoke's 32) narrows the per-batch replay identity count.
        self._replay_count = replay_count
        # Live phase/epoch for curriculum_state_accessor (41-05 mid-stage resume).
        self._active_phase: Optional[str] = None
        self._active_epoch: int = 0

        self.last_handoff_event: Optional[HandoffEvent] = None

        # Phase-42 OPS-03/04b widened logging substrate (CTX-65 / CTX-70).
        # Populated by `_non_data_terms` (via `causal_physics_loss(return_details=True)`)
        # and read by `_log_step` so both Adam and L-BFGS records share one
        # provenance for w_n stats, per-bin residuals, and the non-data term
        # scalars. None-tolerant: tests that monkeypatch `_compose_loss_terms`
        # (bypassing `_non_data_terms`) still log without error.
        self._last_widened_details: Optional[dict] = None
        # Closure-local live non-data tensors. The weighted helper exposes
        # this transient mapping so L-BFGS can inspect each term graph before
        # its ordinary weighted backward; it is never persisted.
        self._last_non_data_terms: Optional[dict[str, torch.Tensor]] = None
        # Per-step-delta wall clock (distinct from `self._wall_clock_baseline`,
        # which is the run-start baseline). Used to derive `s_per_step` (EMA of
        # per-step wall time) and `eta_seconds` (stage-remaining ETA; null until
        # the EMA warms — CTX discretion).
        self._last_step_wall: Optional[float] = None
        self._s_per_step_ema: Optional[float] = None

    # ------------------------------------------------------------------
    # Public checkpoint surface (CTX-44 -- composes model + schedule + clipper
    # + Phase-41 optimizer / rng / counters).
    # ------------------------------------------------------------------
    def state_dict(self) -> dict[str, Any]:
        return {
            "model": self._model.state_dict(),
            "scheduled_weights": self._scheduled_weights.state_dict(),
            "clipper": self._grad_clipper.state_dict(),
            "optimizer": (
                self._optimizer.state_dict() if self._optimizer is not None else None
            ),
            "rng": determinism.capture_rng_state(self._rng),
            "counters": {
                "global_step": int(self._global_step),
                "global_epoch": int(self._global_epoch),
                "wall_clock_baseline": float(self._wall_clock_baseline),
            },
        }

    def load_state_dict(self, state: dict[str, Any]) -> None:
        self._model.load_state_dict(state["model"])
        self._scheduled_weights.load_state_dict(state["scheduled_weights"])
        # Phase-40 nested payloads use ``clipper``; CTX-53 envelopes use
        # ``grad_clip`` (build_checkpoint_payload renames on save).
        if "clipper" in state:
            self._grad_clipper.load_state_dict(state["clipper"])
        elif "grad_clip" in state:
            self._grad_clipper.load_state_dict(state["grad_clip"])
        # CYCLE-4 MEDIUM-5: DEFER optimizer into pending — live optimizer may
        # not exist yet (build-then-load). Boundary anchors carry optimizer=None
        # so pending stays None and the fresh Adam remains reset (CTRL-06).
        if "optimizer" in state:
            self._pending_optimizer_state = state.get("optimizer")
        rng_state = state.get("rng")
        if rng_state is not None:
            determinism.restore_rng_state(rng_state, self._rng)
        counters = state.get("counters")
        if isinstance(counters, Mapping):
            if "global_step" in counters:
                self._global_step = int(counters["global_step"])
            if "global_epoch" in counters:
                self._global_epoch = int(counters["global_epoch"])
            if "wall_clock_baseline" in counters:
                self._wall_clock_baseline = float(counters["wall_clock_baseline"])

    @property
    def checkpoint_store(self):
        return self._checkpoint_store

    @property
    def model(self):
        """The network instance this controller optimizes (read-only)."""
        return self._model

    @property
    def scheduled_weights(self):
        """This stage's PHYS-05 schedule (read-only; constructed once per stage)."""
        return self._scheduled_weights

    @property
    def s_per_step(self) -> Optional[float]:
        """Measured per-step wall-time EMA (read-only; None until it warms).

        43-03 ACC-02: the finite value after a smoke's steps is the sole source
        the persisted timing calibration records — never an invented duration.
        """
        return self._s_per_step_ema

    # ------------------------------------------------------------------
    # Anchor-identity selection + ground-truth conserved quantities.
    # ------------------------------------------------------------------
    def _select_anchor_key(self, batch):
        keys = tuple(batch.replay_keys) + tuple(batch.lookahead_keys)
        if not keys:
            keys = batch.data_points.record_keys
        return keys[0]

    def _build_anchor_context(self, source, batch, fixed_collocation_times) -> _AnchorContext:
        anchor_key = self._select_anchor_key(batch)
        record = source.get(anchor_key)
        ic13 = torch.as_tensor(
            np.asarray(record.ic13, dtype=np.float64), dtype=self._dtype, device=self._device
        )
        masses_t = torch.as_tensor(
            np.asarray(record.masses, dtype=np.float64), dtype=self._dtype, device=self._device
        )

        def traj(u_scalar: torch.Tensor) -> torch.Tensor:
            tau = (2.0 * u_scalar - 1.0).reshape(1)
            tau_ic13 = torch.cat([tau, ic13], dim=0).unsqueeze(0)
            pos = self._model(tau_ic13, masses_t.unsqueeze(0))
            return pos.reshape(3, 3)

        positions_gt = np.asarray(source.snapshot_positions(anchor_key), dtype=np.float64)
        velocities_gt = np.asarray(source.snapshot_velocities(anchor_key), dtype=np.float64)
        true_r0 = torch.as_tensor(positions_gt[0], dtype=self._dtype, device=self._device)
        true_v0 = torch.as_tensor(velocities_gt[0], dtype=self._dtype, device=self._device)

        h0 = float(
            loss_catalog._matched_plummer_hamiltonian(
                true_r0.unsqueeze(0), true_v0.unsqueeze(0), masses_t,
                dtype=self._dtype, device=self._device,
            )[0]
        )
        l0 = loss_catalog._angular_momentum(
            true_r0.unsqueeze(0), true_v0.unsqueeze(0), masses_t,
            dtype=self._dtype, device=self._device,
        )[0]
        # CONF-03 / D-19: ε_H is the dataset-wide scale, energy_floor_factor times
        # the validated run-level S_H (ε_H = 1e-4 · S_H). The per-anchor abs(h0)
        # survives only in the loss denominator (soft_energy_loss), not as the scale.
        eps_h = float(self._config.stage.energy_floor_factor) * self._s_h

        if fixed_collocation_times is None:
            colloc_times = self._collocation_sampler.uniform()
        else:
            colloc_times = fixed_collocation_times
        colloc_times = np.asarray(colloc_times, dtype=np.float64)
        order = np.argsort(colloc_times)

        return _AnchorContext(
            traj=traj,
            masses=masses_t,
            true_r0=true_r0,
            true_v0=true_v0,
            h0=h0,
            l0=l0,
            eps_h=eps_h,
            collocation_times=colloc_times[order],
        )

    # ------------------------------------------------------------------
    # Per-term loss evaluation (real, non-injected -- overridable per-test seams).
    # ------------------------------------------------------------------
    def _data_term(self, data_points) -> torch.Tensor:
        pred = self._model(data_points.tau_ic13, data_points.masses)
        pred_pos = pred.reshape(-1, 3, 3)
        true_pos = data_points.targets.reshape(-1, 3, 3)
        return data_huber_loss(pred_pos, true_pos, dtype=self._dtype, device=self._device)

    def _non_data_terms(self, anchor_ctx: _AnchorContext) -> dict[str, torch.Tensor]:
        zero_u = torch.zeros((), dtype=self._dtype, device=self._device)
        pred_r0 = anchor_ctx.traj(zero_u)
        first0, _second0 = componentwise_du(anchor_ctx.traj, zero_u)
        pred_v0 = first0.reshape(3, 3)
        ic_term = ic_anchor_loss(
            pred_r0, anchor_ctx.true_r0, pred_v0, anchor_ctx.true_v0,
            dtype=self._dtype, device=self._device,
        )

        u_leaf = torch.as_tensor(
            anchor_ctx.collocation_times / T_CHARACTERISTIC_TIME,
            dtype=self._dtype, device=self._device,
        )
        first, second = componentwise_du(anchor_ctx.traj, u_leaf)
        positions = torch.func.vmap(lambda s: anchor_ctx.traj(s).reshape(-1))(u_leaf)
        positions = positions.reshape(-1, 3, 3)
        velocities = first.reshape(-1, 3, 3)
        accel = second.reshape(-1, 3, 3)
        force = softened_acceleration(
            positions, anchor_ctx.masses, dtype=self._dtype, device=self._device,
        )
        residual = accel - force
        # CONF-04 / D-05: one vector-space average per time index.  The
        # residual has shape (N_t, 3 bodies, 3 Cartesian components), while
        # the locked Rbar contract averages the three body-vector energies,
        # not all nine scalar components.
        rbar = (residual ** 2).sum(dim=(-2, -1)) / 3.0
        times_tensor = torch.as_tensor(
            anchor_ctx.collocation_times, dtype=self._dtype, device=self._device,
        )
        # CTX-70 / OPS-04b: `return_details=True` exposes the detached causal
        # weights `w_n` and per-bin residuals `Rbar_n` without altering the
        # scalar `phys_term` (the default return is byte-for-byte unchanged, so
        # `_weighted_non_data_terms` and Phase 38/40 tests are untouched).
        phys_term, phys_details = causal_physics_loss(
            rbar, times=times_tensor, dtype=self._dtype, device=self._device,
            return_details=True,
        )

        energy_term = soft_energy_loss(
            positions, velocities, anchor_ctx.h0, anchor_ctx.eps_h,
            masses=anchor_ctx.masses, dtype=self._dtype, device=self._device,
        )
        angmom_term = angular_momentum_loss(
            positions, velocities, anchor_ctx.l0,
            masses=anchor_ctx.masses, dtype=self._dtype, device=self._device,
        )

        # Phase-42 OPS-03 widened logging surface: stash native-Python scalars
        # (NOT tensors — `json.dumps(allow_nan=False)` in 42-04 would
        # `TypeError` on a raw `torch.Tensor`) so both Adam and L-BFGS log
        # sites read ONE shared source (review finding #7). `front_idx` uses
        # `default=-1` so a collapsed causal-weight vector (no `w_n > 0.5`)
        # returns -1 instead of raising on an empty sequence (cycle-2 agy HIGH).
        w_n = phys_details["w_n"]
        rbar_det = phys_details["rbar"]
        w_n_list = w_n.tolist()
        self._last_widened_details = {
            "w_n_stats": {
                "w_min": float(w_n.min()),
                "w_mean": float(w_n.mean()),
                "w_max": float(w_n.max()),
                "front_idx": max(
                    [n for n, w in enumerate(w_n_list) if w > 0.5], default=-1,
                ),
            },
            "residuals_per_bin": [float(r) for r in rbar_det.tolist()],
            "ic": float(ic_term.detach()),
            "phys": float(phys_term.detach()),
            "energy": float(energy_term.detach()),
            "angmom": float(angmom_term.detach()),
        }
        return {"ic": ic_term, "phys": phys_term, "energy": energy_term, "angmom": angmom_term}

    def _weighted_non_data_terms(self, anchor_ctx: _AnchorContext, weights) -> torch.Tensor:
        terms = self._non_data_terms(anchor_ctx)
        self._last_non_data_terms = terms
        return (
            weights.lambda_ic * terms["ic"]
            + weights.lambda_phys * terms["phys"]
            + weights.lambda_e * terms["energy"]
            + weights.lambda_l * terms["angmom"]
        )

    def _compose_loss_terms(self, batch, anchor_ctx: _AnchorContext, weights) -> LossTerms:
        """The shared forward+compose step (Adam epochs + validation passes).

        A single, well-named seam: tests may monkeypatch this method on a
        constructed instance to inject a controlled ``.phys``/``.total``
        sequence (e.g. driving the plateau/budget-exhaustion handoff or a
        NaN-loss RECOVER path) without needing the real physics to organically
        behave a particular way, while everything else in ``run_stage``
        (fresh optimizer construction, clipping, scheduling, validation
        cadence) still runs for real.
        """
        data_term = self._data_term(batch.data_points)
        others = self._non_data_terms(anchor_ctx)
        terms = {"data": data_term, **others}
        return compose_total(terms, weights)

    # ------------------------------------------------------------------
    # Fixed-batch construction (DATA-05) with the optional replay-budget seam.
    # ------------------------------------------------------------------
    def _stage_batch(self, source, *, stage: int, collocation_count: int):
        """Build one DATA-05 fixed batch, honoring the replay-budget override.

        When ``replay_count`` is unset (every pre-43-03 run) this delegates to
        ``build_stage_batch`` byte-for-byte, so Phase-40/41/42 behavior is
        unchanged. When set (the admitted Stage-0 smoke, 43-03 ACC-02) it drives
        the SAME public DATA-05 selection/sampling pipeline
        (``select_stage_records`` -> ``sample_data_points`` ->
        ``sample_collocation_points``) with the configured replay budget — no
        bespoke smoke loader and no data-policy change, only the ``replay_count``
        argument threaded into ``select_stage_records``.
        """
        if self._replay_count is None:
            return build_stage_batch(
                source, stage=stage, rng=self._rng,
                dtype=self._dtype, device=self._device,
                collocation_count=collocation_count,
            )
        selected = select_stage_records(
            source, stage=stage, rng=self._rng,
            replay_count=int(self._replay_count),
        )
        selected_keys = selected.replay + selected.lookahead
        data_points = sample_data_points(
            source, selected_keys, rng=self._rng,
            dtype=self._dtype, device=self._device,
        )
        collocation_points = sample_collocation_points(
            source, selected_keys, rng=self._rng,
            dtype=self._dtype, device=self._device,
            collocation_count=collocation_count,
        )
        return FixedBatch(
            data_points=data_points,
            collocation_points=collocation_points,
            replay_keys=selected.replay,
            lookahead_keys=selected.lookahead,
        )

    def _validation_batch(self, *, stage: int, collocation_count: int):
        """Build one held-out validation batch over the full Stage-<=k pool.

        Identity set is ``select_validation_records`` — the entire validated
        held-out pool, no replay draw and no lookahead. Does not consult
        ``self._replay_count``.
        """
        selected = select_validation_records(self._validation_source, stage=stage)
        data_points = sample_data_points(
            self._validation_source, selected.replay, rng=self._rng,
            dtype=self._dtype, device=self._device,
        )
        collocation_points = sample_collocation_points(
            self._validation_source, selected.replay, rng=self._rng,
            dtype=self._dtype, device=self._device,
            collocation_count=collocation_count,
        )
        return FixedBatch(
            data_points=data_points,
            collocation_points=collocation_points,
            replay_keys=selected.replay,
            lookahead_keys=(),
        )

    # ------------------------------------------------------------------
    # Validation pass (TRAIN-06 wiring -- ADVANCE criteria 2/3/4 producer).
    # ------------------------------------------------------------------
    def _run_validation(self, k: int, weights) -> LossTerms:
        self._model.eval()
        try:
            batch = self._validation_batch(stage=k, collocation_count=1)
            anchor_ctx = self._build_anchor_context(self._validation_source, batch, None)
            loss_terms = self._compose_loss_terms(batch, anchor_ctx, weights)
        finally:
            self._model.train()
        return loss_terms

    # ------------------------------------------------------------------
    # Non-finite gates (small, independently-mockable seams -- see module
    # docstring on the M1 contract: the clipper's returned flag is the ONLY
    # gradient non-finite signal on the Adam path; the L-BFGS path has no
    # clipper call site, so its gradient check is this explicit method).
    # ------------------------------------------------------------------
    def _loss_finite(self, loss: torch.Tensor) -> bool:
        return bool(torch.isfinite(loss))

    def _grads_finite(self) -> bool:
        return all(
            p.grad is None or bool(torch.isfinite(p.grad).all())
            for p in self._model.parameters()
        )

    # ------------------------------------------------------------------
    # Minimal step log + loss-terms helper for L-BFGS guard bridge.
    # ------------------------------------------------------------------
    def _snapshot_training_causal_details(self) -> tuple[Optional[dict], Optional[list]]:
        """Immutable copy of the training-owned causal stash.

        Validation reuses the loss composer and overwrites
        ``_last_widened_details`` before ``_log_step``.
        """
        details = self._last_widened_details or {}
        stats = details.get("w_n_stats")
        residuals = details.get("residuals_per_bin")
        stats_copy = dict(stats) if isinstance(stats, Mapping) else None
        residuals_copy = list(residuals) if residuals is not None else None
        return stats_copy, residuals_copy

    def _log_step(
        self,
        *,
        step: int,
        loss_terms: Any,
        lr: Optional[float],
        phase: str,
        stage: int = 0,
        grad_norm: Optional[float] = None,
        w_n_stats: Optional[Mapping] = None,
        residuals_per_bin: Optional[Sequence[float]] = None,
        s_per_step: Optional[float] = None,
        eta_seconds: Optional[float] = None,
        epoch: Optional[int] = None,
        step_completed: bool = True,
        weights: Optional[loss_catalog.LossWeights] = None,
        gradient_stats: Optional[Mapping[str, Any]] = None,
    ) -> None:
        """CTX-52 / Phase-42 OPS-03 widened step log (canonical JSONL + TB panel).

        Single emission point (CTX-65): every downstream sink (JSONL handler,
        human mirror, TensorBoard residual panel) fans out from this one
        ``extra=`` dict. Guard-tripped / non-finite steps reach this method
        before the disposition ``return`` (Task 3) so a diverged step is
        recorded, not silently dropped.
        """
        try:
            total = float(loss_terms.total.detach()) if hasattr(loss_terms, "total") else float("nan")
            terms = {
                "data": float(loss_terms.data.detach()) if hasattr(loss_terms, "data") else None,
                "ic": float(loss_terms.ic.detach()) if hasattr(loss_terms, "ic") else None,
                "phys": float(loss_terms.phys.detach()) if hasattr(loss_terms, "phys") else None,
                "energy": float(loss_terms.energy.detach()) if hasattr(loss_terms, "energy") else None,
                "angmom": float(loss_terms.angmom.detach()) if hasattr(loss_terms, "angmom") else None,
            }
        except Exception:
            total = float("nan")
            terms = {}

        # Both Adam and L-BFGS read ONE shared source for w_n stats, per-bin
        # residuals, and the non-data term scalars (review finding #7). The
        # stash is None-tolerant (e.g. tests that monkeypatch
        # `_compose_loss_terms`, bypassing `_non_data_terms`). Explicit kwargs
        # take precedence so the L-BFGS full-record path (Task 3) can override.
        stash = self._last_widened_details or {}
        resolved_w_n_stats = w_n_stats if w_n_stats is not None else stash.get("w_n_stats")
        resolved_residuals = residuals_per_bin if residuals_per_bin is not None else stash.get("residuals_per_bin")

        # Per-step-delta wall clock (distinct from `self._wall_clock_baseline`,
        # the run-start baseline). `s_per_step` is an EMA of per-step wall
        # time; `eta_seconds` is the stage-remaining ETA, null until the EMA
        # warms (CTX discretion). Explicit kwargs override the computed values.
        now = float(time.monotonic())
        if self._last_step_wall is not None:
            dt = now - self._last_step_wall
            alpha = 0.1
            if self._s_per_step_ema is None:
                self._s_per_step_ema = dt
            else:
                self._s_per_step_ema = alpha * dt + (1.0 - alpha) * self._s_per_step_ema
        self._last_step_wall = now
        resolved_s_per_step = s_per_step if s_per_step is not None else self._s_per_step_ema
        resolved_eta_seconds = eta_seconds if eta_seconds is not None else None

        # Lambda weight-vector components under the CANONICAL names matching
        # the `LossWeights` dataclass fields EXACTLY (`lambda_data/ic/phys/e/l`
        # — NOT `lambda_energy`/`lambda_angmom`, which do not exist on
        # `LossWeights`). The logged value is the warmup-ramped
        # `λ·min(1, i/I_warm)` actually applied this step, not the raw
        # `ScheduledWeights` per-stage cap (cycle-2 claude-glm LOW).
        lambda_keys: dict[str, float] = {}
        if weights is not None:
            lambda_keys = {
                "lambda_data": weights.lambda_data,
                "lambda_ic": weights.lambda_ic,
                "lambda_phys": weights.lambda_phys,
                "lambda_e": weights.lambda_e,
                "lambda_l": weights.lambda_l,
            }

        # w_n stats keys (None-tolerant; emitted as null when the stash is
        # absent — the sink applies the null policy).
        w_keys: dict[str, Any] = {}
        if resolved_w_n_stats is not None:
            w_keys = {
                "w_min": resolved_w_n_stats.get("w_min"),
                "w_mean": resolved_w_n_stats.get("w_mean"),
                "w_max": resolved_w_n_stats.get("w_max"),
                "front_idx": resolved_w_n_stats.get("front_idx"),
            }

        # Per-bin residual scalars — OPS-04b TensorBoard-only fields. The
        # JSONL handler (42-04) filters these out when serializing; the TB
        # sink (42-05) reads them from this same widened record. Keeping them
        # in the single extra dict preserves the CTX-65 "one emission point,
        # sinks fan out" invariant.
        res_keys: dict[str, float] = {}
        if resolved_residuals is not None:
            res_keys = {
                f"residuals_bin_{n:02d}": r for n, r in enumerate(resolved_residuals)
            }

        # Gradient telemetry is an explicit step-local mapping rather than
        # part of ``_last_widened_details``: validation can overwrite that
        # stash before the training event is emitted. Recompute completeness
        # from the ten numeric fields so missing/non-finite values cannot be
        # mislabeled as a fully assembled record.
        resolved_gradient_stats = gradient_stats or {}
        grad_stats_complete = bool(
            resolved_gradient_stats.get("grad_stats_complete", False)
        )
        gradient_keys: dict[str, Any] = {}
        for term_name, _weight_name in _GRAD_STAT_TERMS:
            for kind in ("raw", "applied"):
                key = f"grad_norm_{kind}_{term_name}"
                value = resolved_gradient_stats.get(key)
                gradient_keys[key] = value
                try:
                    if value is None or not math.isfinite(float(value)):
                        grad_stats_complete = False
                except (TypeError, ValueError):
                    grad_stats_complete = False
        gradient_keys["grad_stats_provenance"] = resolved_gradient_stats.get(
            "grad_stats_provenance"
        )
        gradient_keys["grad_stats_complete"] = bool(grad_stats_complete)

        extra = {
            "event": "step",
            "step": step,
            "phase": phase,
            "total": total,
            "lr": lr,
            **{f"loss_{k}": v for k, v in terms.items()},
            **lambda_keys,
            "grad_norm": grad_norm,
            **w_keys,
            "s_per_step": resolved_s_per_step,
            "eta_seconds": resolved_eta_seconds,
            "epoch": epoch,
            "stage": stage,
            **gradient_keys,
            # ``record_complete`` asserts the STEP RECORD was fully assembled --
            # not that the optimizer advanced. The call-site ``step_completed``
            # argument carries the optimizer fact; ``grad_stats_complete``
            # carries the telemetry fact; both remain separately readable in
            # the emitted record.
            "record_complete": bool(step_completed) and bool(grad_stats_complete),
            **res_keys,
        }
        _LOGGER.info(
            "step=%s phase=%s total=%s lr=%s terms=%s",
            step, phase, total, lr, terms,
            extra=extra,
        )

    def _scalar_loss_terms(self, total_value: float) -> LossTerms:
        """Build a LossTerms carrier for the L-BFGS guard bridge (total only)."""
        zero = torch.zeros((), dtype=self._dtype, device=self._device)
        total = torch.tensor(float(total_value), dtype=self._dtype, device=self._device)
        return LossTerms(
            data=zero, ic=zero, phys=zero, energy=zero, angmom=zero, total=total,
        )

    def _lbfgs_full_loss_terms(self, closure_state: dict[str, Any]) -> LossTerms:
        """Full five-term LossTerms for the L-BFGS widened step log.

        Sources the data term from the closure's detached capture
        (`closure_state['data_detached']`) and the non-data per-term scalars
        from `self._last_widened_details` (populated by `_non_data_terms` via
        `causal_physics_loss(return_details=True)`), so the phase-2b JSONL
        record carries the full widened field set (review finding #7) rather
        than the total-only carrier from `_scalar_loss_terms`.

        Falls back to `_scalar_loss_terms` when the detached capture or stash
        is absent (e.g. a test bypassed `_non_data_terms`).

        CAVEAT: L-BFGS evaluates the closure multiple times per
        `optimizer.step(closure)` (line-search trials), so the logged
        per-term breakdown reflects the LAST closure evaluation, which may
        not be the accepted step — acceptable for a diagnostic panel.
        """
        stash = self._last_widened_details or {}
        data_detached = closure_state.get("data_detached")
        last_loss = closure_state.get("last_loss")
        if data_detached is None or not stash:
            return self._scalar_loss_terms(
                float(last_loss) if last_loss is not None else float("nan"),
            )
        zero = torch.zeros((), dtype=self._dtype, device=self._device)
        return LossTerms(
            data=torch.tensor(float(data_detached), dtype=self._dtype, device=self._device),
            ic=torch.tensor(stash.get("ic", 0.0), dtype=self._dtype, device=self._device),
            phys=torch.tensor(stash.get("phys", 0.0), dtype=self._dtype, device=self._device),
            energy=torch.tensor(stash.get("energy", 0.0), dtype=self._dtype, device=self._device),
            angmom=torch.tensor(stash.get("angmom", 0.0), dtype=self._dtype, device=self._device),
            total=torch.tensor(
                float(last_loss) if last_loss is not None else float("nan"),
                dtype=self._dtype, device=self._device,
            ),
        )

    def _apply_pending_optimizer_state(self) -> None:
        """CYCLE-4 MEDIUM-5: apply deferred Adam moments after fresh build."""
        if self._optimizer is not None and self._pending_optimizer_state is not None:
            self._optimizer.load_state_dict(self._pending_optimizer_state)
            self._pending_optimizer_state = None

    # ------------------------------------------------------------------
    # Phase 2a: Adam.
    # ------------------------------------------------------------------
    def _run_adam_phase(
        self,
        k: int,
        n_adam_k: int,
        optimizer,
        scheduler,
        plateau: PlateauDetector,
        train_loss_history: list,
        val_loss_history: list,
        state: dict,
        *,
        adam_start: int = 0,
    ) -> tuple[str, int]:
        validation_every = int(self._config.opt.validation_every)
        parameters = tuple(
            parameter for parameter in self._model.parameters()
            if parameter.requires_grad
        )
        handoff_trigger = "budget-exhausted"
        adam_epochs_used = int(adam_start)
        for epoch in range(int(adam_start), n_adam_k):
            if self._should_stop is not None and self._should_stop():
                state["disposition"] = StageDisposition.HALT
                return handoff_trigger, adam_epochs_used
            adam_epochs_used = epoch + 1
            self._active_phase = "2a"
            self._active_epoch = int(adam_epochs_used)
            batch = self._stage_batch(
                self._train_source, stage=k, collocation_count=1,
            )
            anchor_ctx = self._build_anchor_context(self._train_source, batch, None)
            weights = self._scheduled_weights.current(epoch)

            optimizer.zero_grad(set_to_none=True)
            loss_terms = self._compose_loss_terms(batch, anchor_ctx, weights)
            causal_w_n_stats, causal_residuals = self._snapshot_training_causal_details()
            gradient_stats = _build_gradient_stats(
                {
                    "data": getattr(loss_terms, "data", None),
                    "ic": getattr(loss_terms, "ic", None),
                    "phys": getattr(loss_terms, "phys", None),
                    "energy": getattr(loss_terms, "energy", None),
                    "angmom": getattr(loss_terms, "angmom", None),
                },
                weights,
                parameters,
                provenance="pre_total_backward",
            )

            # ---- Guard path (cycle-2 HIGH 1 + cycle-4 MEDIUM-2): Adam ----
            # Loss/grad exist before optimizer.step(); guard runs FIRST so a
            # NaN/Inf writes the failure bundle rather than the bare RECOVER.
            clip_outcome = None
            grad_norm: Optional[float] = None
            if self._guard_hook is not None:
                if self._loss_finite(loss_terms.total):
                    loss_terms.total.backward()
                    clip_outcome = self._grad_clipper.clip(self._model.parameters(), stage=k)
                    try:
                        grad_norm = float(clip_outcome.total_norm)
                    except Exception:
                        grad_norm = None
                guard_outcome = self._guard_hook(
                    self, loss_terms, grad_norm, self._global_step, k, "2a",
                )
                if (
                    guard_outcome is not None
                    and getattr(guard_outcome, "disposition", None) is not None
                ):
                    state["disposition"] = guard_outcome.disposition
                    # CTX-65 / OPS-04b: emit the widened record BEFORE the
                    # disposition return so a diverged step is recorded, not
                    # silently dropped. step = self._global_step + 1 is the
                    # index the completed step would have carried (the increment
                    # at the bottom of the loop hasn't run yet on this path).
                    self._log_step(
                        step=self._global_step + 1, loss_terms=loss_terms, lr=None,
                        phase="2a", stage=k, grad_norm=grad_norm,
                        step_completed=False, weights=weights,
                        gradient_stats=gradient_stats,
                        w_n_stats=causal_w_n_stats,
                        residuals_per_bin=causal_residuals,
                    )
                    return handoff_trigger, adam_epochs_used
                # Guard did not trip — inline checks fire as Phase 40.
                if not self._loss_finite(loss_terms.total):
                    state["disposition"] = StageDisposition.RECOVER
                    self._log_step(
                        step=self._global_step + 1, loss_terms=loss_terms, lr=None,
                        phase="2a", stage=k, grad_norm=None,
                        step_completed=False, weights=weights,
                        gradient_stats=gradient_stats,
                        w_n_stats=causal_w_n_stats,
                        residuals_per_bin=causal_residuals,
                    )
                    return handoff_trigger, adam_epochs_used
                if clip_outcome is None:
                    loss_terms.total.backward()
                    clip_outcome = self._grad_clipper.clip(self._model.parameters(), stage=k)
                if clip_outcome.non_finite:
                    state["disposition"] = StageDisposition.RECOVER
                    self._log_step(
                        step=self._global_step + 1, loss_terms=loss_terms, lr=None,
                        phase="2a", stage=k, grad_norm=grad_norm,
                        step_completed=False, weights=weights,
                        gradient_stats=gradient_stats,
                        w_n_stats=causal_w_n_stats,
                        residuals_per_bin=causal_residuals,
                    )
                    return handoff_trigger, adam_epochs_used
            else:
                # Phase-40 path: inline non-finite checks only.
                if not self._loss_finite(loss_terms.total):
                    state["disposition"] = StageDisposition.RECOVER
                    self._log_step(
                        step=self._global_step + 1, loss_terms=loss_terms, lr=None,
                        phase="2a", stage=k, grad_norm=None,
                        step_completed=False, weights=weights,
                        gradient_stats=gradient_stats,
                        w_n_stats=causal_w_n_stats,
                        residuals_per_bin=causal_residuals,
                    )
                    return handoff_trigger, adam_epochs_used
                loss_terms.total.backward()
                clip_outcome = self._grad_clipper.clip(self._model.parameters(), stage=k)
                if clip_outcome.non_finite:
                    state["disposition"] = StageDisposition.RECOVER
                    self._log_step(
                        step=self._global_step + 1, loss_terms=loss_terms, lr=None,
                        phase="2a", stage=k, grad_norm=grad_norm,
                        step_completed=False, weights=weights,
                        gradient_stats=gradient_stats,
                        w_n_stats=causal_w_n_stats,
                        residuals_per_bin=causal_residuals,
                    )
                    return handoff_trigger, adam_epochs_used

            optimizer.step()
            scheduler.step()

            state["epoch_count"] += 1
            self._global_step += 1
            self._global_epoch += 1
            train_loss_history.append(float(loss_terms.total.detach()))
            fires = plateau.update(float(loss_terms.phys.detach()))

            if state["epoch_count"] % validation_every == 0:
                val_terms = self._run_validation(k, weights)
                val_total = float(val_terms.total.detach())
                val_loss_history.append(val_total)
                self._last_val_total = val_total
                state["val_phys"] = float(val_terms.phys.detach())
                state["val_energy"] = float(val_terms.energy.detach())

            lr_now: Optional[float] = None
            try:
                lr_now = float(scheduler.get_last_lr()[0])
            except Exception:
                lr_now = None
            self._log_step(
                step=self._global_step, loss_terms=loss_terms, lr=lr_now, phase="2a",
                stage=k, grad_norm=grad_norm, epoch=int(adam_epochs_used), weights=weights,
                gradient_stats=gradient_stats,
                w_n_stats=causal_w_n_stats,
                residuals_per_bin=causal_residuals,
            )

            # Checkpoint/best hook AFTER validation so _last_val_total is live.
            if self._checkpoint_hook is not None:
                self._checkpoint_hook(self, self._global_step)

            if fires:
                handoff_trigger = "plateau"
                break

        return handoff_trigger, adam_epochs_used

    # ------------------------------------------------------------------
    # Phase 2b: L-BFGS.
    # ------------------------------------------------------------------
    def _make_lbfgs_closure(self, optimizer, fixed_batch, anchor_ctx, weights, chunk_size, closure_state):
        parameters = tuple(
            parameter for parameter in self._model.parameters()
            if parameter.requires_grad
        )

        def closure():
            if self._should_stop is not None and self._should_stop():
                raise _StopRequested
            optimizer.zero_grad(set_to_none=True)
            # A closure may be evaluated repeatedly by one L-BFGS optimizer
            # step. Never let an earlier evaluation's telemetry survive a
            # failed or partial later evaluation.
            closure_state["gradient_stats"] = None
            weighted_data = accumulate_chunked_data_term(
                self._model, fixed_batch.data_points,
                weight=weights.lambda_data, chunk_size=chunk_size,
                dtype=self._dtype, device=self._device,
            )
            # ``accumulate_chunked_data_term`` has fully accumulated the
            # weighted data-only gradient and freed each chunk graph. Capture
            # that norm before the non-data backward adds anything to .grad.
            data_raw = _global_parameter_grad_norm_from_grads(parameters)
            self._last_non_data_terms = None
            other_total = self._weighted_non_data_terms(anchor_ctx, weights)
            non_data_terms = self._last_non_data_terms or {}
            closure_state["gradient_stats"] = _build_gradient_stats(
                non_data_terms,
                weights,
                parameters,
                provenance="last_closure_evaluation",
                raw_overrides={"data": data_raw},
            )
            try:
                other_total.backward()
            finally:
                # Do not keep live term tensors (and their graph references)
                # beyond this closure evaluation.
                self._last_non_data_terms = None

            total = weighted_data + other_total.detach()
            closure_state["last_loss"] = float(total.detach())
            # Detached data-term capture for the post-step widened log (review
            # finding #7). The LAST closure invocation's value is the one the
            # log site reads; L-BFGS may evaluate the closure multiple times
            # per `optimizer.step(closure)` (line-search trials), so the logged
            # per-term breakdown reflects the last evaluation, which may not be
            # the accepted step — acceptable for a diagnostic panel.
            closure_state["data_detached"] = float(weighted_data.detach())
            if not self._loss_finite(total):
                closure_state["non_finite"] = True
                return total
            if not self._grads_finite():
                closure_state["non_finite"] = True
            return total

        return closure

    def _run_lbfgs_phase(
        self,
        k: int,
        remaining_budget: int,
        epoch_count_start: int,
        train_loss_history: list,
        val_loss_history: list,
        state: dict,
        *,
        lbfgs_start: int = 0,
    ):
        cfg = self._config
        self._scheduled_weights.freeze()
        weights_frozen = self._scheduled_weights.current(0)

        fixed_batch = self._stage_batch(
            self._train_source, stage=k, collocation_count=1,
        )
        fixed_collocation_times = self._collocation_sampler.uniform()
        anchor_ctx = self._build_anchor_context(self._train_source, fixed_batch, fixed_collocation_times)

        optimizer = torch.optim.LBFGS(
            self._model.parameters(),
            history_size=cfg.opt.lbfgs_history_size,
            max_iter=cfg.opt.lbfgs_max_iter,
            line_search_fn=cfg.opt.lbfgs_line_search,
        )
        # Live optimizer exposure is Adam-only for CTRL-06; L-BFGS is local.
        chunk_size = int(cfg.opt.lbfgs_chunk_size)
        validation_every = int(cfg.opt.validation_every)

        epoch_count = epoch_count_start
        # lbfgs_start is the number of L-BFGS epochs already consumed (resume).
        for _lbfgs_epoch in range(int(lbfgs_start), remaining_budget):
            if self._should_stop is not None and self._should_stop():
                self._scheduled_weights.rewarm()
                return StageDisposition.HALT
            self._active_phase = "2b"
            self._active_epoch = int(_lbfgs_epoch + 1)
            closure_state: dict[str, Any] = {
                "non_finite": False,
                "last_loss": None,
                "gradient_stats": None,
            }
            closure = self._make_lbfgs_closure(
                optimizer, fixed_batch, anchor_ctx, weights_frozen, chunk_size, closure_state
            )
            try:
                optimizer.step(closure)
            except _StopRequested:
                self._scheduled_weights.rewarm()
                return StageDisposition.HALT
            epoch_count += 1
            self._global_step += 1
            self._global_epoch += 1
            causal_w_n_stats, causal_residuals = self._snapshot_training_causal_details()

            # ---- Guard path (cycle-4 MEDIUM-2): L-BFGS ----
            # Loss/grads are computed INSIDE the closure during step, so the
            # guard runs AFTER step at the non_finite check — not first.
            if self._guard_hook is not None:
                last_loss = closure_state.get("last_loss")
                if closure_state["non_finite"]:
                    total_for_guard = float("nan")
                else:
                    total_for_guard = (
                        float(last_loss) if last_loss is not None else float("nan")
                    )
                loss_terms_for_guard = self._scalar_loss_terms(total_for_guard)
                guard_outcome = self._guard_hook(
                    self, loss_terms_for_guard, None, self._global_step, k, "2b",
                )
                if (
                    guard_outcome is not None
                    and getattr(guard_outcome, "disposition", None) is not None
                ):
                    self._scheduled_weights.rewarm()
                    # CTX-65 / OPS-04b: emit the widened record BEFORE the
                    # disposition return so a diverged L-BFGS step is recorded.
                    self._log_step(
                        step=self._global_step,
                        loss_terms=self._lbfgs_full_loss_terms(closure_state),
                        lr=None, phase="2b", stage=k, grad_norm=None,
                        step_completed=False, weights=weights_frozen,
                        gradient_stats=closure_state.get("gradient_stats"),
                        w_n_stats=causal_w_n_stats,
                        residuals_per_bin=causal_residuals,
                    )
                    return guard_outcome.disposition
                # Guard did not trip — bare RECOVER still fires if non_finite.
                if closure_state["non_finite"]:
                    self._scheduled_weights.rewarm()
                    self._log_step(
                        step=self._global_step,
                        loss_terms=self._lbfgs_full_loss_terms(closure_state),
                        lr=None, phase="2b", stage=k, grad_norm=None,
                        step_completed=False, weights=weights_frozen,
                        gradient_stats=closure_state.get("gradient_stats"),
                        w_n_stats=causal_w_n_stats,
                        residuals_per_bin=causal_residuals,
                    )
                    return StageDisposition.RECOVER
            else:
                if closure_state["non_finite"]:
                    self._scheduled_weights.rewarm()
                    self._log_step(
                        step=self._global_step,
                        loss_terms=self._lbfgs_full_loss_terms(closure_state),
                        lr=None, phase="2b", stage=k, grad_norm=None,
                        step_completed=False, weights=weights_frozen,
                        gradient_stats=closure_state.get("gradient_stats"),
                        w_n_stats=causal_w_n_stats,
                        residuals_per_bin=causal_residuals,
                    )
                    return StageDisposition.RECOVER

            train_loss_history.append(closure_state["last_loss"])

            if epoch_count % validation_every == 0:
                val_terms = self._run_validation(k, weights_frozen)
                val_total = float(val_terms.total.detach())
                val_loss_history.append(val_total)
                self._last_val_total = val_total
                state["val_phys"] = float(val_terms.phys.detach())
                state["val_energy"] = float(val_terms.energy.detach())

            # Widened step log for L-BFGS. Causal w_n/residuals come from the
            # pre-validation training snapshot; five-term breakdown still uses
            # closure_state['data_detached'] plus the last composer stash.
            if closure_state["last_loss"] is not None:
                self._log_step(
                    step=self._global_step,
                    loss_terms=self._lbfgs_full_loss_terms(closure_state),
                    lr=None, phase="2b", stage=k,
                    epoch=int(epoch_count),
                    weights=weights_frozen,
                    gradient_stats=closure_state.get("gradient_stats"),
                    w_n_stats=causal_w_n_stats,
                    residuals_per_bin=causal_residuals,
                )

            if self._checkpoint_hook is not None:
                self._checkpoint_hook(self, self._global_step)

            outcome = self._stage_exit_machine.evaluate(
                train_loss_history, val_loss_history,
                state["val_phys"], state["val_energy"],
                False, epoch_count,
            )
            if outcome.disposition is not None:
                self._scheduled_weights.rewarm()
                return outcome.disposition

        # Bounded loop exhausted without a disposition -- defensive backstop
        # only; by construction epoch_count reaches MAX_EPOCHS inside the
        # loop above and StageExitMachine.evaluate returns HALT there first.
        self._scheduled_weights.rewarm()
        return StageDisposition.HALT

    # ------------------------------------------------------------------
    # run_stage(k) -- the pinned entry point.
    # ------------------------------------------------------------------
    def run_stage(self, k: int, *, resume_ctx: Optional[Mapping[str, Any]] = None) -> StageDisposition:
        cfg = self._config
        n_adam_k = int(cfg.stage.n_adam)
        max_epochs = int(cfg.stage.max_epochs)

        resume_phase: Optional[str] = None
        resume_epoch = 0
        if resume_ctx is not None:
            resume_phase = resume_ctx.get("phase")  # "2a" | "2b"
            resume_epoch = int(resume_ctx.get("epoch", 0) or 0)

        optimizer = torch.optim.Adam(
            self._model.parameters(),
            lr=cfg.opt.lr_for_stage(k),
            betas=cfg.opt.adam_betas,
            eps=cfg.opt.adam_eps,
        )
        # Expose live Adam (Pattern 4) + apply deferred moments (MEDIUM-5).
        self._optimizer = optimizer
        self._apply_pending_optimizer_state()

        adam_start = 0
        scheduler_last_epoch = -1
        epoch_count_init = 0
        skip_adam = False
        if resume_phase == "2a":
            adam_start = max(0, min(resume_epoch, n_adam_k))
            scheduler_last_epoch = adam_start - 1
            epoch_count_init = adam_start
        elif resume_phase == "2b":
            # Adam budget already consumed; re-enter L-BFGS at resume_epoch.
            skip_adam = True
            adam_start = n_adam_k
            epoch_count_init = n_adam_k + max(0, resume_epoch)

        scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(
            optimizer, T_max=max(n_adam_k, 1), last_epoch=scheduler_last_epoch,
        )

        self._grad_clipper.clear()
        self._scheduled_weights.rewarm()
        plateau = PlateauDetector()

        train_loss_history: list[float] = []
        val_loss_history: list[float] = []
        state: dict[str, Any] = {
            "epoch_count": int(epoch_count_init),
            "val_phys": math.inf,
            "val_energy": math.inf,
            "disposition": None,
        }

        if skip_adam:
            handoff_trigger = "budget-exhausted"
            adam_epochs_used = n_adam_k
        else:
            handoff_trigger, adam_epochs_used = self._run_adam_phase(
                k, n_adam_k, optimizer, scheduler, plateau,
                train_loss_history, val_loss_history, state,
                adam_start=adam_start,
            )
        self.last_handoff_event = HandoffEvent(
            trigger=handoff_trigger, adam_epochs_used=adam_epochs_used,
        )
        if state["disposition"] is not None:
            return state["disposition"]

        remaining_budget = max(max_epochs - adam_epochs_used, 0)
        if remaining_budget == 0 and not skip_adam:
            # CR-02 / GAP-40-02: equality n_adam == max_epochs is legal with
            # zero L-BFGS headroom. Poll the stage-exit machine once at the
            # shared boundary so a satisfied gate yields ADVANCE and an unmet
            # gate yields HALT by construction — do not shortcut to HALT.
            # had_nan_inf=False is correct here: Adam non-finite already
            # returned RECOVER above. Do not rewarm(): freeze() never ran.
            outcome = self._stage_exit_machine.evaluate(
                train_loss_history, val_loss_history,
                state["val_phys"], state["val_energy"],
                False, state["epoch_count"],
            )
            if outcome.disposition is StageDisposition.ADVANCE:
                return StageDisposition.ADVANCE
            if outcome.disposition is StageDisposition.RECOVER:
                return StageDisposition.RECOVER
            return StageDisposition.HALT

        lbfgs_start = 0
        if resume_phase == "2b":
            lbfgs_start = max(0, resume_epoch)
            # remaining_budget is total L-BFGS slots from a full Adam budget;
            # re-entry still iterates range(lbfgs_start, remaining_budget).
            remaining_budget = max(max_epochs - n_adam_k, 0)
            if remaining_budget == 0:
                remaining_budget = max(max_epochs - adam_epochs_used, 1)

        return self._run_lbfgs_phase(
            k, remaining_budget, state["epoch_count"],
            train_loss_history, val_loss_history, state,
            lbfgs_start=lbfgs_start,
        )


# ---------------------------------------------------------------------------
# CurriculumController -- the outer curriculum loop (TRAIN-01).
# ---------------------------------------------------------------------------

_LOGGER = logging.getLogger("pinn.training.controllers")


class ForcedDispositionOnLiveRun(Exception):
    """T-40-09 typed guard -- the ONE mechanism, no alternative.

    Raised at ``CurriculumController`` CONSTRUCTION when a
    ``forced_disposition`` injection is supplied together with ANY live-run
    construct (a live ``run_controller`` and/or a ``stage_factory``). T-40-09
    is the HIGH-severity spurious-stage-advance threat: a test-side "assert
    the injection is unset whenever a live run executes" would guard only
    the code paths a test happens to exercise, whereas raising here makes
    the unsafe combination impossible to construct on EVERY path, including
    ones no test covers. Do not add a second guard (e.g. an ``assert``
    elsewhere in this class) -- two mechanisms for one contract means
    neither is the contract.
    """

    def __init__(self) -> None:
        super().__init__(
            "CurriculumController refuses construction with BOTH a "
            "forced_disposition injection and any live-run construct "
            "(run_controller and/or stage_factory) supplied together -- a "
            "forced signal could silently steer a live run toward a "
            "spurious stage advance (T-40-09, HIGH severity). This is the "
            "ONLY guard: pass forced_disposition alone, or a live-run "
            "construct (run_controller, optionally with stage_factory), "
            "never both."
        )


class StageFactoryModelMismatch(Exception):
    """GAP-40-04 model-continuity guard -- curriculum weights must persist.

    Raised when ``stage_factory(k+1)`` returns a ``RunController`` whose
    ``model`` is not identity-same as the model the curriculum already held.
    Curriculum learning carries network weights across stages; only the Adam
    state resets at a boundary (40-SPEC R2). Accepting a foreign model would
    silently discard all prior training with no symptom.
    """

    def __init__(self) -> None:
        super().__init__(
            "stage_factory returned a RunController whose model is not the "
            "same object the curriculum already held -- curriculum learning "
            "requires weight continuity across stages (only Adam state "
            "resets at a boundary; 40-SPEC R2). A foreign model would "
            "silently discard all prior training (GAP-40-04 / T-40-12)."
        )


class CurriculumController:
    """The outer curriculum loop (TRAIN-01): stage progression + dispatch.

    Wraps a per-stage ``StageDisposition`` (from a live ``RunController`` or
    the forced-disposition injection seam) into stage progression: ADVANCE
    checkpoints the stage boundary (stage-{k}-final + stage-{k+1}-init) and
    increments the stage index; when a ``stage_factory`` is injected the
    controller obtains that stage's ``RunController`` from it (carrying that
    stage's ``ScheduledWeights`` / ``TrainingConfig`` / ``GradClipper``) and
    rebinds its own schedule reference so the two cannot diverge; with no
    factory (the default) the run is single-stage and stages >= 1 are NOT
    reconfigured (PLAT-01) -- only ``ScheduledWeights.rewarm()`` runs.
    RECOVER rolls back to the last well-formed checkpoint and, at the
    default ``recover_retries=0`` (CTX-41's ratified ``recover.retries: 0``),
    transitions straight to HALT with no retrain attempt; HALT stops for
    owner review. There is no fallback advancement -- only ADVANCE ever
    changes the stage.

    Injection seams (TRAIN-01 ACs):

    - ``forced_disposition`` is an optional
      ``Callable[[int], StageDisposition]`` that, when supplied, replaces the
      live ``run_controller.run_stage(k)`` call entirely. Mutually exclusive
      with any live-run construct (``run_controller`` and/or
      ``stage_factory``): supplying both raises
      ``ForcedDispositionOnLiveRun`` at construction (T-40-09).
    - ``stage_factory`` is an optional ``Callable[[int], RunController]``
      (GAP-40-04 Option C). On ADVANCE the controller replaces its live
      ``RunController`` with ``stage_factory(k+1)`` after verifying model
      identity (raises ``StageFactoryModelMismatch`` on mismatch). Default
      ``None`` preserves the single-stage path byte-for-byte (PLAT-01).
      Per-stage ``n_adam`` / ``max_epochs`` / ``eps_*`` are NEVER invented
      here (SCOPE-19) -- they arrive through the seam from the caller.
    - ``stage_0_only`` (bool, default ``False``; SCOPE-27 / 50-CONTEXT.md
      D-01) is a fresh-run-only conformance ceiling: when a Stage-0
      ``run_stage(0)`` returns ADVANCE, ``step()`` persists the ordinary
      ``stage-0-final`` boundary and logs the exit, and ``run()`` then
      returns that ADVANCE as terminal -- before any stage increment,
      ``stage_factory`` / Stage-1 conformance call, ``stage-1-init`` write,
      0->1 promotion, disposition record, or Stage-1 rewarm. ``False`` (the
      default) preserves the ordinary loop byte-for-byte. Not a general
      multi-stage platform switch -- it only enforces the Stage-0-only
      training authorization.

    Owns the current stage index, the injected ``CheckpointStore``, the live
    ``RunController`` (when present), and the rebound ``ScheduledWeights``
    reference (CTX-33/38/41; GAP-40-04).
    """

    def __init__(
        self,
        config: Any,
        checkpoint_store: Any,
        scheduled_weights: Any,
        *,
        run_controller: Optional[RunController] = None,
        forced_disposition: Optional[Callable[[int], StageDisposition]] = None,
        stage_factory: Optional[Callable[[int], RunController]] = None,
        conformance_hook: Optional[Callable[[int, Any], None]] = None,
        invariant_b_state_provider: Optional[Callable[[], Mapping[str, Any]]] = None,
        recover_retries: int = 0,
        initial_stage: int = 0,
        stage_0_only: bool = False,
    ) -> None:
        # T-40-09: forced disposition is mutually exclusive with ANY live-run
        # construct (run_controller and/or stage_factory). One guard, no assert.
        if forced_disposition is not None and (
            run_controller is not None or stage_factory is not None
        ):
            raise ForcedDispositionOnLiveRun()
        if run_controller is None and forced_disposition is None:
            raise ValueError(
                "CurriculumController requires exactly one of run_controller "
                "or forced_disposition to obtain a StageDisposition per stage"
            )
        if (
            not isinstance(recover_retries, int)
            or isinstance(recover_retries, bool)
            or recover_retries < 0
        ):
            raise ValueError(
                f"recover_retries must be a non-negative int (got "
                f"{recover_retries!r}); CTX-41's ratified default is 0"
            )
        self._config = config
        self._checkpoint_store = checkpoint_store
        self._scheduled_weights = scheduled_weights
        self._run_controller = run_controller
        self._forced_disposition = forced_disposition
        self._stage_factory = stage_factory
        self._conformance_hook = conformance_hook
        self._invariant_b_state_provider = invariant_b_state_provider
        self._recover_retries = int(recover_retries)
        self._recover_attempts = 0
        self._stage = int(initial_stage)
        self._stage_0_only = bool(stage_0_only)
        self._halted = False
        # One-shot mid-stage resume context (consumed by first run_stage only).
        self._pending_resume_ctx: Optional[Mapping[str, Any]] = None

    @property
    def stage(self) -> int:
        """The current curriculum stage index (Δstage tracked by tests)."""
        return self._stage

    @property
    def halted(self) -> bool:
        """True once a HALT (direct or RECOVER-exhausted) has been reached."""
        return self._halted

    # ------------------------------------------------------------------
    # Disposition acquisition -- forced injection XOR live RunController
    # (exactly one is non-None per the constructor's T-40-09 guard).
    # ------------------------------------------------------------------
    def _get_disposition(self, stage: int) -> StageDisposition:
        if self._forced_disposition is not None:
            return self._forced_disposition(stage)
        # Consume one-shot resume_ctx for the ENTERED stage only (41-05).
        ctx = self._pending_resume_ctx
        self._pending_resume_ctx = None
        disposition = self._run_controller.run_stage(stage, resume_ctx=ctx)
        self._log_handoff_if_any()
        return disposition

    # ------------------------------------------------------------------
    # Checkpoint payload / run-start anchor (cycle-2 H3).
    # ------------------------------------------------------------------
    def _checkpoint_payload(self, tag: str, stage: int) -> dict[str, Any]:
        """Phase-40 nested payload (tag/stage/run_controller) for save() spies."""
        payload: dict[str, Any] = {"tag": tag, "stage": stage}
        if self._run_controller is not None:
            payload["run_controller"] = self._run_controller.state_dict()
        return payload

    def _curriculum_state(self) -> dict[str, Any]:
        """Live curriculum metadata for build_checkpoint_payload (HIGH 2)."""
        return {
            "stage": int(self._stage),
            "phase": None,
            "epoch": 0,
            "step": self._disposition_step(),
            "disposition_log_pointer": None,
        }

    def _config_identity(self) -> Any:
        """Frozen config identity if set by pinn.train (41-05); else empty dict."""
        return getattr(self, "_config_identity_payload", None) or {}

    def _disposition_step(self) -> int:
        """Global step for ledger rows — live counter or stage surrogate."""
        if self._run_controller is not None:
            return int(getattr(self._run_controller, "_global_step", 0))
        return int(self._stage)

    def _save_ctx53_anchor(self, tag: str, stage: int) -> None:
        """Production CTX-53 anchor via the single composer + save_anchor."""
        if self._run_controller is None:
            return
        payload = build_checkpoint_payload(
            self._run_controller,
            self._curriculum_state(),
            self._config_identity(),
            CHECKPOINT_SCHEMA_VERSION,
            invariant_b_state=(
                self._invariant_b_state_provider()
                if self._invariant_b_state_provider is not None
                else None
            ),
        )
        self._checkpoint_store.save_anchor(tag=tag, stage=stage, payload=payload)

    def _save_run_start_anchor(self) -> None:
        """Save the k=0 rollback anchor BEFORE the first stage is entered.

        The k=0 analog of the stage-{k+1}-init anchor the ADVANCE branch
        already saves at every later boundary: without it, a cold-start
        RECOVER (a NaN/Inf on an early close-encounter sample -- exactly the
        sample class that produces one) would hit a genuinely empty
        CheckpointStore. The ``except EmptyCheckpointStore`` in the RECOVER
        branch below is the backstop that keeps the run numerically valid
        even if this anchor save is skipped, suppressed, or fails -- do not
        drop that catch on the grounds that this anchor makes it redundant.
        """
        # CTRL-06: stage-0-init carries reset Adam (optimizer cleared).
        if self._run_controller is not None:
            self._run_controller._optimizer = None
        self._checkpoint_store.save(self._checkpoint_payload("stage-0-init", self._stage))
        self._save_ctx53_anchor("stage-0-init", self._stage)

    # ------------------------------------------------------------------
    # CTX-38/45 logging (stdlib logging.getLogger('pinn.training.*') tree,
    # machine-readable key/value payloads via ``extra``).
    # ------------------------------------------------------------------
    def _log_run_start(self) -> None:
        fields = self._config.provisional_fields()
        summary = "; ".join(
            f"{f['name']}={f['value']!r} (provisional, {f['provenance']})"
            for f in fields
        )
        _LOGGER.info(
            "run-start provisional thresholds: %s", summary,
            extra={"event": "run_start_provisional_thresholds", "count": len(fields)},
        )

    def _log_stage_exit(self, disposition: StageDisposition, *, stage: int, **fields: Any) -> None:
        _LOGGER.info(
            "stage-exit disposition=%s stage=%s", disposition.value, stage,
            extra={
                "event": "stage_exit_disposition",
                "disposition": disposition.value,
                "stage": stage,
                **fields,
            },
        )

    def _log_handoff_if_any(self) -> None:
        if self._run_controller is None:
            return
        event = self._run_controller.last_handoff_event
        if event is None:
            return
        _LOGGER.info(
            "adam-to-lbfgs handoff trigger=%s adam_epochs_used=%s",
            event.trigger, event.adam_epochs_used,
            extra={
                "event": "adam_lbfgs_handoff",
                "trigger": event.trigger,
                "adam_epochs_used": event.adam_epochs_used,
            },
        )

    # ------------------------------------------------------------------
    # step() -- one stage-exit dispatch; run() -- the full curriculum loop.
    # ------------------------------------------------------------------
    def step(self) -> StageDisposition:
        """Advance the curriculum by exactly one stage-exit dispatch.

        ``check_stage_preflight(k)`` runs BEFORE any disposition is obtained
        (TRAIN-07): a stage >= 3 request is refused before either a live
        RunController or the forced-disposition seam ever runs. Dispatch is
        an exact three-way match on the disposition -- there is no fallback
        advancement (T-40-09): only ADVANCE ever changes ``self.stage``.
        """
        check_stage_preflight(self._stage)
        if self._conformance_hook is not None:
            self._conformance_hook(self._stage, self._scheduled_weights)
        disposition = self._get_disposition(self._stage)

        if disposition is StageDisposition.ADVANCE:
            k = self._stage
            step = self._disposition_step()
            # stage-{k}-final carries the EXITING stage's state (OLD controller).
            self._checkpoint_store.save(self._checkpoint_payload(f"stage-{k}-final", k))
            self._save_ctx53_anchor(f"stage-{k}-final", k)
            if self._stage_0_only and k == 0:
                # SCOPE-27 / 50-CONTEXT.md D-01 fresh-run Stage-0 ceiling: the
                # ordinary stage-0-final boundary is already persisted above;
                # log the Stage-0 exit and terminate here -- BEFORE the stage
                # increment, any stage_factory / Stage-1 conformance_hook
                # call, the stage-1-init write, the 0->1 promotion, the
                # k->k+1 disposition record, and the Stage-1 rewarm. Every
                # persisted stage field therefore stays 0 and no Stage-1
                # checkpoint is ever created. ``run()`` treats this ADVANCE
                # as terminal (below) rather than looping into a second
                # ``run_stage(0)`` call.
                self._log_stage_exit(StageDisposition.ADVANCE, stage=k)
                return StageDisposition.ADVANCE
            self._stage = k + 1
            # GAP-40-04 Option C: replace the live RunController before the
            # stage-{k+1}-init save so the anchor carries the ENTERED stage's
            # collaborators (ScheduledWeights caps restore from payload on
            # RECOVER; a pre-swap init anchor would re-pin stage k+1 to stage
            # k's lambda^max -- T-40-13 / CR-03 through the back door).
            if self._stage_factory is not None:
                previous_model = self._run_controller.model
                new_controller = self._stage_factory(self._stage)
                if new_controller.model is not previous_model:
                    raise StageFactoryModelMismatch()
                # Drop the outgoing stage-k optimizer before the entered-stage
                # init anchor is serialized (CTRL-06 / MEDIUM fix).
                if self._run_controller is not None:
                    self._run_controller._optimizer = None
                self._run_controller = new_controller
                self._scheduled_weights = new_controller.scheduled_weights
            if self._conformance_hook is not None:
                self._conformance_hook(self._stage, self._scheduled_weights)
            # CTRL-06 composition: stage-{k+1}-init is sourced from the ENTERED
            # (post-swap) controller with self._optimizer EXPLICITLY CLEARED so
            # the anchor carries reset Adam (optimizer key None).
            if self._run_controller is not None:
                self._run_controller._optimizer = None
            self._checkpoint_store.save(
                self._checkpoint_payload(f"stage-{self._stage}-init", self._stage)
            )
            self._save_ctx53_anchor(f"stage-{self._stage}-init", self._stage)
            # CTRL-04: ordered/idempotent promote + disposition ledger row.
            # Unconditional — safe via 41-02 no-op store defaults (HIGH 5).
            # Beyond-terminal promote is soft: TRAIN-07 preflight owns the
            # stage>=3 hard stop (phase40 PreflightGateTests advances 0→3
            # then raises StochasticLBFGSNotImplemented). Skip/regress still
            # hard-raises so ordered promotion is preserved.
            try:
                self._checkpoint_store.promote(k, k + 1)
            except PromotionRefused as exc:
                if "beyond terminal" not in str(getattr(exc, "reason", exc)):
                    raise
            self._checkpoint_store.record_disposition(
                k, k + 1, StageDisposition.ADVANCE, step,
            )
            # rewarm is unconditional: on a fresh factory schedule it is an
            # idempotent no-op; on stage_factory=None it is today's call.
            self._scheduled_weights.rewarm()
            self._recover_attempts = 0
            self._log_stage_exit(StageDisposition.ADVANCE, stage=k)
            return StageDisposition.ADVANCE

        if disposition is StageDisposition.RECOVER:
            empty_store = False
            step = self._disposition_step()
            try:
                restored = self._checkpoint_store.rollback()
                # CR-01 / TRAIN-06: actually restore the rolled-back payload
                # before the retry decision so a retried stage resumes from
                # the last well-formed checkpoint, not the diverged weights.
                # Both guard halves are load-bearing: forced_disposition
                # controllers have no run controller (T-40-09), and some
                # payloads (e.g. forced-path seeds) carry no run_controller key.
                if self._run_controller is not None and isinstance(restored, dict):
                    if "run_controller" in restored:
                        self._run_controller.load_state_dict(restored["run_controller"])
                    elif "model" in restored:
                        # Flat CTX-53 envelope (production save_anchor path).
                        self._run_controller.load_state_dict(restored)
            except EmptyCheckpointStore:
                empty_store = True
            self._checkpoint_store.record_disposition(
                self._stage, self._stage, StageDisposition.RECOVER, step,
            )
            self._log_stage_exit(
                StageDisposition.RECOVER, stage=self._stage, empty_store=empty_store,
            )
            if self._recover_attempts < self._recover_retries:
                self._recover_attempts += 1
                return StageDisposition.RECOVER
            self._halted = True
            self._log_stage_exit(
                StageDisposition.HALT, stage=self._stage, reason="recover-exhausted",
            )
            return StageDisposition.HALT

        if disposition is StageDisposition.HALT:
            step = self._disposition_step()
            self._halted = True
            self._checkpoint_store.record_disposition(
                self._stage, self._stage, StageDisposition.HALT, step,
            )
            self._log_stage_exit(StageDisposition.HALT, stage=self._stage)
            return StageDisposition.HALT

        raise AssertionError(
            f"CurriculumController received an unrecognized disposition: {disposition!r}"
        )

    def run(
        self,
        *,
        resume_ctx: Optional[Mapping[str, Any]] = None,
        from_resume: bool = False,
    ) -> StageDisposition:
        """Run the curriculum until a terminal HALT is reached.

        Saves the run-start ``stage-0-init`` anchor and logs the full
        provisional-threshold set ONCE, before the first stage is entered,
        then dispatches ``step()`` repeatedly: ADVANCE and RECOVER (while a
        retry budget remains) continue the loop; HALT is terminal and is
        returned. Always returns NORMALLY -- a RECOVER against an empty
        CheckpointStore is caught inside ``step()`` and never propagates.

        ``resume_ctx`` (41-05 / CTRL-05): optional ``{phase, epoch}`` threaded
        into the ENTERED stage's ``run_stage`` only (subsequent stages start
        fresh). ``from_resume=True`` skips the cold-start stage-0-init anchor
        so a mid-stage / stage-final resume does not clobber prior artifacts.
        """
        self._pending_resume_ctx = dict(resume_ctx) if resume_ctx is not None else None
        if not from_resume:
            self._save_run_start_anchor()
            self._log_run_start()
        while True:
            disposition = self.step()
            if self._stage_0_only and disposition is StageDisposition.ADVANCE:
                # The guarded step() above already stopped before any Stage-1
                # side effect, so self._stage is still 0. Terminate the
                # curriculum normally with this ADVANCE instead of looping
                # into a second Stage-0 run_stage() call (D-01).
                return disposition
            if disposition in (StageDisposition.ADVANCE, StageDisposition.RECOVER):
                continue
            return disposition
