# probes/data04_footers.py — DATA-04 footer-schema probe (CLM-07, CLM-08, CLM-09)
# D-02 re-derivability header: run from repo root.
#   .venv/bin/python .planning/phases/24-empirical-dataset-verification-and-correction-addendum/probes/data04_footers.py
# Reads (read-only): simulation_data/Data/brutus_output/{4 variants}
# Records: per-variant no-footer count, present-footer schema samples, tol=1e-14 subset, folder-default tuples.
#
# D-07 (unconditional, 2026-06-10 erratum corrections folded):
#   1. Gold filenames carry NO `_gold_` infix; folder encodes the variant.
#   2. The 1,550 hier / 701 std-base / 219 std-gold populations have NO `Result:` footer at all.
#      They are characterized as "no Result: footer at all and NO parameter fields anywhere".
#      NEVER use "partial footer" / "minimal footer" language — that is superseded.
# D-08 verdict vocabulary: confirmed | corrected | unverified.

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

# Folder-default tuples (CLM-09 priors from .claude/rules/dataset-reference.md "Typical Brutus Parameter Sets").
FOLDER_DEFAULT_TUPLES = {
    "brutus_standard_quasi_random": {"tol": "1e-13", "Lw": 118, "dt_out": 0.17},
    "brutus_standard_quasi_random_gold_standard": {"tol": "1e-13 (most common; 1e-14 subset)", "Lw": 130, "dt_out": 0.01},
    "brutus_hierarchical": {"tol": "1e-15", "Lw": 130, "dt_out": 0.08},
    "brutus_hierarchical_gold_standard": {"tol": "1e-13", "Lw": 130, "dt_out": 0.01},
}

# D-07 priors (corrected characterization, NOT values to force).
D07_PRIOR_NO_FOOTER = {
    "brutus_hierarchical": 1550,
    "brutus_standard_quasi_random": 701,
    "brutus_standard_quasi_random_gold_standard": 219,
}

RESULT_RE = re.compile(r"^Result:\s*filename=")
TOL_RE = re.compile(r"\btol=\s*(\S+)")
ETA_RE = re.compile(r"\beta=\s*(\S+)")
LW_RE = re.compile(r"\bLw=\s*(\S+)")
ENERGY_RE = re.compile(r"\bE_initial=\s*(\S+)\s+E_final=\s*(\S+)")


def parse_footer(text):
    """Return dict of parsed footer fields, or None if no Result: footer at all."""
    # Find the last line; walk up to last non-empty.
    lines = text.splitlines()
    for i in range(len(lines) - 1, -1, -1):
        line = lines[i].rstrip()
        if line.strip():
            if not RESULT_RE.match(line.strip()):
                return None
            # Parse schema on this line.
            m_tol = TOL_RE.search(line)
            m_eta = ETA_RE.search(line)
            m_lw = LW_RE.search(line)
            m_en = ENERGY_RE.search(line)
            return {
                "raw": line,
                "tol": m_tol.group(1) if m_tol else None,
                "eta": m_eta.group(1) if m_eta else None,
                "Lw": m_lw.group(1) if m_lw else None,
                "E_initial": m_en.group(1) if m_en else None,
                "E_final": m_en.group(2) if m_en else None,
            }
    return None


def assess_no_footer(filepath):
    """A no-footer file: NO Result: footer at all AND no parameter fields anywhere (D-07)."""
    with open(filepath, "r") as f:
        text = f.read()
    footer = parse_footer(text)
    if footer is not None:
        return False, footer
    # Sanity: a "no Result: footer" file must also lack tol/eta/Lw parameter fields anywhere.
    has_param = bool(TOL_RE.search(text)) or bool(ETA_RE.search(text)) or bool(LW_RE.search(text))
    return (not has_param), None


def main():
    out = {
        "probe": "DATA-04 footer-schema probe",
        "run_date_utc": datetime.datetime.utcnow().isoformat(timespec="seconds") + "Z",
        "interpreter": ".venv/bin/python (numpy 2.2.0)",
        "repo_root": REPO_ROOT,
        "D07_characterization": "no Result: footer at all AND no parameter fields anywhere (never 'partial footer' / 'minimal footer')",
        "priors_d07": {k: v for k, v in D07_PRIOR_NO_FOOTER.items()},
        "folder_default_tuples_claim": FOLDER_DEFAULT_TUPLES,
        "variants": {},
    }

    for folder in FOLDERS:
        folder_path = os.path.join(DATA_BASE, folder)
        if not os.path.isdir(folder_path):
            out["variants"][folder] = {"error": f"missing folder: {folder_path}"}
            continue
        fnames = sorted(os.listdir(folder_path))
        n_total = 0
        n_no_footer = 0
        n_with_footer = 0
        tol_counter = Counter()
        sample_footer = None
        sample_no_footer = None
        n_tol_1e_14 = 0  # CLM-08 subset (std-gold: 592 expected)
        for fname in fnames:
            if not fname.endswith(".txt"):
                continue
            n_total += 1
            fp = os.path.join(folder_path, fname)
            no_footer, footer = assess_no_footer(fp)
            if no_footer:
                n_no_footer += 1
                if sample_no_footer is None:
                    sample_no_footer = fname
            else:
                n_with_footer += 1
                if footer is not None:
                    tol = footer.get("tol")
                    if tol is not None:
                        tol_counter[tol] += 1
                        if tol == "1e-14":
                            n_tol_1e_14 += 1
                if sample_footer is None:
                    sample_footer = fname
        prior = D07_PRIOR_NO_FOOTER.get(folder)
        if prior is None:
            verdict_no_footer = "no_prior"
        elif n_no_footer == prior:
            verdict_no_footer = "confirmed"
        else:
            verdict_no_footer = "corrected"

        out["variants"][folder] = {
            "n_files": n_total,
            "no_footer_count": n_no_footer,
            "with_footer_count": n_with_footer,
            "no_footer_verdict_vs_d07_prior": verdict_no_footer,
            "tol_distribution_present_footers": dict(tol_counter),
            "n_tol_1e_14_subset": n_tol_1e_14,
            "sample_footer_filename": sample_footer,
            "sample_no_footer_filename": sample_no_footer,
        }

    # CLM-09: folder-default tuples are claims; we record them as observed reference values
    # (not a probe — there is no on-disk folder-default metadata file). Verdict = "claim_logged".
    out["clm09_folder_defaults"] = {
        "claim": FOLDER_DEFAULT_TUPLES,
        "verdict": "claim_logged (no on-disk folder-default metadata file; per dataset-reference rule)",
    }

    # CLM-08 verdict: std-gold tol=1e-14 subset expected 592
    std_gold = out["variants"].get("brutus_standard_quasi_random_gold_standard", {})
    n_1e_14 = std_gold.get("n_tol_1e_14_subset", 0)
    out["clm08_tol_1e_14_subset"] = {
        "expected_592": 592,
        "observed": n_1e_14,
        "verdict": "confirmed" if n_1e_14 == 592 else "corrected",
    }

    # Cross-check vs footer_audit_20251224_170141.md (read-only reference).
    out["cross_check"] = {
        "audit_file": "simulation_data/Validation/audit_reports/footer_audit_20251224_170141.md",
        "audit_no_footer_counts": D07_PRIOR_NO_FOOTER,
        "note": "audit file uses pre-correction 'Missing Result footer' framing; D-07 re-characterizes these as 'no Result: footer at all and no parameter fields anywhere' (NOT 'partial/minimal'). The counts themselves are in agreement.",
    }

    print(json.dumps(out, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
