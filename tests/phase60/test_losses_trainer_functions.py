"""Phase 60 (INST-05 a): the harness physics step is the trainer's step.

``TracerOracleTests`` build a real ``RunController`` over the Phase 57 stub source
(CPU float64, the production network) and require one harness physics Adam step
to give the same per-term losses and the same ``.grad`` on every parameter as the
controller's own memory-bounded step, for the Stage-0 weights and for weights
with the energy and angular-momentum terms on.

The oracle uses 400 collocation rows rather than the production 4,096. A
production-size step costs about half a minute on this CPU, and the module has to
stay near 30 seconds. 400 rows still exercise what the chunk loop can get wrong:
two chunks at microbatch 256 (256 rows, then 144), so the per-chunk fractions
are 0.64 and 0.36 and not the equal 1/2 that would hide a ``1 / n_chunks``
mistake, unequal rows per bin, and times at both ends of ``[0, T]``.

Every other class runs on a small smooth network with the production call shape.
Identity, mutation, chunk-bound, monitor and polish properties belong to the
composition and do not depend on what the network is, so they need not pay for
the production network. ``mock.patch.object`` on the harness module is the
mutation tool: each trainer function is called by bare name, so patching it moves
the harness output.
"""

from __future__ import annotations

import ast
import contextlib
import dataclasses
import json
import math
import re
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest import mock

import numpy as np
import torch

import pinn.loss_catalog as loss_catalog
import pinn.physics_residual as physics_residual
import pinn.training.controllers as controllers
from pinn.constants import T_CHARACTERISTIC_TIME
from pinn.data import batches
from pinn.data.types import RecordKey
from pinn.loss_catalog import LossWeights
from pinn.verification import learnability_losses as L
from pinn.verification.learnability_losses import (
    make_trajectory,
    physics_adam_step,
    physics_pass1,
)
from tests.phase39.test_prohibitions import executable_source_from_text
from tests.phase57._fixtures import build_run_controller, make_full_slot_source

RTOL = 1e-10
ATOL = 1e-12
MICROBATCH = 256
N_ROWS = 400
TIMES_SEED = 11
TERMS = ("data", "ic", "phys", "energy", "angmom", "total")
MONITOR_KEYS = {
    "w_min",
    "w_mean",
    "w_max",
    "front_idx",
    "residuals_per_bin",
    "raw_residuals_per_bin",
    "r_ref",
}
STAGE0 = LossWeights(lambda_data=1.0, lambda_ic=1.0, lambda_phys=1.0, lambda_e=0.0, lambda_l=0.0)
FULL = LossWeights(lambda_data=1.0, lambda_ic=1.0, lambda_phys=1.0, lambda_e=1.0, lambda_l=1.0)
MIXED = LossWeights(lambda_data=1.0, lambda_ic=0.6, lambda_phys=0.8, lambda_e=1.0, lambda_l=1.0)


def _clear_grads(parameters):
    for parameter in parameters:
        parameter.grad = None


def _snapshot_grads(parameters):
    return [None if p.grad is None else p.grad.detach().clone() for p in parameters]


def _dense(grads, parameters):
    return [torch.zeros_like(p) if g is None else g for g, p in zip(grads, parameters)]


# ---------------------------------------------------------------------------
# The oracle: a real controller step on the production network.
# ---------------------------------------------------------------------------


class TracerOracleTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        tmp = tempfile.TemporaryDirectory()
        cls.addClassCleanup(tmp.cleanup)
        source = make_full_slot_source()
        validation = make_full_slot_source(id_offset=50000)
        cls.controller = build_run_controller(
            source, validation, tmp_dir=tmp.name, s_h=1.0, replay_count=2
        )
        cls.model = cls.controller.model
        cls.dtype = cls.controller._dtype
        cls.device = cls.controller._device
        cls.parameters = tuple(p for p in cls.model.parameters() if p.requires_grad)
        # The batch carries the data points; the collocation rows are supplied
        # directly so the trainer and the harness read the very same array.
        cls.batch = cls.controller._stage_batch(source, stage=0, collocation_count=16)
        rng = np.random.default_rng(TIMES_SEED)
        times = np.sort(rng.uniform(0.0, T_CHARACTERISTIC_TIME, size=N_ROWS))
        times[0] = 0.0
        times[-1] = T_CHARACTERISTIC_TIME
        cls.times = times
        cls.anchor_ctx = cls.controller._build_anchor_context(source, cls.batch, times)
        record = source.get(cls.controller._select_anchor_key(cls.batch))
        cls.ic13_t = torch.as_tensor(
            np.asarray(record.ic13, dtype=np.float64), dtype=cls.dtype, device=cls.device
        )

    def test_fixture_exercises_the_chunk_loop(self):
        self.assertEqual(self.dtype, torch.float64)
        self.assertEqual(self.device.type, "cpu")
        rows = self.anchor_ctx.collocation_times.shape[0]
        self.assertGreater(rows, MICROBATCH)
        self.assertNotEqual(rows % MICROBATCH, 0)
        bins = np.minimum(
            (self.anchor_ctx.collocation_times / T_CHARACTERISTIC_TIME * 16).astype(int), 15
        )
        counts = np.bincount(bins, minlength=16)
        self.assertTrue(bool((counts > 0).all()), counts.tolist())
        self.assertGreater(len(set(counts.tolist())), 1)
        self.assertEqual(float(self.anchor_ctx.collocation_times[0]), 0.0)
        self.assertEqual(float(self.anchor_ctx.collocation_times[-1]), T_CHARACTERISTIC_TIME)
        self.assertEqual(len(self.parameters), 28)

    def test_pass_one_weights_and_bin_counts_equal_the_trainers(self):
        trainer_details, trainer_counts = self.controller._adam_frozen_causal_weights(
            self.anchor_ctx, microbatch_size=MICROBATCH
        )
        traj = make_trajectory(self.model, self.ic13_t, self.anchor_ctx.masses)
        details, counts = physics_pass1(
            traj,
            self.anchor_ctx.masses,
            self.anchor_ctx.collocation_times,
            r_ref=self.controller._r_ref,
            microbatch_size=MICROBATCH,
            dtype=self.dtype,
            device=self.device,
        )
        torch.testing.assert_close(counts, trainer_counts, rtol=0.0, atol=0.0)
        self.assertEqual(float(counts.sum()), float(N_ROWS))
        for key in ("w_n", "rbar", "raw_rbar"):
            torch.testing.assert_close(details[key], trainer_details[key], rtol=RTOL, atol=ATOL)
        self.assertEqual(details["r_ref"], trainer_details["r_ref"])
        self.assertEqual(int(details["w_n"].numel()), 16)

    def _assert_step_equals_the_trainers(self, weights, anchor_ctx):
        controller = self.controller
        _clear_grads(self.parameters)
        trainer_terms, _stats = controller._run_adam_step_microbatched(
            self.batch,
            anchor_ctx,
            weights,
            self.parameters,
            microbatch_size=MICROBATCH,
            want_diagnostics=True,
        )
        trainer_grads = _snapshot_grads(self.parameters)
        _clear_grads(self.parameters)
        harness = physics_adam_step(
            self.model,
            data_points=self.batch.data_points,
            ic13_t=self.ic13_t,
            masses_t=anchor_ctx.masses,
            true_r0=anchor_ctx.true_r0,
            true_v0=anchor_ctx.true_v0,
            collocation_times=anchor_ctx.collocation_times,
            weights=weights,
            r_ref=controller._r_ref,
            h0=anchor_ctx.h0,
            eps_h=anchor_ctx.eps_h,
            l0=anchor_ctx.l0,
            microbatch_size=MICROBATCH,
            dtype=self.dtype,
            device=self.device,
        )
        harness_grads = _snapshot_grads(self.parameters)
        _clear_grads(self.parameters)

        self.assertEqual(set(harness), set(TERMS))
        zero = torch.zeros((), dtype=self.dtype)
        for name in TERMS:
            weight_name = {"energy": "lambda_e", "angmom": "lambda_l"}.get(name)
            skipped = weight_name is not None and getattr(weights, weight_name) == 0.0
            expected = zero if skipped else getattr(trainer_terms, name)
            torch.testing.assert_close(
                harness[name].detach(),
                expected.detach(),
                rtol=RTOL,
                atol=ATOL,
                msg=lambda message, name=name: f"term {name}: {message}",
            )
        # A term whose weight is zero is not evaluated by the harness; the
        # trainer evaluates it and multiplies by zero, so the totals still agree.
        self.assertGreater(float(harness["phys"]), 0.0)
        self.assertGreater(float(harness["ic"]), 0.0)

        self.assertEqual(len(harness_grads), len(trainer_grads))
        compared = 0
        for index, (ours, theirs) in enumerate(zip(harness_grads, trainer_grads)):
            if theirs is None:
                self.assertIsNone(ours, f"parameter {index}")
                continue
            self.assertIsNotNone(ours, f"parameter {index}")
            torch.testing.assert_close(
                ours,
                theirs,
                rtol=RTOL,
                atol=ATOL,
                msg=lambda message, index=index: f"parameter {index} grad: {message}",
            )
            compared += 1
        self.assertEqual(compared, len(self.parameters))
        self.assertGreater(
            sum(float(g.abs().sum()) for g in harness_grads if g is not None), 0.0
        )

    def test_stage_zero_weights_step_equals_the_trainers_microbatched_step(self):
        weights = self.controller.scheduled_weights.current(0)
        self.assertEqual((weights.lambda_e, weights.lambda_l), (0.0, 0.0))
        self._assert_step_equals_the_trainers(weights, self.anchor_ctx)

    def test_energy_and_angular_momentum_on_step_equals_the_trainers_step(self):
        # The stub's initial angular momentum is exactly zero, which makes the
        # angular-momentum scale degenerate (1e-8). Use ordinary conserved
        # quantities, and unequal weights so no lambda is silently fixed at 1.
        weights = LossWeights(
            lambda_data=1.0, lambda_ic=1e-3, lambda_phys=0.7, lambda_e=1.0, lambda_l=1.0
        )
        anchor_ctx = dataclasses.replace(
            self.anchor_ctx,
            h0=-2.0,
            eps_h=0.05,
            l0=torch.tensor([0.5, -0.3, 0.8], dtype=self.dtype, device=self.device),
        )
        self._assert_step_equals_the_trainers(weights, anchor_ctx)


# ---------------------------------------------------------------------------
# A small smooth network and the problem around it.
# ---------------------------------------------------------------------------


class _TinyNet(torch.nn.Module):
    """``forward(tau_ic13 (N, 14), masses (N, 3)) -> (N, 9)``, twice differentiable.

    The three bodies sit near (0, 0, 0), (2, 0, 0) and (0, 2, 0) so the softened
    force stays moderate. What the network computes is irrelevant to the
    properties tested here; it only has to be smooth and parametric.
    """

    def __init__(self, *, dtype, seed):
        super().__init__()
        gen = torch.Generator().manual_seed(seed)
        self.w1 = torch.nn.Parameter(0.6 * torch.randn(17, 10, generator=gen, dtype=dtype))
        self.b1 = torch.nn.Parameter(0.3 * torch.randn(10, generator=gen, dtype=dtype))
        self.w2 = torch.nn.Parameter(0.08 * torch.randn(10, 9, generator=gen, dtype=dtype))
        self.b2 = torch.nn.Parameter(
            torch.tensor([0, 0, 0, 2, 0, 0, 0, 2, 0], dtype=dtype)
        )

    def forward(self, tau_ic13, masses):
        features = torch.cat([tau_ic13, masses], dim=-1)
        return torch.sin(features @ self.w1 + self.b1) @ self.w2 + self.b2


