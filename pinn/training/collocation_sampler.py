"""Phase 40 — collocation-point sampler for the physics-loss interior (TRAIN-04).

``CollocationSampler`` draws interior collocation times in
``[0, T_CHARACTERISTIC_TIME]`` (T = 10.0, sourced from ``pinn.constants`` —
the literal is never hard-coded here). Two modes:

* ``uniform(N)`` — i.i.d. ``rng.uniform(0, T, size=N)``. Reuses the
  ``rng.uniform(0.0, T_CHARACTERISTIC_TIME, size=...)`` idiom from
  ``pinn/data/batches.sample_collocation_points``.
* ``adaptive(N, model, last_residuals, hook=...)`` — invokes the stateful
  ``(model, last_residuals)`` hook (D5-b / LOOP-03) and returns N in-bounds
  points. The *adaptive density algorithm* (how the hook's residual information
  shapes the point distribution) is deferred to PLAT-05; this module locks only
  the call surface — the ``(model, last_residuals)`` signature, the exact-N
  return, and the ``[0, T]`` bounds — not the internal density strategy.

Caller-owned-RNG discipline (mirrors ``pinn/data/batches._require_local_rng``):
the rng argument must be a ``numpy.random.Generator``; anything else raises
``TypeError``. The global numpy/torch RNG state is never touched.

Batch-axis contract: the returned points are shaped for consumption by
``pinn/physics_residual`` (``N_t`` is the leading batch axis). This module
returns a 1-D ``(N,)`` array of times; the caller broadcasts them to the
``(N_t,)`` u leaf that physics_residual expects.
"""
from __future__ import annotations

from typing import Any, Callable, Optional

import numpy as np

from pinn.constants import T_CHARACTERISTIC_TIME


def _require_local_rng(rng: Any) -> np.random.Generator:
    """Require a caller-owned ``numpy.random.Generator``; reject everything
    else with ``TypeError`` (never fall back to the global RNG)."""
    if not isinstance(rng, np.random.Generator):
        raise TypeError(
            "rng must be a caller-owned numpy.random.Generator; "
            f"got {type(rng).__name__}"
        )
    return rng


# The adaptive hook signature: ``(model, last_residuals) -> collocation_times``.
# The deferred PLAT-05 density strategy lives inside the hook; this module only
# enforces the surface contract (signature, count, bounds).
AdaptiveHook = Callable[[Any, Any], Any]


class CollocationSampler:
    """Draws interior physics-loss collocation times in ``[0, T]``.

    Args:
        collocation_count: default budget N used when a caller passes no
            explicit count. Stored verbatim as ``self.collocation_count``.
        rng: caller-owned ``numpy.random.Generator`` threaded through every
            sample site. No global-default mutation, no ``torch.Generator``
            fallback, no ``is_available`` probe.
    """

    def __init__(
        self,
        collocation_count: int,
        rng: np.random.Generator,
    ) -> None:
        self.collocation_count = collocation_count
        # Stored raw; validated at call time so a non-Generator surfaces as a
        # TypeError on uniform()/adaptive() (matching the batches.py idiom,
        # where _require_local_rng runs inside sample_collocation_points).
        self._rng = rng

    def uniform(self, n: Optional[int] = None) -> np.ndarray:
        """Return exactly ``n`` (default ``collocation_count``) i.i.d. uniform
        interior times in ``[0, T_CHARACTERISTIC_TIME]``.

        Validate-validate-sample-validate ordering (mirrors
        ``sample_collocation_points``): rng → count → draw → count assertion.
        """
        rng = _require_local_rng(self._rng)
        n = self.collocation_count if n is None else n
        if n < 0:
            raise ValueError("collocation_count must be non-negative")
        if n == 0:
            return np.empty((0,), dtype=np.float64)
        points = rng.uniform(0.0, T_CHARACTERISTIC_TIME, size=n)
        if points.size != n:
            raise AssertionError(
                f"uniform sample cardinality mismatch: expected {n}, got {points.size}"
            )
        return points

    def adaptive(
        self,
        n: Optional[int] = None,
        model: Any = None,
        last_residuals: Any = None,
        *,
        hook: Optional[AdaptiveHook] = None,
    ) -> np.ndarray:
        """Return exactly ``n`` in-bounds interior times via the stateful
        ``(model, last_residuals)`` adaptive hook.

        The adaptive *density algorithm* is intentionally open (deferred
        PLAT-05, RESEARCH A4). The locked contract this method enforces:

        * the hook is invoked exactly once with the two-argument
          ``(model, last_residuals)`` signature,
        * the return has exactly ``n`` entries,
        * every entry lies in ``[0, T_CHARACTERISTIC_TIME]``.

        A default uniform-with-hook-invoked fallback is used when no hook is
        supplied, so the count/bounds guarantees hold regardless of whether the
        density strategy has been implemented.
        """
        rng = _require_local_rng(self._rng)
        n = self.collocation_count if n is None else n
        if n < 0:
            raise ValueError("collocation_count must be non-negative")

        # The (model, last_residuals) hook invocation is the locked call
        # surface (D5-b / LOOP-03). The adaptive *density algorithm* — how the
        # hook's residual information shapes the point distribution — is
        # deferred to PLAT-05 (RESEARCH A4). For now the hook is invoked purely
        # as a side-effect observation seam (so 40-05/40-06 can wire the
        # signature), and the sampler itself produces a uniform fallback that
        # satisfies the exact-N / in-bounds contract regardless of whether a
        # density strategy has been implemented.
        if hook is not None:
            hook(model, last_residuals)
        points = rng.uniform(0.0, T_CHARACTERISTIC_TIME, size=n)

        if points.size != n:
            raise AssertionError(
                f"adaptive sample cardinality mismatch: expected {n}, got {points.size}"
            )
        if points.size > 0:
            if float(np.min(points)) < 0.0 or float(np.max(points)) > T_CHARACTERISTIC_TIME:
                raise AssertionError(
                    f"adaptive sample out of [0, {T_CHARACTERISTIC_TIME}] bounds"
                )
        return points
