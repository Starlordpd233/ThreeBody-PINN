"""Dataset-free RunController fixture for Phase-50 validation-pool tests."""

from __future__ import annotations

import numpy as np
import torch

from pinn.data.types import RecordKey
from pinn.runtime import resolve_runtime
from pinn.train import _synthetic_split_sources
from pinn.training.checkpoint import TorchSaveCheckpointStore
from pinn.training.collocation_sampler import CollocationSampler
from pinn.training.config import StageConfig, TrainingConfig
from pinn.training.controllers import RunController
from pinn.training.grad_clip import GradClipper
from pinn.training.scheduled_weights import ScheduledWeights
from pinn.training.stage_exit import StageExitMachine


class _QuadraticProbeModel(torch.nn.Module):
    """Small twice-differentiable model matching the Phase-49 producer fixture."""

    def forward(self, tau_ic13, masses):
        tau = tau_ic13[:, :1]
        return (
            tau_ic13[:, 1:10] * 0.05
            + masses.repeat_interleave(3, dim=1) * 0.01
            + tau.square()
        )


class _StageAugmentedSource:
    """Wrap a ``_synthetic_split_sources`` stub and expose a nonempty stage-1 pool.

    ``_synthetic_split_sources`` answers ``has_stage`` true only for stage 0.
    The no-lookahead assertion would pass vacuously without an adjacent-stage
    pool on the validation source.
    """

    def __init__(self, base, stage1_ids):
        self._base = base
        self._s1 = tuple(RecordKey("hierarchical", "base", int(i)) for i in stage1_ids)

    def has_stage(self, k):
        if k == 1:
            return bool(self._s1)
        return self._base.has_stage(k)

    def records_at(self, k):
        if k == 1:
            return self._s1
        return self._base.records_at(k)

    def records_at_or_below(self, k):
        base = list(self._base.records_at_or_below(k))
        if k >= 1:
            base.extend(self._s1)
        return tuple(base)

    def __getattr__(self, name):
        return getattr(self._base, name)


def make_phase50_controller(
    run_dir,
    *,
    n_train: int = 240,
    n_validation: int = 50,
    n_train_stage1: int = 16,
    n_validation_stage1: int = 8,
    replay_count=None,
    seed: int = 0,
) -> RunController:
    """Build a dataset-free ``RunController`` for Phase-50 validation tests.

    Construction follows ``tests/phase49/_producer_fixture.py``. Train and
    validation sources come from ``_synthetic_split_sources`` and are then
    wrapped so ``has_stage(1)`` is true with a nonempty ``records_at(1)``.
    """
    runtime = resolve_runtime("float64", "cpu")
    config = TrainingConfig(
        stage=StageConfig(
            max_epochs=1000,
            n_adam=1000,
            stagnation_window=10,
            percentile_10_relaxation=0.1,
            beta=0.9,
            patience=5,
            eps_plateau=1e-5,
            eps_phys=1e-4,
            eps_energy=1e-4,
            energy_floor_factor=1e-4,
        )
    )
    train_base, validation_base = _synthetic_split_sources(
        n_train=n_train, n_validation=n_validation
    )
    train_source = _StageAugmentedSource(
        train_base, tuple(range(40_000, 40_000 + n_train_stage1))
    )
    validation_source = _StageAugmentedSource(
        validation_base, tuple(range(50_000, 50_000 + n_validation_stage1))
    )
    rng = np.random.default_rng(seed)
    return RunController(
        model=_QuadraticProbeModel().to(
            dtype=runtime.dtype, device=runtime.torch_device
        ),
        train_source=train_source,
        validation_source=validation_source,
        config=config,
        scheduled_weights=ScheduledWeights(
            1000, lambda_e_max=0.0, lambda_l_max=0.0
        ),
        grad_clipper=GradClipper(),
        collocation_sampler=CollocationSampler(2, np.random.default_rng(seed)),
        stage_exit_machine=StageExitMachine(config),
        checkpoint_store=TorchSaveCheckpointStore(run_dir),
        runtime=runtime,
        s_h=5.0,
        rng=rng,
        replay_count=replay_count,
    )


class _MinimalPoolSource:
    """Minimal StageQuery-shaped source for selector-level rejection tests."""

    def __init__(self, keys, *, blacklisted=(), gold_numeric_stage_count=0):
        self._keys = tuple(keys)
        self._black = frozenset(blacklisted)
        self.gold_numeric_stage_count = gold_numeric_stage_count

    @property
    def blacklisted_physical_keys(self):
        return self._black

    def records_at_or_below(self, stage):
        return self._keys

    def is_blacklisted(self, physical_key):
        return physical_key in self._black


def make_minimal_pool_source(keys, *, blacklisted=(), gold_numeric_stage_count=0):
    return _MinimalPoolSource(
        keys,
        blacklisted=blacklisted,
        gold_numeric_stage_count=gold_numeric_stage_count,
    )
