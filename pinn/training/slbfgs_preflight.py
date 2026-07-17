"""Phase 40 — sL-BFGS preflight typed refusal (TRAIN-07).

The ctl_instruction.md curriculum routes stages 3-6 to stochastic L-BFGS,
which has no implementation in the v2.0 slice (deferred PLAT-02). Rather than
silently skipping or no-op'ing those stages — which would deviate from the
locked spec with no signal — this module raises a typed, self-describing
refusal before any stage >= 3 is ever entered.

``CurriculumController`` (40-06) calls ``check_stage_preflight(k)`` before
entering any stage k; the typed refusal makes a missing sL-BFGS implementation
a loud ImportError-free failure, never a silent science deviation
(SPEC Prohibition 2).

Stages 0, 1, 2 are the Adam-only slice and pass the gate unconditionally.
"""
from __future__ import annotations


class StochasticLBFGSNotImplemented(Exception):
    """Typed refusal: stages >= 3 require stochastic L-BFGS (stages 3-6),
    which has no implementation in this build (deferred PLAT-02).

    Carries the refused ``stage`` so the caller can report which curriculum
    stage triggered the gate, mirroring the typed-sentinel_EXCEPTION pattern
    from ``pinn/data/types.py`` (``StageZeroUnderpopulated`` /
    ``DataVersionHashMismatch``).
    """

    def __init__(self, stage: int) -> None:
        self.stage = stage
        super().__init__(
            f"stage {stage} requires stochastic L-BFGS (stages 3-6), which has "
            f"no implementation in this build (deferred PLAT-02); refusing "
            f"rather than silently deviating from the spec"
        )


def check_stage_preflight(stage: int) -> None:
    """Gate invoked before entering a curriculum stage.

    * stages {0, 1, 2}: returns ``None`` (Adam-only slice, proceed).
    * stages >= 3: raises ``StochasticLBFGSNotImplemented`` (typed stop,
      never a silent skip).

    Args:
        stage: the curriculum stage index about to be entered.
    """
    if stage >= 3:
        raise StochasticLBFGSNotImplemented(stage)
