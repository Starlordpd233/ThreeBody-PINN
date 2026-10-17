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
import csv
import dataclasses
import hashlib
import io
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

from pinn.constants import T_CHARACTERISTIC_TIME
from pinn.data.preprocessing import normalize_ic13
from pinn.training.validation_gate import json_safe_float
from pinn.verification import evidence_io, split_allowlist
from pinn.verification.feasibility_scorecard import SCORECARD_SHA256, load_scorecard
from pinn.verification.feasibility_scorer import (
    fd_context_eps_h,
    load_governed_r_ref,
    physics_residual_context,
    score_trajectory,
)
from pinn.verification.nn_copy import (
    copy_accelerations,
    copy_prediction,
    nearest_training_neighbour,
)
from pinn.verification.production_reference import (
    load_reference,
    load_retained_checkpoint,
    recover_normalizer_from_checkpoint,
    stats_digest,
)
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
    formula_applicability,
    two_kepler_accelerations,
    two_kepler_prediction,
)

_REPO_ROOT = Path(__file__).resolve().parents[2]
_PANELS_REL = Path(".planning/phases/59-read-only-baseline-scorecard/evidence/census/panels.json")
_CENSUS_CSV_REL = Path(".planning/phases/59-read-only-baseline-scorecard/evidence/census/census.csv")
_AUDIT_REL = Path(
    ".planning/phases/59-read-only-baseline-scorecard/evidence/audit/reader_acceptance.json"
)
_R_REF_ARTIFACT = "pinn/verification/artifacts/r_ref_stage0.json"
_RUN_NAME = "stage0-v23g7-seed42"
_INIT_FILE = "stage-0-init.pt"
_POPULATIONS = (("train", 1812), ("validation", 227))
_POPULATION_COLUMNS = (
    "split", "id", "applicable", "E", "tier", "eps_h", "physics_residual_mean",
    "physics_residual_max", "E_base", "tier_base", "eps_h_fd_context_base",
)
_COPY_FIELDS = (
    "E", "e_sys_max", "e_in_max", "h", "eps_h", "tier",
    "physics_residual_mean", "physics_residual_max",
)
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


def candidate_pool(allowlist):
    """The Stage-0 training hierarchical base keys, sorted. No validation key."""
    pool = sorted(
        allowlist.records("train", variant="hierarchical", fidelity="base", stage=0)
    )
    for key in pool:
        if allowlist.require(key) != "train":
            raise BaselinesHalt(f"candidate {key} is not in the training split")
    return tuple(pool)


def score_copy(query_gold, neighbour_gold, distance, *, scorecard, r_ref,
               query_base=None, neighbour_base=None):
    """Score the copy of ``neighbour_gold`` as the prediction for ``query_gold`` (D-16)."""
    t_max = _t_max(scorecard)
    positions, velocities, neighbour_masses, times = copy_prediction(
        query_gold, neighbour_gold, t_max=t_max,
    )
    _times, reference, _velocities = _window(query_gold, t_max)
    inner_pair = tuple(int(slot) for slot in query_gold.inner_pair)
    query_masses = np.asarray(query_gold.masses, dtype=np.float64).reshape(3)
    result = score_trajectory(
        positions, velocities, reference, neighbour_masses, inner_pair, times,
        velocity_source="brutus", scorecard=scorecard, grid="gold",
    )
    result = with_residual_context(
        result, positions, copy_accelerations(neighbour_gold, t_max=t_max), query_masses,
        r_ref=r_ref,
    )
    scored = result.to_json_dict()
    row = {
        "id": int(query_gold.record_key.id),
        "neighbour_id": int(neighbour_gold.record_key.id),
        "distance": float(distance),
    }
    row.update({name: scored[name] for name in _COPY_FIELDS})
    if query_base is not None and neighbour_base is not None:
        base_positions, base_velocities, base_masses, base_times = copy_prediction(
            query_base, neighbour_base, t_max=t_max,
        )
        _bt, base_reference, _bv = _window(query_base, t_max)
        base_result = score_trajectory(
            base_positions, base_velocities, base_reference, base_masses, inner_pair, base_times,
            velocity_source="brutus", scorecard=scorecard, grid="base",
        )
        row["E_base"] = base_result.to_json_dict()["E"]
        row["tier_base"] = int(base_result.tier)
    return row


