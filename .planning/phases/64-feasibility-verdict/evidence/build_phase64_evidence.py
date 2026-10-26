#!/usr/bin/env python3
"""Phase 64: producer of the verdict's number manifest.

Every number the feasibility verdict and the owner charter will quote is written
here, once, into ``evidence/numbers.json``: its value, the token the document
will render, the rendering rule, the label that says where it came from, the
source (a committed file and key, a formula, a citation, or the weights a CPU
re-derivation read), the derivation in one sentence, and which documents need
it. ``verify_phase64_verdict.py`` recomputes every entry with its own code; this
producer never imports its checker, and the checker never imports this module.

Two labels separate what the accelerator wrote from what this Mac computes:
``official-mps-float32`` is read from a record's result block, and
``rederived-cpu-float64`` is computed here from the committed weights. The two
are never compared with each other: the CPU value is checked against the
record's own ``cross_check`` block instead.

Nothing is trained, tuned or launched. The CPU re-derivation re-scores weights
that were already committed, read-only, through the Phase 59 allowlist; the open
attestation must show zero test-split, validation, other, blocked and refused
opens.

Usage, from the repository root::

    build_phase64_evidence.py numbers            write evidence/numbers.json
    build_phase64_evidence.py numbers --check    regenerate and compare bytes

``--check`` runs in a second process: it rebuilds the whole manifest (including
the CPU re-derivation) and compares the canonical bytes with the committed file,
so a value that depends on process state cannot pass as reproducible.
"""

from __future__ import annotations

import argparse
import hashlib
import math
import os
import sys
from decimal import Decimal
from pathlib import Path
from typing import Any, Mapping, Optional, Sequence

if __package__ in (None, ""):
    _ROOT = Path(__file__).resolve().parents[4]
    if str(_ROOT) not in sys.path:
        sys.path.insert(0, str(_ROOT))

REPO_ROOT = Path(__file__).resolve().parents[4]
PHASE_REL = Path(".planning/phases/64-feasibility-verdict")
EVIDENCE_REL = PHASE_REL / "evidence"
NUMBERS_REL = EVIDENCE_REL / "numbers.json"
P60_EVIDENCE_REL = Path(".planning/phases/60-single-system-learnability/evidence")
P59_EVIDENCE_REL = Path(".planning/phases/59-read-only-baseline-scorecard/evidence")
SCORECARD_REL = Path("pinn/verification/artifacts/feasibility_scorecard_v1.json")
HANDOFF_REL = P60_EVIDENCE_REL / "g2" / "stop-handoff.json"
RESEARCH_REL = PHASE_REL / "64-RESEARCH.md"
RESEARCH_COMMIT = "7fda0a55fc84447ea17abbb4d1188761add94d8a"
BASELINES_REL = P59_EVIDENCE_REL / "baselines" / "baselines.json"
SURVEY_REL = P59_EVIDENCE_REL / "survey" / "survey.json"
PICKS_REL = P59_EVIDENCE_REL / "survey" / "picks.json"
CENSUS_REL = P59_EVIDENCE_REL / "census" / "census.json"
STATUS_REL = Path("runs/stage0-v23g7-seed42/status.json")
GAPS_REL = Path(".planning/phases/59-read-only-baseline-scorecard/59-GAPS.md")
PROJECT_REL = Path(".planning/PROJECT.md")
AMENDMENTS_REL = Path(
    "docs/work/designs/cross_cutting/v2.4-milestone-proposal/"
    "2026-10-11-v2.4-feasibility-amendments.md"
)
# Each cited source pinned at its last commit before this plan ran.
GAPS_COMMIT = "ec2853b0f445d28ac462afd7cc4d395961934da7"
PROJECT_COMMIT = "bb323a52a7eab24e401d3bdc903a5e01528fcbc0"
AMENDMENTS_COMMIT = "e72060daf0de7b31334ccb7fddf8876d8506c27f"

SCHEMA = "phase64-numbers/v1"
PRODUCER_REL = (EVIDENCE_REL / "build_phase64_evidence.py").as_posix()

# The seven arms the ladder actually ran, in handoff order. Every per-arm list
# in the manifest follows this order, and every exactly compared float sum goes
# through ordered_sum over it.
ARMS = (
    "r1-1632",
    "r1-851",
    "r1-4658",
    "g2s-1632-w060",
    "g2s-1632-w120",
    "g2s-1632-w240",
    "g2s-1632-w480",
)
RUNG1_ARMS = ARMS[:3]
SWEEP_ARMS = ARMS[3:]

# The five labels an entry may carry. official-mps-float32 and committed-record
# are read from a committed file; arithmetic is computed from committed values;
# cited is a published or gap figure pinned to a commit; rederived-cpu-float64 is
# computed here from committed weights.
LABELS = (
    "official-mps-float32",
    "rederived-cpu-float64",
    "committed-record",
    "arithmetic",
    "cited",
)

# The rendering rules, stated once. Every token is Python format() on the IEEE
# double, so the verifier's own copy of these rules re-renders the same string.
RENDER_RULES = (
    "E4",
    "F0",
    "F1",
    "F2",
    "F3",
    "F5",
    "F6",
    "INT",
    "EPS",
    "POW10",
    "SCI2",
    "PCT0",
    "OFN",
    "STR",
    "BOOL",
    "LIT",
)

# This file and every pinned module it imports, by repo-relative path. The
# verifier requires each recorded digest to equal the file on disk, so a producer
# edited after writing the manifest fails closed.
PRODUCER_MODULES = (
    PRODUCER_REL,
    "pinn/architecture_spec.py",
    "pinn/network.py",
    "pinn/verification/diagnostic_architecture.py",
    "pinn/verification/evidence_io.py",
    "pinn/verification/feasibility_scorer.py",
    "pinn/verification/feasibility_scorecard.py",
    "pinn/verification/learnability_arms.py",
    "pinn/verification/learnability_data.py",
    "pinn/verification/learnability_run.py",
)

_SUPERSCRIPT = {
    "0": "\u2070",
    "1": "\u00b9",
    "2": "\u00b2",
    "3": "\u00b3",
    "4": "\u2074",
    "5": "\u2075",
    "6": "\u2076",
    "7": "\u2077",
    "8": "\u2078",
    "9": "\u2079",
    "-": "\u207b",
}


class ProducerError(RuntimeError):
    """Fail-closed producer error: nothing is written."""


def fail(message: str) -> None:
    raise ProducerError(f"build_phase64_evidence FAIL-CLOSED: {message}")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def ordered_sum(values: Any) -> float:
    """Left-to-right float sum, starting at ``0.0``, in the order given.

    The producer's own copy of the verifier's summation loop (it never imports
    its checker). Builtin ``sum()`` is not interpreter-neutral: CPython 3.12
    changed float ``sum()`` to compensated summation, which on the seven Phase 60
    wall-hour values returns one ulp below the sealed total. ``math.fsum`` and a
    sorted order disagree too. Every exactly compared float sum goes through
    this helper over the arms in handoff order, so the two programs agree to the
    bit and ``hours.total`` equals the handoff's ``total_wall_hours`` exactly.
    """
    total = 0.0
    for value in values:
        total += value
    return total


