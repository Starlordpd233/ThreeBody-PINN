"""Phase 37 / ENV-03 — the rebuilt ``pinn.verification`` package marker.

Phase 37 opens this subpackage with the single componentwise-AD worker that
both D1-p profiles (fp32-MPS and fp64-CPU) use unchanged. Second-order residual
work belongs to Phase 38 and is not present here.
"""

from . import componentwise_ad  # noqa: F401  (re-export for module-mode execution)

__all__ = ["componentwise_ad"]
