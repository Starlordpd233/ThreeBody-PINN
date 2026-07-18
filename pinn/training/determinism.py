"""Phase 41 / CTRL-08 — four-stream RNG capture/restore + strict-CPU + honesty.

Exact checkpoint continuation restores the four RNG streams recorded at
checkpoint time (torch, torch.mps, numpy Generator.bit_generator.state,
python random). Restoring is NOT reseeding: a fresh ``default_rng(seed)``
restart is a statistically-equivalent restart, the anti-pattern this module
distinguishes from exact continuation (CTX-62).

``apply_strict_cpu_determinism(seed)`` is the CTX-63 DEBUG switch (default OFF
in ``RunConfig.strict_cpu_determinism``). It RETURNS a ``RuntimeSpec``
(dtype=float64, device=cpu) via the existing ``resolve_runtime("float64","cpu")``
escape hatch so ``pinn.train`` (41-05) can hand the forced spec to
``build_network`` — OVERRIDING config.run.precision/device (HIGH 4 fix).

Reproducibility honesty (CTX-64): the module exposes a single source-of-truth
scope string stating statistical-equivalence + exact-checkpoint-continuation,
explicitly NEVER bitwise. 41-05's run reporting emits this string.
"""

from __future__ import annotations

import random
from typing import Any, Mapping, MutableMapping, Optional

# Documented stream key order — capture and restore iterate in this sequence.
# Consumers (checkpoint payload composition, tests) rely on these names.
RNG_STREAM_KEYS: tuple[str, ...] = (
    "torch",
    "torch_mps",
    "numpy",
    "python_random",
)

# CTX-64 honesty layer — single source of truth for run reporting (41-05).
# MUST state statistical-equivalence + exact-checkpoint-continuation.
# MUST NOT claim bitwise reproducibility.
REPRODUCIBILITY_SCOPE: str = (
    "statistical-equivalence across fresh same-seed runs; "
    "exact-checkpoint-continuation on resume "
    "(does not claim bit-identical results across machines, torch versions, "
    "or devices)"
)


def reproducibility_scope() -> str:
    """Return the run's reproducibility-scope honesty statement (CTX-64)."""
    return REPRODUCIBILITY_SCOPE


def capture_rng_state(rng: Any) -> dict[str, Any]:
    """Capture the four RNG streams into a plain dict (CTX-62 / Edge R8).

    Streams, in documented order:
      * ``torch``         — ``torch.get_rng_state()``
      * ``torch_mps``     — ``torch.mps.get_rng_state()`` when MPS is available;
                            otherwise ``None``
      * ``numpy``         — ``rng.bit_generator.state`` off the INJECTED numpy
                            Generator (``RunController._rng``), NEVER the legacy
                            global ``np.random.get_state()``
      * ``python_random`` — ``random.getstate()``

    The returned dict is a plain container of tensors / containers / scalars /
    tuples that round-trips clean under ``torch.save`` /
    ``torch.load(weights_only=True)`` (RESEARCH-verified this session).
    """
    import torch  # lazy: keep module import torch-free for light consumers

    state: dict[str, Any] = {}
    state["torch"] = torch.get_rng_state()
    state["torch_mps"] = _capture_mps_rng_state(torch)
    # Injected Generator only — never np.random.get_state().
    if not hasattr(rng, "bit_generator"):
        raise TypeError(
            "capture_rng_state expects a numpy Generator with bit_generator "
            f"(got {type(rng)!r}); pass RunController._rng, not the legacy global"
        )
    state["numpy"] = rng.bit_generator.state
    state["python_random"] = random.getstate()
    return state


def restore_rng_state(state: Mapping[str, Any], rng: Any) -> None:
    """Restore the four RNG streams from a captured dict (exact continuation).

    RESTORES ``bit_generator.state`` on the injected Generator — does NOT
    reseed / construct a fresh ``default_rng(seed)`` (that is the
    statistically-equivalent-restart anti-pattern CTRL-08 distinguishes).
    """
    import torch  # lazy

    if not hasattr(rng, "bit_generator"):
        raise TypeError(
            "restore_rng_state expects a numpy Generator with bit_generator "
            f"(got {type(rng)!r}); pass RunController._rng, not the legacy global"
        )

    if "torch" in state and state["torch"] is not None:
        torch.set_rng_state(state["torch"])
    if "torch_mps" in state and state["torch_mps"] is not None:
        _restore_mps_rng_state(torch, state["torch_mps"])
    if "numpy" in state and state["numpy"] is not None:
        # Exact continuation: assign state, never reseed.
        rng.bit_generator.state = state["numpy"]
    if "python_random" in state and state["python_random"] is not None:
        # torch.save may convert nested tuples to lists; random.setstate needs
        # the legacy tuple shape. Coerce defensively.
        py_state = state["python_random"]
        random.setstate(_coerce_python_random_state(py_state))