class _Problem:
    """One system on the small network: truth, conserved quantities, rows, ``r_ref``."""

    def __init__(self, *, n_slots=2, seed=0, n_data=24):
        self.dtype = torch.float64
        self.device = torch.device("cpu")
        self.model = _TinyNet(dtype=self.dtype, seed=seed)
        self.parameters = tuple(self.model.parameters())
        self.ic13_t = torch.linspace(-0.6, 0.6, 13, dtype=self.dtype)
        self.masses_t = torch.tensor([1.0, 1.5, 2.0], dtype=self.dtype)
        self.true_r0 = torch.tensor(
            [[0.0, 0.0, 0.0], [2.0, 0.0, 0.0], [0.0, 2.0, 0.0]], dtype=self.dtype
        )
        self.true_v0 = torch.tensor(
            [[0.0, 0.3, 0.0], [0.0, 0.0, 0.2], [-0.1, 0.0, 0.0]], dtype=self.dtype
        )
        self.h0 = float(
            loss_catalog._matched_plummer_hamiltonian(
                self.true_r0.unsqueeze(0),
                self.true_v0.unsqueeze(0),
                self.masses_t,
                dtype=self.dtype,
                device=self.device,
            )[0]
        )
        self.l0 = loss_catalog._angular_momentum(
            self.true_r0.unsqueeze(0),
            self.true_v0.unsqueeze(0),
            self.masses_t,
            dtype=self.dtype,
            device=self.device,
        )[0]
        self.eps_h = 1e-2
        gen = torch.Generator().manual_seed(seed + 1)
        tau = 2.0 * torch.rand(n_data, 1, generator=gen, dtype=self.dtype) - 1.0
        self.data_points = SimpleNamespace(
            tau_ic13=torch.cat([tau, self.ic13_t.expand(n_data, 13)], dim=1),
            masses=self.masses_t.expand(n_data, 3).clone(),
            targets=self.true_r0.expand(n_data, 3, 3)
            + 0.2 * torch.randn(n_data, 3, 3, generator=gen, dtype=self.dtype),
        )
        self.key = RecordKey("hierarchical", "base", 0)
        self.times = L.draw_collocation_times(
            self.key, np.random.default_rng(3), n_slots=n_slots
        )
        # r_ref makes the normalized per-bin residuals of order one, so the causal
        # weights and every term are far from zero and from saturation.
        details, _counts = physics_pass1(
            self.traj(),
            self.masses_t,
            self.times,
            r_ref=1.0,
            microbatch_size=256,
            dtype=self.dtype,
            device=self.device,
        )
        self.r_ref = float(details["raw_rbar"].mean())

    def traj(self):
        return make_trajectory(self.model, self.ic13_t, self.masses_t)

    def clear(self):
        _clear_grads(self.parameters)

    def grads(self):
        return _snapshot_grads(self.parameters)

    def step(self, weights, *, data=True, times=None, microbatch=16):
        return physics_adam_step(
            self.model,
            data_points=self.data_points if data else None,
            ic13_t=self.ic13_t,
            masses_t=self.masses_t,
            true_r0=self.true_r0,
            true_v0=self.true_v0,
            collocation_times=self.times if times is None else times,
            weights=weights,
            r_ref=self.r_ref,
            h0=self.h0,
            eps_h=self.eps_h,
            l0=self.l0,
            microbatch_size=microbatch,
            dtype=self.dtype,
            device=self.device,
        )

    def pass1(self, times=None, *, microbatch=16):
        return physics_pass1(
            self.traj(),
            self.masses_t,
            self.times if times is None else times,
            r_ref=self.r_ref,
            microbatch_size=microbatch,
            dtype=self.dtype,
            device=self.device,
        )

    def monitor(self, times=None, *, microbatch=16):
        return L.frozen_monitor_log(
            self.traj(),
            self.masses_t,
            self.times if times is None else times,
            r_ref=self.r_ref,
            microbatch_size=microbatch,
            dtype=self.dtype,
            device=self.device,
        )

    def polish(
        self,
        weights,
        *,
        details=None,
        counts=None,
        times=None,
        data=True,
        chunk=7,
        microbatch=16,
    ):
        if details is None:
            details, counts = self.pass1(times, microbatch=microbatch)
        return L.physics_polish_objective(
            self.model,
            frozen_times=self.times if times is None else times,
            frozen_w_n=details["w_n"],
            frozen_bin_counts=counts,
            frozen_weights=weights,
            data_points=self.data_points if data else None,
            ic13_t=self.ic13_t,
            masses_t=self.masses_t,
            true_r0=self.true_r0,
            true_v0=self.true_v0,
            r_ref=self.r_ref,
            h0=self.h0,
            eps_h=self.eps_h,
            l0=self.l0,
            data_chunk_size=chunk,
            microbatch_size=microbatch,
            dtype=self.dtype,
            device=self.device,
        )


def _scaled(original, factor=2.0):
    def wrapper(*args, **kwargs):
        return original(*args, **kwargs) * factor

    return wrapper


def _with_w_n(original, transform):
    """Wrap ``causal_physics_loss`` so the returned detail ``w_n`` is replaced."""

    def wrapper(*args, **kwargs):
        loss, details = original(*args, **kwargs)
        details = dict(details)
        details["w_n"] = transform(details["w_n"])
        return loss, details

    return wrapper


def _assert_ratio(case, mutated, base, ratio=2.0):
    case.assertGreater(abs(float(base)), 1e-6)
    case.assertAlmostEqual(float(mutated) / float(base), ratio, places=12)


def _assert_same(case, mutated, base):
    case.assertTrue(
        math.isclose(float(mutated), float(base), rel_tol=1e-12, abs_tol=1e-12),
        (float(mutated), float(base)),
    )


# ---------------------------------------------------------------------------
# Identity and mutation: the harness calls the trainer's functions.
# ---------------------------------------------------------------------------


class IdentityTests(unittest.TestCase):
    def test_each_function_is_the_trainers_object(self):
        table = (
            ("data_huber_loss", (loss_catalog, controllers)),
            ("ic_anchor_loss", (loss_catalog, controllers)),
            ("causal_physics_loss", (loss_catalog, controllers)),
            ("soft_energy_loss", (loss_catalog, controllers)),
            ("angular_momentum_loss", (loss_catalog, controllers)),
            ("compose_total", (loss_catalog, controllers)),
            ("componentwise_du", (physics_residual, controllers)),
            ("softened_acceleration", (physics_residual, controllers)),
            ("accumulate_chunked_data_term", (controllers,)),
            ("LossWeights", (loss_catalog,)),
            ("_bin_index_for_times", (controllers,)),
            ("_stratified_full_slot_rows", (batches,)),
        )
        for name, owners in table:
            with self.subTest(name=name):
                for owner in owners:
                    self.assertIs(getattr(L, name), getattr(owner, name), owner.__name__)

    def test_the_bin_count_is_the_ratified_sixteen(self):
        self.assertEqual(L._RATIFIED_N_BINS, controllers._RATIFIED_N_BINS)
        self.assertEqual(L._RATIFIED_N_BINS, 16)

    def test_the_trajectory_scale_is_the_ratified_horizon(self):
        self.assertEqual(L.T_CHARACTERISTIC_TIME, T_CHARACTERISTIC_TIME)
        self.assertEqual(L.T_CHARACTERISTIC_TIME, controllers.T_CHARACTERISTIC_TIME)


