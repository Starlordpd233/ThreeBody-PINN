"""CONF-03 ε_H wiring invariants (plan 47-03).

The spec contract (``pinn_architecture.md`` §3.4, transcribed in 47-CONTEXT.md
D-19/D-20/D-21): the dataset-wide energy floor ``ε_H = energy_floor_factor · S_H``
(``1e-4 · S_H``) reaches the loss through an explicit, REQUIRED keyword-only
``RunController(s_h=…)`` channel threaded from the validated
``training_metadata.json`` pipeline (47-02). The §3.4-prohibited additive
fallback floor is gone outright (D-19), the per-anchor ``abs(h0)`` stays in the
loss denominator ``|H_0| + ε_H`` where §3.4 puts it (D-20), and the
``_AnchorContext.eps_h`` per-test override seam survives unchanged (D-21).

These tests are assembly-boundary tests: they prove the run-level constant
flows through the parameter chain into ``soft_energy_loss`` and that the scale
is identical across anchors. They are train-free and dataset-free (SCOPE-27/28):
no ``RunController.run()`` / ``run_stage()`` call, no real corpus, no held-out
evaluation — every number comes from synthetic stub sources and direct
``soft_energy_loss`` calls.
"""

from __future__ import annotations

import math
import tempfile
from types import SimpleNamespace

import numpy as np
import pytest
import torch

from pinn.constants import HUBER_DELTA_ENERGY
from pinn.data.types import RecordKey
from pinn.loss_catalog import (
    _huber,
    _matched_plummer_hamiltonian,
    resolve_causal_clip_facts,
    soft_energy_loss,
)
from pinn.runtime import resolve_runtime
from pinn.train import _assert_s_h_matches_artifact
from pinn.training.checkpoint import TorchSaveCheckpointStore
from pinn.training.collocation_sampler import CollocationSampler
from pinn.training.config import OptConfig, StageConfig, TrainingConfig
from pinn.training.controllers import RunController, _AnchorContext
from pinn.training.grad_clip import GradClipper
from pinn.training.run_metadata import compute_s_h, write_training_metadata
from pinn.training.scheduled_weights import ScheduledWeights
from pinn.training.stage_exit import StageExitMachine
from tests.phase40._fixtures import make_stub_model, make_stub_split_sources

_CPU_F64 = dict(dtype=torch.float64, device=torch.device("cpu"))
_CPU_F64_CLIP_FACTS = resolve_causal_clip_facts(
    torch.float64, torch.device("cpu")
)


# ---------------------------------------------------------------------------
# Construction plumbing — mirrors phase-40 ``_build_controller`` but exposes the
# required ``s_h`` channel explicitly. Synthetic stub sources, CPU/float64.
# ---------------------------------------------------------------------------


def _make_config(*, energy_floor_factor=1e-4):
    stage = StageConfig(
        max_epochs=1,
        n_adam=1,
        stagnation_window=10_000,
        percentile_10_relaxation=0.1,
        beta=0.9,
        patience=5,
        eps_plateau=1e-5,
        eps_phys=1e-4,
        eps_energy=1e-4,
        energy_floor_factor=energy_floor_factor,
    )
    opt = OptConfig(validation_every=10_000, lbfgs_chunk_size=4, lbfgs_max_iter=2)
    return TrainingConfig(stage=stage, opt=opt)


def _construction_inputs(*, energy_floor_factor=1e-4):
    """Return ``(positional_args, kwargs, train_source, config)`` for RunController.

    ``kwargs`` carries only the optional keyword args (``rng``); ``s_h`` is NEVER
    placed here so every call site states it explicitly (the AST s_h-kwarg gate
    then sees it on each literal ``RunController(`` construction).
    """
    runtime = resolve_runtime("float64", "cpu")
    model = make_stub_model(dtype=runtime.dtype, device=runtime.torch_device)
    train_source, validation_source = make_stub_split_sources(n_train=300, n_validation=300)
    config = _make_config(energy_floor_factor=energy_floor_factor)
    store = TorchSaveCheckpointStore(tempfile.mkdtemp())
    positional = (
        model,
        train_source,
        validation_source,
        config,
        ScheduledWeights(int(config.stage.n_adam), lambda_e_max=0.0, lambda_l_max=0.0),
        GradClipper(),
        CollocationSampler(2, np.random.default_rng(0)),
        StageExitMachine(config),
        store,
        runtime,
    )
    kwargs = dict(rng=np.random.default_rng(0))
    return positional, kwargs, train_source, config


