---
phase: 11
slug: data-quality-assessment-verification
status: draft
nyquist_compliant: false
wave_0_complete: false
created: 2026-05-05
---

# Phase 11 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

This phase produces documentation artifacts (a verification report, an authoritative markdown file, and an archive). Validation is therefore a series of **deterministic shell-checkable assertions** rather than executable tests. There is no test framework — every requirement maps to a grep/file-existence assertion.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | Shell-based deterministic assertions (grep / wc / file existence) |
| **Config file** | None — assertions live inline in each plan's tasks |
| **Quick run command** | Inline `grep`/`test` against artifact paths (see Per-Task Verification Map) |
| **Full suite command** | `bash` execution of the assertion blocks compiled from this file |
| **Estimated runtime** | < 1 second |

---

## Sampling Rate

- **After every task commit:** Run citation-stripping + table + heading-hierarchy assertions for the touched section (≤10 grep calls, < 1 sec).
- **After every plan wave:** Run the full Phase Requirements assertion table below (~30 grep calls, ~1 sec).
- **Before `/gsd-verify-work`:** All assertions green AND a manual side-by-side reading of the 6 sections (the human verification step).
- **Max feedback latency:** ~1 second.

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Threat Ref | Secure Behavior | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|------------|-----------------|-----------|-------------------|-------------|--------|
| 11-01-01 | 01 | 1 | CAND-01 | — | N/A | grep | `grep -A2 "Candidate Comparison" pinn_instruction/markdown_conversion/verification_reports/data_quality_assessment_verification_report.md \| grep -E "score\|rank"` | ❌ W0 (Plan 01 creates) | ⬜ pending |
| 11-01-02 | 01 | 1 | CAND-01 | — | N/A | manual | Human structural sanity-check; document override or confirmation | ❌ W0 | ⬜ pending |
| 11-01-03 | 01 | 1 | AUDIT-03 | — | N/A | grep | `grep -A3 "Excluded Comment Ranges" pinn_instruction/markdown_conversion/verification_reports/data_quality_assessment_verification_report.md` | ❌ W0 | ⬜ pending |
| 11-02-01 | 02 | 2 | AUDIT-01, FIDEL-01, FIDEL-04, FIDEL-05 | — | N/A | grep+manual | Per-section subsection + discrepancy table for sections 1–3 | ❌ W0 | ⬜ pending |
| 11-02-02 | 02 | 2 | AUDIT-02, FIDEL-02, FIDEL-03, FIDEL-06, CROSS-01 | — | N/A | grep+manual | Per-section subsection + citation strip + table rebuild for sections 4–6 | ❌ W0 | ⬜ pending |
| 11-03-01 | 03 | 3 | CROSS-01, CLEAN-03 | — | N/A | grep | `grep -qF "Source Issues / Notes for Future Reconciliation" pinn_instruction/markdown_conversion/data_quality_assessment.md` | ❌ W0 | ⬜ pending |
| 11-03-02 | 03 | 3 | CLEAN-01, CLEAN-02 | — | N/A | file | `[ -f pinn_instruction/markdown_conversion/data_quality_assessment.md ] && [ -f pinn_instruction/markdown_conversion/_archive/data-quality-assessment/README.md ]` | ❌ W0 | ⬜ pending |
| 11-03-03 | 03 | 3 | CROSS-02, CLEAN-03 | — | N/A | grep | `grep -qF "Open discrepancies: 0" pinn_instruction/markdown_conversion/verification_reports/data_quality_assessment_verification_report.md` | ❌ W0 | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Phase Requirements → Assertions

Compiled from `11-RESEARCH.md` §Validation Architecture. The plan executor and verifier MUST run these.

