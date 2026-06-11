---
status: active
purpose: other
created: 2026-06-11
milestone: v1.5
phase: 23-research-package-assembly
execution_status: executed
executed_at: 2026-06-11T19:30:00+08:00
review_status: pending
retirement_trigger: all tasks executed and committed; consolidation_input/ delivered and prompt revision applied
---

# Issue-02 Consolidation Packaging Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Package the 8 Issue-02 Stage-1 research reports into a hash-verified anonymized bundle (plus a specs bundle), and revise the Stage-2 consolidation-agent prompt with a verified 14-question verdict crosswalk, so the whole upload set fits in 4 files.

**Architecture:** A deterministic Python script builds two byte-verbatim bundles with collision-checked delimiters and self-verifies by re-splitting and SHA-256-comparing every section against its original; it also writes the evidence manifest. The crosswalk is drafted by extracting only each report's decision-matrix section (never full reports into context), embedded directly into the existing prompt file, then verified column-by-column by 8 parallel subagents before commit.

**Tech Stack:** Python 3 stdlib (hashlib, re, pathlib), bash, git via `scripts/agent-commit`, Claude subagents for verification.

**Spec:** `docs/superpowers/specs/2026-06-11-issue02-research-results-consolidation-packaging-design.md` (approved 2026-06-11). Read it before starting.

---

## Execution context (read first)

- Repo: `<home>/Desktop/3_body_problem`, branch `milestone/v1.5`. Run `git status --short --branch` at session start per repo protocol; pre-existing changes (`.understand-anything/`, `.planning/`) are other sessions' — never stage them.
- Commits: NEVER raw `git commit`. Always `GIT_AGENT_ID="Claude Code (claude-fable-5)" scripts/agent-commit -m "..."`, message per `docs/git-guidelines.md`, body + `Agent-Assisted-By: Claude Code (claude-fable-5)` trailer required for every commit in this plan.
- `BASE` below means `pinn_instruction/markdown_conversion/framework-revisions/research_reports/02-data-pipeline-and-validation`.
- **Do not modify** anything under `BASE/research_results/` or `BASE/research_package/`. Never load a full report file into context (they total ~491 KB) — use the targeted extraction commands given below.
- **Governance (v1.5 STOP protocol):** the crosswalk cell vocabulary is exactly four forms (defined in Task 3). If a report's structure makes those four forms inapplicable (e.g., no identifiable decision matrix and no identifiable resolution sections), STOP and surface to the user — do not invent a new marker or schema.

### File structure

| File | Action | Responsibility |
|---|---|---|
| `BASE/consolidation_input/make_bundles.py` | Create | Build bundles, self-verify, write manifest |
| `BASE/consolidation_input/research-results-bundle.md` | Generate | 8 reports verbatim, anonymized R1–R8 |
| `BASE/consolidation_input/specs-bundle.md` | Generate | 5 spec snapshots verbatim |
| `BASE/consolidation_input/BUNDLE-MANIFEST.md` | Generate | Hashes, R-tag mapping, self-ID scan (committed evidence; never uploaded) |
| `docs/work/plans/milestone_v1.5/23-research-package-assembly/2026-06-10-phase-23-issue-02-consolidation-agent-prompt.md` | Modify | Attach list, Inputs, crosswalk section, Method/inventory tweaks |

### Expected R-tag mapping (alphabetical by filename — cross-check against the generated manifest)

| Tag | File | Bytes |
|---|---|---|
| R1 | chatgpt-plus-resolution.md | 58,143 |
| R2 | chatgpt-pro-deep-research-resolution.md | 54,675 |
| R3 | chatgpt-pro-resolution.md | 69,695 |
| R4 | fable-5-resolution.md | 125,805 |
| R5 | gemini-deep-research-max-resolution.md | 15,806 |
| R6 | gemini-deep-research-resolution.md | 51,878 |
| R7 | glm-resolution.md | 57,260 |
| R8 | kimi-resolution.md | 58,087 |

R5 is the known matrix-only-heavy report: full resolution sections exist only for Q-A1..Q-A5; Q-A6..Q-C4 appear in its decision matrix only.

