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
"""

from __future__ import annotations

import dataclasses
import tempfile
import unittest

import numpy as np
import torch

from pinn.constants import T_CHARACTERISTIC_TIME
from pinn.loss_catalog import LossWeights
from pinn.verification.learnability_losses import (
    make_trajectory,
    physics_adam_step,
    physics_pass1,
)
from tests.phase57._fixtures import build_run_controller, make_full_slot_source

RTOL = 1e-10
ATOL = 1e-12
MICROBATCH = 256
N_ROWS = 400
TIMES_SEED = 11
TERMS = ("data", "ic", "phys", "energy", "angmom", "total")


def _clear_grads(parameters):
    for parameter in parameters:
        parameter.grad = None


def _snapshot_grads(parameters):
    return [None if p.grad is None else p.grad.detach().clone() for p in parameters]


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


if __name__ == "__main__":
    unittest.main()
