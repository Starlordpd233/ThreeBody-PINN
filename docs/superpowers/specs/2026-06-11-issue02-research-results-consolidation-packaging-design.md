---
status: active
purpose: other
created: 2026-06-11
milestone: v1.5
phase: 23-research-package-assembly
retirement_trigger: consolidation_input/ bundles delivered, consolidation-agent prompt revision applied, and the final resolution doc produced from them
---

# Design — Issue-02 Research-Results Consolidation Packaging (Bundle + In-Prompt Crosswalk)

**Approved by user 2026-06-11** (brainstorming session; Approach C variant with crosswalk
embedded in the prompt instead of a second file, and anonymized report tags).

## Problem

Stage 2 of the v1.5 external research pipeline hands a final consolidation agent (an external
web AI) the Stage-1 research reports plus supporting materials. The current attach list in
`docs/work/plans/milestone_v1.5/23-research-package-assembly/2026-06-10-phase-23-issue-02-consolidation-agent-prompt.md`
totals 15 files (RESEARCH-CONTEXT-MASTER.md + 5 `specs/` snapshots + 8 reports +
DATA-07 addendum). The user's upload budget is **6–7 files max** per conversation; individual
files may be large. The 8 reports total ~491 KB and all answer the same 14 framed questions
(Q-A1..A6, Q-B1..B4, Q-C1..C4 from `RESEARCH-CONTEXT-MASTER.md` §"Framed Research Questions").

## Decisions (locked by user approval)

1. **Verbatim bundling, not restructuring.** Reports are concatenated byte-verbatim into one
   bundle file with delimiters; no per-issue regrouping, no content edits.
2. **Crosswalk lives in the prompt**, not in a second uploaded file: compact per-cluster tables
   mapping each of the 14 questions to each report's decision-matrix verdict gist + locator.
3. **Anonymize reports** as `R1`–`R8` in the bundle and crosswalk; the tag→filename mapping is
   recorded only in the in-repo manifest (never uploaded).
4. **Originals stay untouched and authoritative** in `research_results/`; all bundle artifacts
   are derived.
5. **Final upload set (4 files):** `RESEARCH-CONTEXT-MASTER.md`, `specs-bundle.md`,
   `research-results-bundle.md`, `DATA-07-CORRECTION-ADDENDUM.md`.

## Artifacts

New directory:
`pinn_instruction/markdown_conversion/framework-revisions/research_reports/02-data-pipeline-and-validation/consolidation_input/`

| Artifact | Content |
|---|---|
| `research-results-bundle.md` | Generated header + TOC, then the 8 reports byte-verbatim, each wrapped in delimiters |
| `specs-bundle.md` | Same treatment for the 5 `research_package/specs/` snapshot files (not anonymized — spec filenames are meaningful and carry no model identity) |
| `make_bundles.py` | Deterministic builder + self-verification (see below) |
| `BUNDLE-MANIFEST.md` | Per-source: original filename, R-tag (reports only), byte count, SHA-256; build date; self-identification scan results; the committed evidence for the byte-preservation claim |

### Bundle format

