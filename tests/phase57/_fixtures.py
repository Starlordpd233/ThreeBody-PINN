"""Phase 57 — deterministic, dataset-free, held-out-free contract fixtures.

Every helper here drives REAL production seams (``pinn.data.batches``,
``pinn.training.controllers.RunController``, ``pinn.verification.*``,
``pinn.evaluate``) against synthetic CPU/float64 populations built on top of
``tests.phase40._fixtures``'s ``StageQuery``-shaped stub source -- never the
real ``simulation_data/`` corpus and never a materialized held-out split
(threat T-57-02 / trust boundary "training-only -> held-out" in
57-01-PLAN.md's ``<threat_model>``).

Cross-phase fixture reuse (``tests.phase40._fixtures``) is an established
pattern in this suite (also used by ``tests/phase41``, ``tests/phase42``,
``tests/phase46``); Phase 57 does not duplicate the stub-source contract.
"""

from __future__ import annotations

from typing import Optional

import numpy as np

from pinn.constants import T_CHARACTERISTIC_TIME
from pinn.runtime import resolve_runtime
from pinn.training.checkpoint import TorchSaveCheckpointStore
from pinn.training.collocation_sampler import CollocationSampler
from pinn.training.config import InvariantsConfig, OptConfig, RunConfig, StageConfig, TrainingConfig
from pinn.training.grad_clip import GradClipper
from pinn.training.scheduled_weights import ScheduledWeights
from pinn.training.stage_exit import StageExitMachine
from pinn.verification.architecture_characterization_probe import (
    RATIFIED_N_BINS,
    RATIFIED_PER_BIN,
    RATIFIED_TOTAL,
)

from tests.phase40._fixtures import (  # noqa: F401 -- re-exported for tests.phase57.*
    make_stub_model,
    make_stub_source,
    make_stub_split_sources,
)

__all__ = [
    "RATIFIED_N_BINS",
    "RATIFIED_PER_BIN",
    "RATIFIED_TOTAL",
    "FULL_BATCH_SLOTS",
    "REPLAY_ONLY_SLOTS",
    "make_stub_model",
    "make_stub_source",
    "make_stub_split_sources",
    "make_full_slot_source",
    "make_replay_only_source",
    "bin_index_for_time",
    "bin_counts",
    "per_key_row_counts",
    "make_training_config",
    "build_run_controller",
    "geometric_weight_vector",
]

# The ratified §3.2 slot counts (pinn_architecture.md "Phase 56 contract:
# collocation allocation and time draw amended"; 54-RULING.md "Batch
# allocation and bin policy"). ``select_stage_records`` defaults to
# ``replay_count=240, lookahead_count=16`` -- 240 + 16 == 256.
FULL_BATCH_SLOTS = 256
REPLAY_ONLY_SLOTS = 240


def make_full_slot_source(*, id_offset: int = 0):
    """256 distinct slots: 240 stage-0 (replay) + exactly 16 stage-1 (lookahead).

    The lookahead pool size EXACTLY equals ``lookahead_count`` (16), so
    ``pinn.data.batches.select_stage_records`` draws it WITHOUT replacement
    (``len(lookahead_pool) < lookahead_count`` is False) -- every one of the
    256 selected slots is therefore a numerically distinct ``RecordKey``,
    which keeps "one row per slot per bin" checkable by key identity alone
    (no slot-vs-key aliasing to disambiguate in a synthetic fixture).
    """
    return make_stub_source(n_stage0=REPLAY_ONLY_SLOTS, n_stage1=16, id_offset=id_offset)


def make_replay_only_source(*, id_offset: int = 0):
    """240 slots, no Stage-1 pool at all (``has_stage(1)`` is False).

    This is the shape RUN-04 actually trains under: v2.3 is Stage-0-only
    (``--stage-0-only``; SCOPE-36), so no curriculum Stage-1 population
    exists yet and ``select_stage_records`` returns an EMPTY lookahead set.
    The ratified 240-replay-only 17/18-multiplicity construction
    (54-RULING.md "Batch allocation and bin policy") is therefore the real
    production path, not a theoretical edge case.
    """
    return make_stub_source(n_stage0=REPLAY_ONLY_SLOTS, n_stage1=0, id_offset=id_offset)


def bin_index_for_time(
    t, *, n_bins: int = RATIFIED_N_BINS, t_max: float = T_CHARACTERISTIC_TIME,
) -> int:
    """The ratified fixed equal-``u`` bin index for one raw collocation time.

    ``54-RULING.md`` "Batch allocation and bin policy": bins are
    ``[b/n_bins, (b+1)/n_bins)`` of ``t_max`` for ``b = 0 .. n_bins - 2``, and
    ``[(n_bins - 1)/n_bins, 1]`` CLOSED on both edges for the last bin -- a
    time exactly on an interior boundary belongs to the bin that boundary
    OPENS, and the domain endpoint belongs to the final bin. This is an
    independent re-derivation (by content, not by import) of the same
    convention ``stratified_collocation_times`` encodes, so a Phase-57 test
    can bucket ANY returned time -- including one from a not-yet-conformant
    production draw -- without depending on a bin-index field that does not
    exist on ``PhysicsCollocationPoints`` today.
    """
    u = float(t) / float(t_max)
    if u < -1e-12 or u > 1.0 + 1e-12:
        raise ValueError(
            f"time {t!r} maps to u={u!r}, outside the ratified [0, 1] domain"
        )
    idx = int(np.floor(max(u, 0.0) * n_bins))
    if idx >= n_bins:
        idx = n_bins - 1
    return idx


