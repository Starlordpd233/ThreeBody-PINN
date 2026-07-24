#!/usr/bin/env python3
"""DIAG-03: three-seed band characterization (read-only).

Characterizes each pilot seed's validation trend (three-way direction,
first-vs-last per D-11), computes final-loss spreads using 43-CALIBRATION.md's
formulas verbatim, states AGREE/DISAGREE with the '2/3 seeds worsened' claim,
records the held-out-split divergence (splits.json SHA-256), and cites the
Phase 38 single-trajectory overfit rung verbatim as the machinery-integrity
control (never re-run, SCOPE-23/D-12). Deterministic, fail-closed.
"""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

PILOT_SEEDS = ["stage0-pilot-seed41", "stage0-pilot-seed42", "stage0-pilot-seed43"]
ALL_RUNS = ["stage0-smoke"] + PILOT_SEEDS
CAL_FILE = ".planning/milestones/v2.0-phases/43-verification-stage-0-pilot-acceptance/43-CALIBRATION.md"
VERIF38_FILE = ".planning/milestones/v2.0-phases/38-pinn-model-rebuild-from-specs-fut-01/38-VERIFICATION.md"


def repo_root() -> Path:
    p = Path(__file__).resolve()
    while p != p.parent:
        if (p / ".planning").is_dir():
            return p
        p = p.parent
    raise SystemExit("DIAG-03 FAIL-CLOSED: could not locate repo root")


REPO = repo_root()
OUTPUT = Path(__file__).resolve().parent / "seed_band.json"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def fail_closed(msg: str) -> None:
    raise SystemExit(f"DIAG-03 FAIL-CLOSED: {msg} (no output written)")


def load_validation(run: str):
    path = REPO / "runs" / run / "validation.jsonl"
    if not path.is_file():
        fail_closed(f"input missing: {path}")
    recs = []
    with path.open("r") as fh:
        for line in fh:
            line = line.strip()
            if line:
                recs.append(json.loads(line))
    if not recs:
        fail_closed(f"{run}: empty validation.jsonl")
    recs = sorted(recs, key=lambda r: int(r["step"]))
    return path, recs


def first_vs_last_direction(recs):
    first = recs[0]
    last = recs[-1]
    fv, lv = float(first["final_val_loss"]), float(last["final_val_loss"])
    if lv == fv:  # exact equality -> flat, never folded (D-11)
        direction = "flat"
    elif lv < fv:
        direction = "improving"
    else:
        direction = "worsening"
    return {
        "first_step": int(first["step"]),
        "first_val": fv,
        "last_step": int(last["step"]),
        "last_val": lv,
        "direction_first_vs_last": direction,
        "definition": "improving iff last<first, worsening iff last>first, flat iff exact equality (D-11)",
    }


