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
    "BRANCHES",
    "E_CONST_PREDICTED",
    "E_CONST_TOLERANCE",
    "EXP01_RUNS",
    "EXP01_VARIANT",
    "FIRST_LAYER_INPUTS",
    "FREQUENCY_CHECK",
    "IMPROVEMENT_RULE",
    "NEAR_BAND",
    "PHASE66_REGISTRY",
    "REGISTRIES",
    "ROUTES",
    "classify_exp01",
    "confirm",
    "first_layer_frequency_bound",
    "improvement_check",
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
    """The Phase 66 reading CLI: ``read-run``, ``check-run`` and ``review``.

    Exit codes: 0 when the directories were readable (an owner route is a
    valid review result), 2 for an unknown command, missing flags, or
    unreadable, duplicated or wrong-role input. The scorecard is loaded here,
    never at import.
    """
    parser = argparse.ArgumentParser(
        prog="diagnostic_phase66",
        description=(
            "The EXP-01 reading rule: read one run, check one run without its "
            "score, or review the three pre-registered runs."
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
    try:
        args = parser.parse_args(argv)
    except SystemExit as exc:  # argparse's own usage error carries exit code 2
        return int(exc.code) if isinstance(exc.code, int) else 2
    required = {
        "read-run": ("dir",),
        "check-run": ("dir",),
        "review": ("main", "repeat_system", "repeat_seed"),
    }
    if args.command not in required:
        print(
            "EXP01-REFUSED: choose read-run, check-run or review",
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
        return _cmd_review(args.main, args.repeat_system, args.repeat_seed)
    except (OSError, ValueError) as exc:
        print(f"EXP01-REFUSED: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
