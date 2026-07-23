"""Phase 41 fixtures — extend phase40 stubs with clock / step / Stage-0 loop.

Re-exports the phase40 builders (``make_stub_source``, ``make_stub_split_sources``,
``make_stub_model``) rather than duplicating their bodies, and adds:

- ``StubClock`` — controllable monotonic wall-clock (elapsed seconds).
- ``StubStepCounter`` — monotonic integer step counter.
- ``make_synthetic_stage0_loop(...)`` — wires stubs into a minimal runnable
  Stage-0 ``RunController`` / ``CurriculumController`` pair for end-to-end
  plans (41-04/41-05) without a real dataset.
"""

from __future__ import annotations

from typing import Any, Optional

# Re-export phase40 fixtures (do not duplicate bodies).
from tests.phase40._fixtures import (  # noqa: F401
    make_stub_model,
    make_stub_source,
    make_stub_split_sources,
)

__all__ = [
    "StubClock",
    "StubStepCounter",
    "make_stub_model",
    "make_stub_source",
    "make_stub_split_sources",
    "make_synthetic_stage0_loop",
    "write_duration_gate_calibration",
]


def write_duration_gate_calibration(
    runs_root: Any,
    *,
    precision: str = "float64",
    device: str = "cpu",
    full_stage0_steps: int = 2,
) -> Any:
    """Authorize a test launch through the real persisted duration gate.

    The deliberately small measured seconds-per-step keeps these dataset-free
    fixture runs below the production 1800-second boundary while retaining the
    production calibration fingerprint and validation path.
    """
    from pinn.training.timing import write_calibration

    return write_calibration(
        s_per_step=1.0,
        full_stage0_steps=full_stage0_steps,
        precision=precision,
        device=device,
        runs_root=runs_root,
    )


class StubClock:
    """Controllable monotonic time source returning caller-set elapsed seconds.

    Downstream checkpoint-cadence tests (41-02/41-04) inject this instead of
    ``time.monotonic`` so wall-clock ceilings fire without sleeping.
    """

    def __init__(self, start: float = 0.0) -> None:
        self._elapsed = float(start)

    def now(self) -> float:
        return self._elapsed

    def advance(self, seconds: float) -> float:
        self._elapsed += float(seconds)
        return self._elapsed

    def set(self, seconds: float) -> float:
        self._elapsed = float(seconds)
        return self._elapsed


class StubStepCounter:
    """Monotonic integer step counter for cadence tests."""

    def __init__(self, start: int = 0) -> None:
        if not isinstance(start, int) or isinstance(start, bool) or start < 0:
            raise ValueError(f"start must be a non-negative int (got {start!r})")
        self._step = int(start)

    @property
    def step(self) -> int:
        return self._step

    def tick(self, n: int = 1) -> int:
        if not isinstance(n, int) or isinstance(n, bool) or n < 1:
            raise ValueError(f"n must be a positive int (got {n!r})")
        self._step += n
        return self._step

    def set(self, step: int) -> int:
        if not isinstance(step, int) or isinstance(step, bool) or step < 0:
            raise ValueError(f"step must be a non-negative int (got {step!r})")
        self._step = int(step)
        return self._step


def make_synthetic_stage0_loop(
    *,
    n_train: int = 8,
    n_validation: int = 4,
    max_epochs: int = 2,
    n_adam: int = 1,
    seed: int = 0,
    checkpoint_root: Optional[Any] = None,
):
    """Wire phase40 stubs into a minimal Stage-0 controller pair.

    Returns a dict with keys ``model``, ``train_source``, ``validation_source``,
    ``config``, ``run_controller``, ``curriculum``, ``checkpoint_store``,
    ``runtime``, ``clock``, ``steps`` so 41-04/41-05 can drive a synthetic
    Stage-0 loop without a real dataset. Heavy imports are deferred so importing
    this module stays cheap.
    """
    import tempfile
    from pathlib import Path

    import numpy as np
    import torch

    from pinn.runtime import resolve_runtime
    from pinn.training.checkpoint import TorchSaveCheckpointStore
    from pinn.training.collocation_sampler import CollocationSampler
    from pinn.training.config import (
        LossConfig,
        OptConfig,
        RunConfig,
        StageConfig,
        TrainingConfig,
    )
    from pinn.training.controllers import CurriculumController, RunController
    from pinn.training.grad_clip import GradClipper
    from pinn.training.scheduled_weights import ScheduledWeights
    from pinn.training.stage_exit import StageExitMachine

    train_source, validation_source = make_stub_split_sources(
        n_train=n_train, n_validation=n_validation
    )
    # Cheap CPU/fp64 for unit tests (mirrors phase40 make_stub_model defaults).
    runtime = resolve_runtime("float64", "cpu")
    model = make_stub_model(dtype=runtime.dtype, device=runtime.torch_device)

    stage = StageConfig(
        max_epochs=max_epochs,
        n_adam=n_adam,
        stagnation_window=1,
        percentile_10_relaxation=0.1,
    )
    # Prefer float64/cpu for the synthetic loop so it runs without MPS.
    run = RunConfig(seed=seed)
    # Phase-41 RunConfig may already carry precision/device; when present we
    # leave defaults alone here so construction stays valid under both the
    # pre-Task-2 and post-Task-2 surfaces. resolve_runtime above is the
    # authority for the actual tensors.
    config = TrainingConfig(
        stage=stage,
        run=run,
        opt=OptConfig(validation_every=1),
        loss=LossConfig(),
    )

    if checkpoint_root is None:
        checkpoint_root = Path(tempfile.mkdtemp(prefix="phase41-ckpt-"))
    else:
        checkpoint_root = Path(checkpoint_root)
        checkpoint_root.mkdir(parents=True, exist_ok=True)
    checkpoint_store = TorchSaveCheckpointStore(checkpoint_root)

    scheduled_weights = ScheduledWeights(
        int(config.stage.n_adam),  # type: ignore[arg-type]
        lambda_e_max=float(config.loss.lambda_e_max),
    )
    grad_clipper = GradClipper()
    collocation_sampler = CollocationSampler(
        collocation_count=16,
        rng=np.random.default_rng(seed),
    )
    stage_exit_machine = StageExitMachine(config)

    run_controller = RunController(
        model=model,
        train_source=train_source,
        validation_source=validation_source,
        config=config,
        scheduled_weights=scheduled_weights,
        grad_clipper=grad_clipper,
        collocation_sampler=collocation_sampler,
        stage_exit_machine=stage_exit_machine,
        checkpoint_store=checkpoint_store,
        runtime=runtime,
        rng=np.random.default_rng(seed),
    )
    curriculum = CurriculumController(
        config=config,
        checkpoint_store=checkpoint_store,
        scheduled_weights=scheduled_weights,
        run_controller=run_controller,
    )
    return {
        "model": model,
        "train_source": train_source,
        "validation_source": validation_source,
        "config": config,
        "run_controller": run_controller,
        "curriculum": curriculum,
        "checkpoint_store": checkpoint_store,
        "runtime": runtime,
        "clock": StubClock(),
        "steps": StubStepCounter(),
        "checkpoint_root": checkpoint_root,
        "torch": torch,
    }