class MutationTests(unittest.TestCase):
    """INST-05(a), the INST-04 SC3 pattern: patch a trainer function, the output moves."""

    def setUp(self):
        self.problem = _Problem()

    def _base_and_mutated(self, name, replacement, weights=FULL, **step_kwargs):
        base = self.problem.step(weights, **step_kwargs)
        self.problem.clear()
        with mock.patch.object(L, name, side_effect=replacement):
            mutated = self.problem.step(weights, **step_kwargs)
        self.problem.clear()
        return base, mutated

    def _assert_only_moved(self, base, mutated, moved):
        for name in ("data", "ic", "phys", "energy", "angmom"):
            if name != moved:
                _assert_same(self, mutated[name], base[name])

    def test_every_term_is_positive_and_finite_on_the_small_problem(self):
        terms = self.problem.step(FULL)
        for name in TERMS:
            with self.subTest(term=name):
                self.assertGreater(float(terms[name]), 1e-6)
                self.assertTrue(math.isfinite(float(terms[name])))

    def test_data_huber_loss_doubles_the_data_term(self):
        base, mutated = self._base_and_mutated("data_huber_loss", _scaled(L.data_huber_loss))
        _assert_ratio(self, mutated["data"], base["data"])
        self._assert_only_moved(base, mutated, "data")

    def test_data_huber_loss_doubles_the_data_only_loss(self):
        p = self.problem
        kwargs = dict(dtype=p.dtype, device=p.device)
        base = L.data_only_loss(p.model, p.data_points, **kwargs).detach()
        with mock.patch.object(L, "data_huber_loss", side_effect=_scaled(L.data_huber_loss)):
            mutated = L.data_only_loss(p.model, p.data_points, **kwargs).detach()
        _assert_ratio(self, mutated, base)

    def test_ic_anchor_loss_doubles_the_ic_term(self):
        base, mutated = self._base_and_mutated("ic_anchor_loss", _scaled(L.ic_anchor_loss))
        _assert_ratio(self, mutated["ic"], base["ic"])
        self._assert_only_moved(base, mutated, "ic")

    def test_a_causal_physics_loss_that_doubles_w_n_doubles_the_phys_term(self):
        wrapper = _with_w_n(L.causal_physics_loss, lambda w: w * 2.0)
        base, mutated = self._base_and_mutated("causal_physics_loss", wrapper)
        _assert_ratio(self, mutated["phys"], base["phys"])
        self._assert_only_moved(base, mutated, "phys")

    def test_soft_energy_loss_doubles_the_energy_term(self):
        base, mutated = self._base_and_mutated("soft_energy_loss", _scaled(L.soft_energy_loss))
        _assert_ratio(self, mutated["energy"], base["energy"])
        self._assert_only_moved(base, mutated, "energy")

    def test_angular_momentum_loss_doubles_the_angular_momentum_term(self):
        base, mutated = self._base_and_mutated(
            "angular_momentum_loss", _scaled(L.angular_momentum_loss)
        )
        _assert_ratio(self, mutated["angmom"], base["angmom"])
        self._assert_only_moved(base, mutated, "angmom")

    def test_accumulate_chunked_data_term_doubles_the_data_polish_objective(self):
        p = self.problem
        kwargs = dict(chunk_size=7, dtype=p.dtype, device=p.device)
        base = L.data_polish_objective(p.model, p.data_points, **kwargs)
        with mock.patch.object(
            L,
            "accumulate_chunked_data_term",
            side_effect=_scaled(L.accumulate_chunked_data_term),
        ):
            mutated = L.data_polish_objective(p.model, p.data_points, **kwargs)
        _assert_ratio(self, mutated, base)

    def test_componentwise_du_changes_the_phys_term(self):
        original = L.componentwise_du

        def wrapper(fn, u_leaf):
            first, second = original(fn, u_leaf)
            return first, second * 2.0

        base, mutated = self._base_and_mutated("componentwise_du", wrapper)
        self.assertNotAlmostEqual(float(mutated["phys"]), float(base["phys"]), places=6)
        self._assert_only_moved(base, mutated, "phys")

    def test_softened_acceleration_changes_the_phys_term(self):
        base, mutated = self._base_and_mutated(
            "softened_acceleration", _scaled(L.softened_acceleration)
        )
        self.assertNotAlmostEqual(float(mutated["phys"]), float(base["phys"]), places=6)
        self._assert_only_moved(base, mutated, "phys")

    def test_compose_total_makes_the_total(self):
        original = L.compose_total

        def wrapper(terms, weights):
            composed = original(terms, weights)
            return dataclasses.replace(composed, total=composed.total * 2.0)

        base, mutated = self._base_and_mutated("compose_total", wrapper)
        _assert_ratio(self, mutated["total"], base["total"])
        for name in ("data", "ic", "phys", "energy", "angmom"):
            _assert_same(self, mutated[name], base[name])

    def test_the_total_is_the_weighted_sum_of_the_terms(self):
        terms = self.problem.step(MIXED)
        expected = (
            MIXED.lambda_data * terms["data"]
            + MIXED.lambda_ic * terms["ic"]
            + MIXED.lambda_phys * terms["phys"]
            + MIXED.lambda_e * terms["energy"]
            + MIXED.lambda_l * terms["angmom"]
        )
        _assert_same(self, terms["total"], expected)


# ---------------------------------------------------------------------------
# Terms are evaluated only when they have weight; Rung 2a has no data term.
# ---------------------------------------------------------------------------


