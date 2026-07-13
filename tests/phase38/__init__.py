"""Phase 38 PINN model rebuild test suite (FUT-01 / NET-01..05).

Wave 1 of Phase 38 (pinn-model-rebuild-from-specs-fut-01) builds the
spec-derived foundation modules — locked science constants and the frozen
ArchitectureSpec dataclass — before any network, residual, loss, or probe
lands in later waves.

The modules in this package mirror Phase 37's stdlib-unittest style and
deferred-import skip guards: tests that target later-wave production modules
keep those imports inside test methods so compilation is the only green
precondition before the target lands; the full suites turn green only as the
later waves land.
"""
