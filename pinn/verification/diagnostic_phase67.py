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
    "CONFIRMATION_LABELS",
    "GAP_59_08_NOTE",
    "PHASE67_BUDGET_RULE",
    "PHASE67_CASES",
    "PHASE67_EFFECT_RULE",
    "PHASE67_IMPROVEMENT_RULE",
    "SIMILARITY_NOTE",
    "phase67_budget",
    "phase67_cadence",
    "phase67_confirmation",
    "phase67_contrast",
    "phase67_control_arm",
    "phase67_improvement_check",
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


# --------------------------------------------------------------------------
# Plan 67-05 task 67-05-02: the prospective reading, contrast and confirmation
# rules (D-08/D-09/D-10/D-11 through 67-RESEARCH's interpretation
# recommendation), committed before any prediction page or real run exists.
# --------------------------------------------------------------------------

#: The three registered D-09 confirmation cases every declared contrast
#: repeats on: the main comparison system and seed, the second panel system,
#: and the second seed on the main system.
PHASE67_CASES = MappingProxyType({
    role: MappingProxyType(binding)
    for role, binding in (
        ("main", {"orbit_key": "hierarchical/gold/1632", "seed": 42}),
        ("repeat-system", {"orbit_key": "hierarchical/gold/851", "seed": 42}),
        ("repeat-seed", {"orbit_key": "hierarchical/gold/1632", "seed": 41}),
    )
})

#: The final-quarter convergence rule (D-08): an endpoint whose E improves by
#: strictly more than five percent relative to its three-quarter checkpoint
#: is unsettled — a bounded-budget fit that is still improving says nothing
#: about representational impossibility. Exactly five percent is settled.
PHASE67_IMPROVEMENT_RULE = MappingProxyType({
    "reference": "the three-quarter frozen-score checkpoint",
    "final": "the final frozen-score checkpoint",
    "definition": "(E_at_3N_over_4 - E_at_N) / E_at_3N_over_4",
    "threshold": 0.05,
    "comparison": "strictly_greater_is_unsettled",
})

#: The replicated-effect rule (D-09): a case qualifies when the E direction
#: is nonzero and either the frozen tier changes in that same direction or
#: the relative E effect reaches twenty percent. These are finite-budget
#: diagnostic reading labels; they do not amend the frozen FEAS tiers.
PHASE67_EFFECT_RULE = MappingProxyType({
    "relative_effect": "abs(E_arm - E_control) / E_control",
    "threshold": 0.20,
    "comparison": "greater_or_equal_qualifies",
    "tier_ordering": "higher tier number is better; the frozen scorecard levels 3, 2, 1 then otherwise 0",
})

#: The exact confirmation labels of the prospective branch table.
CONFIRMATION_LABELS = (
    "confirmed-improvement",
    "confirmed-worsening",
    "ambiguous",
    "unsettled",
    "inconclusive-mechanical",
)

#: GAP-59-08 stays explicit beside every contrast output (D-11).
GAP_59_08_NOTE = (
    "GAP-59-08: E is the frozen scorecard's position-error score; no energy "
    "bar or scorer definition is adjudicated here"
)

#: Adjacent-time hidden-state similarity stays associated, descriptive
#: evidence (D-02/D-11): no cosine threshold, no causal claim.
SIMILARITY_NOTE = (
    "adjacent-time hidden-state similarity is associated evidence only; no "
    "cosine threshold and no causal claim"
)


