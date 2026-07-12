"""Phase 37 / ENV-04 — the rebuilt ``pinn`` package marker.

v2.0 lifts the v1.3-era ``pinn/`` live-code ban (FUT-01 rebuilds from the
framework specs). Phase 37 opens the package with the narrow precision/device
runtime seam only; model, data, loss, and training modules belong to Phase 38
and later and must NOT be added here.

Public surface (Phase 37):
    RuntimeSpec    — frozen, explicit precision + dtype + requested/resolved device
    resolve_runtime(precision, device) -> RuntimeSpec

These are the only names re-exported at the package level. Downstream code
imports the resolver and passes the resolved dtype/device explicitly into
tensor, model, and AD construction; there is no global default-dtype mutation
and no implicit device selection (CTX-12..CTX-14).
"""

from .runtime import RuntimeSpec, resolve_runtime

__all__ = ["RuntimeSpec", "resolve_runtime"]
