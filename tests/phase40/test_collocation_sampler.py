"""Phase 40 — CollocationSampler interface contract (TRAIN-04).

Uniform + adaptive (model, last_residuals) hook, caller-owned-RNG discipline.
The adaptive *density algorithm* is deferred (PLAT-05); this contract locks
only the call surface ((model, last_residuals) signature), the exact-N return,
and the [0, T_CHARACTERISTIC_TIME] bounds — not the internal point distribution.
"""
from __future__ import annotations

import unittest
from types import SimpleNamespace
from unittest import mock

import numpy as np
import torch

from tests.phase40 import _SKIP_PHRASE
from tests.phase40.test_prohibitions import _require

MODULE = "pinn.training.collocation_sampler"

CollocationSampler = _require("CollocationSampler", MODULE)


def _rng(seed: int = 0) -> np.random.Generator:
    return np.random.default_rng(seed)


def _stub_model() -> object:
    return SimpleNamespace(parameters=lambda: [])


def _spy_hook():
    calls = []

    def hook(model, last_residuals):
        calls.append((model, last_residuals))

    return hook, calls


class CollocationSamplerConstructionTests(unittest.TestCase):
    def test_budget_stored(self):
        sampler = CollocationSampler(collocation_count=1024, rng=_rng(0))
        self.assertEqual(sampler.collocation_count, 1024)


class UniformTests(unittest.TestCase):
    def setUp(self):
        self.sampler = CollocationSampler(collocation_count=256, rng=_rng(7))

    def test_uniform_returns_exactly_N_points(self):
        points = self.sampler.uniform(256)
        self.assertEqual(len(points), 256)

    def test_uniform_respects_requested_budget(self):
        for n in (1, 16, 1024):
            with self.subTest(n=n):
                s = CollocationSampler(collocation_count=n, rng=_rng(n))
                points = s.uniform(n)
                self.assertEqual(len(points), n)

    def test_uniform_all_points_within_bounds(self):
        from pinn.constants import T_CHARACTERISTIC_TIME

        points = self.sampler.uniform(256)
        arr = np.asarray(points)
        self.assertGreaterEqual(float(np.min(arr)), 0.0)
        self.assertLessEqual(float(np.max(arr)), T_CHARACTERISTIC_TIME)

    def test_uniform_zero_budget_returns_empty(self):
        points = self.sampler.uniform(0)
        self.assertEqual(len(points), 0)

    def test_uniform_negative_budget_raises(self):
        with self.assertRaises(ValueError):
            self.sampler.uniform(-1)

    def test_uniform_non_generator_rng_raises_type_error(self):
        sampler = CollocationSampler(collocation_count=8, rng="not-a-generator")
        with self.assertRaises(TypeError):
            sampler.uniform(8)

    def test_uniform_does_not_perturb_global_numpy_rng(self):
        np.random.seed(321)
        before = np.random.get_state()
        self.sampler.uniform(256)
        after = np.random.get_state()
        self.assertEqual(before[0], after[0])
        self.assertTrue(np.array_equal(before[1], after[1]))
        self.assertEqual(before[2:], after[2:])

    def test_uniform_seed_stable(self):
        a = CollocationSampler(collocation_count=64, rng=_rng(42)).uniform(64)
        b = CollocationSampler(collocation_count=64, rng=_rng(42)).uniform(64)
        np.testing.assert_array_equal(np.asarray(a), np.asarray(b))


class AdaptiveTests(unittest.TestCase):
    def setUp(self):
        self.sampler = CollocationSampler(collocation_count=256, rng=_rng(3))
        self.model = _stub_model()
        self.last_residuals = torch.zeros(32, 3, 3, dtype=torch.float64)

    def test_adaptive_returns_exactly_N_points(self):
        hook, calls = _spy_hook()
        points = self.sampler.adaptive(256, self.model, self.last_residuals, hook=hook)
        self.assertEqual(len(points), 256)

    def test_adaptive_respects_requested_budget(self):
        hook, _ = _spy_hook()
        for n in (1, 17, 512):
            with self.subTest(n=n):
                s = CollocationSampler(collocation_count=n, rng=_rng(n))
                points = s.adaptive(n, self.model, self.last_residuals, hook=hook)
                self.assertEqual(len(points), n)

    def test_adaptive_all_points_within_bounds(self):
        from pinn.constants import T_CHARACTERISTIC_TIME

        hook, _ = _spy_hook()
        points = self.sampler.adaptive(256, self.model, self.last_residuals, hook=hook)
        arr = np.asarray(points)
        self.assertGreaterEqual(float(np.min(arr)), 0.0)
        self.assertLessEqual(float(np.max(arr)), T_CHARACTERISTIC_TIME)

    def test_adaptive_invokes_hook_with_model_and_last_residuals(self):
        hook, calls = _spy_hook()
        self.sampler.adaptive(256, self.model, self.last_residuals, hook=hook)
        self.assertEqual(len(calls), 1)
        called_model, called_residuals = calls[0]
        self.assertIs(called_model, self.model)
        self.assertIs(called_residuals, self.last_residuals)

    def test_adaptive_non_generator_rng_raises_type_error(self):
        hook, _ = _spy_hook()
        sampler = CollocationSampler(collocation_count=8, rng=None)
        with self.assertRaises(TypeError):
            sampler.adaptive(8, self.model, self.last_residuals, hook=hook)


if __name__ == "__main__":
    unittest.main()
