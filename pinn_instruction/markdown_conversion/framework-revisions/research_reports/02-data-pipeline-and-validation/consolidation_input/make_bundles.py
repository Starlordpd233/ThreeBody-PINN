#!/usr/bin/env python3
"""Build the Issue-02 consolidation-input bundles.

Concatenates the eight Stage-1 research reports (anonymized R1-R8) and the five
research_package/specs/ snapshots into two upload bundles, verifies byte-exact
round-trip extraction via SHA-256, and writes BUNDLE-MANIFEST.md.

Design: docs/superpowers/specs/2026-06-11-issue02-research-results-consolidation-packaging-design.md

Usage:
    python3 make_bundles.py --selftest
    python3 make_bundles.py --build-date YYYY-MM-DD
"""

import argparse
import hashlib
import re
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent           # consolidation_input/
BASE = HERE.parent                               # 02-data-pipeline-and-validation/

SELF_ID_TOKENS = [
    "chatgpt", "gpt", "openai", "gemini", "google", "kimi", "moonshot",
    "glm", "zhipu", "fable", "claude", "anthropic",
]


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def check_no_delimiter_collision(name: str, data: bytes) -> None:
    for i, line in enumerate(data.split(b"\n"), 1):
        if line.startswith(b"===== "):
            sys.exit(
                f"ABORT: delimiter collision in {name} line {i}: {line[:60]!r}. "
                "Choose a longer delimiter and update the design spec."
            )


def self_id_scan(data: bytes) -> dict:
    text = data.decode("utf-8", errors="replace").lower()
    counts = {}
    for tok in SELF_ID_TOKENS:
        n = len(re.findall(r"\b" + re.escape(tok) + r"\b", text))
        if n:
            counts[tok] = n
    return counts


def begin_line(kind: str, label: str, data: bytes) -> str:
    if kind == "REPORT":
        return (f"===== BEGIN REPORT {label} "
                f"({len(data)} bytes, sha256 {sha256(data)[:12]}) =====")
    return f"===== BEGIN FILE {label} ====="


def end_line(kind: str, label: str) -> str:
    return f"===== END {kind} {label} ====="


def build_bundle(sources, kind: str, header_lines) -> bytes:
    """sources: list of (label, data) tuples. Returns full bundle bytes."""
    parts = [("\n".join(header_lines) + "\n").encode("utf-8")]
    for label, data in sources:
        parts.append(
            b"\n" + begin_line(kind, label, data).encode("utf-8") + b"\n"
            + data
            + b"\n" + end_line(kind, label).encode("utf-8") + b"\n"
        )
    return b"".join(parts)


def extract_sections(bundle: bytes, kind: str) -> dict:
    """Invert build_bundle: return {label: content_bytes}."""
    pat = re.compile(
        rb"===== BEGIN " + kind.encode() + rb" (.+?)"
        rb"(?: \(\d+ bytes, sha256 [0-9a-f]{12}\))? =====\n"
        rb"(.*?)"
        rb"\n===== END " + kind.encode() + rb" (.+?) =====\n",
        re.DOTALL,
    )
    out = {}
    for m in pat.finditer(bundle):
        label_b, content, label_e = m.group(1).decode(), m.group(2), m.group(3).decode()
        if label_b != label_e:
            sys.exit(f"ABORT: mismatched delimiters: BEGIN {label_b!r} vs END {label_e!r}")
        out[label_b] = content
    return out


def verify_roundtrip(bundle_path: Path, kind: str, expected: dict) -> None:
    got = extract_sections(bundle_path.read_bytes(), kind)
    if set(got) != set(expected):
        sys.exit(
            f"ABORT: {bundle_path.name}: extracted sections {sorted(got)} "
            f"!= expected {sorted(expected)}"
        )
    for label, data in expected.items():
        if sha256(got[label]) != sha256(data):
            sys.exit(f"ABORT: {bundle_path.name}: hash mismatch for section {label}")
    print(f"verified {bundle_path.name}: {len(expected)} sections round-trip byte-exact")


def selftest() -> None:
    fixtures = [
        ("R1", b"alpha doc\nends with newline\n"),
        ("R2", b"beta doc without trailing newline"),
        ("R3", "gamma é三体\n\nblank lines inside\n\n".encode("utf-8")),
    ]
    with tempfile.TemporaryDirectory() as td:
        bp = Path(td) / "bundle.md"
        bp.write_bytes(build_bundle(fixtures, "REPORT", ["# selftest bundle"]))
        verify_roundtrip(bp, "REPORT", dict(fixtures))
    try:
        check_no_delimiter_collision("bad.md", b"text\n===== BEGIN REPORT fake =====\n")
    except SystemExit:
        print("collision detection: OK")
    else:
        sys.exit("ABORT: collision check failed to trigger on a colliding fixture")
    print("selftest passed")


