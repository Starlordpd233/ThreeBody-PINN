"""Phase 40 / TRAIN-03 -- PHYS-05 scheduled loss-weight state machine.

Transcribes the PHYS-05 warmup / per-stage ``lambda^max`` / frozen-during-L-BFGS
/ re-warm-at-stage-boundary schedule from ``pinn_architecture.md`` §4.1 (loss
warmup block, ~lines 658-665) into a pure schedule module. ``current(epoch)``
returns the existing :class:`pinn.loss_catalog.LossWeights` container (built
for this phase); the RunController feeds it straight into
:func:`pinn.loss_catalog.compose_total` with no parallel weight type.

Contract (PHYS-05)::

    I_warm = min(2000, floor(0.1 * N_Adam,k))              # integer-floored
    lambda_phys(k, i) = lambda_phys^max(k) * min(1, i / I_warm)
    lambda_E(k, i)     = lambda_E^max(k)     * min(1, i / I_warm)
    lambda_L(k, i)     = lambda_L^max(k)     * min(1, i / I_warm)
    lambda_data = 1.0   (fixed, pinn_architecture.md §3.1 unweighted data term)
    lambda_IC   = 1.0   (default; not on the warmup ramp)
    lambda_E^max <= 1, lambda_L^max <= 1                    # PHYS-05 hard cap

State machine (D5-c / CTX-38):

- ``freeze()``  -- snapshots the ramp fraction at the most recently queried
  epoch and pins every subsequent ``current(epoch)`` to that snapshot for the
  duration of a simulated L-BFGS phase (``lambda_entry == lambda_exit`` to
  floating tolerance; the prohibition "MUST NOT update lambda during an
  L-BFGS line search" is resolved/tested as that identity).
- ``rewarm()`` -- clears the frozen state so the ramp goes live again. At a
  stage boundary the ``CurriculumController`` obtains that stage's
  ``RunController`` from the injected ``stage_factory`` (which carries the
  stage's ``ScheduledWeights`` / ``TrainingConfig`` / ``GradClipper``) and
  rebinds its own schedule reference to it; ``rewarm()`` is then the
  explicit unfreeze that guarantees the ramp restarts from 0. With no
  factory (the default) the run is single-stage and stages >= 1 are NOT
  reconfigured (PLAT-01; ``40-SPEC.md`` defers the full multi-stage
  curriculum beyond the Stage 0-2 full-batch path).

Provisional seams (CTX-38): the per-stage ``lambda^max`` caps and the warmup
horizon are PROVISIONAL, config-overridable defaults carrying PHYS-05 /
Phase-35 LOSS-02 provenance -- never cited as ratified, surfaced for ACC-05
pilot calibration. The ``lambda_E^max <= 1`` invariant is the one hard cap
(enforced at construction, fail-closed).

This module is a pure schedule -- no optimizer coupling, no tensor dtype/device
state (the values are plain python floats consumed as ``LossWeights`` fields).
``state_dict()`` / ``load_state_dict()`` serialize the schedule into a plain
dict of python scalars (CTX-44 weights_only-clean) so TRAIN-03's "schedule
state serialized into checkpoints" is met.
"""

from __future__ import annotations

import math
from typing import Any, Optional

from pinn.loss_catalog import LossWeights

__all__ = ["ScheduledWeights"]

# PHYS-05 warmup ceiling (pinn_architecture.md §4.1): I_warm = min(2000, ...).
_WARMUP_CEIL = 2000
# PHYS-05 warmup fraction of N_Adam,k.
_WARMUP_FRACTION = 0.1