def main() -> None:
    inputs = []

    # ---- per-seed validation trends ----
    per_seed = {}
    for run in PILOT_SEEDS:
        path, recs = load_validation(run)
        d = first_vs_last_direction(recs)
        d["records"] = recs
        d["artifact_last_window_trend"] = recs[-1].get("trend")  # the validation.jsonl field (step200->300)
        per_seed[run] = d
        inputs.append({"path": str(path.relative_to(REPO)), "sha256": sha256(path)})

    # smoke as the separate fourth trace (D-10): reported, never pooled
    smoke_path, smoke_recs = load_validation("stage0-smoke")
    smoke = first_vs_last_direction(smoke_recs)
    smoke["records"] = smoke_recs
    smoke["artifact_last_window_trend"] = smoke_recs[-1].get("trend")
    inputs.append({"path": str(smoke_path.relative_to(REPO)), "sha256": sha256(smoke_path)})

    # ---- spreads over pilot-seed FINAL (step300) final_val_loss (43-CAL formulas verbatim) ----
    finals = {run: float(per_seed[run]["last_val"]) for run in PILOT_SEEDS}
    vals = list(finals.values())
    mn, mx = min(vals), max(vals)
    svals = sorted(vals)
    median = svals[len(svals) // 2]  # 3 values -> middle
    if median == 0:
        fail_closed("median(seed final_val_loss) == 0; cannot compute relative span")
    absolute_span = mx - mn
    relative_span = (mx - mn) / median  # no rounding before calculation

    # cross-check against the value recorded in 43-CALIBRATION.md
    cal_path = REPO / CAL_FILE
    cal_text = cal_path.read_text()
    m = re.search(r"relative span is `([0-9.]+)`", cal_text)
    cal_rel_span = float(m.group(1)) if m else None
    cross_match = (cal_rel_span is not None) and abs(relative_span - cal_rel_span) <= 1e-9 * max(1.0, abs(relative_span))
    inputs.append({"path": CAL_FILE, "sha256": sha256(cal_path)})

    # ---- AGREE/DISAGREE with '2/3 seeds worsened' (D-11), from THIS script's first-vs-last directions ----
    worsened_fvl = [run for run in PILOT_SEEDS if per_seed[run]["direction_first_vs_last"] == "worsening"]
    worsened_lw = [run for run in PILOT_SEEDS if per_seed[run]["artifact_last_window_trend"] == "worsening"]
    claim_count = 2  # 43-CALIBRATION: "2/3 seeds worsened" (two final validation trends worsening)
    agree = (len(worsened_fvl) == claim_count)

    # ---- held-out split divergence (splits.json SHA-256) ----
    split_hashes = {}
    for run in ALL_RUNS:
        sp = REPO / "runs" / run / "splits.json"
        if not sp.is_file():
            fail_closed(f"input missing: {sp}")
        split_hashes[run] = sha256(sp)
        inputs.append({"path": str(sp.relative_to(REPO)), "sha256": split_hashes[run]})
    # group byte-identical
    groups = {}
    for run, h in split_hashes.items():
        groups.setdefault(h, []).append(run)
    identical_groups = sorted([sorted(g) for g in groups.values() if len(g) > 1])
    divergent = sorted([run for run in ALL_RUNS if len(groups[split_hashes[run]]) == 1])

    # ---- Phase 38 single-trajectory overfit rung: verbatim citation (D-12, SCOPE-23) ----
    v38_path = REPO / VERIF38_FILE
    v38_sha = sha256(v38_path)
    inputs.append({"path": VERIF38_FILE, "sha256": v38_sha})
    phase38_citation = {
        "flag": "CITATION-NOT-COMPUTATION (quoted verbatim from 38-VERIFICATION.md; never re-run, SCOPE-23/D-12)",
        "source_file": VERIF38_FILE,
        "source_sha256": v38_sha,
        "source_section": "Rung 4 - single-trajectory overfit (REAL admitted trajectory)",
        "evidence_path": "evidence/overfit/20260713T133619Z/",
        "verbatim": {
            "initial_data_loss_L0": 0.21921204799884003,
            "floor_Lf": 0.0001997174686303869,
            "ratio_L0_over_Lf": 1097.6107873895164,
            "threshold": "1e3",
            "verdict": "PASS",
            "steps_to_floor": 176,
            "optimizer": "Adam lr=1e-4 (early-broke from --max-steps 5000 cap)",
            "conditioning": "tau_ic13(u_n) = [2u_n-1, zeros(13)] (Phase-38 smoke placeholder; physically-normalized IC13 deferred to Phase 39)",
            "com_offset_warning": "none fired (offset << 1e-3 threshold)",
            "soft_energy_status": "not evaluated - requires Phase 39/40 metadata",
        },
        "caveats": [
            "single-trajectory overfit on ONE real admitted Brutus trajectory, not population scale",
            "IC13 slot is a fixed zeros(13) placeholder, NOT the Phase-39 physically-normalized IC13",
            "probe-local fixture loader is NOT the Phase 39 adapter (no Step-1A gate, no splits, no batching)",
            "different optimizer/training context (Adam lr=1e-4 overfit probe) vs the Stage-0 curriculum training",
        ],
        "interpretation_for_DIAG03": (
            "Establishes machinery integrity: the network CAN fit one trajectory (>=1e3x data-loss "
            "reduction), so the Stage-0 population-scale gate failure emerges at population scale / "
            "under the Stage-0 budget and recipe, not from a structurally broken network. Cited as the "
            "machinery-integrity control; not re-run here."
        ),
    }

    out = {
        "schema": "diag03-seed-band/v1",
        "generated_by": "evidence/diag03/seed_band.py",
        "pilot_seeds": PILOT_SEEDS,
        "separate_trace": "stage0-smoke (reported separately, never pooled into seed statistics; D-10)",
        "per_seed_trend": per_seed,
        "stage0_smoke_trace": smoke,
        "spreads_over_pilot_seeds_final_val_loss": {
            "formula_source": (
                "43-CALIBRATION.md 'Defined spread calculation' (verbatim): the absolute span is "
                "max(seed values) - min(seed values); the relative span is (max - min) / median(seed "
                "values); no values are rounded before the calculation."
            ),
            "seed_final_values": finals,
            "min": mn,
            "median": median,
            "max": mx,
            "absolute_span": absolute_span,
            "relative_span": relative_span,
            "median_nonzero_asserted": True,
            "cross_check_43_calibration": {
                "recorded_relative_span": cal_rel_span,
                "matches_within_1e-9_rel": cross_match,
            },
        },
        "calibration_agreement": {
            "claim": "43-CALIBRATION.md: '2/3 seeds worsened' (two final validation trends were worsening)",
            "direction_definition_used": "first-vs-last (step100 -> step300 final_val_loss), per D-11",
            "this_script_first_vs_last_worsened_count": len(worsened_fvl),
            "this_script_first_vs_last_worsened_seeds": worsened_fvl,
            "artifact_last_window_worsened_seeds": worsened_lw,
            "agree": agree,
            "verdict": "AGREE" if agree else "DISAGREE",
            "reason": (
                "This script's D-11 direction is first-vs-last (step100->step300): it counts the seeds "
                "whose final validation loss ENDED HIGHER than it started. 43-CALIBRATION's '2/3' uses "
                "the validation.jsonl `trend` field, which is the LAST-WINDOW (step200->300) direction. "
                "Under first-vs-last a seed can improve net over the whole run yet show a last-window "
                "worsening (or vice versa). Both counts are reported; the difference is the direction "
                "definition, not a data conflict. Neither definition is adjudicated here."
            ),
        },
        "held_out_split_divergence": {
            "method": "SHA-256 of runs/<run>/splits.json",
            "hashes": split_hashes,
            "byte_identical_groups": identical_groups,
            "divergent_runs": divergent,
            "caveat": (
                "seed41 and seed43 each carry a DIFFERENT held-out split from seed42 (and "
                "stage0-smoke == seed42). Cross-seed validation-MAGNITUDE comparisons therefore span "
                "DIFFERENT held-out populations and are not directly comparable; only WITHIN-seed "
                "trend direction is a clean longitudinal signal."
            ),
        },
        "phase38_overfit_rung_citation": phase38_citation,
        "provenance": {"repo_relative": True, "inputs": inputs},
    }

    with OUTPUT.open("w") as fh:
        json.dump(out, fh, indent=2, sort_keys=True)
        fh.write("\n")
    print(f"wrote {OUTPUT.relative_to(REPO)} ({OUTPUT.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
