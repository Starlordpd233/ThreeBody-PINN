"""Phase 37 / ENV-04 — the narrow precision/device runtime seam.

CTX-12..CTX-14 contract:
    * One immutable resolver accepts exactly two explicit profile pairs:
      ``float32`` + ``mps`` and ``float64`` + ``cpu``.
    * Both arguments are mandatory; the resolver does NOT inspect availability,
      infer a device, catch/retry on CPU, call ``torch.set_default_dtype``,
      encode a production configuration default, or carry Phase 38 abstractions
      (model/data/loss/training policy).
    * Downstream code receives the resolved dtype/device and passes them
      explicitly into tensor, model, and AD construction.

The fp64-CPU arm is the in-framework escape hatch (D1-p round mandate). Every
ratified pick holds identically under both branches because both branches run
the same downstream code path, differing only in the resolved profile values.
"""

from dataclasses import dataclass

import torch


@dataclass(frozen=True)
class RuntimeSpec:
    """An immutable resolved precision + device specification.

    Attributes:
        precision: the requested precision label (``"float32"`` or ``"float64"``).
        requested_device: the requested device label (``"mps"`` or ``"cpu"``).
        dtype: the Torch dtype for this profile (``torch.float32`` / ``torch.float64``).
        torch_device: the resolved ``torch.device`` (recorded as-is from the
            requested label; no availability inference per CTX-12).
    """

    precision: str
    requested_device: str
    dtype: torch.dtype
    torch_device: torch.device


# The exact two permitted profile pairs. No other combination resolves; the
# cross-pairs (float64/mps and float32/cpu) are explicitly unsupported and the
# resolver names the two allowed pairs in its error so the caller can recover.
_ALLOWED_PROFILES = {
    ("float32", "mps"): lambda: RuntimeSpec(
        precision="float32",
        requested_device="mps",
        dtype=torch.float32,
        torch_device=torch.device("mps"),
    ),
    ("float64", "cpu"): lambda: RuntimeSpec(
        precision="float64",
        requested_device="cpu",
        dtype=torch.float64,
        torch_device=torch.device("cpu"),
    ),
}

_ALLOWED_PAIR_DESCRIPTION = (
    "the two permitted (precision, device) pairs are "
    "('float32', 'mps') and ('float64', 'cpu')"
)


def resolve_runtime(precision, device):
    """Resolve an explicit (precision, device) profile to an immutable RuntimeSpec.

    Both arguments are mandatory. Only the two approved profile pairs resolve;
    every other input (omitted, partial, unknown, ``float64``/``mps``,
    ``float32``/``cpu``) raises ``ValueError`` BEFORE tensor construction so the
    caller cannot accidentally build a tensor on an unintended runtime.

    Per CTX-12..CTX-14 this function does NOT:
      * inspect ``torch.backends.mps.is_available()`` or any availability probe,
      * infer a device or fall back to CPU on a mismatch,
      * retry on a different pair,
      * call ``torch.set_default_dtype`` or otherwise mutate global state,
      * encode a production configuration default.

    Returns:
        RuntimeSpec: the frozen, explicit precision + dtype + requested/resolved
        device for the requested profile.
    """
    if precision is None or device is None:
        raise ValueError(
            f"resolve_runtime requires both precision and device; got "
            f"precision={precision!r}, device={device!r}. {_ALLOWED_PAIR_DESCRIPTION}"
        )
    factory = _ALLOWED_PROFILES.get((precision, device))
    if factory is None:
        raise ValueError(
            f"unsupported (precision, device) pair "
            f"({precision!r}, {device!r}); {_ALLOWED_PAIR_DESCRIPTION}."
        )
    return factory()
