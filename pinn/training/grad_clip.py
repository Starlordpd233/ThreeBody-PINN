"""Phase 40 / TRAIN-05 -- merged Adam-only adaptive gradient clipper.

Transcribes the ``pinn_architecture.md`` §4.4 Adaptive Gradient Clipping
contract: during Adam epochs only, the clip value is the product of the
curriculum-aware stage multiplier ``C_stage`` and the median of recent global
gradient norms over a rolling window of 100 entries. No clipping is applied
during L-BFGS (the line-search trust region already bounds the step); this
module exposes no L-BFGS / closure entry point -- it is Adam-only by
construction.

Append-then-median ordering (CTX-35 -- load-bearing, do not "fix"):
    Each step's own pre-clip gradient norm is APPENDED to the rolling window
    BEFORE the median is computed, so the current step's norm is INCLUDED in
    its own clip threshold. This is what makes the length-1 bootstrap identity
    hold (``clip == C_stage * the single norm`` at step 1). A later reader must
    not re-order to "median of the prior window" -- that would silently change
    the clip threshold every step and break the SPEC held-out partial-window
    edge.

Partial-window bootstrap (CTX-35 / SPEC held-out edge):
    The median is taken over the PARTIAL window from step 1 onward -- median
    of whatever entries currently exist. The clip is always defined and finite
    for windows with fewer than 100 entries (length 1, 2, 4, ...). At length 1,
    ``clip == C_stage * the single norm``.

Median function (Common Pitfall 1):
    ``torch.median`` is used EXCLUSIVELY -- never ``numpy.median`` or
    ``statistics.median``. ``torch.median`` of an even-length window returns
    the LOWER of the two middle values; the numpy/statistics variants AVERAGE
    the two middle values and would silently disagree on every even-length
    window. The tests build their references with ``torch.median`` the same way.

Provisional seams (CTX-34 / CTX-36 -- never cited as ratified):
    - ``C_stage`` table default ``{0-1: 8.5, 2-3: 5.0, 4-6: 3.0}``. §4.4 puts
      the Stage 0-1 value in an open 7-10 range; 8.5 is the midpoint and is
      the build's provisional default, config-overridable, surfaced for ACC-05
      pilot calibration. Stages 2-3 inherit the pre-Phase-34 fixed 5.0;
      stages 4-6 use 3.0.
    - ``median_floor`` default ``1e-6`` (§4.4 worked-example floor). Without a
      floor, a converged stage drives ``median(grad_norm) -> 0`` and
      ``clip_value -> 0``, silently annihilating every gradient. The floor
      keeps the clip finite and nonzero; ACC-05 calibrates it.
    - Window length 100 (§4.4 normative). Stage boundaries CLEAR the window
      (CTX-37): ``C_stage`` changes at boundaries and the new stage's gradient
      scale differs, so a stale median would mis-clip the new stage's first
      steps.

M1 non-finite contract (PINNED -- exactly one mechanism, no raise):
    A non-finite (NaN/Inf) pre-clip gradient norm makes ``GradClipper.clip``
    RETURN ``GradClipOutcome(non_finite=True, clip_value=None)`` with NO clip
    applied and WITHOUT RAISING. The module defines/imports NO exception type
    and never passes the torch raising kwarg ``error_if_nonfinite=True`` on
    its measure call (it passes ``False`` so the measure returns the norm
    instead of raising). The consumer (RunController, plan 40-05) inspects the
    returned flag and branches to ``StageDisposition.RECOVER``; it wraps
    nothing in ``try/except``. This contract is bound from ONE executable
    place -- ``tests/phase40/test_prohibitions.NonFiniteContractTests`` (owned
    by plan 40-01) -- which arms automatically the moment this module lands.

Window integrity (load-bearing):
    A non-finite norm is NEVER appended to the rolling window. A single NaN
    admitted into the window would make ``torch.median`` return NaN for every
    subsequent step of the stage, permanently collapsing the clip threshold --
    so the non-finite check PRECEDES the append.

The per-step operation is exposed as a SINGLE public method ``clip(params,
*, stage)`` that internally makes the two ``torch.nn.utils.clip_grad_norm_``
calls (inf-norm measure, then apply). It is the spy target plan 40-05 counts
(1 call per Adam step, 0 per L-BFGS step); the internal torch-level calls are
NOT the countable surface.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Any, Iterable, Optional

import torch

__all__ = ["GradClipper", "GradClipOutcome", "DEFAULT_C_STAGE_TABLE"]


# ---------------------------------------------------------------------------
# Provisional defaults (CTX-34 / CTX-36 / §4.4) -- config-overridable, never
# cited as ratified; surfaced for ACC-05 pilot calibration.
# ---------------------------------------------------------------------------

# §4.4 Stage 0-1 C_stage is an open 7-10 range; 8.5 is the midpoint (CTX-34).
# Stages 2-3 inherit the pre-Phase-34 fixed multiplier 5.0; stages 4-6 use 3.0.
DEFAULT_C_STAGE_TABLE = {0: 8.5, 1: 8.5, 2: 5.0, 3: 5.0, 4: 3.0, 5: 3.0, 6: 3.0}

# §4.4 worked-example lower floor on the median (CTX-36).
DEFAULT_MEDIAN_FLOOR = 1e-6

# §4.4 rolling-window length (last 100 gradient norms).
DEFAULT_WINDOW_LENGTH = 100


# ---------------------------------------------------------------------------
# Frozen result container (ConservationOutcome-style).
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class GradClipOutcome:
    """Frozen per-step clip result.

    Attributes:
        non_finite: True iff the pre-clip total norm was NaN/Inf. The signal
            for RunController's RECOVER branch; never raised.
        clip_value: The applied clip threshold (``C_stage * effective_median``),
            or ``None`` when ``non_finite`` is True (no clip applied).
        total_norm: The pre-clip total L2 norm (0-d tensor) returned by the
            measure call. May be non-finite when ``non_finite`` is True.
        window_len: Rolling-window length AFTER this step (the non-finite norm
            is never appended, so ``window_len`` is UNCHANGED across a
            non-finite call).
    """

    non_finite: bool
    clip_value: Optional[float]
    total_norm: Any  # torch.Tensor (0-d)
    window_len: int


# ---------------------------------------------------------------------------
# GradClipper
# ---------------------------------------------------------------------------

class GradClipper:
    """Adaptive median-based gradient clipper (§4.4), Adam-only.

    Owns the rolling grad-norm window, the per-stage ``C_stage`` table, and the
    median floor. Per Adam step, call ``clip(params, stage=...)``; it measures
    the pre-clip total norm, gates on finiteness, appends-and-medians, floors
    the median, applies the clip in place, and returns a frozen
    :class:`GradClipOutcome`.

    Parameters:
        c_stage_table: Per-stage ``C_stage`` multipliers (provisional default
            :data:`DEFAULT_C_STAGE_TABLE`). Config-overridable per CTX-34.
        median_floor: Lower floor on the rolling median (default ``1e-6``,
            §4.4 worked example). Config-overridable per CTX-36.
        window_length: Rolling-window size (default 100, §4.4 normative).
    """

    def __init__(
        self,
        *,
        c_stage_table: Optional[dict[int, float]] = None,
        median_floor: float = DEFAULT_MEDIAN_FLOOR,
        window_length: int = DEFAULT_WINDOW_LENGTH,
    ) -> None:
        self._c_stage_table: dict[int, float] = (
            dict(DEFAULT_C_STAGE_TABLE) if c_stage_table is None
            else self._validate_c_stage_table(c_stage_table)
        )
        if not math.isfinite(float(median_floor)) or float(median_floor) <= 0.0:
            raise ValueError(
                f"GradClipper.median_floor must be positive and finite "
                f"(got {median_floor!r}); the §4.4 floor keeps the clip "
                f"threshold from collapsing to zero (CTX-36)")
        self._median_floor = float(median_floor)
        if not isinstance(window_length, int) or isinstance(window_length, bool):
            raise ValueError(
                f"GradClipper.window_length must be an int (got "
                f"{window_length!r}); §4.4 rolling window of last 100 norms")
        if window_length <= 0:
            raise ValueError(
                f"GradClipper.window_length must be positive "
                f"(got {window_length!r})")
        self._window_length = window_length
        self._window: list[torch.Tensor] = []

    @staticmethod
    def _validate_c_stage_table(table: dict[int, float]) -> dict[int, float]:
        if not isinstance(table, dict) or not table:
            raise ValueError(
                "GradClipper.c_stage_table must be a non-empty dict "
                "{stage: C_stage} (§4.4)")
        out: dict[int, float] = {}
        for stage, c in table.items():
            if not isinstance(stage, int) or isinstance(stage, bool):
                raise ValueError(
                    f"c_stage_table stage keys must be ints (got {stage!r})")
            try:
                cf = float(c)
                ok = math.isfinite(cf)
            except (TypeError, ValueError):
                ok = False
                cf = float("nan")
            if not ok or cf <= 0.0:
                raise ValueError(
                    f"c_stage_table[{stage!r}] must be positive finite "
                    f"(got {c!r}); §4.4 C_stage is a positive multiplier")
            out[stage] = cf
        return out

    def _lookup_c_stage(self, stage: int) -> float:
        try:
            return self._c_stage_table[int(stage)]
        except KeyError:
            raise ValueError(
                f"GradClipper: stage {stage!r} not in C_stage table "
                f"(stages present: {sorted(self._c_stage_table)}); §4.4 covers "
                f"stages 0-6 -- pass c_stage_table override for other stages")

    def clip(self, params: Iterable[torch.Tensor], *, stage: int) -> GradClipOutcome:
        """Measure, gate, append-and-median, floor, and apply the §4.4 clip.

        Single public per-step entry point (Adam-only; the spy target plan
        40-05 counts). Internally makes two ``torch.nn.utils.clip_grad_norm_``
        calls: an inf-norm measure that does not raise on non-finite input,
        then the apply call at the computed clip value.
        """
        c_stage = self._lookup_c_stage(stage)

        # Step 1: measure the pre-clip total L2 norm. ``error_if_nonfinite``
        # is passed as False so a non-finite norm is RETURNED, not raised
        # (M1 contract: the signal is the returned flag, never a raise).
        total_norm = torch.nn.utils.clip_grad_norm_(
            params, max_norm=float("inf"), error_if_nonfinite=False)

        # Step 2: NON-FINITE GATE -- check BEFORE the append (window integrity:
        # a single NaN admitted would poison torch.median for the whole stage).
        if not bool(torch.isfinite(total_norm)):
            return GradClipOutcome(
                non_finite=True,
                clip_value=None,
                total_norm=total_norm,
                window_len=len(self._window),
            )

        # Step 3: APPEND the detached finite norm, then trim to the rolling
        # window. CTX-35 append-then-median: the current step's own norm is
        # part of the window its median is computed over (length-1 identity).
        self._window.append(total_norm.detach())
        if len(self._window) > self._window_length:
            overflow = len(self._window) - self._window_length
            del self._window[:overflow]

        # Step 4: clip_value = C_stage * max(median(window), median_floor).
        # torch.median ONLY (never numpy/statistics -- even-length LOWER middle).
        stacked = torch.stack(self._window)
        median = torch.median(stacked)
        effective_median = torch.clamp(median, min=self._median_floor)
        clip_value = c_stage * float(effective_median)

        # Step 5: apply the clip in place (grads already verified finite above).
        torch.nn.utils.clip_grad_norm_(
            params, max_norm=clip_value, error_if_nonfinite=False)

        return GradClipOutcome(
            non_finite=False,
            clip_value=clip_value,
            total_norm=total_norm,
            window_len=len(self._window),
        )

    def clear(self) -> None:
        """Empty the rolling window at a stage boundary (CTX-37).

        ``C_stage`` changes at boundaries and the new stage's gradient scale
        differs; a stale median would mis-clip the new stage's first steps.
        """
        self._window = []