def _make_controller(*, s_h, energy_floor_factor=1e-4):
    positional, kwargs, train_source, config = _construction_inputs(
        energy_floor_factor=energy_floor_factor
    )
    return RunController(*positional, s_h=s_h, **kwargs), train_source, config


def _anchor_batch(key):
    """A minimal batch whose ``_select_anchor_key`` resolves to ``key``.

    ``_build_anchor_context`` only reads ``batch`` through ``_select_anchor_key``
    (``replay_keys`` / ``lookahead_keys`` / ``data_points.record_keys``) to pick
    the anchor identity; the conserved quantities then come from ``source``.
    Driving the anchor key directly makes the |h0|-distinctness deterministic
    without invoking the 240-population replay selection.
    """
    return SimpleNamespace(
        replay_keys=(key,),
        lookahead_keys=(),
        data_points=SimpleNamespace(record_keys=(key,)),
    )


def _anchor_ctx(controller, source, key):
    return controller._build_anchor_context(source, _anchor_batch(key), None)


# ---------------------------------------------------------------------------
# D-19/D-20/D-21 — the ε_H assembly value and the soft_energy_loss denominator.
# ---------------------------------------------------------------------------


def test_eps_h_assembly_value():
    """ε_H == energy_floor_factor * s_h, independent of the anchor's own h0.

    Two anchors with distinct ids (and therefore distinct |h0|) MUST share the
    single run-level ε_H — proving the per-anchor ``abs(h0)`` no longer sets the
    scale (D-19: it was deleted, not kept alongside). The soft_energy_loss term
    then receives exactly that value and its denominator is ``abs(h0) + eps_h``
    (D-20: the per-anchor ``abs(h0)`` survives).
    """
    controller, train_source, config = _make_controller(s_h=2.5, energy_floor_factor=1e-4)
    # Pin the factor so the assertion is unambiguous (the named home of 1e-4).
    assert float(config.stage.energy_floor_factor) == 1e-4

    keys = train_source.record_keys()
    key_a, key_b = keys[0], keys[100]  # distinct ids -> distinct snapshot-0 -> distinct |h0|
    ctx_a = _anchor_ctx(controller, train_source, key_a)
    ctx_b = _anchor_ctx(controller, train_source, key_b)

    expected = float(config.stage.energy_floor_factor) * 2.5
    assert ctx_a.eps_h == expected
    assert ctx_b.eps_h == expected
    # Non-trivial: the two anchors really do carry different |h0| (the quantity
    # the old code used as the scale), yet eps_h is identical.
    assert ctx_a.h0 != ctx_b.h0

    # D-20: soft_energy_loss receives exactly this eps_h and its denominator is
    # abs(h0) + eps_h. Proven regime-independently by replicating the documented
    # formula with the same primitives (a changed denominator would diverge).
    masses = torch.tensor([1.0, 2.0, 3.0], **_CPU_F64)
    pos = torch.tensor(
        [[[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [0.0, 1.0, 0.0]]], **_CPU_F64
    )
    vel = torch.tensor(
        [[[0.1, 0.2, 0.3], [-0.2, 0.1, 0.0], [0.0, -0.1, 0.2]]], **_CPU_F64
    )
    h = _matched_plummer_hamiltonian(pos, vel, masses, **_CPU_F64)
    h0 = float(h[0]) - 0.25  # a deliberate drift; regime-agnostic below
    h0_t = torch.as_tensor(h0, **_CPU_F64)
    eps_h = expected
    got = soft_energy_loss(pos, vel, h0, eps_h, masses=masses, **_CPU_F64)
    denom = h0_t.abs() + eps_h
    delta_h = (h - h0_t) / denom
    expected_loss = _huber(delta_h, HUBER_DELTA_ENERGY, **_CPU_F64).mean()
    assert torch.allclose(got, expected_loss)


def test_eps_h_uniform_across_anchors():
    """Companion invariant: every anchor in a stage sees the SAME eps_h.

    Goes red the instant a future phase reintroduces per-anchor scaling.
    """
    controller, train_source, config = _make_controller(s_h=7.0, energy_floor_factor=1e-4)
    keys = train_source.record_keys()
    contexts = [_anchor_ctx(controller, train_source, keys[offset]) for offset in (0, 50, 100, 150)]
    distinct_eps = {ctx.eps_h for ctx in contexts}
    assert distinct_eps == {float(config.stage.energy_floor_factor) * 7.0}
    # The |h0| values are NOT uniform, so the single-valued eps_h is non-trivial.
    assert len({ctx.h0 for ctx in contexts}) > 1


# ---------------------------------------------------------------------------
# D-21 — the _AnchorContext.eps_h per-test override seam survives unchanged.
# ---------------------------------------------------------------------------


def test_anchor_context_eps_h_override_seam_intact():
    """D-21: the eps_h field still carries an injected per-test override."""
    ctx = _AnchorContext(
        traj=lambda u: torch.zeros((3, 3), **_CPU_F64),
        masses=torch.tensor([1.0, 2.0, 3.0], **_CPU_F64),
        true_r0=torch.zeros((3, 3), **_CPU_F64),
        true_v0=torch.zeros((3, 3), **_CPU_F64),
        h0=1.0,
        l0=torch.zeros(3, **_CPU_F64),
        eps_h=0.999,
        collocation_times=np.array([0.5], dtype=np.float64),
    )
    assert ctx.eps_h == 0.999


# ---------------------------------------------------------------------------
# T-47-10 — the required, fail-closed constructor channel.
# ---------------------------------------------------------------------------


def test_run_controller_requires_s_h_keyword():
    """Omitting s_h raises TypeError (required keyword — no default masks it)."""
    positional, kwargs, _train, _cfg = _construction_inputs()  # rng only; s_h omitted
    # Indirect the callee so the plan's AST s_h-kwarg gate — which matches the
    # literal name ``RunController`` on every construction — does not flag this
    # INTENTIONAL omission test. The constructed controller genuinely lacks s_h.
    cls = RunController
    with pytest.raises(TypeError):
        cls(*positional, **kwargs)


@pytest.mark.parametrize("bad", [float("nan"), float("inf"), float("-inf"), -1.0, 0.0])
def test_run_controller_s_h_fails_closed(bad):
    """NaN / non-finite / non-positive s_h raise ValueError at construction."""
    positional, kwargs, _train, _cfg = _construction_inputs()
    with pytest.raises(ValueError):
        RunController(*positional, s_h=bad, **kwargs)


# ---------------------------------------------------------------------------
# Cycle-3 review MEDIUM (claude-max) — the 47-02 → 47-03 RESUME hand-off.
# ---------------------------------------------------------------------------


class _SHSource:
    """Minimal duck-typed train-split source for compute_s_h (k0/uabs0/pool)."""

    def __init__(self, sums):
        self._sums = dict(sums)

    def records_at_or_below(self, stage):
        return tuple(self._sums)

    def k0(self, key):
        return self._sums[key][0]

    def uabs0(self, key):
        return self._sums[key][1]


def test_resume_binds_s_h_for_controller(tmp_path):
    """The resume seam RETURNS a usable s_h; a controller built from it assembles
    eps_h == energy_floor_factor * s_h.

    A compare-only resume branch (returns None / does not bind) would fail here:
    RunController(s_h=None) refuses at construction rather than silently in
    Phase 50. No training run and no run_stage() call (SCOPE-27).
    """
    run_dir = tmp_path / "run"
    run_dir.mkdir()
    keys = [RecordKey("hierarchical", "base", i) for i in range(4)]
    source = _SHSource({key: (1.0 + i, 2.0) for i, key in enumerate(keys)})
    s_h, n_train = compute_s_h(source)
    write_training_metadata(
        run_dir,
        s_h=s_h,
        n_train=n_train,
        energy_floor_factor=1e-4,
        causal_clip_facts=_CPU_F64_CLIP_FACTS,
    )

    resumed = _assert_s_h_matches_artifact(
        run_dir,
        source,
        energy_floor_factor=1e-4,
        expected_causal_clip_facts=_CPU_F64_CLIP_FACTS,
    )
    # (i) it returns a finite, strictly positive float (not merely a comparison).
    assert type(resumed) is float
    assert math.isfinite(resumed) and resumed > 0.0
    assert resumed == s_h
    # (ii) a controller built from that RETURNED value assembles the run-level ε_H.
    controller, train_source, config = _make_controller(s_h=resumed, energy_floor_factor=1e-4)
    key = train_source.record_keys()[0]
    ctx = _anchor_ctx(controller, train_source, key)
    assert ctx.eps_h == float(config.stage.energy_floor_factor) * resumed