def feas09_record(allowlist):
    """The formula is not applicable on the FEAS-09 probes (D-38).

    Verified from the manifest: every training-split hierarchical base record
    has manifest stage 0 or 1, so no hierarchical record can enter Stage 4b
    or Stage 6 under the frozen precedence.
    """
    every = allowlist.records("train", variant="hierarchical", fidelity="base")
    staged = (
        len(allowlist.records("train", variant="hierarchical", fidelity="base", stage=0))
        + len(allowlist.records("train", variant="hierarchical", fidelity="base", stage=1))
    )
    if staged == len(every):
        entry = formula_applicability("standard")
        verified = True
    else:
        entry = "unknown: see survey picks"
        verified = False
    return {
        "stage4b": entry,
        "stage6": entry,
        "hierarchical_records_all_stage_0_or_1": verified,
        "training_hierarchical_base_records": len(every),
    }


def _census_samples():
    path = _REPO_ROOT / _CENSUS_CSV_REL
    with path.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    samples = {}
    for row in rows:
        value = row.get("samples_per_inner_period") or ""
        samples[int(row["id"])] = float(value) if value else None
    return samples, {int(row["id"]) for row in rows if row["split"] == "train"}


def _recover_normalizer(reader, scorecard):
    payload, _provenance = load_retained_checkpoint(
        _REPO_ROOT, _RUN_NAME, _INIT_FILE, expected_step=0,
    )
    tolerance = float(scorecard.section("diag07")["tolerances"]["normalizer_recovery_max_abs"])
    recovered = recover_normalizer_from_checkpoint(reader, payload, tolerance=tolerance)
    del payload
    digest = stats_digest(recovered["stats"])
    audit = json.loads((_REPO_ROOT / _AUDIT_REL).read_text(encoding="utf-8"))
    expected = audit["normalizer"]["stats_sha256"]
    if digest != expected:
        raise BaselinesHalt(f"normalizer stats_sha256 {digest} != audit {expected}")
    return recovered["stats"], digest


def _gold_keys(allowlist, split):
    keys = allowlist.records(split, variant="hierarchical", fidelity="gold", stage="UNASSIGNED")
    return {int(key.id): key for key in keys}


def collect(args):
    """Score the formula on every Stage-0 system and the copy on the validation panel."""
    scorecard, allowlist, reader, attestation, data_root, source = _open_context(args)
    panels, panels_sha256 = _load_panels()
    samples, census_train = _census_samples()
    stats, normalizer_sha256 = _recover_normalizer(reader, scorecard)
    r_ref = load_governed_r_ref()
    formula = {"train": {}, "validation": {}}
    normalized = {"train": {}, "validation": {}}
    kept = {}
    pool = candidate_pool(allowlist)
    for split, expected in _POPULATIONS:
        bases = sorted(allowlist.records(split, variant="hierarchical", fidelity="base", stage=0))
        golds = _gold_keys(allowlist, split)
        if len(bases) != expected:
            raise BaselinesHalt(f"{split} Stage-0 population {len(bases)} != {expected}")
        for index, base_key in enumerate(bases, start=1):
            gold_key = golds.get(int(base_key.id))
            if gold_key is None:
                raise BaselinesHalt(f"gold record is absent for id {int(base_key.id)}")
            base = load_reference(reader, base_key)
            gold = load_reference(reader, gold_key)
            formula[split][int(base_key.id)] = score_formula(
                gold, scorecard=scorecard, base_reference=base, r_ref=r_ref,
            )
            normalized[split][base_key] = normalize_ic13(base.raw_ic13, stats)
            if split == "validation":
                kept[int(base_key.id)] = (gold, base)
            del base, gold
            if index == expected or index % 500 == 0:
                print(f"formula {split} {index}/{expected}", file=sys.stderr)
    if set(normalized["train"]) != set(pool):
        raise BaselinesHalt("the candidate pool differs from the Stage-0 training population")
    if {int(key.id) for key in pool} != census_train:
        raise BaselinesHalt("the candidate pool differs from the census training ids")
    candidates = [(key, normalized["train"][key]) for key in pool]
    neighbours = {}
    for query_key, vector in sorted(normalized["validation"].items()):
        neighbours[int(query_key.id)] = nearest_training_neighbour(query_key, vector, candidates)
    copies = {}
    for identifier in sorted(neighbours):
        neighbour_key, distance = neighbours[identifier]
        base_key, gold_key = _keys(neighbour_key.id)
        neighbour_gold = load_reference(reader, gold_key)
        neighbour_base = load_reference(reader, base_key)
        query_gold, query_base = kept[identifier]
        copies[identifier] = score_copy(
            query_gold, neighbour_gold, distance, scorecard=scorecard, r_ref=r_ref,
            query_base=query_base, neighbour_base=neighbour_base,
        )
        del neighbour_gold, neighbour_base
    print(f"copy validation {len(copies)}/227", file=sys.stderr)
    return {
        "scorecard": scorecard,
        "panels": panels,
        "panels_sha256": panels_sha256,
        "samples": samples,
        "formula": formula,
        "copies": copies,
        "feas09": feas09_record(allowlist),
        "normalizer_sha256": normalizer_sha256,
        "r_ref": r_ref,
        "attestation": attestation,
        "data_root": data_root,
        "data_root_source": source,
    }


