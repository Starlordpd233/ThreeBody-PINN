"""Phase 47 — Frame Completion & S_H Pipeline test suite.

Wave 1 (plan 47-01) lands the CONF-09 invariant suite: the assertions that prove
the residency swap was a PURE FRAME COMPLETION rather than a change of physics —
``IC₁₃`` invariance (47-CONTEXT.md D-04), the ``dr'/du = v_gauge`` velocity
identity (D-02), ratified-frame coherence (D-01/D-05), and approximate
gate-metric invariance within a per-trajectory DERIVED bound (D-08).

Scope discipline
----------------
Every test here is dataset-free and train-free (SCOPE-27/28): fixtures come from
``tests/phase39/_fixtures.py::TinyCorpus`` (a deterministic tiny on-disk corpus
under a ``TemporaryDirectory``) and ``tests/phase46/_fixtures.py`` (closed-form
Lagrange trajectories). No model forward pass, no training step, no
``simulation_data/`` access.

Skip discipline
---------------
There is none: this suite ships green. No test in this package is skipped or
expected-to-fail, and no ``_SKIP_PHRASE`` constant exists here — the Phase 47
production symbols all land in the same wave as the tests that exercise them.

Oracle discipline
-----------------
The RESIDENT PAIRING oracle is NOT duplicated here. It lives, corrected in
place, in ``tests/phase46/test_pairing_repair.py`` (47-CONTEXT.md D-06): two
competing oracles for one property is the failure ``46-CONTEXT.md`` warns
against. This package asserts the NEW CONF-09 invariants only.
"""