def apply_strict_cpu_determinism(seed: int) -> Any:
    """CTX-63 DEBUG switch: force float64/cpu + deterministic algos + reseed.

    RETURNS the forced ``RuntimeSpec`` (dtype=float64, device=cpu) resolved
    via ``resolve_runtime("float64", "cpu")`` — the existing escape-hatch pair,
    NOT a new code path (HIGH 4 fix). ``pinn.train`` (41-05) hands this returned
    spec to ``build_network`` INSTEAD of
    ``resolve_runtime(config.run.precision, config.run.device)`` when
    ``run.strict_cpu_determinism`` is True, so the model cannot still build on
    MPS.

    Side effects (acceptable ONLY inside this debug path):
      * ``torch.use_deterministic_algorithms(True)``
      * ``torch.set_num_threads(1)``
      * re-seed all four streams from ``seed`` (legacy globals ok here only)

    Off by default: ``RunConfig.strict_cpu_determinism`` defaults to False.
    """
    import numpy as np
    import torch

    from pinn.runtime import resolve_runtime

    if not isinstance(seed, int) or isinstance(seed, bool):
        raise TypeError(f"seed must be an int (got {seed!r})")

    # Existing escape-hatch pair — fail-closed resolve_runtime, no new path.
    spec = resolve_runtime("float64", "cpu")

    torch.use_deterministic_algorithms(True)
    torch.set_num_threads(1)

    # Re-seed all four streams from the recorded seed (debug path only).
    torch.manual_seed(int(seed))
    _seed_mps(torch, int(seed))
    np.random.seed(int(seed))  # legacy global — acceptable ONLY here
    random.seed(int(seed))

    return spec


def _capture_mps_rng_state(torch_mod: Any) -> Optional[Any]:
    """Best-effort MPS RNG capture without device-availability probes.

    Phase-40 training-module ban: no ``.is_available()`` — try the API and
    treat any failure as "stream absent" (None).
    """
    if not hasattr(torch_mod, "mps"):
        return None
    try:
        return torch_mod.mps.get_rng_state()
    except Exception:
        return None


def _restore_mps_rng_state(torch_mod: Any, mps_state: Any) -> None:
    """Best-effort MPS RNG restore without ``.is_available()`` probes."""
    if mps_state is None or not hasattr(torch_mod, "mps"):
        return
    try:
        torch_mod.mps.set_rng_state(mps_state)
    except Exception:
        # Best-effort: MPS RNG restore can fail on CPU-only hosts; exact
        # continuation of the torch/numpy/python streams still holds.
        return


def _seed_mps(torch_mod: Any, seed: int) -> None:
    """Best-effort MPS re-seed without ``.is_available()`` probes."""
    if not hasattr(torch_mod, "mps"):
        return
    try:
        torch_mod.mps.manual_seed(int(seed))
    except Exception:
        return


def _coerce_python_random_state(py_state: Any) -> Any:
    """Coerce a torch.load-possibly-listified random.getstate() back to tuples.

    ``random.setstate`` requires a 3-tuple ``(version, internal, gauss_next)``
    where ``internal`` is itself a tuple of ints. After a ``torch.save`` /
    ``torch.load(weights_only=True)`` round-trip, nested tuples may become
    lists — convert them back.
    """
    if not isinstance(py_state, (tuple, list)) or len(py_state) < 3:
        return py_state
    version, internal, gauss_next = py_state[0], py_state[1], py_state[2]
    if isinstance(internal, list):
        internal = tuple(internal)
    return (version, internal, gauss_next)


__all__ = [
    "RNG_STREAM_KEYS",
    "REPRODUCIBILITY_SCOPE",
    "apply_strict_cpu_determinism",
    "capture_rng_state",
    "restore_rng_state",
    "reproducibility_scope",
]
