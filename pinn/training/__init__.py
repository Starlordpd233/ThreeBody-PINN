"""Phase 40 training-driver layer (v2.0 BUILD milestone, FUT-04).

This package owns the CTL-PINN stage-0 curriculum training loop: the
``RunController`` that steps through stages, the ``TrainingConfig`` that pins
the topology/precision contract, the ``GradClipper`` that enforces the
single-mechanism non-finite contract, the ``StageExitMachine`` (TRAIN-06), and
the supporting collocation/optimizer/checkpoint plumbing.

Importing this package performs NO model build and NO dataset discovery:
submodules are loaded on demand, so ``import pinn.training`` is side-effect-free
and safe at the top of any module. The full barrel re-export of production
symbols is added by plan 40-06; until then ``__all__`` is empty.
"""

__all__ = []