def _producer():
    return evidence_io.module_hashes(PRODUCER_MODULES, repo_root=_REPO_ROOT)


def _panel_ids(panels):
    return {
        "singles": sorted(int(row["id"]) for row in panels["singles"]),
        "family": sorted(int(row["id"]) for row in panels["family"]),
        "validation": sorted(int(value) for value in panels["validation"]),
    }


def _tier_counts(rows):
    counts = {"0": 0, "1": 0, "2": 0, "3": 0, "not_applicable": 0}
    for row in rows:
        if row.get("applicable") is False:
            counts["not_applicable"] += 1
            continue
        counts[str(int(row["tier"]))] += 1
    return counts


def _at_least_tier1(rows):
    return sum(1 for row in rows if row.get("applicable", True) and int(row["tier"]) >= 1)


def _median(values):
    finite = [float(value) for value in values if isinstance(value, (int, float)) and np.isfinite(value)]
    return float(np.median(finite)) if finite else None


def _formula_rows(collected, split):
    return [collected["formula"][split][key] for key in sorted(collected["formula"][split])]


def _cell(value):
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, int):
        return str(value)
    if isinstance(value, float):
        safe = json_safe_float(value)
        return safe if isinstance(safe, str) else repr(float(value))
    return str(value)


def population_csv(collected):
    buffer = io.StringIO()
    writer = csv.writer(buffer, lineterminator="\n")
    writer.writerow(_POPULATION_COLUMNS)
    for split, _expected in _POPULATIONS:
        for row in _formula_rows(collected, split):
            record = {"split": split, **row}
            writer.writerow([_cell(record.get(name)) for name in _POPULATION_COLUMNS])
    return buffer.getvalue()


