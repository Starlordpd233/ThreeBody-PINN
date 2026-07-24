#!/usr/bin/env python3
"""Phase 44 evidence manifest: pin every input read by the three diag scripts.

Reads the provenance blocks embedded in the three diag outputs, recomputes each
input's SHA-256 from the current tree, and cross-checks that every recorded
path+hash matches EXACTLY (tamper evidence: a hash disagreement between a diag
script's recorded inputs and the current tree halts without writing). Writes
manifest.json with no timestamp, so it is a deterministic function of the tree at
a given commit. git_head / git_head_available mirror pinn/verify.py's bounded
`git rev-parse HEAD`. Plain stdlib only (hashlib, json, subprocess, pathlib); no
CLI args; repo root from __file__; cwd-independent.
"""
from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path

# diag outputs, relative to this script's directory (evidence/).
DIAG_OUTPUTS = [
    "diag01/eps_h_distribution.json",
    "diag02/loss_decomposition.json",
    "diag03/seed_band.json",
]


def repo_root() -> Path:
    p = Path(__file__).resolve()
    while p != p.parent:
        if (p / ".planning").is_dir():
            return p
        p = p.parent
    raise SystemExit("build_manifest FAIL-CLOSED: could not locate repo root")


REPO = repo_root()
EVIDENCE = Path(__file__).resolve().parent
OUTPUT = EVIDENCE / "manifest.json"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def git_head():
    """Bounded `git rev-parse HEAD` -> (head_sha | None, available). Mirrors pinn/verify.py."""
    try:
        r = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=str(REPO), capture_output=True, text=True, timeout=10,
        )
        if r.returncode == 0:
            sha = r.stdout.strip()
            if sha:
                return sha, True
    except Exception:
        pass
    return None, False


def fail_closed(msg):
    raise SystemExit(f"build_manifest FAIL-CLOSED: {msg} (no manifest written)")


def main() -> None:
    # 1. collect provenance inputs recorded by the three diag outputs
    entries = []  # (repo_relative_path, recorded_sha256, source_diag)
    for rel in DIAG_OUTPUTS:
        p = EVIDENCE / rel
        if not p.is_file():
            fail_closed(f"diag output missing: {rel}")
        d = json.loads(p.read_text())
        for e in d.get("provenance", {}).get("inputs", []):
            entries.append((e["path"], e["sha256"], rel))

    # 2. cross-check: recompute each input's sha256 from the live tree; require exact match
    inputs = {}
    mismatches = []
    for path, recorded, src in entries:
        fp = REPO / path
        if not fp.is_file():
            mismatches.append({"path": path, "source": src, "reason": "file missing",
                               "recorded": recorded, "computed": None})
            continue
        computed = sha256(fp)
        if computed != recorded:
            mismatches.append({"path": path, "source": src,
                               "reason": "hash mismatch (tamper evidence)",
                               "recorded": recorded, "computed": computed})
        else:
            inputs[path] = computed
    if mismatches:
        fail_closed(f"{len(mismatches)} provenance cross-check mismatch(es): {mismatches}")

    head, available = git_head()
    diag_outputs_repo_rel = [str((EVIDENCE / rel).relative_to(REPO)) for rel in DIAG_OUTPUTS]
    out = {
        "schema": "phase44-evidence-manifest/v1",
        "generated_by": "evidence/build_manifest.py",
        "git_head": head,
        "git_head_available": available,
        "inputs": inputs,  # repo-relative path -> sha256 (Phase 43 sha256-dict shape)
        "cross_check": {
            "diag_outputs_verified": diag_outputs_repo_rel,
            "provenance_entries_checked": len(entries),
            "all_match": True,
            "mismatches": [],
        },
        "convention_note": (
            "Standalone manifest.json is a NEW Phase 44 convention, assembled from "
            "pinn/verify.py's git_head/git_head_available bounded mechanics plus Phase 43's "
            "inline sha256-dict shape (repo-relative path -> hex digest). It is the phase's "
            "single pinning record; the diag outputs carry no timestamp and remain byte-identical "
            "across re-runs. Recorded choice, not an accident."
        ),
    }
    with OUTPUT.open("w") as fh:
        json.dump(out, fh, indent=2, sort_keys=True)
        fh.write("\n")
    print(f"wrote {OUTPUT.relative_to(REPO)} ({OUTPUT.stat().st_size} bytes); "
          f"{len(inputs)} inputs pinned; all_match=True; git_head_available={available}")


if __name__ == "__main__":
    main()