def real_build(build_date: str) -> None:
    report_files = sorted((BASE / "research_results").glob("*.md"))
    spec_files = sorted((BASE / "research_package" / "specs").glob("*.md"))
    if len(report_files) != 8:
        sys.exit(f"ABORT: expected 8 report files, found {len(report_files)}")
    if len(spec_files) != 5:
        sys.exit(f"ABORT: expected 5 spec files, found {len(spec_files)}")

    reports = []   # (tag, path, data)
    for i, p in enumerate(report_files, 1):
        data = p.read_bytes()
        check_no_delimiter_collision(p.name, data)
        reports.append((f"R{i}", p, data))
    specs = []     # (filename, path, data)
    for p in spec_files:
        data = p.read_bytes()
        check_no_delimiter_collision(p.name, data)
        specs.append((p.name, p, data))

    rb_header = [
        "# Research-Results Bundle — Issue 02 (Derived Artifact)",
        "",
        f"Build date: {build_date}. This file is a packaging artifact: the original report",
        "files in `research_results/` govern. Content between BEGIN/END delimiters is",
        "byte-identical to the originals (SHA-256-verified at build time). Reports are",
        "anonymized as R1-R8; the tag-to-file mapping is recorded only in the project-side",
        "manifest, which is not provided to the consolidation agent.",
        "",
        "## Contents",
        "",
        "| Tag | Bytes |",
        "|-----|-------|",
    ] + [f"| {tag} | {len(data):,} |" for tag, _, data in reports]

    sb_header = [
        "# Specs Bundle — Issue 02 (Derived Artifact)",
        "",
        f"Build date: {build_date}. This file is a packaging artifact: the original spec",
        "snapshot files in `research_package/specs/` govern. Content between BEGIN/END",
        "delimiters is byte-identical to the originals (SHA-256-verified at build time).",
        "",
        "## Contents",
        "",
        "| File | Bytes |",
        "|------|-------|",
    ] + [f"| `{name}` | {len(data):,} |" for name, _, data in specs]

    rb_path = HERE / "research-results-bundle.md"
    sb_path = HERE / "specs-bundle.md"
    rb_path.write_bytes(build_bundle([(t, d) for t, _, d in reports], "REPORT", rb_header))
    sb_path.write_bytes(build_bundle([(n, d) for n, _, d in specs], "FILE", sb_header))

    verify_roundtrip(rb_path, "REPORT", {t: d for t, _, d in reports})
    verify_roundtrip(sb_path, "FILE", {n: d for n, _, d in specs})

    m = [
        "# Bundle Manifest — Issue-02 Consolidation Input",
        "",
        f"Build date: {build_date}. Generated by `make_bundles.py`. Self-verification",
        "(byte-exact round-trip extraction of every section, SHA-256 compare against the",
        "originals) passed at build time. Originals govern: `research_results/` and",
        "`research_package/specs/` are authoritative; the bundles are derived artifacts.",
        "",
        "**Do NOT upload this file to the consolidation agent** — it de-anonymizes the",
        "R-tags. De-reference report provenance here after the output lands.",
        "",
        "## Reports (`research-results-bundle.md`)",
        "",
        "| Tag | Original file | Bytes | SHA-256 | Self-ID token hits |",
        "|-----|---------------|-------|---------|--------------------|",
    ]
    for tag, p, data in reports:
        hits = self_id_scan(data)
        hits_s = ", ".join(f"{k}: {v}" for k, v in sorted(hits.items())) or "none"
        m.append(f"| {tag} | `{p.name}` | {len(data):,} | `{sha256(data)}` | {hits_s} |")
    m += [
        "",
        "Self-ID scan: case-insensitive word-boundary counts of model/vendor name tokens",
        "(" + ", ".join(SELF_ID_TOKENS) + ") inside each verbatim report body.",
        "Anonymization is best-effort at the packaging layer; bodies are not scrubbed.",
        "Note: exact byte sizes also appear in the uploaded bundle header and are themselves",
        "distinguishing (R4 notably so); the prompt's Independence ground rule is the",
        "mitigation.",
        "",
        "## Specs (`specs-bundle.md`)",
        "",
        "| File | Bytes | SHA-256 |",
        "|------|-------|---------|",
    ]
    for name, p, data in specs:
        m.append(f"| `{name}` | {len(data):,} | `{sha256(data)}` |")
    (HERE / "BUNDLE-MANIFEST.md").write_text("\n".join(m) + "\n", encoding="utf-8")

    print(f"wrote {rb_path.name} ({rb_path.stat().st_size:,} bytes), "
          f"{sb_path.name} ({sb_path.stat().st_size:,} bytes), BUNDLE-MANIFEST.md")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--build-date", help="YYYY-MM-DD, stamped into bundle headers")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()
    if args.selftest:
        selftest()
    elif args.build_date:
        real_build(args.build_date)
    else:
        ap.error("pass --selftest or --build-date YYYY-MM-DD")


if __name__ == "__main__":
    main()