def build_payloads(collected):
    """The baselines result files as payloads and text, ready to write or compare."""
    panels = collected["panels"]
    ids = _panel_ids(panels)
    producer = _producer()
    train_rows = _formula_rows(collected, "train")
    validation_rows = _formula_rows(collected, "validation")
    copy_rows = [collected["copies"][key] for key in sorted(collected["copies"])]
    by_id = {**collected["formula"]["train"], **collected["formula"]["validation"]}
    panel_rows = {}
    for panel, members in ids.items():
        rows = []
        for identifier in members:
            row = dict(by_id[identifier])
            row["samples_per_inner_period"] = collected["samples"].get(identifier)
            rows.append(row)
        panel_rows[panel] = rows
    tier1_train = _at_least_tier1(train_rows)
    tier1_validation = _at_least_tier1(validation_rows)
    copy_tier1 = _at_least_tier1(copy_rows)
    formula_median = {"train": _median(row.get("E") for row in train_rows),
                      "validation": _median(row.get("E") for row in validation_rows)}
    copy_median = _median(row["E"] for row in copy_rows)
    two_kepler = {
        "schema": "phase59-two-kepler/v1",
        "plain_language": (
            "The two-Kepler formula treats the inner pair and the outer body as two "
            "separate textbook orbits, started from each system's own t = 0 state, "
            "and is scored with the same FEAS-01 scorer the networks face, on the "
            "dense gold grid with its own analytic velocities. "
            f"{_at_least_tier1(panel_rows['singles'] + panel_rows['family'] + panel_rows['validation'])} "
            f"of the {sum(len(rows) for rows in panel_rows.values())} panel rows reach Tier 1 or better."
        ),
        "scorecard_sha256": SCORECARD_SHA256,
        "producer_sha256": producer,
        "panels_sha256": collected["panels_sha256"],
        "ids": sorted(set(ids["singles"]) | set(ids["family"]) | set(ids["validation"])),
        "rows": panel_rows,
    }
    nn_copy = {
        "schema": "phase59-nn-copy/v1",
        "plain_language": (
            "Each of the 227 validation systems is predicted by copying the Brutus "
            "trajectory of its nearest Stage-0 training system in production-normalized "
            f"IC13. {copy_tier1} of 227 copies reach Tier 1 or better; the median E is "
            f"{copy_median:.3g}."
        ),
        "scorecard_sha256": SCORECARD_SHA256,
        "producer_sha256": producer,
        "normalizer_stats_sha256": collected["normalizer_sha256"],
        "rows": copy_rows,
    }
    panel_counts = {panel: _tier_counts(rows) for panel, rows in panel_rows.items()}
    panel_counts["train"] = _tier_counts(train_rows)
    panel_counts["validation_population"] = _tier_counts(validation_rows)
    baselines = {
        "schema": "phase59-baselines/v1",
        "plain_language": (
            f"The two-Kepler formula reaches Tier 1 or better on {tier1_train} of 1812 "
            f"Stage-0 training systems and {tier1_validation} of 227 validation systems. "
            f"The nearest-neighbour copy reaches Tier 1 or better on {copy_tier1} of 227 "
            "validation systems."
        ),
        "scorecard_sha256": SCORECARD_SHA256,
        "producer_sha256": producer,
        "physics_residual": {
            "r_ref": collected["r_ref"],
            "r_ref_artifact": _R_REF_ARTIFACT,
            "role": "context only, never tier-defining",
            "median_physics_residual_mean": {
                "formula_train": _median(row.get("physics_residual_mean") for row in train_rows),
                "formula_validation": _median(
                    row.get("physics_residual_mean") for row in validation_rows
                ),
                "copy_validation": _median(row["physics_residual_mean"] for row in copy_rows),
            },
        },
        "formula_tier_counts": panel_counts,
        "formula_reaches_tier1_on_stage0": {
            "train": f"{tier1_train} of 1812",
            "validation": f"{tier1_validation} of 227",
        },
        "nn_copy_tier_counts": _tier_counts(copy_rows),
        "nn_copy_reaches_tier1_on_validation": f"{copy_tier1} of 227",
        "median_E": {
            "formula_train": formula_median["train"],
            "formula_validation": formula_median["validation"],
            "copy_validation": copy_median,
        },
        "feas09": collected["feas09"],
        "normalizer_stats_sha256": collected["normalizer_sha256"],
    }
    summary = _summary_markdown(baselines, panel_counts, formula_median, copy_median, collected)
    return {
        "two_kepler.json": two_kepler,
        "two_kepler_population.csv": population_csv(collected),
        "nn_copy.json": nn_copy,
        "baselines.json": baselines,
        "summary.md": summary,
    }