def phase67_control_arm(experiment, arm):
    """The registered control arm a noncontrol arm is contrasted with.

    EXP-02 contrasts every depth arm with ``d12`` (the locked depth), EXP-03
    every rate arm with ``lr1e-4`` (the locked rate), EXP-04 every encoded
    arm with its own backbone's raw input, and EXP-05 every shorter prefix
    with ``lap10``. Raises ``ValueError`` for an unknown experiment or arm.
    """
    if not isinstance(experiment, str) or not isinstance(arm, str):
        raise ValueError(
            f"the experiment and arm must be text; got {experiment!r}, {arm!r}"
        )
    depth_arms = ("d2", "d4", "d6", "d8", "d12")
    rate_arms = ("lr1e-3", "lr3e-4", "lr1e-4", "lr3e-5", "lr1e-5")
    if experiment == "exp02":
        if arm not in depth_arms:
            raise ValueError(
                f"unknown exp02 depth arm {arm!r}; known: {depth_arms}"
            )
        return "d12"
    if experiment == "exp03":
        if arm not in rate_arms:
            raise ValueError(
                f"unknown exp03 rate arm {arm!r}; known: {rate_arms}"
            )
        return "lr1e-4"
    if experiment == "exp05":
        if arm in ("lap1", "lap2", "lap5", "lap10"):
            return "lap10"
        raise ValueError(
            f"unknown exp05 window arm {arm!r}; known: lap1, lap2, lap5, lap10"
        )
    if experiment == "exp04":
        if arm.startswith("locked-"):
            return "locked-raw"
        if arm.startswith("exp01-"):
            return "exp01-raw"
        raise ValueError(
            f"unknown exp04 input arm {arm!r}; known backbones: locked-, exp01-"
        )
    raise ValueError(
        f"unknown Phase 67 experiment {experiment!r}; known: exp02, exp03, "
        "exp04, exp05"
    )


def _checkpoint_e(checkpoint, *, what):
    """One score checkpoint's finite non-negative E, or a refusal."""
    if not isinstance(checkpoint, Mapping):
        raise ValueError(f"{what} must be a score-checkpoint mapping; got {checkpoint!r}")
    score = checkpoint.get("score")
    if not isinstance(score, Mapping):
        raise ValueError(f"{what} names no score block")
    e_value = score.get("E")
    if isinstance(e_value, bool) or not isinstance(e_value, (int, float)) \
            or not math.isfinite(float(e_value)):
        raise ValueError(f"{what} names a non-finite or non-numeric E: {e_value!r}")
    if float(e_value) < 0.0:
        raise ValueError(f"{what} names a negative E: {e_value!r}")
    return float(e_value)


def phase67_improvement_check(checkpoints):
    """The final-quarter improvement rule over the three score checkpoints.

    ``checkpoints`` are the reading's recorded frozen-score checkpoints at
    N/2, 3N/4 and N (each ``{"step", "score": {"E", ...}}``). The improvement
    is ``(E_at_3N/4 - E_at_N) / E_at_3N/4``; strictly greater than the
    five-percent threshold leaves the endpoint unsettled, exactly five
    percent is settled, and a zero reference is settled either way (a zero
    final E is settled and a positive final E is a settled worsening). A
    negative, non-finite, boolean or string E, a wrong checkpoint count or
    non-increasing steps refuse. Returns the reference/final steps, the
    improvement (``None`` on a zero reference), the threshold and the
    ``settled`` flag with a ``reason`` when one is needed.
    """
    if not isinstance(checkpoints, (list, tuple)) or len(checkpoints) != 3:
        raise ValueError(
            "the improvement check needs exactly the three registered score "
            f"checkpoints; got {len(checkpoints) if hasattr(checkpoints, '__len__') else checkpoints!r}"
        )
    steps = []
    for index, checkpoint in enumerate(checkpoints):
        step = checkpoint.get("step") if isinstance(checkpoint, Mapping) else None
        if isinstance(step, bool) or not isinstance(step, int):
            raise ValueError(f"score checkpoint {index} names no integer step")
        steps.append(int(step))
    if not steps[0] < steps[1] < steps[2]:
        raise ValueError(
            f"the score checkpoint steps must be increasing; got {steps}"
        )
    reference = _checkpoint_e(checkpoints[1], what="the three-quarter checkpoint")
    final = _checkpoint_e(checkpoints[2], what="the final checkpoint")
    threshold = float(PHASE67_IMPROVEMENT_RULE["threshold"])
    if reference == 0.0:
        return {
            "reference_step": steps[1],
            "final_step": steps[2],
            "improvement": None,
            "threshold": threshold,
            "settled": True,
            "reason": (
                "the reference E is zero: a zero final E is settled and a "
                "positive final E is a settled worsening"
            ),
        }
    improvement = (reference - final) / reference
    settled = not improvement > threshold
    return {
        "reference_step": steps[1],
        "final_step": steps[2],
        "improvement": improvement,
        "threshold": threshold,
        "settled": settled,
        "reason": None if settled else (
            f"the final-quarter improvement {improvement!r} exceeds the "
            f"registered {threshold} boundary: the endpoint is unsettled"
        ),
    }