- Header block: title, build date, derived-artifact notice ("originals in `research_results/`
  govern; this file is a packaging artifact"), and a TOC listing each section.
  - Research bundle TOC shows **R-tags only** (tag, byte count) — no filenames, no model names.
  - Specs bundle TOC shows filenames.
- Delimiters (plain visible text, one line each):
  - `===== BEGIN REPORT R<n> (<bytes> bytes, sha256 <first-12-hex>) =====`
  - `===== END REPORT R<n> =====`
  - Specs bundle uses `BEGIN FILE <filename>` / `END FILE <filename>`.
- R-tag assignment: alphabetical by original filename → R1..R8. Deterministic; opaque to the
  agent (it never sees the filenames).
- Content between delimiters is byte-identical to the source file.

### `make_bundles.py` behavior

1. Read the 8 report files and 5 spec files from their canonical locations.
2. **Delimiter-collision check:** assert no source file contains a line starting with `===== `;
   abort with a clear message if one does (then choose a longer delimiter and update this spec).
3. Emit both bundles.
4. **Self-verification:** re-read each emitted bundle, split on delimiters, SHA-256 each
   extracted body, compare against the source files' hashes; abort on any mismatch.
5. Print the manifest table (tag, filename, bytes, sha256) for `BUNDLE-MANIFEST.md`.
6. **Self-identification scan:** case-insensitive search of each report body for model/vendor
   names (chatgpt, gpt, openai, gemini, google, kimi, moonshot, glm, zhipu, fable, claude,
   anthropic); report match counts per file into the manifest. Anonymization is best-effort at
   the packaging layer — verbatim bodies may self-identify, and the manifest records honestly
   where they do. No content is scrubbed.

No randomness, no timestamps inside the bundles other than the build date passed explicitly.

## Crosswalk (embedded in the consolidation prompt)

- Three markdown tables, one per cluster (A: 6 rows, B: 4, C: 4). Rows = question IDs with
  their issue aliases (e.g. `Q-A1 (B-06)`). Columns = `R1`..`R8`.
- Cell = verdict gist of **≤ 8 words drawn from that report's own decision-matrix wording**,
  plus report-internal locator, e.g. `gate before training (§3.1)`.
- Coverage markers: `matrix-only (§n)` where a report has a decision-matrix row but no full
  resolution section (known case: the shortest report covers Q-A6..Q-C4 matrix-only); `—` where
  a question is entirely unaddressed.
- Legend above the tables: one line per R-tag (byte count, structural note such as
  "decision-matrix + per-cluster sections"); no model identity.
- Mandatory framing text (verbatim, part of the prompt):
  > Navigation aid only, transcribed from each report's decision matrix by the project.
  > Non-authoritative: the full report text in the bundle prevails over this table. Do not
  > treat it as evidence or as your agreement classification — perform Method step 2 yourself
  > from the full text.

### Crosswalk generation and verification

1. Main agent extracts each report's decision matrix and writes the cells.
2. **One verification subagent per report** independently checks every cell of that report's
   column: (a) the gist is a faithful compression of the matrix verdict, (b) the locator points
   at the right section, (c) coverage markers are correct. Subagents return findings; the main
   agent fixes and re-verifies changed cells.
3. Disagreements a verifier cannot resolve (e.g. a matrix verdict too ambiguous to compress
   faithfully) are not papered over: the cell falls back to locator-only (`see §n`), which is
   always safe.

## Consolidation-prompt revision (in place, structure preserved)

File: `docs/work/plans/milestone_v1.5/23-research-package-assembly/2026-06-10-phase-23-issue-02-consolidation-agent-prompt.md`

1. **Operator notes — "What to attach":** replace with the 4-file upload set; point to
   `consolidation_input/`; note the DATA-07 addendum has shipped (attach up front), keeping the
   forwarding sentence for any post-attach addendum updates (e.g. Phase-24 rerun remediation).
2. **Operator notes:** add a line that `BUNDLE-MANIFEST.md` holds the R-tag → report mapping
   and is deliberately NOT uploaded (de-reference provenance after the output lands).
3. **Inputs §:** describe the two bundles (what they contain, delimiter format, that the
   research bundle's TOC enumerates R1–R8).
4. **New section after Inputs:** "Report coverage and verdict crosswalk (navigation aid)" —
   legend + three tables + framing text per the spec above.
5. **Method step 1:** add one sentence — the crosswalk may be used to locate each report's
   position, never to replace reading it.
6. **Output spec header inventory:** reports are identified by bundle tag (R1–R8).
7. Frontmatter: bump nothing structurally; note the revision date in the operator notes.

## Verification summary (what "done" requires)

- `make_bundles.py` self-verification passes (hash round-trip for all 13 sections).
- `BUNDLE-MANIFEST.md` committed with hashes, byte counts, R-tag mapping, and
  self-identification scan results (git protocol: invariant evidence in committed state).
- Crosswalk verification subagents have signed off every column (or ambiguous cells demoted to
  locator-only).
- Revised prompt renders the crosswalk tables correctly and its attach list matches the actual
  files in `consolidation_input/`.
- Originals in `research_results/` and everything in `research_package/` are byte-identical to
  before (no diff).

## Out of scope

- No edits to the 8 reports, the issue doc, `research_package/`, or any framework spec.
- No per-issue restructuring of report content (rejected as Approach B: verification burden
  outweighs convenience).
- No change to where the final resolution doc lands or to the Phase 25–29 gate (operator notes
  already cover both).
