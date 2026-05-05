# Phase 11: Data-Quality-Assessment Verification - Research

**Researched:** 2026-05-05
**Domain:** Markdown-conversion verification (LaTeX→Markdown fidelity audit)
**Confidence:** HIGH

## Summary

Phase 11 is the second iteration of the v1.3 markdown-conversion verification cycle. Phase 10 (CTL-instruction) established a 3-plan pattern — candidate selection → section audit → fix+verify+archive — that was executed successfully (10 minutes total, 6 files modified). Phase 11 should reuse that exact 3-plan structure with phase-specific adjustments.

The data-quality-assessment source is **strictly simpler** than CTL on every axis except two: (a) both candidates inject reference content not present in the LaTeX source (top-level uses `[?]` placeholders, pandoc uses `[@refN]` keys), and (b) the top-level candidate's only table is HTML-corrupted with merged cells. Conversely the source has zero `\cite{}` commands, one `\label` (`tab:assessment_strategies`), zero `\ref{}`, six displayed equations, one table, no `\begin{comment}` blocks, and no `\authcomment{}` notes — so most of Phase 10's machinery (comment exclusion, author-note rendering) is vacuously satisfied.

**Primary recommendation:** Reuse Phase 10's 3-plan decomposition exactly, with two new procedures slotted in: a citation-stripping pass (replaces Phase 10's author-note rendering pass) and a single-table HTML→GFM rebuild (replaces Phase 10's multi-table rebuild). Forensic inspection of both candidates already determines the likely winner: the **pandoc candidate (390 lines)** has clean heading hierarchy, clean multiline table, and clean math; the **top-level candidate (394 lines)** has corrupted heading hierarchy at 16+ locations, an HTML table with cell-merge corruption, broken display-math (paragraph break inside multiline equation, lines 21–23), and 33 `[?]` placeholders. Mechanical scoring will likely produce a near-tie on token recall, but human sanity-check should heavily favor pandoc on structural fidelity. Plan executors should be alert to this and not over-trust raw token recall.

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions

**Candidate Baseline (carried from Phase 10)**
- **D-01:** Rank both markdown candidates by diff score before selecting a baseline.
- **D-02:** Perform a human sanity-check of the top-ranked candidate before editing. Human inspection can override the raw score.
- **D-03:** Candidate comparison report must include both overall and per-section scores.
- **D-04:** Normalize away formatting-only noise (whitespace, line wrapping, harmless escaping). Do not normalize content, math, reference, table, or hierarchy changes.

**Citation Handling (new — Phase 11 specific)**
- **D-27:** Strip all `[@refN]` inline citations from the markdown body. The LaTeX source body has zero `\cite{}` commands — any citations in the markdown are post-conversion additions. The body must match the LaTeX source exactly.
- **D-28:** bibliography.tex is excluded from audit scope entirely. It is never `\input`'d by main.tex, contains 33 `\bibitem` entries never cited in the body, and is not mentioned in the verification report.

**Table Handling (new — Phase 11 specific)**
- **D-29:** Convert all HTML `<table>` markup to clean GitHub-flavored markdown tables. Verify cell-by-cell against the LaTeX source. The 2 tables in `assessment_strategy.tex` are the only tables affected.

  *Note:* CONTEXT.md says "the 2 tables in `assessment_strategy.tex`" but the LaTeX source contains exactly **one** `\begin{table}` (`tab:assessment_strategies` at line 61–74 of `assessment_strategy.tex`). The objective brief mentions "2 HTML-corrupted tables" — verified false: the top-level candidate has only **one** HTML `<table>` element (line 115 of `assess_data_quality.md`). This is logged in the Source Issues note below for Plan 01 to clarify with the user; for planning purposes Phase 11 should plan for **one** table conversion.

**Comment and Exclusion Policy (carried from Phase 10, vacuously satisfied)**
- **D-05 through D-09:** The data-quality-assessment source has no `\begin{comment}` environments and no `\authcomment{…}` author notes. These policies carry forward but require no action.

**Audit Workflow (carried from Phase 10)**
- **D-10:** Audit the selected candidate section-by-section in source order (6 active sections).
- **D-11:** Each section audit records a pass/fail summary plus a discrepancy table.
- **D-12:** Discrepancy rows include type, severity, source location, markdown location, and fix status.
- **D-13:** Severity labels: `BLOCKING`, `MAJOR`, `MINOR`, `INFO`.
- **D-14:** Math-heavy sections require a formula-by-formula checklist. The data-quality-assessment source has significant math content in `data_quality_metrics.tex` and other sections.
- **D-15:** Final verification requires zero open discrepancies plus a fix log.

**Correction Authority (carried from Phase 10)**
- **D-16:** Apply markdown-only corrections. LaTeX is ground truth.
- **D-17:** Preserve suspected source-level issues exactly in the markdown body; document them in the appended metadata section.
- **D-18:** Source-level issue notes live in a clearly separated `Source Issues / Notes for Future Reconciliation` section at the end of the markdown.
- **D-19:** The appended source-issues section is metadata — excluded from fidelity comparison.
- **D-20:** Fix discrepancies with small section-scoped edits, not whole-file rewrites.
- **D-21:** Log every fix with discrepancy ID, section, and fix summary.

**Report and Archive Layout (adapted from Phase 10)**
- **D-30:** Authoritative filename: `pinn_instruction/markdown_conversion/data_quality_assessment.md`.
- **D-31:** Verification reports live in `pinn_instruction/markdown_conversion/verification_reports/`. Phase 11 report: `verification_reports/data_quality_assessment_verification_report.md`. Phase 10's report was moved here for consistency.
- **D-32:** Unselected candidate archived to `pinn_instruction/markdown_conversion/_archive/data-quality-assessment/` with a `README.md` documenting provenance and why it was not selected.
- **D-33:** Audit scope: 6 active sections only. bibliography.tex excluded (D-28).
- **D-26:** Update `pinn_instruction/markdown_conversion/README.md` index with the Phase 11 row.

### Claude's Discretion

- Exact diff-score implementation and normalization details (per D-04 constraints).
- Exact markdown table format (GitHub-flavored, with alignment pipes).
- Exact verification report filename and structure within `verification_reports/`.
- Exact discrepancy ID format, as long as IDs map from audit table to fix log.
- Whether the top-level or pandoc candidate wins mechanical diff scoring — determined by measurement, not preference.

### Deferred Ideas (OUT OF SCOPE)

- Fixing suspected source-level factual or methodological issues. Document in the appended metadata section, do not resolve.
- Cross-document reconciliation between data-quality-assessment and other instruction documents. v1.3 preserves source-specific content.
- Building automated markdown verification tooling. Deferred to v2.
- Resolving the question of whether the 33 references in bibliography.tex should be reconnected to the document body with proper `\cite{}` commands. That's a LaTeX source edit — outside v1.3 scope.
</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| CAND-01 | Diff-score selection between multiple candidates | Plan 01 — methodology in §"Candidate Ranking Methodology" below |
| AUDIT-01 | Section-by-section comparison of all 6 active sections | Plan 02 — workflow in §"Section-by-Section Audit Workflow" |
| AUDIT-02 | Per-discrepancy report with type/severity/locations | Plan 02–03 — schema reused from Phase 10 (verified compatible) |
| AUDIT-03 | Exclude `\begin{comment}` blocks before comparison | Vacuously satisfied — source has zero comment environments |
| FIDEL-01 | Math formula fidelity (notation, no missing terms) | Plan 02 — formula checklist for §3 (5 equations) and §1 (1 equation) |
| FIDEL-02 | Prose/list/code-block fidelity | Plan 02 — text-diff per section in source order |
| FIDEL-03 | `\ref`/`\cite`/`\label` preservation | Plan 02 — only 1 `\label` (`tab:assessment_strategies`) to preserve; zero cites/refs |
| FIDEL-04 | Cell-by-cell table verification | Plan 02 — single-table cell verification against `assessment_strategy.tex:61-74` |
| FIDEL-05 | Section/subsection hierarchy fidelity | Plan 02 — hierarchy check per section against source `\section`/`\subsection`/`\paragraph` |
| FIDEL-06 | Comment-block absence + intentional exclusions confirmed | Vacuously satisfied for comments; bibliography.tex exclusion documented in report |
| CLEAN-01 | Exactly one authoritative `data_quality_assessment.md` | Plan 03 — promote selected candidate to `data_quality_assessment.md`, archive other |
| CLEAN-02 | Unselected candidate archived with README | Plan 03 — `_archive/data-quality-assessment/README.md` with provenance table |
| CLEAN-03 | Verification report with selection, discrepancies, fixes, zero-diff | Plan 01–03 — report grows across plans, finalized in 03 |
| CROSS-01 | Inter-document inconsistencies preserved (not reconciled) | Plan 02–03 — any source-level concerns documented in appendix only |
| CROSS-02 | Phase follows audit→fix→verify pattern | All 3 plans — same as Phase 10 |
</phase_requirements>

## Architectural Responsibility Map

This is a documentation-only phase — no application tiers. Mapping is between research artifacts:

| Capability | Primary Artifact | Secondary Artifact | Rationale |
|------------|-----------------|--------------------|-----------|
| Candidate ranking | `data_quality_assessment_verification_report.md` (§Candidate Comparison) | — | Same location and schema as Phase 10's report (verified existing). |
| Citation stripping | `data_quality_assessment.md` (body) | Verification report (fix log) | Body is the artifact corrected; report logs each fix. |
| HTML→GFM table conversion | `data_quality_assessment.md` (one table near §2.3) | Verification report (cell-by-cell check) | Body holds the corrected table; report verifies cells. |
| Section audit | Verification report (§Section Audit) | — | Phase 10's section audit subsection schema applies as-is. |
| Math formula verification | Verification report (§3 formula checklist within Section 03 audit) | `data_quality_assessment.md` (math content) | Phase 10 used the same formula-checklist subsection pattern in Section 04. |
| Source-issue metadata | `data_quality_assessment.md` (appended `Source Issues / Notes for Future Reconciliation`) | Verification report (cross-link) | Mirrors Phase 10's CTL dimensionality note placement. |
| Archive provenance | `_archive/data-quality-assessment/README.md` | — | Direct reuse of Phase 10's `_archive/ctl-instruction/README.md` schema. |
| Index update | `pinn_instruction/markdown_conversion/README.md` | — | Append one row using Phase 10's existing column schema. |

## Standard Stack

This phase uses no libraries — it is plain Markdown editing and shell-based verification. Tools used:

### Core

| Tool | Version | Purpose | Why Standard |
|------|---------|---------|--------------|
| `git` | system | Version control | Project standard |
| `grep`/`rg` | system | Pattern search and counting | Phase 10 used the same |
| `wc`/`diff`/`comm` | system | Line counts, content diffs | Standard POSIX |
| `awk`/`sed` | system | Token extraction for scoring | Available everywhere |
| Python 3 (stdlib) | system | Optional scoring helper if a quick token-recall computation is needed | No new dependency; Phase 10 did the scoring inline in the report without scripts |

### Supporting

None. Phase 10 produced its scoring numbers (`0.958 F1`, `0.890 F1`, `0.959 F1`) without committing a script — they were computed and reported as values. Phase 11 should follow the same pattern: produce scores, justify them in the report, and avoid carrying scoring scripts in the repo (consistent with the project decision "Manual comparison only — no automated verification scripts this milestone (deferred to v2)").

**Installation:** None required.

**Version verification:** Not applicable — no packages added.

## Architecture Patterns

### Phase Structure Diagram

```
                                  Phase 11 Workflow
                                  =================

  +------------------------------+           +-----------------------------+
  | LaTeX source (read-only):    |           | Markdown candidates:        |
  | sections/*.tex (6 active)    |           |  - assess_data_quality.md   |
  | + bibliography.tex EXCLUDED  |           |    (top-level, 394 lines)   |
  +-------------+----------------+           |  - pandoc/data_quality_     |
                |                            |    assess.md (390 lines)    |
                |                            +-------------+---------------+
                |                                          |
                v                                          v
  +------------------------------------------------------------------+
  |  Plan 01: Candidate Selection                                    |
  |  - Strip-citation-pre-normalized scoring (D-04)                  |
  |  - Per-section + overall scores (D-03)                           |
  |  - Human sanity-check for math/table/hierarchy (D-02)            |
  |  - Selection rationale + promotion action (D-30)                 |
  |  - Verification report skeleton with all sections stubbed        |
  +-------------------------+----------------------------------------+
                            |
                            v
  +------------------------------------------------------------------+
  |  Plan 02: Section-by-Section Audit + Section-Scoped Fixes        |
  |  - Strip [@refN] / [?] citations (Citation Stripping pass)       |
  |  - Convert HTML <table> to GFM table, cell-verify (D-29)         |
  |  - Audit each of 6 sections in source order (D-10)               |
  |  - Discrepancy table per section (D-11, D-12)                    |
  |  - Formula checklist for §3 (5 eqns) and §1 (1 eqn) (D-14)       |
  |  - Section-scoped edits, not rewrites (D-20)                     |
  +-------------------------+----------------------------------------+
                            |
                            v
  +------------------------------------------------------------------+
  |  Plan 03: Finalize, Archive, Index                               |
  |  - Append Source Issues metadata section (D-17/D-18/D-19)        |
  |  - Promote final to data_quality_assessment.md (D-30)            |
  |  - Archive unselected candidate + README (D-32)                  |
  |  - Update markdown_conversion/README.md index (D-26)             |
  |  - Final Verification: zero open discrepancies + fix log (D-15)  |
  +-------------------------+----------------------------------------+
                            |
                            v
  +------------------------------------------------------------------+
  | Outputs:                                                         |
  |  pinn_instruction/markdown_conversion/                           |
  |    data_quality_assessment.md                            (D-30)  |
  |    verification_reports/                                         |
  |      data_quality_assessment_verification_report.md      (D-31)  |
  |    _archive/data-quality-assessment/                             |
  |      README.md + <unselected>.md                         (D-32)  |
  |    README.md  <-- index updated                          (D-26)  |
  +------------------------------------------------------------------+
```

### Recommended Output Layout

```
pinn_instruction/markdown_conversion/
├── README.md                           # Index — add Phase 11 row
├── ctl_instruction.md                  # Phase 10 (existing, unchanged)
├── data_quality_assessment.md          # Phase 11 NEW — authoritative
├── verification_reports/
│   ├── ctl_instruction_verification_report.md          # Phase 10 (existing)
│   └── data_quality_assessment_verification_report.md  # Phase 11 NEW
├── _archive/
│   ├── ctl-instruction/                # Phase 10 (existing)
│   │   ├── README.md
│   │   ├── ctl_instruction_v2.md
│   │   └── CTL-instruction-final.md
│   └── data-quality-assessment/        # Phase 11 NEW
│       ├── README.md                   # Provenance for unselected candidate
│       └── <unselected>.md             # Either assess_data_quality.md or data_quality_assess.md
├── pandoc_conversion/
│   └── data_quality_assess.md          # Source candidate (left in place if unselected via copy-into-archive; or moved if file-move chosen — see Pattern below)
└── ...
```

### Pattern 1: Move-vs-Copy for Archive

**What:** When archiving the unselected candidate, the file may be **moved** (preserving git history via `git mv`) or **copied** (leaving the candidate in its original location).

**Phase 10 behavior:** Used `git mv` for both unselected candidates (the originals no longer exist in their original paths after Phase 10).

**Recommendation for Phase 11:** Follow Phase 10. Use `git mv` to move the unselected candidate into `_archive/data-quality-assessment/`. The selected candidate is **promoted** by writing/moving its content to `data_quality_assessment.md`. Two cases:

- **If pandoc wins (likely):** `git mv pinn_instruction/markdown_conversion/pandoc_conversion/data_quality_assess.md pinn_instruction/markdown_conversion/data_quality_assessment.md` then `git mv pinn_instruction/markdown_conversion/assess_data_quality.md pinn_instruction/markdown_conversion/_archive/data-quality-assessment/assess_data_quality.md`.
- **If top-level wins:** `git mv pinn_instruction/markdown_conversion/assess_data_quality.md pinn_instruction/markdown_conversion/data_quality_assessment.md` then `git mv pinn_instruction/markdown_conversion/pandoc_conversion/data_quality_assess.md pinn_instruction/markdown_conversion/_archive/data-quality-assessment/data_quality_assess.md`.

### Pattern 2: Verification Report Skeleton (from Phase 10)

The Phase 10 report (`verification_reports/ctl_instruction_verification_report.md`) is the canonical template. Sections in order:

1. Candidate Comparison (Plan 01)
2. Selected Baseline (Plan 01)
3. Excluded Comment Ranges (Plan 01) — *Phase 11: write "None — source has no `\begin{comment}` environments. `bibliography.tex` is orphaned (never imported by `main-data-quality-assess.tex`) and excluded entirely; not part of the audit corpus."*
4. Section Audit (Plan 02–03, one subsection per source `.tex` file)
5. Fix Log (Plan 02–03, accumulated)
6. Source Issues / Notes for Future Reconciliation (Plan 03)
7. Final Verification (Plan 03)

### Anti-Patterns to Avoid

- **Whole-file markdown rewrite.** Phase 10 explicitly chose section-scoped edits (D-20). A rewrite would lose markdown content already correct in the candidate (e.g., pandoc's clean math, clean heading hierarchy).
- **Stripping citations with a global regex without verification.** A bad regex (`s/\[@?ref?\d*\]//g`) could touch unrelated bracket notation. Validate before mass-replace — see Citation Stripping Mechanics below.
- **Inferring tables from prose.** The LaTeX `\begin{table}` is the sole authority for the table. Do not trust either candidate's cells without cross-checking against `assessment_strategy.tex:65-72`.
- **Carrying the candidates' reference lists into the authoritative output.** Both candidates have a trailing reference list that does not exist in the LaTeX source body — strip it entirely (not just the inline `[@refN]`/`[?]` markers).

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Full pandoc reconversion | A from-scratch pipeline that re-runs pandoc | Section-scoped fix-in-place on the chosen candidate | Project decision: "Pandoc re-conversion of LaTeX sources… destroys manual corrections already applied" (REQUIREMENTS.md, Out of Scope) |
| New verification framework | A Python `md_verification_utils.py` | Manual comparison + grep counts | "AUTO-01… deferred to v2" (REQUIREMENTS.md). Phase 10 used manual comparison successfully in 10 minutes. |
| Programmatic LaTeX→MD diff | A Python tokenizer that diffs structures | Side-by-side reading + per-section discrepancy table | Project decision: "Manual comparison only — no automated verification scripts this milestone" (STATE.md) |
| HTML-table parser | An HTML library like BeautifulSoup | Direct GFM rewrite from the LaTeX source | The LaTeX source is the ground truth (D-16). Don't parse the corrupted HTML — re-author the table from `assessment_strategy.tex:65-72`. |
| Citation-pattern fuzzy matcher | A Python NLP pipeline | Two regex patterns documented below | Two distinct, well-formed patterns (`[@refN]` and `[?]`) cover 100% of injected citations. |

**Key insight:** This is a 3-plan, ~10-minute documentation phase. Tooling complexity buys nothing. Phase 10 delivered identical scope without a single helper script.

## Runtime State Inventory

> Phase 11 is documentation-only — no databases, services, or runtime systems are touched. The grep audit covers the entire scope.

| Category | Items Found | Action Required |
|----------|-------------|------------------|
| Stored data | None — verified by directory inspection. No databases or datastores reference these markdown filenames. | None |
| Live service config | None — verified. No CI/CD, webhook, or external service consumes these markdown files. | None |
| OS-registered state | None — verified. No scheduled tasks, daemons, or hooks reference these paths. | None |
| Secrets/env vars | None — verified. No env vars reference these paths. | None |
| Build artifacts | The LaTeX source compiles (verified Phase 8) but the markdown files are not part of the LaTeX build. The pandoc-generated `pandoc_conversion/data_quality_assess.md` was produced by an external pandoc run that is not part of the in-repo build. | If the pandoc candidate is selected and moved to `data_quality_assessment.md`, no rebuild is required (markdown is the artifact). |

**Nothing found in any category requires migration or re-registration.** This phase is pure file edits + a `git mv`.

## Common Pitfalls

### Pitfall 1: Near-Tied Diff Score Misleads Selection

**What goes wrong:** The two candidates are 394 vs 390 lines (~1% difference). Token recall normalized for whitespace/escapes will likely come within ±0.005 of each other, which feels like a "tie" and tempts the executor to pick the first one inspected.

**Why it happens:** Both candidates carry **the same source prose with high fidelity** — the divergence is in *structural* fidelity (heading levels, table format, math display) and in *injected* content (citations, reference lists). Token recall captures content presence but not structural correctness.

**How to avoid:** Phase 10 already established the override pattern. Compute scores with citation tokens (`[@refN]`, `[?]`) and trailing reference lists **stripped before scoring** so they don't bias the recall in either direction. Then run a structural sanity-check on three signals:
1. Heading hierarchy correctness (does `# Section / ## Subsection / #### Paragraph` follow the LaTeX `\section`/`\subsection`/`\paragraph`?)
2. Table format (HTML/corrupted vs clean GFM)
3. Math display correctness (display equations not split by paragraph break)

Document the override exactly as Phase 10 did: "Raw F1 prefers X; human inspection found Y; final baseline is Z because…"

**Warning signs:** Scores within 0.01 of each other; >5 structural discrepancies in the higher-scoring candidate.

### Pitfall 2: Citation Regex Touches Legitimate Bracket Notation

**What goes wrong:** The LaTeX body uses `[?]` and `[@refN]` is used for citations, but **legitimate bracketed text exists** in the source — e.g., math intervals `t \in [0, T]`, `[0, 1]`, list-item indices, or markdown link/image syntax. A naive `s/\[.*?\]//g` corrupts the prose.

**Why it happens:** Both candidates render math intervals as `$t \in [0, T]$` (correctly preserved as math) — these are inside `$...$` math fences and untouched by content-text regex. But pandoc's description-list syntax uses `:   `, and there are other bracketed patterns (e.g., `\[ ... \]` in display math) that must not be confused with citations.

**How to avoid:** Use **two narrow patterns**, each targeting exactly the injected citation syntax:

| Candidate | Pattern | Verified count |
|-----------|---------|----------------|
| Pandoc | `\[@ref[0-9]+\]` (regex) | 32 occurrences across 30 lines |
| Top-level | `\[\?\]` (regex — literal `[?]`) | 33 occurrences across 33 lines |

Both patterns are anchored on syntactically distinctive tokens (`@ref` and `?`). Neither overlaps with math, code, list markers, or markdown link syntax.

**Verification step:** After stripping, the count of remaining matches must be 0. Run:
```bash
grep -cE '\[@ref[0-9]+\]' data_quality_assessment.md  # must print 0
grep -cF '[?]' data_quality_assessment.md              # must print 0
```

**Edge cases:**
- Citations at sentence boundaries: `... gradient descent dynamics [@ref8].` — strip the citation **and** any preceding space, leaving the period attached to the prose: `... gradient descent dynamics.`
- Citations after question marks: `... satisfy Newton's laws? [?]` and `... Newton's laws? [@ref16]` — strip the citation, preserve the question mark.
- Multiple grouped citations on the same line: line 9 of the pandoc candidate has `[@ref1]` and `[@ref3]`, line 11 has `[@ref3]` × 3, line 13 has `[@ref6]` and `[@ref8]`. Each should be stripped individually; no special grouping logic needed.
- The pandoc candidate also has 1 trailing line `99` (line 323) — leftover from the bibliography environment header `\begin{thebibliography}{99}`. This must also be stripped along with the entire reference list (see Pitfall 3).

**Cleanup of trailing whitespace:** After stripping, some lines will end with `  ` (double space, then bracket removed). A second-pass normalization to trim trailing whitespace is recommended — but is **formatting-only** and so is consistent with D-04.

### Pitfall 3: Trailing Reference List Forgotten

**What goes wrong:** The injected `[@refN]` / `[?]` markers are obvious; the **trailing reference list is also injected content** but is easy to miss because it visually looks like a "References" section.

**Why it happens:** The source LaTeX body has zero `\cite` and the only LaTeX bibliography is in `bibliography.tex` which is **orphaned** (never `\input`'d by `main-data-quality-assess.tex`). Both candidates fabricated a reference list:

- **Top-level** (`assess_data_quality.md:331-393`): `## References` heading + numbered `[2]…[33]` list, 32 entries. Note: starts at `[2]`, missing `[1]`. URLs sometimes have stray spaces (e.g., `https:// academic.oup.com`, `https:// www.alphaxiv.org`).
- **Pandoc** (`data_quality_assess.md:323-389`): standalone `99` token (orphan from `\begin{thebibliography}{99}`) + 32 entries, no heading, no numbering, italics for journals.

**How to avoid:** Strip the **entire trailing reference list** — heading, leading-orphan tokens (`99`), and all entries. The chosen candidate must end at the last paragraph of the LaTeX `synthesis_conclusion.tex` source.

**Verification step:**
- Last non-blank, non-source-issues-section line of `data_quality_assessment.md` must contain text matching the final LaTeX line: `... reduces the data quality burden regarding energy drift.` (from `synthesis_conclusion.tex:14`).
- After stripping, the file should end with the last bullet point under "Recommendations for Future Work" — followed only by the appended `## Source Issues / Notes for Future Reconciliation` section.

### Pitfall 4: HTML Table Cell-Merge Corruption

**What goes wrong:** The top-level candidate's HTML table (line 115 of `assess_data_quality.md`) **merges two LaTeX rows into one HTML row**: "Risk Addressed Blind Spot" appears as a single cell label with concatenated values "Garbage In,Garbage OutNeural Network Inductive Bias", "Model DivergencePhysical Validity of Minima", "Systemic FailureNone".

This corruption silently drops the row separator between `\textbf{Risk Addressed}` and `\textbf{Blind Spot}` from the LaTeX source (`assessment_strategy.tex:71-72`).

**Why it happens:** A bad HTML conversion from a Word/Office source likely lost the row break. The pandoc candidate has the table correctly with all 5 rows separated.

**How to avoid:** If the top-level candidate is selected (unlikely per Pitfall 1), the table **must be entirely re-authored** from the LaTeX source — do not attempt to repair the HTML in place. If the pandoc candidate is selected, the existing multiline table should be re-emitted as **GitHub-flavored** markdown (with `|` separators and a `---` header rule) per D-29, since pandoc's multiline-table syntax is not GitHub-flavored.

**Authoritative cell content (from LaTeX source `assessment_strategy.tex:65-72`):**

```
                  Pre-Training Validation     Trial Training              Staged Gate Protocol
Feature           (Static)                    (Dynamic)                   (Hybrid)
-------           --------------------------  --------------------------  -----------------------------
Primary Metric    Physical Conservation,      Convergence Rate,           Composite Score
                  Continuity                  Loss Value
Computational     Low (CPU)                   High (GPU)                  Optimized (CPU first,
Cost                                                                      GPU second)
Detects           Integration Errors,         Gradient Issues,            Both + Architecture
                  Outliers                    Hyperparams                 Mismatch
Risk Addressed    Garbage In, Garbage Out     Model Divergence            Systemic Failure
Blind Spot        Neural Network Inductive    Physical Validity           None
                  Bias                        of Minima
```

Caption: `Comparative Analysis of Assessment Strategies`. Label: `tab:assessment_strategies`.

**Warning sign:** Any rendered table where "Risk Addressed" and "Blind Spot" appear in the same row.

### Pitfall 5: Math Display Equation Split By Paragraph Break

**What goes wrong:** In the top-level candidate, the equation that defines Brutus's iterative precision adjustment is split across `assess_data_quality.md:21-23`:
```
... and decreases the tolerance parameter $ \epsilon $

until the solution converges ...
```

A blank line inside what *should* be a single paragraph (per LaTeX source line 11 of `introduction.tex`) breaks the prose. This is not strictly a math-rendering bug — the math fences are inline `$...$`, not display — but the paragraph segmentation is wrong.

**How to avoid:** If the top-level candidate is selected, scan for paragraphs that begin with a continuation phrase (`until`, `where`, `while`, `then`, `but`) lacking a capitalized sentence start before them, and join them. Pandoc does not have this issue.

**Warning sign:** A paragraph that begins with a lowercase verb ("until", "where") or that flows mid-sentence from the previous block.

### Pitfall 6: Pandoc Description-List Syntax in Selected Candidate

**What goes wrong:** The pandoc candidate uses LaTeX-style description-list syntax (lines 69–88 for "Phase 1/2/3" entries; lines 190–232 for "Risk:/Parameter Consequence:/Mitigation:" entries):

```
Phase 1: The Physics Gate (Static)

:   \
    **Input:** Raw Brutus Trajectories.\
    ...
```

GitHub markdown does not natively render this syntax cleanly — the `:   ` prefix renders as literal text in some viewers.

**How to avoid:** This is a **rendering-fidelity** issue, not a content-fidelity issue. The text content matches the LaTeX `\begin{description}` and `\item[...]` items exactly. Phase 10 chose to convert similar Pandoc-rendered constructs into "plain markdown" (blockquotes for author notes). Phase 11 should follow the same posture: convert `:   \` blocks into a clean Markdown structure such as:

```
**Phase 1: The Physics Gate (Static)**
- **Input:** Raw Brutus Trajectories.
- **Action:** Rigorous checking of conservation laws (Energy, Momentum) and symplectic consistency.
- **Outcome:** Binary Pass/Fail. Trajectories with drift $> \delta_{tol}$ are discarded immediately. This filters out integration failures.
```

This preserves all content, all bold emphasis, and all the math, while rendering correctly on GitHub. Same treatment applies to the description list at lines 190–232 covering the "Causal Firewall Effect" sub-entries.

**Warning sign:** `:   \` literal at the start of a line in the rendered output.

## Code Examples

Verified patterns from Phase 10 and the LaTeX source.

### Citation Stripping (regex)

```bash
# Strip pandoc-style citations (preserve surrounding spaces/punctuation as needed)
sed -i.bak -E 's/ \[@ref[0-9]+\]//g' data_quality_assessment.md      # variant: leading-space form
sed -i.bak -E 's/\[@ref[0-9]+\]//g'  data_quality_assessment.md      # variant: bare form (rare; use both)

# Strip top-level placeholder citations
sed -i.bak -E 's/ \[\?\]//g' data_quality_assessment.md              # leading-space form
sed -i.bak -E 's/\[\?\]//g'  data_quality_assessment.md              # bare form

# Verify zero remaining
grep -cE '\[@ref[0-9]+\]' data_quality_assessment.md   # must print 0
grep -cF '[?]'             data_quality_assessment.md  # must print 0
```

Note: `sed` `-i.bak` creates `.bak` files; remove them before commit. macOS `sed` requires the empty-string suffix (`-i ''`) or `.bak` — use `.bak` and `rm *.bak` to be portable.

### GFM Table Reconstruction

```markdown
| Feature              | Pre-Training Validation (Static) | Trial Training (Dynamic) | Staged Gate Protocol (Hybrid) |
|----------------------|----------------------------------|--------------------------|-------------------------------|
| **Primary Metric**   | Physical Conservation, Continuity | Convergence Rate, Loss Value | Composite Score |
| **Computational Cost** | Low (CPU) | High (GPU) | Optimized (CPU first, GPU second) |
| **Detects**          | Integration Errors, Outliers | Gradient Issues, Hyperparams | Both + Architecture Mismatch |
| **Risk Addressed**   | Garbage In, Garbage Out | Model Divergence | Systemic Failure |
| **Blind Spot**       | Neural Network Inductive Bias | Physical Validity of Minima | None |

*Table 1: Comparative Analysis of Assessment Strategies* {#tab:assessment_strategies}
```

Notes:
- The label `tab:assessment_strategies` is the only `\label` in the entire data-quality-assessment source. It can be represented as a markdown anchor comment `<!-- tab:assessment_strategies -->` or as part of a caption with the kramdown/pandoc identifier `{#tab:assessment_strategies}`. **Phase 10 precedent:** in CTL, table labels were preserved as an anchor reference in the caption text rather than rendered as kramdown identifiers. Recommend the same approach for Phase 11 — output the caption as `*Table 1: Comparative Analysis of Assessment Strategies*` followed (or preceded) by a note that the source label is `tab:assessment_strategies` (visible to readers, not requiring kramdown to render correctly).
- Six rows including the header (matching the LaTeX `\begin{tabular}` 6-row structure: header + 5 data rows).

### Discrepancy Table Schema (reused from Phase 10)

```markdown
### assessment_strategy.tex - Assessment Strategy: Trade-offs Between Pre-Training Validation and Trial Training

Status: PASS

| ID | Type | Severity | Source location | Markdown location | Issue | Fix status |
|---|---|---|---|---|---|---|
| DQA-02-001 | table | MAJOR | `assessment_strategy.tex:61-74` (`tab:assessment_strategies`) | `data_quality_assessment.md:LL-LL` | HTML cell-merge corruption: rows "Risk Addressed" and "Blind Spot" merged into a single row with concatenated cells. | Fixed |
| DQA-02-002 | citation | MAJOR | `assessment_strategy.tex:0` (no `\cite`) | `data_quality_assessment.md:LL` and others | Injected `[@refN]`/`[?]` citations not present in LaTeX source. | Fixed (stripped) |
| DQA-02-003 | hierarchy | MINOR | `assessment_strategy.tex:9,16,26,33,40` (`\paragraph{Advantages:}` etc.) | candidate-dependent | Paragraph headings rendered as `## ` (top-level) or as bold-italic — needs consistent paragraph-level treatment. | Fixed (or Verified) |
```

The schema is identical to Phase 10 except for two new `Type` values that should be added: **`citation`** (for the strip-all-injected-citations work) and **`table-corruption`** (a sub-type of `table`). The rest of the schema is unchanged.

## State of the Art

This is a continuation of Phase 10's pattern. No domain shifts.

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| Verification reports next to artifact | Reports in `verification_reports/` subdirectory | Phase 11 context (CONTEXT.md D-31, applied 2026-05-05) | Cleaner directory listing; Phase 10's report was relocated to match |
| Per-phase comment-exclusion inventory | Phase 11 reports "None applicable" explicitly | This phase | Vacuous satisfaction must be documented, not omitted, so AUDIT-03 and FIDEL-06 traceability is unambiguous |
| Author-note rendering pass | Citation-stripping pass | This phase | Replaces D-06/D-07 work product because there are no `\authcomment` notes |

**Deprecated/outdated:**
- None — Phase 10's pattern is the current state of the art for this milestone.

## Assumptions Log

| # | Claim | Section | Risk if Wrong |
|---|-------|---------|---------------|
| A1 | "The objective brief mentions 2 HTML-corrupted tables; verified the source has only 1 table." | Citation-stripping / HTML table strategy | Low — if a second table is in fact intended (e.g., a description-list group counted as a table), Plan 02 will catch it during the section audit. The plan should not assume "only one table" without re-verifying. [VERIFIED: grep `\\begin{table}` in all sections returned 1 match] |
| A2 | "Pandoc candidate is the likely winner on structural fidelity." | Candidate ranking | Low — Plan 01 measures and overrides if needed. The recommendation is non-binding. [ASSUMED based on structural inspection of both candidates; final scoring is Plan 01's job] |
| A3 | "The pandoc candidate's description-list syntax (`:   \`) should be converted to plain GitHub-flavored markdown (bold + bulleted)." | Pitfall 6 / Pattern 2 | Medium — different markdown viewers render `:` differently. Phase 10 precedent for converting Pandoc-specific renderings into plain markdown supports this approach. [CITED: Phase 10 plan 10-02-SUMMARY.md "Treat Pandoc red style spans for visible authcomments as conversion noise and convert them to plain markdown author-note blockquotes."] |
| A4 | "The disconnected reference list at the end of both candidates must be stripped entirely (heading + all entries + leftover `99` token)." | Pitfall 3 | Low — confirmed by reading the LaTeX source: zero `\cite` and `bibliography.tex` is orphaned. CONTEXT.md decision D-27 supports this. [VERIFIED: `\input` of bibliography.tex is absent from main-data-quality-assess.tex, grepped] |
| A5 | "Discrepancy ID format `DQA-NN-NNN` (Section number, sequential). Source-issue IDs use `SI-DQA-NNN`." | Discrepancy table schema | Very low — this is Claude's discretion per D-30. Phase 10 used `CTL-NN-NNN` and `SI-CTL-NNN`. [VERIFIED via Phase 10 verification report] |

## Open Questions

1. **CONTEXT.md mentions "2 HTML-corrupted tables" but only 1 table exists in the source.**
   - What we know: `\begin{table}` count in `Data-quality-assessment/sections/*.tex` is exactly 1 (in `assessment_strategy.tex`). The top-level candidate has exactly one HTML `<table>` element. The pandoc candidate has one multiline-table block.
   - What's unclear: Whether CONTEXT.md's reference to "2 tables" is a typo, or whether a description-list block (e.g., the "Phase 1/2/3" gates in `assessment_strategy.tex:44-59`) was being counted as a "table" in colloquial usage.
   - Recommendation: Plan 01 should explicitly state the count is 1 table and the description-list is not a table, and verify with the user during candidate selection. No blocking issue.

2. **GFM-anchor strategy for the single `\label`.**
   - What we know: `tab:assessment_strategies` is the only label. There is no `\ref{}` to it in the source. So strictly speaking, FIDEL-03 is satisfied if the label is preserved as a comment, anchor, or caption identifier — anywhere visible.
   - What's unclear: Whether the user wants `{#tab:assessment_strategies}` (kramdown), an HTML anchor `<a id="tab:assessment_strategies"></a>`, or a plain caption mention.
   - Recommendation: Default to plain caption mention with the label visible (e.g., "Table 1 (`tab:assessment_strategies`): Comparative Analysis of Assessment Strategies"). This was the implicit Phase 10 pattern for non-referenced labels.

3. **Should the appended `Source Issues / Notes for Future Reconciliation` section be present even if no source issues are found?**
   - What we know: Phase 10 appended it because it had 1 source issue (the dimensionality inconsistency). Phase 11's source is much simpler.
   - What's unclear: Whether to write the section with "(none — no source-level concerns identified)" content vs. omit the section.
   - Recommendation: Include the section with explicit "(none)" content. This keeps the file structure consistent across all 6 v1.3 phases and makes future re-verification easier.

## Environment Availability

| Dependency | Required By | Available | Version | Fallback |
|------------|------------|-----------|---------|----------|
| `git` | Plan 01–03 (commits, file moves) | ✓ | system | — |
| `grep` / `rg` | All plans (counting/scoring) | ✓ | system | — |
| `wc` | Candidate scoring | ✓ | system | — |
| `sed` (BSD/macOS) | Citation stripping | ✓ | system | Python `re.sub` if needed |
| `diff` | Sanity checks during section audit | ✓ | system | — |
| Python 3 | Optional, only if scoring helper needed | ✓ | 3.x present in project | — |

**Missing dependencies with no fallback:** none

**Missing dependencies with fallback:** none — this is a pure documentation phase using POSIX tools that are universally available.

## Validation Architecture

> Required: `workflow.nyquist_validation` is `true` (verified `.planning/config.json`).

Validation in this phase is a series of **deterministic file-state assertions** rather than executable tests. There is no test framework to run, but each requirement maps to a shell-checkable invariant. Plan-level VALIDATION.md should encode these.

### Test Framework

| Property | Value |
|----------|-------|
| Framework | Shell-based deterministic assertions (grep / wc / file-existence checks) |
| Config file | None — assertions live inline in each plan's TASK ACTIONS or VALIDATION.md |
| Quick run command | `bash .planning/phases/11-data-quality-assessment-verification/validation/quick.sh` (created by Plan 01 if needed) |
| Full suite command | Same — assertions are fast (<1 second) |

### Phase Requirements → Test Map

| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| CAND-01 | Verification report contains candidate ranking with both overall + per-section scores | grep | `grep -A2 "Candidate Comparison" pinn_instruction/markdown_conversion/verification_reports/data_quality_assessment_verification_report.md \| grep -E "score\|rank"` | ❌ Wave 0 (Plan 01 creates) |
| AUDIT-01 | Section audit subsections present for all 6 active sections | grep | `for s in introduction assessment_strategy data_quality_metrics model_parameter_risks implementation_protocol synthesis_conclusion; do grep -q "### $s.tex" pinn_instruction/markdown_conversion/verification_reports/data_quality_assessment_verification_report.md \|\| echo "MISSING $s"; done` | ❌ Wave 0 (Plan 02 creates each) |
| AUDIT-02 | Each section has discrepancy table with required columns | grep | `grep -E "^\| ID \| Type \| Severity \| Source location \|" pinn_instruction/markdown_conversion/verification_reports/data_quality_assessment_verification_report.md \| wc -l` returns ≥ 6 (one header per section) | ❌ Wave 0 (Plan 02) |
| AUDIT-03 | Comment-environment ranges enumerated (or "None" stated) | grep | `grep -A3 "Excluded Comment Ranges" pinn_instruction/markdown_conversion/verification_reports/data_quality_assessment_verification_report.md` returns text containing "None" or table rows | ❌ Wave 0 (Plan 01 creates) |
| FIDEL-01 | All 6 displayed equations from source are present in authoritative markdown | grep+count | `grep -cE '^\$\$\|^\\\\[' pinn_instruction/markdown_conversion/data_quality_assessment.md` returns 6 (or `grep -cE '\\$\\$' ...` returns 12 if inline `$$ ... $$`) | ❌ Wave 0 (Plan 02) |
| FIDEL-02 | First and last sentences of each LaTeX section appear in markdown | grep | `grep -qF "The integration of high-fidelity numerical analysis" data_quality_assessment.md && grep -qF "training the next generation of physics-informed neural solvers." data_quality_assessment.md` | ❌ Wave 0 (Plan 02) |
| FIDEL-03 | Single `\label{tab:assessment_strategies}` label preserved | grep | `grep -qF "tab:assessment_strategies" data_quality_assessment.md` | ❌ Wave 0 (Plan 02) |
| FIDEL-04 | Table contains all 5 row labels and 3 strategy columns | grep | `for r in "Primary Metric" "Computational Cost" "Detects" "Risk Addressed" "Blind Spot"; do grep -qF "$r" data_quality_assessment.md \|\| echo "MISSING $r"; done` | ❌ Wave 0 (Plan 02) |
| FIDEL-05 | Top-level heading count matches LaTeX `\section` count (6) | grep | `grep -cE "^# [^#]" data_quality_assessment.md` returns ≥ 6 (one per section; ignores any title heading by anchoring on space-not-#) | ❌ Wave 0 (Plan 02) |
| FIDEL-06 | Zero comment-block content leaked (vacuously) | grep | `! grep -F "% \begin{comment}" data_quality_assessment.md && ! grep -F "\authcomment" data_quality_assessment.md` | ❌ Wave 0 (Plan 02) |
| CLEAN-01 | Authoritative file exists, unselected does not exist at original path | file | `[ -f pinn_instruction/markdown_conversion/data_quality_assessment.md ] && [ ! -f <original-unselected-path> ]` | ❌ Wave 0 (Plan 03) |
| CLEAN-02 | Archive README + unselected file in archive dir | file | `[ -f pinn_instruction/markdown_conversion/_archive/data-quality-assessment/README.md ] && [ -n "$(ls pinn_instruction/markdown_conversion/_archive/data-quality-assessment/*.md 2>/dev/null \| grep -v README)" ]` | ❌ Wave 0 (Plan 03) |
| CLEAN-03 | Verification report contains: candidate selection, all discrepancies, fix log, zero-diff confirmation | grep | `for s in "## Selected Baseline" "## Section Audit" "## Fix Log" "Open discrepancies: 0"; do grep -qF "$s" pinn_instruction/markdown_conversion/verification_reports/data_quality_assessment_verification_report.md \|\| echo "MISSING $s"; done` | ❌ Wave 0 (Plan 03) |
| CROSS-01 | Source-issues section either present with notes or "(none)" — does not reconcile or rewrite source | grep | `grep -qF "Source Issues / Notes for Future Reconciliation" data_quality_assessment.md` | ❌ Wave 0 (Plan 03) |
| CROSS-02 | Phase has 3 plans matching audit→fix→verify cycle | file | `ls .planning/phases/11-data-quality-assessment-verification/11-0[123]-PLAN.md \| wc -l` returns 3 | ❌ Wave 0 (planner output) |

### Citation-Stripping Validation (NEW for Phase 11)

These assertions are unique to Phase 11 (no Phase 10 analog). They MUST be in VALIDATION.md and run after Plan 02:

| Assertion | Command | Expected |
|-----------|---------|----------|
| Zero pandoc-style citations remain | `grep -cE '\[@ref[0-9]+\]' pinn_instruction/markdown_conversion/data_quality_assessment.md` | `0` |
| Zero placeholder citations remain | `grep -cF '[?]' pinn_instruction/markdown_conversion/data_quality_assessment.md` | `0` |
| No reference list heading | `grep -qE '^# References$\|^## References$' pinn_instruction/markdown_conversion/data_quality_assessment.md && echo FAIL \|\| echo PASS` | `PASS` |
| No orphan `99` token (pandoc bibliography header artifact) | `grep -qE '^99$' pinn_instruction/markdown_conversion/data_quality_assessment.md && echo FAIL \|\| echo PASS` | `PASS` |
| File ends within `synthesis_conclusion` content (or with appended Source Issues section) | `tail -1 pinn_instruction/markdown_conversion/data_quality_assessment.md` | non-empty; either matches LaTeX final line or matches Source Issues text |

### Table Validation (NEW for Phase 11)

| Assertion | Command | Expected |
|-----------|---------|----------|
| No HTML `<table>` markup remains | `grep -cE '<table\|<tr\|<td' pinn_instruction/markdown_conversion/data_quality_assessment.md` | `0` |
| GFM table separator row present | `grep -cE '^\\|.*-+.*\\|' pinn_instruction/markdown_conversion/data_quality_assessment.md` | `≥ 1` |
| All 5 row labels present (cell-by-cell verification) | `for r in "Primary Metric" "Computational Cost" "Detects" "Risk Addressed" "Blind Spot"; do grep -qF "$r" data_quality_assessment.md \|\| echo "MISSING: $r"; done` | (no MISSING output) |
| All 3 column headers present | `for c in "Pre-Training Validation" "Trial Training" "Staged Gate Protocol"; do grep -qF "$c" data_quality_assessment.md \|\| echo "MISSING: $c"; done` | (no MISSING output) |
| No cell-merge corruption (i.e., "Risk Addressed Blind Spot" must NOT appear adjacent) | `! grep -qE 'Risk Addressed[ \\|]+Blind Spot' data_quality_assessment.md && echo PASS \|\| echo FAIL` | `PASS` |

### Math Formula Validation (FIDEL-01 supplement)

The 6 displayed equations expected (per `\begin{equation}` count in source):

| # | Source location | Content signature | grep assertion |
|---|----------------|-------------------|----------------|
| 1 | `introduction.tex:20-22` | Causal weighted loss: `\mathcal{L}(\theta) = \sum_{i=1}^{N_t} w_i \mathcal{L}_i(\theta)` | `grep -qE 'sum_\{i=1\}\^\{N_t\}' data_quality_assessment.md` |
| 2 | `data_quality_metrics.tex:11-13` | Hamiltonian: `H = \sum_i \frac{p_i^2}{2 m_i} - \sum_{i<j} \frac{G m_i m_j}{...}` | `grep -qF '\frac{G m_i m_j}' data_quality_assessment.md \|\| grep -qF 'G m_i m_j' data_quality_assessment.md` |
| 3 | `data_quality_metrics.tex:18-20` | SCS metric definition: `SCS = \log_{10}(\max ...)` | `grep -qE 'SCS *= *\\\\?log_\{10\}' data_quality_assessment.md` |
| 4 | `data_quality_metrics.tex:40-42` | SASD ratio: `SASD_i = \Delta t_i / \tau_{char}` | `grep -qE 'SASD_i *= *\\\\frac\{\\\\Delta t_i\}' data_quality_assessment.md` |
| 5 | `data_quality_metrics.tex:63-65` | IPR formula: `IPR = (1/M) \sum_{k=1}^M \| ... \|^2` | `grep -qE 'IPR *= *\\\\frac\{1\}\{M\}' data_quality_assessment.md` |
| 6 | `data_quality_metrics.tex:77-79` | Shannon entropy: `H_{data} = -\sum p_k \log p_k` | `grep -qE 'H_\{data\} *= *-' data_quality_assessment.md` |

These exact regex patterns are illustrative; Plan 02 can adjust to match the chosen candidate's whitespace/formatting choices.

### Sampling Rate

- **Per task commit:** Run citation-stripping + table + heading-hierarchy assertions from the table above (≤10 grep calls, < 1 sec).
- **Per wave merge:** Run all Phase Requirements assertions (≤30 grep calls, ~1 sec).
- **Phase gate:** Full assertion suite + manual side-by-side reading of the 6 sections (the latter cannot be automated and is the human verification step that completes the phase).

### Wave 0 Gaps

- [ ] `pinn_instruction/markdown_conversion/data_quality_assessment.md` — does not exist; Plan 03 creates by promotion.
- [ ] `pinn_instruction/markdown_conversion/verification_reports/data_quality_assessment_verification_report.md` — does not exist; Plan 01 creates skeleton.
- [ ] `pinn_instruction/markdown_conversion/_archive/data-quality-assessment/README.md` — does not exist; Plan 03 creates.
- [ ] `pinn_instruction/markdown_conversion/_archive/data-quality-assessment/<unselected>.md` — does not exist; Plan 03 creates by `git mv`.
- [ ] Updated `pinn_instruction/markdown_conversion/README.md` with Phase 11 row — Plan 03 modifies.

*(No new test infrastructure required — assertions run via inline shell. The plan authors should embed the assertion table above into VALIDATION.md verbatim.)*

## Plan Decomposition Recommendation

**Recommendation: 3 plans, exactly mirroring Phase 10's structure.**

The data-quality-assessment phase is **strictly easier** than CTL on every axis except citation stripping and table conversion, and these two new procedures fit naturally inside the existing Plan 02 envelope without requiring a 4th plan. A 2-plan compression would over-load Plan 02; a 4-plan expansion would create artificial dependencies. Three plans match Phase 10's velocity (~10 minutes, 6 file modifications) and match the Phase 10 SUMMARY.md cadence (3 min / 4 min / 4 min for the three plans).

### Plan 01: Candidate Selection + Report Skeleton

**Carries:** D-01, D-02, D-03, D-04, D-30, D-31, D-33, D-28
**Output files:**
- `pinn_instruction/markdown_conversion/verification_reports/data_quality_assessment_verification_report.md` (created)

**Tasks (3, mirroring Phase 10 Plan 01):**
1. Compute citation/reference-stripped, whitespace-normalized token recall + F1 for both candidates against the 6 LaTeX sections; record per-section scores.
2. Run human structural sanity-check on heading hierarchy, table format, math display continuity. Document any override of raw scoring.
3. Create the verification report skeleton with: Candidate Comparison table, Selected Baseline section + rationale + override note (if applicable), Excluded Comment Ranges section ("None — source has zero comment environments. `bibliography.tex` is orphaned and excluded entirely."), Section Audit placeholder (one subsection per source `.tex` file), Fix Log placeholder, Source Issues placeholder, Final Verification placeholder.

**Requirements completed:** CAND-01, AUDIT-03, CLEAN-01 (partial — selection recorded; promotion happens in Plan 03)

**Decisions made by this plan:**
- Selected candidate (rationale + override note if needed)
- Promotion strategy (file-move vs file-copy)

### Plan 02: Section-by-Section Audit + Section-Scoped Fixes

**Carries:** D-10, D-11, D-12, D-13, D-14, D-16, D-20, D-21, D-27, D-29
**Output files:**
- `pinn_instruction/markdown_conversion/verification_reports/data_quality_assessment_verification_report.md` (modified — section audits added, fix log entries added)
- The selected candidate file (modified — citations stripped, table rebuilt, hierarchy normalized, descriptions converted to plain markdown)

**Tasks (2, mirroring Phase 10 Plan 02 — possibly 3 if executor wants to split fixes):**
1. **Audit pass — sections 1, 2, 3** (Introduction, Assessment Strategy, Data Quality Metrics): create section audit subsections with discrepancy tables; for §2, include the table-conversion discrepancy and the formula-checklist for §1's one equation; for §3, include the formula checklist for the 5 equations (`H`, `SCS`, `SASD_i`, `IPR`, `H_data`).
2. **Audit pass — sections 4, 5, 6** (Model Parameter Risks, Implementation Protocol, Synthesis Conclusion): create section audit subsections with discrepancy tables; apply citation-stripping pass globally (covers all 6 sections — easier to do as a single global edit per Pitfall 2's regex strategy); apply description-list-to-bullet-list conversion if pandoc was selected (Pitfall 6); apply table rebuild (Pitfall 4) if not done in task 1.

**Requirements completed:** AUDIT-01, AUDIT-02, AUDIT-03, FIDEL-01 (math), FIDEL-02 (prose), FIDEL-03 (1 label), FIDEL-04 (table), FIDEL-05 (hierarchy), FIDEL-06 (vacuous comment exclusion), CROSS-01 (preserve source content)

**Decisions made by this plan:**
- Discrepancy ID prefix (recommend `DQA-NN-NNN`)
- Whether the description-list conversion is "rendering normalization" or a fidelity-preserving fix
- Whether any source-level concern is identified (most likely none, given the source's simplicity)

### Plan 03: Promotion, Archive, Index, Final Verification

**Carries:** D-15, D-17, D-18, D-19, D-26, D-30, D-32
**Output files:**
- `pinn_instruction/markdown_conversion/data_quality_assessment.md` (created via `git mv`)
- `pinn_instruction/markdown_conversion/_archive/data-quality-assessment/README.md` (created)
- `pinn_instruction/markdown_conversion/_archive/data-quality-assessment/<unselected>.md` (created via `git mv`)
- `pinn_instruction/markdown_conversion/README.md` (modified — Phase 11 row appended)
- `pinn_instruction/markdown_conversion/verification_reports/data_quality_assessment_verification_report.md` (modified — Source Issues filled in, Final Verification populated)

**Tasks (3, mirroring Phase 10 Plan 03):**
1. Append the `## Source Issues / Notes for Future Reconciliation` section to `data_quality_assessment.md`. Recommended content: "(none — no source-level mathematical, factual, or methodological concerns identified during section audit)" plus a note about the orphaned `bibliography.tex` referencing 33 `\bibitem` entries with no in-body `\cite` commands, which is a documented LaTeX-source-level concern but does NOT affect markdown fidelity.
2. Promote the selected candidate via `git mv` to `pinn_instruction/markdown_conversion/data_quality_assessment.md`. Move the unselected candidate via `git mv` to `pinn_instruction/markdown_conversion/_archive/data-quality-assessment/<filename>.md`. Create the archive README with provenance table.
3. Update `pinn_instruction/markdown_conversion/README.md` index with the Phase 11 row. Finalize the verification report's Final Verification section: "Open discrepancies: 0", "Zero open discrepancies: yes", "Converted body excludes appended source-issue metadata from fidelity comparison: yes", "Fix log complete: yes".

**Requirements completed:** CLEAN-01, CLEAN-02, CLEAN-03, CROSS-02

**Decisions made by this plan:**
- Whether to keep the trailing blank line consistent with Phase 10
- Final phrasing of the Source Issues "(none)" section

### Why not 2 plans?

Compressing into 2 plans would force Plan 01 to also do candidate selection AND audit setup (no value), or compress audit + fixes + archive into one plan (loses the natural commit boundary between "audit done" and "archived & finalized"). Phase 10's 3-plan cadence committed in distinct points and was efficient (10 minutes total).

### Why not 4 plans?

Splitting audit into "audit only" + "fix only" plans would require carrying state between them — every discrepancy ID becomes a coordination point. Phase 10's experience: discrepancies are best identified and fixed in the same plan because the identification *informs* the fix immediately. Splitting them adds overhead without reducing risk.

## Project Constraints (from CLAUDE.md / ANTIGRAVITY.md)

The project's `CLAUDE.md` is dataset/codebase oriented (Brutus, PINN, simulation pipeline) and is not directly relevant to this documentation phase. Two cross-cutting constraints apply:

1. **"LaTeX sources are the ground truth"** — D-16 already encodes this. No markdown edit may modify LaTeX source files.
2. **"Surgical changes — touch only what the task requires"** — Plan 02 must follow section-scoped edits (D-20). Do not reformat unrelated prose, rewrap lines, or normalize formatting in sections that already pass.
3. **"Mandatory: ALWAYS use Sequentialthinking MCP server"** (from user's global `~/.claude/CLAUDE.md`) — Treat as a per-session preference; not enforceable from a static research artifact, but plan executors should consider using sequential reasoning for multi-step verification tasks.

## Sources

### Primary (HIGH confidence)
- `pinn_instruction/original_latex/Data-quality-assessment/main-data-quality-assess.tex` — verified 6 sections imported, 0 imports of `bibliography.tex`
- `pinn_instruction/original_latex/Data-quality-assessment/sections/*.tex` — verified all 6 active sections, equation counts, label counts, citation counts (zero)
- `pinn_instruction/markdown_conversion/assess_data_quality.md` — line counts, heading hierarchy, `[?]` placeholder count (33), HTML table corruption verified by reading
- `pinn_instruction/markdown_conversion/pandoc_conversion/data_quality_assess.md` — line counts, heading hierarchy, `[@refN]` count (32), trailing reference list verified
- `pinn_instruction/markdown_conversion/verification_reports/ctl_instruction_verification_report.md` — Phase 10 report schema (read in full as canonical template)
- `pinn_instruction/markdown_conversion/_archive/ctl-instruction/README.md` — Phase 10 archive README schema
- `pinn_instruction/markdown_conversion/README.md` — index format (existing single-row table)
- `.planning/phases/10-ctl-instruction-verification/10-CONTEXT.md` and `10-0[123]-SUMMARY.md` — verified 3-plan cadence, decision IDs, requirements coverage

### Secondary (MEDIUM confidence)
- None — all sources are local file artifacts

### Tertiary (LOW confidence)
- None — research is deterministic on local files

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH — no libraries; tools are POSIX
- Architecture: HIGH — directly mirrors Phase 10's verified structure
- Pitfalls: HIGH — derived from direct inspection of both candidates and the LaTeX source
- Plan decomposition: HIGH — Phase 10 is a working, recent precedent for nearly-identical scope
- Validation Architecture: HIGH — assertions are deterministic shell checks against well-defined file states

**Research date:** 2026-05-05
**Valid until:** Indefinite — verifies a static set of files. Re-research only if the LaTeX source or candidate files change.

## RESEARCH COMPLETE
