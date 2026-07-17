"""Phase 40 / TRAIN-06 — dual-path stage-exit decision machine (CURR-03).

Transcribes ``ctl_instruction.md`` Stage Transition Criteria (~1924-1998):

* ``StageDisposition`` has exactly THREE members — ADVANCE, RECOVER, HALT —
  per line 1928 ("three dispositions"). A fourth CONTINUE is ruled out
  (GAP-40-01 → B, RESOLVED-WITH-INSTRUCTION 2026-07-17).
* Mid-flight "no exit decision" is ``StageExitOutcome.disposition is None``.
* ADVANCE is the conjunction of four criteria; NaN/Inf → RECOVER first;
  max-epoch without the gate → HALT; never fall through to ADVANCE.

Criterion 1's β-EMA + patience counter lives in ``TotalLossPlateauSmoother``
(a separately constructible mechanism, distinct from the TRAIN-02 handoff
detector that lands in 40-05). Thresholds are read from an injected
duck-typed config surface — never hardcoded here — so the machine implements
the gate FORM, not a calibrated pass level (CTX-38 provisional).

Pinned signature (40-05 call site):
    evaluate(train_loss_history, val_loss_history, val_phys, val_energy,
             had_nan_inf, epoch_count) -> StageExitOutcome
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Optional, Sequence


class StageDisposition(Enum):
    """Three exit dispositions — ctl_instruction.md:1928. Do not add CONTINUE."""

    ADVANCE = "ADVANCE"
    RECOVER = "RECOVER"
    HALT = "HALT"


@dataclass(frozen=True)
class StageExitOutcome:
    """Result of one stage-exit poll.

    ``disposition is None`` means mid-flight / keep training
    (GAP-40-01 → B). The three enum members are the only exit decisions.
    Per-criterion diagnostics let callers log which gate clause failed.
    """

    disposition: Optional[StageDisposition]
    train_plateau: bool
    val_stable: bool
    phys_ok: bool
    energy_ok: bool


class TotalLossPlateauSmoother:
    """CURR-03 criterion 1: β-EMA of total train loss + patience counter.

    ``L_smooth(i) = β · L_smooth(i-1) + (1-β) · L_train,total(i)`` with
    ``L_smooth(0)`` initialized to the first supplied loss. Plateau fires when
    the relative change over ``patience`` steps is strictly below
    ``eps_plateau``:

        |L_smooth(i) - L_smooth(i - patience)| / L_smooth(i) < eps_plateau

    Distinct from the TRAIN-02 handoff PlateauDetector (40-05) — separate
    object, separate state, no shared smoothing.
    """

    def __init__(self, beta: float, patience: int, eps_plateau: float) -> None:
        if not (0.0 < float(beta) < 1.0):
            raise ValueError(f"beta must be in (0, 1), got {beta!r}")
        if not isinstance(patience, int) or patience < 1:
            raise ValueError(f"patience must be a positive int, got {patience!r}")
        if not (float(eps_plateau) > 0.0):
            raise ValueError(f"eps_plateau must be positive, got {eps_plateau!r}")
        self._beta = float(beta)
        self._patience = int(patience)
        self._eps = float(eps_plateau)
        self._l_smooth: Optional[float] = None
        self._history: list[float] = []
        self._plateau = False

    @property
    def l_smooth(self) -> Optional[float]:
        return self._l_smooth

    @property
    def plateau(self) -> bool:
        return self._plateau

    def reset(self) -> None:
        self._l_smooth = None
        self._history = []
        self._plateau = False

    def update(self, loss: float) -> bool:
        """Ingest one raw train-loss scalar; return whether plateau currently fires."""
        x = float(loss)
        if self._l_smooth is None:
            self._l_smooth = x
        else:
            self._l_smooth = self._beta * self._l_smooth + (1.0 - self._beta) * x
        self._history.append(self._l_smooth)
        self._plateau = self._evaluate_plateau()
        return self._plateau

    def feed(self, history: Sequence[float]) -> bool:
        """Reset and ingest a full raw history; return final plateau state."""
        self.reset()
        for v in history:
            self.update(v)
        return self._plateau

    def _evaluate_plateau(self) -> bool:
        i = len(self._history) - 1
        p = self._patience
        if i < p:
            return False
        cur = self._history[i]
        past = self._history[i - p]
        # Guard zero / near-zero current EMA: treat as non-firing rather than
        # divide-by-zero (a zero loss with nonzero past is not a "plateau").
        if cur == 0.0:
            return past == 0.0
        rel = abs(cur - past) / abs(cur)
        return rel < self._eps


class StageExitMachine:
    """Four-criterion ADVANCE gate + RECOVER / HALT routing.

    Config is duck-typed: any object exposing ``beta``, ``patience``,
    ``eps_plateau``, ``eps_phys``, ``eps_energy``, ``max_epochs`` (and
    optionally ``stagnation_window``, ``energy_floor``) works. Task 2's
    ``TrainingConfig`` exposes the same names as top-level properties so
    40-05 can inject the real config without paraphrase drift.
    """

    def __init__(self, config) -> None:
        self._cfg = config

    def evaluate(
        self,
        train_loss_history: Sequence[float],
        val_loss_history: Sequence[float],
        val_phys: float,
        val_energy: float,
        had_nan_inf: bool,
        epoch_count: int,
    ) -> StageExitOutcome:
        """Pinned signature — 40-05 calls this verbatim.

        Criterion 1's β-smoothing is computed INSIDE from the RAW
        ``train_loss_history``; callers never pass a pre-smoothed signal.
        """
        # 1) NaN/Inf → RECOVER first (CTX-41), regardless of optimizer phase.
        if had_nan_inf:
            return StageExitOutcome(
                disposition=StageDisposition.RECOVER,
                train_plateau=False,
                val_stable=False,
                phys_ok=False,
                energy_ok=False,
            )

        cfg = self._cfg
        smoother = TotalLossPlateauSmoother(
            beta=cfg.beta,
            patience=cfg.patience,
            eps_plateau=cfg.eps_plateau,
        )
        train_plateau = smoother.feed(train_loss_history) if train_loss_history else False
        val_stable = self._val_stable(val_loss_history)
        phys_ok = float(val_phys) < float(cfg.eps_phys)
        energy_ok = float(val_energy) < float(cfg.eps_energy)

        if train_plateau and val_stable and phys_ok and energy_ok:
            return StageExitOutcome(
                disposition=StageDisposition.ADVANCE,
                train_plateau=True,
                val_stable=True,
                phys_ok=True,
                energy_ok=True,
            )

        # Max-epoch without the gate → HALT (no fallback ADVANCE).
        if int(epoch_count) >= int(cfg.max_epochs):
            return StageExitOutcome(
                disposition=StageDisposition.HALT,
                train_plateau=train_plateau,
                val_stable=val_stable,
                phys_ok=phys_ok,
                energy_ok=energy_ok,
            )

        # Optional stagnation HALT: val not at min for a full stagnation window.
        stag = getattr(cfg, "stagnation_window", None)
        if (
            stag is not None
            and int(stag) > 0
            and len(val_loss_history) >= int(stag)
            and not val_stable
        ):
            # If the recent window never recovers the running min, halt.
            window = list(val_loss_history)[-int(stag) :]
            running_min = min(val_loss_history)
            if all(v > running_min for v in window):
                return StageExitOutcome(
                    disposition=StageDisposition.HALT,
                    train_plateau=train_plateau,
                    val_stable=val_stable,
                    phys_ok=phys_ok,
                    energy_ok=energy_ok,
                )

        # Mid-flight: no exit decision (GAP-40-01 → B).
        return StageExitOutcome(
            disposition=None,
            train_plateau=train_plateau,
            val_stable=val_stable,
            phys_ok=phys_ok,
            energy_ok=energy_ok,
        )

    @staticmethod
    def _val_stable(val_loss_history: Sequence[float]) -> bool:
        """Criterion 2: L_val(i) ≤ min_{j≤i} L_val(j)."""
        if not val_loss_history:
            return False
        cur = float(val_loss_history[-1])
        return cur <= min(float(v) for v in val_loss_history)
