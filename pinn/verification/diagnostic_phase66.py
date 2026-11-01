"""Phase 66 (EXP-01): the small-network control catalog and reading rule.

EXP-01 registers one smaller, shallower diagnostic variant — a 1-hidden-layer
network 384 wide with its first SIREN frequency scaled to the orbit's inner-lap
rate (``first_omega_0 = 1000.0``, covering system 851's fundamental) at the
locked learning rate, window and hidden frequency — through
``register_variant`` into a NEW immutable registry, so the sealed Phase 65
catalog (exactly ``locked-12``) is never altered. ``REGISTRIES`` is the closed
name table a committed fit registration selects through its
``settings.variant_registry`` key; the harness (``diagnostic_fit``) imports
this module, so this module must never import the harness, the guard, the data
seam, the similarity logger or the launcher.

``tier1_e_max`` reads the frozen FEAS-01 scorecard's Tier-1 ``E_max`` from the
scorecard itself, never retyped, and ``classify_exp01`` is the pre-registered
EXP-01 reading rule: tier 1, the constant-predictor band, between, other, or —
for a finite non-Tier-1 run that was still improving when its steps ran out —
``unsettled``. ``improvement_check`` reads that verdict from the DIAG-09
logger's output movement (never the loss), ``read_exp01_record`` and
``read_run_directory`` turn a run's record into that reading while refusing to
read a branch from any run with a mechanical or setting problem, and
``confirm``/``route`` compute the three-run confirmation and its pre-registered
route. Every function is pure except the CLI's JSON file reads.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import sys
from datetime import datetime
from pathlib import Path
from types import MappingProxyType

from pinn.verification.diagnostic_variants import (
    REGISTRY,
    DiagnosticVariant,
    register_variant,
)

__all__ = [
    "BUDGET_RULE",
    "BRANCHES",
    "E_CONST_PREDICTED",
    "E_CONST_TOLERANCE",
    "EXP01_PARAMETERS",
    "EXP01_RUNS",
    "EXP01_VARIANT",
    "FIRST_LAYER_INPUTS",
    "FREQUENCY_CHECK",
    "IMPROVEMENT_RULE",
    "LOCKED_12_PARAMETERS",
    "NEAR_BAND",
    "PHASE66_REGISTRY",
    "REGISTRIES",
    "ROUTES",
    "classify_exp01",
    "confirm",
    "exp01_budget",
    "exp01_cadence",
    "exp01_design",
    "exp01_loss_trace_stride",
    "first_layer_frequency_bound",
    "improvement_check",
    "launch_wall_seconds",
    "loss_trace_entries",
    "main",
    "read_exp01_record",
    "read_run_directory",
    "route",
    "tier1_e_max",
]

#: The EXP-01 positive-control network (D-04, D-05, D-06): the production
#: layer types at depth 1 and width 384 (157,065 parameters, under the locked
#: 795,657), ``first_omega_0`` 1000.0 so the first layer's starting
#: time-frequency range covers the faster repeat system's fundamental, and
#: every other setting at its locked or harness value (``hidden_omega_0`` stays
#: at its locked default 1.0).
EXP01_VARIANT = DiagnosticVariant(
    name="exp01-d1-w384-o1000",
    time_features="raw_tau_ic13",
    depth=1,
    width=384,
    learning_rate=1e-4,
    window_length=10.0,
    first_omega_0=1000.0,
)

#: The Phase 66 registry: a fresh immutable copy of the sealed catalog extended
#: with EXP-01 in registration order. ``register_variant`` never alters
#: ``REGISTRY`` and refuses duplicate names.
PHASE66_REGISTRY = register_variant(EXP01_VARIANT, into=REGISTRY)

#: The closed registry-name table a registration's ``settings.variant_registry``
#: selects from. Absent or null keeps the sealed Phase 65 behaviour; anything
#: else is refused before any data access.
REGISTRIES = MappingProxyType({"phase66": PHASE66_REGISTRY})

#: D-09's numeric constant-predictor band, a pre-registered fraction either
#: side of the record's own window-mean-constant E.
NEAR_BAND = 0.05

#: The Phase 64 CPU float64 re-derivations of the window-mean-constant
#: predictor's E per EXP-01 orbit (the 1632 value equals the Phase 65 smoke
#: record's comparison row). A record's own constant-predictor score must
#: agree with its prediction to within :data:`E_CONST_TOLERANCE`, or the run
#: did not score the registered orbit's window and reads out-of-branch.
E_CONST_PREDICTED = MappingProxyType({
    "hierarchical/gold/1632": 1.1538408194255343,
    "hierarchical/gold/851": 1.233696866477104,
})
E_CONST_TOLERANCE = 1e-9

#: The production input design's width: the first layer's starting
#: time-frequency bound is ``first_omega_0 / (14 * pi)`` cycles per window.
FIRST_LAYER_INPUTS = 14

#: The step-0 first-layer bandwidth check (D-05): the logged step-0
#: ``first_layer_frequency.max`` must lie inside ``(0.95, 1.00001)`` times the
#: bound, or the variant's frequency scale never reached the network. A
#: failure is a setting problem, not a mechanical one.
FREQUENCY_CHECK = (0.95, 1.00001)

#: The improvement rule (checker blocker 1): a run is still improving when its
#: output movement at the final cadence entry exceeds its value at the last
#: cadence entry at or before 0.75 of the final step by more than 0.01 — about
#: three times the 0.0030-0.0034 at which every v2.4 network settled. The
#: signal is the DIAG-09 logger's output movement, never the loss.
IMPROVEMENT_RULE = MappingProxyType({
    "signal": "similarity.entries[*].output_movement.value",
    "reference_fraction": 0.75,
    "min_growth": 0.01,
})

#: The three pre-registered EXP-01 runs (D-07): the main run and its two
#: repeats, run whichever branch the main run lands in.
EXP01_RUNS = (
    MappingProxyType({"role": "main", "orbit_key": "hierarchical/gold/1632", "seed": 42}),
    MappingProxyType({"role": "repeat-system", "orbit_key": "hierarchical/gold/851", "seed": 42}),
    MappingProxyType({"role": "repeat-seed", "orbit_key": "hierarchical/gold/1632", "seed": 41}),
)

#: The five branch labels. ``out-of-branch`` is not one of them: it is the
#: refusal label for a run that did not test the registered network on the
#: registered orbit under the gate.
BRANCHES = ("tier1", "near", "between", "other", "unsettled")

#: The pre-registered routes (D-09, RESEARCH Pattern 5 item 6, SCOPE-47).
ROUTES = ("phase67-as-planned", "propose-66.1", "owner")

#: The EXP-01 variant's exact parameter count (CPU float64 seed-42 build) and
#: the sealed locked-12 network's, for the design block and the pages.
EXP01_PARAMETERS = 157065
LOCKED_12_PARAMETERS = 795657

#: The one budget rule (checker blocker 2): time alone sets the run length —
#: the largest step count, a multiple of ``step_quantum``, whose projected
#: wall at the ``rate_margin`` stays within ``time_fraction`` of the
#: ``cap_seconds`` (strictly below the harness's 3,600-second refusal). The
#: record size is bounded at its source (the stride and the cadence), so the
#: staged-blob limit appears only in the N-independent record-size ceiling
#: guard: it can refuse a broken input but can never shorten a run. The
#: timing-run settings are registered here too.
BUDGET_RULE = MappingProxyType({
    "cap_seconds": 3300.0,
    "time_fraction": 0.75,
    "rate_margin": 0.25,
    "size_limit_bytes": 10485760,
    "size_fraction": 0.9,
    "loss_entry_bytes": 32,
    "similarity_margin": 1.15,
    "warmup_steps": 200,
    "step_quantum": 1000,
    "cadence_head": (0, 100, 300, 1000, 3000, 10000, 30000, 100000),
    "cadence_tail_entries": 6,
    "loss_trace_entries_max": 10000,
    "timing_steps": 5200,
    "timing_warmup": 200,
    "timing_cadence": (0, 1300, 2600, 3900, 5200),
    "timing_cap_seconds": 600,
    "timing_loss_trace_stride": 1,
})


def tier1_e_max(card):
    """The frozen scorecard's Tier-1 ``E_max``, read from its own tiers section.

    The limit is read, never retyped (the Phase 64 ``_tier1_max`` precedent).
    """
    for level in card.section("tiers")["levels"]:
        if int(level["tier"]) == 1:
            return float(level["E_max"])
    raise ValueError("the scorecard names no level whose tier is 1")


def classify_exp01(e, e_const, *, tier1_max, band=NEAR_BAND, still_improving=False):
    """The pre-registered EXP-01 branch for one record's network error.

    ``e`` is the record's ``scores.network.E`` and ``e_const`` its own
    ``window_mean_constant`` comparison score; the Tier-1 limit comes from the
    frozen scorecard through :func:`tier1_e_max`. Inclusive edges, fixed by
    tests before any run; a non-finite error is ``other``. With
    ``still_improving`` — the improvement check's verdict — a finite non-Tier-1
    error is ``unsettled``: the run missed Tier 1 while its output was still
    learning to move with time when its steps ran out, so its score is not
    final, it is never confirmed, and it routes to the owner.
    """
    if not math.isfinite(e):
        return "other"
    if e <= tier1_max:
        return "tier1"
    if still_improving:
        return "unsettled"
    low, high = (1.0 - band) * e_const, (1.0 + band) * e_const
    if low <= e <= high:
        return "near"
    return "between" if e < low else "other"


def first_layer_frequency_bound(first_omega_0, inputs=FIRST_LAYER_INPUTS):
    """The first layer's starting time-frequency bound in cycles per window.

    The input layer initializes its time weight in ``U[-1/n_in, 1/n_in]`` and
    applies ``first_omega_0``, so the fastest starting frequency is
    ``first_omega_0 / (n_in * pi)`` — the same unit as the logged
    ``first_layer_frequency.max`` and a lap count.
    """
    return first_omega_0 / (inputs * math.pi)


def _movement_value(entry, which):
    """The finite output-movement value of one similarity entry."""
    try:
        value = entry["output_movement"]["value"]
    except (TypeError, KeyError, IndexError) as exc:
        raise ValueError(
            f"the {which} similarity entry carries no output movement"
        ) from exc
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(
            f"the {which} similarity entry's output movement is not a number"
        )
    if not math.isfinite(value):
        raise ValueError(
            f"the {which} similarity entry's output movement is not finite"
        )
    return float(value)


def improvement_check(entries, *, final_step, rule=IMPROVEMENT_RULE):
    """Whether the run's output movement was still growing when it ran out.

    The reference is the last cadence entry whose step is at or before
    ``reference_fraction`` of ``final_step``; the signal is the DIAG-09
    logger's output movement (``similarity.entries[*].output_movement.value``),
    never the loss. Returns ``reference_step``, ``reference_output_movement``,
    ``final_step``, ``final_output_movement``, ``growth`` (final minus
    reference), ``min_growth`` and ``still_improving`` (growth strictly greater
    than ``min_growth``). Raises ``ValueError`` when there is no final-step
    entry, or when a used value is missing or non-finite.
    """
    fraction = float(rule["reference_fraction"])
    min_growth = float(rule["min_growth"])
    threshold = fraction * final_step
    final_entry = None
    reference_entry = None
    for entry in entries:
        try:
            step = entry["step"]
        except (TypeError, KeyError, IndexError) as exc:
            raise ValueError("a similarity entry carries no step") from exc
        if step == final_step:
            final_entry = entry
        if step <= threshold and (
            reference_entry is None or step >= reference_entry["step"]
        ):
            reference_entry = entry
    if final_entry is None:
        raise ValueError(
            f"the similarity log carries no entry at the final step {final_step}"
        )
    if reference_entry is None:
        raise ValueError(
            "the similarity log carries no entry at or before the reference "
            f"fraction {fraction} of the final step {final_step}"
        )
    reference_value = _movement_value(reference_entry, "reference")
    final_value = _movement_value(final_entry, "final")
    growth = final_value - reference_value
    return {
        "reference_step": int(reference_entry["step"]),
        "reference_output_movement": reference_value,
        "final_step": int(final_step),
        "final_output_movement": final_value,
        "growth": growth,
        "min_growth": min_growth,
        "still_improving": bool(growth > min_growth),
    }


def confirm(main, repeat_system, repeat_seed):
    """Whether the main run's branch is confirmed by both repeats (D-07).

    Confirmed only when all three runs share the tier1 or the near branch;
    everything else — any disagreement, three runs that agree on between,
    other or unsettled (those labels have no pre-registered consequence), and
    any out-of-branch input — is unconfirmed and goes to the owner.
    """
    if main == repeat_system == repeat_seed and main in ("tier1", "near"):
        return "confirmed"
    return "unconfirmed"


def route(main_branch, confirmation):
    """The pre-registered route for a confirmed-or-not main branch (D-09)."""
    if main_branch == "tier1" and confirmation == "confirmed":
        return "phase67-as-planned"
    if main_branch == "near" and confirmation == "confirmed":
        return "propose-66.1"
    return "owner"


def exp01_cadence(n):
    """The bounded EXP-01 similarity cadence for an ``n``-step run.

    The registered head entries strictly below ``n``, then ``n`` itself when
    ``n`` is at most the head's last entry; above it, the
    ``cadence_tail_entries`` evenly floored points from the head's end to
    ``n``, duplicates dropped. The last tail entry is always ``n``, so a
    cadence never has more than ``len(cadence_head) + cadence_tail_entries``
    (14) entries — the record's similarity weight is bounded at every length.
    """
    head = list(BUDGET_RULE["cadence_head"])
    tail_entries = int(BUDGET_RULE["cadence_tail_entries"])
    below = [step for step in head if step < n]
    if n <= head[-1]:
        return sorted(set(below + [int(n)]))
    tail = [
        head[-1] + (k * (n - head[-1])) // tail_entries
        for k in range(1, tail_entries + 1)
    ]
    return sorted(set(below + tail))


def exp01_loss_trace_stride(n):
    """The Site F loss-trace stride: ceil(n / loss_trace_entries_max)."""
    maximum = int(BUDGET_RULE["loss_trace_entries_max"])
    return (int(n) + maximum - 1) // maximum


def loss_trace_entries(n, stride):
    """The recorded trace length for ``n`` losses at stride ``stride``.

    Exactly the length diagnostic_fit's Site F records: every stride-th loss,
    then the final loss when ``n`` is not a multiple of the stride.
    """
    return int(n) // int(stride) + (1 if int(n) % int(stride) else 0)


def launch_wall_seconds(receipt, attempt):
    """The launch-to-end wall seconds, plus the 2-second timestamp margin.

    The difference between the receipt's ``checked_utc`` and the attempt's
    ``ended_utc`` covers process start, admission, data load, setup, scoring
    and publication. Raises ``ValueError`` when a timestamp is missing or not
    ISO 8601, or when the attempt ended before the receipt was written.
    """
    try:
        checked_text = receipt["checked_utc"]
        ended_text = attempt["ended_utc"]
    except (KeyError, TypeError) as exc:
        raise ValueError(f"the run is missing the {exc} timestamp") from exc
    try:
        checked = datetime.fromisoformat(str(checked_text))
        ended = datetime.fromisoformat(str(ended_text))
    except ValueError as exc:
        raise ValueError(f"a run timestamp is not ISO 8601: {exc}") from exc
    if ended < checked:
        raise ValueError("the attempt ended before the receipt was written")
    return (ended - checked).total_seconds() + 2.0


def exp01_budget(timing_record, *, record_bytes, launch_wall_seconds, rule=BUDGET_RULE):
    """The step count for one EXP-01 run, set by time alone (D-08).

    ``timing_record`` is the registered timing run's record; ``record_bytes``
    its record's byte length and ``launch_wall_seconds`` its
    :func:`launch_wall_seconds` value. The projected wall for ``N`` steps is
    the fixed cost (the launch wall minus the record's own warmup, measured
    and logging seconds) plus the warmup, plus the measured steps at the
    timing run's per-step rate with the ``rate_margin``, plus the cadence
    logging cost. ``N`` is the largest multiple of ``step_quantum`` whose
    wall stays within ``time_fraction`` of ``cap_seconds`` — the only bound.
    The record-size ceiling (which does not depend on ``N``) refuses a broken
    input above ``size_fraction`` of ``size_limit_bytes`` but can never
    shorten a run. Raises ``ValueError`` for an incomplete record, a missing
    timing field, a non-positive rate, a negative fixed cost, no feasible N
    above the warmup, or an over-limit ceiling. Holds no score, similarity
    value or loss value.
    """
    if timing_record.get("status") != "complete":
        raise ValueError("the timing record is not complete")
    timing = timing_record.get("timing") or {}
    phases = timing.get("phases") or {}
    try:
        seconds_per_step = float(timing["seconds_per_step"])
        warmup_seconds = float(timing["warmup_seconds"])
        measured_seconds = float(timing["measured_seconds"])
        logging_seconds = float(phases["logging_seconds"])
    except KeyError as exc:
        raise ValueError(f"the timing record carries no {exc} field") from exc
    similarity = timing_record.get("similarity") or {}
    entries = similarity.get("entries") or []
    timing_entries = len(entries)
    if timing_entries <= 0:
        raise ValueError("the timing record carries no similarity entries")
    entry_bytes = len(json.dumps(similarity, indent=2, sort_keys=True)) / timing_entries
    loss_trace_length = len((timing_record.get("loss") or {}).get("trace") or [])
    if seconds_per_step <= 0:
        raise ValueError("the timing record's measured rate is not positive")
    fixed_wall = float(launch_wall_seconds) - (
        warmup_seconds + measured_seconds + logging_seconds
    )
    if fixed_wall < 0:
        raise ValueError(
            "the timing record's fixed cost is negative: the launch wall is "
            "shorter than the record's own warmup, measured and logging seconds"
        )
    cap = float(rule["cap_seconds"])
    target = float(rule["time_fraction"]) * cap
    quantum = int(rule["step_quantum"])
    warmup_steps = int(rule["warmup_steps"])
    margin = float(rule["rate_margin"])
    logging_per_entry = logging_seconds / timing_entries

    def projected_wall(steps):
        return (
            fixed_wall
            + warmup_seconds
            + (steps - warmup_steps) * seconds_per_step * (1.0 + margin)
            + len(exp01_cadence(steps)) * logging_per_entry
        )

    low = 1
    if projected_wall(low * quantum) > target:
        raise ValueError(
            "no feasible step count above the warmup stays within the time "
            "fraction of the cap"
        )
    high = 2
    while projected_wall(high * quantum) <= target:
        low = high
        high *= 2
    while high - low > 1:
        middle = (low + high) // 2
        if projected_wall(middle * quantum) <= target:
            low = middle
        else:
            high = middle
    steps = low * quantum
    stride = exp01_loss_trace_stride(steps)
    cadence = exp01_cadence(steps)
    cadence_max = len(BUDGET_RULE["cadence_head"]) + int(BUDGET_RULE["cadence_tail_entries"])
    per_entry = math.ceil(float(rule["similarity_margin"]) * entry_bytes)
    projected_bytes = int(record_bytes) + int(rule["loss_entry_bytes"]) * max(
        0, loss_trace_entries(steps, stride) - loss_trace_length
    ) + per_entry * max(0, len(cadence) - timing_entries)
    ceiling = int(record_bytes) + int(rule["loss_entry_bytes"]) * max(
        0,
        int(rule["loss_trace_entries_max"]) + 1 - loss_trace_length,
    ) + per_entry * max(0, cadence_max - timing_entries)
    size_limit = int(rule["size_limit_bytes"])
    size_fraction = float(rule["size_fraction"])
    if ceiling > size_fraction * size_limit:
        raise ValueError(
            "the record-size ceiling exceeds the staged-blob limit "
            f"({ceiling} > {size_fraction * size_limit} bytes): the timing "
            "record's similarity block is too large for any run length"
        )
    return {
        "optimizer_steps": int(steps),
        "warmup_steps": warmup_steps,
        "measured_steps": int(steps - warmup_steps),
        "similarity_cadence": cadence,
        "loss_trace_stride": int(stride),
        "whole_run_cap_seconds": cap,
        "projected_wall_seconds": projected_wall(steps),
        "projected_record_bytes": projected_bytes,
        "record_bytes_ceiling": ceiling,
        "size_limit_bytes": size_limit,
        "size_fraction": size_fraction,
        "limit_source": "scripts/git_policy/validate_staged_paths.py",
        "inputs": {
            "seconds_per_step": seconds_per_step,
            "warmup_seconds": warmup_seconds,
            "measured_seconds": measured_seconds,
            "logging_seconds": logging_seconds,
            "similarity_entries": timing_entries,
            "similarity_bytes_per_entry": entry_bytes,
            "loss_trace_entries": loss_trace_length,
            "record_bytes": int(record_bytes),
            "launch_wall_seconds": float(launch_wall_seconds),
            "fixed_wall_seconds": fixed_wall,
            "time_fraction": float(rule["time_fraction"]),
            "rate_margin": margin,
            "step_quantum": quantum,
        },
    }


def exp01_design():
    """The frozen EXP-01 design block the pages embed (JSON-normal).

    Every sequence is a list and every key a string, so
    ``json.loads(json.dumps(exp01_design())) == exp01_design()`` and the
    DESIGN-OK check and the page tests compare content. This block is fixed
    before the timing run; the pages repeat it verbatim (SCOPE-47).
    """
    budget_rule = dict(BUDGET_RULE)
    budget_rule["cadence_head"] = list(BUDGET_RULE["cadence_head"])
    budget_rule["timing_cadence"] = list(BUDGET_RULE["timing_cadence"])
    return {
        "experiment": "EXP-01",
        "variant": dict(EXP01_VARIANT.to_json_dict()),
        "variant_registry": "phase66",
        "parameters": EXP01_PARAMETERS,
        "locked_12_parameters": LOCKED_12_PARAMETERS,
        "first_layer_inputs": FIRST_LAYER_INPUTS,
        "first_layer_frequency_bound": first_layer_frequency_bound(1000.0),
        "runtime": {"dtype": "float32", "device": "mps"},
        "optimizer": {"kind": "adam_constant_rate", "lr": 0.0001},
        "loss": "data_only",
        "physical_window": [0.0, 10.0],
        "runs": [dict(spec) for spec in EXP01_RUNS],
        "reading_rule": {
            "tier1": "pinn/verification/artifacts/feasibility_scorecard_v1.json",
            "near_band": NEAR_BAND,
            "e_const_source": "comparisons[comparison=window_mean_constant].score.E",
            "e_const_predicted": dict(E_CONST_PREDICTED),
            "e_const_tolerance": E_CONST_TOLERANCE,
            "frequency_check": list(FREQUENCY_CHECK),
            "branches": list(BRANCHES),
            "improvement": dict(IMPROVEMENT_RULE),
            "confirmation": "confirmed only when all three runs share tier1 or near",
            "routes": {
                "confirmed tier1": "phase67-as-planned",
                "confirmed near": "propose-66.1",
                "otherwise": "owner",
            },
        },
        "budget_rule": budget_rule,
    }


#: The value-free mechanical problem strings. None of them embeds a score
#: value (E, tier, eps_h, E_const, an output movement or a loss), so the
#: check-run CLI can print them without showing the timing run's score.
_PROBLEM_STATUS = "the run status is not complete"
_PROBLEM_TIER = "the recorded scorecard grade disagrees with the network error"
_PROBLEM_E_CONST = (
    "the record's constant-predictor score disagrees with its predicted value"
)
_PROBLEM_ROWS = "the similarity log carries rows other than input and h1"
_PROBLEM_IMPROVEMENT = "the improvement check cannot be evaluated"
_PROBLEM_REGISTRY = "the record's variant registry fields are wrong"
_PROBLEM_SPLITS = "a validation or test split was opened"
_PROBLEM_RECEIPT_MISSING = "the power-gate receipt is missing"
_PROBLEM_RECEIPT_UNREADABLE = "the power-gate receipt is not readable JSON"
_PROBLEM_RECEIPT_SCHEMA = "the receipt schema is not phase66-power-gate/v1"
_PROBLEM_RECEIPT_SOURCE = "the receipt does not record AC Power"
_PROBLEM_RECEIPT_WINDOW = "the receipt window is outside the weekend window"
_PROBLEM_RECEIPT_LATE = "the receipt was written after the attempt started"
_PROBLEM_ATTEMPT_MISSING = "the attempt claim is missing"
_PROBLEM_ATTEMPT_UNREADABLE = "the attempt claim is not readable JSON"
_PROBLEM_ATTEMPT_STATUS = "the attempt is not published"
_PROBLEM_ATTEMPT_DIGEST = (
    "the attempt's record digest disagrees with the record bytes"
)
_SETTING_BANDWIDTH = "the step-0 first-layer bandwidth check failed"

_RECEIPT_SCHEMA = "phase66-power-gate/v1"
_WINDOW_TIMEZONE = "America/Chicago"
_WINDOW_SUNDAY_LAST_HOUR = 22


def read_exp01_record(record, *, tier1_max):
    """One record's mechanical and setting reading; pure.

    Returns the run's identity (``run_id``, ``orbit_key`` from
    ``orbit.train.record_key``, ``seed``, ``registration_sha256``), its scores
    (``E``, ``tier``, ``eps_h``, ``E_const`` from the record's own
    ``window_mean_constant`` row, ``two_kepler``), the similarity context (the
    final output movement, the h1 cosine trace, the step-0 and final
    first-layer frequencies), the improvement check over the record's entries,
    the value-free ``mechanical_problems`` and ``setting_problems`` lists, and
    the two labels: ``e_band`` (classify on E alone) and ``branch`` —
    out-of-branch when any mechanical problem (or a setting problem on a
    Tier-1 fit) stands, otherwise the classify verdict under the improvement
    check. A branch is never read from a run that did not test the registered
    network on the registered orbit (D-10).
    """
    problems = []
    if record.get("status") != "complete":
        problems.append(_PROBLEM_STATUS)
    variant = record.get("variant") or {}
    if variant.get("registered") is not True or variant.get("registry") not in REGISTRIES:
        problems.append(_PROBLEM_REGISTRY)
    network = (record.get("scores") or {}).get("network") or {}
    e = network.get("E")
    tier = network.get("tier")
    eps_h = network.get("eps_h")
    e_is_number = (
        not isinstance(e, bool) and isinstance(e, (int, float)) and math.isfinite(e)
    )
    tier_is_number = not isinstance(tier, bool) and isinstance(tier, int)
    if not (e_is_number and tier_is_number):
        problems.append(_PROBLEM_TIER)
    elif e <= tier1_max and tier < 1:
        problems.append(_PROBLEM_TIER)
    elif e > tier1_max and tier != 0:
        problems.append(_PROBLEM_TIER)
    orbit_key = ((record.get("orbit") or {}).get("train") or {}).get("record_key")
    seed = record.get("seed")
    registration_sha256 = (record.get("registration") or {}).get("sha256")
    e_const = None
    two_kepler = None
    for row in record.get("comparisons") or []:
        if not isinstance(row, dict):
            continue
        if row.get("comparison") == "window_mean_constant":
            e_const = (row.get("score") or {}).get("E")
        elif row.get("comparison") == "two_kepler":
            if row.get("applicable") is True:
                two_kepler = (row.get("score") or {}).get("E")
            else:
                two_kepler = row.get("reason")
    predicted = (
        E_CONST_PREDICTED.get(orbit_key) if isinstance(orbit_key, str) else None
    )
    if predicted is not None:
        const_ok = (
            not isinstance(e_const, bool)
            and isinstance(e_const, (int, float))
            and math.isfinite(e_const)
            and abs(float(e_const) - predicted) <= E_CONST_TOLERANCE
        )
        if not const_ok:
            problems.append(_PROBLEM_E_CONST)
    similarity = record.get("similarity") or {}
    entries = similarity.get("entries") or []
    if any(
        [layer.get("name") for layer in (entry.get("layers") or [])] != ["input", "h1"]
        for entry in entries
    ):
        problems.append(_PROBLEM_ROWS)
    access = record.get("access") or {}
    reads = access.get("reads") or {}
    attestation = access.get("attestation") or {}
    attestation_opened = attestation.get("opened") or {}
    split_opens = sum(
        int(block.get(key, 0) or 0)
        for block in (reads, attestation, attestation_opened)
        for key in ("validation", "test", "test_split_opened")
        if key in block
    )
    if split_opens:
        problems.append(_PROBLEM_SPLITS)
    steps_completed = (record.get("steps") or {}).get("completed")
    improvement = None
    try:
        improvement = improvement_check(entries, final_step=steps_completed)
    except (TypeError, ValueError):
        problems.append(_PROBLEM_IMPROVEMENT)
    h1_cosine_trace = [
        {
            "step": int(entry.get("step")),
            "adjacent_cosine_mean": float(layer.get("adjacent_cosine_mean")),
        }
        for entry in entries
        for layer in (entry.get("layers") or [])
        if layer.get("name") == "h1"
    ]
    step0_entry = next((item for item in entries if item.get("step") == 0), None)
    final_entry = next(
        (item for item in entries if item.get("step") == steps_completed), None
    )
    first_layer_frequency = {
        "step_0": (
            (step0_entry.get("first_layer_frequency") or {}).get("max")
            if step0_entry is not None else None
        ),
        "final": (
            (final_entry.get("first_layer_frequency") or {}).get("max")
            if final_entry is not None else None
        ),
    }
    output_movement_final = (
        (entries[-1].get("output_movement") or {}).get("value") if entries else None
    )
    setting_problems = []
    first_omega_0 = variant.get("first_omega_0")
    step0_max = first_layer_frequency["step_0"]
    frequency_ok = (
        not isinstance(first_omega_0, bool)
        and isinstance(first_omega_0, (int, float))
        and not isinstance(step0_max, bool)
        and isinstance(step0_max, (int, float))
    )
    if frequency_ok:
        bound = first_layer_frequency_bound(float(first_omega_0))
        low, high = FREQUENCY_CHECK[0] * bound, FREQUENCY_CHECK[1] * bound
        frequency_ok = low <= step0_max <= high
    if not frequency_ok:
        setting_problems.append(_SETTING_BANDWIDTH)
    e_band = (
        classify_exp01(e, e_const, tier1_max=tier1_max)
        if e_is_number and isinstance(e_const, (int, float))
        else None
    )
    if problems:
        branch = "out-of-branch"
    elif setting_problems and e_is_number and e <= tier1_max:
        # A Tier-1 fit from a network the run did not register (D-05).
        branch = "out-of-branch"
    else:
        still = bool(
            (improvement is not None and improvement["still_improving"])
            or setting_problems
        )
        branch = classify_exp01(
            e, e_const, tier1_max=tier1_max, still_improving=still
        )
    return {
        "run_id": record.get("run_id"),
        "orbit_key": orbit_key,
        "seed": seed,
        "registration_sha256": registration_sha256,
        "E": e,
        "tier": tier,
        "eps_h": eps_h,
        "E_const": e_const,
        "two_kepler": two_kepler,
        "output_movement_final": output_movement_final,
        "h1_cosine_trace": h1_cosine_trace,
        "first_layer_frequency": first_layer_frequency,
        "loss_final": (record.get("loss") or {}).get("final"),
        "steps_completed": steps_completed,
        "seconds_per_step": (record.get("timing") or {}).get("seconds_per_step"),
        "improvement": improvement,
        "mechanical_problems": problems,
        "setting_problems": setting_problems,
        "e_band": e_band,
        "branch": branch,
    }


def read_run_directory(path, *, tier1_max):
    """One run directory's reading: the record plus the receipt and attempt.

    Reads ``record.json``, ``attempt.json`` and ``power-gate.json`` from
    ``path`` and adds the run-identity checks to the record's mechanical
    problems: the receipt exists with the phase66 schema and ``AC Power``,
    its window block names America/Chicago on a Saturday or a Sunday before
    22:00 local, its ``checked_utc`` is not later than the attempt's
    ``started_utc``, the attempt is published, and its ``record_sha256``
    equals the SHA-256 of the record bytes. A missing ``record.json`` raises
    (the directory is unreadable, not merely suspect); every other failure is
    a value-free mechanical problem, and a run with any mechanical problem
    reads out-of-branch.
    """
    directory = Path(path)
    record_raw = (directory / "record.json").read_bytes()
    record = json.loads(record_raw.decode("utf-8"))
    reading = read_exp01_record(record, tier1_max=tier1_max)
    problems = reading["mechanical_problems"]
    receipt = None
    receipt_path = directory / "power-gate.json"
    if not receipt_path.is_file():
        problems.append(_PROBLEM_RECEIPT_MISSING)
    else:
        try:
            receipt = json.loads(receipt_path.read_bytes().decode("utf-8"))
        except (UnicodeDecodeError, ValueError):
            problems.append(_PROBLEM_RECEIPT_UNREADABLE)
        if isinstance(receipt, dict):
            if receipt.get("schema") != _RECEIPT_SCHEMA:
                problems.append(_PROBLEM_RECEIPT_SCHEMA)
            if receipt.get("power_source") != "AC Power":
                problems.append(_PROBLEM_RECEIPT_SOURCE)
            window = receipt.get("window") or {}
            window_ok = False
            try:
                local = datetime.fromisoformat(str(window.get("local_time")))
                weekday = window.get("isoweekday")
                window_ok = (
                    window.get("timezone") == _WINDOW_TIMEZONE
                    and (
                        weekday == 6
                        or (weekday == 7 and local.hour < _WINDOW_SUNDAY_LAST_HOUR)
                    )
                )
            except ValueError:
                window_ok = False
            if not window_ok:
                problems.append(_PROBLEM_RECEIPT_WINDOW)
        elif receipt is not None:
            problems.append(_PROBLEM_RECEIPT_UNREADABLE)
    attempt = None
    attempt_path = directory / "attempt.json"
    if not attempt_path.is_file():
        problems.append(_PROBLEM_ATTEMPT_MISSING)
    else:
        try:
            attempt = json.loads(attempt_path.read_bytes().decode("utf-8"))
        except (UnicodeDecodeError, ValueError):
            problems.append(_PROBLEM_ATTEMPT_UNREADABLE)
        if not isinstance(attempt, dict):
            problems.append(_PROBLEM_ATTEMPT_UNREADABLE)
            attempt = None
    if attempt is not None:
        if attempt.get("status") != "published":
            problems.append(_PROBLEM_ATTEMPT_STATUS)
        if attempt.get("record_sha256") != hashlib.sha256(record_raw).hexdigest():
            problems.append(_PROBLEM_ATTEMPT_DIGEST)
        if receipt is not None:
            try:
                checked = datetime.fromisoformat(str(receipt.get("checked_utc")))
                started = datetime.fromisoformat(str(attempt.get("started_utc")))
            except ValueError:
                problems.append(_PROBLEM_RECEIPT_LATE)
            else:
                if checked > started:
                    problems.append(_PROBLEM_RECEIPT_LATE)
    if problems:
        reading["branch"] = "out-of-branch"
    return reading


# --------------------------------------------------------------------------
# Plan 66-02: the read-run, check-run and review CLI (pure readers; the only
# file access is reading the run directories' JSON, and the scorecard is
# loaded inside main only).
# --------------------------------------------------------------------------


def _tier1_max_from_scorecard():
    """The frozen scorecard's Tier-1 limit, read once per CLI invocation."""
    from pinn.verification.feasibility_scorecard import load_scorecard

    return tier1_e_max(load_scorecard())


