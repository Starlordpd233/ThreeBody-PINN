"""Phase 57 — Corrected Re-Run & the Preserved Evaluation test suite.

Plan 57-01 (Wave 0) lands the complete, focused, dataset-free and
held-out-free stdlib-``unittest`` contract for the bounded GAP-57-01
amended-recipe conformance patch BEFORE any production code changes. Every
test here drives a real production seam (``pinn.data.batches``,
``pinn.loss_catalog``, ``pinn.training.controllers.RunController``,
``pinn.training.guards``, ``pinn.verification.gate04_train_free``,
``pinn.evaluate``) rather than a parallel test-only reimplementation, per
57-RESEARCH.md's "Architectural Responsibility Map" and "Component and
Symbol Map". The suite is deliberately RED: it fails only because the
ratified §3.2 allocation/normalization/monitor/L-BFGS/gate/evaluation
contracts (57-CONTEXT.md D-01..D-20; 57-RULING.md) are not yet implemented
-- never because of an import, syntax, fixture, data, or environment error.

Modules:

* ``_fixtures.py`` -- deterministic CPU/float64 synthetic populations and
  real-collaborator builders (no ``simulation_data/`` access, no held-out
  split ever constructed).
* ``test_recipe_production_path.py`` -- Task 1/2: the controller-level
  allocation, all-slot physics, and normalized-loss production path.
* ``test_runtime_freeze.py`` -- Task 2/3: the frozen training-only
  invariant-B monitor, the L-BFGS segment freeze, and the immutable
  Checkpoint-③ config band.
* ``test_gate_and_evaluation.py`` -- Task 2/3: the exact GATE-04 ruling,
  the EVAL-02 canonical-frame boundary, structural candidate selection, and
  run-failure classification.

Runnable ONLY under the ``pinn-train`` conda env's stdlib ``unittest``
(D-18 -- no ``pytest`` in that env)::

    <home>/miniforge3/bin/conda run -n pinn-train \\
        python -m unittest discover -s tests/phase57 -p 'test_*.py' -v
"""