def bin_counts(
    times, *, n_bins: int = RATIFIED_N_BINS, t_max: float = T_CHARACTERISTIC_TIME,
) -> list:
    """Per-bin membership counts for an iterable of raw collocation times."""
    counts = [0] * n_bins
    for t in times:
        counts[bin_index_for_time(t, n_bins=n_bins, t_max=t_max)] += 1
    return counts


def per_key_row_counts(record_keys) -> dict:
    """Map each distinct key in ``record_keys`` to its occurrence count."""
    counts: dict = {}
    for key in record_keys:
        counts[key] = counts.get(key, 0) + 1
    return counts


def make_training_config(
    *,
    max_epochs: int = 2,
    n_adam: int = 2,
    validation_every: int = 10_000,
    lbfgs_chunk_size: int = 4,
    lbfgs_max_iter: int = 2,
    front_advance_window_n: Optional[int] = None,
    seed: int = 0,
    **stage_overrides,
) -> TrainingConfig:
    """A cheap, REAL ``TrainingConfig``.

    Mirrors ``tests/phase40/test_controllers.py``'s ``_make_config`` helper
    exactly (same ``StageConfig``/``OptConfig`` field set) plus the Phase-57
    ``run.invariants.front_advance_window_n`` seam (checkpoint ③, D-03).
    """
    stage_kwargs = dict(
        max_epochs=max_epochs,
        n_adam=n_adam,
        stagnation_window=10_000,
        percentile_10_relaxation=0.1,
        beta=0.9,
        patience=5,
        eps_plateau=1e-5,
        eps_phys=1e-4,
        eps_energy=1e-4,
    )
    stage_kwargs.update(stage_overrides)
    stage = StageConfig(**stage_kwargs)
    opt = OptConfig(
        validation_every=validation_every,
        lbfgs_chunk_size=lbfgs_chunk_size,
        lbfgs_max_iter=lbfgs_max_iter,
    )
    run = RunConfig(
        seed=seed,
        invariants=InvariantsConfig(front_advance_window_n=front_advance_window_n),
    )
    return TrainingConfig(stage=stage, opt=opt, run=run)


def build_run_controller(
    train_source,
    validation_source,
    *,
    tmp_dir,
    s_h: float = 1.0,
    config: Optional[TrainingConfig] = None,
    seed: int = 0,
    replay_count: Optional[int] = None,
    n_collocation_sampler_points: int = 2,
):
    """A REAL ``pinn.training.controllers.RunController`` over stub sources.

    Mirrors ``tests/phase40/test_controllers.py``'s real-controller
    construction pattern (identical collaborator classes and ``s_h``/``rng``
    keyword wiring) so Phase-57 tests drive the SAME production seam rather
    than a parallel harness (57-RESEARCH.md "Don't Hand-Roll").
    """
    from pinn.training.controllers import RunController

    if config is None:
        config = make_training_config(seed=seed)
    runtime = resolve_runtime("float64", "cpu")
    model = make_stub_model(dtype=runtime.dtype, device=runtime.torch_device)
    scheduled_weights = ScheduledWeights(1)
    grad_clipper = GradClipper()
    collocation_sampler = CollocationSampler(
        n_collocation_sampler_points, np.random.default_rng(seed + 1000),
    )
    stage_exit_machine = StageExitMachine(config)
    checkpoint_store = TorchSaveCheckpointStore(tmp_dir)
    return RunController(
        model, train_source, validation_source, config,
        scheduled_weights, grad_clipper, collocation_sampler,
        stage_exit_machine, checkpoint_store, runtime,
        rng=np.random.default_rng(seed), s_h=s_h, replay_count=replay_count,
    )


def geometric_weight_vector(*, first_ratio: float = 0.5, n_bins: int = RATIFIED_N_BINS):
    """A synthetic monotone-non-increasing 16-entry causal weight vector.

    ``weights[0] == 1.0`` always (the exclusive prefix into bin 0 is empty --
    identical to the real ``causal_physics_loss`` construction); the tail
    decays geometrically by ``first_ratio`` per bin, giving a non-anchor
    spread ``max(weights[1:]) / min(weights[1:])`` of
    ``first_ratio ** -(n_bins - 2)`` -- comfortably >= 2:1 for any
    ``first_ratio < 1.0`` and ``n_bins >= 3``, satisfying the 57-RULING.md
    condition-(ii) baseline non-degeneracy precondition without needing a
    real network forward pass.
    """
    return tuple(float(first_ratio) ** n for n in range(n_bins))
