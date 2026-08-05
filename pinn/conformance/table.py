"""GATE-01: exact PHYS-05 per-stage table assertion.

The scheduler exposes its configured caps through ``state_dict``.  Its
``current(epoch)`` method intentionally reports ramped values, so consulting
that method here would make an epoch-zero scheduler appear conformant even
when its configured caps are wrong.  This module therefore remains a small,
side-effect-free assertion over the serialized schedule state.
"""

from __future__ import annotations

import math
from collections.abc import Mapping
from dataclasses import fields
from typing import Any

from pinn.constants import (
    PHYS05_I_WARM_CAP,
    PHYS05_I_WARM_FRACTION,
    PHYS05_LAMBDA_DATA,
    PHYS05_LAMBDA_E_MAX,
    PHYS05_LAMBDA_IC_ADVISORY,
    PHYS05_LAMBDA_L_MAX,
    PHYS05_LAMBDA_PHYS_MAX,
)
from pinn.loss_catalog import LossWeights

__all__ = ["assert_phys05_table"]

_STAGE_COUNT = len(PHYS05_LAMBDA_PHYS_MAX)
_STATE_KEYS = frozenset(
    {
        "lambda_phys_max",
        "lambda_e_max",
        "lambda_l_max",
        "lambda_ic",
        "warmup_length",
        "n_adam_k",
    }
)


def _check(
    checks: list[dict[str, Any]],
    *,
    name: str,
    tier: str,
    expected: Any,
    actual: Any,
) -> bool:
    passed = actual == expected
    checks.append(
        {
            "name": name,
            "tier": tier,
            "expected": expected,
            "actual": actual,
            "passed": passed,
        }
    )
    return passed


def _raise_locked(*, stage: int, name: str, expected: Any, actual: Any) -> None:
    raise ValueError(
        f"PHYS-05 conformance failed for stage {stage}: {name} expected "
        f"{expected!r}, actual {actual!r}; the entered stage's "
        "ScheduledWeights was not reconfigured for stage "
        f"{stage} (read its state_dict() caps and configure the entered "
        "stage before running it)"
    )


def _lambda_data_default() -> Any:
    """Read ``LossWeights.lambda_data`` without constructing a weight object."""
    for field in fields(LossWeights):
        if field.name == "lambda_data":
            return field.default
    raise ValueError(
        "PHYS-05 conformance cannot locate LossWeights.lambda_data dataclass "
        "field; restore the locked five-term loss catalog"
    )


def assert_phys05_table(scheduled_weights: Any, stage: int) -> dict[str, Any]:
    """Assert the PHYS-05 row for ``stage`` against live scheduler state.

    Returns a JSON-serializable record containing every check.  Locked-tier
    mismatches raise ``ValueError``; the IC default is advisory and is retained
    in the record without blocking the caller.
    """
    if scheduled_weights is None:
        raise ValueError(
            "PHYS-05 conformance requires a ScheduledWeights instance; got None"
        )
    if not isinstance(stage, int) or isinstance(stage, bool):
        raise ValueError(f"PHYS-05 conformance stage must be an int; got {stage!r}")
    if stage < 0 or stage >= _STAGE_COUNT:
        raise ValueError(
            f"PHYS-05 conformance stage {stage} is outside the table range "
            f"0..{_STAGE_COUNT - 1}"
        )
    state_method = getattr(scheduled_weights, "state_dict", None)
    if not callable(state_method):
        raise ValueError(
            "PHYS-05 conformance requires ScheduledWeights.state_dict(); "
            "the live scheduler does not expose serialized caps"
        )
    try:
        state = state_method()
    except Exception as exc:
        raise ValueError(
            f"PHYS-05 conformance could not read ScheduledWeights.state_dict(): "
            f"{exc}"
        ) from exc
    if not isinstance(state, Mapping):
        raise ValueError(
            "PHYS-05 conformance ScheduledWeights.state_dict() must return a "
            f"mapping; got {type(state).__name__}"
        )
    missing = sorted(_STATE_KEYS.difference(state))
    if missing:
        raise ValueError(
            "PHYS-05 conformance ScheduledWeights.state_dict() is missing "
            f"required key(s): {', '.join(missing)}"
        )

    checks: list[dict[str, Any]] = []
    locked_rows = (
        ("lambda_phys_max", PHYS05_LAMBDA_PHYS_MAX[stage]),
        ("lambda_e_max", PHYS05_LAMBDA_E_MAX[stage]),
        ("lambda_l_max", PHYS05_LAMBDA_L_MAX[stage]),
    )
    for name, expected in locked_rows:
        actual = state[name]
        if not _check(
            checks, name=name, tier="locked", expected=expected, actual=actual
        ):
            _raise_locked(stage=stage, name=name, expected=expected, actual=actual)

    actual_ic = state["lambda_ic"]
    _check(
        checks,
        name="lambda_ic",
        tier="advisory",
        expected=PHYS05_LAMBDA_IC_ADVISORY,
        actual=actual_ic,
    )

    n_adam_k = state["n_adam_k"]
    expected_warmup = min(
        PHYS05_I_WARM_CAP,
        math.floor(PHYS05_I_WARM_FRACTION * n_adam_k),
    )
    actual_warmup = state["warmup_length"]
    if not _check(
        checks,
        name="warmup_length",
        tier="locked",
        expected=expected_warmup,
        actual=actual_warmup,
    ):
        _raise_locked(
            stage=stage,
            name="warmup_length",
            expected=expected_warmup,
            actual=actual_warmup,
        )

    actual_lambda_data = _lambda_data_default()
    if not _check(
        checks,
        name="lambda_data",
        tier="locked",
        expected=PHYS05_LAMBDA_DATA,
        actual=actual_lambda_data,
    ):
        _raise_locked(
            stage=stage,
            name="lambda_data",
            expected=PHYS05_LAMBDA_DATA,
            actual=actual_lambda_data,
        )

    return {"stage": stage, "checks": checks}
