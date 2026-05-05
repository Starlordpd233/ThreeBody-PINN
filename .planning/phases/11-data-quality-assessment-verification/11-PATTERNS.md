# Phase 11: Data-Quality-Assessment Verification - Pattern Map

**Mapped:** 2026-05-05
**Files analyzed:** 5 (3 created, 2 modified — counting `data_quality_assessment.md` move-target as create)
**Analogs found:** 5 / 5 (100% coverage — all analogs are Phase 10 outputs)

## File Classification

| New/Modified File | Role | Data Flow | Closest Analog | Match Quality |
|-------------------|------|-----------|----------------|---------------|
| `pinn_instruction/markdown_conversion/verification_reports/data_quality_assessment_verification_report.md` | documentation/report | document-build (skeleton → fill across 3 plans) | `pinn_instruction/markdown_conversion/verification_reports/ctl_instruction_verification_report.md` | exact |
| `pinn_instruction/markdown_conversion/data_quality_assessment.md` | documentation/authoritative-markdown | move + section-scoped edit | `pinn_instruction/markdown_conversion/ctl_instruction.md` | exact |
| `pinn_instruction/markdown_conversion/_archive/data-quality-assessment/README.md` | documentation/archive-provenance | static metadata file | `pinn_instruction/markdown_conversion/_archive/ctl-instruction/README.md` | exact |
| `pinn_instruction/markdown_conversion/_archive/data-quality-assessment/<unselected>.md` | archived asset | `git mv` (no edit) | `pinn_instruction/markdown_conversion/_archive/ctl-instruction/CTL-instruction-final.md` | exact |
| `pinn_instruction/markdown_conversion/README.md` (modify — append row) | documentation/index | row-append | `pinn_instruction/markdown_conversion/README.md` (existing CTL row) | exact |

All five new/modified files have an exact Phase 10 analog. There are no files in Phase 11 scope without a Phase 10 precedent. The Phase 10 directory layout is the canonical template for Phase 11.

---

## Pattern Assignments

### `verification_reports/data_quality_assessment_verification_report.md` (documentation/report, document-build)

**Analog:** `pinn_instruction/markdown_conversion/verification_reports/ctl_instruction_verification_report.md`

**Top-level structure** (full file is the template — sections in order):

1. `# <Document> Markdown Verification Report` (H1 title)
2. `## <Document> Candidate Comparison` — scoring methodology paragraph + comparison table
3. `## Selected Baseline` — bullet list (selected, promoted target, rationale, override flag, promotion action)
4. `## Excluded Comment Ranges` — table OR explicit "None" prose
5. `## Section Audit` — one `### <filename>.tex - <Section Title>` subsection per active source `.tex`
6. `## Fix Log` — single accumulated table
7. `## Source Issues / Notes for Future Reconciliation` — table (or "(none)" entry)
8. `## Final Verification` — bullet list of zero-discrepancy assertions

**Plan ownership:**
- Plan 01 creates skeleton with sections 1–4 populated and 5–8 stubbed.
- Plan 02 populates section 5 (Section Audit) and appends to section 6 (Fix Log).
- Plan 03 finalizes sections 7 and 8.

**Candidate Comparison table pattern** (lines 5–11 of analog):

```markdown
Scoring normalized whitespace, line wrapping, escaped underscores, URI escaping, and harmless Markdown punctuation. Scores do not normalize away formula changes, table-cell changes, label/reference loss, missing prose, added prose, heading drift, or omitted visible `\authcomment{...}` text.

| Candidate | Overall score | Rank | Per-section score summary | Human inspection notes |
|---|---:|---:|---|---|
| `pinn_instruction/markdown_conversion/<file>.md` | 0.XXX F1 / 0.XXX recall | N raw / N selected | 01: 1.000 recall; 02: 0.XXX; 03: 0.XXX; ... | <one-line rationale> |
```

Phase 11 adjustment: replace the "omitted visible `\authcomment{...}` text" clause with "injected `[@refN]`/`[?]` citations and trailing reference list" because that is the relevant non-normalizable category for this source.

**Selected Baseline pattern** (lines 13–19 of analog):

