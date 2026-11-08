"""Phase 68: The Yardstick Audit runner.

Audits every judging metric and gate on Brutus's recorded trajectory and the
constant predictor across Stage-0 training panel systems (1632, 851, 4658).
Compares explicit-velocity FEAS-01 metrics against finite-difference energy
at the native 0.01 gold cadence and coarse 0.08 base cadence, as well as
same-sample float32 input precision sensitivity.

Read-only CLI:
- Default: run audit over fixed panel, print canonical JSON to stdout.
- ``--check PATH``: replay saved audit and verify reproducibility.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import subprocess
import sys
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from types import SimpleNamespace
from typing import Any, Mapping, Optional, Sequence

import numpy as np
import torch

from pinn.constants import T_CHARACTERISTIC_TIME
from pinn.data.adapter import dt_out_disagreement_warns, measure_dt_out
from pinn.data.types import RecordKey
from pinn.training.validation_gate import (
    RATIFIED_VALIDATION_FRAME,
    gate_time_coordinate,
    json_safe_float,
)
from pinn.verification import evidence_io, gate_metrics
from pinn.verification.diagnostic_data import (
    Stage0TrainingReader,
    Stage0TrainingRefused,
    orbit_stage,
    physical_window,
    require_stage0_training,
)
from pinn.verification.evidence_io import (
    FreezeNotEstablished,
    canonical_json_bytes,
    files_opened_record,
    is_ancestor,
    module_hashes,
    provenance_record,
    require_frozen_scorecard,
)
from pinn.verification.feasibility_scorecard import (
    SCORECARD_SHA256,
    load_scorecard,
)
from pinn.verification.feasibility_scorer import (
    ScoreResult,
    score_trajectory,
)
from pinn.verification.gate_metrics import (
    EPS_INV,
    aggregate_gate_verdict,
    finite_difference_velocity,
    gate_verdict,
    matched_plummer_hamiltonian_series,
    scs_from_eps_h,
    trajectory_eps_h,
)
from pinn.verification.production_reference import load_reference
from pinn.verification.split_allowlist import (
    GENERATION7_SPLITS_REL,
    SplitAllowlist,
    SplitRefused,
    expected_splits_sha256,
    install_open_attestation,
    resolve_data_root,
)
from pinn.verification.stage0_census import gold_base_agreement

__all__ = [
    "SCHEMA_VERSION",
    "FIXED_PANEL_SYSTEM_IDS",
    "PANELS_JSON_REL",
    "PRODUCER_MODULES",
    "YardstickAuditError",
    "array_digest",
    "compute_fd_metrics",
    "compute_fd_metrics_float32_input",
    "audit_pair",
    "run_fixed_panel_audit",
    "replay_check",
    "main",
]

SCHEMA_VERSION = "phase68-yardstick-audit/v1"
FIXED_PANEL_SYSTEM_IDS = (1632, 851, 4658)
PANELS_JSON_REL = Path(
    ".planning/phases/59-read-only-baseline-scorecard/evidence/census/panels.json"
)

PRODUCER_MODULES = (
    "pinn/verification/yardstick_audit.py",
    "pinn/verification/evidence_io.py",
    "pinn/verification/feasibility_scorecard.py",
    "pinn/verification/feasibility_scorer.py",
    "pinn/verification/gate_metrics.py",
    "pinn/training/validation_gate.py",
    "pinn/verification/split_allowlist.py",
    "pinn/verification/diagnostic_data.py",
    "pinn/verification/production_reference.py",
    "pinn/verification/stage0_census.py",
)

_CENSUS_COUNTS = {
    1632: {"gold": 1001, "base": 126},
    851: {"gold": 1001, "base": 126},
    4658: {"gold": 1001, "base": 126},
}


class YardstickAuditError(RuntimeError):
    """Raised when yardstick audit invariants fail."""


def _repo_root(repo_root: Optional[Path] = None) -> Path:
    if repo_root is not None:
        return Path(repo_root).resolve()
    return Path(__file__).resolve().parents[2]


def array_digest(arr: np.ndarray) -> dict[str, Any]:
    """Compute sha256 digest and shape for a numpy array in little-endian float64."""
    a = np.ascontiguousarray(np.asarray(arr, dtype="<f8"))
    digest = hashlib.sha256(a.tobytes()).hexdigest()
    return {
        "sha256": digest,
        "shape": list(a.shape),
        "dtype": "<f8",
    }


def compute_fd_metrics(positions, times, masses, *, eps_inv: float = EPS_INV) -> dict[str, Any]:
    """Compute FD gate metrics and Hamiltonian series diagnostics for one trajectory.

    Args:
        positions: (N_t, 3, 3) positions.
        times: (N_t,) strictly increasing native snapshot times.
        masses: (3,) ordered raw masses.
        eps_inv: Plummer softening parameter.

    Returns:
        Dictionary with eps_h, scs, verdict, h0, last_h, peak_abs_change, peak_time,
        peak_location, and peak_index.
    """
    u = gate_time_coordinate(times, RATIFIED_VALIDATION_FRAME)
    v_fd = finite_difference_velocity(positions, u)
    h_series = matched_plummer_hamiltonian_series(positions, v_fd, masses, eps_inv=eps_inv)
    eps_h = float(trajectory_eps_h(h_series))
    scs = scs_from_eps_h(eps_h)
    verdict = gate_verdict(eps_h)

    h_cpu = h_series.detach().cpu().numpy()
    h0 = float(h_cpu[0])
    last_h = float(h_cpu[-1])
    diff_h = np.abs(h_cpu - h0)
    peak_idx = int(np.argmax(diff_h))
    peak_abs_change = float(diff_h[peak_idx])
    time_arr = np.asarray(times, dtype=np.float64)
    peak_time = float(time_arr[peak_idx])

    n_samples = len(time_arr)
    if peak_idx in (0, n_samples - 1):
        peak_loc = "endpoint"
    else:
        peak_loc = "interior"

    return {
        "eps_h": json_safe_float(eps_h),
        "scs": json_safe_float(scs),
        "verdict": str(verdict),
        "h0": json_safe_float(h0),
        "last_h": json_safe_float(last_h),
        "peak_abs_change": json_safe_float(peak_abs_change),
        "peak_time": json_safe_float(peak_time),
        "peak_location": peak_loc,
        "peak_index": peak_idx,
    }


def compute_fd_metrics_float32_input(
    positions, times, masses, *, eps_inv: float = EPS_INV
) -> dict[str, Any]:
    """Compute FD gate metrics with positions, times, and masses rounded to float32 before the shared calculation."""
    pos_f32 = np.asarray(positions, dtype=np.float32).astype(np.float64)
    times_f32 = np.asarray(times, dtype=np.float32).astype(np.float64)
    masses_f32 = np.asarray(masses, dtype=np.float32).astype(np.float64)
    return compute_fd_metrics(pos_f32, times_f32, masses_f32, eps_inv=eps_inv)


def audit_pair(reader: Stage0TrainingReader, base_key: RecordKey, gold_key: RecordKey, *, scorecard: Any) -> dict[str, Any]:
    """Audit one hierarchical system pair (base and gold records).

    Reuses Stage0TrainingReader and pre-open admission. Verifies matching physical identity,
    slices to physical_window t_max, verifies gold_base_agreement, and scores both
    predictions ('brutus' and 'window_mean_constant') on both grids.

    Returns:
        dict with 'record_info' and 'rows' (4 rows).
    """
    if not isinstance(base_key, RecordKey) or not isinstance(gold_key, RecordKey):
        raise TypeError(f"keys must be RecordKey; got {base_key!r}, {gold_key!r}")

    # Explicit admission check before any read
    base_admit = require_stage0_training(reader.allowlist, base_key)
    gold_admit = require_stage0_training(reader.allowlist, gold_key)

    base_ref = load_reference(reader, base_key)
    gold_ref = load_reference(reader, gold_key)

    # Verify identical physical identity
    if base_ref.record_key.physical_key != gold_ref.record_key.physical_key:
        raise YardstickAuditError(
            f"physical key mismatch: {base_ref.record_key.physical_key} != {gold_ref.record_key.physical_key}"
        )
    if not np.array_equal(base_ref.masses, gold_ref.masses):
        raise YardstickAuditError("masses mismatch between base and gold")
    if not np.array_equal(base_ref.permutation, gold_ref.permutation):
        raise YardstickAuditError("permutation mismatch between base and gold")
    if tuple(base_ref.inner_pair) != tuple(gold_ref.inner_pair):
        raise YardstickAuditError("inner_pair mismatch between base and gold")

    t_max = float(scorecard.section("scoring_grid")["t_max"])
    base_mask = physical_window(base_ref.times, t_max)
    gold_mask = physical_window(gold_ref.times, t_max)

    base_times = np.asarray(base_ref.times, dtype=np.float64)[base_mask]
    base_positions = np.asarray(base_ref.positions, dtype=np.float64)[base_mask]
    base_velocities = np.asarray(base_ref.velocities, dtype=np.float64)[base_mask]

    gold_times = np.asarray(gold_ref.times, dtype=np.float64)[gold_mask]
    gold_positions = np.asarray(gold_ref.positions, dtype=np.float64)[gold_mask]
    gold_velocities = np.asarray(gold_ref.velocities, dtype=np.float64)[gold_mask]

    if len(base_times) < 2 or len(gold_times) < 2:
        raise YardstickAuditError("both base and gold must have >= 2 window samples")
    if not np.all(base_times[1:] > base_times[:-1]):
        raise YardstickAuditError("base times must be strictly increasing")
    if not np.all(gold_times[1:] > gold_times[:-1]):
        raise YardstickAuditError("gold times must be strictly increasing")

    # Check gold_base_agreement on windowed positions
    sliced_base = SimpleNamespace(times=base_times, positions=base_positions)
    sliced_gold = SimpleNamespace(times=gold_times, positions=gold_positions)
    agreement_dev = gold_base_agreement(sliced_base, sliced_gold)
    agreement_tol = float(scorecard.section("scoring_grid")["gold_base_agreement_max"])
    agreement_passed = bool(agreement_dev <= agreement_tol)
    if not agreement_passed:
        raise YardstickAuditError(
            f"gold_base_agreement failed: deviation {agreement_dev} > tolerance {agreement_tol}"
        )

    base_dt_measured = measure_dt_out(base_times)
    gold_dt_measured = measure_dt_out(gold_times)
    base_dt_expected = float(scorecard.section("scoring_grid")["base_dt"])
    gold_dt_expected = float(scorecard.section("scoring_grid")["gold_dt"])
    base_dt_warn = bool(dt_out_disagreement_warns(base_dt_measured, base_dt_expected))
    gold_dt_warn = bool(dt_out_disagreement_warns(gold_dt_measured, gold_dt_expected))

    base_intervals = np.diff(base_times)
    gold_intervals = np.diff(gold_times)

    system_id = int(base_ref.record_key.id)
    masses = np.asarray(base_ref.masses, dtype=np.float64)
    inner_pair = tuple(int(s) for s in base_ref.inner_pair)

    record_info = {
        "system_id": system_id,
        "variant": str(base_ref.record_key.variant),
        "split": str(base_ref.split),
        "physical_stage": int(base_admit["stage"]),
        "record_stage_base": base_admit["record_stage"],
        "record_stage_gold": gold_admit["record_stage"],
        "window": {"t_min": 0.0, "t_max": t_max},
        "D": float(base_ref.D),
        "T": float(base_ref.T),
        "ordered_masses": [float(m) for m in masses],
        "permutation": [int(p) for p in base_ref.permutation],
        "inner_pair": list(inner_pair),
        "gold_base_agreement": {
            "deviation": json_safe_float(agreement_dev),
            "tolerance": json_safe_float(agreement_tol),
            "passed": agreement_passed,
        },
        "base_grid": {
            "n_snapshots": int(len(base_times)),
            "dt_out_measured": json_safe_float(base_dt_measured),
            "dt_out_expected": json_safe_float(base_dt_expected),
            "dt_out_disagreement_warns": base_dt_warn,
            "interval_min": json_safe_float(float(np.min(base_intervals))),
            "interval_max": json_safe_float(float(np.max(base_intervals))),
            "digests": {
                "times": array_digest(base_times),
                "positions": array_digest(base_positions),
                "velocities": array_digest(base_velocities),
                "masses": array_digest(masses),
            },
        },
        "gold_grid": {
            "n_snapshots": int(len(gold_times)),
            "dt_out_measured": json_safe_float(gold_dt_measured),
            "dt_out_expected": json_safe_float(gold_dt_expected),
            "dt_out_disagreement_warns": gold_dt_warn,
            "interval_min": json_safe_float(float(np.min(gold_intervals))),
            "interval_max": json_safe_float(float(np.max(gold_intervals))),
            "digests": {
                "times": array_digest(gold_times),
                "positions": array_digest(gold_positions),
                "velocities": array_digest(gold_velocities),
                "masses": array_digest(masses),
            },
        },
    }

    rows = []
    # Canonical grid and prediction order: base (brutus, constant), then gold (brutus, constant)
    for grid_name, (times, positions, velocities, rec_key) in [
        ("base", (base_times, base_positions, base_velocities, base_key)),
        ("gold", (gold_times, gold_positions, gold_velocities, gold_key)),
    ]:
        for pred_kind in ("brutus", "window_mean_constant"):
            if pred_kind == "brutus":
                pred_pos = positions
                pred_vel = velocities
                vel_src = "brutus"
            else:
                pred_pos = np.broadcast_to(
                    positions.mean(axis=0, keepdims=True), positions.shape
                ).copy()
                pred_vel = np.zeros_like(pred_pos)
                vel_src = "analytic"

            score = score_trajectory(
                pred_pos,
                pred_vel,
                positions,
                masses,
                inner_pair,
                times,
                velocity_source=vel_src,
                scorecard=scorecard,
                grid=grid_name,
            )

            gate_native = compute_fd_metrics(pred_pos, times, masses)
            gate_f32 = compute_fd_metrics_float32_input(pred_pos, times, masses)

            rows.append({
                "record_key": evidence_io.record_key_str(rec_key),
                "system_id": system_id,
                "grid": grid_name,
                "prediction": pred_kind,
                "feas01": score.to_json_dict(),
                "gate_fd_native": gate_native,
                "gate_fd_float32_input": gate_f32,
            })

    return {
        "record_info": record_info,
        "rows": rows,
    }


def run_fixed_panel_audit(repo_root: Optional[Path] = None, *, argv: Optional[Sequence[str]] = None) -> dict[str, Any]:
    """Execute the complete fixed-panel audit over systems 1632, 851, 4658."""
    utc_started = datetime.now(timezone.utc).isoformat()
    mono_started = time.monotonic()
    repo = _repo_root(repo_root)

    # 1. Scorecard freeze check
    freeze_info = require_frozen_scorecard(repo)
    scorecard = load_scorecard()

    # 2. Split allowlist and manifest check
    splits_path = repo / GENERATION7_SPLITS_REL
    splits_expected_sha = expected_splits_sha256(repo)
    allowlist = SplitAllowlist.from_manifest(splits_path, expected_sha256=splits_expected_sha)

    # 3. Panels singles check
    panels_path = repo / PANELS_JSON_REL
    if not panels_path.is_file():
        raise YardstickAuditError(f"panels file missing: {panels_path}")
    panels_raw = panels_path.read_bytes()
    panels_sha256 = hashlib.sha256(panels_raw).hexdigest()
    panels_data = json.loads(panels_raw.decode("utf-8"))
    singles_ids = tuple(int(entry["id"]) for entry in panels_data.get("singles", []))
    if singles_ids != FIXED_PANEL_SYSTEM_IDS:
        raise YardstickAuditError(
            f"panels.json singles {singles_ids} != expected {FIXED_PANEL_SYSTEM_IDS}"
        )

    # 4. Construct all 6 keys and check admission before any corpus path
    keys_to_audit = []
    for sys_id in FIXED_PANEL_SYSTEM_IDS:
        b_key = RecordKey("hierarchical", "base", sys_id)
        g_key = RecordKey("hierarchical", "gold", sys_id)
        require_stage0_training(allowlist, b_key)
        require_stage0_training(allowlist, g_key)
        keys_to_audit.append((sys_id, b_key, g_key))

    # 5. Set up open attestation and Stage0TrainingReader
    data_root, data_root_source = resolve_data_root(None)
    attestation = install_open_attestation(
        data_root=data_root,
        data_root_source=data_root_source,
        withheld_basenames=allowlist.withheld_basenames(),
        split_by_basename=allowlist.split_by_basename(),
    )
    reader = Stage0TrainingReader(
        allowlist=allowlist,
        data_root=data_root,
        data_root_source=data_root_source,
    )

    all_records = {}
    all_rows = []
    problems = []

    # 6. Execute audit for each pair
    for sys_id, b_key, g_key in keys_to_audit:
        pair_result = audit_pair(reader, b_key, g_key, scorecard=scorecard)
        rec_info = pair_result["record_info"]

        # Verify sample counts against census expectations
        exp_counts = _CENSUS_COUNTS.get(sys_id, {})
        if exp_counts:
            base_cnt = rec_info["base_grid"]["n_snapshots"]
            gold_cnt = rec_info["gold_grid"]["n_snapshots"]
            if base_cnt != exp_counts["base"]:
                problems.append(
                    f"system {sys_id} base count {base_cnt} != census {exp_counts['base']}"
                )
            if gold_cnt != exp_counts["gold"]:
                problems.append(
                    f"system {sys_id} gold count {gold_cnt} != census {exp_counts['gold']}"
                )

        all_records[str(sys_id)] = rec_info
        all_rows.extend(pair_result["rows"])

    # Verify access: each admitted key opened exactly once, 6 opens, 0 refusals
    access_summary = reader.access_summary()
    if access_summary["actual_opens"] != 6:
        raise YardstickAuditError(
            f"expected exactly 6 opens, got {access_summary['actual_opens']}"
        )
    if access_summary["refused_before_open"] != 0:
        raise YardstickAuditError(
            f"expected 0 refusals during fixed panel audit, got {access_summary['refused_before_open']}"
        )

    # 7. Aggregate the 8 gate aggregates
    # Combinations: grid in (base, gold) x pred in (brutus, constant) x precision in (native_float64, float32_input)
    aggregates = []
    for grid in ("base", "gold"):
        for pred in ("brutus", "window_mean_constant"):
            for prec in ("native_float64", "float32_input"):
                matching_rows = [
                    r for r in all_rows if r["grid"] == grid and r["prediction"] == pred
                ]
                if len(matching_rows) != len(FIXED_PANEL_SYSTEM_IDS):
                    raise YardstickAuditError(
                        f"expected {len(FIXED_PANEL_SYSTEM_IDS)} rows for {grid}/{pred}, got {len(matching_rows)}"
                    )

                if prec == "native_float64":
                    per_sys_eps = [
                        float(r["gate_fd_native"]["eps_h"]) for r in matching_rows
                    ]
                else:
                    per_sys_eps = [
                        float(r["gate_fd_float32_input"]["eps_h"]) for r in matching_rows
                    ]

                agg = aggregate_gate_verdict(per_sys_eps)
                aggregates.append({
                    "grid": grid,
                    "prediction": pred,
                    "fd_precision": prec,
                    "eps_h": json_safe_float(agg.eps_h),
                    "scs": json_safe_float(agg.scs),
                    "verdict": agg.verdict,
                    "system_ids": list(FIXED_PANEL_SYSTEM_IDS),
                    "per_system_eps_h": [json_safe_float(val) for val in per_sys_eps],
                })

    # 8. Provenance and source hashes
    prod_hashes = module_hashes(PRODUCER_MODULES, repo_root=repo)
    files_opened = files_opened_record("yardstick_audit", attestation.summary())
    provenance = provenance_record(
        "yardstick_audit",
        argv or sys.argv,
        data_root=data_root,
        data_root_source=data_root_source,
        utc_started=utc_started,
        monotonic_started=mono_started,
    )

    payload = {
        "schema": SCHEMA_VERSION,
        "coverage": {
            "complete": (len(problems) == 0 and len(all_rows) == 12 and len(aggregates) == 8),
            "expected_keys": 6,
            "actual_opens": access_summary["actual_opens"],
            "expected_rows": 12,
            "retained_rows": len(all_rows),
            "expected_aggregates": 8,
            "retained_aggregates": len(aggregates),
            "systems": list(FIXED_PANEL_SYSTEM_IDS),
            "grids": ["base", "gold"],
            "predictions": ["brutus", "window_mean_constant"],
        },
        "sources": {
            "scorecard_sha256": SCORECARD_SHA256,
            "scorecard_freeze_commit": freeze_info["freeze_commit"],
            "splits_manifest_sha256": allowlist.manifest_sha256,
            "panels_json_sha256": panels_sha256,
            "producer_sha256": prod_hashes,
        },
        "provenance": provenance,
        "reader_access": access_summary,
        "files_opened": files_opened,
        "records": all_records,
        "rows": all_rows,
        "aggregates": aggregates,
        "problems": problems,
    }

    return payload


def replay_check(check_path: Path, repo_root: Optional[Path] = None) -> bool:
    """Replay saved audit JSON and verify full reproducibility."""
    repo = _repo_root(repo_root)
    file_path = Path(check_path)
    if not file_path.is_file():
        raise YardstickAuditError(f"check path does not exist: {file_path}")

    raw = file_path.read_bytes()
    try:
        saved = json.loads(raw.decode("utf-8"))
    except Exception as exc:
        raise YardstickAuditError(f"failed to parse JSON from {file_path}: {exc}") from exc

    if saved.get("schema") != SCHEMA_VERSION:
        raise YardstickAuditError(
            f"schema mismatch in {file_path}: {saved.get('schema')} != {SCHEMA_VERSION}"
        )

    # Verify capture commit is in git history
    saved_prov = saved.get("provenance", {})
    capture_commit = saved_prov.get("git_head")
    if not capture_commit:
        raise YardstickAuditError("saved provenance missing git_head")
    rev_proc = subprocess.run(
        ["git", "rev-parse", "--verify", f"{capture_commit}^{{commit}}"],
        cwd=str(repo),
        capture_output=True,
        text=True,
        check=False,
    )
    if rev_proc.returncode != 0:
        raise YardstickAuditError(f"capture commit {capture_commit} is not in repository history")

    # Check live producer bytes against recorded producer hashes
    saved_sources = saved.get("sources", {})
    saved_producers = saved_sources.get("producer_sha256", {})
    live_producers = module_hashes(PRODUCER_MODULES, repo_root=repo)
    for mod, exp_sha in saved_producers.items():
        if live_producers.get(mod) != exp_sha:
            raise YardstickAuditError(
                f"live producer hash for {mod} ({live_producers.get(mod)}) != recorded {exp_sha}"
            )

    # Fresh computation
    fresh = run_fixed_panel_audit(repo, argv=["pinn.verification.yardstick_audit", "--check", str(file_path)])

    # Compare stable fields
    stable_fields = ("schema", "coverage", "sources", "reader_access", "records", "rows", "aggregates", "problems")
    for field in stable_fields:
        saved_val = saved.get(field)
        fresh_val = fresh.get(field)
        saved_bytes = canonical_json_bytes(saved_val)
        fresh_bytes = canonical_json_bytes(fresh_val)
        if saved_bytes != fresh_bytes:
            raise YardstickAuditError(
                f"replay discrepancy in field {field!r}:\nSAVED: {saved_val}\nFRESH: {fresh_val}"
            )

    return True


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        prog="yardstick_audit",
        description="Phase 68 yardstick known-answer audit runner and replay checker.",
    )
    parser.add_argument(
        "--check",
        metavar="PATH",
        type=Path,
        help="Replay a saved audit JSON and verify complete reproducibility.",
    )

    args = parser.parse_args(argv)

    try:
        if args.check:
            ok = replay_check(args.check)
            if ok:
                print("YARDSTICK-AUDIT-OK")
                return 0
            return 1
        else:
            payload = run_fixed_panel_audit(argv=argv)
            output_bytes = canonical_json_bytes(payload)
            sys.stdout.buffer.write(output_bytes)
            sys.stdout.buffer.write(b"\n")
            return 0
    except Exception as exc:
        sys.stderr.write(f"YARDSTICK-AUDIT-HALT: {exc}\n")
        return 2


if __name__ == "__main__":
    sys.exit(main())