def _cmd_read_run(dir_path):
    reading = read_run_directory(dir_path, tier1_max=_tier1_max_from_scorecard())
    print(json.dumps(reading, indent=2, sort_keys=True))
    problems = reading["mechanical_problems"] + reading["setting_problems"]
    if problems:
        print("EXP01-RUN-PROBLEMS: " + "; ".join(problems))
        return 2
    print("EXP01-RUN-OK")
    return 0


def _cmd_check_run(dir_path):
    reading = read_run_directory(dir_path, tier1_max=_tier1_max_from_scorecard())
    print(json.dumps(
        {
            "dir": dir_path,
            "mechanical_problems": reading["mechanical_problems"],
            "setting_problems": reading["setting_problems"],
        },
        indent=2,
        sort_keys=True,
    ))
    problems = reading["mechanical_problems"] + reading["setting_problems"]
    if problems:
        print("EXP01-CHECK-PROBLEMS: " + "; ".join(problems))
        return 2
    print("EXP01-CHECK-OK")
    return 0


def _cmd_design():
    print(json.dumps(exp01_design(), indent=2, sort_keys=True))
    return 0


def _cmd_budget(timing_dir):
    """The timing directory's budget, without its score (warning 4)."""
    directory = Path(timing_dir)
    raw = (directory / "record.json").read_bytes()
    record = json.loads(raw.decode("utf-8"))
    receipt = json.loads((directory / "power-gate.json").read_bytes().decode("utf-8"))
    attempt = json.loads((directory / "attempt.json").read_bytes().decode("utf-8"))
    wall = launch_wall_seconds(receipt, attempt)
    budget = exp01_budget(record, record_bytes=len(raw), launch_wall_seconds=wall)
    print(json.dumps(budget, indent=2, sort_keys=True))
    print(
        f"EXP01-BUDGET steps={budget['optimizer_steps']} "
        f"loss_trace_stride={budget['loss_trace_stride']} "
        f"cap={budget['whole_run_cap_seconds']}"
    )
    return 0