R6's decision matrix is keyed by issue IDs only (B-06, B-11, M11, M12, M13, D7, M16, "Seed
Conflict") — it never received the framed-questions catalog, and Q-IDs appear nowhere in the
report. The six alias-backed rows map mechanically via the crosswalk's own parentheticals:
B-06→Q-A1, B-11→Q-A2, M11→Q-A3, M13→Q-A4, D7→Q-A5, M12→Q-B1. The remaining mappings are NOT
pre-decided: whether "Seed Conflict (SCS Thresholds)" §3.8 fills Q-C1, whether M16 §3.7 maps
to any crosswalk row, and Q-B2..Q-B4 coverage — for these, STOP and surface to the user per
the governance note above; do not infer.

---

### Task 1: Bundle builder script with self-test

**Files:**
- Create: `BASE/consolidation_input/make_bundles.py`

- [ ] **Step 1: Create the directory and write the script**

```bash
mkdir -p "pinn_instruction/markdown_conversion/framework-revisions/research_reports/02-data-pipeline-and-validation/consolidation_input"
```

Write `make_bundles.py` with exactly this content (Write tool):

```python
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
```

- [ ] **Step 2: Run the self-test**

```bash
cd "pinn_instruction/markdown_conversion/framework-revisions/research_reports/02-data-pipeline-and-validation/consolidation_input" && python3 make_bundles.py --selftest
```

Expected output (exactly these three lines):
```
verified bundle.md: 3 sections round-trip byte-exact
collision detection: OK
selftest passed
```
(The self-test exercises: round-trip byte-exactness including a file without trailing newline and one with multi-byte UTF-8, plus the negative path — collision detection must abort.) If it fails, fix the script before proceeding; do not weaken an assertion to make it pass.

- [ ] **Step 3: Commit**

```bash
cd <home>/Desktop/3_body_problem && \
git add "pinn_instruction/markdown_conversion/framework-revisions/research_reports/02-data-pipeline-and-validation/consolidation_input/make_bundles.py"
GIT_AGENT_ID="Claude Code (claude-fable-5)" scripts/agent-commit -m "feat(23): add consolidation bundle builder with self-verification

Deterministic builder for the Issue-02 Stage-2 upload bundles: byte-verbatim
concatenation with collision-checked delimiters, R1-R8 anonymization for
reports, SHA-256 round-trip self-verification, manifest generation with
self-ID scan. Selftest passes (round-trip incl. no-trailing-newline and
multi-byte UTF-8 fixtures; negative collision path).

Agent-Assisted-By: Claude Code (claude-fable-5)"
```

---

### Task 2: Build the real bundles and commit the evidence

**Files:**
- Generate: `BASE/consolidation_input/research-results-bundle.md`, `specs-bundle.md`, `BUNDLE-MANIFEST.md`

