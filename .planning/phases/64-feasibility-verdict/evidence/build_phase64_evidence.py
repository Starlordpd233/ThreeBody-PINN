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
    current = payload
    for part in dotted.split("."):
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


def derive_state(ctx: Any, card: Any, arm_id: str, state: str) -> dict[str, Any]:
    """Re-score one committed weights file on the CPU in float64.

    The record, the arm catalog and the frozen loaders supply the reference; the
    weights file's SHA-256 is checked against the record before ``torch.load``
    with ``weights_only=True``. Returns ``pos``, ``ref``, ``times``,
    ``inner_pair``, ``e_sys`` and ``e_in``, one value per scored time.
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


def _inputs(repo_root: Path, record_arms: Sequence[str]) -> list[dict[str, str]]:
    """Every committed file a value is read from, sorted by path."""
    rels = {
        SCORECARD_REL.as_posix(),
        HANDOFF_REL.as_posix(),
        *_retained_rels(),
    }
    for arm_id in record_arms:
        rels.add(_record_rel(arm_id))
    entries = []
    for relative in sorted(rels):
        path = repo_root / relative
        if not path.is_file():
            fail(f"input is missing: {relative}")
        entries.append({"path": relative, "sha256": sha256_file(path)})
    return entries


def build_manifest(repo_root: Path) -> dict[str, Any]:
    """The whole manifest. One real context per process; nothing is written here."""
    import torch

    from pinn.verification.feasibility_scorer import tier_defining_error
    from pinn.verification.feasibility_scorecard import load_scorecard
    from pinn.verification.learnability_data import open_real_context

    root = Path(repo_root)
    torch.set_num_threads(1)
    card = load_scorecard()
    ctx = open_real_context(repo_root=root)
    handoff = _read_json(root / HANDOFF_REL)
    records = {arm_id: _read_json(root / _record_rel(arm_id)) for arm_id in ARMS}

    total_hours = ordered_sum(records[arm_id]["wall"]["hours"] for arm_id in ARMS)
    stored_total = handoff.get("total_wall_hours")
    if total_hours != stored_total:
        fail(
            "the seven wall.hours do not sum to the handoff's total_wall_hours: "
            f"ordered_sum {total_hours!r} != stored {stored_total!r}"
        )

    entries = [
        _entry(
            "arm.r1-1632.E",
            records["r1-1632"]["result"]["E"],
            "E4",
            "official-mps-float32",
            {"path": _record_rel("r1-1632"), "key": "result.E"},
            "result.E of the committed r1-1632 record: the official score the arm wrote on the MPS device in float32.",
            ["verdict"],
        ),
        _entry(
            "hours.total",
            total_hours,
            "F3",
            "arithmetic",
            {"formula": "hours_total"},
            "ordered_sum over the seven records' wall.hours in handoff arm order, the explicit left-to-right += loop from 0.0.",
            ["verdict", "charter"],
        ),
        _entry(
            "pub.kollias.energy_range",
            "0.02\u20133%",
            "LIT",
            "cited",
            {
                "path": RESEARCH_REL.as_posix(),
                "commit": RESEARCH_COMMIT,
                "token": "to within \u223c 0.02\u20133%",
            },
            "The 2026 study's relative energy error over one orbital period, quoted from the Phase 64 research page.",
            ["verdict", "charter"],
        ),
    ]

    derived = derive_state(ctx, card, "r1-1632", "polish")
    entries.append(
        _entry(
            "cpu.r1-1632.polish.E",
            tier_defining_error(derived["e_sys"], derived["e_in"]),
            "E4",
            "rederived-cpu-float64",
            {
                "record": _record_rel("r1-1632"),
                "weights": _weights_rel("r1-1632", "polish"),
                "state": "polish",
            },
            "Re-scored from the committed polish weights on the CPU in float64; equals states.polish.cross_check.E within 1e-12 and is never compared with the official E.",
            ["verdict"],
        )
    )
    entries.sort(key=lambda entry: entry["id"])

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
