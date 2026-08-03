"""Phase 48 loss-math conformance tests.

The suite is dataset-free and train-free: it uses synthetic tensors and the
real controller/catalog seams only.  MPS-specific arms skip explicitly when
MPS is unavailable; the locked CPU/float64 arm remains the non-waivable proof.
The Phase 47 ``eps_H`` assembly oracle is retained in its owning module and is
run alongside these tests rather than duplicated here.
"""