- [ ] **Step 1: Run the real build** (substitute today's date)

```bash
cd "pinn_instruction/markdown_conversion/framework-revisions/research_reports/02-data-pipeline-and-validation/consolidation_input" && python3 make_bundles.py --build-date 2026-06-11
```

Expected output: two `verified … round-trip byte-exact` lines (8 sections and 5 sections) followed by the `wrote …` summary line. Any `ABORT:` line means stop and investigate — do not hand-edit bundle output.

- [ ] **Step 2: Spot-check without loading bundles into context**

```bash
cd "pinn_instruction/markdown_conversion/framework-revisions/research_reports/02-data-pipeline-and-validation/consolidation_input" && \
grep -c "^===== BEGIN REPORT" research-results-bundle.md && \
grep -c "^===== BEGIN FILE" specs-bundle.md && \
head -20 research-results-bundle.md && \
git status --short -- ../research_results ../research_package
```

Expected: `8`, then `5`, then the bundle header (title, derived-artifact notice, Contents table with R1–R8 and byte counts, no filenames or model names), then **no `M`/`D`/`A` entries** for the two source directories (originals untouched; a pre-existing `?? …/research_results/` line is expected — the Stage-1 reports are not yet committed — and counts as pass). Also open `BUNDLE-MANIFEST.md` (it is small) and confirm the R-tag mapping matches the table in this plan's header.

- [ ] **Step 3: Commit bundles + manifest**

```bash
cd <home>/Desktop/3_body_problem && \
git add "pinn_instruction/markdown_conversion/framework-revisions/research_reports/02-data-pipeline-and-validation/consolidation_input/research-results-bundle.md" \
        "pinn_instruction/markdown_conversion/framework-revisions/research_reports/02-data-pipeline-and-validation/consolidation_input/specs-bundle.md" \
        "pinn_instruction/markdown_conversion/framework-revisions/research_reports/02-data-pipeline-and-validation/consolidation_input/BUNDLE-MANIFEST.md" && \
git diff --cached --stat && git diff --check
GIT_AGENT_ID="Claude Code (claude-fable-5)" scripts/agent-commit -m "docs(23): build issue-02 consolidation input bundles and manifest

Derived upload artifacts for the Stage-2 consolidation agent: eight Stage-1
reports byte-verbatim as anonymized R1-R8, five spec snapshots byte-verbatim,
4-file upload set total. Byte-for-byte preservation verified by SHA-256
round-trip at build time; per-section hashes, R-tag mapping, and self-ID scan
recorded in BUNDLE-MANIFEST.md (committed evidence; never uploaded). Originals
in research_results/ and research_package/ unchanged.

Agent-Assisted-By: Claude Code (claude-fable-5)"
```

---

### Task 3: Revise the consolidation prompt and draft the crosswalk

**Files:**
- Modify: `docs/work/plans/milestone_v1.5/23-research-package-assembly/2026-06-10-phase-23-issue-02-consolidation-agent-prompt.md`

Do NOT commit in this task — the commit happens in Task 5 after column verification.

- [ ] **Step 1: Extract every report's decision matrix (targeted, not full files)**

```bash
cd "pinn_instruction/markdown_conversion/framework-revisions/research_reports/02-data-pipeline-and-validation/research_results" && python3 - <<'EOF'
import re, pathlib
for p in sorted(pathlib.Path('.').glob('*.md')):
    lines = p.read_text(encoding='utf-8').splitlines()
    heads = [(i, l) for i, l in enumerate(lines) if l.startswith('#')]
    start = next((i for i, l in heads if re.search(r'decision matrix', l, re.I)), None)
    if start is None:
        print(f'### {p.name}: NO DECISION MATRIX HEADING'); continue
    end = next((i for i, _ in heads if i > start), len(lines))
    print(f'### {p.name} (lines {start+1}-{end})')
    print('\n'.join(lines[start:end]))
EOF
```

If any report prints `NO DECISION MATRIX HEADING`, STOP and surface to the user (governance note in the header) — do not improvise an alternative source for that column.

- [ ] **Step 2: Build each report's heading map (for locators and legend)**

```bash
cd "pinn_instruction/markdown_conversion/framework-revisions/research_reports/02-data-pipeline-and-validation/research_results" && for f in *.md; do echo "=== $f ==="; grep -nE "^#" "$f"; done
```

- [ ] **Step 3: Apply the mechanical prompt edits** (Edit tool, exact pairs)

**Edit A — operator notes attach list.** Replace:

```
- **What to attach:**
  1. The full `research_package/` (same set as Stage 1: `RESEARCH-CONTEXT-MASTER.md` — the
     consolidated research-context master holding the manifest, framed questions, CLM claims
     register, dataset context, and correction provenance — plus all of `specs/`). The
     consolidator must be able to verify report positions against the primary materials, not
     consolidate hearsay.
  2. Every Stage-1 individual research report.
  3. The Phase 24 DATA-07 correction addendum, if it has shipped by then. If it has not, forward
     it mid-task the moment it does — the prompt tells the agent how to treat it.
```

with:

```
- **What to attach (4 files; bundles live in
  `research_reports/02-data-pipeline-and-validation/consolidation_input/`):**
  1. `research_package/RESEARCH-CONTEXT-MASTER.md` — the consolidated research-context master
     holding the manifest, framed questions, CLM claims register, dataset context, and
     correction provenance. The consolidator must be able to verify report positions against
     the primary materials, not consolidate hearsay.
  2. `consolidation_input/specs-bundle.md` — all five `research_package/specs/` snapshot
     files, byte-verbatim in one file with `===== BEGIN FILE <name> =====` delimiters.
  3. `consolidation_input/research-results-bundle.md` — all eight Stage-1 reports,
     byte-verbatim in one file, anonymized as R1–R8 with `===== BEGIN REPORT R<n> =====`
     delimiters.
  4. `research_package/DATA-07-CORRECTION-ADDENDUM.md` — shipped 2026-06-11; attach up front.
     If a further Phase-24 correction update lands mid-task, forward it the moment it does —
     the prompt tells the agent how to treat it.
- **Anonymization:** the R-tag → report-file mapping lives only in
  `consolidation_input/BUNDLE-MANIFEST.md`, which is deliberately NOT uploaded; de-reference
  report provenance there after the output lands. (Repo-side note: report bodies are verbatim
  and may self-identify — see the manifest's self-ID scan column; byte sizes in the uploaded
  bundle header are also distinguishing, R4 notably so — the prompt's Independence ground rule
  is the mitigation.)
- **Revision note (2026-06-11):** attach list rebundled to 4 files; reports anonymized R1–R8;
  crosswalk section added. Design:
  `docs/superpowers/specs/2026-06-11-issue02-research-results-consolidation-packaging-design.md`.
```

**Edit B — Inputs section.** Replace:

```
1. **The research package** — `RESEARCH-CONTEXT-MASTER.md` (its "Package Orientation And
   Manifest" section defines every file's role and authority level; its "Framed Research
   Questions" section is the complete question set; its "CLM Claims Register" and
   "Consolidated Dataset Context" sections carry the factual baseline) and the files under
   `specs/`.
2. **The independent research reports** — one per agent. Treat them as argued candidate
   positions, nothing more.
3. **Possibly a correction addendum** — empirically verified values for figures the package
   marked `claimed-unverified`. It may be provided up front or forwarded mid-task.

Read in this order: the master's manifest section → its question set → every report in full →
then the master's "CLM Claims Register" and "Consolidated Dataset Context" sections and
`specs/` as adjudication requires.
```

with:

```
1. **The research package** — `RESEARCH-CONTEXT-MASTER.md` (its "Package Orientation And
   Manifest" section defines every file's role and authority level; its "Framed Research
   Questions" section is the complete question set; its "CLM Claims Register" and
   "Consolidated Dataset Context" sections carry the factual baseline) and the spec snapshots
   inside `specs-bundle.md` (five files, each delimited by `===== BEGIN FILE <name> =====` /
   `===== END FILE <name> =====` lines).
2. **The independent research reports** — eight, inside `research-results-bundle.md`,
   anonymized as `R1`–`R8` and each delimited by `===== BEGIN REPORT R<n> … =====` /
   `===== END REPORT R<n> =====` lines; the bundle header's Contents table enumerates them.
   Treat them as argued candidate positions, nothing more.
3. **A correction addendum** — empirically verified values for figures the package marked
   `claimed-unverified`, provided up front. An updated version may be forwarded mid-task.

Read in this order: the master's manifest section → its question set → every report in the
bundle in full (R1–R8) → then the master's "CLM Claims Register" and "Consolidated Dataset
Context" sections and the `specs-bundle.md` contents as adjudication requires.
```

**Edit C — Method step 1.** Replace:

```
1. **Collect** each report's position on the question (including "not addressed").
```

with:

```
1. **Collect** each report's position on the question (including "not addressed"). The
   crosswalk section above may be used to locate positions quickly — never as a substitute
   for reading the report's full text.
```

**Edit D — output header inventory.** Replace:

```
- **Header:** title, date, and an inventory of inputs received: every package file and every
  report (identified by filename or label), plus whether a correction addendum was received.
```

with:

```
- **Header:** title, date, and an inventory of inputs received: every package file and every
  report (reports identified by bundle tag R1–R8), plus whether a correction addendum was
  received.
```

- [ ] **Step 4: Insert the crosswalk section**

Insert immediately after the (now-edited) "Read in this order…" paragraph of the Inputs section and before `## What consolidation means here`. Skeleton (every `_` cell MUST be replaced in Step 5; byte sizes shown are from this plan's R-tag table — cross-check against `BUNDLE-MANIFEST.md`; write each legend line's structural note from the heading maps, e.g. "§-numbered decision matrix, per-cluster resolutions, open-items register"):

```
## Report coverage and verdict crosswalk (navigation aid)

> Navigation aid only, transcribed from each report's decision matrix by the project.
> Non-authoritative: the full report text in the bundle prevails over this table. Do not
> treat it as evidence or as your agreement classification — perform Method step 2 yourself
> from the full text.

Legend (structure only; byte sizes are of the original report files):

- **R1** — 58 KB; <structural note>
- **R2** — 55 KB; <structural note>
- **R3** — 70 KB; <structural note>
- **R4** — 126 KB; <structural note>
- **R5** — 16 KB; <structural note>
- **R6** — 52 KB; <structural note>
- **R7** — 57 KB; <structural note>
- **R8** — 58 KB; <structural note>

Cell forms: `<verdict gist> (<section>)` — full resolution section exists there;
`matrix-only (<section>)` — covered only as a decision-matrix row at that section;
`—` — not addressed anywhere in the report; `see <section>` — verdict too nuanced to
compress faithfully, read the section.

### Cluster A — Ingestion & Selection

| Question | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 |
|---|---|---|---|---|---|---|---|---|
| Q-A1 (B-06) | _ | _ | _ | _ | _ | _ | _ | _ |
| Q-A2 (B-11) | _ | _ | _ | _ | _ | _ | _ | _ |
| Q-A3 (M11) | _ | _ | _ | _ | _ | _ | _ | _ |
| Q-A4 (M13) | _ | _ | _ | _ | _ | _ | _ | _ |
| Q-A5 (D7) | _ | _ | _ | _ | _ | _ | _ | _ |
| Q-A6 (D-03) | _ | _ | _ | _ | _ | _ | _ | _ |

### Cluster B — Sampling, Precision & Global Scale

| Question | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 |
|---|---|---|---|---|---|---|---|---|
| Q-B1 (M12) | _ | _ | _ | _ | _ | _ | _ | _ |
| Q-B2 | _ | _ | _ | _ | _ | _ | _ | _ |
| Q-B3 | _ | _ | _ | _ | _ | _ | _ | _ |
| Q-B4 | _ | _ | _ | _ | _ | _ | _ | _ |

### Cluster C — Validation Metrics

| Question | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 |
|---|---|---|---|---|---|---|---|---|
| Q-C1 (SCS) | _ | _ | _ | _ | _ | _ | _ | _ |
| Q-C2 (SASD) | _ | _ | _ | _ | _ | _ | _ | _ |
| Q-C3 (IPR) | _ | _ | _ | _ | _ | _ | _ | _ |
| Q-C4 (PSC) | _ | _ | _ | _ | _ | _ | _ | _ |
```

- [ ] **Step 5: Fill every cell** using the Step-1 matrices and Step-2 heading maps, under these rules:

1. **Gist:** at most 8 words, compressed from the report's OWN decision-matrix wording — same direction, keep qualifiers that change meaning ("conditional on X" must not become unconditional), no added precision the report didn't state.
2. **Locator:** the report's own most specific heading identifier for that question's full resolution — its section number/§ if the heading carries one, else the heading's literal Q-ID text (e.g. `(Q-A3)`).
3. **Coverage:** `matrix-only (<matrix section>)` only when the matrix covers the question but no fuller section exists (expected for R5 on Q-A6..Q-C4); `—` only when the question appears nowhere in the report.
4. **Fallback:** if a verdict cannot be compressed faithfully in 8 words, use `see <section>` — always safe, never wrong.
5. No `|` characters inside cells; no model/vendor names anywhere in the section.
6. Only these four cell forms exist. If none fits a situation, STOP and surface to the user (do not invent a fifth form).

- [ ] **Step 6: Shape-check the tables**

```bash
awk -F'|' '/^\|/ && NF != 11 {print FNR": "NF-2" columns: "$0}' "docs/work/plans/milestone_v1.5/23-research-package-assembly/2026-06-10-phase-23-issue-02-consolidation-agent-prompt.md"
```

Expected: no output (every table row has exactly 9 columns). Also confirm no fill-markers remain: `grep -nE "\| _ \||<structural note>" <same file>` must return nothing.

---

### Task 4: Verify every crosswalk column with parallel subagents

No file changes except fixes to the crosswalk cells. No commit yet.

- [ ] **Step 1: Dispatch 8 verification subagents in parallel** (one per report; single message, 8 Agent calls, `subagent_type: general-purpose`). Prompt template — substitute `<n>` and `<report path>`:

```
You are verifying one column of a navigation crosswalk against its source report. Work
read-only: do NOT edit any file.

Source report: <absolute path to BASE/research_results/<file>.md>
Your column: R<n> in the crosswalk tables of
<home>/Desktop/3_body_problem/docs/work/plans/milestone_v1.5/23-research-package-assembly/2026-06-10-phase-23-issue-02-consolidation-agent-prompt.md
(section "Report coverage and verdict crosswalk (navigation aid)").

Read your column's 14 cells (rows Q-A1..Q-A6, Q-B1..Q-B4, Q-C1..Q-C4), the R<n> legend
line, and the source report (its decision matrix and the sections the cells point at).
Check each cell:
a) GIST: a faithful <=8-word compression of the report's decision-matrix verdict for that
   question — same direction, no dropped qualifier that changes meaning, no added precision.
b) LOCATOR: the section identifier exists in the report and is where that question's full
   resolution lives.
c) COVERAGE: `matrix-only (<sec>)` only if the decision matrix covers it but no fuller
   section does; `—` only if the question appears nowhere; gist+locator only if a full
   resolution section exists; `see <sec>` is acceptable wherever the section is right.
d) LEGEND: the R<n> legend line's size and structural note are accurate and contain no
   model/vendor identity.

Return a compact list: one line per row — `Q-xN: OK` or `Q-xN: ISSUE — <what is wrong> —
suggested cell: <replacement>`. If a verdict is too ambiguous to compress faithfully,
suggest `see <sec>`. End with `LEGEND: OK` or `LEGEND: ISSUE — <fix>`.
```

- [ ] **Step 2: Apply fixes.** For every ISSUE, replace the cell with the suggested form (Edit tool), keeping the four-form vocabulary. If a verifier reports something outside that vocabulary or a structural surprise (e.g., decision matrix missing), STOP and surface to the user.

- [ ] **Step 3: Re-verify changed cells.** Dispatch ONE follow-up subagent with the same template, restricted to the changed rows/columns (list them explicitly in the prompt). Repeat fix→re-verify until all OK. Re-run the Task 3 Step 6 shape-check after any edit.

---

### Task 5: Final sweep and commit the prompt revision

- [ ] **Step 1: Attach-list ↔ filesystem consistency**

```bash
cd "pinn_instruction/markdown_conversion/framework-revisions/research_reports/02-data-pipeline-and-validation" && \
ls consolidation_input/research-results-bundle.md consolidation_input/specs-bundle.md \
   research_package/RESEARCH-CONTEXT-MASTER.md research_package/DATA-07-CORRECTION-ADDENDUM.md
```

Expected: all four paths print (the 4-file upload set named in the prompt exists exactly).

- [ ] **Step 2: Source-integrity re-check**

```bash
git status --short -- "pinn_instruction/markdown_conversion/framework-revisions/research_reports/02-data-pipeline-and-validation/research_results" "pinn_instruction/markdown_conversion/framework-revisions/research_reports/02-data-pipeline-and-validation/research_package"
```

Expected: no `M`/`D`/`A` entries (originals byte-identical to before; a pre-existing `?? …/research_results/` line is expected — the Stage-1 reports are not yet committed — and counts as pass).

- [ ] **Step 3: Review the full prompt diff**

```bash
git diff -- "docs/work/plans/milestone_v1.5/23-research-package-assembly/2026-06-10-phase-23-issue-02-consolidation-agent-prompt.md" | head -250
```

Confirm: only Edits A–D and the crosswalk section; operator-notes "Where the output goes" and "Gate" untouched; framing blockquote present verbatim; `git diff --check` clean.

- [ ] **Step 4: Commit**

```bash
cd <home>/Desktop/3_body_problem && \
git add "docs/work/plans/milestone_v1.5/23-research-package-assembly/2026-06-10-phase-23-issue-02-consolidation-agent-prompt.md"
GIT_AGENT_ID="Claude Code (claude-fable-5)" scripts/agent-commit -m "docs(23): revise consolidation agent prompt for bundled inputs and crosswalk

Attach list rebundled to the 4-file upload set (master, specs bundle,
anonymized R1-R8 research bundle, DATA-07 addendum); Inputs section describes
bundle delimiters; new non-authoritative 14-question verdict crosswalk
(navigation aid) added after Inputs, every column verified by an independent
subagent against its source report; Method step 1 and output inventory updated
for R-tags. R-tag mapping stays repo-side in BUNDLE-MANIFEST.md.

Agent-Assisted-By: Claude Code (claude-fable-5)"
```

- [ ] **Step 5: Mark this plan executed** — set `execution_status: executed`, add `executed_at: <date and time>` and `review_status: pending` to this plan's frontmatter, and close per `docs/README.md` (dedicated commit with `Plan-Execution:` and `Plan-Source:` trailers, separate from the work commits above).

---

## Done means

- `make_bundles.py --selftest` and the real build both pass; bundles + manifest committed with per-section SHA-256 recorded.
- Crosswalk: 14 × 8 cells, all four-form vocabulary, every column subagent-verified, no `_` left, tables shape-clean.
- Prompt names exactly the 4 files that exist on disk; originals untouched (`git status` clean for both source dirs).
- The user can upload 4 files and paste nothing extra: the crosswalk travels inside the prompt.
