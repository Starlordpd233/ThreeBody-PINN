#!/usr/bin/env python3
"""DIAG-02: five-term loss decomposition across the smoke + three pilot runs.

Read-only forensic over train.log.jsonl for runs/stage0-{smoke,pilot-seed41,
pilot-seed42,pilot-seed43}. For every step it records RAW per-term values AND
their lambda-weighted contributions, locates+attributes each run's warmup spike
independently, and characterizes the PHYS-05 scheduled-weight interaction
(including the structural lambda_l == 0.0 fact). Deterministic, fail-closed.

Determinism: stdlib + numpy (pinn-train). No CLI args, no new deps, no generated
timestamps, cwd-independent (repo root from __file__). Non-finite floats are
serialized as explicit string tokens ("Infinity"/"NaN") so the JSON stays valid
and the artifact records exactly what the log carried.
"""
from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path

import numpy as np

LOSS_TERMS = ["loss_data", "loss_ic", "loss_phys", "loss_energy", "loss_angmom"]
LAMBDA_FOR = {
    "loss_data": "lambda_data",
    "loss_ic": "lambda_ic",
    "loss_phys": "lambda_phys",
    "loss_energy": "lambda_e",
    "loss_angmom": "lambda_l",
}
DIAG_KEYS = [
    "step", "epoch", "stage", "phase", "front_idx", "lr", "grad_norm", "total",
    "finite", "nonfinite_keys", "w_min", "w_mean", "w_max", "s_per_step",
    "eta_seconds", "step_completed",
]
REQUIRED_KEYS = LOSS_TERMS + list(LAMBDA_FOR.values()) + DIAG_KEYS  # 26 keys
RUNS = ["stage0-smoke", "stage0-pilot-seed41", "stage0-pilot-seed42", "stage0-pilot-seed43"]
EXPECTED_STEPS = set(range(1, 301))


def repo_root() -> Path:
    p = Path(__file__).resolve()
    while p != p.parent:
        if (p / ".planning").is_dir():
            return p
        p = p.parent
    raise SystemExit("DIAG-02 FAIL-CLOSED: could not locate repo root")


REPO = repo_root()
OUTPUT = Path(__file__).resolve().parent / "loss_decomposition.json"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def fail_closed(msg: str) -> None:
    raise SystemExit(f"DIAG-02 FAIL-CLOSED: {msg} (no output written)")


def safe(x):
    """Finite floats pass through at full precision; non-finite -> explicit token."""
    if isinstance(x, bool):
        return x
    if isinstance(x, (int, float)):
        f = float(x)
        if math.isnan(f):
            return "NaN"
        if math.isinf(f):
            return "Infinity" if f > 0 else "-Infinity"
        return f
    return x


def load_steps(run: str):
    path = REPO / "runs" / run / "logs" / "train.log.jsonl"
    if not path.is_file():
        fail_closed(f"input missing: {path}")
    recs = []
    with path.open("r") as fh:
        for ln, line in enumerate(fh, 1):
            line = line.strip()
            if not line:
                continue
            r = json.loads(line)
            if r.get("event") != "step":
                fail_closed(f"{run} line {ln} event={r.get('event')!r} != 'step'")
            recs.append(r)
    return path, recs


