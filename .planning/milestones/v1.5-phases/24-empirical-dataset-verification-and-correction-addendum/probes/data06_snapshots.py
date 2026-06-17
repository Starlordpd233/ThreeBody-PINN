# probes/data06_snapshots.py — DATA-06 snapshot-count + final-timestep distribution probe (CLM-10, CLM-11)
# D-02 re-derivability header: run from repo root.
#   .venv/bin/python .planning/phases/24-empirical-dataset-verification-and-correction-addendum/probes/data06_snapshots.py
# Reads (read-only): simulation_data/Data/brutus_output/{4 variants}
# Records: per-variant snapshot-count distribution (min/median/mode/max + modal counts) and
#          final_timestep>=9.5 prevalence fraction.
#
# D-09: distributions, not single examples. CLM-10 judged at MEDIAN with integer rounding
#       (locked 2026-06-11; commit 71e4d6e9). Mode and pilot central value are EVIDENCE ONLY.
# D-11: contradictions with Documentation/README recorded + README correction PROPOSED for sign-off.
# A1: block-delimiting assumption; gold files may differ.

import os
import re
import json
import datetime
import statistics
from collections import Counter

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))
DATA_BASE = os.path.join(REPO_ROOT, "simulation_data", "Data", "brutus_output")

FOLDERS = [
    "brutus_standard_quasi_random",
    "brutus_standard_quasi_random_gold_standard",
    "brutus_hierarchical",
    "brutus_hierarchical_gold_standard",
]

ID_RE = re.compile(r"^brutus_(?:standard|hierarchical)_(\d{4})\.txt$")

# CLM-10 claims (from RESEARCH-CONTEXT-MASTER.md; D-09 median-locked 2026-06-11).
CLM10_CLAIMS = {
    "brutus_standard_quasi_random": "~59",
    "brutus_standard_quasi_random_gold_standard": "~1000",
    "brutus_hierarchical": "~125",
    "brutus_hierarchical_gold_standard": "~1000",
}


def split_blocks(text):
    return [b for b in text.split("\n\n") if b.strip()]


def parse_final_time(blocks):
    """final_time = first token of last block's header line."""
    if not blocks:
        return None
    last = blocks[-1]
    lines = [ln for ln in last.splitlines() if ln.strip()]
    if not lines:
        return None
    header = lines[0].split()
    if not header:
        return None
    try:
        return float(header[0])
    except ValueError:
        return None


def stats_for(values):
    if not values:
        return None
    counter = Counter(values)
    mode_val, mode_count = counter.most_common(1)[0]
    median_val = statistics.median(values)
    # Integer rounding per D-09.
    return {
        "n": len(values),
        "min": min(values),
        "median": median_val,
        "median_integer_rounded": int(round(median_val)),
        "mode": mode_val,
        "mode_count": mode_count,
        "max": max(values),
    }


def main():
    out = {
        "probe": "DATA-06 snapshot-count + final-timestep distribution probe",
        "run_date_utc": datetime.datetime.utcnow().isoformat(timespec="seconds") + "Z",
        "interpreter": ".venv/bin/python (numpy 2.2.0)",
        "repo_root": REPO_ROOT,
        "method": "split on '\\n\\n', non-empty blocks = snapshots; final_time = first token of last block's header; split: per D-09 distributions (min/median/mode/max + modal counts), median with integer rounding used for CLM-10",
        "clm10_claims": CLM10_CLAIMS,
        "variants": {},
    }

    for folder in FOLDERS:
        folder_path = os.path.join(DATA_BASE, folder)
        if not os.path.isdir(folder_path):
            out["variants"][folder] = {"error": f"missing folder"}
            continue
        snapshot_counts = []
        final_times = []
        n_files = 0
        n_final_ge_9_5 = 0
        for fname in sorted(os.listdir(folder_path)):
            if not fname.endswith(".txt"):
                continue
            n_files += 1
            with open(os.path.join(folder_path, fname), "r") as f:
                text = f.read()
            blocks = split_blocks(text)
            snapshot_counts.append(len(blocks))
            ft = parse_final_time(blocks)
            if ft is not None:
                final_times.append(ft)
                if ft >= 9.5:
                    n_final_ge_9_5 += 1
        snap_stats = stats_for(snapshot_counts)
        ft_stats = stats_for(final_times) if final_times else None
        prevalence = (n_final_ge_9_5 / len(final_times)) if final_times else 0.0

        # CLM-10 verdict: integer-rounded median vs claim.
        claim_str = CLM10_CLAIMS.get(folder, "")
        claim_int = int(re.sub(r"[^\d]", "", claim_str)) if claim_str else None
        observed_median_int = snap_stats["median_integer_rounded"] if snap_stats else None
        if observed_median_int is None or claim_int is None:
            verdict = "unverified"
        elif observed_median_int == claim_int:
            verdict = "confirmed"
        else:
            verdict = "corrected"

        out["variants"][folder] = {
            "n_files": n_files,
            "snapshot_count_stats": snap_stats,
            "final_time_stats": ft_stats,
            "n_final_time_parsed": len(final_times),
            "n_final_ge_9_5": n_final_ge_9_5,
            "prevalence_final_ge_9_5": prevalence,
            "clm10_claim_str": claim_str,
            "clm10_claim_int": claim_int,
            "clm10_observed_median_int": observed_median_int,
            "clm10_verdict": verdict,
            "clm10_evidence_mode_count": snap_stats["mode_count"] if snap_stats else None,
            "clm10_evidence_mode_value": snap_stats["mode"] if snap_stats else None,
        }

    print(json.dumps(out, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