def _run_identity(reading):
    """A run's identity triple: (orbit_key, seed, registration_sha256)."""
    return (reading["orbit_key"], reading["seed"], reading["registration_sha256"])


def _cmd_review(main_dir, repeat_system_dir, repeat_seed_dir):
    tier1_max = _tier1_max_from_scorecard()
    roles = {
        "main": main_dir,
        "repeat-system": repeat_system_dir,
        "repeat-seed": repeat_seed_dir,
    }
    readings = {
        role: read_run_directory(path, tier1_max=tier1_max)
        for role, path in roles.items()
    }
    seen = {}
    for role in ("main", "repeat-system", "repeat-seed"):
        identity = _run_identity(readings[role])
        if identity in seen:
            print(
                "EXP01-REFUSED: the "
                f"{role} directory {roles[role]} is the same run as the "
                f"{seen[identity]} directory: orbit "
                f"{identity[0]}, seed {identity[1]}, registration "
                f"{identity[2]}",
                file=sys.stderr,
            )
            return 2
        seen[identity] = role
    for spec in EXP01_RUNS:
        reading = readings[spec["role"]]
        if (
            reading["orbit_key"] != spec["orbit_key"]
            or reading["seed"] != spec["seed"]
        ):
            print(
                f"EXP01-REFUSED: the {spec['role']} directory "
                f"{roles[spec['role']]} holds orbit {reading['orbit_key']} at "
                f"seed {reading['seed']}; the pre-registered run is orbit "
                f"{spec['orbit_key']} at seed {spec['seed']}",
                file=sys.stderr,
            )
            return 2
    branches = {role: reading["branch"] for role, reading in readings.items()}
    confirmation = confirm(
        branches["main"], branches["repeat-system"], branches["repeat-seed"]
    )
    route_to = route(branches["main"], confirmation)
    runs = {
        role: {
            "dir": str(roles[role]),
            "run_id": readings[role]["run_id"],
            "orbit_key": readings[role]["orbit_key"],
            "seed": readings[role]["seed"],
            "registration_sha256": readings[role]["registration_sha256"],
            "branch": branches[role],
        }
        for role in ("main", "repeat-system", "repeat-seed")
    }
    print(json.dumps(
        {"runs": runs, "confirmation": confirmation, "route": route_to},
        indent=2,
        sort_keys=True,
    ))
    print(f"EXP01-REVIEW confirmation={confirmation} route={route_to}")
    return 0


