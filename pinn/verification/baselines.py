"""Phase 59 (FEAS-07; D-15, D-16, D-17, D-38): the comparison-point runner.

Scores the two no-learning comparison points with the FEAS-01 scorer: the
two-Kepler formula on every panel system and on the whole Stage-0 population,
and the nearest-neighbour copy on the validation panel. The corpus is read
only through the split allowlist and the production reference. The freeze
guard runs before any read in every mode, and every mode ends with the
600-second runtime gate. The physics-residual columns are context only; they
never change E or a tier.
"""

from __future__ import annotations

import argparse
import dataclasses
import hashlib
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

from pinn.constants import T_CHARACTERISTIC_TIME
from pinn.verification import evidence_io, split_allowlist
from pinn.verification.feasibility_scorecard import SCORECARD_SHA256, load_scorecard
from pinn.verification.feasibility_scorer import (
    fd_context_eps_h,
    load_governed_r_ref,
    physics_residual_context,
    score_trajectory,
)
from pinn.verification.production_reference import load_reference
from pinn.verification.split_allowlist import (
    GENERATION7_SPLITS_REL,
    AllowlistedCorpusReader,
    SplitAllowlist,
    expected_splits_sha256,
    install_open_attestation,
    resolve_data_root,
)
from pinn.verification.two_kepler import (
    NotApplicable,
    two_kepler_accelerations,
    two_kepler_prediction,
)

_REPO_ROOT = Path(__file__).resolve().parents[2]
_PANELS_REL = Path(".planning/phases/59-read-only-baseline-scorecard/evidence/census/panels.json")
_CENSUS_CSV_REL = Path(".planning/phases/59-read-only-baseline-scorecard/evidence/census/census.csv")
PRODUCER_MODULES = (
    "pinn/verification/baselines.py",
    "pinn/verification/two_kepler.py",
    "pinn/verification/nn_copy.py",
    "pinn/verification/feasibility_scorer.py",
    "pinn/verification/feasibility_scorecard.py",
    "pinn/verification/split_allowlist.py",
    "pinn/verification/production_reference.py",
    "pinn/verification/evidence_io.py",
)


class BaselinesHalt(RuntimeError):
    """Fail closed. ``main`` prints ``BASELINES-HALT: <reason>`` and returns 2."""


def with_residual_context(result, positions, accelerations, masses, *, r_ref):
    """``result`` with the FEAS-01(i) residual columns filled. Nothing else changes."""
    context = physics_residual_context(positions, accelerations, masses, r_ref=r_ref)
    return dataclasses.replace(
        result,
        physics_residual_mean=context["mean"],
        physics_residual_max=context["max"],
    )


def _window(reference, t_max):
    """Times, positions and velocities with t <= t_max (+1e-9)."""
    times = np.asarray(reference.times, dtype=np.float64).reshape(-1)
    keep = times <= float(t_max) + 1e-9
    return (
        times[keep],
        np.asarray(reference.positions, dtype=np.float64)[keep],
        np.asarray(reference.velocities, dtype=np.float64)[keep],
    )


def _t_max(scorecard):
    return float(scorecard.section("scoring_grid")["t_max"])


def _require_pair(gold_reference, base_reference):
    if base_reference is None:
        return
    if not np.array_equal(
        np.asarray(base_reference.permutation), np.asarray(gold_reference.permutation),
    ):
        raise BaselinesHalt(
            f"base and gold permutations differ for id {int(gold_reference.record_key.id)}"
        )


def score_formula(gold_reference, *, scorecard, base_reference=None, r_ref):
    """Score the two-Kepler formula from the gold t = 0 state (D-15, D-30, D-31)."""
    identifier = int(gold_reference.record_key.id)
    inner_pair = tuple(int(slot) for slot in gold_reference.inner_pair)
    masses = np.asarray(gold_reference.masses, dtype=np.float64).reshape(3)
    t_max = _t_max(scorecard)
    _require_pair(gold_reference, base_reference)
    times, positions, velocities = _window(gold_reference, t_max)
    elapsed = (times - times[0]) / float(T_CHARACTERISTIC_TIME)
    try:
        predicted, predicted_v = two_kepler_prediction(
            positions[0], velocities[0], masses, inner_pair, elapsed,
        )
    except NotApplicable as exc:
        return {"id": identifier, "applicable": False, "reason": exc.reason}
    result = score_trajectory(
        predicted, predicted_v, positions, masses, inner_pair, times,
        velocity_source="analytic", scorecard=scorecard, grid="gold",
    )
    result = with_residual_context(
        result, predicted, two_kepler_accelerations(predicted, masses, inner_pair), masses,
        r_ref=r_ref,
    )
    row = {"id": identifier, "inner_pair": list(inner_pair), "applicable": True}
    row.update(result.to_json_dict())
    if base_reference is not None:
        base_times, base_positions, _base_v = _window(base_reference, t_max)
        base_u = (base_times - times[0]) / float(T_CHARACTERISTIC_TIME)
        base_predicted, base_predicted_v = two_kepler_prediction(
            positions[0], velocities[0], masses, inner_pair, base_u,
        )
        base_result = score_trajectory(
            base_predicted, base_predicted_v, base_positions, masses, inner_pair, base_times,
            velocity_source="analytic", scorecard=scorecard, grid="base",
        )
        row["E_base"] = base_result.to_json_dict()["E"]
        row["tier_base"] = int(base_result.tier)
        row["eps_h_fd_context_base"] = evidence_io.json_safe(
            float(fd_context_eps_h(base_predicted, base_u, masses))
        )
    return row


