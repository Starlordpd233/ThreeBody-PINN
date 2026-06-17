# probes/data02_blacklist.py — DATA-02 blacklist composition + consumption map (CLM-03)
# D-02 re-derivability header: run from repo root.
#   .venv/bin/python .planning/phases/24-empirical-dataset-verification-and-correction-addendum/probes/data02_blacklist.py
# Reads (read-only):
#   simulation_data/Documentation/problematic_ics_blacklist.json
#   simulation_data/Scripts/** (grep for blacklist loading)
#   simulation_data/Validation/** (grep for blacklist loading)
# Records: per-key counts, total, and a nuanced consumption map into 24-VERIFIED-FACTS.md.
#
# D-10: the M11 "not loaded at training time" aspect concerns pinn/ (SCOPE-10) — recorded
#       as `unverified — outside grounding limits, deferred to Phase 25 adjudication and
#       the FUT-01 handoff`. We grep SCOPE-07 grounding only.
# D-08 verdict vocabulary: confirmed | corrected | unverified.

import os
import re
import json
import subprocess
import datetime

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))
BLACKLIST = os.path.join(REPO_ROOT, "simulation_data", "Documentation", "problematic_ics_blacklist.json")
SCRIPTS_DIR = os.path.join(REPO_ROOT, "simulation_data", "Scripts")
VALIDATION_DIR = os.path.join(REPO_ROOT, "simulation_data", "Validation")


def main():
    with open(BLACKLIST) as f:
        bl = json.load(f)

    composition = {k: len(v) for k, v in bl.items()}
    total = sum(composition.values())

    # Nuanced consumption map (D-10): grep SCOPE-07 grounding paths for blacklist loading.
    # The expected nuance: Validation/dataset_readiness_checks/config.py loads the json,
    # but current Brutus runners do NOT (they use Documentation/problematic_ics/{type}/ dirs).
    grep_paths = [SCRIPTS_DIR, VALIDATION_DIR]
    grep_results = {}
    for p in grep_paths:
        # -l: list files. Use --include for source extensions to skip pycache.
        r = subprocess.run(
            [
                "grep", "-rln", "--include=*.py", "--include=*.json", "--include=*.md",
                "-E", "problematic_ics_blacklist|blacklist",
                p,
            ],
            capture_output=True, text=True,
        )
        grep_results[p] = [ln for ln in r.stdout.splitlines() if ln]

    out = {
        "probe": "DATA-02 blacklist composition + consumption map",
        "run_date_utc": datetime.datetime.utcnow().isoformat(timespec="seconds") + "Z",
        "interpreter": ".venv/bin/python",
        "repo_root": REPO_ROOT,
        "blacklist_path": BLACKLIST,
        "composition": composition,
        "total": total,
        "consumption_grep_paths": grep_paths,
        "files_mentioning_blacklist": grep_results,
        "consumption_map": {
            "Validation/dataset_readiness_checks/config.py": (
                "Loads problematic_ics_blacklist.json (D-10 cross-check; SCOPE-07 grounding)"
            ),
            "simulation_data/Scripts/brutus_runners/*": (
                "Do NOT load the json blacklist; use Documentation/problematic_ics/{type}/ dirs "
                "(README:1005 — legacy … not used by current runners)"
            ),
            "pinn/ training-time load": (
                "unverified — outside grounding limits (SCOPE-10); deferred to Phase 25 "
                "adjudication and the FUT-01 handoff"
            ),
        },
    }
    print(json.dumps(out, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