def analyze_run(run: str, path: Path, recs: list):
    # ---- fail-closed: required keys present (none imputed as zero) ----
    actual_keys = set(recs[0].keys())
    for i, r in enumerate(recs):
        missing = set(REQUIRED_KEYS) - set(r.keys())
        if missing:
            fail_closed(f"{run} step record {i} missing required keys {sorted(missing)}")
    steps = sorted((int(r["step"]) for r in recs))
    if set(steps) != EXPECTED_STEPS:
        fail_closed(f"{run} step set {sorted(set(steps))[:5]}...{sorted(set(steps))[-5:]} != {{1..300}}")

    recs_by_step = {int(r["step"]): r for r in recs}

    # lambda_l structural fact (asserted): angular-momentum weight is 0.0 everywhere
    lambda_l_vals = [float(r["lambda_l"]) for r in recs]
    lambda_l_all_zero = all(v == 0.0 for v in lambda_l_vals)
    if not lambda_l_all_zero:
        fail_closed(f"{run}: lambda_l not 0.0 at all 300 steps (structural assumption violated)")

    # lambda_phys first reaches 1.0 (derived from data)
    lambda_phys_first_ge1 = None
    for s in range(1, 301):
        if float(recs_by_step[s]["lambda_phys"]) >= 1.0:
            lambda_phys_first_ge1 = s
            break

    # non-finite summary
    nonfinite_steps = []
    for s in range(1, 301):
        r = recs_by_step[s]
        if not bool(r.get("finite", True)) or r.get("nonfinite_keys"):
            nonfinite_steps.append({
                "step": s,
                "finite": bool(r.get("finite")),
                "nonfinite_keys": list(r.get("nonfinite_keys") or []),
            })

    # per-step raw + weighted (ascending step)
    per_step = {}
    cum_raw = {t: 0.0 for t in LOSS_TERMS}
    cum_weighted = {t: 0.0 for t in LOSS_TERMS}
    for s in range(1, 301):
        r = recs_by_step[s]
        finite = bool(r.get("finite", True)) and not any(
            (isinstance(r[t], float) and not math.isfinite(r[t])) for t in LOSS_TERMS
        )
        raw = {t: safe(r[t]) for t in LOSS_TERMS}
        weighted = {t: safe(float(r[t]) * float(r[LAMBDA_FOR[t]])) for t in LOSS_TERMS}
        per_step[str(s)] = {"raw": raw, "weighted": weighted}
        if finite:
            for t in LOSS_TERMS:
                cum_raw[t] += float(r[t])
                cum_weighted[t] += float(r[t]) * float(r[LAMBDA_FOR[t]])

    # warmup spike: max total, earliest step on tie (first occurrence in ascending order)
    def total_key(r):
        t = r["total"]
        if isinstance(t, (int, float)) and not (isinstance(t, float) and math.isnan(t)):
            return float(t)
        return float("-inf")

    spike_step = min(range(1, 301), key=lambda s: (-total_key(recs_by_step[s]), s))
    # min of (-total, step) == max total, earliest step on tie
    sr = recs_by_step[spike_step]
    spike_raw = {t: float(sr[t]) for t in LOSS_TERMS}
    spike_total = total_key(sr)
    dominant_term = max(LOSS_TERMS, key=lambda t: spike_raw[t])
    dominant_raw = spike_raw[dominant_term]
    dominant_share = (dominant_raw / spike_total) if spike_total not in (0.0,) else None

    # dominance: cumulative raw vs cumulative weighted (finite steps only)
    dom_raw = max(LOSS_TERMS, key=lambda t: cum_raw[t])
    dom_weighted = max(LOSS_TERMS, key=lambda t: cum_weighted[t])

    return {
        "input_path": str(path.relative_to(REPO)),
        "input_sha256": sha256(path),
        "n_steps": len(recs),
        "step_set_is_1_to_300": (set(steps) == EXPECTED_STEPS),
        "required_keys_present": True,
        "required_keys_count": len(REQUIRED_KEYS),
        "actual_record_keys": sorted(actual_keys),
        "actual_record_key_count": len(actual_keys),
        "key_count_note": (
            "Plan 44-02 references '26 expected keys'; the artifact carries "
            f"{len(actual_keys)} (the extra is the 'event' discriminator). All 26 "
            "required keys are present; no loss term is imputed as zero."
        ),
        "records_processed_in_ascending_step_order": True,
        "nonfinite_summary": {
            "count": len(nonfinite_steps),
            "steps": nonfinite_steps,
        },
        "per_step": per_step,
        "warmup_spike": {
            "selection": "step with maximum 'total' loss; earliest step wins on tie (first occurrence in ascending step order)",
            "step": spike_step,
            "epoch": sr.get("epoch"),
            "phase": sr.get("phase"),
            "front_idx": sr.get("front_idx"),
            "total": safe(sr["total"]),
            "raw_terms": {t: safe(sr[t]) for t in LOSS_TERMS},
            "dominant_term": dominant_term,
            "dominant_raw": safe(dominant_raw),
            "dominant_share_of_total": safe(dominant_share) if dominant_share is not None else None,
            "grad_norm": safe(sr["grad_norm"]),
            "lr": safe(sr["lr"]),
            "finite": bool(sr.get("finite")),
            "nonfinite_keys": list(sr.get("nonfinite_keys") or []),
        },
        "phys05_interaction": {
            "lambda_phys_first_ge_1p0_step": lambda_phys_first_ge1,
            "lambda_l_all_zero_at_all_steps": lambda_l_all_zero,
            "lambda_l_note": "angular-momentum term (loss_angmom) never contributed gradient signal: lambda_l == 0.0 at every one of the 300 steps",
            "lambda_values_at_final_step": {t: safe(recs_by_step[300][LAMBDA_FOR[t]]) for t in LOSS_TERMS},
        },
        "dominance": {
            "by_cumulative_raw": dom_raw,
            "by_cumulative_weighted": dom_weighted,
            "raw_weighted_dominance_differ": (dom_raw != dom_weighted),
            "cumulative_raw": {t: cum_raw[t] for t in LOSS_TERMS},
            "cumulative_weighted": {t: cum_weighted[t] for t in LOSS_TERMS},
            "cumulative_note": "summed over finite steps only; non-finite steps excluded and listed in nonfinite_summary",
        },
        "tb_parsed": False,
        "tb_decision": "TensorBoard event files (tb/) were not parsed; every required DIAG-02 field is present in train.log.jsonl",
    }


def main() -> None:
    runs_out = {}
    inputs = []
    for run in RUNS:
        path, recs = load_steps(run)
        if not recs:
            fail_closed(f"{run}: no step records")
        runs_out[run] = analyze_run(run, path, recs)
        inputs.append({"path": str(path.relative_to(REPO)), "sha256": sha256(path)})

    out = {
        "schema": "diag02-loss-decomposition/v1",
        "generated_by": "evidence/diag02/loss_decomposition.py",
        "loss_terms": LOSS_TERMS,
        "lambda_mapping": LAMBDA_FOR,
        "runs": runs_out,
        "stage0_smoke_handling": (
            "stage0-smoke is reported as a SEPARATE fourth trace and is never pooled "
            "into seed statistics (D-10); it is a different run configuration, cited as such."
        ),
        "pooled_seed_statistics": None,
        "provenance": {"repo_relative": True, "inputs": inputs},
    }

    with OUTPUT.open("w") as fh:
        json.dump(out, fh, indent=2, sort_keys=True)
        fh.write("\n")
    print(f"wrote {OUTPUT.relative_to(REPO)} ({OUTPUT.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
