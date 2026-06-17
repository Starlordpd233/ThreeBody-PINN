#!/usr/bin/env python3
"""AC-PIPE-05 (M13 / G4): standard-base minus standard-gold set-difference probe.

Disposable Phase-29 dataset probe. Reads only the on-disk simulation_data/ ID sets and the
standard_quasi_random_ids_not_in_gold.md documentation list; touches no production model
code and mutates nothing (VER-09 / SCOPE-10).

Invariant asserted: { standard-base IDs } - { standard-gold IDs } == { IDs listed in
not_in_gold.md }, with an exact (whole-set) intersection. Under Phase 29 D-01/D-03 zero gold
reruns are promoted, so the gold set is unchanged and the difference holds at its current size.

Anti-hardcode rule (mirrors the blacklist-contract Step-1A discipline): every count is DERIVED
from the parsed on-disk sets and the parsed documentation list. No expected count is written as
a literal in this file; the probe would pass at any size for which the three sets agree.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve()
# Walk up to the repo root (the dir that holds simulation_data/).
for parent in ROOT.parents:
    if (parent / "simulation_data").is_dir():
        REPO = parent
        break
else:
    print("AC-PIPE-05 FAIL: could not locate simulation_data/ from probe path")
    sys.exit(1)

BRUTUS = REPO / "simulation_data" / "Data" / "brutus_output"
BASE_DIR = BRUTUS / "brutus_standard_quasi_random"
GOLD_DIR = BRUTUS / "brutus_standard_quasi_random_gold_standard"
DOC = REPO / "simulation_data" / "Documentation" / "standard_quasi_random_ids_not_in_gold.md"

ID_RE = re.compile(r"^brutus_standard_(\d{4})\.txt$")


def ids_in(folder: Path) -> set:
    out = set()
    for p in folder.iterdir():
        m = ID_RE.match(p.name)
        if m:
            out.add(int(m.group(1)))
    return out


def doc_ids(md: Path) -> set:
    """Parse the 4-digit IDs from the fenced ID block under '## The ... IDs'."""
    text = md.read_text()
    out = set()
    in_fence = False
    for line in text.splitlines():
        if line.strip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            for tok in re.findall(r"\b(\d{4})\b", line):
                out.add(int(tok))
    return out


def main() -> int:
    for d in (BASE_DIR, GOLD_DIR):
        if not d.is_dir():
            print(f"AC-PIPE-05 FAIL: missing dataset folder {d}")
            return 1
    if not DOC.is_file():
        print(f"AC-PIPE-05 FAIL: missing documentation list {DOC}")
        return 1

    base = ids_in(BASE_DIR)
    gold = ids_in(GOLD_DIR)
    diff = base - gold
    documented = doc_ids(DOC)

    n_diff = len(diff)
    n_doc = len(documented)
    inter = diff & documented
    n_inter = len(inter)

    ok = True
    # Gold IDs must be a subset of base IDs (gold ICs are a byte-identical subset of base).
    if not gold.issubset(base):
        print(f"AC-PIPE-05 FAIL: {len(gold - base)} gold IDs absent from base set")
        ok = False
    # The computed difference must exactly equal the documented not-in-gold set.
    if diff != documented:
        only_diff = sorted(diff - documented)
        only_doc = sorted(documented - diff)
        print(f"AC-PIPE-05 FAIL: set mismatch; diff-only={only_diff[:8]} doc-only={only_doc[:8]}")
        ok = False
    # Intersection must cover the whole difference set (n_inter / n_diff).
    if n_inter != n_diff or n_inter != n_doc:
        print(f"AC-PIPE-05 FAIL: intersection {n_inter} != diff {n_diff} or doc {n_doc}")
        ok = False

    if ok:
        print(f"AC-PIPE-05 PASS {n_inter}/{n_diff}")
        print(f"  base={len(base)} gold={len(gold)} not_in_gold(doc)={n_doc} promoted=0 (D-01/D-03)")
        return 0
    return 1


if __name__ == "__main__":
    sys.exit(main())