class ZeroWeightAndRungTwoATests(unittest.TestCase):
    def setUp(self):
        self.problem = _Problem()

    def test_energy_and_angular_momentum_are_not_evaluated_at_zero_weight(self):
        with mock.patch.object(
            L, "soft_energy_loss", wraps=L.soft_energy_loss
        ) as energy, mock.patch.object(
            L, "angular_momentum_loss", wraps=L.angular_momentum_loss
        ) as angmom:
            terms = self.problem.step(STAGE0)
        self.assertEqual(energy.call_count, 0)
        self.assertEqual(angmom.call_count, 0)
        self.assertEqual(float(terms["energy"]), 0.0)
        self.assertEqual(float(terms["angmom"]), 0.0)

    def test_each_term_is_gated_by_its_own_weight(self):
        energy_only = LossWeights(
            lambda_data=1.0, lambda_ic=1.0, lambda_phys=1.0, lambda_e=1.0, lambda_l=0.0
        )
        angmom_only = LossWeights(
            lambda_data=1.0, lambda_ic=1.0, lambda_phys=1.0, lambda_e=0.0, lambda_l=1.0
        )
        for weights, called, silent in (
            (energy_only, "soft_energy_loss", "angular_momentum_loss"),
            (angmom_only, "angular_momentum_loss", "soft_energy_loss"),
        ):
            with self.subTest(called=called):
                with mock.patch.object(
                    L, called, wraps=getattr(L, called)
                ) as on, mock.patch.object(L, silent, wraps=getattr(L, silent)) as off:
                    self.problem.step(weights)
                self.assertGreater(on.call_count, 0)
                self.assertEqual(off.call_count, 0)

    def test_rung_2a_never_evaluates_the_data_term(self):
        with mock.patch.object(L, "data_huber_loss", wraps=L.data_huber_loss) as huber:
            terms = self.problem.step(STAGE0, data=False)
        self.assertEqual(huber.call_count, 0)
        self.assertEqual(float(terms["data"]), 0.0)
        self.assertGreater(float(terms["ic"]), 0.0)
        self.assertGreater(float(terms["phys"]), 0.0)

    def test_rung_2a_hands_compose_total_a_zero_tensor_for_data(self):
        seen = []
        original = L.compose_total

        def spy(terms, weights):
            seen.append((dict(terms), weights))
            return original(terms, weights)

        with mock.patch.object(L, "compose_total", side_effect=spy):
            self.problem.step(STAGE0, data=False)
        self.assertEqual(len(seen), 1)
        terms, weights = seen[0]
        self.assertEqual(set(terms), {"data", "ic", "phys", "energy", "angmom"})
        self.assertTrue(torch.is_tensor(terms["data"]))
        self.assertEqual(terms["data"].dim(), 0)
        self.assertEqual(terms["data"].dtype, torch.float64)
        self.assertEqual(float(terms["data"]), 0.0)
        # The weights keep lambda_data at 1.0: Rung 2a is never "lambda_data = 0".
        self.assertEqual(weights.lambda_data, 1.0)

    def test_the_trainers_weights_cannot_switch_the_data_term_off(self):
        with self.assertRaises(ValueError):
            LossWeights(lambda_data=0.0)

    def test_rung_2a_gradient_is_the_full_gradient_minus_the_data_gradient(self):
        p = self.problem
        p.step(FULL)
        full = _dense(p.grads(), p.parameters)
        p.clear()
        L.data_only_loss(p.model, p.data_points, dtype=p.dtype, device=p.device).backward()
        data = _dense(p.grads(), p.parameters)
        p.clear()
        p.step(FULL, data=False)
        rung_a = _dense(p.grads(), p.parameters)
        p.clear()
        for index, (g_full, g_data, g_a) in enumerate(zip(full, data, rung_a)):
            torch.testing.assert_close(
                g_full - g_data,
                g_a,
                rtol=1e-8,
                atol=1e-10,
                msg=lambda message, index=index: f"parameter {index}: {message}",
            )


# ---------------------------------------------------------------------------
# The collocation draw.
# ---------------------------------------------------------------------------


class DrawTests(unittest.TestCase):
    key = RecordKey("hierarchical", "base", 0)

    def _bins(self, times):
        return controllers._bin_index_for_times(
            torch.as_tensor(times), n_bins=16, t_max=T_CHARACTERISTIC_TIME
        )

    def test_the_default_draw_is_4096_rows_with_256_in_each_bin(self):
        times = L.draw_collocation_times(self.key, np.random.default_rng(5))
        self.assertEqual(times.shape, (4096,))
        self.assertEqual(times.dtype, np.float64)
        self.assertTrue(bool((np.diff(times) >= 0.0).all()))
        self.assertGreaterEqual(float(times.min()), 0.0)
        self.assertLessEqual(float(times.max()), T_CHARACTERISTIC_TIME)
        counts = torch.bincount(self._bins(times), minlength=16).tolist()
        self.assertEqual(counts, [256] * 16)

    def test_the_draw_is_the_ratified_stratified_rows_sorted(self):
        times = L.draw_collocation_times(self.key, np.random.default_rng(5), n_slots=3)
        rows = batches._stratified_full_slot_rows([self.key] * 3, rng=np.random.default_rng(5))
        expected = np.sort(np.asarray([t for _k, t in rows], dtype=np.float64))
        np.testing.assert_array_equal(times, expected)

    def test_one_slot_gives_one_row_per_bin(self):
        times = L.draw_collocation_times(self.key, np.random.default_rng(5), n_slots=1)
        self.assertEqual(times.shape, (16,))
        self.assertEqual(self._bins(times).tolist(), list(range(16)))

    def test_a_draw_advances_the_stream_and_a_reseed_repeats_it(self):
        rng = np.random.default_rng(5)
        first = L.draw_collocation_times(self.key, rng, n_slots=2)
        second = L.draw_collocation_times(self.key, rng, n_slots=2)
        again = L.draw_collocation_times(self.key, np.random.default_rng(5), n_slots=2)
        self.assertFalse(np.array_equal(first, second))
        np.testing.assert_array_equal(first, again)

    def test_a_non_positive_or_non_integer_slot_count_is_refused(self):
        for bad in (0, -1, 2.0, True, None):
            with self.subTest(n_slots=bad):
                with self.assertRaises(ValueError):
                    L.draw_collocation_times(self.key, np.random.default_rng(5), n_slots=bad)

    def test_one_row_per_bin_runs_end_to_end(self):
        # Plan 60-11's fixture arms draw one slot (16 rows).
        problem = _Problem(n_slots=1)
        terms = problem.step(FULL, microbatch=256)
        for name in TERMS:
            self.assertTrue(math.isfinite(float(terms[name])), name)
        _details, counts = problem.pass1(microbatch=256)
        self.assertEqual(counts.tolist(), [1.0] * 16)


# ---------------------------------------------------------------------------
# No evaluation path ever builds more than one chunk's graph.
# ---------------------------------------------------------------------------


class _ChunkSpy:
    """Record the leading size of every vector ``u`` given to ``componentwise_du``."""

    def __init__(self):
        self.sizes = []
        self.releases = 0
        self._du = L.componentwise_du
        self._release = L.release_chunk_memory

    def du(self, fn, u_leaf):
        if torch.is_tensor(u_leaf) and u_leaf.dim() == 1:
            self.sizes.append(int(u_leaf.shape[0]))
        return self._du(fn, u_leaf)

    def release(self, device):
        self.releases += 1
        return self._release(device)

    @contextlib.contextmanager
    def installed(self):
        with mock.patch.object(L, "componentwise_du", side_effect=self.du), mock.patch.object(
            L, "release_chunk_memory", side_effect=self.release
        ):
            yield self


