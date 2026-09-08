"""Structural-only candidate selection for Phase-57 EVAL-02.

The evaluator has one pre-registered look.  This module carries forward the
Phase-50 candidate seam without importing or inspecting any scientific metric:
four existing structural facts are evaluated for each finished run and the
first eligible seed is selected in the locked order ``42 -> 41 -> 43``.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

__all__ = [
    "CANDIDATE_ORDER",
    "REQUIRED_STRUCTURAL_FACTS",
    "TERMINAL_OUTCOMES",
    "BLOCKING_OUTCOMES",
    "structural_facts",
    "select_candidate",
    "classify_run_outcome",
]


CANDIDATE_ORDER: tuple[int, ...] = (42, 41, 43)
REQUIRED_STRUCTURAL_FACTS: tuple[str, ...] = (
    "eval01_precondition_i",
    "guard_invariant_rule",
    "finished",
    "eval01_precondition_iii",
)
TERMINAL_OUTCOMES = frozenset({
    "gate04_block",
    "invariant_b_halt_no_advance",
})
BLOCKING_OUTCOMES = frozenset({
    "resource_exhaustion",
    "guard_recover_exhausted",
    "config_error",
    "operational_failure",
    "interrupted",
})


def structural_facts(record: Mapping[str, Any]) -> dict[str, bool]:
    """Project exactly the four Phase-50 eligibility facts plus ``eligible``.

    Values are accepted only when they are the literal boolean ``True``;
    truthy strings/numbers cannot accidentally authorize the held-out look.
    Additional fields, including ``scs``/loss/front metrics, are ignored by
    construction and therefore cannot influence selection.
    """
    if not isinstance(record, Mapping):
        raise TypeError(f"candidate record must be a mapping; got {type(record).__name__}")
    facts = {name: record.get(name) is True for name in REQUIRED_STRUCTURAL_FACTS}
    facts["eligible"] = all(facts.values())
    return facts


def select_candidate(facts_by_seed: Mapping[Any, Mapping[str, Any]]) -> int | None:
    """Return the first eligible seed in the fixed ``42, 41, 43`` order.

    Missing seeds and all non-structural record fields are treated as
    ineligible.  No metric comparison or fallback after an attempted
    evaluation is possible in this function.
    """
    if not isinstance(facts_by_seed, Mapping):
        raise TypeError(
            f"facts_by_seed must be a mapping; got {type(facts_by_seed).__name__}"
        )
    for seed in CANDIDATE_ORDER:
        record = facts_by_seed.get(seed)
        if record is None:
            record = facts_by_seed.get(str(seed))
        if not isinstance(record, Mapping):
            continue
        # Always recompute the projection.  A caller-provided ``eligible``
        # field is not trusted because it could be stale or metric-derived.
        if structural_facts(record)["eligible"]:
            return seed
    return None


def classify_run_outcome(outcome: str) -> str:
    """Classify a run as ``terminal`` or ``blocking`` without ambiguity.

    The two declared scientific terminal branches preserve the evaluation
    unspent and close the phase. Resource, guard, operational, and unknown
    outcomes remain blocking/incomplete; an unknown label is never promoted to
    a clean terminal result.
    """
    if not isinstance(outcome, str) or not outcome:
        raise ValueError(f"run outcome must be a non-empty string; got {outcome!r}")
    if outcome in TERMINAL_OUTCOMES:
        return "terminal"
    if outcome in BLOCKING_OUTCOMES:
        return "blocking"
    return "blocking"
