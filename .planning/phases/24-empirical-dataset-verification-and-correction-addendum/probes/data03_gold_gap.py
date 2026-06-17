# probes/data03_gold_gap.py — DATA-03 gold-counterpart gap (CLM-04, CLM-05)
# D-02 re-derivability header: run from repo root.
#   .venv/bin/python .planning/phases/24-empirical-dataset-verification-and-correction-addendum/probes/data03_gold_gap.py
# Reads (read-only):
#   simulation_data/Data/brutus_output/brutus_standard_quasi_random/         (base)
#   simulation_data/Data/brutus_output/brutus_standard_quasi_random_gold_standard/  (gold)
#   simulation_data/Data/ic_final/ic_standard_quasi_random/                  (IC folders, WR-04)
#   simulation_data/Documentation/standard_quasi_random_ids_not_in_gold.md   (cross-check)
# Records: base_ids − gold_ids set diff, IC-folder count, Brutus-output counts per
#          CLM-05 observables (WR-04), doc-list cross-check, verdicts.
#
# D-13: ID parse + set arithmetic, NOT a grep of the doc (Pitfall 5: naive 4-digit grep
#       captures summary numbers 2565/2749 and yields 185 instead of 184).
# WR-04: count IC folders and Brutus output folders separately.
# D-08 verdict vocabulary: confirmed | corrected | unverified.

import os
import re
import json
import datetime

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))
BASE_DIR = os.path.join(REPO_ROOT, "simulation_data", "Data", "brutus_output", "brutus_standard_quasi_random")
GOLD_DIR = os.path.join(REPO_ROOT, "simulation_data", "Data", "brutus_output", "brutus_standard_quasi_random_gold_standard")
IC_DIR = os.path.join(REPO_ROOT, "simulation_data", "Data", "ic_final", "ic_standard_quasi_random")
DOC = os.path.join(REPO_ROOT, "simulation_data", "Documentation", "standard_quasi_random_ids_not_in_gold.md")

ID_RE = re.compile(r"^brutus_standard_(\d{4})\.txt$")
IC_RE = re.compile(r"^ic_(?:standard|hierarchical)_(\d{4})\.txt$")


def parse_ids(folder, pattern):
    out = []
    for fname in os.listdir(folder):
        m = pattern.match(fname)
        if m:
            out.append(int(m.group(1)))
    return sorted(set(out))


def parse_doc_ids(path):
    """Parse the listed ID block in the doc (text lines containing 4-digit IDs at line start)."""
    ids = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            # Lines like "0001" or "0001, 0002, ..." (whitespace/comma-separated 4-digit IDs)
            for tok in re.split(r"[\s,]+", line):
                if re.fullmatch(r"\d{4}", tok):
                    ids.append(int(tok))
    return sorted(set(ids))


def main():
    base_ids = parse_ids(BASE_DIR, ID_RE)
    gold_ids = parse_ids(GOLD_DIR, ID_RE)
    ic_ids = parse_ids(IC_DIR, IC_RE)
    diff = sorted(set(base_ids) - set(gold_ids))
    doc_ids = parse_doc_ids(DOC)
    diff_in_doc = sorted(set(diff) & set(doc_ids))

    out = {
        "probe": "DATA-03 gold-counterpart gap (set diff) + CLM-05 WR-04 split counts",
        "run_date_utc": datetime.datetime.utcnow().isoformat(timespec="seconds") + "Z",
        "interpreter": ".venv/bin/python",
        "repo_root": REPO_ROOT,
        "brutus_base_dir": BASE_DIR,
        "brutus_gold_dir": GOLD_DIR,
        "ic_dir": IC_DIR,
        "doc_path": DOC,
        "clm_05_split_counts": {
            "ic_folder_count": len(ic_ids),
            "brutus_base_output_count": len(base_ids),
            "brutus_gold_output_count": len(gold_ids),
        },
        "set_diff": {
            "base_minus_gold_count": len(diff),
            "first_10_ids": diff[:10],
            "last_10_ids": diff[-10:],
        },
        "doc_cross_check": {
            "doc_listed_id_count": len(doc_ids),
            "intersection_with_set_diff": len(diff_in_doc),
            "intersection_matches_set_diff": diff_in_doc == diff,
        },
    }
    print(json.dumps(out, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