class ChunkBoundTests(unittest.TestCase):
    ROWS = 4096

    def setUp(self):
        self.problem = _Problem(n_slots=256)
        self.assertEqual(self.problem.times.shape[0], self.ROWS)

    def _check(self, spy, *, passes, microbatch):
        n_chunks = -(-self.ROWS // microbatch)
        self.assertEqual(max(spy.sizes), microbatch)
        self.assertEqual(len(spy.sizes), n_chunks * passes)
        self.assertGreaterEqual(len(spy.sizes), 16 * passes if microbatch == 256 else 1)
        self.assertEqual(sum(spy.sizes), self.ROWS * passes)
        self.assertGreaterEqual(spy.releases, len(spy.sizes))

    def _paths(self, microbatch):
        p = self.problem
        details, counts = p.pass1(microbatch=microbatch)
        weights = MIXED
        return {
            "physics_pass1": (1, lambda: p.pass1(microbatch=microbatch)),
            "physics_pass2_backward": (
                1,
                lambda: L.physics_pass2_backward(
                    p.traj(),
                    p.masses_t,
                    p.times,
                    w_n=details["w_n"],
                    bin_counts=counts,
                    r_ref=p.r_ref,
                    weights=weights,
                    h0=p.h0,
                    eps_h=p.eps_h,
                    l0=p.l0,
                    microbatch_size=microbatch,
                    dtype=p.dtype,
                    device=p.device,
                ),
            ),
            "frozen_monitor_log": (1, lambda: p.monitor(microbatch=microbatch)),
            "physics_polish_objective": (
                1,
                lambda: p.polish(
                    weights, details=details, counts=counts, chunk=1024, microbatch=microbatch
                ),
            ),
            "physics_adam_step": (2, lambda: p.step(weights, microbatch=microbatch)),
        }

    def test_every_path_uses_chunks_of_at_most_256_rows(self):
        for name, (passes, call) in self._paths(256).items():
            with self.subTest(path=name):
                spy = _ChunkSpy()
                with spy.installed():
                    call()
                self._check(spy, passes=passes, microbatch=256)
                self.problem.clear()

    def test_a_microbatch_that_does_not_divide_the_rows(self):
        for name, (passes, call) in self._paths(100).items():
            with self.subTest(path=name):
                spy = _ChunkSpy()
                with spy.installed():
                    call()
                self._check(spy, passes=passes, microbatch=100)
                self.assertEqual(spy.sizes[-1], self.ROWS - 40 * 100)
                self.problem.clear()

    def test_a_non_positive_microbatch_is_refused(self):
        p = self.problem
        for bad in (0, -256):
            with self.subTest(microbatch=bad):
                with self.assertRaises(ValueError):
                    p.pass1(microbatch=bad)
                with self.assertRaises(ValueError):
                    p.monitor(microbatch=bad)


class ReleaseChunkMemoryTests(unittest.TestCase):
    def test_a_cpu_device_collects_generation_zero_and_leaves_the_cache_alone(self):
        with mock.patch.object(L.gc, "collect") as collect, mock.patch.object(
            L.torch.mps, "empty_cache"
        ) as empty_cache:
            L.release_chunk_memory(torch.device("cpu"))
        collect.assert_called_once_with(0)
        empty_cache.assert_not_called()

    def test_an_mps_device_empties_the_cache(self):
        with mock.patch.object(L.gc, "collect") as collect, mock.patch.object(
            L.torch.mps, "empty_cache"
        ) as empty_cache:
            L.release_chunk_memory(SimpleNamespace(type="mps"))
        collect.assert_called_once_with(0)
        empty_cache.assert_called_once_with()

    def test_an_error_from_the_cache_call_is_ignored(self):
        with mock.patch.object(L.gc, "collect"), mock.patch.object(
            L.torch.mps, "empty_cache", side_effect=RuntimeError("no mps backend")
        ) as empty_cache:
            L.release_chunk_memory(SimpleNamespace(type="mps"))
        empty_cache.assert_called_once_with()

    def test_an_error_from_the_collector_is_not_ignored(self):
        with mock.patch.object(L.gc, "collect", side_effect=RuntimeError("collector")):
            with self.assertRaises(RuntimeError):
                L.release_chunk_memory(torch.device("cpu"))


# ---------------------------------------------------------------------------
# D-06: the frozen monitor is logged, never acted on.
# ---------------------------------------------------------------------------


class MonitorTests(unittest.TestCase):
    def setUp(self):
        self.problem = _Problem(n_slots=256)  # one fixed 4,096-row set

    def test_the_log_has_the_seven_keys_and_plain_json_values(self):
        log = self.problem.monitor(microbatch=256)
        self.assertEqual(set(log), MONITOR_KEYS)
        self.assertEqual(len(log["residuals_per_bin"]), 16)
        self.assertEqual(len(log["raw_residuals_per_bin"]), 16)
        for key in ("w_min", "w_mean", "w_max", "r_ref"):
            self.assertIs(type(log[key]), float, key)
        self.assertIs(type(log["front_idx"]), int)
        for key in ("residuals_per_bin", "raw_residuals_per_bin"):
            self.assertTrue(all(type(value) is float for value in log[key]), key)
        round_trip = json.loads(json.dumps(log, allow_nan=False))
        self.assertEqual(round_trip, log)

    def test_the_log_is_the_pass_one_statistics(self):
        p = self.problem
        log = p.monitor(microbatch=256)
        details, _counts = p.pass1(microbatch=256)
        w_n = details["w_n"].tolist()
        self.assertEqual(log["w_min"], min(w_n))
        self.assertEqual(log["w_max"], max(w_n))
        self.assertAlmostEqual(log["w_mean"], sum(w_n) / 16.0, places=14)
        self.assertEqual(log["front_idx"], max([n for n, w in enumerate(w_n) if w > 0.5], default=-1))
        self.assertEqual(log["residuals_per_bin"], details["rbar"].tolist())
        self.assertEqual(log["raw_residuals_per_bin"], details["raw_rbar"].tolist())
        self.assertEqual(log["r_ref"], p.r_ref)
        # R_ref is the explicit argument: the normalized residuals divide by it.
        for raw, normalized in zip(log["raw_residuals_per_bin"], log["residuals_per_bin"]):
            self.assertAlmostEqual(normalized, raw / p.r_ref, places=12)

    def test_front_idx_is_the_largest_bin_whose_weight_exceeds_one_half(self):
        cases = (
            ([1.0] * 6 + [0.1] * 10, 5),
            ([1.0, 0.9, 0.1, 0.8, 0.1] + [0.1] * 11, 3),
            ([1.0] * 16, 15),
            ([0.5] + [0.4] * 15, -1),
        )
        for weights, expected in cases:
            with self.subTest(expected=expected):
                wrapper = _with_w_n(
                    L.causal_physics_loss,
                    lambda w, values=weights: torch.tensor(values, dtype=w.dtype),
                )
                with mock.patch.object(L, "causal_physics_loss", side_effect=wrapper):
                    log = self.problem.monitor(microbatch=256)
                self.assertEqual(log["front_idx"], expected)

    def test_a_stalled_front_is_logged_not_halted(self):
        wrapper = _with_w_n(L.causal_physics_loss, lambda w: torch.full_like(w, 0.25))
        with mock.patch.object(L, "causal_physics_loss", side_effect=wrapper):
            log = self.problem.monitor(microbatch=256)
        self.assertEqual(log["front_idx"], -1)
        self.assertEqual(log["w_max"], 0.25)
        self.assertEqual(log["w_min"], 0.25)
        self.assertEqual(set(log), MONITOR_KEYS)

    def test_a_collapsed_weight_vector_is_logged_not_halted(self):
        # The smallest positive weights the trainer's formula can return.
        tiny = torch.finfo(torch.float64).tiny
        wrapper = _with_w_n(L.causal_physics_loss, lambda w: torch.full_like(w, tiny))
        with mock.patch.object(L, "causal_physics_loss", side_effect=wrapper):
            log = self.problem.monitor(microbatch=256)
        self.assertEqual(log["front_idx"], -1)
        self.assertEqual(log["w_max"], tiny)

    def test_a_patched_causal_loss_moves_the_logged_weights(self):
        base = self.problem.monitor(microbatch=256)
        wrapper = _with_w_n(L.causal_physics_loss, lambda w: w * 2.0)
        with mock.patch.object(L, "causal_physics_loss", side_effect=wrapper):
            doubled = self.problem.monitor(microbatch=256)
        for key in ("w_min", "w_mean", "w_max"):
            self.assertAlmostEqual(doubled[key] / base[key], 2.0, places=12)

    def test_the_same_frozen_rows_give_the_same_log_at_the_same_parameters(self):
        first = self.problem.monitor(microbatch=256)
        second = self.problem.monitor(microbatch=256)
        self.assertEqual(first, second)

    def test_the_log_follows_the_parameters_it_is_called_at(self):
        before = self.problem.monitor(microbatch=256)
        with torch.no_grad():
            self.problem.model.w2.add_(0.05)
        after = self.problem.monitor(microbatch=256)
        self.assertNotEqual(before["raw_residuals_per_bin"], after["raw_residuals_per_bin"])

    def test_the_monitor_leaves_no_gradient_behind(self):
        self.problem.monitor(microbatch=256)
        self.assertTrue(all(p.grad is None for p in self.problem.parameters))

    def test_the_monitor_has_no_halt_path(self):
        tree = ast.parse(Path(L.__file__).read_text(encoding="utf-8"))
        monitors = [
            node
            for node in ast.walk(tree)
            if isinstance(node, ast.FunctionDef) and node.name == "frozen_monitor_log"
        ]
        self.assertEqual(len(monitors), 1)
        for node in ast.walk(monitors[0]):
            self.assertNotIsInstance(node, (ast.Raise, ast.Assert, ast.Try), ast.dump(node))
        names = {n.id for n in ast.walk(monitors[0]) if isinstance(n, ast.Name)}
        self.assertTrue(names.isdisjoint({"sys", "exit", "quit", "HarnessHalt"}))


# ---------------------------------------------------------------------------
# GAP-60-05: the polish freezes rows, causal weights and loss weights.
# ---------------------------------------------------------------------------


class PolishObjectiveTests(unittest.TestCase):
    def setUp(self):
        self.problem = _Problem()
        self.details, self.counts = self.problem.pass1()

    def _polish(self, weights=MIXED, **kwargs):
        kwargs.setdefault("details", self.details)
        kwargs.setdefault("counts", self.counts)
        return self.problem.polish(weights, **kwargs)

    def test_two_evaluations_on_the_same_frozen_inputs_are_identical(self):
        p = self.problem
        first = self._polish()
        first_grads = p.grads()
        p.clear()
        second = self._polish()
        second_grads = p.grads()
        p.clear()
        self.assertEqual(float(first), float(second))
        for ours, theirs in zip(first_grads, second_grads):
            torch.testing.assert_close(ours, theirs, rtol=0.0, atol=0.0)

    def test_the_value_is_detached_and_scalar(self):
        value = self._polish()
        self.assertTrue(torch.is_tensor(value))
        self.assertEqual(value.dim(), 0)
        self.assertFalse(value.requires_grad)
        self.assertEqual(value.dtype, torch.float64)

    def test_the_value_equals_the_sum_of_the_terms_the_adam_step_reports(self):
        p = self.problem
        adam = p.step(MIXED)
        p.clear()
        value = self._polish()
        p.clear()
        expected = (
            MIXED.lambda_data * adam["data"]
            + MIXED.lambda_ic * adam["ic"]
            + MIXED.lambda_phys * adam["phys"]
            + MIXED.lambda_e * adam["energy"]
            + MIXED.lambda_l * adam["angmom"]
        )
        _assert_same(self, value, expected)
        _assert_same(self, value, adam["total"])

    def test_the_gradient_equals_the_adam_steps_when_w_n_is_the_pass_one_result(self):
        p = self.problem
        p.step(MIXED)
        adam_grads = _dense(p.grads(), p.parameters)
        p.clear()
        self._polish()
        polish_grads = _dense(p.grads(), p.parameters)
        p.clear()
        for index, (ours, theirs) in enumerate(zip(polish_grads, adam_grads)):
            torch.testing.assert_close(
                ours,
                theirs,
                rtol=RTOL,
                atol=ATOL,
                msg=lambda message, index=index: f"parameter {index}: {message}",
            )

    def test_the_frozen_rows_and_weights_are_not_redrawn_or_recomputed(self):
        p = self.problem
        with mock.patch.object(
            L, "causal_physics_loss", wraps=L.causal_physics_loss
        ) as causal, mock.patch.object(
            L, "_stratified_full_slot_rows", wraps=L._stratified_full_slot_rows
        ) as redraw:
            at_handoff = float(self._polish())
            with torch.no_grad():
                p.model.w2.add_(0.05)
            moved = float(self._polish())
            moved_again = float(self._polish())
        self.assertEqual(causal.call_count, 0)
        self.assertEqual(redraw.call_count, 0)
        self.assertNotEqual(at_handoff, moved)
        self.assertEqual(moved, moved_again)

    def test_the_supplied_causal_weights_are_the_ones_used(self):
        p = self.problem
        base = float(self._polish())
        doubled = {"w_n": self.details["w_n"] * 2.0}
        raised = float(self._polish(details=doubled))
        # Only the physics part scales with w_n, and it is linear in it.
        adam = p.step(MIXED)
        p.clear()
        self.assertAlmostEqual(
            (raised - base) / (MIXED.lambda_phys * float(adam["phys"])), 1.0, places=10
        )

    def test_the_loss_weights_are_the_frozen_ones(self):
        p = self.problem
        first = float(self._polish(weights=MIXED))
        other = LossWeights(
            lambda_data=1.0, lambda_ic=0.3, lambda_phys=0.2, lambda_e=0.5, lambda_l=0.1
        )
        second = float(self._polish(weights=other))
        self.assertNotEqual(first, second)
        adam = p.step(other)
        p.clear()
        _assert_same(self, second, adam["total"])

    def test_rung_2a_polish_has_no_data_term(self):
        p = self.problem
        with mock.patch.object(
            L, "accumulate_chunked_data_term", wraps=L.accumulate_chunked_data_term
        ) as chunked:
            value = self._polish(STAGE0, data=False)
        self.assertEqual(chunked.call_count, 0)
        p.clear()
        adam = p.step(STAGE0, data=False)
        _assert_same(self, value, adam["total"])

    def test_the_data_term_comes_from_the_trainers_chunked_function(self):
        p = self.problem
        calls = []
        original = L.accumulate_chunked_data_term

        def spy(*args, **kwargs):
            calls.append(kwargs)
            return original(*args, **kwargs)

        with mock.patch.object(L, "accumulate_chunked_data_term", side_effect=spy):
            self._polish(MIXED, chunk=5)
        p.clear()
        self.assertEqual(len(calls), 1)
        self.assertEqual(calls[0]["weight"], MIXED.lambda_data)
        self.assertEqual(calls[0]["chunk_size"], 5)
        self.assertEqual(calls[0]["dtype"], p.dtype)

    def test_doubling_the_chunked_data_term_raises_the_value_by_the_data_part(self):
        p = self.problem
        base = float(self._polish(MIXED))
        p.clear()
        data_part = float(
            L.data_polish_objective(p.model, p.data_points, chunk_size=7, dtype=p.dtype, device=p.device)
        )
        p.clear()
        with mock.patch.object(
            L,
            "accumulate_chunked_data_term",
            side_effect=_scaled(L.accumulate_chunked_data_term),
        ):
            mutated = float(self._polish(MIXED))
        p.clear()
        self.assertTrue(
            math.isclose(mutated - base, MIXED.lambda_data * data_part, rel_tol=1e-10),
            (mutated - base, data_part),
        )

    def test_gradients_are_cleared_before_accumulating(self):
        p = self.problem
        self._polish()
        clean = _dense(p.grads(), p.parameters)
        p.clear()
        for parameter in p.parameters:
            parameter.grad = torch.ones_like(parameter)
        self._polish()
        dirty = _dense(p.grads(), p.parameters)
        p.clear()
        for ours, theirs in zip(dirty, clean):
            torch.testing.assert_close(ours, theirs, rtol=0.0, atol=0.0)

    def test_zero_weight_terms_are_not_evaluated_in_the_polish(self):
        with mock.patch.object(
            L, "soft_energy_loss", wraps=L.soft_energy_loss
        ) as energy, mock.patch.object(
            L, "angular_momentum_loss", wraps=L.angular_momentum_loss
        ) as angmom:
            self._polish(STAGE0)
        self.assertEqual(energy.call_count, 0)
        self.assertEqual(angmom.call_count, 0)

    def test_the_value_is_independent_of_the_microbatch_size(self):
        small = float(self._polish(microbatch=8))
        self.problem.clear()
        large = float(self._polish(microbatch=256))
        self.problem.clear()
        self.assertTrue(math.isclose(small, large, rel_tol=1e-12), (small, large))


# ---------------------------------------------------------------------------
# What the module exports and what it must never name.
# ---------------------------------------------------------------------------


class ModuleContractTests(unittest.TestCase):
    PLANNED_EXPORTS = {
        "make_trajectory",
        "draw_collocation_times",
        "collocation_chunk_raw",
        "physics_pass1",
        "ic_term",
        "physics_pass2_backward",
        "physics_adam_step",
        "physics_polish_objective",
        "frozen_monitor_log",
        "release_chunk_memory",
        "data_only_loss",
        "data_polish_objective",
    }

    def test_the_exports_are_the_planned_twelve(self):
        self.assertEqual(set(L.__all__), self.PLANNED_EXPORTS)
        self.assertEqual(len(L.__all__), len(set(L.__all__)))
        for name in L.__all__:
            self.assertTrue(callable(getattr(L, name)), name)

    def test_the_module_names_no_full_batch_trainer_path_and_no_halting_rule(self):
        executable = executable_source_from_text(Path(L.__file__).read_text(encoding="utf-8"))
        forbidden = (
            "_weighted_non_data_terms",
            "_non_data_terms",
            "_compose_loss_terms",
            "_bin_mean_residuals",
            "sample_collocation_points",
            "RunController",
            "PlateauDetector",
            "StageDisposition",
            "invariant",
            "load_frozen_r_ref_artifact",
            "r_ref_stage0",
        )
        for name in forbidden:
            with self.subTest(name=name):
                self.assertIsNone(re.search(rf"\b{re.escape(name)}\b", executable), name)

    def test_the_module_reads_no_file(self):
        executable = executable_source_from_text(Path(L.__file__).read_text(encoding="utf-8"))
        for token in ("open(", "Path(", "json.", "torch.load"):
            with self.subTest(token=token):
                self.assertNotIn(token, executable)


if __name__ == "__main__":
    unittest.main()