def _contrast_endpoint(reading, *, experiment, arm, role):
    """One validated endpoint reading of a contrast case."""
    if not isinstance(reading, Mapping):
        raise ValueError(
            f"the {role} {arm} reading must be a mapping; got {reading!r}"
        )
    problems = []
    for field in ("mechanical_problems", "setting_problems"):
        values = reading.get(field)
        if not isinstance(values, list) or any(
            not isinstance(value, str) for value in values
        ):
            raise ValueError(
                f"the {role} {arm} reading names no {field} string list"
            )
        problems.extend(f"{field}: {value}" for value in values)
    identity = reading.get("identity")
    if not isinstance(identity, Mapping):
        raise ValueError(f"the {role} {arm} reading names no identity")
    registered = PHASE67_CASES[role]
    for field, expected in (
        ("experiment", experiment),
        ("arm", arm),
        ("orbit_key", registered["orbit_key"]),
    ):
        if identity.get(field) != expected:
            raise ValueError(
                f"the {role} {arm} reading's identity {field} is "
                f"{identity.get(field)!r}; the registered contrast expects "
                f"{expected!r}"
            )
    seed = identity.get("seed")
    if isinstance(seed, bool) or not isinstance(seed, int) \
            or int(seed) != int(registered["seed"]):
        raise ValueError(
            f"the {role} {arm} reading's seed is {seed!r}; the registered "
            f"contrast expects {registered['seed']}"
        )
    scores = reading.get("scores")
    network = scores.get("network") if isinstance(scores, Mapping) else None
    if not isinstance(network, Mapping):
        raise ValueError(f"the {role} {arm} reading names no network score")
    e_value = _checkpoint_e({"score": network}, what=f"the {role} {arm} E")
    tier = network.get("tier")
    if isinstance(tier, bool) or not isinstance(tier, int) \
            or not 0 <= int(tier) <= 3:
        raise ValueError(
            f"the {role} {arm} reading's tier must be an integer 0..3; got {tier!r}"
        )
    unsettled = reading.get("unsettled")
    if not isinstance(unsettled, bool):
        raise ValueError(
            f"the {role} {arm} reading's unsettled flag must be a boolean; "
            f"got {unsettled!r}"
        )
    trace = reading.get("layer_trace")
    if not isinstance(trace, list):
        trace = []
    return {
        "E": e_value,
        "tier": int(tier),
        "unsettled": unsettled,
        "problems": problems,
        "layer_trace": trace,
    }


