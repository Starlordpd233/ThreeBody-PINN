"""Phase 37 / ENV-04 — the rebuilt ``pinn`` package marker.

v2.0 lifts the v1.3-era ``pinn/`` live-code ban (FUT-01 rebuilds from the
framework specs). Phase 37 opens the package with the narrow precision/device
runtime seam; Phase 38 adds the model modules (architecture spec, constants,
the SQR-SkipResNet-SIREN backbone, and the COM projection head).

Public surface:
    Phase 37:
        RuntimeSpec                       — frozen precision + dtype + device
        resolve_runtime(precision, device) -> RuntimeSpec
    Phase 38 (plan 01):
        ArchitectureSpec                  — frozen validated topology config
    Phase 38 (plan 02):
        SQRSkipResNetSIREN                — spec-faithful backbone (projected-only forward)
        build_network(spec, *, dtype, device) -> SQRSkipResNetSIREN

Downstream code imports the resolver and passes the resolved dtype/device
explicitly into tensor, model, and AD construction; there is no global
default-dtype mutation and no implicit device selection (CTX-12..CTX-14).
"""

from .architecture_spec import ArchitectureSpec
from .network import SQRSkipResNetSIREN, build_network
from .runtime import RuntimeSpec, resolve_runtime

__all__ = [
    "ArchitectureSpec",
    "RuntimeSpec",
    "SQRSkipResNetSIREN",
    "build_network",
    "resolve_runtime",
]