def _summary_markdown(baselines, panel_counts, formula_median, copy_median, collected):
    reach = baselines["formula_reaches_tier1_on_stage0"]
    copy_reach = baselines["nn_copy_reaches_tier1_on_validation"]
    formula_answer = (
        "No. The formula does not already reach Tier 1 on Stage 0"
        if reach["train"].startswith("0 ") and reach["validation"].startswith("0 ")
        else "Partly. The formula reaches Tier 1 on some Stage-0 systems"
    )
    lines = [
        "## In plain language",
        "",
        f"{formula_answer}: it reaches Tier 1 or better (E at most 0.1) on {reach['train']} "
        f"training systems and {reach['validation']} validation systems. Its median E is "
        f"{formula_median['train']:.3g} on the training systems and "
        f"{formula_median['validation']:.3g} on the validation systems. Treating the inner "
        "pair and the outer body as two separate textbook orbits misses the third body's "
        "pull, and the error grows over the inner laps.",
        "",
        f"Copying the nearest training system reaches Tier 1 or better on {copy_reach} "
        f"validation systems, with a median E of {copy_median:.3g}. That is how densely "
        "1,812 systems cover Stage 0: the nearest training system starts close in the "
        "network's own input coordinates, but its orbit drifts away from the query's.",
        "",
        "Under the counting rule, a network result counts only if it beats both of these "
        "comparison points on the same scorer. The physics-residual columns are context "
        "only and never change E or a tier. The formula does not apply to the FEAS-09 "
        "probes, because those are standard records with no hierarchical split.",
        "",
        "## Tier counts",
        "",
        "| Rows | Tier 0 | Tier 1 | Tier 2 | Tier 3 | Not applicable |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    labels = (
        ("singles", "Formula, single panel"),
        ("family", "Formula, family panel"),
        ("validation", "Formula, validation panel"),
        ("train", "Formula, all 1812 training"),
    )
    for key, label in labels:
        counts = panel_counts[key]
        lines.append(
            f"| {label} | {counts['0']} | {counts['1']} | {counts['2']} | {counts['3']} "
            f"| {counts['not_applicable']} |"
        )
    copy_counts = baselines["nn_copy_tier_counts"]
    lines.append(
        f"| Copy, 227 validation | {copy_counts['0']} | {copy_counts['1']} | {copy_counts['2']} "
        f"| {copy_counts['3']} | {copy_counts['not_applicable']} |"
    )
    lines.extend([
        "",
        "## FEAS-09 probes",
        "",
        f"Stage 4b: {collected['feas09']['stage4b']}. Stage 6: {collected['feas09']['stage6']}.",
        "",
    ])
    return "\n".join(lines)


def _rendered_bytes(payloads):
    rendered = {}
    for name, payload in payloads.items():
        if name.endswith(".json"):
            rendered[name] = evidence_io.canonical_json_bytes(payload)
        else:
            rendered[name] = payload.encode("utf-8")
    return rendered


def _evidence_dir(args):
    if args.evidence_root:
        root = Path(args.evidence_root)
        if not root.is_absolute():
            root = Path.cwd() / root
    else:
        root = _REPO_ROOT / evidence_io.EVIDENCE_ROOT_REL
    return root / "baselines"


def _opened_zeros(attestation, directory):
    summary = attestation.summary()
    for key in ("test_split_opened", "blocked_attempts", "refused_before_open"):
        if summary.get(key) != 0:
            print(f"BASELINES-CHECK-DIFF: live {key} is {summary.get(key)}", file=sys.stderr)
            return False
    path = directory / "files_opened.json"
    if path.is_file():
        payload = json.loads(path.read_text(encoding="utf-8"))
        for key in ("test_split_opened", "blocked_attempts", "refused_before_open"):
            if payload.get(key) != 0:
                print(f"BASELINES-CHECK-DIFF: files_opened {key}", file=sys.stderr)
                return False
    return True


def _full_mode(args, *, check, started_wall, started):
    collected = collect(args)
    payloads = build_payloads(collected)
    rendered = _rendered_bytes(payloads)
    directory = _evidence_dir(args)
    if check:
        same = True
        for name, raw in rendered.items():
            if not evidence_io.bytes_identical(directory / name, raw):
                print(f"BASELINES-CHECK-DIFF: {name}", file=sys.stderr)
                same = False
        same = _opened_zeros(collected["attestation"], directory) and same
        if not same:
            return 1
        print("BASELINES-CHECK-OK")
        return 0
    data_root = collected["data_root"]
    for name, payload in payloads.items():
        if name.endswith(".json"):
            evidence_io.write_json(directory / name, payload, data_root=data_root)
        else:
            evidence_io.write_text(directory / name, payload, data_root=data_root)
    evidence_io.write_json(
        directory / "files_opened.json",
        evidence_io.files_opened_record("baselines", collected["attestation"].summary()),
        data_root=data_root,
    )
    evidence_io.write_json(
        directory / "provenance.json",
        evidence_io.provenance_record(
            "baselines",
            sys.argv,
            data_root=data_root,
            data_root_source=collected["data_root_source"],
            utc_started=started_wall,
            monotonic_started=started,
        ),
        data_root=data_root,
    )
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
    return _full_mode(args, check=args.check, started_wall=started_wall, started=started)


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
    "candidate_pool",
    "feas09_record",
    "main",
    "score_copy",
    "score_formula",
    "with_residual_context",
]