| REQ ID | Behavior | Automated Command | Expected |
|--------|----------|-------------------|----------|
| CAND-01 | Verification report contains candidate ranking (overall + per-section) | `grep -A2 "Candidate Comparison" .../verification_reports/data_quality_assessment_verification_report.md \| grep -E "score\|rank"` | ≥1 match |
| AUDIT-01 | Section audit subsections present for all 6 active sections | `for s in introduction assessment_strategy data_quality_metrics model_parameter_risks implementation_protocol synthesis_conclusion; do grep -q "### $s.tex" .../verification_reports/data_quality_assessment_verification_report.md \|\| echo "MISSING $s"; done` | (no MISSING output) |
| AUDIT-02 | Each section has discrepancy table | `grep -cE "^\| ID \| Type \| Severity \|" .../verification_reports/data_quality_assessment_verification_report.md` | ≥6 |
| AUDIT-03 | Comment-environment ranges enumerated or "None" stated | `grep -A3 "Excluded Comment Ranges" .../verification_reports/data_quality_assessment_verification_report.md` | text containing "None" |
| FIDEL-01 | All 6 displayed equations present in authoritative markdown | `grep -cE '^\$\$\|^\\\\[' pinn_instruction/markdown_conversion/data_quality_assessment.md` | ≥6 |
| FIDEL-02 | First and last sentences of each LaTeX section appear in markdown | manual section read + targeted `grep -qF "<exact phrase>"` | match per section |
| FIDEL-03 | `\label{tab:assessment_strategies}` preserved as visible text/anchor | `grep -qF "tab:assessment_strategies" pinn_instruction/markdown_conversion/data_quality_assessment.md` | match |
| FIDEL-04 | Table contains all 5 row labels and 3 strategy columns | `for r in "Primary Metric" "Computational Cost" "Detects" "Risk Addressed" "Blind Spot"; do grep -qF "$r" .../data_quality_assessment.md \|\| echo "MISSING $r"; done` | (no MISSING) |
| FIDEL-05 | Top-level heading count matches `\section` count (6) | `grep -cE "^# [^#]" pinn_instruction/markdown_conversion/data_quality_assessment.md` | ≥6 |
| FIDEL-06 | Zero comment-block content leaked (vacuous — source has none) | `! grep -F "% \begin{comment}" pinn_instruction/markdown_conversion/data_quality_assessment.md && ! grep -F "\authcomment" pinn_instruction/markdown_conversion/data_quality_assessment.md` | both absent |
| CLEAN-01 | Authoritative file exists; unselected does not at original path | `[ -f pinn_instruction/markdown_conversion/data_quality_assessment.md ] && [ ! -f <original-unselected> ]` | both true |
| CLEAN-02 | Archive README + unselected file present in archive dir | `[ -f pinn_instruction/markdown_conversion/_archive/data-quality-assessment/README.md ] && ls pinn_instruction/markdown_conversion/_archive/data-quality-assessment/*.md \| grep -v README \| head -1` | both present |
| CLEAN-03 | Verification report has selection, audits, fix log, zero-diff | `for s in "## Selected Baseline" "## Section Audit" "## Fix Log" "Open discrepancies: 0"; do grep -qF "$s" .../verification_reports/data_quality_assessment_verification_report.md \|\| echo "MISSING $s"; done` | (no MISSING) |
| CROSS-01 | Source-issues section present (with notes or "(none)") | `grep -qF "Source Issues / Notes for Future Reconciliation" pinn_instruction/markdown_conversion/data_quality_assessment.md` | match |
| CROSS-02 | Phase has 3 plans matching audit→fix→verify cycle | `ls .planning/phases/11-data-quality-assessment-verification/11-0[123]-PLAN.md \| wc -l` | 3 |

---

## Citation-Stripping Validation (NEW for Phase 11)

These assertions are unique to Phase 11 (no Phase 10 analog). They MUST run after Plan 02:

| Assertion | Command | Expected |
|-----------|---------|----------|
| Zero pandoc-style citations remain | `grep -cE '\[@ref[0-9]+\]' pinn_instruction/markdown_conversion/data_quality_assessment.md` | `0` |
| Zero placeholder citations remain | `grep -cF '[?]' pinn_instruction/markdown_conversion/data_quality_assessment.md` | `0` |
| No reference list heading | `! grep -qE '^# References$\|^## References$' pinn_instruction/markdown_conversion/data_quality_assessment.md` | exit 0 |
| No orphan `99` token (pandoc bibliography header artifact) | `! grep -qE '^99$' pinn_instruction/markdown_conversion/data_quality_assessment.md` | exit 0 |
| File ends within content (or with appended Source Issues section) | `tail -1 pinn_instruction/markdown_conversion/data_quality_assessment.md` | non-empty |

---

