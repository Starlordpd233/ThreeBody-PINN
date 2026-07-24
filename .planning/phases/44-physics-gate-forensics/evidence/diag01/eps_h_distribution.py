#!/usr/bin/env python3
"""DIAG-01: per-trajectory eps_h distribution from the preserved metrics.json.

Read-only forensic over runs/stage0-pilot-seed42/evaluation/metrics.json ONLY.
The evaluator is NOT invoked (SCOPE-22). Produces eps_h_distribution.json with
the full distribution, a pre-registered uniform-vs-tail criterion stated BEFORE
the verdict, by-variant / by-fidelity group breakdowns, and the D-07 observation
(max-vs-mean gate statistic) SURFACED, not decided.

Determinism: plain Python 3 stdlib + numpy (already installed in pinn-train).
No CLI args, no new deps, no generated timestamps, cwd-independent (repo root
resolved from __file__). sort_keys=True + full-repr floats -> byte-identical
JSON across re-runs at the same commit.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np


def repo_root() -> Path:
    p = Path(__file__).resolve()
    while p != p.parent:
        if (p / ".planning").is_dir():
            return p
        p = p.parent
    raise SystemExit("DIAG-01 FAIL-CLOSED: could not locate repo root (no .planning ancestor)")


REPO = repo_root()
INPUT = REPO / "runs" / "stage0-pilot-seed42" / "evaluation" / "metrics.json"
OUTPUT = Path(__file__).resolve().parent / "eps_h_distribution.json"

# Pre-registered gate semantics (constants in source -> cannot be post-hoc tuned).
EPS_H_REJECT_THRESHOLD = 1e-5
COMPARISON_OPERATOR = ">"  # strict greater-than matching gate semantics
REQUIRED_ENTRY_KEYS = {"eps_h", "fidelity", "id", "variant"}
PERCENTILES = [25, 50, 75, 90, 99]


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def fail_closed(msg: str) -> None:
    raise SystemExit(f"DIAG-01 FAIL-CLOSED: {msg} (no output written)")


def group_stats(values):
    arr = np.sort(np.asarray(values, dtype=float))
    pct = np.percentile(arr, PERCENTILES)  # default interpolation = 'linear'
    n = int(arr.size)
    n_exc = int(np.count_nonzero(arr > EPS_H_REJECT_THRESHOLD))
    return {
        "n": n,
        "min": float(arr[0]),
        "p25": float(pct[0]),
        "p50": float(pct[1]),
        "p75": float(pct[2]),
        "p90": float(pct[3]),
        "p99": float(pct[4]),
        "max": float(arr[-1]),
        "mean": float(arr.mean()),
        "median": float(pct[1]),
        "comparison_operator": COMPARISON_OPERATOR,
        "threshold": EPS_H_REJECT_THRESHOLD,
        "n_exceeding_threshold": n_exc,
        "frac_exceeding_threshold": (n_exc / n) if n else 0.0,
    }


def separates(bucket):
    """Flag a >=10x median gap between groups as a separating attribute (D-06)."""
    meds = [v["median"] for v in bucket.values()]
    if len(meds) < 2:
        return False, None
    lo, hi = min(meds), max(meds)
    sep = (lo > 0.0) and (hi > 0.0) and ((hi / lo) >= 10.0)
    return sep, (lo, hi)


def main() -> None:
    if not INPUT.is_file():
        fail_closed(f"input missing: {INPUT}")
    with INPUT.open("r") as fh:
        m = json.load(fh)

    per_traj = m.get("per_trajectory")
    if not isinstance(per_traj, list):
        fail_closed("per_trajectory is not a list")

    # ---- fail-closed assertions: write NOTHING on any failure ----
    if len(per_traj) != 1500:
        fail_closed(f"len(per_trajectory)={len(per_traj)} != 1500")
    for i, e in enumerate(per_traj):
        if set(e.keys()) != REQUIRED_ENTRY_KEYS:
            fail_closed(f"entry {i} keys {sorted(e.keys())} != {sorted(REQUIRED_ENTRY_KEYS)}")

    eps = [float(e["eps_h"]) for e in per_traj]
    top_level_eps_h = float(m["eps_h"])
    if max(eps) != top_level_eps_h:  # EXACT float equality, no tolerance
        fail_closed(f"max(per-traj eps_h)={max(eps)} != top-level eps_h={top_level_eps_h}")

    eps_sorted = sorted(eps)  # ascending before statistics (D-04/D-06)
    overall = group_stats(eps_sorted)
    assert overall["n"] == 1500

    # ---- by_variant / by_fidelity (D-06): only attributes present in artifact ----
    by_variant, by_fidelity = {}, {}
    for key, bucket in (("variant", by_variant), ("fidelity", by_fidelity)):
        groups: dict[str, list[float]] = {}
        for e in per_traj:
            groups.setdefault(e[key], []).append(float(e["eps_h"]))
        for gname, gvals in sorted(groups.items()):
            bucket[gname] = group_stats(sorted(gvals))

    var_sep, var_range = separates(by_variant)
    fid_sep, fid_range = separates(by_fidelity)

    # ---- pre-registered uniform-vs-tail criterion (D-05) ----
    pre_registered = {
        "name": "uniform-vs-tail",
        "comparison_operator": COMPARISON_OPERATOR,
        "threshold": EPS_H_REJECT_THRESHOLD,
        "rule": (
            "failure is UNIFORM iff min(per_trajectory.eps_h) > threshold "
            "(strict greater-than, matching gate semantics; a value exactly equal "
            "to the threshold does NOT count as exceeding)"
        ),
        "stated_before_verdict": True,
    }
    uniform_failure = bool(overall["min"] > EPS_H_REJECT_THRESHOLD)
    median = overall["median"] if overall["median"] else 1.0
    tail_structure = {
        "max_over_median": overall["max"] / median,
        "p99_over_median": overall["p99"] / median,
        "note": "magnitude spread reported separately from the uniform/tail verdict",
    }

    # ---- D-07: surfaced, NOT decided ----
    d07 = {
        "top_level_eps_h": top_level_eps_h,
        "max_per_trajectory_eps_h": float(max(eps)),
        "mean_per_trajectory_eps_h": overall["mean"],
        "median_per_trajectory_eps_h": overall["median"],
        "exact_equality_max_vs_top_level": (max(eps) == top_level_eps_h),
        "gap": "GAP-44-01",
        "note": (
            "The reported gate value (eps_h=237.2086...) is EXACTLY the MAX per-trajectory "
            "eps_h, not the mean (5.6222...) nor median (2.2327...). Whether a worst-case max "
            "is the SPEC-INTENDED gate statistic is a source-silent semantics question "
            "(GAP-44-01) and is NOT decided here."
        ),
    }

    worst = max(per_traj, key=lambda e: e["eps_h"])
    in_sha = sha256(INPUT)

    out = {
        "schema": "diag01-eps-h-distribution/v1",
        "generated_by": "evidence/diag01/eps_h_distribution.py",
        "percentile_interpolation": "linear",
        "input": {
            "path": str(INPUT.relative_to(REPO)),
            "sha256": in_sha,
            "schema_version": m.get("schema_version"),
            "artifact_top_level": {
                "eps_h": top_level_eps_h,
                "scs": float(m["scs"]),
                "n_test_trajectories": int(m["n_test_trajectories"]),
                "eps_h_reject_threshold": float(m["eps_h_reject_threshold"]),
                "scs_reject_threshold": float(m["scs_reject_threshold"]),
                "verdict": m["verdict"],
            },
        },
        "pre_registered_criterion": pre_registered,
        "overall": overall,
        "tail_structure": tail_structure,
        "by_variant": by_variant,
        "by_fidelity": by_fidelity,
        "attribute_separation": {
            "method": ">=10x median gap between groups flagged as separating",
            "variant": {"separates_population": var_sep, "median_range": var_range},
            "fidelity": {"separates_population": fid_sep, "median_range": fid_range},
        },
        "verdict": {
            "uniform_failure": uniform_failure,
            "statement": (
                "UNIFORM failure: the minimum per-trajectory eps_h exceeds the 1e-5 reject "
                "threshold (strict >), so 100% of held-out trajectories fail; a heavy right "
                "tail is reported separately in tail_structure."
                if uniform_failure
                else "TAIL-driven failure: min per-trajectory eps_h is at/below threshold."
            ),
        },
        "worst_trajectory": {
            "id": worst["id"],
            "variant": worst["variant"],
            "fidelity": worst["fidelity"],
            "eps_h": float(worst["eps_h"]),
        },
        "d07_observation": d07,
        "provenance": {
            "repo_relative": True,
            "inputs": [{"path": str(INPUT.relative_to(REPO)), "sha256": in_sha}],
        },
    }

    with OUTPUT.open("w") as fh:
        json.dump(out, fh, indent=2, sort_keys=True)
        fh.write("\n")
    print(f"wrote {OUTPUT.relative_to(REPO)} ({OUTPUT.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
