"""Phase 37 verification contract suite.

Wave 0 of Phase 37 (developer-environment-precision-adjudication) builds the
hermetic executable contracts for every ENV-01 through ENV-04 requirement and
CTX-01 through CTX-14 decision before any host mutation, package installation,
or empirical MPS run.

The six modules in this package are intentionally importable with host
``python3`` using only the Python standard library. Tests that target later-wave
production modules (``setup.sh``, ``scripts/verify_environment.py``,
``pinn.runtime``, ``pinn.verification.componentwise_ad``,
``scripts/run_precision_probe.py``) keep those imports inside test methods so
that ``py_compile`` is the only Wave 0 green condition; the full suites turn
green only as the later waves land.
"""