def main(argv=None):
    """The Phase 66 CLI: ``read-run``, ``check-run``, ``review``, ``budget``.

    ``design`` prints the frozen design block. Exit codes: 0 when the
    directories were readable (an owner route is a valid review result), 2 for
    an unknown command, missing flags, or unreadable, duplicated or
    wrong-role input. The scorecard is loaded here, never at import.
    """
    parser = argparse.ArgumentParser(
        prog="diagnostic_phase66",
        description=(
            "The EXP-01 reading rule: read one run, check one run without its "
            "score, review the three pre-registered runs, size the budget from "
            "the timing run, or print the frozen design block."
        ),
    )
    commands = parser.add_subparsers(dest="command")
    read_run = commands.add_parser("read-run")
    read_run.add_argument("--dir", required=False)
    check_run = commands.add_parser("check-run")
    check_run.add_argument("--dir", required=False)
    review = commands.add_parser("review")
    review.add_argument("--main", required=False)
    review.add_argument("--repeat-system", required=False)
    review.add_argument("--repeat-seed", required=False)
    budget = commands.add_parser("budget")
    budget.add_argument("--timing-dir", required=False)
    commands.add_parser("design")
    try:
        args = parser.parse_args(argv)
    except SystemExit as exc:  # argparse's own usage error carries exit code 2
        return int(exc.code) if isinstance(exc.code, int) else 2
    required = {
        "read-run": ("dir",),
        "check-run": ("dir",),
        "review": ("main", "repeat_system", "repeat_seed"),
        "budget": ("timing_dir",),
        "design": (),
    }
    if args.command not in required:
        print(
            "EXP01-REFUSED: choose read-run, check-run, review, budget or design",
            file=sys.stderr,
        )
        return 2
    missing = [
        f"--{name.replace('_', '-')}"
        for name in required[args.command]
        if getattr(args, name) is None
    ]
    if missing:
        print(
            f"EXP01-REFUSED: missing required flags: {', '.join(missing)}",
            file=sys.stderr,
        )
        return 2
    try:
        if args.command == "read-run":
            return _cmd_read_run(args.dir)
        if args.command == "check-run":
            return _cmd_check_run(args.dir)
        if args.command == "budget":
            return _cmd_budget(args.timing_dir)
        if args.command == "design":
            return _cmd_design()
        return _cmd_review(args.main, args.repeat_system, args.repeat_seed)
    except (OSError, ValueError) as exc:
        print(f"EXP01-REFUSED: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
