# probes/data01_id_gaps.py — DATA-01 ID-gap probe (CLM-01, CLM-02, CLM-12)
# D-02 re-derivability header: run from repo root.
#   .venv/bin/python .planning/phases/24-empirical-dataset-verification-and-correction-addendum/probes/data01_id_gaps.py
# Reads (read-only): simulation_data/Data/brutus_output/{brutus_standard_quasi_random,brutus_hierarchical}
# Records: n, min, max, gaps[0..max], gaps[0..nominal_end=3999/4999] per variant into 24-VERIFIED-FACTS.md.
#
# D-13: ID parse + diff against nominal range. NEVER bare file counts.
# D-08 verdict vocabulary: confirmed | corrected | unverified.
#
# Nominal-range convention grounding (D-13):
#   simulation_data/Documentation/README.md:146-153 (Dataset Variants and Inventory table)
#   declares ID Range as "0000-3998" for standard and "0000-4999" for hierarchical — i.e.
#   the *observed max ID* defines the nominal range end, NOT a prescreening cumulative
#   count or generation-script n_samples. This is the same convention the README's
#   "Gaps" column uses (1,250 std / 143 hier), so the authoritative gap count is
#   `gaps[0..max]` (NOT gaps[0..3999]). Both are emitted for transparency.

import os
import re
import datetime
import json

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))
DATA_BASE = os.path.join(REPO_ROOT, "simulation_data", "Data", "brutus_output")

FOLDERS = {
    "standard": "brutus_standard_quasi_random",
    "hierarchical": "brutus_hierarchical",
}

ID_RE = re.compile(r"^brutus_(?:standard|hierarchical)_(\d{4})\.txt$")


def parse_ids(folder_path):
    out = []
    for fname in os.listdir(folder_path):
        m = ID_RE.match(fname)
        if m:
            out.append(int(m.group(1)))
    out.sort()
    return out


def gap_stats(ids, nominal_end):
    s = set(ids)
    max_id = ids[-1] if ids else 0
    gaps_to_max = len(set(range(0, max_id + 1)) - s)
    gaps_to_nominal = len(set(range(0, nominal_end + 1)) - s)
    return max_id, gaps_to_max, gaps_to_nominal


def main():
    out = {
        "probe": "DATA-01 ID-gap probe",
        "run_date_utc": datetime.datetime.utcnow().isoformat(timespec="seconds") + "Z",
        "interpreter": ".venv/bin/python (numpy 2.2.0)",
        "repo_root": REPO_ROOT,
        "dataset_paths": {
            v: os.path.join(DATA_BASE, sub) for v, sub in FOLDERS.items()
        },
        "nominal_range_grounding": {
            "source": "simulation_data/Documentation/README.md:146-153 (Dataset Variants and Inventory)",
            "convention": "ID Range column defines nominal end as the observed max ID (0000-3998 std; 0000-4999 hier). README's 'Gaps' column equals gaps[0..max].",
            "note": "Both gaps[0..max] and gaps[0..nominal_end=3999/4999] are emitted for transparency per D-13.",
        },
        "results": {},
    }
    for variant, sub in FOLDERS.items():
        folder = os.path.join(DATA_BASE, sub)
        ids = parse_ids(folder)
        nominal_end = 3999 if variant == "standard" else 4999
        max_id, gaps_to_max, gaps_to_nominal = gap_stats(ids, nominal_end)
        out["results"][variant] = {
            "n_files": len(ids),
            "min_id": ids[0] if ids else None,
            "max_id": max_id,
            "gaps_0_to_max": gaps_to_max,
            f"gaps_0_to_{nominal_end}": gaps_to_nominal,
        }
    print(json.dumps(out, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