class ScheduledWeights:
    """PHYS-05 warmup / lambda^max / freeze / re-warm schedule.

    Construct one instance per stage with that stage's ``N_Adam,k`` and
    per-stage ``lambda^max`` caps. ``current(epoch)`` is a pure function of
    (epoch, frozen/warmup state, config); it has no optimizer coupling.

    Parameters
    ----------
    n_adam_k:
        The stage's configured Adam epoch budget ``N_Adam,k``. Drives the
        warmup length ``I_warm = min(2000, floor(0.1 * N_Adam,k))``.
    lambda_phys_max, lambda_e_max, lambda_l_max:
        Per-stage lambda^max caps (PHYS-05). ``lambda_e_max`` and
        ``lambda_l_max`` MUST be ``<= 1.0`` (the PHYS-05 / Phase-35 LOSS-02
        hard cap); construction fails-closed otherwise. Provisional defaults
        are the Stage-0 values from the PHYS-05 table (``lambda_E^max =
        lambda_L^max = 0`` for ``k in {0, 1}``); downstream stages pass their
        own values.
    lambda_ic:
        IC anchor weight (PHYS-05 default 1.0; not on the warmup ramp).
    warmup_length:
        Optional explicit override for ``I_warm``. Defaults to
        ``min(2000, floor(0.1 * n_adam_k))`` (the PHYS-05 formula).
    """

    def __init__(
        self,
        n_adam_k: int,
        *,
        lambda_phys_max: float = 1.0,
        lambda_e_max: float = 0.0,
        lambda_l_max: float = 0.0,
        lambda_ic: float = 1.0,
        warmup_length: Optional[int] = None,
    ) -> None:
        # --- N_Adam,k / warmup length -------------------------------------
        if not isinstance(n_adam_k, int) or isinstance(n_adam_k, bool):
            raise ValueError(
                f"ScheduledWeights.n_adam_k must be an int (got {n_adam_k!r}); "
                "it is the stage's configured Adam epoch budget N_Adam,k "
                "(PHYS-05 warmup length input)"
            )
        if n_adam_k < 0:
            raise ValueError(
                f"ScheduledWeights.n_adam_k must be non-negative "
                f"(got {n_adam_k!r})"
            )
        self._n_adam_k = n_adam_k
        if warmup_length is None:
            warmup_length = min(_WARMUP_CEIL, int(_WARMUP_FRACTION * n_adam_k))
        if not isinstance(warmup_length, int) or isinstance(warmup_length, bool):
            raise ValueError(
                f"ScheduledWeights.warmup_length must be an int (got "
                f"{warmup_length!r}); I_warm = min(2000, floor(0.1*N_Adam,k)) "
                "(PHYS-05)"
            )
        if warmup_length < 0:
            raise ValueError(
                f"ScheduledWeights.warmup_length must be non-negative "
                f"(got {warmup_length!r})"
            )
        self._warmup_length = warmup_length

        # --- lambda^max caps (PHYS-05; lambda_E^max <= 1 hard cap) --------
        self._lambda_phys_max = self._validate_max(
            "lambda_phys_max", lambda_phys_max)
        self._lambda_e_max = self._validate_max(
            "lambda_e_max", lambda_e_max, enforce_le_one=True)
        self._lambda_l_max = self._validate_max(
            "lambda_l_max", lambda_l_max, enforce_le_one=True)
        self._lambda_ic = self._validate_max("lambda_ic", lambda_ic)

        # --- Stateful ramp / freeze --------------------------------------
        self._frozen: bool = False
        self._frozen_ramp: Optional[float] = None
        self._last_epoch: int = 0

    # ------------------------------------------------------------------
    # Construction-time validation
    # ------------------------------------------------------------------
    @staticmethod
    def _validate_max(name: str, value: float,
                      *, enforce_le_one: bool = False) -> float:
        try:
            v = float(value)
            finite = math.isfinite(v)
        except (TypeError, ValueError):
            finite = False
            v = float("nan")
        if not finite or v < 0.0:
            raise ValueError(
                f"ScheduledWeights.{name} must be finite and non-negative "
                f"(got {value!r}); a negative lambda silently flips the term "
                f"into gradient ascent (PHYS-05)"
            )
        if enforce_le_one and v > 1.0:
            raise ValueError(
                f"ScheduledWeights.{name} must be <= 1.0 (got {value!r}); "
                f"the PHYS-05 / Phase-35 LOSS-02 hard cap lambda_E^max <= 1 / "
                f"lambda_L^max <= 1 forbids a conservation weight above 1"
            )
        return v

    # ------------------------------------------------------------------
    # Public schedule surface
    # ------------------------------------------------------------------
    @property
    def warmup_length(self) -> int:
        """``I_warm = min(2000, floor(0.1 * N_Adam,k))`` (PHYS-05)."""
        return self._warmup_length

    @property
    def n_adam_k(self) -> int:
        """The configured Adam epoch budget for this stage."""
        return self._n_adam_k

    def _ramp_fraction(self, epoch: int) -> float:
        """``min(1, max(0, epoch) / I_warm)``; saturated at 1 when I_warm == 0."""
        if self._warmup_length <= 0:
            return 1.0
        e = int(epoch)
        if e < 0:
            e = 0
        return min(1.0, e / float(self._warmup_length))

    def current(self, epoch: int) -> LossWeights:
        """Return a fresh, already-validated :class:`LossWeights` at ``epoch``.

        Pure function of (epoch, frozen/warmup state, config). When frozen,
        every call returns the snapshot ramp's ``LossWeights`` (entry == exit
        across a simulated L-BFGS phase). Otherwise the warmup ramp scales
        ``lambda_phys`` / ``lambda_e`` / ``lambda_l`` by
        ``min(1, epoch / I_warm)``; ``lambda_data`` stays 1.0 and
        ``lambda_ic`` stays at its configured value (neither is on the ramp).
        """
        if self._frozen:
            ramp = self._frozen_ramp if self._frozen_ramp is not None else 0.0
        else:
            ramp = self._ramp_fraction(epoch)
            self._last_epoch = int(epoch)
        return LossWeights(
            lambda_data=1.0,
            lambda_ic=self._lambda_ic,
            lambda_phys=self._lambda_phys_max * ramp,
            lambda_e=self._lambda_e_max * ramp,
            lambda_l=self._lambda_l_max * ramp,
        )

    def freeze(self) -> None:
        """Pin ``current(epoch)`` to the ramp value at the last-queried epoch.

        Snapshots the current ramp fraction so every subsequent ``current()``
        call returns identical weights across a simulated L-BFGS phase
        (resolves the prohibition "MUST NOT update lambda during an L-BFGS
        line search" as entry == exit to floating tolerance). Idempotent.
        """
        self._frozen = True
        self._frozen_ramp = self._ramp_fraction(self._last_epoch)

    def rewarm(self) -> None:
        """Clear the freeze so the warmup ramp goes live again.

        At a stage boundary the ``CurriculumController`` obtains that stage's
        ``RunController`` from the injected ``stage_factory`` (carrying the
        stage's ``ScheduledWeights`` / ``TrainingConfig`` / ``GradClipper``)
        and rebinds its schedule reference; ``rewarm()`` is then the explicit
        unfreeze guaranteeing the ramp restarts from 0 on the (possibly new)
        schedule instance. With no factory (the default) the run is
        single-stage and stages >= 1 are NOT reconfigured (PLAT-01) -- only
        this unfreeze runs on the same instance. After this call, small-epoch
        ``current(epoch)`` values yield ``lambda < lambda^max`` again when
        ``I_warm > 0``.
        """
        self._frozen = False
        self._frozen_ramp = None
        self._last_epoch = 0

    # ------------------------------------------------------------------
    # Checkpoint serialization (CTX-44: plain python scalars, weights_only-clean)
    # ------------------------------------------------------------------
    def state_dict(self) -> dict[str, Any]:
        """Serialize schedule state into a plain dict of python scalars."""
        return {
            "n_adam_k": self._n_adam_k,
            "warmup_length": self._warmup_length,
            "lambda_phys_max": self._lambda_phys_max,
            "lambda_e_max": self._lambda_e_max,
            "lambda_l_max": self._lambda_l_max,
            "lambda_ic": self._lambda_ic,
            "frozen": self._frozen,
            "frozen_ramp": self._frozen_ramp,
            "last_epoch": self._last_epoch,
        }

    def load_state_dict(self, state: dict[str, Any]) -> None:
        """Restore schedule state from a ``state_dict()`` dict (round-trip)."""
        self._n_adam_k = int(state["n_adam_k"])
        self._warmup_length = int(state["warmup_length"])
        self._lambda_phys_max = float(state["lambda_phys_max"])
        self._lambda_e_max = float(state["lambda_e_max"])
        self._lambda_l_max = float(state["lambda_l_max"])
        self._lambda_ic = float(state["lambda_ic"])
        self._frozen = bool(state["frozen"])
        ramp = state["frozen_ramp"]
        self._frozen_ramp = None if ramp is None else float(ramp)
        self._last_epoch = int(state["last_epoch"])
