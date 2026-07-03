#!/usr/bin/env python3
"""Build the Phase 30 six-file upload package.

The source package parts remain under research_package/source_parts/. This script
mechanically creates the six files in research_package/upload/, verifies that
bundle sections extract back to the exact source bytes, and records a manifest
for re-derivation.
"""

from __future__ import annotations

import argparse
import hashlib
import re
import shutil
import sys
import tempfile
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
PACKAGE = (
    ROOT
    / "pinn_instruction/markdown_conversion/framework-revisions/research_reports"
    / "03-curriculum-and-training-loop/research_package"
)
SOURCE = PACKAGE / "source_parts"
UPLOAD = PACKAGE / "upload"
MANIFEST = HERE / "30-UPLOAD-BUNDLE-MANIFEST.md"

SOURCE_BASELINE_RE = re.compile(r"^source_baseline:\s*(\S+)\s*$", re.MULTILINE)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def read_bytes(path: Path) -> bytes:
    if not path.exists():
        sys.exit(f"ABORT: missing expected source part: {path.relative_to(ROOT)}")
    return path.read_bytes()


def source_baseline() -> str:
    master = read_bytes(SOURCE / "RESEARCH-CONTEXT-MASTER.md").decode(
        "utf-8", errors="replace"
    )
    match = SOURCE_BASELINE_RE.search(master)
    if not match:
        sys.exit("ABORT: source_parts/RESEARCH-CONTEXT-MASTER.md lacks source_baseline")
    return match.group(1)


def check_no_delimiter_collision(label: str, data: bytes) -> None:
    for line_no, line in enumerate(data.split(b"\n"), 1):
        if line.startswith(b"===== "):
            sys.exit(
                f"ABORT: delimiter collision in {label} line {line_no}: "
                f"{line[:80]!r}"
            )


def begin_line(label: str, data: bytes) -> str:
    return f"===== BEGIN FILE {label} ({len(data)} bytes, sha256 {sha256(data)}) ====="


def end_line(label: str) -> str:
    return f"===== END FILE {label} ====="


def build_bundle(sources: list[tuple[str, bytes]], header_lines: list[str]) -> bytes:
    parts = [("\n".join(header_lines) + "\n").encode("utf-8")]
    for label, data in sources:
        check_no_delimiter_collision(label, data)
        parts.append(
            b"\n"
            + begin_line(label, data).encode("utf-8")
            + b"\n"
            + data
            + b"\n"
            + end_line(label).encode("utf-8")
            + b"\n"
        )
    return b"".join(parts)


def extract_sections(bundle: bytes) -> dict[str, bytes]:
    pattern = re.compile(
        rb"===== BEGIN FILE (.+?) \(\d+ bytes, sha256 [0-9a-f]{64}\) =====\n"
        rb"(.*?)"
        rb"\n===== END FILE (.+?) =====\n",
        re.DOTALL,
    )
    sections: dict[str, bytes] = {}
    for match in pattern.finditer(bundle):
        begin = match.group(1).decode("utf-8")
        body = match.group(2)
        end = match.group(3).decode("utf-8")
        if begin != end:
            sys.exit(f"ABORT: mismatched bundle delimiters: {begin!r} vs {end!r}")
        sections[begin] = body
    return sections


def verify_roundtrip(path: Path, expected: dict[str, bytes]) -> None:
    got = extract_sections(path.read_bytes())
    if set(got) != set(expected):
        sys.exit(
            f"ABORT: {path.name} sections {sorted(got)} != expected {sorted(expected)}"
        )
    for label, data in expected.items():
        if got[label] != data:
            sys.exit(f"ABORT: {path.name} section {label} changed during bundling")


def bundle_header(title: str, build_date: str, rows: list[tuple[str, bytes]]) -> list[str]:
    return [
        f"# {title}",
        "",
        f"Build date: {build_date}. This is a mechanical transport bundle for the",
        "doc-03 research package. Content between BEGIN/END delimiters is",
        "byte-identical to the source package parts, verified at build time by",
        "round-trip extraction and SHA-256 comparison. The wrapper text is not a",
        "source edit and does not summarize the enclosed files.",
        "",
        "## Contents",
        "",
        "| File | Bytes | SHA-256 |",
        "|------|-------|---------|",
        *[f"| `{label}` | {len(data):,} | `{sha256(data)}` |" for label, data in rows],
    ]