def phase67_contrast(experiment, arm, readings):
    """One declared matched contrast across the three registered cases.

    ``readings`` maps each D-09 role to ``{"arm": reading, "control": reading}``
    — mechanically clean :func:`read_phase67_run_directory` readings with
    scores. The control arm is the registered control of ``arm``
    (:func:`phase67_control_arm`); every reading's identity must match its
    case's registered orbit and seed, its experiment, and its arm, and all
    six run identities must be distinct. Per case the contrast records the
    direction (exact E ordering; equal E is a tie), the relative E effect
    ``abs(E_arm - E_control) / E_control`` (a positive control only — a zero
    control retains the direction and flags the percentage inapplicable
    rather than dividing by zero), the frozen tier direction, whether the
    case qualifies (nonzero direction and either a matching tier change or a
    relative effect of at least twenty percent), both endpoint statuses and
    the observed fit. The confirmation label follows the registered table:
    all three cases qualifying in the same direction with all six endpoints
    settled and clean confirms improvement or worsening; any problematic
    endpoint is inconclusive-mechanical; any unsettled endpoint is unsettled;
    everything else (ties, small effects, opposed directions) is ambiguous
    with reasons. Adjacent-time similarity and the loss stay descriptive
    context and GAP-59-08 stays explicit. These labels describe finite-budget
    diagnostic effects and never amend the frozen FEAS tiers.
    """
    if not isinstance(readings, Mapping):
        raise ValueError(f"the contrast readings must be a mapping; got {readings!r}")
    if set(readings) != set(PHASE67_CASES):
        raise ValueError(
            "a declared contrast repeats on exactly the three registered "
            f"cases {sorted(PHASE67_CASES)}; got {sorted(map(str, readings))}"
        )
    control = phase67_control_arm(experiment, arm)
    if arm == control:
        raise ValueError(
            f"the control arm {control!r} is not contrasted with itself"
        )
    endpoints = {}
    seen = {}
    for role in PHASE67_CASES:
        pair = readings[role]
        if not isinstance(pair, Mapping) or set(pair) != {"arm", "control"}:
            raise ValueError(
                f"the {role} case must map exactly arm and control readings"
            )
        endpoints[role] = {
            "arm": _contrast_endpoint(
                pair["arm"], experiment=experiment, arm=arm, role=role
            ),
            "control": _contrast_endpoint(
                pair["control"], experiment=experiment, arm=control, role=role
            ),
        }
        for kind, endpoint in endpoints[role].items():
            key = (
                PHASE67_CASES[role]["orbit_key"],
                int(PHASE67_CASES[role]["seed"]),
                pair[kind]["identity"]["arm"],
            )
            if key in seen:
                raise ValueError(
                    "two contrast readings share one run identity "
                    f"{key}; an interrupted or duplicate attempt never counts "
                    "as an additional replicate"
                )
            seen[key] = (role, kind)

    threshold = float(PHASE67_EFFECT_RULE["threshold"])
    cases = {}
    reasons: list[str] = []
    for role, pair in endpoints.items():
        arm_end = pair["arm"]
        control_end = pair["control"]
        e_arm, e_control = arm_end["E"], control_end["E"]
        if e_arm < e_control:
            direction = "improvement"
        elif e_arm > e_control:
            direction = "worsening"
        else:
            direction = "tie"
        applicable = e_control > 0.0
        relative = abs(e_arm - e_control) / e_control if applicable else None
        if arm_end["tier"] > control_end["tier"]:
            tier_direction = "improved"
        elif arm_end["tier"] < control_end["tier"]:
            tier_direction = "worsened"
        else:
            tier_direction = "unchanged"
        tier_matches = (
            (direction == "improvement" and tier_direction == "improved")
            or (direction == "worsening" and tier_direction == "worsened")
        )
        qualifies = direction != "tie" and (
            tier_matches or (applicable and relative >= threshold)
        )
        case_reasons = []
        if direction == "tie":
            case_reasons.append("an exact E tie carries no direction")
        if direction != "tie" and not tier_matches and not (
            applicable and relative >= threshold
        ):
            case_reasons.append(
                "the effect is below the registered twenty-percent line with "
                "no matching tier change"
            )
        if not applicable:
            case_reasons.append(
                "the control E is zero: the percentage effect is inapplicable "
                "and only a matching tier change can qualify"
            )
        cases[role] = {
            "direction": direction,
            "relative_E_effect": relative,
            "percentage_applicable": applicable,
            "tier_direction": tier_direction,
            "qualifies_effect": qualifies,
            "endpoint_status": {
                "arm": "unsettled" if arm_end["unsettled"] else "settled",
                "control": "unsettled" if control_end["unsettled"] else "settled",
            },
            "observed_fit": {
                "arm": {"E": e_arm, "tier": arm_end["tier"]},
                "control": {"E": e_control, "tier": control_end["tier"]},
            },
            "reasons": case_reasons,
        }
        reasons.extend(f"{role}: {reason}" for reason in case_reasons)

    problem_endpoints = [
        f"{role}/{kind}"
        for role, pair in endpoints.items()
        for kind, endpoint in pair.items()
        if endpoint["problems"]
    ]
    unsettled_endpoints = [
        f"{role}/{kind}"
        for role, pair in endpoints.items()
        for kind, endpoint in pair.items()
        if endpoint["unsettled"]
    ]
    if problem_endpoints:
        confirmation = "inconclusive-mechanical"
        reasons = [
            f"the {name} reading carries problems" for name in problem_endpoints
        ]
    elif unsettled_endpoints:
        confirmation = "unsettled"
        reasons = [
            f"the {name} endpoint is unsettled" for name in unsettled_endpoints
        ]
    else:
        directions = {cases[role]["direction"] for role in cases}
        all_qualify = all(cases[role]["qualifies_effect"] for role in cases)
        if all_qualify and directions == {"improvement"}:
            confirmation = "confirmed-improvement"
            reasons = []
        elif all_qualify and directions == {"worsening"}:
            confirmation = "confirmed-worsening"
            reasons = []
        else:
            confirmation = "ambiguous"
            if len(directions) > 1:
                reasons.insert(
                    0, "the registered cases disagree on the E direction"
                )
    return {
        "experiment": experiment,
        "arm": arm,
        "control": control,
        "cases": cases,
        "confirmation": confirmation,
        "reasons": reasons,
        "descriptive": {
            "adjacent_time_similarity": {
                role: {
                    kind: endpoints[role][kind]["layer_trace"]
                    for kind in ("arm", "control")
                }
                for role in endpoints
            },
            "note": SIMILARITY_NOTE,
            "gap_59_08": GAP_59_08_NOTE,
            "loss": "context only",
        },
    }


