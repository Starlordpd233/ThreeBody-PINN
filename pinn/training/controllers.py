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
copy). ``eps_h`` is a provisional ``|h0| * 1e-4`` scale (mirrors the
documented ``eps_h = 1e-4 * S_H`` form; no ``S_H`` pipeline exists yet upstream
of this plan) with a tiny additive floor to avoid a zero denominator.
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
from dataclasses import dataclass, replace
from typing import Any, Callable, Optional

import numpy as np
import torch

import pinn.loss_catalog as loss_catalog
from pinn.constants import T_CHARACTERISTIC_TIME
from pinn.data.batches import build_stage_batch
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
from pinn.training.checkpoint import EmptyCheckpointStore
from pinn.training.slbfgs_preflight import check_stage_preflight
from pinn.training.stage_exit import StageDisposition

__all__ = [
    "PlateauDetector",
    "HandoffEvent",
    "RunController",
    "accumulate_chunked_data_term",
    "CurriculumController",
    "ForcedDispositionOnLiveRun",
    "StageFactoryModelMismatch",
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
        rng: Optional[np.random.Generator] = None,
    ) -> None:
        if validation_source is None:
            raise ValueError(
                "RunController requires a validation_source: ADVANCE criterion 2 "
                "is defined on a held-out set (ctl_instruction.md CURR-03), so a "
                "RunController built without one could not evaluate the gate"
            )
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

        self.last_handoff_event: Optional[HandoffEvent] = None

    # ------------------------------------------------------------------
    # Public checkpoint surface (CTX-44 -- composes model + schedule + clipper).
    # ------------------------------------------------------------------
    def state_dict(self) -> dict[str, Any]:
        return {
            "model": self._model.state_dict(),
            "scheduled_weights": self._scheduled_weights.state_dict(),
            "clipper": self._grad_clipper.state_dict(),
        }

    def load_state_dict(self, state: dict[str, Any]) -> None:
        self._model.load_state_dict(state["model"])
        self._scheduled_weights.load_state_dict(state["scheduled_weights"])
        self._grad_clipper.load_state_dict(state["clipper"])

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
        # WR-02: eps_h scale is the config-overridable StageConfig.energy_floor_factor
        # (CTX-38 provisional default 1e-4 = ctl_instruction.md CURR-03 ε_H=1e-4·S_H).
        # The +1e-12 additive floor is a numeric-safety zero-denominator guard, not
        # the configurable scale.
        eps_h = abs(h0) * float(self._config.stage.energy_floor_factor) + 1e-12

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
        rbar = (residual ** 2).mean(dim=(-2, -1))
        times_tensor = torch.as_tensor(
            anchor_ctx.collocation_times, dtype=self._dtype, device=self._device,
        )
        phys_term = causal_physics_loss(
            rbar, times=times_tensor, dtype=self._dtype, device=self._device,
        )

        energy_term = soft_energy_loss(
            positions, velocities, anchor_ctx.h0, anchor_ctx.eps_h,
            masses=anchor_ctx.masses, dtype=self._dtype, device=self._device,
        )
        angmom_term = angular_momentum_loss(
            positions, velocities, anchor_ctx.l0,
            masses=anchor_ctx.masses, dtype=self._dtype, device=self._device,
        )
        return {"ic": ic_term, "phys": phys_term, "energy": energy_term, "angmom": angmom_term}

    def _weighted_non_data_terms(self, anchor_ctx: _AnchorContext, weights) -> torch.Tensor:
        terms = self._non_data_terms(anchor_ctx)
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
    # Validation pass (TRAIN-06 wiring -- ADVANCE criteria 2/3/4 producer).
    # ------------------------------------------------------------------
    def _run_validation(self, k: int, weights) -> LossTerms:
        self._model.eval()
        try:
            batch = build_stage_batch(
                self._validation_source, stage=k, rng=self._rng,
                dtype=self._dtype, device=self._device, collocation_count=1,
            )
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
    # Phase 2a: Adam.
    # ------------------------------------------------------------------
    def _run_adam_phase(self, k: int, n_adam_k: int, optimizer, scheduler, plateau: PlateauDetector,
                        train_loss_history: list, val_loss_history: list, state: dict) -> tuple[str, int]:
        validation_every = int(self._config.opt.validation_every)
        handoff_trigger = "budget-exhausted"
        adam_epochs_used = 0
        for epoch in range(n_adam_k):
            adam_epochs_used = epoch + 1
            batch = build_stage_batch(
                self._train_source, stage=k, rng=self._rng,
                dtype=self._dtype, device=self._device, collocation_count=1,
            )
            anchor_ctx = self._build_anchor_context(self._train_source, batch, None)
            weights = self._scheduled_weights.current(epoch)

            optimizer.zero_grad(set_to_none=True)
            loss_terms = self._compose_loss_terms(batch, anchor_ctx, weights)
            if not self._loss_finite(loss_terms.total):
                state["disposition"] = StageDisposition.RECOVER
                return handoff_trigger, adam_epochs_used
            loss_terms.total.backward()

            outcome = self._grad_clipper.clip(self._model.parameters(), stage=k)
            if outcome.non_finite:
                state["disposition"] = StageDisposition.RECOVER
                return handoff_trigger, adam_epochs_used

            optimizer.step()
            scheduler.step()

            state["epoch_count"] += 1
            train_loss_history.append(float(loss_terms.total.detach()))
            fires = plateau.update(float(loss_terms.phys.detach()))

            if state["epoch_count"] % validation_every == 0:
                val_terms = self._run_validation(k, weights)
                val_loss_history.append(float(val_terms.total.detach()))
                state["val_phys"] = float(val_terms.phys.detach())
                state["val_energy"] = float(val_terms.energy.detach())

            if fires:
                handoff_trigger = "plateau"
                break

        return handoff_trigger, adam_epochs_used

    # ------------------------------------------------------------------
    # Phase 2b: L-BFGS.
    # ------------------------------------------------------------------
    def _make_lbfgs_closure(self, optimizer, fixed_batch, anchor_ctx, weights, chunk_size, closure_state):
        def closure():
            optimizer.zero_grad(set_to_none=True)
            weighted_data = accumulate_chunked_data_term(
                self._model, fixed_batch.data_points,
                weight=weights.lambda_data, chunk_size=chunk_size,
                dtype=self._dtype, device=self._device,
            )
            other_total = self._weighted_non_data_terms(anchor_ctx, weights)
            other_total.backward()

            total = weighted_data + other_total.detach()
            closure_state["last_loss"] = float(total.detach())
            if not self._loss_finite(total):
                closure_state["non_finite"] = True
                return total
            if not self._grads_finite():
                closure_state["non_finite"] = True
            return total

        return closure

    def _run_lbfgs_phase(self, k: int, remaining_budget: int, epoch_count_start: int,
                         train_loss_history: list, val_loss_history: list, state: dict):
        cfg = self._config
        self._scheduled_weights.freeze()
        weights_frozen = self._scheduled_weights.current(0)

        fixed_batch = build_stage_batch(
            self._train_source, stage=k, rng=self._rng,
            dtype=self._dtype, device=self._device, collocation_count=1,
        )
        fixed_collocation_times = self._collocation_sampler.uniform()
        anchor_ctx = self._build_anchor_context(self._train_source, fixed_batch, fixed_collocation_times)

        optimizer = torch.optim.LBFGS(
            self._model.parameters(),
            history_size=cfg.opt.lbfgs_history_size,
            max_iter=cfg.opt.lbfgs_max_iter,
            line_search_fn=cfg.opt.lbfgs_line_search,
        )
        chunk_size = int(cfg.opt.lbfgs_chunk_size)
        validation_every = int(cfg.opt.validation_every)

        epoch_count = epoch_count_start
        for _lbfgs_epoch in range(remaining_budget):
            closure_state: dict[str, Any] = {"non_finite": False, "last_loss": None}
            closure = self._make_lbfgs_closure(
                optimizer, fixed_batch, anchor_ctx, weights_frozen, chunk_size, closure_state
            )
            optimizer.step(closure)
            epoch_count += 1

            if closure_state["non_finite"]:
                self._scheduled_weights.rewarm()
                return StageDisposition.RECOVER

            train_loss_history.append(closure_state["last_loss"])

            if epoch_count % validation_every == 0:
                val_terms = self._run_validation(k, weights_frozen)
                val_loss_history.append(float(val_terms.total.detach()))
                state["val_phys"] = float(val_terms.phys.detach())
                state["val_energy"] = float(val_terms.energy.detach())

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
    def run_stage(self, k: int) -> StageDisposition:
        cfg = self._config
        n_adam_k = int(cfg.stage.n_adam)
        max_epochs = int(cfg.stage.max_epochs)

        optimizer = torch.optim.Adam(
            self._model.parameters(),
            lr=cfg.opt.lr_for_stage(k),
            betas=cfg.opt.adam_betas,
            eps=cfg.opt.adam_eps,
        )
        scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=n_adam_k)

        self._grad_clipper.clear()
        self._scheduled_weights.rewarm()
        plateau = PlateauDetector()

        train_loss_history: list[float] = []
        val_loss_history: list[float] = []
        state: dict[str, Any] = {
            "epoch_count": 0,
            "val_phys": math.inf,
            "val_energy": math.inf,
            "disposition": None,
        }

        handoff_trigger, adam_epochs_used = self._run_adam_phase(
            k, n_adam_k, optimizer, scheduler, plateau,
            train_loss_history, val_loss_history, state,
        )
        self.last_handoff_event = HandoffEvent(
            trigger=handoff_trigger, adam_epochs_used=adam_epochs_used,
        )
        if state["disposition"] is not None:
            return state["disposition"]

        remaining_budget = max(max_epochs - adam_epochs_used, 0)
        if remaining_budget == 0:
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
        return self._run_lbfgs_phase(
            k, remaining_budget, state["epoch_count"],
            train_loss_history, val_loss_history, state,
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
        recover_retries: int = 0,
        initial_stage: int = 0,
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
        self._recover_retries = int(recover_retries)
        self._recover_attempts = 0
        self._stage = int(initial_stage)
        self._halted = False

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
        disposition = self._run_controller.run_stage(stage)
        self._log_handoff_if_any()
        return disposition

    # ------------------------------------------------------------------
    # Checkpoint payload / run-start anchor (cycle-2 H3).
    # ------------------------------------------------------------------
    def _checkpoint_payload(self, tag: str, stage: int) -> dict[str, Any]:
        payload: dict[str, Any] = {"tag": tag, "stage": stage}
        if self._run_controller is not None:
            payload["run_controller"] = self._run_controller.state_dict()
        return payload

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
        self._checkpoint_store.save(self._checkpoint_payload("stage-0-init", self._stage))

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
        disposition = self._get_disposition(self._stage)

        if disposition is StageDisposition.ADVANCE:
            k = self._stage
            # stage-{k}-final carries the EXITING stage's state (OLD controller).
            self._checkpoint_store.save(self._checkpoint_payload(f"stage-{k}-final", k))
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
                self._run_controller = new_controller
                self._scheduled_weights = new_controller.scheduled_weights
            self._checkpoint_store.save(
                self._checkpoint_payload(f"stage-{self._stage}-init", self._stage)
            )
            # rewarm is unconditional: on a fresh factory schedule it is an
            # idempotent no-op; on stage_factory=None it is today's call.
            self._scheduled_weights.rewarm()
            self._recover_attempts = 0
            self._log_stage_exit(StageDisposition.ADVANCE, stage=k)
            return StageDisposition.ADVANCE

        if disposition is StageDisposition.RECOVER:
            empty_store = False
            try:
                restored = self._checkpoint_store.rollback()
                # CR-01 / TRAIN-06: actually restore the rolled-back payload
                # before the retry decision so a retried stage resumes from
                # the last well-formed checkpoint, not the diverged weights.
                # Both guard halves are load-bearing: forced_disposition
                # controllers have no run controller (T-40-09), and some
                # payloads (e.g. forced-path seeds) carry no run_controller key.
                if (
                    self._run_controller is not None
                    and isinstance(restored, dict)
                    and "run_controller" in restored
                ):
                    self._run_controller.load_state_dict(restored["run_controller"])
            except EmptyCheckpointStore:
                empty_store = True
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
            self._halted = True
            self._log_stage_exit(StageDisposition.HALT, stage=self._stage)
            return StageDisposition.HALT

        raise AssertionError(
            f"CurriculumController received an unrecognized disposition: {disposition!r}"
        )

    def run(self) -> StageDisposition:
        """Run the curriculum until a terminal HALT is reached.

        Saves the run-start ``stage-0-init`` anchor and logs the full
        provisional-threshold set ONCE, before the first stage is entered,
        then dispatches ``step()`` repeatedly: ADVANCE and RECOVER (while a
        retry budget remains) continue the loop; HALT is terminal and is
        returned. Always returns NORMALLY -- a RECOVER against an empty
        CheckpointStore is caught inside ``step()`` and never propagates.
        """
        self._save_run_start_anchor()
        self._log_run_start()
        while True:
            disposition = self.step()
            if disposition in (StageDisposition.ADVANCE, StageDisposition.RECOVER):
                continue
            return disposition
