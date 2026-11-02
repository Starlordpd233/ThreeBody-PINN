"""Phase 67 (design & settings ladders): the pure cadence and budget rule.

This module owns the registered Phase 67 checkpoint schedule and the
cost-only common-update budget (D-07/D-08/D-09/D-10 through
67-RESEARCH's budget recommendation):

* :func:`phase67_cadence` — the five normalized similarity events
  ``0, N/4, N/2, 3N/4, N`` every registered Phase 67 run logs, defined at
  positive step counts that are multiples of the 100-step quantum.
* :func:`phase67_score_cadence` — the three frozen ``score_network``
  checkpoints ``N/2, 3N/4, N``; the final one supplies the endpoint score,
  so no fourth scoring call happens (D-08).
* :func:`phase67_loss_trace_stride` — the bounded recorded loss trace
  ``ceil(N / 1000)`` with the final loss retained, so at most 1001 entries
  exist at any length.
* :data:`PHASE67_BUDGET_RULE` — the registered numbers both scales use:
  the science budget (the 3,540-second cap, the 0.75 time fraction, the 25
  percent optimizer-rate margin, the 200 warmup updates, the 100-step
  quantum and the 300-step floor) and the timing run that measures the
  schedule's actual cost (N = 1200, warmup 200, measured 1000, under its
  own 900-second whole-launch cap, D-07/D-10).

Everything here is pure arithmetic over validated cost rows: no score,
loss, tier or cosine value enters a projection or an output (T-67-10).
The fit harness imports this module; it never imports the harness, the
guard, the data seam, the similarity logger, the launcher or any reader,
so the catalog/declaration direction established by 67-01/67-02 holds.
"""

from __future__ import annotations

from types import MappingProxyType

__all__ = [
    "PHASE67_BUDGET_RULE",
    "phase67_cadence",
    "phase67_loss_trace_entries",
    "phase67_loss_trace_stride",
    "phase67_score_cadence",
]

#: The one Phase 67 budget rule (D-07/D-08/D-09/D-10). ``cap_seconds`` with
#: ``time_fraction`` bounds every projected whole-run wall; ``rate_margin``
#: is the optimizer-rate safety factor; ``warmup_steps`` is the common warmup
#: both scales retain; ``step_quantum``/``min_steps`` fix the admissible step
#: counts (the cadence is defined at multiples of the quantum, and no budget
#: falls below the floor); the size fields bound the recorded record at its
#: source and refuse an unsafe size rather than shortening science; and the
#: ``timing_*`` fields are the registered timing run every cost row must
#: come from. Science keeps the 200-update warmup under the 3,540-second
#: cap; the timing run itself keeps 200 warmup of its 1,200 updates under a
#: 900-second whole-launch cap.
PHASE67_BUDGET_RULE = MappingProxyType({
    "cap_seconds": 3540.0,
    "time_fraction": 0.75,
    "rate_margin": 0.25,
    "warmup_steps": 200,
    "step_quantum": 100,
    "min_steps": 300,
    "similarity_events": 5,
    "score_events": 3,
    "loss_trace_entries_max": 1000,
    "loss_entry_bytes": 32,
    "residual_tolerance": 1e-9,
    "size_limit_bytes": 10485760,
    "size_fraction": 0.9,
    "timing_steps": 1200,
    "timing_warmup": 200,
    "timing_measured": 1000,
    "timing_cap_seconds": 900.0,
})


def _schedule_steps(n):
    """A positive step count that is a multiple of the step quantum."""
    quantum = int(PHASE67_BUDGET_RULE["step_quantum"])
    if isinstance(n, bool) or not isinstance(n, int) or n <= 0 or n % quantum:
        raise ValueError(
            "the Phase 67 schedule is defined at positive step counts that "
            f"are multiples of the {quantum}-step quantum; got {n!r}"
        )
    return int(n)


def phase67_cadence(n):
    """The five normalized similarity events of an ``n``-step Phase 67 run.

    ``[0, n//4, n//2, 3*n//4, n]`` — the registered schedule every Phase 67
    timing and science run shares (D-08: identical normalized schedule), so
    timing measures the events science actually performs. Raises
    ``ValueError`` for a step count that is not a positive multiple of the
    100-step quantum.
    """
    steps = _schedule_steps(n)
    return [0, steps // 4, steps // 2, 3 * steps // 4, steps]


def phase67_score_cadence(n):
    """The three frozen-score checkpoints of an ``n``-step Phase 67 run.

    ``[n//2, 3*n//4, n]`` — every checkpoint rides the similarity cadence
    grid, and the final checkpoint supplies the endpoint score, so the fit
    never makes a fourth scoring call (D-08/D-10). Raises ``ValueError``
    under the same contract as :func:`phase67_cadence`.
    """
    cadence = phase67_cadence(n)
    return cadence[2:]


def phase67_loss_trace_stride(n):
    """The bounded recorded loss-trace stride: ``ceil(n / 1000)``.

    With the harness's final-loss retention this keeps at most 1001 entries
    at any length, so the recorded record's loss block is bounded at its
    source (the Phase 66 Site F precedent at the Phase 67 quantum).
    """
    if isinstance(n, bool) or not isinstance(n, int) or n < 1:
        raise ValueError(f"the step count must be a positive integer; got {n!r}")
    maximum = int(PHASE67_BUDGET_RULE["loss_trace_entries_max"])
    return (int(n) + maximum - 1) // maximum


def phase67_loss_trace_entries(n, stride):
    """The recorded trace length for ``n`` losses at stride ``stride``.

    Exactly the length the fit harness records: every stride-th loss, then
    the final loss when ``n`` is not a multiple of the stride.
    """
    if isinstance(stride, bool) or not isinstance(stride, int) or stride < 1:
        raise ValueError(f"the stride must be a positive integer; got {stride!r}")
    if isinstance(n, bool) or not isinstance(n, int) or n < 1:
        raise ValueError(f"the step count must be a positive integer; got {n!r}")
    return n // stride + (1 if n % stride else 0)