def phase67_confirmation(experiment, contrasts, *, declared_arms):
    """The experiment-level confirmation over every declared contrast.

    ``declared_arms`` is the experiment's complete declared arm set (the
    prediction page's arms). Every declared noncontrol arm — each arm whose
    registered control differs from itself — must carry exactly one contrast,
    no control arm is contrasted, no undeclared arm appears, and every
    contrast must belong to this experiment. The output persists every
    declared paired contrast with its confirmation and nonconfirmation
    reasons (T-67-15), separating the confirmed effects from the ambiguous,
    unsettled and mechanically inconclusive ones beside the association and
    GAP-59-08 notes. A favourable main run alone can never confirm anything:
    each contrast already required all three registered cases.
    """
    if not isinstance(contrasts, (list, tuple)) or not contrasts:
        raise ValueError("the confirmation needs the experiment's contrasts")
    if not isinstance(declared_arms, (list, tuple)) or not declared_arms:
        raise ValueError("the confirmation needs the complete declared arm set")
    arms = []
    for arm in declared_arms:
        if not isinstance(arm, str) or not arm:
            raise ValueError(f"a declared arm must be non-empty text; got {arm!r}")
        if arm in arms:
            raise ValueError(f"the declared arm {arm!r} appears twice")
        arms.append(arm)
    noncontrol = [
        arm for arm in arms if phase67_control_arm(experiment, arm) != arm
    ]
    by_arm = {}
    for contrast in contrasts:
        if not isinstance(contrast, Mapping):
            raise ValueError(f"a contrast must be a mapping; got {contrast!r}")
        if contrast.get("experiment") != experiment:
            raise ValueError(
                f"a contrast of experiment {contrast.get('experiment')!r} "
                f"cannot join the {experiment} confirmation"
            )
        arm = contrast.get("arm")
        if not isinstance(arm, str) or not arm:
            raise ValueError(f"a contrast arm must be non-empty text; got {arm!r}")
        if arm not in noncontrol:
            raise ValueError(
                f"the contrast arm {arm!r} is not a declared noncontrol arm "
                f"of {experiment}; the declared noncontrol arms are {noncontrol}"
            )
        if arm in by_arm:
            raise ValueError(f"the contrast for {arm!r} appears twice")
        by_arm[arm] = contrast
    missing = sorted(set(noncontrol) - set(by_arm))
    if missing:
        raise ValueError(
            "every declared noncontrol contrast is required before the "
            f"experiment confirmation exists; missing: {', '.join(missing)}"
        )
    confirmed = []
    unconfirmed = []
    for arm in sorted(by_arm):
        contrast = by_arm[arm]
        confirmation = contrast.get("confirmation")
        if confirmation in ("confirmed-improvement", "confirmed-worsening"):
            confirmed.append({"arm": arm, "confirmation": confirmation})
        else:
            unconfirmed.append({
                "arm": arm,
                "confirmation": confirmation,
                "reasons": list(contrast.get("reasons") or []),
            })
    return {
        "experiment": experiment,
        "contrasts": {arm: by_arm[arm] for arm in sorted(by_arm)},
        "confirmed": confirmed,
        "unconfirmed": unconfirmed,
        "descriptive": {
            "note": SIMILARITY_NOTE,
            "gap_59_08": GAP_59_08_NOTE,
            "loss": "context only",
        },
    }