def _real(value: Any, rule: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        fail(f"render rule {rule} needs a real number, got {value!r}")
    number = float(value)
    if not math.isfinite(number):
        fail(f"render rule {rule} needs a finite number, got {value!r}")
    return number


def _superscript(exponent: int) -> str:
    try:
        return "".join(_SUPERSCRIPT[character] for character in str(int(exponent)))
    except KeyError as exc:  # pragma: no cover - the table covers every digit and '-'
        fail(f"cannot render the exponent {exponent!r}: {exc}")


def _power_of_ten(value: Any) -> int:
    """The exponent when ``value`` is the double nearest an exact power of ten."""
    number = _real(value, "POW10")
    if number <= 0.0:
        fail(f"render rule POW10 needs a positive number, got {value!r}")
    exponent = int(round(math.log10(number)))
    if Decimal(repr(number)) != Decimal(10) ** exponent:
        fail(f"render rule POW10 needs an exact power of ten, got {value!r}")
    return exponent


def _scientific(value: Any) -> str:
    """``a.bc × 10ⁿ``: two decimals, mantissa in [1, 10), Unicode exponent."""
    number = _real(value, "SCI2")
    if number <= 0.0:
        fail(f"render rule SCI2 needs a positive number, got {value!r}")
    exponent = int(math.floor(math.log10(number)))
    mantissa = number / (10.0**exponent)
    if round(mantissa, 2) >= 10.0:
        exponent += 1
        mantissa = number / (10.0**exponent)
    return f"{mantissa:.2f} \u00d7 10{_superscript(exponent)}"


def _ofn(value: Any) -> str:
    if (
        not isinstance(value, (list, tuple))
        or len(value) != 2
        or isinstance(value[0], bool)
        or isinstance(value[1], bool)
        or not isinstance(value[0], int)
        or not isinstance(value[1], int)
    ):
        fail(f"render rule OFN needs [count, total] as two ints, got {value!r}")
    return f"{value[0]} of {value[1]}"


def render(value: Any, rule: str) -> str:
    """The document token for ``value`` under ``rule``. Unknown rules fail closed."""
    if rule == "E4":
        return f"{_real(value, rule):.4f}"
    if rule in {"F0", "F1", "F2", "F3", "F5", "F6"}:
        decimals = int(rule[1:])
        return f"{_real(value, rule):.{decimals}f}"
    if rule == "INT":
        if isinstance(value, bool) or not isinstance(value, int):
            fail(f"render rule INT needs an int, got {value!r}")
        return f"{value:,}"
    if rule == "EPS":
        number = _real(value, rule)
        return f"{number:.2f}" if number < 1000.0 else f"{number:,.1f}"
    if rule == "POW10":
        return f"10{_superscript(_power_of_ten(value))}"
    if rule == "SCI2":
        return _scientific(value)
    if rule == "PCT0":
        return f"{_real(value, rule) * 100.0:.0f}%"
    if rule == "OFN":
        return _ofn(value)
    if rule == "STR":
        if not isinstance(value, str):
            fail(f"render rule STR needs a string, got {value!r}")
        return value
    if rule == "BOOL":
        if not isinstance(value, bool):
            fail(f"render rule BOOL needs a bool, got {value!r}")
        return "true" if value else "false"
    if rule == "LIT":
        if not isinstance(value, str):
            fail(f"render rule LIT needs a literal string, got {value!r}")
        return value
    fail(f"unknown render rule {rule!r}")


def _read_json(path: Path) -> Any:
    import json

    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        fail(f"{path.as_posix()} is unreadable JSON: {exc}")


def _field(payload: Any, dotted: str) -> Any:
    """Walk a dotted key path; a numeric part indexes a list (``trace.0.E``)."""
    current = payload
    for part in dotted.split("."):
        if isinstance(current, (list, tuple)) and part.isdigit():
            index = int(part)
            if index >= len(current):
                fail(f"missing field {dotted}")
            current = current[index]
            continue
        if not isinstance(current, Mapping) or part not in current:
            fail(f"missing field {dotted}")
        current = current[part]
    return current


def _record_rel(arm_id: str) -> str:
    return (P60_EVIDENCE_REL / "arms" / arm_id / "record.json").as_posix()


def _weights_rel(arm_id: str, state: str) -> str:
    return (P60_EVIDENCE_REL / "arms" / arm_id / f"{state}.weights").as_posix()


def _retained_rels() -> tuple[str, ...]:
    """The two tracked files the CPU re-derivation reads through frozen loaders."""
    from pinn.verification.learnability_data import NORMALIZER_FILE, NORMALIZER_RUN
    from pinn.verification.split_allowlist import GENERATION7_SPLITS_REL

    normalizer = Path("runs") / NORMALIZER_RUN / "checkpoints" / NORMALIZER_FILE
    return (normalizer.as_posix(), GENERATION7_SPLITS_REL.as_posix())


def _entry(
    entry_id: str,
    value: Any,
    rule: str,
    label: str,
    source: Mapping[str, Any],
    derivation: str,
    required_in: Sequence[str],
) -> dict[str, Any]:
    if label not in LABELS:
        fail(f"entry {entry_id} has unknown label {label!r}")
    if rule not in RENDER_RULES:
        fail(f"entry {entry_id} has unknown render rule {rule!r}")
    for document in required_in:
        if document not in {"verdict", "charter"}:
            fail(f"entry {entry_id} is required in unknown document {document!r}")
    return {
        "id": entry_id,
        "value": value,
        "render": render(value, rule),
        "render_rule": rule,
        "label": label,
        "source": dict(source),
        "derivation": derivation,
        "required_in": list(required_in),
    }


def derive_state(
    ctx: Any, card: Any, arm_id: str, state: str, *, arm_data: Any = None
) -> dict[str, Any]:
    """Re-score one committed weights file on the CPU in float64.

    The record, the arm catalog and the frozen loaders supply the reference; the
    weights file's SHA-256 is checked against the record before ``torch.load``
    with ``weights_only=True``. Returns ``pos``, ``ref``, ``times``,
    ``inner_pair``, ``e_sys`` and ``e_in``, one value per scored time.

    ``arm_data`` lets a caller that re-scores several states of one arm load the
    frozen data once; the five 1632 arms share one reference, so the caller can
    also share it across arms of the same system.
    """
    from collections import OrderedDict

    import numpy as np
    import torch

    from pinn.architecture_spec import ArchitectureSpec
    from pinn.network import build_network
    from pinn.verification.diagnostic_architecture import build_network_with_first_omega
    from pinn.verification.feasibility_scorer import network_trajectory, position_errors
    from pinn.verification.learnability_arms import SEED, arm_spec
    from pinn.verification.learnability_data import load_arm_data
    from pinn.verification.learnability_run import _float32_rounded

    if state not in {"adam", "polish"}:
        fail(f"unknown state {state!r} for arm {arm_id}")
    record = _read_json(REPO_ROOT / _record_rel(arm_id))
    recorded = _field(record, f"states.{state}.weights")
    weights_rel = _weights_rel(arm_id, state)
    if recorded.get("file") != f"{state}.weights":
        fail(f"{arm_id} {state} record names weights file {recorded.get('file')!r}")
    weights_path = REPO_ROOT / weights_rel
    if not weights_path.is_file():
        fail(f"weights file is missing: {weights_rel}")
    disk = sha256_file(weights_path)
    if disk != recorded.get("sha256"):
        fail(f"weights SHA-256 {disk} != recorded {recorded.get('sha256')} for {arm_id} {state}")

    weights = torch.load(weights_path, map_location="cpu", weights_only=True)
    if not isinstance(weights, Mapping):
        fail(f"weights file {weights_rel} is not a mapping")
    widened = OrderedDict(
        (name, tensor.detach().to("cpu").to(torch.float64))
        for name, tensor in weights.items()
    )
    first_omega_0 = float(record["first_omega_0"])
    if abs(first_omega_0 - 30.0) < 1e-9:
        model = build_network(
            ArchitectureSpec(seed=SEED), dtype=torch.float64, device="cpu"
        )
    else:
        model = build_network_with_first_omega(
            first_omega_0, seed=SEED, dtype=torch.float64, device="cpu"
        )
    model.load_state_dict(widened)

    if arm_data is None:
        arm_data = load_arm_data(
            arm_spec(arm_id), ctx, scorecard=card, dtype=torch.float32, device="cpu"
        )
    pos, _velocities = network_trajectory(
        model,
        _float32_rounded(arm_data.ic13),
        _float32_rounded(arm_data.masses),
        arm_data.score.times,
        dtype=torch.float64,
        device=torch.device("cpu"),
    )
    ref = np.asarray(arm_data.score.positions, dtype=np.float64)
    e_sys, e_in, _r_sys = position_errors(pos, ref, arm_data.score.inner_pair)
    return {
        "pos": pos,
        "ref": ref,
        "times": np.asarray(arm_data.score.times, dtype=np.float64),
        "inner_pair": tuple(arm_data.score.inner_pair),
        "e_sys": np.asarray(e_sys, dtype=np.float64),
        "e_in": np.asarray(e_in, dtype=np.float64),
    }


def constant_predictor_error(ref: Any, inner_pair: Any) -> tuple[Any, Any]:
    """Each body held at its time-mean position, scored with the frozen scorer.

    The predictor learns nothing: every body sits at its average position over
    the window. Returns ``(e_sys, e_in)``, one value per scored time.
    """
    import numpy as np

    from pinn.verification.feasibility_scorer import position_errors

    reference = np.asarray(ref, dtype=np.float64)
    constant = np.broadcast_to(reference.mean(axis=0, keepdims=True), reference.shape)
    e_sys, e_in, _r_sys = position_errors(constant, reference, inner_pair)
    return np.asarray(e_sys, dtype=np.float64), np.asarray(e_in, dtype=np.float64)


def _deviation(positions: Any) -> float:
    """RMS deviation about the series' own time mean, all bodies and coordinates."""
    import numpy as np

    array = np.asarray(positions, dtype=np.float64)
    centered = array - array.mean(axis=0, keepdims=True)
    return float(np.sqrt((centered ** 2).sum(axis=(1, 2)).mean()))


def timevar_ratio(pos: Any, ref: Any) -> float:
    """The output's time variation over the real orbit's own time variation."""
    return _deviation(pos) / _deviation(ref)


def rms_ratio(pos: Any, ref: Any) -> float:
    """The output's RMS error over the orbit's RMS deviation about its own mean."""
    import numpy as np

    predicted = np.asarray(pos, dtype=np.float64)
    reference = np.asarray(ref, dtype=np.float64)
    error = float(np.sqrt(((predicted - reference) ** 2).sum(axis=(1, 2)).mean()))
    return error / _deviation(reference)


def _facts(root: Path) -> dict[str, Any]:
    """Every committed file the manifest reads, loaded once."""
    from pinn.verification.feasibility_scorecard import load_scorecard

    return {
        "records": {arm_id: _read_json(root / _record_rel(arm_id)) for arm_id in ARMS},
        "handoff": _read_json(root / HANDOFF_REL),
        "card": load_scorecard(),
        "baselines": _read_json(root / BASELINES_REL),
        "survey": _read_json(root / SURVEY_REL),
        "picks": _read_json(root / PICKS_REL),
        "census": _read_json(root / CENSUS_REL),
        "status": _read_json(root / STATUS_REL),
    }


def _arm_field(facts: Mapping[str, Any], arm_id: str, dotted: str) -> Any:
    return _field(facts["records"][arm_id], dotted)


def _tier_level(card: Any, tier: int) -> Mapping[str, Any]:
    for level in card.section("tiers")["levels"]:
        if int(level["tier"]) == tier:
            return level
    fail(f"the scorecard names no level whose tier is {tier}")


def _f_hours(facts: Mapping[str, Any], arms: Sequence[str]) -> float:
    return ordered_sum(_arm_field(facts, arm_id, "wall.hours") for arm_id in arms)


def _f_adam_steps(facts: Mapping[str, Any], arm_id: str) -> int:
    budget = facts["records"][arm_id]["budget"]
    value = budget["new_budget_steps"] if budget["extended"] else budget["budget_steps"]
    if isinstance(value, bool) or not isinstance(value, int):
        fail(f"arm {arm_id} budget names no integer step count: {value!r}")
    return value


def _f_trace(facts: Mapping[str, Any], arm_id: str) -> Sequence[Mapping[str, Any]]:
    trace = facts["records"][arm_id]["trace"]
    if not isinstance(trace, Sequence) or len(trace) < 2:
        fail(f"arm {arm_id} trace is not a list of at least two readings")
    return trace


def _f_sustained(facts: Mapping[str, Any], arm_id: str) -> float:
    return facts["records"][arm_id]["wall"]["adam_seconds"] / _f_adam_steps(facts, arm_id)


def _f_extended_hours(facts: Mapping[str, Any]) -> float:
    extended = [
        arm_id for arm_id in ARMS if facts["records"][arm_id]["budget"]["extended"]
    ]
    if len(extended) != 1:
        fail(f"expected exactly one arm with a doubled budget, found {extended!r}")
    return _arm_field(facts, extended[0], "wall.hours")


def _f_first_reading_fraction(facts: Mapping[str, Any], arm_id: str) -> float:
    return _f_trace(facts, arm_id)[1]["step"] / facts["records"][arm_id]["budget"][
        "frozen_budget_steps"
    ]


def _f_range_after_first(facts: Mapping[str, Any], arm_id: str) -> float:
    tail = [entry["E"] for entry in _f_trace(facts, arm_id)[1:]]
    return max(tail) - min(tail)


def _f_sweep_budget(facts: Mapping[str, Any]) -> list[int]:
    """The frozen budget rule re-applied to each sweep arm's own timing run."""
    from pinn.verification import feasibility_scorecard as scorecard_module

    cap = float(facts["card"].section("budget_rule")["cap_hours_single_system"])
    values = []
    for arm_id in SWEEP_ARMS:
        timing = facts["records"][arm_id]["timing"]
        computed = scorecard_module.steps_budget(
            cap, timing["wall_seconds"], timing["steps"], scorecard=facts["card"]
        )
        recorded = facts["records"][arm_id]["budget"]["budget_steps"]
        if computed != recorded:
            fail(
                f"{arm_id} recorded budget {recorded} != the frozen rule's {computed}"
            )
        values.append(computed)
    return values


def _f_best_eps_h(facts: Mapping[str, Any]) -> float:
    return min(_arm_field(facts, arm_id, "result.eps_h") for arm_id in ARMS)


def _f_best_eps_h_arms(facts: Mapping[str, Any]) -> str:
    best = _f_best_eps_h(facts)
    return ", ".join(
        arm_id for arm_id in ARMS if _arm_field(facts, arm_id, "result.eps_h") == best
    )


def _f_state_eps_h(facts: Mapping[str, Any]) -> list[tuple[float, str, str]]:
    return [
        (_arm_field(facts, arm_id, f"states.{state}.score_gold.eps_h"), arm_id, state)
        for arm_id in ARMS
        for state in ("adam", "polish")
    ]


def _f_trace_eps_h(facts: Mapping[str, Any]) -> list[tuple[float, str, int]]:
    return [
        (entry["eps_h"], arm_id, entry["step"])
        for arm_id in ARMS
        for entry in _f_trace(facts, arm_id)
    ]


def _f_rung1_below(facts: Mapping[str, Any]) -> int:
    return sum(
        1
        for arm_id in RUNG1_ARMS
        if _arm_field(facts, arm_id, "result.E")
        < _arm_field(facts, arm_id, "formula.E_formula")
    )


def _f_rung1_below_systems(facts: Mapping[str, Any]) -> str:
    return ", ".join(
        arm_id[len("r1-") :]
        for arm_id in RUNG1_ARMS
        if _arm_field(facts, arm_id, "result.E")
        < _arm_field(facts, arm_id, "formula.E_formula")
    )


def _f_rung1_counts_true(facts: Mapping[str, Any]) -> int:
    return sum(
        1 for arm_id in RUNG1_ARMS if _arm_field(facts, arm_id, "formula.counts") is True
    )


def _f_curve(facts: Mapping[str, Any], fn: Any) -> list[float]:
    return [fn(facts, arm_id) for arm_id in ARMS]


def _f_rung_rule(facts: Mapping[str, Any], which: str) -> list[int]:
    rule = facts["card"].section("decision_rule")
    return [int(rule[f"{which}_min_count"]), int(rule[f"{which}_panel_size"])]


def _f_rung3_share(facts: Mapping[str, Any]) -> float:
    minimum, panel = _f_rung_rule(facts, "rung3")
    return minimum / panel


def _f_formula_tier1(facts: Mapping[str, Any], split: str) -> list[int]:
    counts = facts["baselines"]["formula_tier_counts"][split]
    total = sum(int(counts[key]) for key in ("0", "1", "2", "3", "not_applicable"))
    reached = sum(int(counts[key]) for key in ("1", "2", "3"))
    return [reached, total]


def _f_gen7_rate(facts: Mapping[str, Any]) -> float:
    return float(facts["status"]["s_per_step_ema"])


def _f_example_sps(facts: Mapping[str, Any]) -> float:
    values = sorted(_arm_field(facts, arm_id, "timing.seconds_per_step") for arm_id in ARMS)
    return values[len(values) // 2]


# The illustration sizes the for-scale and example entries quote. The cited
# entries carry the same ints, so the citation and the arithmetic cannot drift.
FORSCALE_STEPS_LOW = 200000
FORSCALE_STEPS_HIGH = 300000
EXAMPLE_STEPS = 100000

# The three panel systems and the two committed states every arm recorded. Each
# system's constant predictor is scored against that system's own gold reference.
CPU_SYSTEMS = ("1632", "851", "4658")
CPU_STATES = ("adam", "polish")


def _arm_id_of(entry_id: str) -> str:
    parts = entry_id.split(".")
    if len(parts) < 3 or parts[0] != "arm":
        fail(f"{entry_id} is not an arm.<arm>.<field> id")
    return parts[1]


def _cpu_values(facts: Mapping[str, Any], field: str) -> list[Any]:
    """One field of every one of the 14 CPU states, in handoff arm order."""
    return [
        facts["cpu"][f"cpu.{arm_id}.{state}.{field}"]
        for arm_id in ARMS
        for state in CPU_STATES
    ]


def _one_cpu_value(facts: Mapping[str, Any], field: str) -> Any:
    values = _cpu_values(facts, field)
    if len(set(values)) != 1:
        fail(f"the 14 CPU states disagree on {field}: {sorted(set(values))!r}")
    return values[0]


def _const_gaps(facts: Mapping[str, Any]) -> list[float]:
    """Each Rung-1 system's official E minus its constant-predictor E."""
    return [
        (
            facts["records"][f"r1-{system}"]["result"]["E"]
            - facts["cpu"][f"cpu.const.{system}.E"]
        )
        for system in CPU_SYSTEMS
    ]


# Every arithmetic entry's formula, by name. Both programs carry their own copy
# of this table; the manifest records only the name.
ARITHMETIC: dict[str, Any] = {
    "hours_total": lambda facts, _id: _f_hours(facts, ARMS),
    "hours_rung1": lambda facts, _id: _f_hours(facts, RUNG1_ARMS),
    "hours_sweep": lambda facts, _id: _f_hours(facts, SWEEP_ARMS),
    "steps_total_adam": lambda facts, _id: sum(_f_adam_steps(facts, a) for a in ARMS),
    "steps_sweep_budget_min": lambda facts, _id: min(_f_sweep_budget(facts)),
    "steps_sweep_budget_max": lambda facts, _id: max(_f_sweep_budget(facts)),
    "timed_sps_min": lambda facts, _id: min(
        _arm_field(facts, a, "timing.seconds_per_step") for a in ARMS
    ),
    "timed_sps_max": lambda facts, _id: max(
        _arm_field(facts, a, "timing.seconds_per_step") for a in ARMS
    ),
    "sustained_sps_min": lambda facts, _id: min(_f_sustained(facts, a) for a in ARMS),
    "sustained_sps_max": lambda facts, _id: max(_f_sustained(facts, a) for a in ARMS),
    "timing_wall_min": lambda facts, _id: min(
        _arm_field(facts, a, "timing.wall_seconds") for a in ARMS
    ),
    "timing_wall_max": lambda facts, _id: max(
        _arm_field(facts, a, "timing.wall_seconds") for a in ARMS
    ),
    "timing_wall_total": lambda facts, _id: ordered_sum(
        _arm_field(facts, a, "timing.wall_seconds") for a in ARMS
    ),
    "polish_min": lambda facts, _id: min(
        _arm_field(facts, a, "wall.polish_seconds") for a in ARMS
    ),
    "polish_max": lambda facts, _id: max(
        _arm_field(facts, a, "wall.polish_seconds") for a in ARMS
    ),
    "unextended_hours_min": lambda facts, _id: min(
        _arm_field(facts, a, "wall.hours")
        for a in ARMS
        if not facts["records"][a]["budget"]["extended"]
    ),
    "unextended_hours_max": lambda facts, _id: max(
        _arm_field(facts, a, "wall.hours")
        for a in ARMS
        if not facts["records"][a]["budget"]["extended"]
    ),
    "extended_hours": lambda facts, _id: _f_extended_hours(facts),
    "best_eps_h_official": lambda facts, _id: _f_best_eps_h(facts),
    "best_eps_h_official_arms": lambda facts, _id: _f_best_eps_h_arms(facts),
    "best_ratio_to_bar": lambda facts, _id: _f_best_eps_h(facts)
    / float(_tier_level(facts["card"], 3)["eps_h_max"]),
    "best_lowest_state": lambda facts, _id: min(v for v, _a, _s in _f_state_eps_h(facts)),
    "best_lowest_state_arm": lambda facts, _id: next(
        a for v, a, _s in _f_state_eps_h(facts) if v == min(x for x, _b, _c in _f_state_eps_h(facts))
    ),
    "best_lowest_state_state": lambda facts, _id: next(
        s for v, _a, s in _f_state_eps_h(facts) if v == min(x for x, _b, _c in _f_state_eps_h(facts))
    ),
    "best_lowest_trace": lambda facts, _id: min(v for v, _a, _s in _f_trace_eps_h(facts)),
    "best_lowest_trace_arm": lambda facts, _id: next(
        a for v, a, _s in _f_trace_eps_h(facts) if v == min(x for x, _b, _c in _f_trace_eps_h(facts))
    ),
    "best_lowest_trace_step": lambda facts, _id: next(
        s for v, _a, s in _f_trace_eps_h(facts) if v == min(x for x, _b, _c in _f_trace_eps_h(facts))
    ),
    "rung1_below_formula": lambda facts, _id: [_f_rung1_below(facts), len(RUNG1_ARMS)],
    "rung1_below_formula_systems": lambda facts, _id: _f_rung1_below_systems(facts),
    "rung1_counts_true": lambda facts, _id: [_f_rung1_counts_true(facts), len(RUNG1_ARMS)],
    "curve_e_step0_min": lambda facts, _id: min(
        _f_curve(facts, lambda f, a: _arm_field(f, a, "trace.0.E"))
    ),
    "curve_e_step0_max": lambda facts, _id: max(
        _f_curve(facts, lambda f, a: _arm_field(f, a, "trace.0.E"))
    ),
    "curve_first_reading_min": lambda facts, _id: min(
        _f_curve(facts, lambda f, a: _arm_field(f, a, "trace.1.E"))
    ),
    "curve_first_reading_max": lambda facts, _id: max(
        _f_curve(facts, lambda f, a: _arm_field(f, a, "trace.1.E"))
    ),
    "curve_fold_drop_min": lambda facts, _id: min(
        _f_curve(
            facts,
            lambda f, a: _arm_field(f, a, "trace.0.E")
            / _arm_field(f, a, "trace.1.E"),
        )
    ),
    "curve_fold_drop_max": lambda facts, _id: max(
        _f_curve(
            facts,
            lambda f, a: _arm_field(f, a, "trace.0.E")
            / _arm_field(f, a, "trace.1.E"),
        )
    ),
    "curve_first_fraction_min": lambda facts, _id: min(
        _f_curve(facts, _f_first_reading_fraction)
    ),
    "curve_first_fraction_max": lambda facts, _id: max(
        _f_curve(facts, _f_first_reading_fraction)
    ),
    "curve_e_final_min": lambda facts, _id: min(
        _f_curve(facts, lambda f, a: _arm_field(f, a, "result.E"))
    ),
    "curve_e_final_max": lambda facts, _id: max(
        _f_curve(facts, lambda f, a: _arm_field(f, a, "result.E"))
    ),
    "curve_tier1_multiple_min": lambda facts, _id: min(
        _f_curve(
            facts,
            lambda f, a: _arm_field(f, a, "result.E")
            / float(_tier_level(f["card"], 1)["E_max"]),
        )
    ),
    "curve_tier1_multiple_max": lambda facts, _id: max(
        _f_curve(
            facts,
            lambda f, a: _arm_field(f, a, "result.E")
            / float(_tier_level(f["card"], 1)["E_max"]),
        )
    ),
    "curve_range_after_first_min": lambda facts, _id: min(
        _f_curve(facts, _f_range_after_first)
    ),
    "curve_range_after_first_max": lambda facts, _id: max(
        _f_curve(facts, _f_range_after_first)
    ),
    "decision_rung2b": lambda facts, _id: _f_rung_rule(facts, "rung2b"),
    "decision_rung3": lambda facts, _id: _f_rung_rule(facts, "rung3"),
    "decision_rung3_share": lambda facts, _id: _f_rung3_share(facts),
    "formula_tier1_train": lambda facts, _id: _f_formula_tier1(facts, "train"),
    "formula_tier1_validation": lambda facts, _id: _f_formula_tier1(facts, "validation"),
    "census_one_part_in_0p1": lambda facts, _id: int(
        facts["census"]["phase_accuracy"]["0.1"]["one_part_in"]
    ),
    "forscale_days_low": lambda facts, _id: FORSCALE_STEPS_LOW
    * _f_gen7_rate(facts)
    / 86400.0,
    "forscale_days_high": lambda facts, _id: FORSCALE_STEPS_HIGH
    * _f_gen7_rate(facts)
    / 86400.0,
    "forscale_hours_low": lambda facts, _id: FORSCALE_STEPS_LOW
    * _f_gen7_rate(facts)
    / 3600.0,
    "example_sps": lambda facts, _id: _f_example_sps(facts),
    "example_hours": lambda facts, _id: EXAMPLE_STEPS * _f_example_sps(facts) / 3600.0,
    "arm_adam_steps": lambda facts, entry_id: _f_adam_steps(facts, _arm_id_of(entry_id)),
    "arm_sustained": lambda facts, entry_id: _f_sustained(facts, _arm_id_of(entry_id)),
    "arm_first_fraction": lambda facts, entry_id: _f_first_reading_fraction(
        facts, _arm_id_of(entry_id)
    ),
    "arm_range_after_first": lambda facts, entry_id: _f_range_after_first(
        facts, _arm_id_of(entry_id)
    ),
    "cpu_const_range_min": lambda facts, _id: min(
        facts["cpu"][f"cpu.const.{system}.E"] for system in CPU_SYSTEMS
    ),
    "cpu_const_range_max": lambda facts, _id: max(
        facts["cpu"][f"cpu.const.{system}.E"] for system in CPU_SYSTEMS
    ),
    "cpu_range_e_sys_t0_min": lambda facts, _id: min(
        _cpu_values(facts, "e_sys_t0")
    ),
    "cpu_range_e_sys_t0_max": lambda facts, _id: max(
        _cpu_values(facts, "e_sys_t0")
    ),
    "cpu_range_e_in_t0_min": lambda facts, _id: min(_cpu_values(facts, "e_in_t0")),
    "cpu_range_e_in_t0_max": lambda facts, _id: max(_cpu_values(facts, "e_in_t0")),
    "cpu_range_best_moment_min": lambda facts, _id: min(
        _cpu_values(facts, "best_moment")
    ),
    "cpu_range_best_moment_max": lambda facts, _id: max(
        _cpu_values(facts, "best_moment")
    ),
    "cpu_range_timevar_min": lambda facts, _id: min(
        _cpu_values(facts, "timevar_ratio")
    ),
    "cpu_range_timevar_max": lambda facts, _id: max(
        _cpu_values(facts, "timevar_ratio")
    ),
    "cpu_range_rms_ratio_min": lambda facts, _id: min(
        _cpu_values(facts, "rms_ratio")
    ),
    "cpu_range_rms_ratio_max": lambda facts, _id: max(
        _cpu_values(facts, "rms_ratio")
    ),
    "cpu_total_n_within_tier1": lambda facts, _id: sum(
        _cpu_values(facts, "n_within_tier1")
    ),
    "cpu_n_times": lambda facts, _id: _one_cpu_value(facts, "n_times"),
    "const_gap_min": lambda facts, _id: min(_const_gaps(facts)),
    "const_gap_max": lambda facts, _id: max(_const_gaps(facts)),
    "cpu_attestation_test_split_opened": lambda facts, _id: int(
        facts["attestation"]["test_split_opened"]
    ),
    "cpu_attestation_validation": lambda facts, _id: int(
        facts["attestation"]["opened"]["validation"]
    ),
    "cpu_attestation_other_under_root": lambda facts, _id: int(
        facts["attestation"]["opened"]["other_under_root"]
    ),
    "cpu_attestation_blocked_attempts": lambda facts, _id: int(
        facts["attestation"]["blocked_attempts"]
    ),
    "cpu_attestation_refused_before_open": lambda facts, _id: int(
        facts["attestation"]["refused_before_open"]
    ),
}


def _record_entry(
    entry_id: str,
    value: Any,
    rule: str,
    arm_id: str,
    key: str,
    derivation: str,
    required_in: Sequence[str],
    label: str = "committed-record",
) -> dict[str, Any]:
    return _entry(
        entry_id,
        value,
        rule,
        label,
        {"path": _record_rel(arm_id), "key": key},
        derivation,
        required_in,
    )


def _arithmetic(
    entry_id: str, rule: str, formula: str, derivation: str, required_in: Sequence[str]
) -> dict[str, Any]:
    return _entry(
        entry_id,
        ARITHMETIC[formula](_FACTS, entry_id),
        rule,
        "arithmetic",
        {"formula": formula},
        derivation,
        required_in,
    )


_FACTS: dict[str, Any] = {}


def _inputs(root: Path, record_arms: Sequence[str]) -> list[dict[str, str]]:
    """Every committed file a value is read from, sorted by path."""
    rels = {
        SCORECARD_REL.as_posix(),
        HANDOFF_REL.as_posix(),
        BASELINES_REL.as_posix(),
        SURVEY_REL.as_posix(),
        PICKS_REL.as_posix(),
        CENSUS_REL.as_posix(),
        STATUS_REL.as_posix(),
        *_retained_rels(),
    }
    for arm_id in record_arms:
        rels.add(_record_rel(arm_id))
    entries = []
    for relative in sorted(rels):
        path = root / relative
        if not path.is_file():
            fail(f"input is missing: {relative}")
        entries.append({"path": relative, "sha256": sha256_file(path)})
    return entries


def _arm_entries(facts: Mapping[str, Any]) -> list[dict[str, Any]]:
    """Group 1: every per-arm number, in handoff order."""
    entries: list[dict[str, Any]] = []
    for arm_id in ARMS:
        result = facts["records"][arm_id]["result"]
        official = "official-mps-float32"
        entries += [
            _record_entry(
                f"arm.{arm_id}.tier",
                result["tier"],
                "INT",
                arm_id,
                "result.tier",
                f"result.tier of the committed {arm_id} record: the tier the official score earned.",
                ["verdict"],
                label=official,
            ),
            _record_entry(
                f"arm.{arm_id}.E",
                result["E"],
                "E4",
                arm_id,
                "result.E",
                f"result.E of the committed {arm_id} record: the official MPS float32 score.",
                ["verdict"],
                label=official,
            ),
            _record_entry(
                f"arm.{arm_id}.eps_h",
                result["eps_h"],
                "EPS",
                arm_id,
                "result.eps_h",
                f"result.eps_h of the committed {arm_id} record, the official MPS float32 value.",
                ["verdict"],
                label=official,
            ),
            _record_entry(
                f"arm.{arm_id}.h_1pct",
                _field(result, "h.0.1"),
                "F1",
                arm_id,
                "result.h.0.1",
                f"The recorded fraction of the window the {arm_id} arm held within 1%.",
                ["verdict"],
                label=official,
            ),
            _record_entry(
                f"arm.{arm_id}.h_10pct",
                _field(result, "h.1.1"),
                "F1",
                arm_id,
                "result.h.1.1",
                f"The recorded fraction of the window the {arm_id} arm held within 10%.",
                ["verdict"],
                label=official,
            ),
            _record_entry(
                f"arm.{arm_id}.state",
                result["state"],
                "STR",
                arm_id,
                "result.state",
                f"The state the {arm_id} record reports as its better one.",
                ["verdict"],
            ),
            _record_entry(
                f"arm.{arm_id}.first_omega_0",
                facts["records"][arm_id]["first_omega_0"],
                "F0",
                arm_id,
                "first_omega_0",
                f"The first-layer frequency the {arm_id} arm ran at.",
                ["verdict"],
            ),
            _record_entry(
                f"arm.{arm_id}.E_formula",
                _field(facts["records"][arm_id], "formula.E_formula"),
                "E4",
                arm_id,
                "formula.E_formula",
                f"The two-Kepler formula's own error on {arm_id}'s system, for comparison with the arm.",
                ["verdict"],
            ),
            _record_entry(
                f"arm.{arm_id}.counts",
                _field(facts["records"][arm_id], "formula.counts"),
                "BOOL",
                arm_id,
                "formula.counts",
                f"Whether the formula alone reaches Tier 1 on {arm_id}'s system.",
                [],
            ),
            _record_entry(
                f"arm.{arm_id}.seconds_per_step",
                _field(facts["records"][arm_id], "timing.seconds_per_step"),
                "F6",
                arm_id,
                "timing.seconds_per_step",
                f"The {arm_id} timing run's wall seconds per step; it must equal the handoff's.",
                ["verdict"],
            ),
            _record_entry(
                f"arm.{arm_id}.timing_wall_seconds",
                _field(facts["records"][arm_id], "timing.wall_seconds"),
                "F1",
                arm_id,
                "timing.wall_seconds",
                f"The {arm_id} timing run's wall seconds.",
                [],
            ),
            _record_entry(
                f"arm.{arm_id}.polish_seconds",
                _field(facts["records"][arm_id], "wall.polish_seconds"),
                "F1",
                arm_id,
                "wall.polish_seconds",
                f"The {arm_id} arm's L-BFGS polish wall seconds.",
                [],
            ),
            _record_entry(
                f"arm.{arm_id}.wall_hours",
                _field(facts["records"][arm_id], "wall.hours"),
                "F3",
                arm_id,
                "wall.hours",
                f"The {arm_id} arm's measured wall hours; it must equal the handoff's.",
                ["verdict"],
            ),
            _record_entry(
                f"arm.{arm_id}.curve.E_step0",
                _field(facts["records"][arm_id], "trace.0.E"),
                "F1",
                arm_id,
                "trace.0.E",
                f"The {arm_id} convergence curve's E at step 0.",
                [],
            ),
            _record_entry(
                f"arm.{arm_id}.curve.E_first_reading",
                _field(facts["records"][arm_id], "trace.1.E"),
                "F1",
                arm_id,
                "trace.1.E",
                f"The {arm_id} convergence curve's E at its first reading.",
                [],
            ),
        ]
        entries += [
            _arithmetic(
                f"arm.{arm_id}.adam_steps",
                "INT",
                "arm_adam_steps",
                f"The {arm_id} arm's Adam steps: the doubled budget when it was extended, else the recorded budget.",
                [],
            ),
            _arithmetic(
                f"arm.{arm_id}.sustained_seconds_per_step",
                "F5",
                "arm_sustained",
                f"The {arm_id} arm's sustained rate: wall.adam_seconds over its Adam steps.",
                ["verdict"],
            ),
            _arithmetic(
                f"arm.{arm_id}.curve.first_reading_fraction",
                "PCT0",
                "arm_first_fraction",
                f"The {arm_id} first reading's step as a fraction of its frozen budget.",
                [],
            ),
            _arithmetic(
                f"arm.{arm_id}.curve.range_after_first",
                "F2",
                "arm_range_after_first",
                f"The {arm_id} curve's E range after the first reading: max minus min of trace[1:].E.",
                [],
            ),
        ]
    return entries


def _aggregate_entries(facts: Mapping[str, Any]) -> list[dict[str, Any]]:
    """Group 2: totals, ranges, the best readings and the curve aggregates."""
    both = ["verdict", "charter"]
    entries = [
        _arithmetic(
            "hours.total",
            "F3",
            "hours_total",
            "ordered_sum over the seven records' wall.hours in handoff arm order, the explicit left-to-right += loop from 0.0.",
            both,
        ),
        _arithmetic(
            "hours.rung1",
            "F3",
            "hours_rung1",
            "ordered_sum over the three Rung 1 arms' wall.hours in handoff order.",
            ["verdict"],
        ),
        _arithmetic(
            "hours.sweep",
            "F3",
            "hours_sweep",
            "ordered_sum over the four sweep arms' wall.hours in handoff order.",
            ["verdict"],
        ),
        _arithmetic(
            "steps.total_adam",
            "INT",
            "steps_total_adam",
            "The sum of the seven arms' Adam steps, the doubled 1,961,246 for r1-4658 included.",
            [],
        ),
        _arithmetic(
            "steps.sweep_budget.min",
            "INT",
            "steps_sweep_budget_min",
            "The least budget_steps of the four sweep arms, each equal to the frozen steps_budget rule re-applied to its own timing run.",
            ["verdict"],
        ),
        _arithmetic(
            "steps.sweep_budget.max",
            "INT",
            "steps_sweep_budget_max",
            "The greatest budget_steps of the four sweep arms, each equal to the frozen steps_budget rule re-applied to its own timing run.",
            ["verdict"],
        ),
        _arithmetic(
            "seconds_per_step.timed.min",
            "F6",
            "timed_sps_min",
            "The least timing.seconds_per_step of the seven timing runs.",
            [],
        ),
        _arithmetic(
            "seconds_per_step.timed.max",
            "F6",
            "timed_sps_max",
            "The greatest timing.seconds_per_step of the seven timing runs.",
            [],
        ),
        _arithmetic(
            "seconds_per_step.sustained.min",
            "F5",
            "sustained_sps_min",
            "The least sustained rate, wall.adam_seconds over Adam steps, across the seven arms.",
            [],
        ),
        _arithmetic(
            "seconds_per_step.sustained.max",
            "F5",
            "sustained_sps_max",
            "The greatest sustained rate, wall.adam_seconds over Adam steps, across the seven arms.",
            [],
        ),
        _arithmetic(
            "timing.wall_seconds.min",
            "F1",
            "timing_wall_min",
            "The least timing-run wall seconds across the seven arms.",
            [],
        ),
        _arithmetic(
            "timing.wall_seconds.max",
            "F1",
            "timing_wall_max",
            "The greatest timing-run wall seconds across the seven arms.",
            [],
        ),
        _arithmetic(
            "timing.wall_seconds.total",
            "F1",
            "timing_wall_total",
            "ordered_sum over the seven timing runs' wall seconds in handoff order.",
            [],
        ),
        _arithmetic(
            "polish.seconds.min",
            "F1",
            "polish_min",
            "The least L-BFGS polish wall seconds across the seven arms.",
            [],
        ),
        _arithmetic(
            "polish.seconds.max",
            "F1",
            "polish_max",
            "The greatest L-BFGS polish wall seconds across the seven arms.",
            [],
        ),
        _arithmetic(
            "cost.arm_hours.unextended.min",
            "F3",
            "unextended_hours_min",
            "The least wall hours among the six arms that did not earn a budget doubling.",
            both,
        ),
        _arithmetic(
            "cost.arm_hours.unextended.max",
            "F3",
            "unextended_hours_max",
            "The greatest wall hours among the six arms that did not earn a budget doubling.",
            both,
        ),
        _arithmetic(
            "cost.arm_hours.extended",
            "F3",
            "extended_hours",
            "The wall hours of the one arm whose budget was doubled, r1-4658.",
            both,
        ),
        _arithmetic(
            "best.eps_h_official",
            "EPS",
            "best_eps_h_official",
            "The minimum result.eps_h over the seven arms: the official best energy reading.",
            both,
        ),
        _arithmetic(
            "best.eps_h_official_arms",
            "STR",
            "best_eps_h_official_arms",
            "Every arm attaining that exact minimum, in handoff order; no tie on the committed records.",
            both,
        ),
        _arithmetic(
            "best.ratio_to_bar",
            "SCI2",
            "best_ratio_to_bar",
            "The best official eps_h over the scorecard's Tier-3 eps_h_max.",
            ["verdict"],
        ),
        _arithmetic(
            "best.eps_h_lowest_state",
            "EPS",
            "best_lowest_state",
            "The least score_gold.eps_h over all fourteen scored states.",
            ["verdict"],
        ),
        _arithmetic(
            "best.eps_h_lowest_state_arm",
            "STR",
            "best_lowest_state_arm",
            "The arm holding that least state eps_h.",
            ["verdict"],
        ),
        _arithmetic(
            "best.eps_h_lowest_state_state",
            "STR",
            "best_lowest_state_state",
            "The state holding that least state eps_h.",
            ["verdict"],
        ),
        _arithmetic(
            "best.eps_h_lowest_trace",
            "E4",
            "best_lowest_trace",
            "The least trace eps_h at any reading of any arm.",
            ["verdict"],
        ),
        _arithmetic(
            "best.eps_h_lowest_trace_arm",
            "STR",
            "best_lowest_trace_arm",
            "The arm holding that least trace eps_h.",
            ["verdict"],
        ),
        _arithmetic(
            "best.eps_h_lowest_trace_step",
            "INT",
            "best_lowest_trace_step",
            "The training step of that least trace eps_h.",
            ["verdict"],
        ),
        _arithmetic(
            "rung1.below_formula",
            "OFN",
            "rung1_below_formula",
            "How many Rung 1 arms scored strictly below their system's formula E, under the frozen strictly-less rule.",
            ["verdict"],
        ),
        _arithmetic(
            "rung1.below_formula_systems",
            "STR",
            "rung1_below_formula_systems",
            "The systems whose Rung 1 arm scored below the formula, as their numeric ids.",
            ["verdict"],
        ),
        _arithmetic(
            "rung1.counts_true",
            "OFN",
            "rung1_counts_true",
            "How many Rung 1 systems the formula alone reaches Tier 1 on.",
            [],
        ),
    ]
    for name, rule, formula, what in (
        ("E_step0", "F1", "curve_e_step0_min", "The least E at step 0 across the seven convergence curves."),
        ("E_step0", "F1", "curve_e_step0_max", "The greatest E at step 0 across the seven convergence curves."),
        ("E_first_reading", "F1", "curve_first_reading_min", "The least E at the first reading across the seven convergence curves."),
        ("E_first_reading", "F1", "curve_first_reading_max", "The greatest E at the first reading across the seven convergence curves."),
        ("fold_drop", "F0", "curve_fold_drop_min", "The least step-0 E over first-reading E across the seven curves."),
        ("fold_drop", "F0", "curve_fold_drop_max", "The greatest step-0 E over first-reading E across the seven curves."),
        ("first_reading_fraction", "PCT0", "curve_first_fraction_min", "The least first-reading fraction of the frozen budget."),
        ("first_reading_fraction", "PCT0", "curve_first_fraction_max", "The greatest first-reading fraction of the frozen budget."),
        ("E_final", "F2", "curve_e_final_min", "The least final result.E across the seven arms."),
        ("E_final", "F2", "curve_e_final_max", "The greatest final result.E across the seven arms."),
        ("tier1_multiple", "F0", "curve_tier1_multiple_min", "The least result.E over the Tier-1 E_max across the seven arms."),
        ("tier1_multiple", "F0", "curve_tier1_multiple_max", "The greatest result.E over the Tier-1 E_max across the seven arms."),
        ("range_after_first", "F2", "curve_range_after_first_min", "The least E range after the first reading across the seven curves."),
        ("range_after_first", "F2", "curve_range_after_first_max", "The greatest E range after the first reading across the seven curves."),
    ):
        suffix = "min" if formula.endswith("_min") else "max"
        entries.append(
            _arithmetic(
                f"curve.{name}.{suffix}",
                rule,
                formula,
                what,
                both if name == "E_final" else [],
            )
        )
    entries.append(
        _arithmetic(
            "decision.rung3_share",
            "PCT0",
            "decision_rung3_share",
            "The frozen Rung-3 proportion: rung3_min_count over rung3_panel_size.",
            ["charter"],
        )
    )
    return entries


def _handoff_entries(facts: Mapping[str, Any]) -> list[dict[str, Any]]:
    """Group 3: the sealed handoff's own statements."""
    entries = []
    for entry_id, key, rule, what in (
        ("handoff.verdict", "verdict.verdict", "STR", "The sealed handoff's verdict string."),
        ("handoff.reason", "verdict.reasons.0", "STR", "The sealed handoff's first reason, verbatim."),
        ("handoff.qualifier", "verdict.representation_limit_qualifier", "BOOL", "The sealed handoff's representation-limit qualifier."),
        ("handoff.level3", "level3", "STR", "The sealed handoff's Level-3 readiness statement."),
        ("handoff.phases_61_63", "phases_61_63", "STR", "The sealed handoff's statement about Phases 61 to 63."),
        ("handoff.stop_reason", "stop_reason", "STR", "The sealed handoff's stop reason."),
    ):
        entries.append(
            _entry(
                entry_id,
                _field(facts["handoff"], key),
                rule,
                "committed-record",
                {"path": HANDOFF_REL.as_posix(), "key": key},
                what,
                ["verdict"],
            )
        )
    return entries


def _scorecard_entries(facts: Mapping[str, Any]) -> list[dict[str, Any]]:
    """Group 4: the frozen thresholds and decision proportions."""
    card = facts["card"]
    levels = card.section("tiers")["levels"]
    index = {int(level["tier"]): position for position, level in enumerate(levels)}
    entries = []
    for entry_id, tier, field, rule, what, required in (
        ("tiers.tier1.E_max", 1, "E_max", "F1", "The Tier-1 E limit from the frozen scorecard.", ["verdict", "charter"]),
        ("tiers.tier2.E_max", 2, "E_max", "F2", "The Tier-2 E limit from the frozen scorecard.", ["verdict", "charter"]),
        ("tiers.tier2.eps_h_max", 2, "eps_h_max", "POW10", "The Tier-2 eps_h limit from the frozen scorecard.", ["verdict", "charter"]),
        ("tiers.tier3.E_max", 3, "E_max", "F2", "The Tier-3 E limit, the E_max of the level whose tier is 3.", ["verdict", "charter"]),
        ("tiers.tier3.eps_h_max", 3, "eps_h_max", "POW10", "The Tier-3 eps_h limit from the frozen scorecard.", ["verdict", "charter"]),
    ):
        key = f"tiers.levels.{index[tier]}.{field}"
        entries.append(
            _entry(
                entry_id,
                levels[index[tier]][field],
                rule,
                "committed-record",
                {"path": SCORECARD_REL.as_posix(), "key": key},
                what,
                required,
            )
        )
    for entry_id, formula, rule, what in (
        ("decision.rung2b", "decision_rung2b", "OFN", "The frozen Rung-2b proportion: min count over panel size."),
        ("decision.rung3", "decision_rung3", "OFN", "The frozen Rung-3 proportion: min count over panel size."),
    ):
        entries.append(
            _arithmetic(entry_id, rule, formula, what, ["verdict"])
        )
    return entries


def _baseline_entries(facts: Mapping[str, Any]) -> list[dict[str, Any]]:
    """Group 5: the Phase 59 baseline medians and Tier-1 counts."""
    both = ["verdict", "charter"]
    entries = []
    for entry_id, key, what in (
        ("baseline.formula.median_E.train", "median_E.formula_train", "The formula's median E on the 1,812 Stage-0 training systems."),
        ("baseline.formula.median_E.validation", "median_E.formula_validation", "The formula's median E on the 227 validation systems."),
        ("baseline.copy.median_E.validation", "median_E.copy_validation", "The nearest-neighbour copy's median E on the 227 validation systems."),
    ):
        entries.append(
            _entry(
                entry_id,
                _field(facts["baselines"], key),
                "F3",
                "committed-record",
                {"path": BASELINES_REL.as_posix(), "key": key},
                what,
                both,
            )
        )
    for entry_id, formula, what in (
        ("baseline.formula.tier1.train", "formula_tier1_train", "How many of the 1,812 Stage-0 training systems the formula alone brings to Tier 1 or better."),
        ("baseline.formula.tier1.validation", "formula_tier1_validation", "How many of the 227 validation systems the formula alone brings to Tier 1 or better."),
    ):
        entries.append(_arithmetic(entry_id, "OFN", formula, what, ["verdict"]))
    entries.append(
        _entry(
            "baseline.copy.tier1.validation",
            facts["baselines"]["nn_copy_reaches_tier1_on_validation"],
            "STR",
            "committed-record",
            {"path": BASELINES_REL.as_posix(), "key": "nn_copy_reaches_tier1_on_validation"},
            "The committed count of validation systems the nearest-neighbour copy brings to Tier 1 or better.",
            ["verdict"],
        )
    )
    return entries


def _survey_entries(facts: Mapping[str, Any]) -> list[dict[str, Any]]:
    """Group 6: the dataset survey and the inner-lap census."""
    entries = []
    for entry_id, path, key, rule, what, required in (
        ("survey.stage0.error_growth_median", SURVEY_REL, "per_stage.0.measures.error_growth.median", "F2", "Stage 0's median error-growth measure from the committed survey.", ["verdict"]),
        ("survey.stage4b.error_growth_median", SURVEY_REL, "per_stage.4b.measures.error_growth.median", "F2", "Stage 4b's median error-growth measure from the committed survey.", ["verdict"]),
        ("survey.stage6.error_growth_median", SURVEY_REL, "per_stage.6.measures.error_growth.median", "F1", "Stage 6's median error-growth measure from the committed survey.", ["verdict"]),
        ("survey.stage3.count", SURVEY_REL, "stage3.count", "INT", "How many records the committed survey places in Stage 3: none.", ["verdict"]),
        ("survey.picks.stage4b", PICKS_REL, "stage4b.record", "STR", "The FEAS-09 Stage-4b probe system the frozen rule picked.", ["verdict"]),
        ("survey.picks.stage6", PICKS_REL, "stage6.record", "STR", "The FEAS-09 Stage-6 probe system the frozen rule picked.", ["verdict"]),
        ("census.stage0.N_in_median", CENSUS_REL, "distributions.N_in.quantiles.50", "F2", "The median inner-lap count over the 1,812 Stage-0 training systems.", ["charter"]),
    ):
        source = facts["survey"] if path is SURVEY_REL else facts["picks"] if path is PICKS_REL else facts["census"]
        entries.append(
            _entry(
                entry_id,
                _field(source, key),
                rule,
                "committed-record",
                {"path": path.as_posix(), "key": key},
                what,
                required,
            )
        )
    entries.append(
        _arithmetic(
            "census.one_part_in_0p1",
            "INT",
            "census_one_part_in_0p1",
            "The census's 10% phase-accuracy figure as one part in this many, read from the committed census.",
            ["charter"],
        )
    )
    return entries


def _cost_entries(facts: Mapping[str, Any]) -> list[dict[str, Any]]:
    """Group 7: the measured cost primitives and the labelled for-scale figure."""
    both = ["verdict", "charter"]
    entries = [
        _entry(
            "cost.gen7.seconds_per_step",
            _field(facts["status"], "s_per_step_ema"),
            "F1",
            "committed-record",
            {"path": STATUS_REL.as_posix(), "key": "s_per_step_ema"},
            "Generation 7's measured seconds per step, the EMA at step 951 of a run that ended in a failed state.",
            both,
        ),
        _entry(
            "cost.gen7.step",
            _field(facts["status"], "step"),
            "INT",
            "committed-record",
            {"path": STATUS_REL.as_posix(), "key": "step"},
            "The step at which generation 7's status file was last written.",
            ["verdict"],
        ),
        _entry(
            "cost.forscale.steps_low",
            FORSCALE_STEPS_LOW,
            "INT",
            "cited",
            {
                "path": AMENDMENTS_REL.as_posix(),
                "commit": AMENDMENTS_COMMIT,
                "token": "200,000",
            },
            "The lower for-scale step count the v2.4 amendments doc states, quoted for scale only.",
            both,
        ),
        _entry(
            "cost.forscale.steps_high",
            FORSCALE_STEPS_HIGH,
            "INT",
            "cited",
            {
                "path": RESEARCH_REL.as_posix(),
                "commit": RESEARCH_COMMIT,
                "token": "300,000",
            },
            "The upper for-scale step count the Phase 64 research page states, quoted for scale only.",
            both,
        ),
        _entry(
            "cost.example.steps",
            EXAMPLE_STEPS,
            "INT",
            "cited",
            {
                "path": RESEARCH_REL.as_posix(),
                "commit": RESEARCH_COMMIT,
                "token": "10\u2075 steps",
            },
            "The data-only illustration the research page states as 10 to the fifth steps, written as its decimal transcription.",
            ["verdict"],
        ),
    ]
    entries += [
        _arithmetic("cost.forscale.days_low", "F1", "forscale_days_low", "The lower for-scale step count at generation 7's rate, over 86,400 seconds: for scale only, not a forecast.", both),
        _arithmetic("cost.forscale.days_high", "F1", "forscale_days_high", "The upper for-scale step count at generation 7's rate, over 86,400 seconds: for scale only, not a forecast.", both),
        _arithmetic("cost.forscale.hours_low", "F1", "forscale_hours_low", "The lower for-scale step count at generation 7's rate, in hours.", []),
        _arithmetic("cost.example.seconds_per_step", "F6", "example_sps", "The median of the seven timing runs' seconds per step, the rate the example uses.", ["verdict"]),
        _arithmetic("cost.example.hours", "F1", "example_hours", "The 100,000-step data-only example at that median rate, in hours: a labelled illustration, not a plan.", ["verdict"]),
    ]
    return entries


def _cpu_entries(
    facts: Mapping[str, Any], ctx: Any, card: Any
) -> list[dict[str, Any]]:
    """Group 9: the CPU float64 re-derivation of the 14 states and the constant predictor.

    The Tier-1 limit is read from the scorecard's own tiers section, never a
    literal. The five 1632 arms share one reference, so the frozen arm data is
    loaded once per system and re-used for both states of every arm in it.
    """
    import numpy as np
    import torch

    from pinn.verification.feasibility_scorer import tier_defining_error
    from pinn.verification.learnability_arms import arm_spec
    from pinn.verification.learnability_data import load_arm_data

    tier1_max = float(_tier_level(card, 1)["E_max"])
    cache: dict[Any, Any] = {}

    def arm_data_for(arm_id: str) -> Any:
        system = arm_spec(arm_id).score_key.id
        if system not in cache:
            cache[system] = load_arm_data(
                arm_spec(arm_id),
                ctx,
                scorecard=card,
                dtype=torch.float32,
                device="cpu",
            )
        return cache[system]

    values: dict[str, Any] = {}
    derived_by: dict[tuple[str, str], dict[str, Any]] = {}
    entries: list[dict[str, Any]] = []
    for arm_id in ARMS:
        for state in CPU_STATES:
            derived = derive_state(
                ctx, card, arm_id, state, arm_data=arm_data_for(arm_id)
            )
            derived_by[(arm_id, state)] = derived
            e_sys = np.asarray(derived["e_sys"], dtype=np.float64)
            e_in = np.asarray(derived["e_in"], dtype=np.float64)
            error = np.maximum(e_sys, e_in)
            source = {
                "record": _record_rel(arm_id),
                "weights": _weights_rel(arm_id, state),
                "state": state,
            }
            rederived = f"Re-derived from the committed {arm_id} {state} weights on the CPU in float64"
            fields = (
                (
                    "E",
                    float(tier_defining_error(e_sys, e_in)),
                    "E4",
                    f"{rederived}; equals states.{state}.cross_check.E within 1e-12 and is never compared with the official E.",
                ),
                (
                    "e_sys_t0",
                    float(e_sys[0]),
                    "F3",
                    f"{rederived}: e_sys at the first scored time.",
                ),
                (
                    "e_in_t0",
                    float(e_in[0]),
                    "F3",
                    f"{rederived}: e_in at the first scored time.",
                ),
                (
                    "best_moment",
                    float(error.min()),
                    "F3",
                    f"{rederived}: the minimum over the scored times of max(e_sys, e_in).",
                ),
                (
                    "n_within_tier1",
                    int(np.count_nonzero(error <= tier1_max)),
                    "INT",
                    f"{rederived}: the scored times whose max(e_sys, e_in) is at or below the scorecard's Tier-1 E_max, inclusive.",
                ),
                (
                    "n_times",
                    int(len(derived["times"])),
                    "INT",
                    f"{rederived}: the number of scored times on the gold grid.",
                ),
                (
                    "timevar_ratio",
                    timevar_ratio(derived["pos"], derived["ref"]),
                    "E4",
                    f"{rederived}: RMS deviation of the output about its own time mean over the same for the real orbit, all bodies and coordinates.",
                ),
                (
                    "rms_ratio",
                    rms_ratio(derived["pos"], derived["ref"]),
                    "E4",
                    f"{rederived}: RMS error over the RMS of the orbit about its own mean, all bodies and coordinates.",
                ),
            )
            for field, value, rule, derivation in fields:
                entry_id = f"cpu.{arm_id}.{state}.{field}"
                values[entry_id] = value
                entries.append(
                    _entry(
                        entry_id,
                        value,
                        rule,
                        "rederived-cpu-float64",
                        source,
                        derivation,
                        [],
                    )
                )

    constants: dict[str, float] = {}
    for system in CPU_SYSTEMS:
        arm_id = f"r1-{system}"
        reference = derived_by[(arm_id, "adam")]
        e_sys, e_in = constant_predictor_error(
            reference["ref"], reference["inner_pair"]
        )
        value = float(tier_defining_error(e_sys, e_in))
        constants[system] = value
        entry_id = f"cpu.const.{system}.E"
        values[entry_id] = value
        entries.append(
            _entry(
                entry_id,
                value,
                "E4",
                "rederived-cpu-float64",
                {
                    "record": _record_rel(arm_id),
                    "weights": _weights_rel(arm_id, "adam"),
                    "state": "adam",
                },
                "Each body held at its time-mean position and scored with the frozen position_errors on the CPU in float64 against the "
                f"{system} gold reference; the r1-{system} adam weights are named for provenance and are not read by the constant predictor.",
                ["verdict"],
            )
        )

    summary = ctx.attestation.summary()
    _FACTS["attestation"] = summary
    opened = summary["opened"]
    counters = (
        ("test_split_opened", summary["test_split_opened"]),
        ("validation", opened["validation"]),
        ("other_under_root", opened["other_under_root"]),
        ("blocked_attempts", summary["blocked_attempts"]),
        ("refused_before_open", summary["refused_before_open"]),
    )
    for name, value in counters:
        entry_id = f"cpu.attestation.{name}"
        values[entry_id] = int(value)
        entries.append(
            _entry(
                entry_id,
                int(value),
                "INT",
                "arithmetic",
                {"formula": f"cpu_attestation_{name}"},
                f"The open attestation's {name} counter: every read in this run went through the Phase 59 allowlist.",
                [],
            )
        )

    _FACTS["cpu"] = values
    both = ["verdict", "charter"]
    entries += [
        _arithmetic(
            "cpu.const.range.min",
            "E4",
            "cpu_const_range_min",
            "The least constant-predictor E across the three systems.",
            both,
        ),
        _arithmetic(
            "cpu.const.range.max",
            "E4",
            "cpu_const_range_max",
            "The greatest constant-predictor E across the three systems.",
            both,
        ),
        _arithmetic(
            "cpu.range.e_sys_t0.min",
            "F3",
            "cpu_range_e_sys_t0_min",
            "The least e_sys at the first scored time across the 14 states.",
            ["verdict"],
        ),
        _arithmetic(
            "cpu.range.e_sys_t0.max",
            "F3",
            "cpu_range_e_sys_t0_max",
            "The greatest e_sys at the first scored time across the 14 states.",
            ["verdict"],
        ),
        _arithmetic(
            "cpu.range.e_in_t0.min",
            "F3",
            "cpu_range_e_in_t0_min",
            "The least e_in at the first scored time across the 14 states.",
            ["verdict"],
        ),
        _arithmetic(
            "cpu.range.e_in_t0.max",
            "F3",
            "cpu_range_e_in_t0_max",
            "The greatest e_in at the first scored time across the 14 states.",
            ["verdict"],
        ),
        _arithmetic(
            "cpu.range.best_moment.min",
            "F3",
            "cpu_range_best_moment_min",
            "The least best moment across the 14 states.",
            ["verdict"],
        ),
        _arithmetic(
            "cpu.range.best_moment.max",
            "F3",
            "cpu_range_best_moment_max",
            "The greatest best moment across the 14 states.",
            ["verdict"],
        ),
        _arithmetic(
            "cpu.range.timevar.min",
            "E4",
            "cpu_range_timevar_min",
            "The least time-variation ratio across the 14 states.",
            ["verdict"],
        ),
        _arithmetic(
            "cpu.range.timevar.max",
            "E4",
            "cpu_range_timevar_max",
            "The greatest time-variation ratio across the 14 states.",
            ["verdict"],
        ),
        _arithmetic(
            "cpu.range.rms_ratio.min",
            "E4",
            "cpu_range_rms_ratio_min",
            "The least RMS ratio across the 14 states.",
            ["verdict"],
        ),
        _arithmetic(
            "cpu.range.rms_ratio.max",
            "E4",
            "cpu_range_rms_ratio_max",
            "The greatest RMS ratio across the 14 states.",
            ["verdict"],
        ),
        _arithmetic(
            "cpu.total.n_within_tier1",
            "INT",
            "cpu_total_n_within_tier1",
            "The sum over the 14 states of the scored times within the Tier-1 limit.",
            ["verdict"],
        ),
        _arithmetic(
            "cpu.n_times",
            "INT",
            "cpu_n_times",
            "The number of scored times, the same on every state.",
            ["verdict"],
        ),
        _arithmetic(
            "const_gap.min",
            "E4",
            "const_gap_min",
            "The least gap between a system's official Rung-1 E and its constant-predictor E.",
            ["verdict"],
        ),
        _arithmetic(
            "const_gap.max",
            "E4",
            "const_gap_max",
            "The greatest gap between a system's official Rung-1 E and its constant-predictor E.",
            ["verdict"],
        ),
    ]
    return entries


def _cited_entries() -> list[dict[str, Any]]:
    """Group 8: the published and gap figures, each pinned to a commit."""
    research = RESEARCH_REL.as_posix()
    gaps = GAPS_REL.as_posix()
    project = PROJECT_REL.as_posix()
    both = ["verdict", "charter"]
    rows = [
        ("pub.breen.energy_typical", "10\u207b\u00b2", research, RESEARCH_COMMIT, "of order 10\u207b\u00b2", both, "Breen et al.'s relative energy error, quoted from the Phase 64 research page."),
        ("pub.breen.energy_projected", "10\u207b\u2075", research, RESEARCH_COMMIT, "brings it to order 10\u207b\u2075", ["verdict"], "Breen et al.'s energy error after the projection layer, quoted from the research page."),
        ("pub.kollias.energy_range", "0.02\u20133%", research, RESEARCH_COMMIT, "to within \u223c 0.02\u20133%", both, "The 2026 study's relative energy error over one orbital period; the research page corrects the amendment's 0.08-3%."),
        ("pub.kollias.euler", "7.74 \u00d7 10\u207b\u2074", research, RESEARCH_COMMIT, "Euler 7.74 \u00d7 10\u207b\u2074", ["verdict"], "The 2026 study's Euler-orbit energy error, quoted from the research page."),
        ("pub.kollias.lagrange", "3.23 \u00d7 10\u207b\u00b2", research, RESEARCH_COMMIT, "Lagrange 3.23 \u00d7 10\u207b\u00b2", ["verdict"], "The 2026 study's Lagrange-orbit energy error, quoted from the research page."),
        ("pub.kollias.figure8", "1.64 \u00d7 10\u207b\u2074", research, RESEARCH_COMMIT, "figure-eight 1.64 \u00d7 10\u207b\u2074", ["verdict"], "The 2026 study's figure-eight energy error, quoted from the research page."),
        ("pub.kollias.adam_epochs", "2 to 3 \u00d7 10\u2075", research, RESEARCH_COMMIT, "2 to 3 \u00d7 10\u2075 Adam epochs", ["verdict"], "The 2026 study's Adam training length for one forward orbit, quoted from the research page."),
        ("pub.kollias.lbfgs_epochs", "1.5 \u00d7 10\u2074", research, RESEARCH_COMMIT, "1.5 \u00d7 10\u2074 L-BFGS epochs", ["verdict"], "The 2026 study's L-BFGS training length for one forward orbit, quoted from the research page."),
        ("gap5908.floor.1632", "4.7e-2", gaps, GAPS_COMMIT, "4.7e-2, 2.1e-1 and 3.8e-1", ["charter"], "The finite-difference eps_h floor GAP-59-08 measured on system 1632."),
        ("gap5908.floor.851", "2.1e-1", gaps, GAPS_COMMIT, "4.7e-2, 2.1e-1 and 3.8e-1", ["charter"], "The finite-difference eps_h floor GAP-59-08 measured on system 851."),
        ("gap5908.floor.4658", "3.8e-1", gaps, GAPS_COMMIT, "4.7e-2, 2.1e-1 and 3.8e-1", ["charter"], "The finite-difference eps_h floor GAP-59-08 measured on system 4658."),
        ("gap5908.floor_range", "5\u201338%", gaps, GAPS_COMMIT, "5\u201338%", ["charter"], "The exact Brutus answer's own score range on the coarse grid, GAP-59-08's floor."),
        ("machine.model", "Apple M5 Pro", project, PROJECT_COMMIT, "Apple M5 Pro", ["verdict"], "The machine every number here was measured on, from PROJECT.md."),
        ("machine.memory", "24 GB", project, PROJECT_COMMIT, "24 GB", ["verdict"], "The machine's unified memory, from PROJECT.md."),
    ]
    return [
        _entry(
            entry_id,
            value,
            "LIT",
            "cited",
            {"path": path, "commit": commit, "token": token},
            derivation,
            required,
        )
        for entry_id, value, path, commit, token, required, derivation in rows
    ]


def build_manifest(repo_root: Path) -> dict[str, Any]:
    """The whole manifest. One real context per process; nothing is written here."""
    import torch

    from pinn.verification.learnability_data import open_real_context

    root = Path(repo_root)
    torch.set_num_threads(1)
    facts = _facts(root)
    _FACTS.clear()
    _FACTS.update(facts)
    card = facts["card"]
    ctx = open_real_context(repo_root=root)

    total_hours = _f_hours(facts, ARMS)
    stored_total = facts["handoff"].get("total_wall_hours")
    if total_hours != stored_total:
        fail(
            "the seven wall.hours do not sum to the handoff's total_wall_hours: "
            f"ordered_sum {total_hours!r} != stored {stored_total!r}"
        )

    entries = (
        _arm_entries(facts)
        + _aggregate_entries(facts)
        + _handoff_entries(facts)
        + _scorecard_entries(facts)
        + _baseline_entries(facts)
        + _survey_entries(facts)
        + _cost_entries(facts)
        + _cpu_entries(facts, ctx, card)
        + _cited_entries()
    )

    entries.sort(key=lambda entry: entry["id"])
    ids = [entry["id"] for entry in entries]
    if len(set(ids)) != len(ids):
        duplicates = sorted({entry_id for entry_id in ids if ids.count(entry_id) > 1})
        fail(f"the manifest names these ids twice: {duplicates!r}")

    attestation = ctx.attestation
    if attestation is None:
        fail("the real context carries no open attestation")
    return {
        "schema": SCHEMA,
        "plain_language": (
            "Every number the Phase 64 verdict and charter quote, each with the "
            "file it comes from and how it was computed, re-derived independently "
            "by verify_phase64_verdict.py."
        ),
        "producer_sha256": {
            relative: sha256_file(root / relative) for relative in PRODUCER_MODULES
        },
        "scorecard_sha256": sha256_file(root / SCORECARD_REL),
        "handoff_sha256": sha256_file(root / HANDOFF_REL),
        "inputs": _inputs(root, ARMS),
        "attestation": attestation.summary(),
        "entries": entries,
    }


def cmd_numbers(*, check: bool) -> int:
    """Write the manifest, or regenerate it and compare the committed bytes."""
    from pinn.verification import evidence_io

    os.chdir(REPO_ROOT)
    payload = build_manifest(REPO_ROOT)
    raw = evidence_io.canonical_json_bytes(payload)
    target = REPO_ROOT / NUMBERS_REL
    if check:
        if not evidence_io.bytes_identical(target, raw):
            print("NUMBERS-CHECK-DIFF", file=sys.stderr)
            return 1
        print("NUMBERS-CHECK-OK")
        return 0
    digest = evidence_io.write_json(target, payload)
    print(f"NUMBERS-WRITTEN {digest}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("numbers",))
    parser.add_argument(
        "--check",
        action="store_true",
        help="regenerate in this process and compare the committed bytes",
    )
    return parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = build_parser().parse_args(list(argv) if argv is not None else None)
    try:
        if args.command == "numbers":
            return cmd_numbers(check=bool(args.check))
    except Exception as exc:  # noqa: BLE001 - fail-closed CLI
        print(str(exc), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