def _open_context(args):
    scorecard = load_scorecard()
    allowlist = SplitAllowlist.from_manifest(
        _REPO_ROOT / GENERATION7_SPLITS_REL,
        expected_sha256=expected_splits_sha256(_REPO_ROOT),
    )
    data_root, source = resolve_data_root(args.data_root)
    attestation = install_open_attestation(
        data_root=data_root,
        data_root_source=source,
        withheld_basenames=allowlist.withheld_basenames(),
        split_by_basename=allowlist.split_by_basename(),
    )
    reader = AllowlistedCorpusReader(
        allowlist=allowlist, data_root=data_root, data_root_source=source,
    )
    return scorecard, allowlist, reader, attestation, data_root, source


def _sha256_file(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def _load_panels():
    """The committed panels, after checking their scorecard and census digests."""
    path = _REPO_ROOT / _PANELS_REL
    raw = path.read_bytes()
    panels = json.loads(raw.decode("utf-8"))
    if panels.get("scorecard_sha256") != SCORECARD_SHA256:
        raise BaselinesHalt("panels.json scorecard_sha256 is not the frozen scorecard")
    if panels.get("census_csv_sha256") != _sha256_file(_REPO_ROOT / _CENSUS_CSV_REL):
        raise BaselinesHalt("panels.json census_csv_sha256 does not match census.csv")
    return panels, hashlib.sha256(raw).hexdigest()


def _keys(identifier):
    from pinn.data.types import RecordKey

    return (
        RecordKey("hierarchical", "base", int(identifier)),
        RecordKey("hierarchical", "gold", int(identifier)),
    )


def _stdout_singles(args):
    scorecard, _allowlist, reader, _attestation, _root, _source = _open_context(args)
    panels, _digest = _load_panels()
    r_ref = load_governed_r_ref()
    for single in sorted(panels["singles"], key=lambda row: int(row["id"])):
        base_key, gold_key = _keys(single["id"])
        gold = load_reference(reader, gold_key)
        base = load_reference(reader, base_key)
        row = score_formula(gold, scorecard=scorecard, base_reference=base, r_ref=r_ref)
        print(json.dumps(evidence_io.json_safe(row), sort_keys=True))
    return 0


def _parse_args(argv):
    parser = argparse.ArgumentParser(prog="baselines")
    parser.add_argument("--panel", choices=("singles",), default=None)
    parser.add_argument("--stdout", action="store_true")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--data-root", default=None)
    parser.add_argument("--evidence-root", default=None)
    return parser.parse_args(argv)


def _run(argv, *, started_wall, started):
    args = _parse_args(argv)
    try:
        freeze = evidence_io.require_frozen_scorecard(_REPO_ROOT)
    except evidence_io.FreezeNotEstablished as exc:
        print(f"FREEZE-REFUSED: {exc}", file=sys.stderr)
        return 1
    print(f"FREEZE-OK {freeze['freeze_commit']}", file=sys.stderr)
    if args.panel or args.stdout:
        if not (args.panel and args.stdout) or args.check:
            raise BaselinesHalt("--panel and --stdout are a read-only pair")
        return _stdout_singles(args)
    raise BaselinesHalt("the full run is not implemented yet")


def main(argv=None) -> int:
    """Baselines CLI. The freeze guard runs before any corpus or checkpoint read."""
    started_wall = datetime.now(timezone.utc).isoformat()
    started = time.monotonic()
    try:
        code = _run(argv, started_wall=started_wall, started=started)
    except BaselinesHalt as exc:
        print(f"BASELINES-HALT: {exc}", file=sys.stderr)
        code = 2
    except split_allowlist.SplitRefused as exc:
        print(f"SplitRefused: {exc}", file=sys.stderr)
        code = 2
    gate = evidence_io.runtime_gate(time.monotonic() - started, label="BASELINES")
    if gate != 0:
        return gate
    return code


if __name__ == "__main__":
    raise SystemExit(main())


__all__ = [
    "PRODUCER_MODULES",
    "BaselinesHalt",
    "main",
    "score_formula",
    "with_residual_context",
]