```markdown
## Selected Baseline

- Selected candidate: `pinn_instruction/markdown_conversion/<path>.md`
- Promoted target: `pinn_instruction/markdown_conversion/data_quality_assessment.md`
- Selection rationale: <one or two sentence rationale citing both raw score and human sanity-check>
- Override used: yes|no
- Promotion action: <e.g., `git mv pandoc_conversion/data_quality_assess.md data_quality_assessment.md`>
```

**Excluded Comment Ranges pattern** (lines 21–29 of analog):

Phase 10 used a 5-row table for actual ranges. Phase 11's source has zero comment environments, so the section becomes a short prose paragraph (per RESEARCH.md line 236):

```markdown
## Excluded Comment Ranges

None — source has no `\begin{comment}` environments. `bibliography.tex` is orphaned (never imported by `main-data-quality-assess.tex`) and excluded entirely; not part of the audit corpus.
```

**Section Audit subsection pattern** (lines 33–55 of analog, repeating per `.tex` file):

```markdown
### <source>.tex - <Section Title from \section{...}>

Status: PASS

| ID | Type | Severity | Source location | Markdown location | Issue | Fix status |
|---|---|---|---|---|---|---|
| DQA-NN-NNN | <type> | <severity> | `<source>.tex:LL-LL` | `data_quality_assessment.md:LL-LL` | <one-sentence issue> | Fixed | No fix needed | Verified |
```

Optional supplementary tables that may follow the discrepancy table (use exactly the headers Phase 10 used):

- **Formula checklist** (use for §1 introduction.tex with 1 equation and §3 data_quality_metrics.tex with 5 equations — pattern from analog lines 82–90):

```markdown
| Formula ID | Source location | Markdown location | Status | Notes |
|---|---|---|---|---|
| <name or anchor> | `<source>.tex:LL-LL` | `data_quality_assessment.md:LL-LL` | PASS | <preservation note> |
```

- **Generic check items** (pattern from analog lines 51–55, 65–70, 92–96):

```markdown
| Check item | Source location | Markdown location | Status | Notes |
|---|---|---|---|---|
| <description> | `<source>.tex:LL-LL` | `data_quality_assessment.md:LL-LL` | PASS | <one-line note> |
```