def write_upload_master(build_date: str, baseline: str) -> None:
    text = f"""---
title: doc-03 Research Context Master
package_for: doc-03 (curriculum + training loop)
role: uploaded entry point for the six-file transport package
status: active
created: 2026-06-18
updated: {build_date}
source_baseline: {baseline}
self_contained: true
form: six-file upload package; prompt is pasted separately
---

# doc-03 Research Context Master

This is the entry point for the doc-03 ("Curriculum and Training Loop")
external-research package. The package has exactly six uploaded files. The
prompt is pasted separately and is not an attachment.

The package is self-contained. Work only from the six attached files. Do not
assume, invent, fetch, or request any file that is not attached. Some uploaded
files are mechanical bundles: content between BEGIN/END delimiters is
byte-identical to the named source part and was round-trip verified before
handoff. Treat bundled sections exactly as if the corresponding bare filename
had been attached separately.

## Reading Order

1. `RESEARCH-CONTEXT-MASTER.md` - this file.
2. `TASK-AND-CONSTRAINTS-BUNDLE.md` - hard constraints, framed questions, and
   the non-binding resolution skeleton.
3. `CLAIMS-AND-FACTS-BUNDLE.md` - claimed-vs-verified figure register,
   v1.5-verified dataset anchors, and minimal consolidated dataset context.
4. `03-curriculum-and-training-loop.md` - the issue doc, the adjudication
   subject.
5. `FRAMEWORK-SPECS-BUNDLE.md` - the framework spec snapshots.
6. `BASELINE-REPORTS-BUNDLE.md` - the baseline design-intent reports.

## Source-Treatment Preamble

- The issue doc is non-authoritative. Its findings and "Recommended
  Resolutions" may contain errors. Adjudicate them; do not treat them as
  settled.
- `ctl_instruction.md` and `pinn_architecture.md`, inside
  `FRAMEWORK-SPECS-BUNDLE.md`, are the framework spec-edit targets and the
  source of truth for downstream adjudication.
- The issue doc's implementation-code "Canonical" citations are overridden.
  The framework specs govern where those citations conflict with the package
  constraints.
- The hard constraints in `scope-12-hard-constraints.md`, inside
  `TASK-AND-CONSTRAINTS-BUNDLE.md`, are locked v1.4 + v1.5 outcomes. Do not
  re-open them.
- Current doc-03 positions in the framework specs on curriculum staging, batch
  construction, stage transitions, loss scaling, tau_L / L_max formulas, and
  gradient clipping are the revisable baseline. Reconcile any proposed changes
  under the locked constraints.
- Figures are claims until verified. Use `claims-register.md`, inside
  `CLAIMS-AND-FACTS-BUNDLE.md`, for every CLM-NN status. A
  `claimed-unverified` row is an input claim, not a fact.
- Annotations live in this master and in bundle wrapper tables, not inside the
  byte-identical bundled sections.

## Uploaded File Manifest

| Uploaded file | Contents | Treatment |
|---------------|----------|-----------|
| `RESEARCH-CONTEXT-MASTER.md` | This entry point | Orientation and source treatment only |
| `TASK-AND-CONSTRAINTS-BUNDLE.md` | `scope-12-hard-constraints.md`; `framed-research-questions.md`; `resolution-doc-skeleton.md` | Generated/source-authored package parts, bundled byte-identically for transport |
| `CLAIMS-AND-FACTS-BUNDLE.md` | `claims-register.md`; `verified-facts-reference.md`; `consolidated-context.md` | Grounding-class package parts; verified rows retain their provenance labels by design |
| `03-curriculum-and-training-loop.md` | Issue doc snapshot | Non-authoritative adjudication subject |
| `FRAMEWORK-SPECS-BUNDLE.md` | `ctl_instruction.md`; `pinn_architecture.md`; `sampling_method.md` | Byte-identical framework-spec snapshots; bundled for transport, not summarized |
| `BASELINE-REPORTS-BUNDLE.md` | `review_of_framework.md`; `stage_strat_revision.md` | Byte-identical baseline design-intent reports; critique mandate applies |

## Bundle Reading Rule

When a bundle contains multiple BEGIN/END sections, read the wrapper table first,
then read each enclosed section as its named file. The wrapper exists only to
reduce the upload count. It does not merge findings, change source standing, or
resolve conflicts between enclosed files.
"""
    (UPLOAD / "RESEARCH-CONTEXT-MASTER.md").write_text(text, encoding="utf-8")


def collect_sources() -> dict[str, list[tuple[str, bytes]]]:
    return {
        "TASK-AND-CONSTRAINTS-BUNDLE.md": [
            ("scope-12-hard-constraints.md", read_bytes(SOURCE / "scope-12-hard-constraints.md")),
            ("framed-research-questions.md", read_bytes(SOURCE / "framed-research-questions.md")),
            ("resolution-doc-skeleton.md", read_bytes(SOURCE / "resolution-doc-skeleton.md")),
        ],
        "CLAIMS-AND-FACTS-BUNDLE.md": [
            ("claims-register.md", read_bytes(SOURCE / "claims-register.md")),
            ("verified-facts-reference.md", read_bytes(SOURCE / "verified-facts-reference.md")),
            (
                "consolidated-context.md",
                read_bytes(SOURCE / "specs/consolidated-context.md"),
            ),
        ],
        "FRAMEWORK-SPECS-BUNDLE.md": [
            ("ctl_instruction.md", read_bytes(SOURCE / "specs/ctl_instruction.md")),
            ("pinn_architecture.md", read_bytes(SOURCE / "specs/pinn_architecture.md")),
            ("sampling_method.md", read_bytes(SOURCE / "specs/sampling_method.md")),
        ],
        "BASELINE-REPORTS-BUNDLE.md": [
            ("review_of_framework.md", read_bytes(SOURCE / "specs/review_of_framework.md")),
            ("stage_strat_revision.md", read_bytes(SOURCE / "specs/stage_strat_revision.md")),
        ],
    }