## Table Validation (NEW for Phase 11)

| Assertion | Command | Expected |
|-----------|---------|----------|
| No HTML `<table>` markup remains | `grep -cE '<table\|<tr\|<td' pinn_instruction/markdown_conversion/data_quality_assessment.md` | `0` |
| GFM table separator row present | `grep -cE '^\\|.*-+.*\\|' pinn_instruction/markdown_conversion/data_quality_assessment.md` | `≥1` |
| All 5 row labels present | `for r in "Primary Metric" "Computational Cost" "Detects" "Risk Addressed" "Blind Spot"; do grep -qF "$r" .../data_quality_assessment.md \|\| echo "MISSING: $r"; done` | (no MISSING) |
| All 3 column headers present | `for c in "Pre-Training Validation" "Trial Training" "Staged Gate Protocol"; do grep -qF "$c" .../data_quality_assessment.md \|\| echo "MISSING: $c"; done` | (no MISSING) |
| No cell-merge corruption | `! grep -qE 'Risk Addressed[ \\|]+Blind Spot' pinn_instruction/markdown_conversion/data_quality_assessment.md` | exit 0 |

---

## Math Formula Validation (FIDEL-01 supplement)

The 6 displayed equations expected (per `\begin{equation}` count in source):

| # | Source location | Content signature | grep assertion |
|---|----------------|-------------------|----------------|
| 1 | `introduction.tex:20-22` | Causal weighted loss | `grep -qE 'sum_\{i=1\}\^\{N_t\}' data_quality_assessment.md` |
| 2 | `data_quality_metrics.tex:11-13` | Hamiltonian | `grep -qF 'G m_i m_j' data_quality_assessment.md` |
| 3 | `data_quality_metrics.tex:18-20` | SCS metric | `grep -qE 'SCS *= *\\\\?log_\{10\}' data_quality_assessment.md` |
| 4 | `data_quality_metrics.tex:40-42` | SASD ratio | `grep -qE 'SASD_i *= *\\\\frac\{\\\\Delta t_i\}' data_quality_assessment.md` |
| 5 | `data_quality_metrics.tex:63-65` | IPR formula | `grep -qE 'IPR *= *\\\\frac\{1\}\{M\}' data_quality_assessment.md` |
| 6 | `data_quality_metrics.tex:77-79` | Shannon entropy | `grep -qE 'H_\{data\} *= *-' data_quality_assessment.md` |

Plan 02 may adjust whitespace/formatting in regexes to match the chosen candidate's conventions.

---

## Wave 0 Requirements

- [ ] `pinn_instruction/markdown_conversion/data_quality_assessment.md` — does not exist; Plan 03 creates by promotion via `git mv`.
- [ ] `pinn_instruction/markdown_conversion/verification_reports/data_quality_assessment_verification_report.md` — does not exist; Plan 01 creates skeleton.
- [ ] `pinn_instruction/markdown_conversion/_archive/data-quality-assessment/README.md` — does not exist; Plan 03 creates.
- [ ] `pinn_instruction/markdown_conversion/_archive/data-quality-assessment/<unselected>.md` — does not exist; Plan 03 creates by `git mv`.
- [ ] Updated `pinn_instruction/markdown_conversion/README.md` index with Phase 11 row — Plan 03 modifies.

*No new test infrastructure required — all assertions are inline shell.*

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| Section content fidelity (math, prose, table) reads as one-to-one with LaTeX source | FIDEL-01 .. FIDEL-06 | Visual rendering equivalence cannot be assured by pure shell | Open `pinn_instruction/markdown_conversion/data_quality_assessment.md` in a markdown previewer and the LaTeX source side-by-side; walk all 6 sections in source order. |
| Selected candidate human sanity-check overrides raw diff score (D-02) | CAND-01 | Inherently subjective | Inspect heading hierarchy, table format, math display continuity in both candidates before finalizing the selection. |

---

## Validation Sign-Off

- [ ] All tasks have automated verify or Wave 0 dependencies
- [ ] Sampling continuity: no 3 consecutive tasks without automated verify
- [ ] Wave 0 covers all MISSING references (5 file artifacts, all created in Plans 01 + 03)
- [ ] No watch-mode flags
- [ ] Feedback latency < 2s
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