**Discrepancy ID convention** (per A5 of RESEARCH.md): `DQA-NN-NNN` where `NN` = section number (01–06), `NNN` = sequential within that section. Source-issue IDs use `SI-DQA-NNN`. Plan 01 baseline-creation entry uses the form `DQA-10-01-BASELINE` (mirroring Phase 10's `CTL-10-01-BASELINE`, analog line 160).

Severity values are exactly: `BLOCKING`, `MAJOR`, `MINOR`, `INFO`.

Type values used by Phase 10: `text`, `table`, `comment`, `figure`, `structure`. Phase 11 adds two values: `citation` (for `[@refN]`/`[?]` injections) and `table-corruption` (sub-type of `table` for HTML cell-merge). Reuse Phase 10 values where applicable.

**Fix Log pattern** (analog lines 156–170):

```markdown
## Fix Log

| ID | Section | Fix summary |
|---|---|---|
| DQA-10-01-BASELINE | Candidate selection | Created candidate comparison, selected `<file>`, and recorded comment-exclusion vacuous-satisfaction note. |
| DQA-NN-NNN | `<source>.tex` | <one-sentence past-tense fix description> |
```

**Source Issues pattern** (analog lines 172–176):

```markdown
## Source Issues / Notes for Future Reconciliation

| ID | Source section | Markdown heading | Note |
|---|---|---|---|
| SI-DQA-NNN | `<source>.tex` | `<heading text>` | <preservation + reconciliation note> |
```

If no source-level concerns are identified, replace the table body with one row: `| — | — | — | (none — no source-level mathematical, factual, or methodological concerns identified during section audit) |` — or follow Open Question #3 in RESEARCH.md and write a single-paragraph "(none)" stub. Phase 10 always populated the table; preferring the "(none)" row over omitting the section keeps the structure consistent.

**Final Verification pattern** (analog lines 178–183):

```markdown
## Final Verification

- Open discrepancies: 0
- Zero open discrepancies: yes
- Converted body excludes appended source-issue metadata from fidelity comparison: yes
- Fix log complete: yes
```

These four bullets are verbatim — no rewording.

---

### `data_quality_assessment.md` (documentation/authoritative-markdown, move + section-scoped edit)

**Analog:** `pinn_instruction/markdown_conversion/ctl_instruction.md`

**File-creation mechanism:** `git mv <selected-candidate> data_quality_assessment.md`. The file content is the selected candidate after Plan 02's edits. Phase 10 did not have to move the selected file because the existing target already occupied the authoritative path; Phase 11 will move it because both candidates currently live elsewhere.

**Top-of-file pattern** (analog lines 1–7) — **conditional**:

If the pandoc candidate wins (likely), the existing pandoc front-matter style is YAML between `---` fences. Compare to Phase 10:

```markdown
---
author:
- Starlordpd233
date: June 2025
title: Final CTL Instruction on Training PINNs for the Three-Body
  Problem
---

# <First section heading from source>
```

Phase 11 should preserve whatever the candidate emitted — do **not** invent front matter not present in the LaTeX source. The current pandoc candidate (`pandoc_conversion/data_quality_assess.md:1`) starts directly with `# Introduction: ...` (no front matter); the top-level candidate may also lack front matter. Either is acceptable; do not add Phase 10's YAML block.

**Heading hierarchy convention** (analog lines 9, 17, 19, 44, …):

- LaTeX `\section{...}` → markdown `# ` (H1) — there are 6 of these in the data-quality-assessment source.
- LaTeX `\subsection{...}` → markdown `## ` (H2).
- LaTeX `\subsubsection{...}` → markdown `### ` (H3).
- LaTeX `\paragraph{...}` → markdown bold paragraph or `#### ` (H4) — choose the convention used by the surviving candidate; do not mix within one file.

**Math display convention** (analog lines 25, and inline preserved widely):

- Inline math: `$...$` (e.g., analog line 25 `$1\text{e-}15$`).
- Display math: `$$...$$` on its own line, or LaTeX-anchored block. Phase 10 preferred inline `$$ $$` over `\[ \]` brackets when the pandoc candidate emitted brackets; check what the chosen Phase 11 candidate uses and keep it consistent.

**Label preservation pattern** (analog line 21):

The data-quality-assessment source has exactly one `\label`: `tab:assessment_strategies`. Phase 10's pattern for table labels was an HTML anchor immediately above the table:

```markdown
<a id="tab:assessment_strategies"></a>

| Feature | Pre-Training Validation (Static) | Trial Training (Dynamic) | Staged Gate Protocol (Hybrid) |
|---|---|---|---|
| ... | ... | ... | ... |

*Table `tab:assessment_strategies`: Comparative Analysis of Assessment Strategies.*
```

The label is also visible in the caption (analog line 30: `*Table \`tab:brutus_compare\`: ...*`). Reuse both — anchor above for navigability, label in caption text for reader visibility.

**GFM table pattern** (analog lines 23–28):

```markdown
| <header1>           | <header2>            | <header3>            |
|---|---|---|
| <cell> | <cell> | <cell> |
| **<bold-row-label>** | <cell> | <cell> |
```

Header separator row `|---|` (no alignment colons) for left-aligned, `|---:|` for right-aligned numbers (used by Phase 10 for numeric columns). Match the analog: bold the row labels (`**Primary Metric**`, etc.) when the row label is the leftmost column. The five row labels in Phase 11's table are: `Primary Metric`, `Computational Cost`, `Detects`, `Risk Addressed`, `Blind Spot` (RESEARCH.md authoritative cell content, lines 348–361).

**Trailing Source Issues section pattern** (analog lines 1233–1242):

```markdown
# Source Issues / Notes for Future Reconciliation

These notes are metadata for future reconciliation. They are not part of the converted source body and are excluded from fidelity comparison in `data_quality_assessment_verification_report.md`.

## SI-DQA-NNN: <short title>

- Source sections: `<file>.tex`<, `<file>.tex`>.
- Markdown headings: `<heading text>`<, `<heading text>`>.
- Note: <one-paragraph reconciliation note>.
```

Use `# ` (H1) for the metadata section heading — Phase 10 did this so the section is structurally distinct from the source body's H1 sections. If no concerns are identified, write a single short subsection with title `SI-DQA-000: No source-level concerns identified` and a one-line note (per RESEARCH.md Open Question #3).

**Section ordering inside the body** — fixed by source, not by analog:

```
1. introduction.tex          → # Introduction: ...
2. assessment_strategy.tex   → # Assessment Strategy: ...     (contains the single table at \label{tab:assessment_strategies})
3. data_quality_metrics.tex  → # Data Quality Metrics ...     (contains 5 equations; heaviest math)
4. model_parameter_risks.tex → # Model Parameter Risks ...
5. implementation_protocol.tex → # Implementation Protocol ...
6. synthesis_conclusion.tex  → # Synthesis and Conclusion ...
[appended] # Source Issues / Notes for Future Reconciliation
```

---

### `_archive/data-quality-assessment/README.md` (documentation/archive-provenance, static metadata)

**Analog:** `pinn_instruction/markdown_conversion/_archive/ctl-instruction/README.md` (full file is the template — 11 lines)

**Full template** (lines 1–11 of analog, with Phase 11 substitutions):

```markdown
# Data Quality Assessment Candidate Archive

## Candidate provenance

The authoritative Data-Quality-Assessment markdown for Phase 11 is `../../data_quality_assessment.md`. Selection rationale and final verification details are documented in `../../verification_reports/data_quality_assessment_verification_report.md`.

| Archived file | Original path | Score/rank | Disposition | Reason |
|---|---|---|---|---|
| `<unselected>.md` | `pinn_instruction/markdown_conversion/<original-path>` | 0.XXX F1 / rank N | Archived unselected candidate | <one-line reason — e.g., HTML table corruption + 33 `[?]` placeholder citations + corrupted heading hierarchy at 16+ locations>. |
```

**Differences from analog:**
- Phase 10's verification report path was `../../ctl_instruction_verification_report.md` (no `verification_reports/` subdirectory at the time the README was first written). Phase 11 must use `../../verification_reports/data_quality_assessment_verification_report.md` per CONTEXT.md D-31.
- Phase 10 archived **two** unselected candidates (so the table has two rows). Phase 11 has **one** unselected candidate, so the table has exactly one row.
- The "Reason" column is one-line free text. Phase 10 examples: "Lower source recall in sections 03-05 and noisy heading hierarchy from code comments." and "Narrow raw F1 lead was overridden because the existing target had better recall in section 04 and appendix figure preservation." Phase 11 should use a similar one-liner that names the dominant defect (HTML table corruption / disconnected reference list / heading-hierarchy noise / `[@refN]` injection — whichever applies to the loser).

---

### `_archive/data-quality-assessment/<unselected>.md` (archived asset, `git mv`)

**Analog:** `pinn_instruction/markdown_conversion/_archive/ctl-instruction/CTL-instruction-final.md` (or `ctl_instruction_v2.md`)

**Operation:** Pure `git mv`. No content edit. The unselected candidate is moved as-is — citations, broken tables, and all — so the archive preserves the pre-edit state for forensic comparison. Phase 10 archived its losers untouched (file size of `CTL-instruction-final.md` is 56324 bytes and matches the original).

**Two `git mv` cases** (per RESEARCH.md lines 226–228):

- **Pandoc wins (likely):**
  ```bash
  git mv pinn_instruction/markdown_conversion/pandoc_conversion/data_quality_assess.md \
         pinn_instruction/markdown_conversion/data_quality_assessment.md
  git mv pinn_instruction/markdown_conversion/assess_data_quality.md \
         pinn_instruction/markdown_conversion/_archive/data-quality-assessment/assess_data_quality.md
  ```
- **Top-level wins:**
  ```bash
  git mv pinn_instruction/markdown_conversion/assess_data_quality.md \
         pinn_instruction/markdown_conversion/data_quality_assessment.md
  git mv pinn_instruction/markdown_conversion/pandoc_conversion/data_quality_assess.md \
         pinn_instruction/markdown_conversion/_archive/data-quality-assessment/data_quality_assess.md
  ```

The promoted file is then edited in place (Plan 02 citation strip, table rebuild, etc.). The archived file is **never** edited after `git mv`.

---

### `pinn_instruction/markdown_conversion/README.md` (documentation/index — modified, row-append)

**Analog:** Existing CTL row in the same file (line 7 of `pinn_instruction/markdown_conversion/README.md`)

**Existing index pattern** (full file is 7 lines):

```markdown
# Markdown Conversion Index

This index tracks authoritative markdown conversions for the v1.3 verification milestone. It is designed to scale to all 6 v1.3 authoritative markdowns as each source document is verified.

| Source | Authoritative markdown | Verification report | Candidate archive |
|---|---|---|---|
| CTL instruction | [`ctl_instruction.md`](ctl_instruction.md) | [`verification_reports/ctl_instruction_verification_report.md`](verification_reports/ctl_instruction_verification_report.md) | [`_archive/ctl-instruction/README.md`](_archive/ctl-instruction/README.md) |
```

**Phase 11 row to append** (one row, copy column conventions exactly — relative paths, backticked link text, all four columns populated):

```markdown
| Data Quality Assessment | [`data_quality_assessment.md`](data_quality_assessment.md) | [`verification_reports/data_quality_assessment_verification_report.md`](verification_reports/data_quality_assessment_verification_report.md) | [`_archive/data-quality-assessment/README.md`](_archive/data-quality-assessment/README.md) |
```

**Edit operation:** Append-only. Insert exactly one new line after the CTL row. Do not reformat the existing line, change the table header, or modify the introductory paragraph. (Per CLAUDE.md surgical-changes rule.)

---

## Shared Patterns

### Naming/path conventions
**Source:** Phase 10 directory layout (verified via `ls`)
**Apply to:** All file creation in this phase

```
pinn_instruction/markdown_conversion/
├── README.md                                                       # index — append row
├── data_quality_assessment.md                                      # NEW (D-30)
├── verification_reports/
│   └── data_quality_assessment_verification_report.md              # NEW (D-31)
└── _archive/
    └── data-quality-assessment/                                    # kebab-case dir, NEW
        ├── README.md                                               # NEW (D-32)
        └── <unselected-candidate-filename-preserved>.md            # `git mv`d
```

Naming rules (matched Phase 10):
- Authoritative markdown filename: snake_case + descriptive (`data_quality_assessment.md`, mirrors `ctl_instruction.md`).
- Archive directory: kebab-case (`data-quality-assessment/`, mirrors `ctl-instruction/`).
- Verification report filename: `<authoritative-stem>_verification_report.md` (`data_quality_assessment_verification_report.md`, mirrors `ctl_instruction_verification_report.md`).
- Archived candidate filenames: preserve the original filename (Phase 10 archived `CTL-instruction-final.md` and `ctl_instruction_v2.md` with no rename).

### Discrepancy/issue ID conventions
**Source:** Phase 10 verification report (`ctl_instruction_verification_report.md` lines 39, 47, 78, 104, 127, 175)
**Apply to:** Verification report (Plan 02–03)

| ID Type | Phase 10 Pattern | Phase 11 Pattern |
|---|---|---|
| Section discrepancy | `CTL-NN-NNN` where NN = section file number | `DQA-NN-NNN` where NN = section number 01–06 |
| Baseline log entry | `CTL-10-01-BASELINE` | `DQA-10-01-BASELINE` (note: `10` here is the plan number, not phase — Phase 10 used the same "10-01" pattern for "plan 01"; Phase 11 should mirror as `DQA-11-01-BASELINE` OR `DQA-10-01-BASELINE` — Phase 10's analog used `10-01` for "Phase 10 Plan 01", so Phase 11 should use `DQA-11-01-BASELINE` for "Phase 11 Plan 01" |
| Source issue | `SI-CTL-NNN` | `SI-DQA-NNN` |
| Section info-only entry | `CTL-NN-000` (zero suffix indicates "PASS, nothing to fix") | `DQA-NN-000` |

(Per A5 of RESEARCH.md, the exact ID format is Claude's discretion as long as IDs map cleanly between the audit table and the fix log. The `DQA-NN-NNN` pattern is the recommendation.)

### Severity vocabulary
**Source:** Phase 10 (D-13 carried forward)
**Apply to:** All discrepancy tables

Allowed values: `BLOCKING`, `MAJOR`, `MINOR`, `INFO`. Do not invent new severity levels.

Phase 10 example mapping for guidance:
- Table cell-merge corruption → `MAJOR` (analog line 47).
- Author note rendered as Pandoc style span → `MINOR` (analog line 48).
- Excluded comment confirmed absent → `INFO` (analog line 49).

Phase 11 expected mapping:
- HTML table cell-merge in top-level candidate → `MAJOR`.
- Injected `[@refN]` / `[?]` citations stripped → `MAJOR`.
- Trailing reference list stripped → `MAJOR`.
- Heading hierarchy fixes → `MINOR`.
- Description-list `:   \` syntax converted to plain markdown → `MINOR`.
- Vacuous comment-exclusion confirmed → `INFO`.

### Status vocabulary
**Source:** Phase 10 (analog "Status: PASS" lines 36, 44, 60, 75, 100, 124, 138, 146)
**Apply to:** Section audit subsections

Each section audit subsection begins with one line: `Status: PASS` or `Status: FAIL`. Phase 10's final report has every section at `PASS` because all discrepancies were fixed before report finalization. Phase 11 should mirror this — every section reaches `PASS` by the time Plan 03 finalizes the report.

### Fix-status vocabulary
**Source:** Phase 10 ("Fix status" column, analog lines 39, 47, 78, 104, 127, 141, 149)
**Apply to:** Discrepancy tables

Allowed values for the rightmost column: `Fixed`, `No fix needed`, `Verified`.
- `Fixed` — markdown was edited to resolve the issue.
- `No fix needed` — INFO entries that document a passing condition.
- `Verified` — used when the assertion is "absence" (e.g., excluded comments are confirmed absent from converted body).

### Citation-stripping mechanics (NEW — no Phase 10 analog)
**Source:** RESEARCH.md Pitfall 2 (lines 292–319) and Code Examples (lines 414–428)
**Apply to:** Plan 02 (selected candidate edit pass)

Two narrow regex patterns. Both must be applied; both must verify zero remaining matches afterward. **Do not** generalize to a single broad regex — the legitimate `$t \in [0, T]$` and similar constructs must survive.

```bash
# Strip pandoc-style citations (apply both forms — leading-space variant first to absorb the space)
sed -i.bak -E 's/ \[@ref[0-9]+\]//g' data_quality_assessment.md
sed -i.bak -E 's/\[@ref[0-9]+\]//g'  data_quality_assessment.md

# Strip top-level placeholder citations (apply both forms)
sed -i.bak -E 's/ \[\?\]//g' data_quality_assessment.md
sed -i.bak -E 's/\[\?\]//g'  data_quality_assessment.md

# Verify zero remaining
grep -cE '\[@ref[0-9]+\]' data_quality_assessment.md   # must print 0
grep -cF '[?]'             data_quality_assessment.md  # must print 0

# Cleanup macOS sed backups before commit
rm data_quality_assessment.md.bak
```

Trailing reference list (entire `## References` heading + numbered list, plus pandoc's orphan `99` token) must also be removed. The chosen file should end with the last line of `synthesis_conclusion.tex` content, optionally followed by the appended `# Source Issues / Notes for Future Reconciliation` section.

### Tool/command conventions
**Source:** RESEARCH.md "Standard Stack" (lines 116–134) — Phase 10 precedent
**Apply to:** All plans

- Use `git mv` for file moves to preserve history.
- Use `grep -c`, `grep -F`, `grep -E`, `wc -l` for assertions; no helper scripts.
- Use `sed -i.bak` (BSD/macOS portable form), then `rm *.bak` before commit.
- No new dependencies. No Python scripts committed (Phase 10 produced its scoring numbers inline in the report without a script).

---

## No Analog Found

None. Every Phase 11 file has an exact Phase 10 analog. The two new procedures (citation stripping and HTML→GFM table rebuild) are documented in RESEARCH.md (Pitfalls 2–4 and Code Examples) and do not require a code analog — they are direct shell operations on the chosen candidate.

---

## Metadata

**Analog search scope:**
- `pinn_instruction/markdown_conversion/verification_reports/` (1 file — Phase 10 report)
- `pinn_instruction/markdown_conversion/_archive/ctl-instruction/` (3 files — Phase 10 archive: README + 2 unselected candidates)
- `pinn_instruction/markdown_conversion/README.md` (1 file — index)
- `pinn_instruction/markdown_conversion/ctl_instruction.md` (1 file — Phase 10 authoritative output, sampled head + tail for structural conventions)
- `pinn_instruction/markdown_conversion/pandoc_conversion/data_quality_assess.md` (1 file — sampled head only, to confirm front-matter absence)

**Files scanned:** 7
**Pattern extraction date:** 2026-05-05