def build(build_date: str) -> None:
    UPLOAD.mkdir(exist_ok=True)
    baseline = source_baseline()
    write_upload_master(build_date, baseline)

    issue_data = read_bytes(SOURCE / "specs/03-curriculum-and-training-loop.md")
    issue_path = UPLOAD / "03-curriculum-and-training-loop.md"
    issue_path.write_bytes(issue_data)

    bundles = collect_sources()
    for bundle_name, rows in bundles.items():
        title = bundle_name.replace("-", " ").replace(".md", "").title()
        bundle_path = UPLOAD / bundle_name
        bundle_path.write_bytes(build_bundle(rows, bundle_header(title, build_date, rows)))
        verify_roundtrip(bundle_path, dict(rows))

    if issue_path.read_bytes() != issue_data:
        sys.exit("ABORT: standalone issue doc changed during copy")

    upload_files = sorted(p.name for p in UPLOAD.iterdir() if p.is_file())
    expected_uploads = sorted(
        [
            "RESEARCH-CONTEXT-MASTER.md",
            "TASK-AND-CONSTRAINTS-BUNDLE.md",
            "CLAIMS-AND-FACTS-BUNDLE.md",
            "03-curriculum-and-training-loop.md",
            "FRAMEWORK-SPECS-BUNDLE.md",
            "BASELINE-REPORTS-BUNDLE.md",
        ]
    )
    if upload_files != expected_uploads:
        sys.exit(f"ABORT: upload files {upload_files} != expected {expected_uploads}")

    write_manifest(build_date, baseline, issue_data, bundles)
    print("built Phase 30 upload package: 6 files")


def write_manifest(
    build_date: str,
    baseline: str,
    issue_data: bytes,
    bundles: dict[str, list[tuple[str, bytes]]],
) -> None:
    lines = [
        "# Phase 30 Upload Bundle Manifest",
        "",
        f"Build date: {build_date}",
        f"Source baseline: `{baseline}`",
        "",
        "Generated by `build_phase30_upload_bundles.py`. The upload package",
        "contains exactly six files under `research_package/upload/`; the",
        "paste-ready prompt remains `research_package/RESEARCH-AGENT-PROMPT.md`",
        "and is not counted as an uploaded file.",
        "",
        "## Upload Files",
        "",
        "| Upload file | Source parts | Verification |",
        "|-------------|--------------|--------------|",
        (
            "| `RESEARCH-CONTEXT-MASTER.md` | generated from package metadata | "
            "authored upload entry point |"
        ),
        (
            "| `03-curriculum-and-training-loop.md` | "
            "`source_parts/specs/03-curriculum-and-training-loop.md` | "
            f"byte-identical copy; sha256 `{sha256(issue_data)}` |"
        ),
    ]
    for bundle_name, rows in bundles.items():
        labels = ", ".join(f"`{label}`" for label, _ in rows)
        lines.append(
            f"| `{bundle_name}` | {labels} | round-trip extraction + SHA-256 passed |"
        )
    lines += [
        "",
        "## Source Part Hashes",
        "",
        "| Source part | Bytes | SHA-256 |",
        "|-------------|-------|---------|",
        (
            "| `source_parts/specs/03-curriculum-and-training-loop.md` | "
            f"{len(issue_data):,} | `{sha256(issue_data)}` |"
        ),
    ]
    for rows in bundles.values():
        for label, data in rows:
            lines.append(f"| `{label}` | {len(data):,} | `{sha256(data)}` |")
    lines += [
        "",
        "## Verification Notes",
        "",
        "- Bundles use `===== BEGIN FILE ... =====` / `===== END FILE ... =====` delimiters.",
        "- The builder aborts if any source part already contains a delimiter-looking line.",
        "- Each bundle is extracted immediately after build; every extracted section must",
        "  match the source bytes exactly.",
        "- Bundling is transport-only. It does not summarize, rewrite, or adjudicate any",
        "  bundled section.",
        "",
    ]
    MANIFEST.write_text("\n".join(lines), encoding="utf-8")


def selftest() -> None:
    fixtures = [
        ("alpha.md", b"alpha\nends with newline\n"),
        ("beta.md", b"beta without trailing newline"),
    ]
    with tempfile.TemporaryDirectory() as td:
        path = Path(td) / "bundle.md"
        path.write_bytes(build_bundle(fixtures, ["# Selftest Bundle"]))
        verify_roundtrip(path, dict(fixtures))
    try:
        check_no_delimiter_collision("bad.md", b"before\n===== BEGIN FILE x =====\n")
    except SystemExit:
        pass
    else:
        sys.exit("ABORT: delimiter collision selftest did not fail")
    print("selftest passed")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--build-date", help="YYYY-MM-DD, stamped into generated files")
    parser.add_argument("--selftest", action="store_true")
    args = parser.parse_args()
    if args.selftest:
        selftest()
        return
    if args.build_date:
        build(args.build_date)
        return
    parser.error("pass --selftest or --build-date YYYY-MM-DD")


if __name__ == "__main__":
    main()
