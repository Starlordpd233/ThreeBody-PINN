"""Phase 39 — the sole record-level Stage-0/1 classifier (GAP-39-03 / GAP-39-08).

This is the ONLY module in ``pinn/data`` permitted to own a numeric Stage-0/1
invariant predicate (mechanically enforced by
``tests/phase39/test_prohibitions.py::test_only_stages_owns_the_numeric_classifier``).
Every other module (adapter, splits, batches, stage_scan) consumes the
persisted ``stage_label`` this function returns and must never reclassify.

Authoritative membership (``ctl_instruction.md:23-28,138-198``; GAP-39-03
resolves the reversed derived-SPEC wording; GAP-39-08 carries the CTL
fidelity boundary into one production seam):

* Only ORIGINAL/BASE hierarchical Set 1a records may receive a numeric label
  (``variant == Variant.HIERARCHICAL and fidelity == Fidelity.BASE``).
* Stage 0 is evaluated BEFORE the collapsed Stage 1a/1b branch.
* Every gold record (including hierarchical Set 2a), every non-Set-1a record,
  and every degenerate-``L_max`` record (``l_ratio`` is ``None`` or non-finite,
  e.g. NaN) is ``UNASSIGNED``.
* The Stage-0/1 criterion is strict ``s_min > s0``; equality is NOT Stage 0/1
  (GAP-39-03 corrects the reversed ``39-SPEC.md`` wording).
* Stage 2-6 are NEVER returned; the only outputs are ``StageLabel.STAGE_0``,
  ``StageLabel.STAGE_1`` (the collapsed Stage 1a/1b union), and
  ``StageLabel.UNASSIGNED``.
"""

from __future__ import annotations

import math
from typing import Any

from pinn.data.types import Fidelity, StageLabel, Variant

# CTL Stage-0/1 thresholds (ctl_instruction.md:138-184). These are the
# AUTHORITATIVE conjunction values, not implementation defaults.
_E_STAGE0_MAX = -0.5          # Stage 0 / Stage 1b: E < -0.5
_E_STAGE1A_LOW = -0.5         # Stage 1a: -0.5 <= E < -0.1
_E_STAGE1A_HIGH = -0.1
_L_RATIO_STAGE0_MIN = 0.5     # Stage 0 / Stage 1a: l_ratio > 0.5
_L_RATIO_STAGE1B_LOW = 0.1    # Stage 1b: 0.1 <= l_ratio < 0.5
_L_RATIO_STAGE1B_HIGH = 0.5
_Q_LOW = 0.7                  # common: 0.7 <= Q <= 1.3
_Q_HIGH = 1.3


def _is_degenerate(l_ratio: Any) -> bool:
    """True iff ``l_ratio`` is the degenerate-``L_max`` sentinel (``None``) or
    non-finite (NaN/inf) -- both must short-circuit to UNASSIGNED before any
    numeric comparison (``None > 0.5`` / ``nan > 0.5`` are a ``TypeError``/
    silently-False trap respectively; the guard makes both explicit)."""
    if l_ratio is None:
        return True
    try:
        return not math.isfinite(l_ratio)
    except TypeError:
        return True


def classify_stage_label(record: Any, interim_s0: float = 0.01) -> StageLabel:
    """Classify one admitted record's CTL Stage-0/1 membership.

    ``record`` is attribute-based: ``variant`` (``Variant``), ``fidelity``
    (``Fidelity``), ``E``, ``l_ratio`` (angular-momentum ratio; ``None`` or
    non-finite for a degenerate ``L_max``), ``Q``, and ``s_min`` (minimal
    initial separation). ``interim_s0`` is an input seam (GAP-39-08 interim
    floor ``0.01``, pending owner ratification from the Phase-39 DATA-06 scan)
    -- this function must never mutate or "ratify" it.
    """
    if record.variant != Variant.HIERARCHICAL or record.fidelity != Fidelity.BASE:
        return StageLabel.UNASSIGNED

    if _is_degenerate(record.l_ratio):
        return StageLabel.UNASSIGNED

    l_ratio = record.l_ratio
    common = (_Q_LOW <= record.Q <= _Q_HIGH) and (record.s_min > interim_s0)

    if record.E < _E_STAGE0_MAX and l_ratio > _L_RATIO_STAGE0_MIN and common:
        return StageLabel.STAGE_0

    stage_1a = _E_STAGE1A_LOW <= record.E < _E_STAGE1A_HIGH and l_ratio > _L_RATIO_STAGE0_MIN
    stage_1b = (record.E < _E_STAGE0_MAX
                and _L_RATIO_STAGE1B_LOW <= l_ratio < _L_RATIO_STAGE1B_HIGH)
    if (stage_1a or stage_1b) and common:
        return StageLabel.STAGE_1

    return StageLabel.UNASSIGNED
