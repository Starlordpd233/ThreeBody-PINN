"""The ``pinn.verification`` package — probe-local verification machinery.

Phase 37 (ENV-03) opened this subpackage with the single componentwise-AD
worker that both D1-p profiles (fp32-MPS and fp64-CPU) use unchanged; it stays
the re-export below so ``python -m pinn.verification.componentwise_ad`` keeps
working.

Phase 38 (NET-03) adds the read-only, provenance-recording single-trajectory
Brutus fixture loader (``fixture_loader``) plus the verification-rung probes.
Those modules are imported ON DEMAND, not from this package ``__init__`` — the
rung modules are Torch-heavy and pull in the network, so forcing them at
package-import time would make every ``pinn.verification`` import pay for them.

Second-order (residual) physics itself lives in ``pinn.physics_residual``, not
here: this package holds verification machinery, not the science kernel.
"""

from . import componentwise_ad  # noqa: F401  (re-export for module-mode execution)

__all__ = ["componentwise_ad"]
