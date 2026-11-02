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

:func:`phase67_budget` (plan 67-04 task 67-04-02) derives the common
update budget from one experiment's complete validated timing rows: every
main and repeat row (including the seed-41 repeat, D-09) must be present,
keyed by its complete experiment/arm/orbit/seed/window identity and
carrying the registered timing scale (1,200 steps, 200 warmup, 1,000
measured), the five individually measured logger-event seconds, the three
individually measured scorer-event seconds, the publication I/O seconds,
the full-launch wall and the published byte counts. The projected wall at
a candidate ``N`` is the launch residual ``F`` (the launch wall minus the
row's own itemized durations, which retains every comparison, data-load,
power, admission and supervision cost) plus the measured warmup, the
measured steps at the timing rate with the 25 percent margin, five
maximum logger-event seconds, three maximum scorer-event seconds and the
publication I/O scaled by the predicted byte bound. ``N`` is the largest
multiple of the 100-step quantum at or above the 300-step floor whose
every-row projection stays within 0.75 of the 3,540-second cap, found by
integer exponential bracketing plus binary search; equality at the target
admits and the next 100-step candidate must exceed it. An unsafe predicted
record size refuses rather than shortening science, and a timing row set
with no admissible ``N`` is an explicit resource refusal — never a
borrowed historical rate (D-07/D-08, T-67-10/T-67-11).
"""

from __future__ import annotations

import math
import re
from collections.abc import Mapping
from types import MappingProxyType

__all__ = [
    "PHASE67_BUDGET_RULE",
    "phase67_budget",
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


# --------------------------------------------------------------------------
# Plan 67-04 task 67-04-02: the cost-only common update budget.
# --------------------------------------------------------------------------

_DIGEST_RE = re.compile(r"[0-9a-f]{64}")


def _finite_number(value, *, what):
    """A finite number excluding booleans, or a refusal naming it."""
    if isinstance(value, bool) or not isinstance(value, (int, float)) \
            or not math.isfinite(float(value)):
        raise ValueError(f"{what} must be a finite number excluding booleans; got {value!r}")
    return float(value)


def _identity_key(identity):
    """The canonical key of a complete experiment/arm/orbit/seed/window identity."""
    if not isinstance(identity, Mapping):
        raise ValueError(f"an identity must be a mapping; got {identity!r}")
    for field in ("experiment", "arm", "orbit_key"):
        value = identity.get(field)
        if not isinstance(value, str) or not value:
            raise ValueError(
                f"the identity {field} must be non-empty text; got {value!r}"
            )
    seed = identity.get("seed")
    if isinstance(seed, bool) or not isinstance(seed, int):
        raise ValueError(f"the identity seed must be an integer; got {seed!r}")
    window = _finite_number(identity.get("window"), what="the identity window")
    return "|".join((
        identity["experiment"],
        identity["arm"],
        identity["orbit_key"],
        str(int(seed)),
        repr(window),
    ))


def _event_seconds(value, *, count, what, key):
    """Exactly ``count`` individually measured non-negative event seconds."""
    if not isinstance(value, list) or len(value) != count:
        raise ValueError(
            f"the cost row for {key} must carry exactly {count} {what}; got {value!r}"
        )
    events = [
        _finite_number(entry, what=f"each of the {what} for {key}")
        for entry in value
    ]
    for event in events:
        if event < 0.0:
            raise ValueError(
                f"the {what} for {key} must be non-negative; got {value!r}"
            )
    return events


def _positive_int(value, *, what):
    if isinstance(value, bool) or not isinstance(value, int) or value < 1:
        raise ValueError(f"{what} must be a positive integer; got {value!r}")
    return int(value)


def _parse_cost_row(row):
    """One validated cost row, or a refusal naming the breach (T-67-10)."""
    if not isinstance(row, Mapping):
        raise ValueError(f"a cost row must be a mapping; got {row!r}")
    key = _identity_key(row.get("identity"))
    timing = row.get("timing")
    if not isinstance(timing, Mapping):
        raise ValueError(f"the cost row for {key} names no timing block")
    for field, expected in (
        ("optimizer_steps", int(PHASE67_BUDGET_RULE["timing_steps"])),
        ("warmup_steps", int(PHASE67_BUDGET_RULE["timing_warmup"])),
        ("measured_steps", int(PHASE67_BUDGET_RULE["timing_measured"])),
    ):
        value = timing.get(field)
        if isinstance(value, bool) or not isinstance(value, int) or value != expected:
            raise ValueError(
                f"the timing row for {key} must carry {field}={expected} (the "
                f"registered timing scale); got {value!r}"
            )
    seconds_per_step = _finite_number(
        timing.get("seconds_per_step"),
        what=f"the measured rate of {key}",
    )
    if seconds_per_step <= 0.0:
        raise ValueError(
            f"the measured rate of {key} is not positive; got {seconds_per_step!r}"
        )
    warmup_seconds = _finite_number(
        timing.get("warmup_seconds"), what=f"the warmup seconds of {key}"
    )
    measured_seconds = _finite_number(
        timing.get("measured_seconds"), what=f"the measured seconds of {key}"
    )
    for name, value in (("warmup_seconds", warmup_seconds),
                        ("measured_seconds", measured_seconds)):
        if value < 0.0:
            raise ValueError(
                f"the {name} of {key} must be non-negative; got {value!r}"
            )
    logger_events = _event_seconds(
        row.get("logger_event_seconds"),
        count=int(PHASE67_BUDGET_RULE["similarity_events"]),
        what="logger-event seconds", key=key,
    )
    scorer_events = _event_seconds(
        row.get("scorer_event_seconds"),
        count=int(PHASE67_BUDGET_RULE["score_events"]),
        what="scorer-event seconds", key=key,
    )
    publication_io = _finite_number(
        row.get("publication_io_seconds"),
        what=f"the publication-I/O seconds of {key}",
    )
    if publication_io < 0.0:
        raise ValueError(
            f"the publication-I/O seconds of {key} must be non-negative; "
            f"got {publication_io!r}"
        )
    launch_wall = _finite_number(
        row.get("launch_wall_seconds"), what=f"the launch wall of {key}"
    )
    if launch_wall < 0.0:
        raise ValueError(
            f"the launch wall of {key} must be non-negative; got {launch_wall!r}"
        )
    record_bytes = _positive_int(
        row.get("record_bytes"), what=f"the record bytes of {key}"
    )
    weights_bytes = _positive_int(
        row.get("weights_bytes"), what=f"the weights bytes of {key}"
    )
    digest = row.get("timing_evidence_sha256")
    if digest is not None and (
        not isinstance(digest, str) or _DIGEST_RE.fullmatch(digest) is None
    ):
        raise ValueError(
            f"the timing-evidence digest of {key} must be 64 lowercase hex "
            f"characters or absent; got {digest!r}"
        )
    itemized = (
        warmup_seconds + measured_seconds
        + sum(logger_events) + sum(scorer_events) + publication_io
    )
    residual = launch_wall - itemized
    if residual < -float(PHASE67_BUDGET_RULE["residual_tolerance"]):
        raise ValueError(
            f"the cost row for {key} has an inconsistent negative launch "
            f"residual ({residual!r} s): the launch wall is shorter than its "
            "own itemized durations beyond the tolerance"
        )
    return {
        "key": key,
        "experiment": row["identity"]["experiment"],
        "seconds_per_step": seconds_per_step,
        "warmup_seconds": warmup_seconds,
        "logger_events": logger_events,
        "scorer_events": scorer_events,
        "publication_io_seconds": publication_io,
        "residual_seconds": residual,
        "published_bytes": record_bytes + weights_bytes,
        "timing_evidence_sha256": digest,
    }


def phase67_budget(cost_rows, *, expected_identities, unmeasured=None):
    """The common update budget derived from every registered timing row.

    ``cost_rows`` are the validated cost-only rows of one experiment's
    registered timing runs; ``expected_identities`` is the complete declared
    identity set — every main and repeat row, including the seed-41 repeat
    (D-09), must be present exactly once, and no undeclared row may appear.
    ``unmeasured`` optionally maps experiment names without timing rows to
    their declared run counts, reserved at the whole-run cap. Returns the
    largest multiple of the 100-step quantum at or above the 300-step floor
    whose every-row projected whole-run wall stays within 0.75 of the
    3,540-second cap, beside the exact cadence/score cadence/bounded stride
    at that count, the per-row and per-experiment projections, the timing
    evidence digests and the phase cost ledger. No score, loss, tier or
    cosine value is read from a row or appears in the output (T-67-10).
    Raises ``ValueError`` for every malformed, missing, duplicate or
    non-finite row, a negative launch residual beyond the 1e-9 s tolerance,
    an unsafe predicted record size (which refuses rather than shortening
    science), or a row set with no admissible update count.
    """
    if not isinstance(cost_rows, (list, tuple)) or not cost_rows:
        raise ValueError("the budget needs at least one cost row")
    if not isinstance(expected_identities, (list, tuple)) or not expected_identities:
        raise ValueError("the budget needs the complete declared identity set")
    expected = {}
    for identity in expected_identities:
        key = _identity_key(identity)
        if key in expected:
            raise ValueError(f"the declared identity {key} appears twice")
        expected[key] = identity
    rows = {}
    for row in cost_rows:
        parsed = _parse_cost_row(row)
        if parsed["key"] in rows:
            raise ValueError(
                f"a duplicate cost row for {parsed['key']} refuses: one timing "
                "run per declared identity"
            )
        if parsed["key"] not in expected:
            raise ValueError(
                f"the cost row for {parsed['key']} is not a declared identity; "
                "an undeclared timing run cannot size the budget"
            )
        rows[parsed["key"]] = parsed
    missing = sorted(key for key in expected if key not in rows)
    if missing:
        raise ValueError(
            "every declared timing row is required before a budget exists; "
            "missing: " + "; ".join(missing)
        )

    cap = float(PHASE67_BUDGET_RULE["cap_seconds"])
    target = float(PHASE67_BUDGET_RULE["time_fraction"]) * cap
    quantum = int(PHASE67_BUDGET_RULE["step_quantum"])
    warmup_steps = int(PHASE67_BUDGET_RULE["warmup_steps"])
    min_steps = int(PHASE67_BUDGET_RULE["min_steps"])
    margin = 1.0 + float(PHASE67_BUDGET_RULE["rate_margin"])
    similarity_events = int(PHASE67_BUDGET_RULE["similarity_events"])
    score_events = int(PHASE67_BUDGET_RULE["score_events"])
    loss_entry_bytes = int(PHASE67_BUDGET_RULE["loss_entry_bytes"])
    timing_steps = int(PHASE67_BUDGET_RULE["timing_steps"])
    timing_trace_entries = phase67_loss_trace_entries(
        timing_steps, phase67_loss_trace_stride(timing_steps)
    )
    size_ceiling = float(PHASE67_BUDGET_RULE["size_fraction"]) * int(
        PHASE67_BUDGET_RULE["size_limit_bytes"]
    )
    keys = sorted(rows)

    def byte_bound(row, n):
        """Weights plus the measured record, extra loss entries and growth."""
        stride = phase67_loss_trace_stride(n)
        entries = phase67_loss_trace_entries(n, stride)
        growth = max(0, len(str(int(n))) - len(str(timing_steps)))
        return (
            row["published_bytes"]
            + loss_entry_bytes * max(0, entries - timing_trace_entries)
            + growth * (similarity_events + score_events + entries)
        )

    def projection(row, n):
        """The registered per-row projected whole-run wall at ``n`` steps."""
        bound = byte_bound(row, n)
        if bound > size_ceiling:
            raise ValueError(
                f"the predicted record byte bound for {row['key']} at {n} steps "
                f"({bound} bytes) exceeds the staged-blob safety ceiling "
                f"({int(size_ceiling)} bytes); the size refuses rather than "
                "shortening science from its registered checkpoints"
            )
        value = (
            row["residual_seconds"]
            + row["warmup_seconds"]
            + (n - warmup_steps) * row["seconds_per_step"] * margin
            + similarity_events * max(row["logger_events"])
            + score_events * max(row["scorer_events"])
            + row["publication_io_seconds"]
            * max(1.0, bound / row["published_bytes"])
        )
        if not math.isfinite(value):
            raise ValueError(
                f"the projected wall for {row['key']} at {n} steps is not finite"
            )
        return value

    def worst(n):
        return max(projection(rows[key], n) for key in keys)

    low = min_steps // quantum
    if worst(low * quantum) > target:
        raise ValueError(
            f"no admissible update count at or above {min_steps} steps stays "
            f"within {target:g} seconds (the projected minimum is "
            f"{worst(low * quantum):g} s); the budget is an explicit resource "
            "refusal, never a borrowed historical rate"
        )
    high = low * 2
    while worst(high * quantum) <= target:
        low = high
        high *= 2
    while high - low > 1:
        middle = (low + high) // 2
        if worst(middle * quantum) <= target:
            low = middle
        else:
            high = middle
    steps = low * quantum

    per_row = {key: projection(rows[key], steps) for key in keys}
    experiment_projection = {}
    experiment_runs = {}
    for key in keys:
        experiment = rows[key]["experiment"]
        experiment_runs[experiment] = experiment_runs.get(experiment, 0) + 1
        experiment_projection[experiment] = (
            experiment_projection.get(experiment, 0.0) + per_row[key]
        )
    ledger_experiments = [
        {
            "experiment": experiment,
            "basis": "measured_projection",
            "declared_runs": experiment_runs[experiment],
            "planned_seconds": experiment_projection[experiment],
            "note": (
                "measured timing rows; update this ledger with the measured "
                "projections before each science launch"
            ),
        }
        for experiment in sorted(experiment_projection)
    ]
    if unmeasured is not None:
        if not isinstance(unmeasured, Mapping) or not unmeasured:
            raise ValueError(
                "unmeasured must map experiment names to declared run counts"
            )
        for experiment, runs in sorted(unmeasured.items()):
            if isinstance(experiment, bool) or not isinstance(experiment, str) \
                    or not experiment:
                raise ValueError(
                    f"an unmeasured experiment name must be non-empty text; "
                    f"got {experiment!r}"
                )
            if experiment in experiment_projection:
                raise ValueError(
                    f"the experiment {experiment} has measured timing rows; it "
                    "cannot also be declared unmeasured"
                )
            if isinstance(runs, bool) or not isinstance(runs, int) or runs < 1:
                raise ValueError(
                    f"the unmeasured experiment {experiment} must declare a "
                    f"positive run count; got {runs!r}"
                )
            ledger_experiments.append({
                "experiment": experiment,
                "basis": "cap_reservation_unmeasured",
                "declared_runs": runs,
                "reserved_upper_bound_seconds": runs * cap,
                "note": (
                    "no measured timing rows yet; an explicit cap-based upper "
                    f"reservation of {cap:g} seconds per run; no historical "
                    "per-step cost is borrowed"
                ),
            })
    return {
        "common_optimizer_steps": int(steps),
        "warmup_steps": warmup_steps,
        "measured_steps": int(steps - warmup_steps),
        "similarity_cadence": phase67_cadence(steps),
        "score_cadence": phase67_score_cadence(steps),
        "loss_trace_stride": phase67_loss_trace_stride(steps),
        "per_row_projection_seconds": per_row,
        "timing_evidence_digests": {
            key: rows[key]["timing_evidence_sha256"] for key in keys
        },
        "experiment_projected_seconds": experiment_projection,
        "phase_cost_ledger": {
            "cap_seconds": cap,
            "experiments": ledger_experiments,
        },
        "inputs": {
            "cap_seconds": cap,
            "target_seconds": target,
            "time_fraction": float(PHASE67_BUDGET_RULE["time_fraction"]),
            "rate_margin": float(PHASE67_BUDGET_RULE["rate_margin"]),
            "step_quantum": quantum,
            "min_steps": min_steps,
            "size_ceiling_bytes": int(size_ceiling),
            "rows": {
                key: {
                    "residual_seconds": rows[key]["residual_seconds"],
                    "warmup_seconds": rows[key]["warmup_seconds"],
                    "seconds_per_step": rows[key]["seconds_per_step"],
                    "published_bytes": rows[key]["published_bytes"],
                    "predicted_byte_bound": byte_bound(rows[key], steps),
                }
                for key in keys
            },
        },
    }
