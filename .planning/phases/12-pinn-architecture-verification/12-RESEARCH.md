# Phase 12: PINN-Architecture Verification - Research

**Researched:** 2026-05-05
**Domain:** Markdown conversion verification (LaTeX → Markdown fidelity with inactive section exclusion)
**Confidence:** HIGH

## Summary

Phase 12 verifies that the PINN-architecture markdown is an authoritative, one-to-one faithful reproduction of its 7 active LaTeX source sections, with all 3 inactive sections correctly excluded. Unlike Phase 10's `\begin{comment}...\end{comment}` exclusion mechanism, PINN-architecture uses `%\input` file-level exclusion (commented import statements in main_pinn.tex). This requires a hybrid verification approach: structural check that markdown section count matches 7 active imports, plus content search for distinctive inactive-section terms to confirm absence.

The source structure is: main_pinn.tex imports 7 active section files in explicit order (lines 12, 14, 18, 20, 22, 28, 30) and comments out 3 inactive imports (lines 16, 24, 26). The largest markdown candidate (pinn_architecture.md, 52885 bytes) may contain inactive-section leakage — a key sanity-check focus per D-34/D-38.

**Primary recommendation:** Follow the 3-plan wave pattern from Phase 10/11 exactly: Wave 1 (candidate selection with diff-scoring and human sanity-check focused on inactive content leakage), Wave 2 (section-by-section audit + fixes including bibliography verification since it IS imported unlike Phase 11), Wave 3 (archive unselected candidates, finalize report with explicit inactive exclusion confirmation).

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions
- **D-34:** Verify inactive section exclusion using a hybrid approach: (1) structural check that markdown section count/order matches the 7 active imports in main_pinn.tex, (2) content search for distinctive key terms from the 3 inactive files to confirm absence. The verification report explicitly lists the 3 inactive files and confirms each is absent.
- **D-35:** Inactive section content is NOT documented in the authoritative markdown's metadata section. The phase goal is exclusion verification, not content preservation.
- **D-36:** Authoritative filename: `pinn_instruction/markdown_conversion/pinn_architecture.md` (lowercase, underscores, matching Phase 10/11 convention).
- **D-37:** bibliography.tex IS in audit scope (unlike Phase 11's orphaned bibliography). It is imported by main_pinn.tex (line 30) and contains `\bibitem` entries that require full fidelity verification.
- **D-38:** The final verification report includes an explicit confirmation section: "Inactive Section Exclusion: All 3 inactive sections (input_vector_inactive.tex, advanced_training_inactive.tex, consolidated_blueprint_inactive.tex) are confirmed absent from the authoritative markdown."

### Claude's Discretion
- Exact diff-score implementation and normalization details (per D-04 constraints).
- Exact search terms used for inactive content verification (per D-34 hybrid approach).
- Exact verification report filename and structure within `verification_reports/`.
- Exact discrepancy ID format, as long as IDs remain stable and map from audit table to fix log.
- Which candidate wins mechanical diff scoring — determined by measurement, not preference.

### Deferred Ideas (OUT OF SCOPE)
- Documenting the content of the 3 inactive section files in the authoritative markdown's metadata.
- Fixing suspected source-level mathematical, factual, or methodological issues in PINN-architecture.
- Cross-document reconciliation between PINN-architecture and other instruction documents.
- Building shared automated markdown-verification tooling for all 6 documents.
- Auditing the 3 inactive section files for future reference.
</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| CAND-01 | Automated diff-score comparison selects best starting candidate | Established diff-scoring methodology from Phase 10/11; apply to 3 candidates with byte-size ordering noted for leakage correlation |
| AUDIT-01 | Section-by-section manual comparison of LaTeX against markdown | 7 active sections in known order; physics_constrained_loss.tex (15383 bytes) requires extra formula checklist time |
| AUDIT-02 | Every discrepancy documented with section location, type, severity | Established discrepancy table format from Phase 10/11 |
| AUDIT-03 | Comparison explicitly excludes `\begin{comment}...\end{comment}` blocks | PINN-architecture uses `%\input` file-level exclusion; hybrid approach per D-34 |
| FIDEL-01 | Every mathematical formula appears with accurate notation | physics_constrained_loss.tex and sqr_skipresnet_siren_backbone.tex are math-heavy; formula-by-formula checklist required |
| FIDEL-02 | All prose text, lists, code blocks, inline formatting match exactly | Standard prose verification per Phase 10/11 pattern |
| FIDEL-03 | All references preserved with correct target identifiers | bibliography.tex IS imported (D-37); all `\bibitem` entries require full audit |
| FIDEL-04 | All tables verified cell-by-cell | Source may contain tables in training_optimization_strategy.tex or other sections; verify if present |
| FIDEL-05 | Section hierarchy matches LaTeX source structure exactly | 7 active imports define canonical order; verify markdown section count/order |
| FIDEL-06 | Commented-out content absent from markdown | Hybrid inactive exclusion verification per D-34; 3 inactive files confirmed absent |
| CLEAN-01 | Each source has exactly one authoritative markdown file | Target: `pinn_instruction/markdown_conversion/pinn_architecture.md` per D-36 |
| CLEAN-02 | Unselected duplicate markdown files archived with README | 2 unselected candidates to `_archive/pinn-architecture/` with provenance README |
| CLEAN-03 | Verification report documents selection, discrepancies, fixes, zero-diff | Target: `verification_reports/pinn_architecture_verification_report.md` with D-38 explicit confirmation |
| CROSS-01 | Inter-document inconsistencies preserved in markdown | Source-level issues documented in metadata section, not corrected |
| CROSS-02 | 6 phases execute sequentially following same audit pattern | Phase 12 follows Phase 10/11 3-wave pattern exactly |
</phase_requirements>

## Architectural Responsibility Map

| Capability | Primary Tier | Secondary Tier | Rationale |
|------------|-------------|----------------|-----------|
| Markdown file comparison | Documentation | - | Pure file-system operations, no runtime components |
| Diff scoring computation | CLI/Shell | - | Bash/shell commands for token counting, F1/recall calculation |
| Inactive content search | CLI/Shell | - | grep for distinctive term search across candidates |
| Verification report writing | Documentation | - | Markdown report generation, file creation |
| Git archive operations | CLI/Shell | - | git mv for candidate promotion/archive |

**This phase is purely documentation tier:** No API, browser, database, or service dependencies. All work is file-system operations on markdown and LaTeX files.

## Standard Stack

### Core
| Tool/Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| git | any | File promotion, archive operations | Phase 10/11 established git-mv pattern for candidate handling |
| grep | any | Inactive content term search | D-34 hybrid approach requires content search for exclusion verification |
| wc | any | Byte-size comparison, token counting | Diff scoring methodology requires token/byte metrics |

### Supporting
| Tool/Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| diff | any | Line-by-line comparison | Manual inspection during section audit |
| head/tail | any | File segment inspection | Sampling candidate content during sanity-check |

### Alternatives Considered
| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| grep for inactive search | Python script with regex | Python more flexible but grep is sufficient for distinctive term search and faster |
| Manual diff scoring | Automated diff tool | Phase 10 established manual F1/recall scoring as user choice for v1.3 |

**Installation:**
No package installation required — uses standard shell utilities available on macOS.

**Version verification:**
```bash
# Verify standard tools available
git --version 2>/dev/null | head -1
grep --version 2>/dev/null | head -1
wc --version 2>/dev/null || echo "wc available (version varies by system)"
```

## Architecture Patterns

### System Architecture Diagram

```
                            Phase 12 Verification Flow
                            ==========================

Wave 1: Candidate Selection
┌──────────────────────────────────────────────────────────────────┐
│  LaTeX Source (7 active imports)                                  │
│  ↓                                                                │
│  main_pinn.tex → extract import order                             │
│  ↓                                                                │
│  3 Markdown Candidates                                            │
│  ├── pinn_architecture.md (52885 bytes) ───────────────────────┐ │
│  ├── pinn_architecture_v2.md (46355 bytes)                     │ │
│  └── PINN_architecture_plan.md (51268 bytes)                   │ │
│  ↓                                                             │ │
│  Diff Scoring (F1/recall per section)                          │ │
│  ↓                                                             │ │
│  Human Sanity-Check                                            │ │
│  ├── Check inactive content leakage ────────────────────────┐  │ │
│  ├── Check math formula fidelity                             │  │ │
│  ├── Check bibliography presence (D-37)                      │  │ │
│  └── Override if needed                                      │  │ │
│  ↓                                                           │  │ │
│  Select Baseline + Create Report Skeleton                    │  │ │
└─────────────────────────────────────────────────────────────┘──┘ │
                                                                    │
Wave 2: Section Audit + Fixes                                       │
┌─────────────────────────────────────────────────────────────┐    │
│  For each of 7 active sections (in source order):            │    │
│  ├── foundational_principles.tex                              │    │
│  ├── sqr_skipresnet_siren_backbone.tex (math-heavy)          │    │
│  ├── physics_constrained_loss.tex (largest, math-heavy)      │    │
│  ├── training_optimization_strategy.tex                       │    │
│  ├── inference_and_output.tex                                 │    │
│  ├── blueprint_summary.tex                                    │    │
│  └── bibliography.tex (imported, unlike Phase 11)            │    │
│  ↓                                                            │    │
│  Formula-by-formula checklist (especially physics loss)      │    │
│  ↓                                                            │    │
│  Discrepancy table (ID, type, severity, source/md loc)       │    │
│  ↓                                                            │    │
│  Apply markdown-only fixes                                    │    │
│  ↓                                                            │    │
│  Update fix log                                               │    │
└─────────────────────────────────────────────────────────────┘    │
                                                                    │
Wave 3: Archive + Verify                                            │
┌─────────────────────────────────────────────────────────────┐    │
│  Inactive Section Exclusion Verification (D-34/D-38)         │    │
│  ├── Structural: 7 sections in markdown = 7 active imports   │    │
│  └── Content search: distinctive terms from 3 inactive files │    │
│  ↓                                                            │    │
│  Append Source Issues metadata (if any found)                │    │
│  ↓                                                            │    │
│  Archive 2 unselected candidates → _archive/pinn-architecture/ │
│  ├── Create archive README with provenance                    │    │
│  └─────────────────────────────────────────────────────────────┘
│  ↓                                                            │
│  Update conversion index README                               │    │
│  ↓                                                            │    │
│  Finalize verification report                                 │    │
│  ├── Zero open discrepancies confirmed                        │    │
│  ├── D-38 explicit inactive exclusion confirmation            │    │
│  └── Complete fix log                                         │    │
└─────────────────────────────────────────────────────────────┘
```

### Recommended Project Structure (Phase 12 outputs)

```
pinn_instruction/markdown_conversion/
├── pinn_architecture.md                    # Authoritative markdown (D-36)
├── pinn_architecture_v2.md                 # Candidate (archived in Wave 3)
├── verification_reports/
│   └── pinn_architecture_verification_report.md  # Full audit + fixes + exclusion confirmation
├── pandoc_conversion/
│   └── PINN_architecture_plan.md           # Candidate (archived in Wave 3)
├── _archive/
│   └── pinn-architecture/
│       ├── README.md                        # Provenance document
│       ├── [unselected_candidate_1].md     # Moved in Wave 3
│       └── [unselected_candidate_2].md     # Moved in Wave 3
└── README.md                                # Conversion index (Phase 12 row added)

pinn_instruction/original_latex/pinn-architecture/
├── main_pinn.tex                           # Source entry point (7 active + 3 commented imports)
├── preamble.tex                            # Macros (reference only)
└── sections/
    ├── foundational_principles.tex         # Active section 1
    ├── sqr_skipresnet_siren_backbone.tex   # Active section 2 (math-heavy)
    ├── input_vector_inactive.tex           # Inactive (commented import)
    ├── physics_constrained_loss.tex        # Active section 3 (largest, math-heavy)
    ├── training_optimization_strategy.tex  # Active section 4
    ├── advanced_training_inactive.tex      # Inactive (commented import)
    ├── inference_and_output.tex            # Active section 5
    ├── consolidated_blueprint_inactive.tex # Inactive (commented import)
    ├── blueprint_summary.tex               # Active section 6
    └── bibliography.tex                    # Active section 7 (imported, D-37)
```

### Pattern 1: Three-Wave Execution (from Phase 10/11)

**What:** Execute Phase 12 as 3 sequential plans: Wave 1 (candidate selection), Wave 2 (audit+fix), Wave 3 (archive+verify). Each wave depends on prior wave completion.

**When to use:** All Phase 12 work follows this pattern — it's the established v1.3 execution model.

**Example (Wave 1 structure from Phase 10):**
```
Wave 1 Plan Tasks:
1. Score all 3 candidates with normalized diff (F1/recall per section)
2. Human sanity-check top-ranked candidate (special focus on inactive content leakage)
3. Select baseline, create report skeleton with:
   - Candidate comparison table
   - Selected baseline rationale
   - Excluded inactive files list (for D-34/D-38)
   - Section audit placeholders
   - Fix log placeholder
   - Source Issues placeholder
```

### Pattern 2: Hybrid Inactive Exclusion Verification (D-34)

**What:** Two-step verification that inactive sections are absent from markdown.

**When to use:** Required for all PINN-architecture candidates during Wave 1 sanity-check and Wave 3 final verification.

**Example:**
```markdown
## Inactive Section Exclusion Verification (D-34)

### Structural Check
- Markdown section count: X sections
- Expected active imports: 7
- Match: YES/NO

### Content Search
| Inactive file | Search term | Found in markdown? | Status |
|---------------|-------------|--------------------|--------|
| input_vector_inactive.tex | "Input Vector Formulation" | NO | PASS |
| input_vector_inactive.tex | "14-dimensional injective" | NO | PASS |
| advanced_training_inactive.tex | "Adaptive Loss Balancing via ALM" | NO | PASS |
| advanced_training_inactive.tex | "training_hyperparameters" | NO | PASS |
| consolidated_blueprint_inactive.tex | "Consolidated Implementation Blueprint" | NO | PASS |
| consolidated_blueprint_inactive.tex | "Final Recommendations" | NO | PASS |

### D-38 Explicit Confirmation
All 3 inactive sections (input_vector_inactive.tex, advanced_training_inactive.tex, consolidated_blueprint_inactive.tex) are confirmed absent from the authoritative markdown.
```

### Anti-Patterns to Avoid

- **Size-based candidate selection:** Largest candidate (52885 bytes) may contain inactive content leakage. Do NOT select based on size alone — diff scoring and human sanity-check required.
- **Skipping bibliography audit:** Unlike Phase 11 where bibliography.tex was orphaned, Phase 12's bibliography IS imported (main_pinn.tex line 30) and requires full `\bibitem` audit.
- **Assuming `%\input` exclusion is automatic:** Commented imports in LaTeX do not guarantee absence in markdown conversions — pandoc may have processed the full sections/ directory. MUST verify with content search.

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Diff scoring algorithm | Custom F1/recall Python script | Phase 10 methodology (tokenization, whitespace normalization, bag-of-words) | Phase 10 established working approach; reuse reduces risk |
| Inactive exclusion report | New D-38 confirmation format | D-38 text verbatim from CONTEXT.md | Locked decision requires exact wording |
| Verification report structure | New section ordering | Phase 10/11 report template (Candidate Comparison → Selected Baseline → Excluded Comment Ranges → Section Audit → Fix Log → Source Issues → Final Verification) | Established pattern provides complete coverage |
| Archive README | Custom provenance format | Phase 10 `_archive/ctl-instruction/README.md` template | Established provenance documentation |

**Key insight:** Phase 12 has no novel verification challenges — all patterns established in Phase 10 (diff scoring, audit workflow, fix log, archive structure) and Phase 11 (verification_reports/ directory, index update). The only new element is the hybrid inactive exclusion verification (D-34), which is fully specified in locked decisions.

## Runtime State Inventory

> Not applicable — Phase 12 is pure documentation verification with no runtime services, databases, or live configuration.

| Category | Items Found | Action Required |
|----------|-------------|------------------|
| Stored data | None — no databases or datastores involved in this phase | None |
| Live service config | None — no external services with UI config | None |
| OS-registered state | None — no systemd/launchd/pm2 tasks | None |
| Secrets/env vars | None — no credentials or environment dependencies | None |
| Build artifacts | None — documentation-only phase | None |

**Phase scope:** Documentation file operations only. No runtime state categories apply.

## Common Pitfalls

### Pitfall 1: Inactive Content Leakage in Largest Candidate

**What goes wrong:** The largest candidate (pinn_architecture.md, 52885 bytes) may contain content from the 3 inactive sections if the converter processed the full sections/ directory without respecting `%\input` comments. This creates a fidelity mismatch that diff scoring may penalize, but human sanity-check MUST explicitly search for inactive terms.

**Why it happens:** pandoc conversions often process directory contents without parsing LaTeX import directives. The `%\input` comment pattern is source-level exclusion that may not translate to automated conversions.

**How to avoid:**
1. During Wave 1 sanity-check, grep for distinctive inactive-section terms:
   - `input_vector_inactive.tex`: "Input Vector Formulation", "14-dimensional injective input vector", "non-injective", "Scaling the Training Data", "Characteristic Time", "Characteristic Length"
   - `advanced_training_inactive.tex`: "Advanced Training Dynamics", "Adaptive Loss Balancing via ALM", "Curriculum-Aware Energy Regularization", "Two-Phase Optimization", "Stabilizing Training with Adaptive Gradient Clipping", "training_hyperparameters"
   - `consolidated_blueprint_inactive.tex`: "Consolidated Implementation Blueprint", "Unified View of the Architecture", "Integration with the CTL Framework", "Final Recommendations"
2. If any term found, record as BLOCKING discrepancy in candidate comparison
3. Prefer smaller candidate if leakage confirmed

**Warning signs:** Candidate byte-size significantly larger than expected for 7 sections only; section headings in markdown that don't match the 7 active import names.

### Pitfall 2: Bibliography Omission (assuming Phase 11 pattern)

**What goes wrong:** Planner/executor assumes bibliography.tex is orphaned like Phase 11 and skips its audit, creating an incomplete verification.

**Why it happens:** Phase 11's bibliography.tex was never imported by main-data-quality-assess.tex. Phase 12's bibliography.tex IS imported (main_pinn.tex line 30). The difference is critical.

**How to avoid:**
1. Read main_pinn.tex and confirm bibliography import at line 30
2. Include bibliography.tex as Section 7 in audit plan
3. Verify all `\bibitem` entries match markdown reference section

**Warning signs:** Verification report missing bibliography audit section; markdown missing reference/bibliography content.

### Pitfall 3: Math Formula Corruption in physics_constrained_loss.tex

**What goes wrong:** The largest section (physics_constrained_loss.tex, 15383 bytes) contains complex loss-function formulas, ALM update rules, and code listings. Formula corruption (missing terms, altered symbols, whitespace in math) is high-risk.

**Why it happens:** LaTeX math notation is complex; markdown conversions may introduce rendering artifacts, split inline math across lines, or corrupt `$$` delimiters.

**How to avoid:**
1. Allocate extra formula-by-formula checklist time for this section
2. Compare each formula term-by-term against source
3. Verify code listings preserve indentation and syntax

**Warning signs:** Display formulas rendering with syntax errors; code listings with broken indentation.

### Pitfall 4: Assuming Section Count Matches Imports Without Counting

**What goes wrong:** Executor assumes markdown has 7 sections without counting, then finds mismatch during Wave 3 verification.

**Why it happens:** Candidate may have merged sections, split sections, or added inactive content sections. Structural check (D-34 part 1) must be explicit.

**How to avoid:**
1. Count `#` headings in markdown during Wave 1 sanity-check
2. Compare against 7 active imports in main_pinn.tex
3. Document section count in candidate comparison report

**Warning signs:** Markdown heading count > 7 (suggests inactive content present); heading count < 7 (suggests merged sections).

## Code Examples

Verified patterns from Phase 10/11 execution:

### Inactive Content Search (grep pattern)
```bash
# Search distinctive terms from inactive files in each candidate
for candidate in pinn_architecture.md pinn_architecture_v2.md pandoc_conversion/PINN_architecture_plan.md; do
  echo "=== $candidate ==="
  grep -c "Input Vector Formulation" "$candidate" || echo "0"
  grep -c "Advanced Training Dynamics" "$candidate" || echo "0"
  grep -c "Consolidated Implementation Blueprint" "$candidate" || echo "0"
done
```

### Candidate Byte-Size Comparison
```bash
# Candidate sizes (already known from ls -la)
wc -c pinn_instruction/markdown_conversion/pinn_architecture.md
wc -c pinn_instruction/markdown_conversion/pinn_architecture_v2.md
wc -c pinn_instruction/markdown_conversion/pandoc_conversion/PINN_architecture_plan.md
```

### Section Import Order Extraction (from main_pinn.tex)
```bash
# Extract active imports from main_pinn.tex (lines without leading %)
grep -v "^%" pinn_instruction/original_latex/pinn-architecture/main_pinn.tex | grep "\\\\input{sections"
```
Expected output (7 lines):
```
\input{sections/foundational_principles}
\input{sections/sqr_skipresnet_siren_backbone}
\input{sections/physics_constrained_loss}
\input{sections/training_optimization_strategy}
\input{sections/inference_and_output}
\input{sections/blueprint_summary}
\input{sections/bibliography}
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| Manual candidate inspection without scoring | Diff-score ranking with F1/recall metrics | Phase 10 (v1.3) | Objective selection reduces human bias |
| Assumed `\begin{comment}` exclusion only | Hybrid structural + content search for `%\input` exclusion | Phase 12 (D-34) | Handles file-level exclusion mechanism correctly |
| Bibliography audit optional | Bibliography audit required when imported (D-37) | Phase 12 | Ensures complete verification for active imports |

**Deprecated/outdated:**
- Selecting candidate by byte-size alone (inactive content may inflate size)
- Skipping bibliography verification (Phase 11 pattern does not apply when bibliography IS imported)

## Assumptions Log

> All claims in this research are verified from source files or CONTEXT.md. No [ASSUMED] tags required.

| # | Claim | Section | Risk if Wrong |
|---|-------|---------|---------------|
| — | All claims verified from file reads or locked decisions | — | None |

**If this table is empty:** All claims in this research were verified or cited — no user confirmation needed.

## Open Questions

1. **Exact diff scoring normalization details**
   - What we know: D-04 specifies normalization of whitespace, line wrapping, harmless escaping; no normalization of content/math/table/reference changes
   - What's unclear: Exact tokenization method (whitespace-split confirmed in Phase 10/11)
   - Recommendation: Reuse Phase 10 methodology exactly — bag-of-words with multiplicity, whitespace-split on stripped lowercased text

2. **Which candidate wins mechanical scoring**
   - What we know: 3 candidates exist with sizes 52885, 46355, 51268 bytes; largest may have inactive content leakage
   - What's unclear: Exact F1/recall scores until computed
   - Recommendation: Compute during Wave 1; human sanity-check specifically for inactive terms before finalizing selection

## Environment Availability

> Skip this section — Phase 12 has no external dependencies beyond standard shell tools.

| Dependency | Required By | Available | Version | Fallback |
|------------|------------|-----------|---------|----------|
| git | Candidate promotion/archive | ✓ | any | — |
| grep | Inactive content search | ✓ | any | — |
| wc | Byte-size/token counting | ✓ | any | — |

**Missing dependencies with no fallback:** None — all required tools are standard shell utilities available on macOS.

**Missing dependencies with fallback:** None.

## Validation Architecture

> `workflow.nyquist_validation` is true in config.json — include this section.

### Test Framework
| Property | Value |
|----------|-------|
| Framework | None — documentation verification phase |
| Config file | None |
| Quick run command | N/A |
| Full suite command | N/A |

**Note:** Phase 12 is documentation verification with no automated tests. Validation is human inspection of diff reports and verification reports.

### Phase Requirements → Verification Map
| Req ID | Behavior | Verification Method | File Exists? |
|--------|----------|---------------------|-------------|
| CAND-01 | Diff-score candidate comparison | Human inspection of comparison report | Wave 1 creates |
| AUDIT-01 | Section-by-section comparison | Human inspection of audit tables | Wave 2 creates |
| AUDIT-02 | Discrepancy documentation | Human inspection of discrepancy tables | Wave 2 creates |
| AUDIT-03 | Comment block exclusion | Hybrid structural + content search (D-34) | Wave 1 sanity-check, Wave 3 confirm |
| FIDEL-01 | Formula accuracy | Formula-by-formula checklist in audit tables | Wave 2 creates |
| FIDEL-02 | Prose fidelity | Line-by-line comparison in audit tables | Wave 2 creates |
| FIDEL-03 | Reference fidelity | Bibliography entry comparison | Wave 2 creates |
| FIDEL-04 | Table cell verification | Cell-by-cell comparison if tables present | Wave 2 creates |
| FIDEL-05 | Section hierarchy | Heading count/order verification | Wave 1 sanity-check |
| FIDEL-06 | Inactive content absence | D-34 hybrid verification, D-38 explicit confirmation | Wave 3 confirms |
| CLEAN-01 | Single authoritative file | File existence check at target path | Wave 3 verifies |
| CLEAN-02 | Archive with provenance | Archive directory + README existence | Wave 3 creates |
| CLEAN-03 | Complete verification report | Report structure check against template | Wave 3 finalizes |
| CROSS-01 | Inter-doc inconsistencies preserved | Source Issues metadata section (if needed) | Wave 3 appends |
| CROSS-02 | Sequential phase execution | Phase dependency order | Planner enforces |

### Sampling Rate
- **Per task commit:** Human inspection of task output before commit
- **Per wave merge:** Full wave review before proceeding to next wave
- **Phase gate:** Zero open discrepancies, D-38 confirmation complete, index updated

### Wave 0 Gaps
- [ ] None — documentation verification requires no test infrastructure

*(No test infrastructure needed — all validation is human inspection of verification reports)*

## Security Domain

> `security_enforcement` absent in config.json — omit this section as documentation verification phase has no security implications.

Phase 12 involves no user input, network access, database queries, authentication, or cryptographic operations. Security domain not applicable.

## Sources

### Primary (HIGH confidence)
- `.planning/phases/12-pinn-architecture-verification/12-CONTEXT.md` - All locked decisions (D-34, D-35, D-36, D-37, D-38) and phase boundary
- `pinn_instruction/original_latex/pinn-architecture/main_pinn.tex` - Verified 7 active imports at lines 12,14,18,20,22,28,30 and 3 commented imports at lines 16,24,26
- `pinn_instruction/original_latex/pinn-architecture/sections/*.tex` - Verified all 10 section files exist, 7 active + 3 inactive
- `.planning/REQUIREMENTS.md` - All 15 Phase 12 requirements (CAND-01 through CROSS-02)

### Secondary (MEDIUM confidence)
- `.planning/phases/10-ctl-instruction-verification/10-01-SUMMARY.md` - Established 3-wave pattern, diff scoring methodology
- `.planning/phases/11-data-quality-assessment-verification/11-03-SUMMARY.md` - Archive structure, index update pattern
- `pinn_instruction/markdown_conversion/verification_reports/ctl_instruction_verification_report.md` - Report template structure
- `pinn_instruction/markdown_conversion/verification_reports/data_quality_assessment_verification_report.md` - Report template structure

### Tertiary (LOW confidence)
- Candidate byte-sizes (wc -c output) — verified but actual diff scores pending Wave 1 computation

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH — shell tools verified available, Phase 10/11 patterns established
- Architecture: HIGH — source structure verified (main_pinn.tex read), candidate locations verified
- Pitfalls: HIGH — inactive files read, distinctive terms identified; bibliography import verified

**Research date:** 2026-05-05
**Valid until:** 30 days — source files and decisions stable for milestone duration